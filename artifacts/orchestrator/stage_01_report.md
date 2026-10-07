# Stage 01 Report

Date: 2026-10-06

## Scope
- Functional requirement extraction and summary table generation from full specification text.
- Source specification: `specs/DDS_STBIO1.pdf`.

## Evidence
- Functional requirements extracted
- Functional Description sentences extracted through final sentence punctuation
- PDF table row/value candidates extracted
- Timing table rows extracted with one requirement per timing row
- Analog/electrical/measurement characteristic tables extracted with one requirement per row
- Block diagram block names extracted and crosschecked against specification behavior sentences
- PDF image/caption context candidates extracted as derived-from-structure evidence
- Requirement summary table generated
- Source paragraph references validated

## Extraction Metrics
- Total requirements listed: 271
- System requirements: 117
- Analog requirements: 0
- Digital requirements: 154
- Tagged preserve rows: 191
- Generated standard rows: 0

## Status
- Gate 1: pass

## Risks
- Tagged-source strict mode active: only source-tagged IDs are emitted.
- Some statements may need wording normalization during domain review.

## Stage1 Text Quality Cross-Check
- Checked requirements: 271
- Corrected split/truncated statements: 11
- RAG exact matches: 232
- RAG warnings: 39
- RAG fails: 0
