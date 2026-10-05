# Architecture Profile Approval Request

## Required User Action

1. Review `architecture_profile_draft.json` against the source requirements and ontology artifacts.
2. Review and edit `architecture_mapping_preview.csv` for preliminary requirement-ID-to-block assignments and generated block paragraph previews.
3. Review the final summary tables and traceability outputs generated beside the draft.
4. Define or correct real device blocks, functions, inputs, outputs, aliases, mapping rules, interaction rows, and preliminary requirement ownership.
5. Resolve or waive every critical/major ambiguity disposition with rationale; minor issues are informational.
6. Save the approved profile at the configured Stage 2 profile path.
7. Set `approval.status` to `approved`, provide non-empty `approved_by` and `approved_at`, copy the current evidence hashes, set `approval.reviewed_draft_profile_sha256` to:
   `4a92bbb6e593a4ed3a040ff74ae4fa673c8879b20cad2d9ede3f781c3b66535c`
8. Set `approval.reviewed_mapping_preview_csv_sha256` to the hash of the reviewed CSV:
   `24ad3c476b33ade7e8860fc869b5d0d77e766fcdd4c26f986cd767e71a9cabf0`
9. Run Stage 2A only after approval; it will stop when this approval record is incomplete, stale, or has unresolved critical/major ambiguity items.

## Draft Evidence Summary

- Stage 1 requirements analyzed: 314
- Candidate architecture terms: 37
- Ontology link rows analyzed: 611
- Ambiguity items requiring approval disposition: 0
- Text, table, and figure extraction completeness: not enforced by this approval gate

## Mapping CSV Review Decisions

- `approved`: accept the candidate block and generated paragraph preview.
- `approved`: use the confirmed or edited `approved_block` value.
- `rejected`: reject this preliminary assignment; Stage 2A remains blocked.
- Set `review_decision` explicitly in the workbook; block or classification edits never infer approval.
- `pending_review`: generated default, not approved for downstream use.

## Final Summary Tables / Traceability Outputs

- `architecture_mapping_preview.csv`
- `architecture_profile_requirements_summary.csv`
- `architecture_profile_block_summary.csv`
- `architecture_profile_traceability.csv`
- `architecture_profile_ambiguity_dispositions.csv`

## Evidence Hashes

- requirements_summary_csv: `19be065b5a11ef44aaed38641d93827249480615504756c7336c42f9aa00916c`
- ontology_requirement_links_csv: `28dfcc98be8ceaa3b70308a6b822a98bded7d035b78c163609d2f109a32b98c1`
- semantic_issues_md: `9161122fba5a620d263acc48c4bbec3556aa1c31a0e92724ed7f3f2abb7659a9`
- mapping_preview_csv: `24ad3c476b33ade7e8860fc869b5d0d77e766fcdd4c26f986cd767e71a9cabf0`
- draft_profile_sha256: `4a92bbb6e593a4ed3a040ff74ae4fa673c8879b20cad2d9ede3f781c3b66535c`
- ADC: 36 source requirements
- ADSP: 20 source requirements
- Block: 12 source requirements
- Buffer: 6 source requirements
- Bus: 4 source requirements
- Channel: 40 source requirements
- Chopper: 1 source requirements
- Clamp: 1 source requirements
- Configuration: 4 source requirements
- Configuration Register: 2 source requirements
- Controller: 32 source requirements
- DAC: 7 source requirements
- Destination: 4 source requirements
- Domain: 3 source requirements
- DSP: 30 source requirements
- FIFO: 33 source requirements
- Function: 8 source requirements
- I2C_SPI_AHB: 15 source requirements
- Interface: 12 source requirements
- ISPU: 25 source requirements
- Main Controller: 124 source requirements
- Memory: 13 source requirements
- Mode: 67 source requirements
- OTP: 4 source requirements
- PAD MUX: 17 source requirements
- PGA: 1 source requirements
- PMU: 12 source requirements
- Port: 6 source requirements
- Processor: 1 source requirements
- Regmap: 29 source requirements
- Sensor: 28 source requirements
- Sensor-Hub: 23 source requirements
- Serial Interface: 1 source requirements
- Smart FIFO: 13 source requirements
- Source: 4 source requirements
- State: 48 source requirements
- System: 3 source requirements
