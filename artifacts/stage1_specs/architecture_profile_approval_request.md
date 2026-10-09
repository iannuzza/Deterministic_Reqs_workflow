# Architecture Profile Approval Request

## Required User Action

1. Review `architecture_profile_draft.json` against the source requirements and ontology artifacts.
2. Review and edit `architecture_mapping_preview.csv` for preliminary requirement-ID-to-block assignments and generated block paragraph previews.
3. Review the final summary tables and traceability outputs generated beside the draft.
4. Define or correct real device blocks, functions, inputs, outputs, aliases, mapping rules, interaction rows, and preliminary requirement ownership.
5. Resolve or waive every critical/major ambiguity disposition with rationale; minor issues are informational.
6. Save the approved profile at the configured Stage 2 profile path.
7. Set `approval.status` to `approved`, provide non-empty `approved_by` and `approved_at`, copy the current evidence hashes, set `approval.reviewed_draft_profile_sha256` to:
   `99408ebf35f43c6bbf86f96cc989c073d37039f4200273acb6359e96de55f2c0`
8. Set `approval.reviewed_mapping_preview_csv_sha256` to the hash of the reviewed CSV:
   `1c881387d2542440dbbe1091c041082c856fbbe9157d33e5c85737702b418933`
9. Run Stage 2A only after approval; it will stop when this approval record is incomplete, stale, or has unresolved critical/major ambiguity items.

## Draft Evidence Summary

- Stage 1 requirements analyzed: 357
- Candidate architecture terms: 37
- Ontology link rows analyzed: 643
- Ambiguity items requiring approval disposition: 1
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

- requirements_summary_csv: `3d036916a8f9baecb5d370fd548f8ce295c97eb7b08c50109088e94933a4580d`
- ontology_requirement_links_csv: `720bf547f764dce6c361a6980f0794af3083b760f72ce4789468b351c0dcafed`
- semantic_issues_md: `3c642564650d136fbf4432ea5e5fb13a37e301ed25e9a8b11817d1536de4ee37`
- mapping_preview_csv: `1c881387d2542440dbbe1091c041082c856fbbe9157d33e5c85737702b418933`
- draft_profile_sha256: `99408ebf35f43c6bbf86f96cc989c073d37039f4200273acb6359e96de55f2c0`
- ADC: 41 source requirements
- ADSP: 20 source requirements
- Block: 12 source requirements
- Buffer: 7 source requirements
- Bus: 4 source requirements
- Channel: 45 source requirements
- Chopper: 1 source requirements
- Clamp: 1 source requirements
- Configuration: 4 source requirements
- Configuration Register: 2 source requirements
- Controller: 33 source requirements
- DAC: 7 source requirements
- Destination: 4 source requirements
- Domain: 3 source requirements
- DSP: 30 source requirements
- FIFO: 33 source requirements
- Function: 8 source requirements
- I2C_SPI_AHB: 15 source requirements
- Interface: 12 source requirements
- ISPU: 25 source requirements
- Main Controller: 167 source requirements
- Memory: 13 source requirements
- Mode: 71 source requirements
- OTP: 4 source requirements
- PAD MUX: 17 source requirements
- PGA: 2 source requirements
- PMU: 12 source requirements
- Port: 6 source requirements
- Processor: 1 source requirements
- Regmap: 29 source requirements
- Sensor: 28 source requirements
- Sensor-Hub: 23 source requirements
- Serial Interface: 1 source requirements
- Smart FIFO: 13 source requirements
- Source: 4 source requirements
- State: 62 source requirements
- System: 3 source requirements
