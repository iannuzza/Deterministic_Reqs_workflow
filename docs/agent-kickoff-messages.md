# Agent Kickoff Messages

## Ontological Specification Analyzer Agent
Scope: Build semantic ontology baseline, normalize terminology, and flag semantic blockers before requirement extraction.
Execution model: Run Stage 0 Phase 0 through Phase 7, produce ontology/glossary/semantic issue artifacts, and issue explicit Gate 0 `go`/`no-go` recommendation for Stage 1.

## Requirements Extraction Agent
Scope: Run Stage 1 OCR + deterministic taxonomy update, extract explicit functional requirements, reuse or assign IDs, and produce canonical requirement summary tables.

## Specs Agent
Scope: Formalize extracted requirements into acceptance tests, assertions, and implementation-ready specification artifacts.

## Numeric Core Agent
Scope: Implement deterministic reference model and ensure unit-test baseline.

## Verification and Vectors Agent
Scope: Execute regression and emit reproducible golden vectors with metadata.

## Design Agent
Scope: Implement synthesizable design aligned with validated model behavior.

## Verification Agent
Scope: Run implementation-vs-golden verification and severity triage.

## Synthesis Agent
Scope: Run synthesis, collect timing/area metrics, and classify blockers.

## Performance and Optimization Agent
Scope: Produce prioritized optimization plan with quantified expected deltas.
