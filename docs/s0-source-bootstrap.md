# S0 Primary Source Bootstrap

The incremental S0 hook is implemented in `scripts/s0_source_bootstrap.py`.

It accepts a local PDF, HTML, or DOCX source and deterministically reports:

- `tagged`, `untagged`, or `ambiguous` status;
- a proposed base req-ID prefix when evidence supports one;
- tagged, table, and unbracketed ID evidence with page/line context;
- a reason for the result.

The detector reuses `requirement_id_rules.table_req_id_patterns` and does not replace
Stage 1 requirement extraction. Table headers are normalized, including `Req-ID`,
`Req_ID`, `Req Id`, `Requirement ID`, `Spec ID`, and equivalent forms.

`persist_candidate` stores the assessment in the existing canonical
`profile_revisions` table as `profile_kind=source_baseline`, with `lifecycle_state=staged`
and `approval_state=pending`. It also records a source-import audit event. No
approval or active-baseline change occurs.

The Step 5 GUI must provide primary-source selection and show the assessment for
explicit approve, edit, or reject decisions. Step 5 must also promote only an
approved source-baseline candidate into the active workflow context.
