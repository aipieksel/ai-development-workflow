#!/usr/bin/env python3
"""Run a reviewed acceptance-command list once, retaining all independent failures."""
from __future__ import annotations
import argparse
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import time

# Script-relative import: no assumption about the installed skill or home directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from workflow_log import emit, safe_argv


def load_checks(path: Path, root: Path) -> list[dict]:
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict) or not isinstance(value.get('checks'), list) or not value['checks']:
        raise ValueError('manifest requires a nonempty checks list')
    checks, ids = [], set()
    for item in value['checks']:
        if not isinstance(item, dict):
            raise ValueError('each check must be an object')
        identifier, argv = item.get('id'), item.get('argv')
        if not isinstance(identifier, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', identifier) or identifier in ids:
            raise ValueError('check IDs must be unique safe names')
        if not isinstance(argv, list) or not argv or any(not isinstance(a, str) or '\0' in a for a in argv) or not argv[0].strip():
            raise ValueError('argv must be a nonempty literal argument array')
        raw_cwd = item.get('cwd', '.')
        if not isinstance(raw_cwd, str) or Path(raw_cwd).is_absolute():
            raise ValueError('check cwd must be relative to the project')
        cwd = (root / raw_cwd).resolve(strict=True)
        if not cwd.is_relative_to(root) or not cwd.is_dir():
            raise ValueError('check cwd escapes the project or is not a directory')
        timeout = item.get('timeoutSeconds', 300)
        if isinstance(timeout, bool) or not isinstance(timeout, (float, int)) or not math.isfinite(timeout) or timeout <= 0:
            raise ValueError('timeoutSeconds must be positive and finite')
        deps = item.get('dependsOn', [])
        if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps) or len(deps) != len(set(deps)):
            raise ValueError('dependsOn must contain unique check IDs')
        ids.add(identifier)
        checks.append({'id': identifier, 'argv': argv, 'cwd': str(cwd), 'timeoutSeconds': timeout, 'dependsOn': deps})
    for item in checks:
        if not set(item['dependsOn']) <= ids or item['id'] in item['dependsOn']:
            raise ValueError('unknown or self-referencing dependency')
    ordered, remaining = [], checks[:]
    while remaining:
        ready = [c for c in remaining if set(c['dependsOn']) <= {p['id'] for p in ordered}]
        if not ready:
            raise ValueError('acceptance dependency cycle')
        ordered.extend(ready)
        remaining = [c for c in remaining if c not in ready]
    return ordered


def run_suite(checks: list[dict], root: Path, output: Path) -> dict:
    results, states = [], {}
    for check in checks:
        name = check['id']
        failed_dependencies = [d for d in check['dependsOn'] if states[d] != 'passed']
        if failed_dependencies:
            result = {'id': name, 'status': 'blocked', 'blockedBy': failed_dependencies, 'exitCode': None}
        else:
            started = time.monotonic()
            status, code, child = 'failed', 127, None
            emit('acceptance.start', root=root, source='runner', name=name, argv=safe_argv(check['argv']))
            with (output / f'{name}.stdout.log').open('wb') as stdout, (output / f'{name}.stderr.log').open('wb') as stderr:
                try:
                    child = subprocess.Popen(check['argv'], cwd=check['cwd'], stdin=subprocess.DEVNULL,
                        stdout=stdout, stderr=stderr, start_new_session=os.name == 'posix', shell=False)
                    code = child.wait(timeout=check['timeoutSeconds'])
                    status = 'passed' if code == 0 else 'failed'
                except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
                    if child is not None:
                        if os.name == 'posix': os.killpg(child.pid, signal.SIGTERM)
                        else: child.terminate()
                        try: child.wait(timeout=2)
                        except subprocess.TimeoutExpired:
                            if os.name == 'posix': os.killpg(child.pid, signal.SIGKILL)
                            else: child.kill()
                            child.wait()
                    status, code = ('timeout', 124) if isinstance(exc, subprocess.TimeoutExpired) else ('interrupted', 130)
                except OSError as exc:
                    stderr.write(f'{type(exc).__name__}: cannot run configured executable\n'.encode())
            result = {'id': name, 'status': status, 'exitCode': code,
                'durationSeconds': round(time.monotonic()-started, 3), 'argv': safe_argv(check['argv']),
                'stdout': f'{name}.stdout.log', 'stderr': f'{name}.stderr.log'}
            emit('acceptance.finish', root=root, source='runner', name=name, outcome=status, exitCode=code)
        results.append(result); states[name] = result['status']
        # Retain useful partial results even when execution is interrupted.
        summary = {'status': 'passed' if len(results) == len(checks) and all(s == 'passed' for s in states.values()) else 'incomplete',
            'projectRoot': str(root), 'configured': len(checks), 'results': results,
            'boundary': 'Configured commands only; coverage and live model execution are not inferred.'}
        (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
        if result['status'] == 'interrupted': break
    summary['status'] = 'passed' if len(results) == len(checks) and all(s == 'passed' for s in states.values()) else 'failed'
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', required=True, type=Path)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--output-dir', type=Path, help='Parent for unique run folders; relative to project root')
    args = parser.parse_args()
    try:
        root = args.project_root.expanduser().resolve(strict=True)
        if not root.is_dir(): raise ValueError('project-root must be an existing directory')
        checks = load_checks(args.manifest.expanduser().resolve(strict=True), root)
        base = args.output_dir.expanduser() if args.output_dir else Path('tmp/aidw-acceptance')
        base = (base if base.is_absolute() else root/base).resolve()
        if args.output_dir is None and not base.is_relative_to(root):
            raise ValueError('default output escapes project; select an explicit output directory')
        base.mkdir(parents=True, exist_ok=True)
        output = Path(tempfile.mkdtemp(prefix='run-', dir=base)).resolve()
        summary = run_suite(checks, root, output)
        print(json.dumps({'status': summary['status'], 'checks': len(summary['results']), 'output': str(output)}, indent=2))
        return 0 if summary['status'] == 'passed' else 1
    except (OSError, ValueError, TypeError) as exc:
        print(f'Acceptance runner: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
