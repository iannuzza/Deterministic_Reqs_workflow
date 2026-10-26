# Approved SRS Rules Checkpoint

- ID: `2026-10-26-srs-rules-approved`.
- User approved the SRS rule baseline for the main official workflow.
- General rules: [copilot-instructions.md](../../../.github/copilot-instructions.md),
  dated SRS semantic-composition section.
- Current project state: [chat handoff](../../chat_handoff.md) and
  [checkpoint index](../../checkpoint.md).
- Suggested Git tag: `srs-rules-baseline-2026-10-26`. No tag, commit or push created.

## Scope and authority

This save updates general rules and memory/checkpoint metadata. It does NOT import
trial runtime code, overwrite official generated documents, approve pending source
uses, change canonical approvals, select/freeze another snapshot or certify
publication/implementation readiness.

The latest pilot is in the sibling `review_srs_20261026_1437` workspace under
`artifacts/reviews/system_requirements_specification/pilot_final`.
It retains its non-authoritative review labels. Its last editorial corrections
are source-bound review data, not yet automatic official composer behaviour.

## Preserved material

`srs_rules_and_trial_backup.zip` contains isolated trial scripts/tests, the SRS
template/process documentation, final Word/Markdown pilot and source-bound review
data, exact prior diffs, verification evidence, updated memories and restart notes.
`checkpoint_manifest.json` records every archive member, size and SHA256, archive
integrity, official Git HEAD and protected-file verification.
`before_metadata.zip` preserves the four changed official metadata files before
this save. The existing dirty sync manifest is left unchanged.

This is a source/evidence checkpoint, not a standalone repository or canonical
database backup. Canonical databases, source specifications, approval workbooks,
personal GUI state, caches and WAL/SHM are not archived or implicitly approved.
Do not blindly extract it over newer work.

## Verification and open work

Retained trial evidence: 203 focused tests, 44 bounded actual-prose checks and a
passing final renderer regression. Word/Markdown parity and unchanged remaining
prose were checked. The broader independent assessment remains UNRESOLVED
(335 findings); no new full-flow run or whole-hierarchy closure is claimed.

Ambiguous "cent inputs" remains verbatim. "Eventually" is retained without adding
optionality, timing guarantees or inferred transitions; both ambiguities are
tracked separately. DRS and Main Controller IPOS remain the next focused
priorities, or separately scoped official runtime integration.

Use a small restart handoff, one practical trial and targeted verification.
Parallel implementations need separate local copies/worktrees, not only separate
VS Code windows sharing runtime, database, workbook or artifact paths.
