# Workflow: Source Specification to Generated Specifications

## Ordered flow

- **S0 — Source baseline and ontology:** establish the approved primary-source baseline and prepare source-backed ontology evidence. Gate 0 must pass.
- **S1 — Source ingestion:** the only stage that reads the source specification directly. Extract requirements, source-backed descriptive content, IDs, and file/page/section/table/line provenance. Build the Stage 1 catalog and retrieval artifacts; pass Gate 1.
- **S2 — Formalization and mapping preparation:** consume Stage 0 and Stage 1 artifacts to prepare the architecture profile and mapping-review package. Stage 2+ remains artifact-driven and must not reread the source specification.
- **Review and synchronization:** approve the architecture profile and requirement mapping. Synchronize the saved review workbook to the machine-readable mapping CSV and verify its evidence hashes.
- **S2A — Architecture mapping:** use approved Stage 1 evidence, ontology links, and profile data to determine ownership, allocation, and block structure. Complete mapping crosschecks and pass the gate.
- **S2H — Snapshot approval:** persist approved requirements, mappings, allocation, provenance, and lineage, then freeze one immutable snapshot. Resolve one snapshot ID and pass that same ID to every downstream generator and validator.
- **Pre-generation validation:** run central downstream coherence validation for the selected snapshot before generating specifications.
- **Specification generation:** generate SRS, ARS, and DRS under their own scopes from the same approved snapshot. Generate Digital and Analog IPOS from that snapshot and approved block-local evidence.
- **Materialization and gates:** render Markdown and DOCX, run document crosschecks and local gates, then run central downstream coherence validation.

## Two content paths

- **Descriptive content:** Stage 1's source-backed descriptions and capability statements are eligible evidence for descriptive sections. The approved mapping and snapshot provide scope, ownership, and structural context. A deterministic composer selects and organizes supported evidence, preserves provenance in the applicable audit, and renders descriptive prose without creating requirements or normative `Covers` links. Stage 1/RAG discovery alone does not approve content or override snapshot scope.
- **Normative requirements:** requirements are admitted and allocated through approved snapshot data. Authored requirements retain exact IDs, text, allocation, and traceability required by the document contract. For IPOS, each requirement keeps the approved hierarchical parent reference (`Covers`) when a parent requirement exists, and its traceability record also retains the direct Stage 1/source-spec origin and location provenance.
- **Direct IPOS lineage:** when approved evidence explicitly selects `direct_source_to_ipos` and no meaningful intermediate requirement exists, IPOS links directly to the approved source requirement ID. Do not invent an SRS/ARS/DRS parent. Supplementary-source direct lineage follows its separately approved lineage mode.

## Dependency rules

- Source specification → Stage 1 extraction/catalog/provenance → Stage 2 preparation → reviewed mapping and allocation → S2A → immutable snapshot → generated specifications.
- Stage 0 ontology supports classification and mapping; it does not create unsupported requirements or replace source provenance.
- SRS, ARS, and DRS are parallel semantic derivations from the approved snapshot. Their execution order does not make one generated document a general authority for another.
- A requirement-level dependency is recorded only when approved lineage supports it. `Covers` expresses the normative upstream requirement relationship; source-spec provenance is retained separately. Descriptive content uses provenance, not normative `Covers`.
- IPOS adds approved block inventory, ownership, and same-block evidence as dependencies. Cross-scope evidence cannot establish block-local requirements.
- A failed stage or gate blocks advancement. Correct the blocker and rerun the affected forward sequence; never alter approved source, ownership, allocation, or snapshot state merely to satisfy a validator.
