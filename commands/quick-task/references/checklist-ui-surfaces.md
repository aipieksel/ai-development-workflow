# Visible checklists and optional host mirroring

The durable `checklist.md` and visible checklist contain the same stable item IDs, scope and
completion state. Show ordinary Markdown in the conversation at initial planning, material
changes, progress updates and final handoff. A file link or promise is not the visible list.

An actually available host checklist/plan tool may mirror the same work. Discover its real
schema, supported statuses and return contract first. Require its actual acknowledged result
before saying the host surface updated. This package does not install a panel or prescribe
an editor extension's API. If mirroring is unavailable, failed or incomplete, show the complete
current Markdown without implying a panel exists.

## Stable item states

Give each outcome a stable R ID and source reference. Preserve IDs when wording changes.
Use `[ ]` for pending, `[~]` for in progress, `[x]` for verified completion, and `[!]` for blocked
in the durable file. In ordinary rendered Markdown, use unchecked boxes plus explicit status
text for in-progress/blocked items when the renderer does not support those extension markers.
Completion requires the actual work and decisive checks, not a worker claim.

```markdown
- [ ] R1 Restore the specified destination. — in progress
- [ ] R2 Verify the original navigation behavior. — pending
```

Keep at most one quick-task item actively in progress. Update the durable file first and the
visible state in the same work interval. Preserve unresolved items and reasons. A replacement
list must intentionally reconcile the complete current list; never hide unfinished work.

## Optional generic payload conversion

The bundled helper retains a generic JSON conversion interface for compatible consumers and
for the quick-record auditor's shared parser. Resolve it from the directory containing the
quick-task `workflow.md`:

```bash
python3 <quick-task>/scripts/checklist_payload.py   --checklist <record>/checklist.md --id <stable-record-id> --title <task-title>
```

Use the record directory name as a stable checklist ID, qualified by project if needed.
Do not use the development-record `--record` form for a compact quick record: it has no
development `record.json`. The helper requires Python 3.10+ and the standard library.

The converter retains R IDs/source references, handles wrapped/nested items, ignores fenced
examples and rejects duplicate IDs or empty lists. Anonymous IDs derive from labels, so use
explicit R IDs to keep renames stable. It prints `id`, optional `title`, `mode` and `items`;
item states map to `pending`, `in_progress`, `completed` and `blocked`. This is local data,
not a universal host-tool schema. Adapt only through the actual consumer's documented contract.

Generating JSON does not send it, publish progress, prove persistence or establish host access.
If the real tool lacks a blocked state, keep the item unresolved and explain the blocker.
Partial acknowledgments do not prove the complete checklist was published. Final reporting
must expose all actual completed and remaining items through a supported visible surface.
