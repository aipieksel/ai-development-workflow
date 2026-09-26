#!/usr/bin/env python3
"""Create a unique, populated project development plan record."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path("documents/tasks/development")
DIR_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})-(\d{5})-[a-z0-9][a-z0-9-]*$")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("title must contain at least one letter or number")
    return slug[:64].rstrip("-")


def next_number(root: Path, date: str) -> int:
    numbers: list[int] = []
    if root.is_dir():
        for child in root.iterdir():
            match = DIR_PATTERN.fullmatch(child.name)
            if child.is_dir() and match and match.group(1) == date:
                numbers.append(int(match.group(2)))
    return max(numbers, default=0) + 1


def create_record(project_root: Path, title: str) -> dict[str, object]:
    if not project_root.is_dir():
        raise ValueError(f"project root is not a directory: {project_root}")
    clean_title = title.strip()
    slug = slugify(clean_title)
    now = datetime.now().astimezone()
    date = now.strftime("%Y-%m-%d")
    root = project_root / ROOT
    if not root.resolve().is_relative_to(project_root.resolve()):
        raise ValueError("task root escapes the project through a symlink")
    root.mkdir(parents=True, exist_ok=True)
    number = next_number(root, date)
    while True:
        record = root / f"{date}-{number:05d}-{slug}"
        try:
            record.mkdir()
            break
        except FileExistsError:
            number += 1

    markdown = {
        "checklist.md": f"# Checklist: {clean_title}\n\nReplace this placeholder with source-linked R items for the actual requested outcomes and constraints, not the mechanics of creating a plan. Preserve the original messages in record.json requestSources first.\n",
        "fix-plan.md": f"# Implementation plan: {clean_title}\n\n## Evidence and current behavior\n\n_Pending investigation._\n\n## Root causes or gaps\n\n_Pending investigation._\n\n## Ordered implementation changes\n\n_Pending investigation._\n\n## Constraints, risks, and non-goals\n\n_Pending investigation._\n",
        "test-plan.md": f"# Verification plan: {clean_title}\n\n| Outcome | Verification method | Expected result | Evidence boundary |\n|---|---|---|---|\n| Requested change | Pending investigation | Decisive proof | Not yet run |\n",
        "critique.md": f"# Plan critique: {clean_title}\n\n> Status: pending\n\n_No critique has been performed._\n",
        "results.md": f"# Execution results: {clean_title}\n\n> Status: not-started\n\n_No implementation has been executed._\n",
    }
    for name, content in markdown.items():
        (record / name).write_text(content, encoding="utf-8")
    metadata = {
        "schema": "project-development-plan/v1",
        "contractVersion": 2,
        "title": clean_title,
        "projectRoot": str(project_root),
        "recordPath": str(record.relative_to(project_root)),
        "status": "draft",
        "readiness": "not_ready",
        "blockers": [],
        "planRevision": 1,
        "critiqueOutcome": "not_requested",
        "reviewedPlanRevision": None,
        "sourceBaseline": {"description": "", "revision": None, "dirtyPaths": []},
        "scope": {"in": [], "out": []},
        "requestSources": [],
        "requestHashes": {},
        "requirements": [],
        "steps": [],
        "checks": [],
        "planHashes": {},
        "createdAt": now.isoformat(),
        "updatedAt": now.isoformat(),
        "files": ["checklist.md", "fix-plan.md", "test-plan.md", "critique.md", "results.md"],
    }
    (record / "record.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return {"status": "initialized", "recordPath": str(record), "files": metadata["files"] + ["record.json"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()
    try:
        payload = create_record(Path(args.project_root).expanduser().resolve(), args.title)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
