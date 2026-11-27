# AI Development Workflow — Version 2

A complete plugin with one main skill and five public controls: **auto**, **plan**, **build**, **review** and **loop**. Auto selects a concrete Plan, Build, Review or Loop mode. XR remains a compatibility alias for Loop.

Every task requires actual delegated work. Known localized builds use **Fast full build / Ponytail** with the **Fast Engineer**; changes across pages, features or shared contracts require **Architect** advice before final planning. Unknown impact is investigated before implementation. The workflow announces its selected mode, routing reason, phases and actual workers, and preserves independent criticism and review.

Read the [complete user guide](skills/ai-development-workflow/README.md), [task and agent routing rules](skills/ai-development-workflow/references/task-routing.md) and [advanced reference](skills/ai-development-workflow/references/advanced-reference.md). All commands, operational role instructions and runtime dependencies are bundled inside the main skill directory.

Install this complete archive through a supported plugin host. In ChatGPT, type `@`, select AI Development Workflow from autocomplete, then enter `auto` followed by your task. The host must provide real worker dispatch. Missing dispatch is reported as a blocker; reading a role profile does not count as spawning an agent. File access and monitoring also depend on that host.

See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md) for licensing and attribution.
