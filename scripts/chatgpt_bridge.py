#!/usr/bin/env python3
"""ChatGPT source snapshots and portable record exports; never grants readiness.

Only caller-selected, visible messages are handled. No network calls, history
retrieval, execution routing, record allocation, or readiness mutations occur.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from plan_record import load_record


def encode(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return value


def build_snapshot(payload: Any) -> dict[str, Any]:
    """Validate and preserve caller-provided source without inventing metadata."""
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")
    for key in ("selectionBasis", "endpointLocator", "verificationBoundary"):
        nonempty(payload.get(key), key)
    if payload.get("threadId") is not None:
        nonempty(payload["threadId"], "threadId")
    messages = payload.get("messages")
    if not isinstance(messages, list) or not messages:
        raise ValueError("messages must be a nonempty list")
    locators: set[str] = set()
    for message in messages:
        if not isinstance(message, dict):
            raise ValueError("each message must be an object")
        if message.get("role") not in {"user", "assistant"}:
            raise ValueError("only visible user/assistant messages are permitted")
        locator = nonempty(message.get("locator"), "message locator")
        nonempty(message.get("text"), "message text")
        if locator in locators:
            raise ValueError("message locators must be unique")
        locators.add(locator)
        stamp = message.get("timestamp")
        if stamp is not None:
            nonempty(stamp, "timestamp")
            parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                raise ValueError("provided timestamps must include a timezone")
    if messages[-1]["locator"] != payload["endpointLocator"]:
        raise ValueError("endpointLocator must identify the last selected message")
    if messages[-1]["role"] != "user":
        raise ValueError("the endpoint must be the user's invocation")
    # This is a separate evidence envelope, not a new development-record schema.
    return {
        "schema": "aidw-chatgpt-source-snapshot/v1",
        "sourceKind": "caller-selected-visible-messages",
        "messageCount": len(messages),
        "payloadSha256": sha256(encode(payload)),
        "verificationLimit": (
            "Verified against the supplied JSON only. This helper cannot prove "
            "chat-history completeness, message authenticity, scope, or authority."
        ),
        "source": payload,
    }


def capture(input_path: Path, output_path: Path, verify: bool = False) -> dict[str, Any]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    snapshot = build_snapshot(payload)
    content = encode(snapshot)
    if verify:
        if output_path.read_bytes() != content:
            raise ValueError("snapshot differs from the supplied selected messages")
    else:
        # Exclusive creation cannot silently replace previous source evidence.
        with output_path.open("xb") as stream:
            stream.write(content)
    return {
        "path": str(output_path.resolve()),
        "messages": snapshot["messageCount"],
        "sha256": sha256(content),
        "verifiedAgainstSuppliedInput": verify,
        "historyRetrieved": False,
    }


def export_record(project_root: Path, explicit_record: str, output_path: Path) -> dict[str, Any]:
    """Export exactly one existing record without changing its lifecycle."""
    project = project_root.expanduser().resolve(strict=True)
    record, metadata = load_record(project, explicit_record)
    output = output_path.expanduser().absolute()
    if output.is_symlink() or output.exists():
        raise ValueError("export output already exists; choose a new output path")
    if output.resolve().is_relative_to(record):
        raise ValueError("export output must be outside the selected record")
    snapshots: dict[str, bytes] = {}
    for path in sorted(record.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"record contains a symlink: {path.relative_to(record)}")
        if path.is_dir():
            continue
        if not path.is_file() or not path.resolve().is_relative_to(record):
            raise ValueError(f"record contains an unsafe entry: {path}")
        snapshots[path.relative_to(project).as_posix()] = path.read_bytes()
    manifest = {
        "schema": "aidw-record-handoff/v1",
        "recordPath": record.relative_to(project).as_posix(),
        "originalProjectRoot": metadata.get("projectRoot"),
        "planRevision": metadata.get("planRevision"),
        "status": metadata.get("status"),
        "readiness": metadata.get("readiness"),
        "files": {name: sha256(data) for name, data in snapshots.items()},
        "importRule": (
            "Verify checksums, source baseline and project identity before using "
            "the original relocation and readiness-review rules. This export "
            "does not grant execution permission or rebind projectRoot."
        ),
    }
    # Keep complete record bytes, including original admission hashes/history.
    with output.open("xb") as stream:
        with ZipFile(stream, "w", ZIP_DEFLATED) as archive:
            archive.writestr("handoff.json", encode(manifest))
            for name, data in snapshots.items():
                archive.writestr(name, data)
    return {
        "path": str(output.resolve()),
        "recordPath": str(record),
        "fileCount": len(snapshots),
        "sha256": sha256(output.read_bytes()),
        "recordModified": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    snapshot = commands.add_parser("capture", help="Capture or verify selected visible messages")
    snapshot.add_argument("--input", required=True, type=Path)
    snapshot.add_argument("--output", required=True, type=Path)
    snapshot.add_argument("--verify", action="store_true")
    export = commands.add_parser("export", help="Export exactly one existing development record")
    export.add_argument("--project-root", required=True, type=Path)
    export.add_argument("--record", required=True)
    export.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "capture":
            result = capture(args.input, args.output, args.verify)
        else:
            result = export_record(args.project_root, args.record, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
