# Public versioning policy

## Product and public release identity

The product name is **AI Development Workflow**. Human-facing headings, plugin display names and agent metadata use that plain name without a version suffix.

The public release tag is `2.0`. It is the concise public release presentation, not a replacement for the source and package machine version.

## Machine package identity: 2.0.0

The internal source/package SemVer is `2.0.0`. Keep `VERSION`, both plugin manifest `version` fields, the `2.0.0` changelog key and package-content metadata aligned. The canonical builder derives archive filenames from `VERSION`, so its current archive names remain `ai-development-workflow-v2.0.0-local-skill.zip` and `ai-development-workflow-v2.0.0-plugin.zip`; do not hardcode the public `2.0` presentation into machine package names. For this corrective Release, external staging renames those exact verified bytes to `ai-development-workflow-2.0-local-skill.zip` and `ai-development-workflow-2.0-plugin.zip` before generating `SHA256SUMS.txt` from the final basenames.

Display identity and machine identity are separate contracts. A plain product heading must not be rejected because it omits SemVer, and a correct display name must never excuse a mismatched manifest or package version.

## Corrective replacement of the v2.0.0 release

The earlier `v2.0.0` Git tag and same-named GitHub release were created with incorrect public presentation. The owner authorized replacing that release with tag `2.0`, removing the old GitHub Release and deleting only its `v2.0.0` tag ref after the replacement is public and verified. The corrective commit remains a normal descendant: do not rewrite, force-push or retrospectively relabel commit history.

The replacement archives retain internal package version `2.0.0`. Previously downloaded `v2.0.0` assets cannot be recalled and may differ from the corrective replacement bytes; release notes and checksums must state the replacement honestly.

Public commit `9df3b6b` also carried an untagged mistaken/preparatory higher patch source label before the formal release. It is a historical source snapshot, not the active product identity or an instruction to recreate a higher release. Consumers that copied that source may observe the normalized machine version as a numerical downgrade; source normalization does not automatically downgrade an installed plugin.

## Next machine patch

After this explicitly authorized corrective replacement, the next machine package release is `2.0.1`, followed by `2.0.2` and later patches. Do not reuse `2.0.0` again, and do not change the `2.0` major/minor line unless the owner explicitly requests it.

Before preparing a release, compare the current source, tags and published releases. A proposed title is publication metadata, not the active source version, and a prepared candidate is not a published release.

Schema versions, protocol revisions and independently versioned integration packages are separate identifiers. Preserve them unless their own contract is deliberately changed; never apply a global version substitution. Validate generated archives and their machine version fields before an authorized publication.
