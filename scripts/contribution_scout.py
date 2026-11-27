#!/usr/bin/env python3
"""Read-only repository inventory and strict contribution portfolio validation.

Only 'inventory' writes (--output); 'validate' reads and returns a status code.
No project scripts/dependency commands are executed. Standard library only.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys

SCHEMA = 'aidw/contribution-portfolio/v1'
CATEGORIES = ('existing-functionality','new-functionality','bug-fix','performance',
              'reliability','security','testing','documentation','developer-experience',
              'architecture','accessibility','interoperability')
EXCLUDED_DIRS = {'node_modules','.git','.cache','.venv','venv','vendor','dist','build','coverage',
                 '__pycache__','.next','target','.gradle','.turbo'}
LANGUAGES = {'.py':'Python','.js':'JavaScript','.jsx':'JavaScript','.ts':'TypeScript',
             '.tsx':'TypeScript','.go':'Go','.rs':'Rust','.php':'PHP','.java':'Java',
             '.kt':'Kotlin','.swift':'Swift','.cs':'C#','.rb':'Ruby','.cpp':'C++',
             '.c':'C','.h':'C/C++','.html':'HTML','.css':'CSS','.vue':'Vue',
             '.svelte':'Svelte','.sh':'Shell','.md':'Markdown','.yml':'YAML',
             '.yaml':'YAML','.json':'JSON','.toml':'TOML'}

def git(repo: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True,
                                text=True, errors='replace', timeout=12, check=False)
    except (OSError,subprocess.TimeoutExpired): return None
    return result.stdout.strip() if result.returncode == 0 else None

def candidate_paths(repo: Path):
    # Path enumeration only. Never read file content, follow links, or traverse ignored vendor trees.
    r = subprocess.run(['git','-C',str(repo),'ls-files','-z'], capture_output=True,
                       timeout=30, check=False)
    if r.returncode == 0:
        return [p.decode('utf-8',errors='replace') for p in r.stdout.split(b'\0') if p], 'git-tracked'
    paths = []
    for base, dirs, files in os.walk(repo, topdown=True, followlinks=False):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not (Path(base)/d).is_symlink()]
        for name in files:
            entry = Path(base)/name
            if not entry.is_symlink() and entry.is_file():
                paths.append(entry.relative_to(repo).as_posix())
    return paths, 'filesystem-fallback'

def inventory(repo: Path) -> dict:
    repo = repo.expanduser().resolve(strict=True)
    if not repo.is_dir(): raise ValueError('Repository path is not a directory')
    paths, method = candidate_paths(repo)
    paths = [p.replace('\\','/') for p in paths]
    excluded = [p for p in paths if (set(PurePosixPath(p).parts) & EXCLUDED_DIRS)]
    maintained = [p for p in paths if p not in excluded]
    lang = Counter(LANGUAGES.get(Path(p).suffix.lower(),'Other') for p in maintained)
    areas = Counter(PurePosixPath(p).parts[0] if len(PurePosixPath(p).parts)>1 else '(root)' for p in maintained)
    docs = [p for p in maintained if PurePosixPath(p).name.upper() in ('README.MD','CONTRIBUTING.MD',
           'CODE_OF_CONDUCT.MD','SECURITY.MD','GOVERNANCE.MD','AGENTS.MD','CLAUDE.MD','CODEOWNERS',
           'LICENSE','LICENSE.MD') or p.startswith('.github/')]
    tests = [p for p in maintained if 'test' in PurePosixPath(p).name.lower() or
             any(i in {'test','tests','spec','specs','__tests__'} for i in PurePosixPath(p).parts)]
    status = git(repo,'status','--porcelain=v1','-uno')
    sha = git(repo,'rev-parse','HEAD')
    data = {
       'schema':'aidw/repository-inventory/v1', 'generatedAt':datetime.now(timezone.utc).isoformat(),
       'root':str(repo),'method':method,'head':sha or 'unknown','branch':git(repo,'branch','--show-current') or '(detached/non-git)',
       'dirty':bool(status) if status is not None else None,
       'totalListed':len(paths),'maintainedFileCount':len(maintained),'excludedCount':len(excluded),
       'excludedExamples':excluded[:40], 'languageCounts':dict(lang.most_common()),
       'subsystemCounts':dict(areas.most_common()), 'governanceAndCiFiles':docs[:200],
       'testFilesSample':tests[:100], 'maintainedFiles':maintained,
       'limits':['Inventory enumerates paths; it does not mean every file was semantically inspected.',
                 'Generated and vendored content excluded from maintained-source review.',
                 'GitHub issue/PR status must be checked separately.']
    }
    return data

def valid_repo_path(repo: Path, value: str) -> bool:
    if not isinstance(value,str) or not value or '\\' in value: return False
    p=PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or '.' == value: return False
    q=repo.joinpath(*p.parts)
    # Resolve symlinks and reject path escaping the root.
    try: return q.resolve(strict=False).is_relative_to(repo) and q.exists() and q.is_file()
    except (OSError,RuntimeError): return False

def validate(portfolio: dict, repo: Path) -> list[str]:
    errors=[]
    if not isinstance(portfolio,dict):return ['Root must be JSON object']
    if portfolio.get('schema')!=SCHEMA:errors.append('Invalid schema')
    r=portfolio.get('repository')
    if not isinstance(r,dict) or not isinstance(r.get('head'),str) or not r['head']:
        errors.append('repository.head is required')
    elif r['head'] not in {'unknown'} and (actual_head := git(repo,'rev-parse','HEAD')) and r['head'] != actual_head:
        errors.append('repository.head differs from current checked-out HEAD; reassess before approval')
    if isinstance(r,dict) and r.get('root') != str(repo):
        errors.append('repository.root must match the validated repository')
    inspect=portfolio.get('inspection')
    if not isinstance(inspect,dict):errors.append('inspection required');inspect={}
    for key in ('trackedFiles','inspectedFiles','excludedFiles'):
        if type(inspect.get(key)) is not int or inspect[key]<0:errors.append(f'inspection.{key} non-negative integer required')
    listed, method = candidate_paths(repo)
    if method == 'git-tracked' and isinstance(inspect.get('trackedFiles'),int) and inspect['trackedFiles'] != len(listed):
        errors.append('inspection.trackedFiles differs from git tracked-file inventory')
    if isinstance(inspect.get('trackedFiles'),int) and isinstance(inspect.get('inspectedFiles'),int) and inspect['inspectedFiles']>inspect['trackedFiles']:
        errors.append('inspectedFiles cannot exceed trackedFiles')
    if not isinstance(inspect.get('coverageNotes'),str) or not inspect['coverageNotes'].strip():errors.append('inspection.coverageNotes required')
    if type(inspect.get('githubChecked')) is not bool:errors.append('inspection.githubChecked boolean required')
    if inspect.get('githubChecked') and not inspect.get('githubCheckedAt'):errors.append('inspection.githubCheckedAt required when checked')
    categories=portfolio.get('categories',[])
    if not isinstance(categories,list):categories=[];errors.append('categories array required')
    cat_index={}
    for c in categories:
        if not isinstance(c,dict) or c.get('id') not in CATEGORIES or c.get('id') in cat_index:
            errors.append('Invalid or repeated category');continue
        if c.get('status') not in {'covered','insufficient-evidence','not-applicable'}:errors.append('Invalid category status '+c['id'])
        if not isinstance(c.get('explanation'),str) or not c['explanation'].strip():errors.append('Category rationale missing '+c['id'])
        cat_index[c['id']]=c
    for id in CATEGORIES:
        if id not in cat_index:errors.append('Missing category '+id)
    proposals=portfolio.get('proposals',[])
    if not isinstance(proposals,list):proposals=[];errors.append('proposals array required')
    ids=set();counts=Counter();scores={}
    for i,o in enumerate(proposals):
        if not isinstance(o,dict):errors.append(f'Proposal {i}: not an object');continue
        pid=o.get('id');category=o.get('category')
        if not isinstance(pid,str) or not pid.startswith('RC-') or pid in ids:errors.append(f'Proposal {i}: invalid/repeated ID')
        ids.add(pid)
        if category not in CATEGORIES:errors.append(f'{pid}: invalid category')
        else:counts[category]+=1
        for key in ('title','problem','pitch'):
            if not isinstance(o.get(key),str) or len(o[key].strip())<12:errors.append(f'{pid}: {key} needs detail')
        for key in ('ownerPaths','steps','acceptance','tests','evidence'):
            if not isinstance(o.get(key),list) or not o[key]:errors.append(f'{pid}: {key} cannot be empty')
        for path in o.get('ownerPaths',[]):
            if not valid_repo_path(repo,path):errors.append(f'{pid}: source owner path missing or unsafe: {path}')
        for e in o.get('evidence',[]):
            if not isinstance(e,dict) or not valid_repo_path(repo,e.get('path')):
                errors.append(f'{pid}: source evidence path missing or unsafe: {e}');continue
            if not str(e.get('reason','')).strip():errors.append(f'{pid}: evidence reason required')
        for key in ('impact','maintainability','maintainerFit','confidence','effort','risk'):
            if type(o.get(key)) is not int or not 1<=o[key]<=5:errors.append(f'{pid}: {key} must be 1..5')
        if all(type(o.get(k)) is int and 1<=o[k]<=5 for k in ('impact','maintainability','maintainerFit','confidence','effort','risk')):
            scores[pid]=3*o['impact']+2*o['maintainability']+2*o['maintainerFit']+o['confidence']-o['effort']-o['risk']
        if o.get('size') not in {'S','M','L'}:errors.append(f'{pid}: size must be S/M/L')
        if o.get('overlapStatus') not in {'unchecked','none-found','related-issue','open-pr','closed-pr','duplicate'}:
            errors.append(f'{pid}: invalid overlapStatus')
        if o.get('overlapStatus')=='duplicate':errors.append(f'{pid}: duplicate PR should be in rejected candidate list, not proposal')
        if not inspect.get('githubChecked') and o.get('overlapStatus')!='unchecked':errors.append(f'{pid}: cannot assert overlap status without GitHub check')
        if not isinstance(o.get('overlapRefs'),list):errors.append(f'{pid}: overlapRefs array required')
    for cid,c in cat_index.items():
        if c.get('status')=='covered' and counts[cid]<2:errors.append(f'{cid}: covered requires >=2 proposals, got {counts[cid]}')
        if c.get('status')!='covered' and counts[cid]:errors.append(f'{cid}: category status conflicts with listed proposals')
    rank=portfolio.get('rankedIds')
    if not isinstance(rank,list):errors.append('rankedIds array required')
    else:
        if len(set(rank))!=len(rank) or any(x not in ids for x in rank):errors.append('rankedIds must be unique known IDs')
        if ids-set(rank):errors.append('rankedIds must include every proposal')
        # Stable ties allowed.
        if all(x in scores for x in rank) and any(scores[a]<scores[b] for a,b in zip(rank,rank[1:])):
            errors.append('rankedIds not descending by score')
    return errors

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sp=ap.add_subparsers(dest='command',required=True)
    ai=sp.add_parser('inventory');ai.add_argument('--repo',required=True);ai.add_argument('--output',required=True)
    av=sp.add_parser('validate');av.add_argument('--repo',required=True);av.add_argument('--input',required=True)
    args=ap.parse_args()
    try:
        repo=Path(args.repo).expanduser().resolve(strict=True)
        if args.command=='inventory':
            report=inventory(repo);out=Path(args.output).expanduser().resolve()
            if out.is_relative_to(repo):raise ValueError('Refusing to write inventory inside repository; output must be in task record outside checkout')
            out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
            print(f'OK inventory {report["maintainedFileCount"]} maintained files, {report["excludedCount"]} excluded -> {out}')
        else:
            errors=validate(json.loads(Path(args.input).read_text()),repo)
            for e in errors:print('ERROR:',e,file=sys.stderr)
            if errors:return 1
            print('OK portfolio validated')
        return 0
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print('ERROR:',exc,file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
