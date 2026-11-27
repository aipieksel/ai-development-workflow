#!/usr/bin/env python3
"""Convert a Markdown checklist to a structured task-list payload.
Stdlib only. Prints JSON; the calling agent publishes it through the chat-scoped tool.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[3] / "scripts"))
from workflow_log import emit
import re


def unfenced_lines(markdown):
    """Yield physical line numbers and prose; blank out code fences and their content."""
    fence = None
    for number, line in enumerate(markdown.splitlines(), 1):
        marker = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
        if fence is not None:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            yield number, ''
        elif marker:
            fence = marker[1]
            yield number, ''
        else:
            yield number, line


def checklist_rows(markdown):
    """Shared parser for publication and audit; location stays out of tool payloads."""
    items = []
    seen = set()
    current = None
    for number, line in unfenced_lines(markdown):
        match = re.match(r'^(\s*)(?:[-*+]|\d+[.)])\s+\[([ xX~!])\]\s+(.+?)\s*$', line)
        if match:
            label = match[3]
            explicit = re.match(r'^(R\d+)\b[\s:.-]*(.*)$', label)
            item_id = explicit[1] if explicit else 'item-' + hashlib.sha256(label.encode()).hexdigest()[:16]
            if item_id in seen:
                raise ValueError(f'Duplicate item ID {item_id}; give each item a unique stable R ID.')
            seen.add(item_id)
            current = {'id': item_id, 'text': label,
                       'status': {' ': 'pending', 'x': 'completed', '~': 'in_progress', '!': 'blocked'}[match[2].lower()],
                       'line': number}
            items.append(current)
        elif current and line.strip() and line[:1].isspace() and not re.match(r'^\s*(?:[-*+]|\d+[.)])\s', line):
            current['text'] += ' ' + line.strip()
        else:
            current = None
    if not items:
        raise ValueError('No checklist items found; refusing to publish an empty replacement.')
    return items


def parse_checklist(markdown):
    return [{key: item[key] for key in ('id', 'text', 'status')}
            for item in checklist_rows(markdown)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--record', type=Path, help='Development record containing checklist.md and record.json')
    source.add_argument('--checklist', type=Path, help='Any skill Markdown checklist')
    parser.add_argument('--id', help='Stable checklist ID (defaults to record directory name)')
    parser.add_argument('--title')
    parser.add_argument('--mode', choices=['merge', 'replace'], default='merge')
    parser.add_argument('--output', type=Path, help='Write JSON here instead of stdout')
    args = parser.parse_args()
    try:
        metadata = json.loads((args.record / 'record.json').read_text()) if args.record else {}
        checklist = args.record / 'checklist.md' if args.record else args.checklist
        identifier = args.id or (args.record.name if args.record else None)
        if not identifier:
            raise ValueError('--id is required with --checklist')
        payload = {'id': identifier, 'title': args.title or metadata.get('title') or checklist.stem, 'mode': args.mode, 'items': parse_checklist(checklist.read_text())}
        emit("checklist.convert", record=str(args.record) if args.record else None, itemCount=len(payload["items"]), outcome="success", published=False)
        result = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            args.output.write_text(result)
        else:
            print(result, end='')
    except (OSError, ValueError) as error:
        emit("checklist.convert", outcome="failed", errorType=type(error).__name__, published=False)
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
