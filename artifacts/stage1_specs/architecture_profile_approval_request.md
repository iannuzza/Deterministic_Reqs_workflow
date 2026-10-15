# Architecture Profile Approval Request

## Required User Action

1. In the GUI, open Architecture Map Review -> Approval / Snapshot Controls -> Open Architecture Map in Excel.
2. Review only the pending 5.3.2 passage in Descriptive Content Review, including its exact text, source revision, page/section, spans and hashes.
3. Explicitly set review_decision, mapped_block, domain and review_rationale. The proposed owner/domain is Main Controller / digital; proposals are not approval.
4. Preserve existing requirement mappings. Do not rerun ingestion, merge, retrieval indexing or Stage 2 generation for this review.
5. Save and close Excel. Select Enable Gate from Workbook and provide your explicit reviewer identity. The GUI records the reviewed profile and hashes; do not edit approval JSON manually.
6. Stop after approval for validation. Do not freeze a new snapshot until explicit approval and successful validation. The current snapshot remains unchanged.

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
- mapping_preview_csv: `21f00e814f1d59329a84d50507987fbb5751963998464a9b78fa112371746090`
- draft_profile_sha256: `61e9fa2f2c646bbde379acde99e59aa26b61c7aba7f412d810799d9ddf844a66`
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

## Pending Supplementary Descriptive Content

Review Descriptive Content Review in the existing architecture workbook. This is not a new approval lane. Do not approve through the IPOS blocker workbook or user clarified.

Baseline snapshot (unchanged): `snap-73c872b1307b6adb5eaf843e`. Candidate decision: pending. Proposed owner/domain: Main Controller / digital.

Exact extracted passage:

> This block is divided into two FSMs. The first FSM called Device_FSM, is in charge of identify the working state of the device. The second FSM called Elab_FSM, is in charge of identify what signal is in elaboration and to check and generate signal from and for the Analog Domain. The Elab_FSM is also in charge to start writing to the AHB Crossbar and to talk with Hardware DSPs block like the Avarage Circuit and ADSP, or to start PPG operation talking with the PPG_FSM. This Block is also in charge to turn of the Fast Ring Oscillator (16 MHz) and to enable the User Read Operation.

Provenance:

```json
{
  "record_id": "source-context-ab8d0db457f35c8e8f814ac5",
  "statement": "This block is divided into two FSMs. The first FSM called Device_FSM, is in charge of identify the working state of the device. The second FSM called Elab_FSM, is in charge of identify what signal is in elaboration and to check and generate signal from and for the Analog Domain. The Elab_FSM is also in charge to start writing to the AHB Crossbar and to talk with Hardware DSPs block like the Avarage Circuit and ADSP, or to start PPG operation talking with the PPG_FSM. This Block is also in charge to turn of the Fast Ring Oscillator (16 MHz) and to enable the User Read Operation.",
  "source_file": "C:\\Users\\iannuzza\\LOCAL_PROJ\\Github_copilot_proj\\STBIO_AI\\specs\\IPOS_MAIN_CTRL.pdf",
  "source_revision": "1",
  "source_revision_id": "source-rev-db3d1f0ab762a5e1d80cb718",
  "ingestion_id": "ipos_main_ctrl_20260921_143819",
  "section": "5.3.2",
  "section_context_json": "[[\"5.3.2\", \"Description of the Block\"]]",
  "source_spans_json": "[{\"artifact_sha256\": \"689b0ebcfebc4de2ffc326b80c51dc500fd36c3f61aedd6ddfa2f245a0f3f3df\", \"line\": 5, \"page\": 56, \"text_file\": \"C:\\\\Users\\\\iannuzza\\\\LOCAL_PROJ\\\\Github_copilot_proj\\\\STBIO_AI\\\\artifacts\\\\source_ingestion\\\\ipos_main_ctrl_20260921_143819\\\\ocr_extracts\\\\IPOS_MAIN_CTRL_p056.txt\"}, {\"artifact_sha256\": \"689b0ebcfebc4de2ffc326b80c51dc500fd36c3f61aedd6ddfa2f245a0f3f3df\", \"line\": 6, \"page\": 56, \"text_file\": \"C:\\\\Users\\\\iannuzza\\\\LOCAL_PROJ\\\\Github_copilot_proj\\\\STBIO_AI\\\\artifacts\\\\source_ingestion\\\\ipos_main_ctrl_20260921_143819\\\\ocr_extracts\\\\IPOS_MAIN_CTRL_p056.txt\"}, {\"artifact_sha256\": \"689b0ebcfebc4de2ffc326b80c51dc500fd36c3f61aedd6ddfa2f245a0f3f3df\", \"line\": 7, \"page\": 56, \"text_file\": \"C:\\\\Users\\\\iannuzza\\\\LOCAL_PROJ\\\\Github_copilot_proj\\\\STBIO_AI\\\\artifacts\\\\source_ingestion\\\\ipos_main_ctrl_20260921_143819\\\\ocr_extracts\\\\IPOS_MAIN_CTRL_p056.txt\"}, {\"artifact_sha256\": \"689b0ebcfebc4de2ffc326b80c51dc500fd36c3f61aedd6ddfa2f245a0f3f3df\", \"line\": 8, \"page\": 56, \"text_file\": \"C:\\\\Users\\\\iannuzza\\\\LOCAL_PROJ\\\\Github_copilot_proj\\\\STBIO_AI\\\\artifacts\\\\source_ingestion\\\\ipos_main_ctrl_20260921_143819\\\\ocr_extracts\\\\IPOS_MAIN_CTRL_p056.txt\"}, {\"artifact_sha256\": \"689b0ebcfebc4de2ffc326b80c51dc500fd36c3f61aedd6ddfa2f245a0f3f3df\", \"line\": 9, \"page\": 56, \"text_file\": \"C:\\\\Users\\\\iannuzza\\\\LOCAL_PROJ\\\\Github_copilot_proj\\\\STBIO_AI\\\\artifacts\\\\source_ingestion\\\\ipos_main_ctrl_20260921_143819\\\\ocr_extracts\\\\IPOS_MAIN_CTRL_p056.txt\"}, {\"artifact_sha256\": \"689b0ebcfebc4de2ffc326b80c51dc500fd36c3f61aedd6ddfa2f245a0f3f3df\", \"line\": 10, \"page\": 56, \"text_file\": \"C:\\\\Users\\\\iannuzza\\\\LOCAL_PROJ\\\\Github_copilot_proj\\\\STBIO_AI\\\\artifacts\\\\source_ingestion\\\\ipos_main_ctrl_20260921_143819\\\\ocr_extracts\\\\IPOS_MAIN_CTRL_p056.txt\"}]",
  "content_sha256": "cf09c77280002cd0affde36a789cf54a00a3d6347c793a429fdd9f4dab86c886",
  "evidence_kind": "descriptive",
  "admission_state": "candidate",
  "source_spec_id": "spec-8e4bb64c9781f14cc42f68b9",
  "source_revision_date": "2026-09-21",
  "source_revision_fingerprint": "524ed01d85bd8b0ad2bb3d7d749879a36980782ddd32e3001777c03dee3d8654",
  "proposed_mapped_block": "Main Controller",
  "proposed_domain": "digital",
  "required_for_review": true,
  "review_decision": "pending",
  "mapped_block": "",
  "domain": "",
  "review_rationale": "",
  "printed_page": "55"
}
```

Explicitly set review_decision, mapped_block, domain and review_rationale; save and close Excel. Only explicit architecture-profile approval and successful validation permit a subsequent new snapshot.
