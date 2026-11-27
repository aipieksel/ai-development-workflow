# Optional debug logging

Logging is off unless explicitly enabled. It is a local diagnostic trail, not a
new task record, test result or approval gate. No service, telemetry upload or
background watcher is installed. Requires the existing Python 3.10+ runtime.

## Enable, inspect or disable

Resolve the actual installed skill root as `SKILL` and project root as `ROOT`:

```bash
python3 "$SKILL/scripts/workflow_log.py" enable --project-root "$ROOT"
python3 "$SKILL/scripts/workflow_log.py" status --project-root "$ROOT"
python3 "$SKILL/scripts/workflow_log.py" disable --project-root "$ROOT"
```

Configuration is `$ROOT/.aidw-debug/config.json`; events are appended to
`$ROOT/.aidw-debug/events.jsonl`. Disabling preserves existing logs. The directory
gets its own ignore file; existing repository ignore rules are not rewritten.
`AIDW_LOG=0` overrides enabled configuration for one process; `AIDW_LOG=1` enables
it for a process. Child commands inherit this setting. Explicit roots are preferred;
otherwise the helper looks for enabled configuration from the current directory
upwards. Nothing is created while logging is off.

## What is automatic

The bundled router, allocator, plan finaliser, admission gate, quick allocator/auditor
and checklist converters emit events for their actual calls when logging is enabled.
Gate failures stay failures. A checklist-conversion event is not a Tasks publication.

For other shell actions, use the wrapper instead of executing the command twice:

```bash
python3 "$SKILL/scripts/workflow_log.py" run \
  --project-root "$ROOT" --preset G1 --record "$RECORD" \
  --run-id task-001 --step T1 -- python3 -m unittest discover
```

It runs the exact argument array with `shell=False`, passes through stdout/stderr,
and records start, finish, duration and actual exit code. It returns the command’s
exit status; missing executables return 127, timeout 124 and interruption 130.
Use `--cwd DIRECTORY` for a package/subdirectory and `--timeout SECONDS` only when appropriate. Reuse a run ID across the task’s
calls; the wrapper propagates run/preset/record context into child helpers.

## Host stages, tools and agents

Native Read/Edit/browser/subagent calls do not pass through the Python runner.
Their host must forward events, or the agent must record the actual tool receipt
with this API. Do not invent an ID or report an unobserved result.

```bash
python3 "$SKILL/scripts/workflow_log.py" event \
  --project-root "$ROOT" --run-id task-001 --preset GA --record "$RECORD" \
  --kind agent --phase finish --name architect --call-id ACTUAL_CHILD_ID \
  --outcome success --evidence ACTUAL_RESULT_LOCATOR
```

Use kind `stage`, `agent`, `tool` or `task`, and phase `start`, `finish` or `blocked`.
A finish needs outcome and evidence; agent/tool events need actual call IDs unless
blocked before launch. The Python `emit` API is also available to a host bridge.
No native event bridge is automatically installed by this skill.

Events distinguish `helper`, `runner`, `host-report` and `test-adapter`. A host report
is a recorded claim with an evidence locator, not independently authenticated proof.
Planning a handoff does not mean the agent ran. `--schedule` on route_workflow.py
only describes planned order. Incomplete pairs, failures and missing receipts stay
visible; do not manufacture finish events after an interruption.

## Privacy and reliability

Logs do not capture command output, environment contents, conversation text or source
files. Common credential flags/assignments, URL queries, inline `-c`/`-e` code and
prompt arguments are masked. Redaction is best-effort: arbitrary positional secrets
can still leak, so keep secrets out of command arguments and inspect logs before sharing.
Files use private creation permissions. Symlinked debug destinations are rejected.
Logging failures warn on stderr and never change the underlying command’s result.
