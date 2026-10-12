# IPOS Executable Document Contract

This presentation contract applies to Digital and Analog block-local IPOS.
It creates no approval, ownership, allocation or requirement authority.
The existing approved snapshot resolver supplies all technical scope.
The generator invokes the shared semantic core before rendering; the
orchestrator coordinates only. Unknown or unimplemented rules block execution.

```yaml ipos-document-contract
version: 1
document_type: IPOS
profile: block_local_v1
mandatory_rules: [section_roles, functional_claims, information_gain, semantic_fidelity, publication_quality, materialization]
interpretation: admitted_normative_clauses_v1
synthesis: explicit_functional_claims_v1
detail_policy: preserve_essential_block_detail_v1
gap_policy: required_sections_with_audited_omissions_v1
essential_sources: {purpose: ["inventory:function"], capabilities: ["inventory:main_functions", "inventory:inputs", "inventory:outputs"]}
rendering: scoped_explanatory_prose_v1
paragraph: {
required: [responsibility, supported_behavior],
when_supported: [condition, effect, result, dependency, exception],
claim_scope: [initiation, behavior, result, exception, local_interaction]
}
sections: [
{role: purpose, title: "1.1 Functionality", required: true, information_gain: true},
{role: capabilities, title: "1.2 Supported functions and scope", required: true, information_gain: true},
{role: organization, title: "1.3 Internal structure", required: false, information_gain: true},
{role: functions, title: "1.4 Supported block functions", required: false, information_gain: true},
{role: architecture, title: "1.5 General architecture", required: false, information_gain: true}
]
validation_hooks: [semantic_fidelity, publication_quality, materialization]
```

Purpose explains overall responsibility. Capabilities contribute distinct
supported responsibilities, boundaries or restrictions, not copies of purpose.
Organization requires explicit containment and cannot be inferred from names.
Functional descriptions explain supported behavior and effects, retaining
conditions and dependencies. Titles disclose claim scope and do not promote
initiation-only evidence into full lifecycle coverage. Architecture requires
explicit local interactions rather than co-occurring signals or labels.

Every admitted span has a preserved, justified-excluded or unresolved
disposition. Independent complete meaning is retained; dependent meaning with
an unresolved essential restriction is withheld. Gaps remain in derived audits
and block clean acceptance only when they prevent a required section or affect
an explicit dependency of its essential sources. Unsupported independent detail
is withheld and reported, never completed or printed with uncertainty markers.
Essential sources are declared above; their dependency closure is mandatory.
Every retained claim still requires independent source-fidelity verification.
No rule authorizes inferred completion of sources.
Exact normative statements, IDs, Covers and source I/O remain unchanged.

The renderer consumes structured claims, never raw source fragments. Its bounded
paraphrases must preserve role, polarity, modality, guards, quantities, effects,
directed dependencies and exact technical identifiers. Semantic fidelity,
publication quality and materialization are separate mandatory checks against
the admitted evidence and actual Markdown/DOCX. Composer or hash agreement
alone cannot establish acceptance. No legacy rendering fallback is permitted.