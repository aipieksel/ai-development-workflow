# Public versioning policy

## First formal Version 2 release: 2.0.0

Version `2.0.0` is the first formal tag and GitHub release for Version 2 by explicit owner decision. The preceding public repository snapshot had no formal version tag or release; do not invent or retrospectively tag a `1.0.0` release.

Public commit `9df3b6b` carried an untagged mistaken/preparatory higher patch source label before the first formal release. That commit is an untagged public source snapshot, not a formal tag or GitHub Release and not the active product version. The normalized active source/package version is `2.0.0`. Preserve this fact in release history rather than rewriting or tagging the old commit.

The prepared 3.5.3 candidate was renumbered into this Version 2 baseline before formal publication. This statement describes that candidate only; it does not assert that every earlier 3.5.x plugin was unpublished. Consumers that copied the untagged higher-patch-labelled source may observe the normalized version as a numerical downgrade. Source normalization does not automatically downgrade an installed plugin, and no automatic downgrade path is promised.

## Post-release Version 2 display correction

The exact human-facing identity is **AI Development Workflow — Version 2**. This display label is deliberately independent from the machine package version: `VERSION`, both manifest `version` fields, changelog keys and archive filenames continue to use SemVer.

After the first formal release, the Version 2 display label may be corrected narrowly without pretending that its human heading is a new machine version. This exception does not authorize rebuilding, replacing or distributing packages under `2.0.0`. Existing release artifacts remain immutable, and the next distributable release must be `2.0.1`.

## Routine updates: patch only

Routine updates stay within the current major and minor version. The next routine release after the first formal `2.0.0` release is `2.0.1`, followed by `2.0.2` and so on. Do not change `2.0` to `2.1` or advance the major version unless the owner explicitly requests that version change.

Before preparing a release, compare the current source and published version to avoid reusing an existing release number. Keep `VERSION`, both plugin manifest `version` fields, changelog keys and release filenames consistent. Keep the exact Version 2 display identity synchronized independently across human-facing headings and interface metadata. A proposed or future GitHub release title is publication metadata; it does not change the active source version. A prepared candidate is not a published release.

Schema versions, protocol revisions and independently versioned integration packages are separate identifiers. Preserve them unless their own contract is deliberately changed; never apply a global version substitution.

A byte-preserving export may retain its source version. Except for the narrow non-distributable display correction above, source or instruction changes receive a new patch version. Validate the actual generated archives and their version fields before an authorized publication.
