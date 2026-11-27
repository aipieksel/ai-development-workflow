#!/usr/bin/env python3
"""Validate task-checklist request/checklist traceability records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3] / "scripts"))
from workflow_log import traced
from workflow_contract import validate_quick, BOUNDARY
from checklist_payload import checklist_rows, unfenced_lines


SOURCE_ID_RE = re.compile(r"^(#{1,6})\s+(?P<id>S\d+(?:\.\d+)*)\b")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
REF_RE = re.compile(
    r"request\.md\s+(?P<id>S\d+(?:\.\d+)*),\s+lines?\s+"
    r"(?P<start>\d+)(?:-(?P<end>\d+))?"
)
AGENT_ADDED_RE = re.compile(r"\(agent-added [^)]+ necessity(?::[^)]*)?\)\s*$")


def load_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        raise SystemExit(f"missing required file: {path}") from None


def source_sections(lines):
    """Return real source extents and explicit coverage dispositions, not semantic judgements."""
    headings = []
    dispositions = {}
    in_coverage = False
    for number, line in unfenced_lines('\n'.join(lines)):
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading[1])
            if level <= 2:
                in_coverage = heading[2].strip().casefold() == 'coverage map'
            source = SOURCE_ID_RE.match(line)
            headings.append((number, level, source['id'] if source else None))
        if in_coverage:
            disposition = re.match(r'^\s*[-*+]\s+(S\d+(?:\.\d+)*):\s*'
                                   r'(context-only|grouping-only)\s*[—–:-]\s*(\S.*)$', line)
            if disposition:
                dispositions[disposition[1]] = (disposition[2], disposition[3])
    sections = {}
    errors = []
    for index, (start, level, source_id) in enumerate(headings):
        if source_id is None:
            continue
        if source_id in sections:
            errors.append(f'duplicate source ID {source_id}')
            continue
        end = next((n - 1 for n, depth, _ in headings[index + 1:] if depth <= level), len(lines))
        sections[source_id] = {'start': start, 'end': end, 'group': False}
    for source_id, section in sections.items():
        children = [child for sid, child in sections.items()
                    if sid.startswith(source_id + '.')
                    and section['start'] < child['start'] <= child['end'] <= section['end']]
        # Non-source subheadings and code examples can also contain parent instructions.
        own_text = any(lines[n - 1].strip()
                       for n in range(section['start'] + 1, section['end'] + 1)
                       if not any(child['start'] <= n <= child['end'] for child in children))
        section['group'] = bool(children) and not own_text
    for source_id, (kind, _) in dispositions.items():
        if source_id not in sections:
            errors.append(f'coverage disposition references unknown source ID {source_id}')
        elif kind == 'grouping-only' and not sections[source_id]['group']:
            errors.append(f'{source_id} has its own source text; grouping-only cannot hide it')
    return sections, dispositions, errors


def source_ids(lines):
    return set(source_sections(lines)[0])


def checklist_items(lines):
    items = []
    for row in checklist_rows('\n'.join(lines)):
        text = row['text']
        refs = [{'id': ref['id'], 'start': int(ref['start']),
                 'end': int(ref['end'] or ref['start'])} for ref in REF_RE.finditer(text)]
        items.append({**row, 'done': row['status'] == 'completed', 'refs': refs,
                      'agent_added': bool(AGENT_ADDED_RE.search(text))})
    return items


@traced("quick.audit")
def validate(record_dir: Path) -> dict[str, object]:
    request_path = record_dir / "request.md"
    checklist_path = record_dir / "checklist.md"
    request_lines = load_lines(request_path)
    checklist_lines = load_lines(checklist_path)

    errors: list[str] = []
    required_headings = ["## Goal", "## Source instructions", "## Coverage map"]
    visible_lines = {line for _, line in unfenced_lines('\n'.join(request_lines))}
    for heading in required_headings:
        if heading not in visible_lines:
            errors.append(f"request.md missing heading: {heading}")

    sections, dispositions, section_errors = source_sections(request_lines)
    errors.extend(section_errors)
    ids = set(sections)
    if not ids:
        errors.append("request.md has no source IDs like S1.1")

    try:
        items = checklist_items(checklist_lines)
    except ValueError as error:
        errors.append(str(error))
        items = []
    if not items:
        errors.append("checklist.md has no Markdown checkbox items")

    covered_ids: set[str] = set()
    for item in items:
        refs = item["refs"]
        if not refs:
            if not item["agent_added"]:
                errors.append(f"checklist.md line {item['line']} has no source reference")
            continue
        for ref in refs:  # type: ignore[assignment]
            ref_id = ref["id"]
            start = ref["start"]
            end = ref["end"]
            if ref_id not in ids:
                errors.append(
                    f"checklist.md line {item['line']} references unknown source ID {ref_id}"
                )
            if start < 1 or end < start or end > len(request_lines):
                errors.append(
                    f"checklist.md line {item['line']} references invalid request.md "
                    f"line range {start}-{end}"
                )
            if ref_id in sections:
                section = sections[ref_id]
                if not section['start'] <= start <= end <= section['end']:
                    errors.append(f"checklist.md line {item['line']} references lines {start}-{end} "
                                  f"outside source section {ref_id} ({section['start']}-{section['end']})")
                    continue
            covered_ids.add(ref_id)

    exempt = {sid for sid, section in sections.items() if section['group']}
    exempt.update(sid for sid, (kind, _) in dispositions.items() if kind == 'context-only')
    missing = sorted(ids - covered_ids - exempt)
    for source_id in missing:
        errors.append(f"source item {source_id} is not referenced by any checklist item")

    completed = sum(1 for item in items if item["done"])
    pending = len(items) - completed
    return {
        "ok": not errors,
        "record_dir": str(record_dir),
        "request_lines": len(request_lines),
        "source_ids": sorted(ids),
        "grouping_sources": sorted(sid for sid in sections if sections[sid]["group"]),
        "coverage_dispositions": dispositions,
        "checklist_items": len(items),
        "completed": completed,
        "pending": pending,
        "plan": plan_items(items),
        "errors": errors,
    }


def plan_items(items: list[dict[str, object]]) -> list[dict[str, str]]:
    plan: list[dict[str, str]] = []
    for item in items:
        text = str(item["text"])
        text = re.sub(r"\s+\(source:\s*request\.md.+\)$", "", text)
        text = re.sub(r"\s+\(agent-added [^)]+ necessity(?::[^)]*)?\)$", "", text)
        plan.append(
            {
                "step": text,
                # Native update_plan has no blocked state; retain it as pending.
                "status": "pending" if item["status"] == "blocked" else str(item["status"]),
            }
        )
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record_dir", type=Path)
    parser.add_argument("--execution", action="store_true",
                        help="Also require the current compact plan/criticism/public briefing contract")
    parser.add_argument(
        "--plan-json",
        action="store_true",
        help="print only the update_plan-shaped plan array",
    )
    args = parser.parse_args()

    result = validate(args.record_dir)
    result["executionAdmitted"] = False
    if args.execution and result["ok"]:
        try:
            admission = validate_quick(args.record_dir)
            result["executionAdmitted"] = admission["admitted"]
            result["workHash"] = admission["workHash"]
        except (OSError, ValueError, TypeError, KeyError) as error:
            result["ok"] = False
            result["errors"].append(str(error))
    result["boundary"] = BOUNDARY if args.execution else "Traceability inspection only; no execution admission."
    output = result["plan"] if args.plan_json else result
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
