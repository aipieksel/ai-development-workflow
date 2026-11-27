# Public versioning policy

## Public baseline: 2.0.0

The rebuilt public repository starts at 2.0.0 by explicit owner decision. The preceding GitHub snapshot was unversioned, with no version tags or releases at the time of this decision. Do not invent or retrospectively tag a 1.0.0 release.

The prepared 3.5.3 candidate was renumbered 2.0.0 before publication to that repository. This statement describes that candidate only; it does not assert that every earlier 3.5.x plugin was unpublished. Existing higher-numbered private installations are separate: a prepared public version does not alter an installed plugin or guarantee an automatic upgrade path.

## Routine updates: patch only

Routine updates stay within the current major and minor version. Increment only the final patch number: 2.0.0, 2.0.1, 2.0.2, and so on. Do not change 2.0 to 2.1 or advance the major version unless the owner explicitly requests that version change.

Before preparing a release, compare the current source and published version to avoid reusing an existing release number. Keep VERSION, the main SKILL.md version heading, both plugin packaging manifests, release filenames and release notes consistent. A prepared candidate is not a published release.

Schema versions, protocol revisions and independently versioned integration packages are separate identifiers. Preserve them unless their own contract is deliberately changed; never apply a global version substitution.

A byte-preserving export may retain its source version. Source or instruction changes receive a new patch version. Validate the actual generated archives and their version fields before an authorized publication.
