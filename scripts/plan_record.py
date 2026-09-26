#!/usr/bin/env python3
"""Portable plan contract v2. Validation checks structure, not truth or permission."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path("documents/tasks/development")
FILES = ("checklist.md", "fix-plan.md", "test-plan.md", "critique.md", "results.md")
PLAN_FILES = FILES[:3]
STATES = {"draft", "planned", "criticized", "executing", "blocked", "complete"}
PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{5}-[a-z0-9][a-z0-9-]*$")

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def request_hashes(data):
    sources = data.get("requestSources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("requestSources missing; preserve the original request before readiness review")
    hashes = {}
    for source in sources:
        if not isinstance(source, dict) or any(
            not isinstance(source.get(key), str) or not source[key].strip()
            for key in ("id", "text", "origin", "role")
        ):
            raise ValueError("request source requires id, verbatim text, origin and role")
        if source["id"] in hashes or source["role"] not in {"user", "context", "policy"}:
            raise ValueError("duplicate request source ID or invalid role")
        encoded = json.dumps(source, sort_keys=True, separators=(",", ":")).encode()
        hashes[source["id"]] = hashlib.sha256(encoded).hexdigest()
    if not any(source["role"] == "user" for source in sources):
        raise ValueError("requestSources must include the actual user request")
    return hashes

def seal_request_sources(data):
    """Allow source addenda, never silently reseal edited or deleted sources."""
    hashes = request_hashes(data)
    previous = data.get("requestHashes", {})
    if not isinstance(previous, dict):
        raise ValueError("requestHashes must be an object")
    if any(hashes.get(key) != value for key, value in previous.items()):
        raise ValueError("preserved request source changed or removed; restore it and append a correction")
    return hashes

def definition_hash(data):
    keys = ("projectRoot", "recordPath", "planRevision", "sourceBaseline",
            "scope", "requirements", "steps", "checks", "requestSources", "requestHashes")
    encoded = json.dumps({key: data.get(key) for key in keys},
                         sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()

def load_record(project_root, explicit):
    project = Path(project_root).expanduser().resolve(strict=True)
    raw = Path(explicit).expanduser()
    record = (raw if raw.is_absolute() else project / raw)
    if record.is_symlink():
        raise ValueError("record cannot be a symlink")
    record = record.resolve(strict=True)
    if record.parent != (project / ROOT).resolve() or not PATTERN.fullmatch(record.name):
        raise ValueError("record must be a direct dated child of documents/tasks/development")
    # Reject an escaped/symlinked task root, metadata or document.
    if not record.is_relative_to(project):
        raise ValueError("record escapes project")
    for name in ("record.json",) + FILES:
        path = record / name
        if path.is_symlink() or not path.is_file() or not path.stat().st_size:
            raise ValueError("missing, empty or symlinked record file: " + name)
    data = json.loads((record / "record.json").read_text())
    if not isinstance(data, dict) or data.get("schema") != "project-development-plan/v1":
        raise ValueError("incompatible plan record")
    if data.get("status") not in STATES:
        raise ValueError("invalid lifecycle status")
    return record, data

def select(project_root, explicit=None):
    project = Path(project_root).expanduser().resolve(strict=True)
    if explicit:
        return load_record(project, explicit)
    candidates = []
    root = project / ROOT
    if root.is_dir():
        for child in sorted(root.iterdir()):
            if not PATTERN.fullmatch(child.name):
                continue
            # A damaged record must be reported, not silently skipped for an older plan.
            record, data = load_record(project, child)
            if data["status"] != "complete":
                candidates.append((record, data))
    if not candidates:
        raise ValueError("no active record; provide --record for historical review")
    if len(candidates) != 1:
        raise ValueError("multiple active records; select --record explicitly: " +
                         ", ".join(p.name for p, _ in candidates))
    return candidates[0]

def gate(record, data, project_root, resume=False):
    def text_list(value):
        return isinstance(value, list) and bool(value) and all(isinstance(x, str) and x.strip() for x in value)
    if data.get("contractVersion") != 2:
        raise ValueError("legacy record: inspect and migrate to contractVersion 2 before execution")
    project = Path(project_root).expanduser().resolve(strict=True)
    if data.get("projectRoot") != str(project):
        raise ValueError("projectRoot mismatch; rebind only after verifying project identity and sources")
    if data.get("recordPath") != str(record.relative_to(project)):
        raise ValueError("recordPath mismatch")
    allowed = {"executing", "blocked"} if resume else {"planned", "criticized"}
    if data["status"] not in allowed:
        raise ValueError("status not eligible; interrupted work requires explicit --resume")
    if data.get("readiness") != "ready" or data.get("blockers") != []:
        raise ValueError("unresolved readiness or blockers")
    if data.get("critiqueOutcome") not in {"not_requested", "ready", "revised"}:
        raise ValueError("critique is blocked or unfinished")
    revision = data.get("planRevision")
    if type(revision) is not int or revision < 1:
        raise ValueError("planRevision must be a positive integer")
    if data.get("critiqueOutcome") != "not_requested":
        if data.get("reviewedPlanRevision") != revision:
            raise ValueError("critique covers a different plan revision")
        if data.get("critiqueHash") != digest(record / "critique.md"):
            raise ValueError("critique changed since review")
    baseline = data.get("sourceBaseline")
    if not isinstance(baseline, dict) or not baseline.get("description"):
        raise ValueError("source baseline missing")
    scope = data.get("scope")
    if not isinstance(scope, dict) or not text_list(scope.get("in")) or not text_list(scope.get("out")):
        raise ValueError("scope and exclusions required")
    requirements, steps, checks = (data.get(k) for k in ("requirements", "steps", "checks"))
    if not all(isinstance(x, list) and x for x in (requirements, steps, checks)):
        raise ValueError("requirements, steps and checks required")
    def ids(items):
        values = [x.get("id") if isinstance(x, dict) else None for x in items]
        if any(not isinstance(x, str) or not x for x in values) or len(set(values)) != len(values):
            raise ValueError("missing or duplicate traceability IDs")
        return set(values)
    reqids, stepids, checkids = ids(requirements), ids(steps), ids(checks)
    for item in requirements:
        if not item.get("text"):
            raise ValueError("requirement text missing")
    for item in steps:
        if not text_list(item.get("paths")) or not isinstance(item.get("change"), str) or not item.get("change"):
            raise ValueError("step paths/change missing")
    for item in checks:
        if not item.get("method") or not item.get("expected") or not item.get("boundary"):
            raise ValueError("verification method/expected/evidence boundary missing")
    for group in (steps, checks):
        covered = set()
        for item in group:
            refs = item.get("requirements")
            if not text_list(refs) or not set(refs) <= reqids:
                raise ValueError("invalid requirement reference")
            covered.update(refs)
        if covered != reqids:
            raise ValueError("unmapped requirements")
    sources = request_hashes(data)
    if data.get("requestHashes") != sources:
        raise ValueError("request sources changed since review; preserve old sources and review addenda")
    roles = {item["id"]: item["role"] for item in data["requestSources"]}
    for item in requirements:
        refs = item.get("sources")
        if not text_list(refs) or not set(refs) <= sources.keys():
            raise ValueError("requirement source references missing or unknown")
        kind = item.get("kind")
        if kind == "requested":
            if not any(roles[ref] == "user" for ref in refs):
                raise ValueError("requested requirement needs a user source, not assistant context")
        elif kind == "necessary":
            if not any(roles[ref] in {"user", "policy"} for ref in refs):
                raise ValueError("necessary requirement needs a user or policy source")
            if not isinstance(item.get("justification"), str) or not item["justification"].strip():
                raise ValueError("necessary requirement needs an evidence-backed justification")
        else:
            raise ValueError("requirement kind must be requested or necessary; proposals are not executable")
    graph = {}
    for step in steps:
        deps = step.get("dependsOn", [])
        if not isinstance(deps, list) or not set(deps) <= stepids:
            raise ValueError("unknown step dependency")
        graph[step["id"]] = deps
    visiting, done = set(), set()
    def visit(node):
        if node in visiting:
            raise ValueError("dependency cycle")
        if node in done:
            return
        visiting.add(node)
        for dep in graph[node]:
            visit(dep)
        visiting.remove(node)
        done.add(node)
    for node in graph:
        visit(node)
    hashes = data.get("planHashes", {})
    if not isinstance(hashes, dict):
        raise ValueError("planHashes must be an object")
    for name in PLAN_FILES:
        if hashes.get(name) != digest(record / name):
            raise ValueError("plan changed since readiness review: " + name)
    if data.get("definitionHash") != definition_hash(data):
        raise ValueError("plan metadata changed since readiness review")
    return True

def main(default_execution=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--record")
    parser.add_argument("--execution", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    try:
        record, data = select(args.project_root, args.record)
        if args.resume and not args.record:
            raise ValueError("--resume requires an explicit --record")
        if default_execution or args.execution or args.resume:
            gate(record, data, args.project_root, args.resume)
        print(json.dumps({"status": "resolved", "recordPath": str(record), "record": data}, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
