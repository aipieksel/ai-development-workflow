#!/usr/bin/env python3
"""Create the next visible task-checklist record directory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3] / "scripts"))
from workflow_log import traced


RECORD_RE = re.compile(r"^(?P<id>\d{5,})-\d{4}-\d{2}-\d{2}-.+$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def existing_ids(record_root: Path) -> list[int]:
    if not record_root.exists():
        return []
    ids: list[int] = []
    for child in record_root.iterdir():
        if not child.is_dir():
            continue
        match = RECORD_RE.match(child.name)
        if match:
            ids.append(int(match.group("id")))
    return ids


@traced("quick.allocate")
def allocate(workspace_root: Path, slug: str, date: str, dry_run: bool) -> dict[str, object]:
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("slug must use lowercase ASCII letters, digits, and single hyphens")
    workspace_root = workspace_root.expanduser()
    if not workspace_root.is_dir():
        raise ValueError(f"workspace root is not a directory: {workspace_root}")
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        if parsed_date.date().isoformat() != date:
            raise ValueError("non-canonical date")
    except ValueError as exc:
        raise ValueError("date must use YYYY-MM-DD") from exc

    workspace_root = workspace_root.expanduser().resolve(strict=True)
    record_root = (workspace_root / "docs" / "tasks" / "checklist").resolve()
    if not record_root.is_relative_to(workspace_root):
        raise ValueError("task record destination escapes the verified workspace through a symlink")
    ids = existing_ids(record_root)
    next_id = max(ids, default=0) + 1
    directory_name = f"{next_id:05d}-{date}-{slug}"
    record_dir = record_root / directory_name

    if record_dir.exists() or record_dir.is_symlink():
        raise FileExistsError(f"refusing to overwrite existing record: {record_dir}")
    if not dry_run:
        record_root.mkdir(parents=True, exist_ok=True)
        if not record_root.resolve().is_relative_to(workspace_root):
            raise ValueError("task record destination changed to a path outside the workspace")
        record_dir.mkdir(exist_ok=False)

    return {
        "created": not dry_run,
        "directory_name": directory_name,
        "next_id": next_id,
        "record_dir": str(record_dir),
        "record_root": str(record_root),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace_root", type=Path)
    parser.add_argument("slug")
    parser.add_argument(
        "--date",
        default=datetime.now().astimezone().date().isoformat(),
        help="record date in YYYY-MM-DD format; defaults to the local date",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the next directory without creating it",
    )
    args = parser.parse_args()

    try:
        result = allocate(args.workspace_root.expanduser().resolve(), args.slug, args.date, args.dry_run)
    except (FileExistsError, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "ok": False}, indent=2), file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, **result}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
