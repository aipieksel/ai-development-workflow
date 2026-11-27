# Optional acceptance runner

Helper: [run_acceptance.py](../scripts/run_acceptance.py).

Prefer the project's existing combined test command. Otherwise write a reviewed JSON
manifest: `{"checks":[{"id":"unit","argv":["npm","run","test:unit"]}]}`.
Each check may set `cwd` relative to the project, `dependsOn` check IDs, and a positive
`timeoutSeconds`. Commands are literal arrays, not shell strings. Never put secrets
in arguments; stdout/stderr evidence may be sensitive. This runs exactly those commands,
not a browser or AI by itself. Independent checks still run after another check fails;
dependent checks are blocked, not passed. A missing/empty suite is an error.

From the skill root:
`python3 agents/fast-engineer/scripts/run_acceptance.py --project-root /actual/project --manifest /path/to/checks.json`

The runner creates a fresh project-local `tmp/aidw-acceptance/run-...` directory or
an explicit `--output-dir` parent, retains per-check output and writes summary.json.
Exit 0 means all configured checks passed, not that coverage is complete or native
agents ran. Scope and required checks must be established before execution.
