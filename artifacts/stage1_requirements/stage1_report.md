# Stage 01 Report

Date: 2026-08-28

## Scope
- Functional requirement extraction and summary table generation from full specification text.
- Source specification: `C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf`.

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
- Total requirements listed: 187
- System requirements: 40
- Analog requirements: 2
- Digital requirements: 145
- Tagged preserve rows: 187
- Generated standard rows: 0

## Status
- Gate 1: pass

## Risks
- Tagged-source strict mode active: only source-tagged IDs are emitted.
- Some statements may need wording normalization during domain review.
