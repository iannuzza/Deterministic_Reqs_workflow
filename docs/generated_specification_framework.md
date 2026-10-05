# Generated Specification Framework

## A. Reusable end-to-end framework model

Every generated specification follows one forward-only chain:

1. Resolve one immutable approved snapshot.
2. Collect document-authoritative sources.
3. Collect support/discovery sources separately.
4. Classify authority tier, ownership, scope, and priority.
5. Build deterministic normalized records for retained and suppressed candidates.
6. Compose ordered semantic units within the document-type contract.
7. Render the units passively to Markdown.
8. Convert and post-process DOCX without semantic rewriting.
9. Record normalized inputs, semantic units, provenance, and final artifact hashes.
10. Run the document-local gate and central downstream validator.

The composer is the only semantic projection. Rendering may change presentation but cannot add,
remove, reorder, or reinterpret semantic units. Support sources can discover candidates but cannot
promote themselves or override authoritative sources.

### Descriptive and normative content paths

Generated specifications carry two distinct content paths:

- **Descriptive content** may use source-backed descriptions and capability statements from the
  Stage 1 catalog. The approved mapping and immutable snapshot provide scope, ownership, and
  structural context. A deterministic composer selects and organizes supported evidence, preserves
  provenance in the applicable audit, and renders descriptive prose without creating requirements
  or normative `Covers` links. Stage 1/RAG discovery does not itself approve content or override
  snapshot scope.
- **Normative requirements** are admitted and allocated from approved snapshot data and retain the
  document contract's exact IDs, text, and traceability. `Covers` records an approved requirement-to-
  requirement dependency; it is not a substitute for source provenance.
- **IPOS lineage** preserves both the approved hierarchical parent reference when one exists and the
  direct Stage 1/source-spec origin and location provenance in traceability records. When approved
  lineage is `direct_source_to_ipos` and no meaningful intermediate requirement exists, IPOS links
  directly to the approved source requirement ID without inventing a parent. Source type or
  provenance alone never authorizes direct allocation.

SRS, ARS, and DRS are parallel semantic derivations from the same approved snapshot. Their runner
order does not make one generated document a general authority for another. A requirement-level
dependency is recorded only where approved lineage supports it; descriptive source-backed text
retains provenance but no normative `Covers` dependency. The operational sequence and handoffs are
summarized in [workflow_source_spec_to_gen_spec.md](workflow_source_spec_to_gen_spec.md).

## B. Shared vs document-type-specific contracts

Shared code owns authority-tier representation, normalized records, semantic-unit identity and
ordering, audit structure, artifact hashing, Markdown/DOCX fidelity checks, determinism, and central
validation alignment.

Document-specific adapters own authority paths and priority, abstraction level, local or integration
scope, required sections, allowed detail, and promotion/suppression rules:

| Type | Authority and scope | Abstraction boundary |
|---|---|---|
| SRS | Approved system-owned snapshot requirements | System behavior and externally observable capability |
| ARS | Approved analog/mixed-signal architecture requirements | Top-analog and analog integration behavior |
| DRS | Approved top-digital and integration requirements | Digital architecture and integration behavior |
| IPOS | Approved block inventory plus approved same-block requirements | One concrete block's purpose, interfaces, capabilities, and requirements |

The executable registry is `DOCUMENT_TYPE_CONTRACTS` in
`scripts/spec_document_contract.py`. Adding an adapter must not weaken another document's boundary.

## C. File-level implementation plan

- `scripts/spec_document_contract.py`: shared contracts, normalized records, semantic units,
  materialization audit, hashes, and independent Markdown/DOCX checks.
- `scripts/workflow_routing.py`: IPOS normalized-input adapter and deterministic composer.
- `scripts/generate_ipos_specs.py`: passive IPOS Markdown rendering, DOCX materialization, and final
  audit write after post-processing.
- `scripts/validate_ipos_gate.py`: local IPOS authority, audit, Markdown, and DOCX validation.
- `scripts/validate_downstream_coherence.py`: central shared downstream enforcement.
- `scripts/run_srs_gen_spec_agent.py`, `scripts/run_ars_gen_spec_agent.py`, and
  `scripts/run_drs_gen_spec_agent.py`: future document-specific adapters using the shared contract.
- `.github/skills/workflow-stage-gate/SKILL.md` and
  `.github/agents/workflow-orchestrator.agent.md`: canonical execution guidance.
- `tests/test_spec_document_contract.py`: reusable synthetic end-to-end tests.
- `tests/test_descriptive_summary.py`: focused IPOS projection and boundary tests.

## D. Source, normalized-record, composer, renderer, validator, and final-DOCX contract

An authoritative source can support retained output only within its approved ownership and scope.
A discovery source can identify a candidate only. Conflicts resolve by authority tier, then approved
scope and ownership; unresolved equal-authority conflicts are suppressed for review.

Each normalized record contains a stable ID, candidate text, authority tier, ownership scope,
provenance references, retained/suppressed decision, and rationale. Each semantic unit contains a
stable ID, target section, rendered text, source-record IDs, and output order.

The composer consumes authorized normalized records and emits semantic units. The renderer emits
those units unchanged except for safe formatting. `materialization_audit.json` is written only after
DOCX post-processing and records the normalized-input fingerprint, complete records, semantic units,
and final Markdown/DOCX hashes.

The IPOS adapter projects supported same-block requirements into generic action families. An action
family is eligible only when the requirement has a recognized functional action and intersects the
approved block function or I/O boundary. The emitted sentence names the action only; it does not copy
requirement prose or use a project capability catalogue. Cross-scope ownership suppression takes
precedence and every supporting local requirement ID remains linked to the family semantic unit.

Validation checks approved-input parity independently of rendering, verifies that every retained
record is represented and no suppressed record is promoted, then checks unit presence and order in
both Markdown and final DOCX. This complements composer parity; it does not rely on composer parity
alone.

## E. Central orchestrator-validator and General Rules alignment

`scripts/workflow_cli.py validate --all --snapshot-id <id>` remains the central entry point. It
resolves one snapshot and invokes central downstream coherence before stage-local validators. The
central validator enforces the same materialization contract used by local gates and remains the
shared downstream source of truth. Local validators cannot redefine allocation, authority, or
cross-document policy.

Canonical guidance requires authority/discovery separation, normalized provenance, one composer,
passive rendering, final-DOCX validation, project-agnostic shared logic, and reusable synthetic tests.
Project names, block catalogues, capability catalogues, and golden project prose are forbidden in
shared rules and shared tests.

## F. Test and audit/provenance model

Reusable tests use synthetic document names and content. They cover deterministic contract
registration, retained-input completeness, suppressed-source promotion, provenance references,
semantic-unit order, Markdown loss, DOCX post-processing loss, and artifact hash drift. IPOS tests
add same-block retention, cross-block suppression, conflict suppression, normative-copy suppression,
candidate-universe parity, and digital/analog policy parity.

The CSV descriptive audit remains the detailed composition-decision surface. The JSON
materialization audit binds those decisions to final artifacts and makes post-generation mutation
detectable.

## G. Staged implementation order

1. Define the shared executable contract and audit model.
2. Add independent materialization validation.
3. Instantiate normalized records and semantic units for IPOS.
4. Enforce the contract in the local IPOS gate and central validator.
5. Align canonical workflow and orchestrator guidance.
6. Add synthetic reusable and IPOS-focused tests.
7. Regenerate IPOS and execute local and central validation.
8. Migrate SRS, ARS, and DRS adapters one at a time without changing their authority boundaries.

## H. Validation execution plan

Run in this order and stop on the first failure:

1. `python -m unittest -v tests.test_spec_document_contract tests.test_descriptive_summary`
2. Generate the targeted IPOS stage from the approved snapshot.
3. Run `scripts/validate_ipos_gate.py` for that IPOS kind and snapshot.
4. Run the opposite IPOS gate when both partitions are materialized.
5. Run `scripts/validate_downstream_coherence.py --snapshot-id <id>`.
6. Run `scripts/workflow_cli.py validate --all --snapshot-id <id>`.

Report local generation defects separately from pre-existing downstream coherence findings. Never
change approved source, allocation, ownership, or snapshot state merely to make a validator pass.