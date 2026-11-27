# Context-Only Invocation

Use this reference only when the user invokes G0/GO or the Quick Task entry without adding
a substantive task in the same message.

## Select the issue corpus

1. Ignore the bare invocation when identifying the task subject.
2. Locate the most recent assistant completion handoff that closed a task. Use
   it as the boundary anchor.
3. Collect every related user and assistant message from that boundary through
   the invocation. This includes the completion handoff, later feedback and
   corrections, the immediately preceding explanation, and the user message it
   answered.
4. Follow direct conversational references needed to make that corpus complete,
   such as an issue document or thread explicitly identified in those messages.
5. Stop before an older completed task or unrelated topic.
6. If the completion boundary, relationship of an intervening message, or
   intended remediation outcome is uncertain, ask the user before writing the
   record or checklist.
7. If no unresolved issue, correction, or new requirement exists after the
   completion handoff, ask the user what should become the checklist subject.

Do not add speculative interpretations, optional features, extra test targets,
or suggested product behavior. If the corpus is already operationally clear,
use its wording directly. If a missing decision is necessary to proceed, ask
the user and record the answer as a user-confirmed clarification.

The resulting source record should be extensive. Preserve the issue-bearing
content at its original level of detail instead of replacing it with a short
summary.

## NewsAI multi-message example

An agent completes a NewsAI task. The user then changes the scope to local-only,
asks for the local link, corrects the port choice, and discusses the result over
several turns before invoking G0/GO or the Quick Task entry alone. The source corpus begins
at the completion handoff and includes all of those related turns through the
invocation. It is not limited to the port explanation or its user message.

## Build two checklist layers

The first and primary layer is the issue-remediation checklist. It must cover:

- each observed defect or failure;
- each missing or incorrect behavior;
- each affected component, page, workflow, or artifact when separately stated;
- each unresolved question that requires investigation;
- each requested correction or outcome;
- each constraint, example, acceptance criterion, and verification condition.

The second layer contains workflow necessities such as preserving the source,
checking repository state, updating documentation, testing, and reporting.
These items support the first layer and must not replace it.

## Page Audit regression example

Scenario: an investigation produces a long document explaining that Page Audit
recommendations are confusing, weakly actionable, inconsistently grouped,
missing actions from several stages, and need a consolidated presentation. The
user then sends only G0/GO or the Quick Task entry.

Incorrect primary checklist:

- inspect the Page Audit page;
- find the original scope;
- document the stages and results;
- validate and report the document.

Those items describe creation of the analysis document. They can all be
completed while every diagnosed product problem remains.

Correct primary checklist categories:

- verify and characterize each confusing or non-actionable recommendation
  presentation identified by the investigation;
- account for recommendations omitted from the consolidated view;
- correct the grouping and display behavior described in the issue corpus;
- resolve each explicitly open product question before implementation;
- implement every approved correction with the stated constraints;
- verify the corrected behavior against every acceptance criterion and affected
  surface named in the issue corpus.

Exact checkbox wording and granularity must come from the actual issue corpus,
not from this example.

## Semantic acceptance test

Ask: "Could an agent check every primary item while leaving the documented
underlying problems untouched?"

If yes, the checklist targets the meta-task. Rebuild it from the underlying
issues before showing it to the user or beginning implementation.
