# IPOS Descriptive Rendering

## Stage 6 block-local blocker review (2026-10-12)

The shared `ipos_blocker_review` coordinator evaluates each Digital IPOS against
the unchanged approved-input, claim and document checks. A clean block is generated
without a review workbook or GUI interruption. A blocked block is not published;
other blocks continue, even while its review workbook is unsaved or open.
Stage 6 remains unsuccessful overall if any block remains blocked.

Only current active blockers appear in that block's dedicated
`artifacts/orchestrator/ipos_blocker_reviews/<block-slug>/blocker_review.xlsx`
and short Markdown companion. The GUI opens the workbook automatically and exposes
its exact path, an Open Excel action and a block-only Re-evaluate action in a
non-modal window. Select User decision from the three flow choices and edit Note,
save and close Excel, then re-evaluate. Tool recommendations and facts stay read-only. The checker
re-reads the saved workbook and reruns the existing checks for the selected block.
An open, unchanged or altered-facts workbook holds only its own block.

`omit (as non-blocking)` is an explicit operational exclusion from descriptive
elaboration and writing only (user-authorized rule update, 2026-10-13). A saved,
closed selection binds to the exact current claim or explicitly selected section;
it does not require a clarification Note. Normative requirement rows, authored
IDs/text, Covers and traceability remain complete and unchanged. Selecting a
section excludes every descriptive claim assigned to that section, not just the
individual rows also listed in the workbook. Required overview sections and all
checks on remaining content still apply.
`user clarified` requires a Note for re-evaluation. `need source/spec update -
clarification` remains blocked and records a future source/spec task; Stage 6 does
not perform that update. Notes cannot introduce authority, change approved meaning
or waive any gate. A review is retired from the active location only after fresh
checks independently clear the block. Failed publication preserves earlier output.
The selected decision is checked independently of Excel's dropdown validation.
A source-update selection holds the block pending a future update; another choice
cannot clear a tool-reported source-update blocker. Descriptive omit selections
are audited as `user_omit_descriptive_only`, never as normative deletions or
automatic approval of unrelated failures. The
displayed Resulting action remains the tool recommendation; the checker records
the effective action from the saved selection. Existing workbooks can be upgraded
without losing notes or treating the programmatic upgrade as a user save.
Resolved omit decisions are retained in a snapshot/block-bound receipt backed by
the hash-verified archived workbook. Generation and independent gates reconstruct
the same descriptive exclusions from that evidence; changed or unbound decisions
are rejected. No approved snapshot, requirement allocation or canonical text is
edited by this content-selection policy.

## Clock and reset connection presentation (2026-10-12)

The shared IPOS presentation path renders admitted, connection-only clock and
reset claims as dedicated tables within the existing General architecture
section. Supported block functions retains descriptive behavior, including
sequencing and conditional signal actions, not static connection lists.
Clock rows contain Source requirement, Source, Destination, Clock frequency and
Clock gate condition; reset rows contain Source requirement, Source and Destination.
Only retained same-owner approved spans supply cells. Unsupported fields remain
empty; explicit absence of clock gating is rendered as Not gated. Incomplete
source fragments remain preserved in omission audits, never completed by inference.
Existing fidelity and materialization checks cover exact cells, contributors,
table placement and actual Markdown/DOCX. Authority, allocation, executable
contract and gate entrypoints are unchanged; this is not a semantic-model migration.

## Descriptive obligation boundary (2026-10-12)

The centralized `descriptive-obligations-v1` policy separates source admission,
textual obligations, and output representation. Only unresolved textual
obligations of the current document/profile contract block descriptive synthesis.
Explicit configuration rows, register catalogs, table-only spans and formula
payloads remain exact in their existing structured/normative path and auditable
as `nonprose_output_path` dispositions. Register catalogs are never copied into
I/O or interface tables. Mixed behavior/table/procedure evidence is not exempted
as a whole; complete functional relationships and dependent contexts remain
subject to the existing fidelity and publication checks.

Approved requirement and structured content can support description only when
already admitted within the selected snapshot, owner scope and document profile.
For IPOS, inventory bounds macro-purpose; same-owner requirements and admitted
I/O descriptions may refine local detail. Neither a table, an identifier hit nor
a profile creates approval, a capability or an architectural responsibility.
SRS and the integration profiles retain their existing admission and detail
controls; this policy does not activate a disabled profile or migrate a renderer.

Identifier support retrieval is bounded and deterministic: exact spelling first,
then case/whitespace/hyphen/underscore variants, with admitted I/O descriptions
before same-scope requirement evidence at equal lexical rank. Guard actors may
use the approved owner or a uniquely described admitted I/O identifier. Preserve
authored spelling and exact authoritative IDs. Conflicting descriptions, budget
overflow, prefix changes, inferred abbreviations and fuzzy equivalence remain
unresolved. Independent source checks consume the same scoped support, and all
semantic, publication and materialization gates remain mandatory.

The five-category read-only review is produced by the existing report generator
with `--render-only --descriptive-review`. It does not regenerate specifications,
modify the original cross-specification report or certify publication.

## Current direction: common descriptive contract (2026-10-09)

Contract identity: `shared-descriptive-contract-v2` (planned contract revision,
not a runtime schema, profile activation or canonical approval change). This is
the single shared strategy for SRS, DRS, ARS, Digital IPOS and Analog IPOS, despite
the historical filename. The user-authorized regression review supersedes the
earlier local repair strategy and its publication acceptance assumptions.

The common contract preserves meaning and produces coherent technical
explanation, not lightly rewritten requirements. Centralization, a valid model,
cleaner audits, more headings or passing unit tests do not establish publication
acceptance. The observed failures require claim synthesis and independent quality
obligations; do not address them through more isolated parser or heading patches.
No project, owner name, signal, source ID or historical paragraph supplies a rule.

The established SRS introductory writing rule and DRS evidence-bounded technical
prose direction remain profile-specific baselines. This plan does not change
their frozen preferences, runtime activation, authority boundaries or outputs.
Shared integrity is invariant. Profiles control only abstraction level, detail
policy, section intent and presentation style within centrally resolved scope.

Implementation checkpoint: `2026-10-09-ipos-yaml-shared-core`. The separate
`templates/IPOS_document_contract.md` embeds the block-local IPOS YAML profile.
DRS and IPOS share only the duplicate-safe loader/framework, not a YAML instance.
Unknown policies, weakened obligations and forged derived hashes are rejected.
Paragraph slots, claim scopes, section roles, information gain, detail/gap rules
and the three independent validation hooks are declared in this profile.

The shared synthesis model is version `1.1`. Its IPOS adapter interprets admitted
artifact clauses into exact spans and typed responsibility, action, object,
condition, effect, scope and provenance before prose. Explicit shared
responsibility is a registered grouping rule, not a dependency inferred from
labels. Unresolved references create conservative dependency edges; independent
complete meaning survives while dependent claims remain withheld. Dependencies
retain their direction. All unresolved spans remain auditable; unresolved textual
obligations block acceptance, while explicitly routed non-prose stays separate.

The sole active composer and structural audit consume this claim plan. The
renderer does not concatenate precomposed fact paragraphs or infer FSM titles.
The generator loads/applies YAML and runs claim preflight before writing a block
document. DOCX prerequisites are mandatory; there is no Markdown-only success
fallback. Actual final Markdown and DOCX must then pass separate semantic,
publication and materialization checks. Existing stage and central gates invoke
the same document-contract boundary; the canonical resolver remains sole authority.

Semantic readback does not recompose expected prose. Its bounded grammar admits
contain/comprise equivalence and a repositioned guard, while independently
checking responsibility, predicates, objects, effects, guards, polarity,
contributors, headings and exact uppercase/underscore identifiers. Cross-record
contradictions are blocking. Publication checks examine actual prose; material
hashes and parity remain fidelity checks, not semantic or editorial proof.
The model-only acceptance envelope cannot certify a document or create approval.

Focused verification: 141 descriptive +15 document-contract +8 DRS template
+19 SRS coherence +2 source-I/O tests =185 PASS; touched Python diagnostics clean.
The initial SRS discovery pattern matched zero tests and is not included.

Main Controller remains a proving case, not reusable-code policy. Read-only proof
at the unchanged approved snapshot:138 normative records,67 propositions,49
claims,111 unresolved contexts; proposed prose also has subject-verb agreement
and missing-action-link findings. The strict block gate FAILs; central scoped
coherence is BLOCK_DOWNSTREAM with287 findings. Canonical DB and5218 existing
artifacts were hash-checked unchanged. No specification was regenerated, no PDF
was read, and no Git save or canonical approval/mapping/allocation write occurred.

Publication is NOT resolved. The bounded interpreter still lacks constructions
present in approved evidence, and complete block-functional explanation requires
further interpretation/synthesis work. Do not label every parser gap source
damage, demand reapproval, silently weaken checks or publish a fragmentary preview.
The following previous implementation observations are historical diagnostics,
not publication acceptance or a justification for preserving current prose.

### Previous implementation observations: publication rejected

Previous implementation status (2026-10-09): the shared typed model and central
application policies are connected to the bounded IPOS adapter, existing generator
and gate. DRS/ARS remain inactive; a general context-preserving semantic adapter is
not complete. Only Main Controller was regenerated in this follow-up.

Section 1.2 now includes an audited main-functions role derived literally from the
approved inventory Function field: an actual named list with a separate description
for each function, followed by I/O boundaries. Controlled clause separation keeps
coordinated predicates sharing an object and bracketed details intact. Main-function
facts remain separate during aggregation, and independent source reconstruction
rejects lost/duplicated entries and invented conditions or qualifiers. The three
Main Controller entries were verified in both formats after09:01:37-09:01:55
regeneration; fresh124+9+19=152 focused tests PASS, strict gate still FAIL.
Latest follow-up (2026-10-09 09:52) restores section1.4 through the central path:
complete passive initiation relationships, guarded flag set/clear lifecycles and
literal FSM/phase behavior can form named functional groups. Parenthesized guard
thresholds and same-subject coordinated modal predicates are preserved; incomplete
clauses and unsupported multi-actor constructions remain gaps. Titles derive from
supported effects or explicit functional entities, never arbitrary actors or an
activated legacy project catalogue. Section metadata follows the same application
profile, and final-artifact token accounting includes each source-backed label once.

Main Controller now has six groups: PPG saturation flag control, Elaboration FSM,
Measurement initiation, Device FSM, PPG FSM and Digital ramp control. These are
bounded descriptions, not complete algorithms. GSR acquisition/processing, ADC
phases, full measurement setup and an aggregate Main Controller FSM remain unresolved;
old project-specific summaries are not authority to complete them. Final generation
09:52:42-09:52:56 has paired overview parity and unchanged138 normative blocks/Covers,
source I/O, canonical database and5210 protected artifacts. Tests127+9+19=155 PASS;
strict gate remains FAIL. General context-preserving functional synthesis is incomplete.

The438/774 counts below are historical pre-list whole-semantic checks, not current
acceptance totals. Historical state: 123 descriptive +9 document-contract +19 SRS coherence tests PASS;
Main Controller gate FAIL, 438 overlapping descriptive findings, central
BLOCK_DOWNSTREAM 774. Original 138 normative blocks/Covers/history/I/O, canonical
database and 5,210 protected artifacts unchanged. One auxiliary snapshot-selection
report is additional to the original backup inventory. Actual local backup/reports:
`local_memory/checkpoints/2026-10-08-main-controller-regeneration-201105/`.
Model spans are still record-level; dependency extraction remains unimplemented.
Do not equate parser gaps with damaged sources or unit-test PASS with functional
description completeness. Independent functional-role/context interpretation,
functional synthesis and publication acceptance remain required. The observed
section1.4 materialization is not a successful block-level explanation.

### 1. Ownership and execution boundary

There is one descriptive contract to implement at the existing shared assembly
boundary in `scripts/workflow_routing.py`, not a separate engine per document.
The existing central downstream
validator in `scripts/validate_downstream_coherence.py` remains the authority
provider for snapshot, allocation, ownership, partition and approved-context
resolution. `scripts/spec_document_contract.py` remains the normalized-input and
final-materialization boundary. Do not introduce a second authority resolver or
a parallel stage-specific semantic policy.

Generators supply centrally resolved inputs and an explicit versioned profile,
then render supported derived claims through their existing document formatters.
Adapters preserve source constructions and dependencies; they do not decide
authority or publication acceptance. The common synthesis boundary plans claims
and sections before producing prose. Profile controls are explicit centrally
registered data, not generator-local branches or lexical acceptance shortcuts.
Project values come only from selected approved context, never reusable examples.

The redesigned flow is:

`approved-context resolution -> intact evidence admission -> typed propositions
and dependencies -> profile-level obligations -> functional-claim synthesis ->
section plan and information-gain checks -> explanatory prose -> independent
semantic-fidelity validation -> independent publication-quality validation ->
final Markdown/DOCX materialization validation`.

Evidence, claim, section and output dispositions accompany every boundary. The
composer is not the semantic oracle, and an audit is not a second authority store.

### 2. Shared integrity invariants

These rules apply unchanged to every profile and hierarchy level:

1. Preserve exact normative text, IDs, Covers, allocation, revisions, ownership
	and immutable snapshot identity. Description is derived, never new authority.
2. Keep source evidence intact, with source/revision identity and exact locations.
	Preserve enclosing context, clause boundaries, continuations and explicit
	references needed to interpret a proposition. Stage 2+ remains artifact-only.
3. Preserve relation type, direction, endpoints, actor, object where applicable,
	result, polarity, guard, mode, alternatives, exceptions and essential qualifiers.
	Containment, interaction, responsibility and state transition are not equivalent.
4. Preserve explicit dependency and sequence edges. Input order, neighboring
	sentences, shared names and grouping never establish temporal order or causality.
5. Aggregate only semantically compatible propositions. Distinct guards, actors,
	destinations, modes, branch operators, quantities or polarity remain distinct.
	Equivalent descriptions may share prose but retain every contributor identity.
6. Every admitted span and supported proposition has a disposition. No silent
	truncation, top-k selection, facet cap, parser-driven exclusion or normative-only
	retention may hide essential meaning. Pagination cannot reduce semantic coverage.
7. Render complete, readable, non-normative technical propositions. Remove normative
	modality only from prose without converting optional or conditional behavior into
	unconditional capability. Keep process language, raw source markers and coverage
	statistics in audits, not technical description.
8. Validate source-to-model meaning and model-to-final claims independently of
	composer parity. Literal phrases, term counters, contributor presence, names,
	fingerprints and normative-section occurrences are ancillary integrity checks,
	never sufficient semantic or publication acceptance.
9. Missing approval, incomplete source, context conflict and unsupported projection
	are different failures. Keep each explicit; never invent a completion or repair
	authority to make a generated document pass.
10. Identical approved inputs and profile/adapter versions produce reproducible,
	 local-only, deterministic outputs. Unknown or altered profiles fail closed;
	 no fallback to another document's policy or a legacy local renderer.
11. Preserve independently supported meaning at proposition/dependency granularity,
	 not all-or-nothing record granularity. A gap in one clause cannot silently
	 suppress a complete independent clause. Never publish a partial claim if its
	 missing restriction or dependency would make that claim misleading.
12. Every published section adds supported information at its declared level.
	 Splitting a purpose sentence into titled repetitions is not information gain.
	 Naming a component does not explain its role, nor does one transition establish
	 its lifecycle. Semantic fidelity, publication quality and format fidelity are
	 separate obligations; success in one cannot compensate for failure in another.

### 3. Typed structural model before prose

Reuse `NormalizedSourceRecord` and `SemanticUnit` as input and materialization
contracts. Evolve the shared fact model deliberately, with versioned audit
compatibility, rather than extending a subject/action/object sentence template
one failing construction at a time.

| Model element | Required meaning |
| --- | --- |
| Evidence record | Exact admitted text, snapshot/context binding, source/revision identity, locations, explicit owner/domain/layer and enclosing context. |
| Proposition | Stable derived identity, typed relation or predicate, exact source spans, actor/endpoints as appropriate, affected objects if present, result and qualifiers. Intransitive behavior is valid; an artificial object is not required. |
| Structural relation | Explicit containment/composition, responsibility, directed interaction, data transformation, configuration dependency, state transition or other centrally declared relation. Preserve the container and children separately from the enclosing block. |
| Context expression | Scoped guards, modes, conjunction/disjunction, negation, alternatives and exceptions attached to the propositions they qualify; not a detached string shared indiscriminately by a paragraph. |
| Dependency edge | Source-supported initiation, completion, before/after, causal or referenced-context dependency with explicit endpoints and source spans. Resolve references only against admitted evidence. |
| Functional claim | A supported responsibility or relationship, affected entities, result, scoped conditions/alternatives and explicit dependencies, target section role, abstraction/detail decisions, exact proposition/span contributors and a versioned synthesis rule. A claim may have many sources; one source may support several claims. It is not a sentence template or aggregate architecture inferred from mentions. |
| Section plan | Ordered claim assignments, intent, supported information contributed beyond earlier sections, references to shared context, and dispositions for omitted or unresolved essential meaning. A heading or extra sentence alone is not a new contribution. |
| Publication realization | Complete explanatory prose or a supported structured presentation linked to claims, exact identifier roles, a declared versioned realization rule and independently checked semantic obligations. Surface wording need not mirror source clauses. |
| Disposition | Preserved, justified excluded or unresolved at span and proposition level, with rule identity, rationale and any representative claim/dependency link. |

The shared relation schema is not an architectural discovery mechanism. Entity
mentions cannot create containment, a component, a responsibility or an owner.
Keep supported propositions separate from unresolved dependencies. Preserve a
complete independent proposition even when another clause in its source record is
unresolved. Construct the minimum source-supported dependency closure needed to
interpret each candidate claim: guards, exceptions, quantities, references and
completion/sequence restrictions must either be resolved or explicitly block it.
If closure is complete, publish its bounded meaning and retain the other gap.
If closure is incomplete and omission would broaden or misattribute the claim,
withhold only the affected claim and record the precise reason and affected spans.
An essential unresolved gap still blocks clean release acceptance; useful partial
publication must not imply complete coverage or fabricate a missing continuation.

### 4. Profile-controlled application

The common descriptive strategy is purpose -> responsibilities/capability families
-> boundaries -> explicit organization -> supported operating behavior. Profiles
map those roles into the existing document sections and determine abstraction,
detail policy and presentation. This is a content strategy, not one forced heading
layout for all documents. Scope, approval, ownership and admissibility are resolved
by the central authority contract, not loosened or rediscovered by a profile.

| Profile | Scope and abstraction | Profile-controlled application |
| --- | --- | --- |
| SRS | Approved system-level capability and explicitly admitted architecture context. | Preserve the frozen introduction/terminology rule and seven overview roles. Explain system identity, capabilities, domains, external boundaries, operating concept, top-level power/clock/reset and engineering limits. Do not promote block-local signal/register detail into system capability. |
| DRS | Approved digital/top-digital/shared integration context. | Explain digital organization, resource responsibilities, access, interfaces, directed connections and operating/power integration. Retain supported numerical engineering values and owner-scoped tables. Known behavior first, supporting tables second, narrow clarification last. Local behavior cannot establish top-level integration authority. |
| ARS | Approved analog/mixed-signal/shared integration context. | Explain analog responsibilities, interfaces, operating conditions, supply/bias and supported domain/sequence relationships. Retain essential physical quantities and restrictions without inheriting digital operating assumptions. |
| Digital IPOS | Approved same-owner digital block-local scope. | Explain block purpose, capability families, boundaries, explicit internal organization and supported local behavior. Retain configuration, signal, timing and calculation relationships when essential. Do not inherit SRS implementation-detail exclusions. |
| Analog IPOS | Approved same-owner analog block-local scope. | Use the same block-level roles and shared integrity rules; apply analog operating conditions, physical quantities and local supply/bias behavior only where supported. No digital signal/FSM assumption. |

Each runtime profile explicitly declares identity/version, document target,
abstraction level, detail policy, section intents/role mapping and presentation
style. Runtime registration separately binds the profile to centrally resolved
authority tiers, evidence kinds, owner/domain/layer/scope, adapter versions and
activation. These bindings are mandatory execution boundaries, not profile knobs
for changing source truth or shared integrity. Digital and Analog IPOS may share
a block-profile base; callers supply an explicit centrally resolved domain.

Profiles may control whether a source-supported detail belongs at their level;
they may not weaken direction, guards, polarity, dependency or coverage checks.
An exclusion needs a profile rule and rationale, not merely a matched word.
Presentation profiles remain derived metadata and do not alter approved workflow
profiles or snapshot authority. Changes to frozen SRS preferences require separate
explicit authorization, not incidental migration.

No profile may substitute a verb allowlist, entity-name suffix, lexical topic
score or identifier occurrence for a functional relationship or its fidelity.
Vocabulary may help name an already supported claim; it cannot supply purpose,
approval, interaction, sequence or eligibility. A presentation preference for
brevity may split prose or move nonessential detail, never cap essential meaning.

### 5. Synthesis and publication contract

#### 5.1 Explicit functional-claim synthesis

Synthesize claims before composing sentences. Apply versioned local rules to the
admitted proposition/dependency model; no LLM, remote service, similarity-based
semantic approval or unbounded natural-language equivalence is required or allowed.
The output is a claim plan, not prose generated directly from atomic facts.

For each supported responsibility or relationship, record its functional subject,
action/role, affected objects/endpoints, result, complete interpretation context,
dependencies and exact contributors. Identify capability families from supported
relationships at the profile's abstraction level, not from a project catalogue,
shared actor name, generic verb family or a list of register writes. Grouping
establishes explanatory membership only, never containment, temporal order or cause.

Combine complementary propositions only when their supported relationships justify
one explanation. Keep distinct conditions, alternatives and outcomes explicit
within that explanation. Reuse shared context through a resolved claim link only
when its scope is unambiguous; do not silently apply one guard to all contributors.
Every synthesized relation and connective requires source-supported obligations.
Headings name the supported role and extent, not a subject fragment or a larger
lifecycle/algorithm than the claim actually establishes.

#### 5.2 Enforceable section-role obligations

Purpose describes the supported overall role. Capability families describe distinct
responsibilities rather than raw subjects or one entry per requirement. Boundaries
retain relevant limits and exclusions. Internal organization states explicit
container/child relationships before explaining each child's responsibilities and
supported interactions. Operating behavior preserves relevant initiation,
evolution, completion and dependencies only where the source attests them.

| Section role | Required contribution | Publication rejection |
| --- | --- | --- |
| Purpose/functionality | Concise overall responsibility and intended supported result at the declared level. | Inventory clauses repeated as a list, implementation-step instructions or unsupported promises of completeness. |
| Capabilities/supported scope | Distinct supported responsibility families plus applicable boundaries, limits, modes or exclusions not already explained by purpose. | A purpose sentence split into heading/body duplicates; an I/O list used as a substitute for functional scope. |
| Organization | Explicit supported containment/composition and child responsibilities or interactions. | Organization inferred from names, co-occurrence or an FSM label; an isolated behavior presented as aggregate structure. |
| Detailed functions/operating behavior | A coherent extension of a capability: relevant initiation, evolution, result/completion or interactions, only where attested. | One atomic condition or register write pretending to explain a function; wholesale repetition of the capability entry. |
| Interfaces/boundaries/limits | Supported endpoints, access, operating restrictions and essential quantities placed at the appropriate level. | Unstructured field dumps, detached values, duplicate I/O text or removal of constraints needed to interpret a claim. |

Information gain is a claim-level obligation, not a word-count or phrase-similarity
score. Each section/entry records which responsibility, relationship, restriction,
result or dependency it adds relative to prior descriptions. A detailed section
can refine an existing capability but must add an explicit supported obligation;
renaming, re-inflecting or repeating the same predicate/object is not refinement.
Repeated names or essential context are allowed where needed for clear reference,
but not duplicated explanations or heading/body tautologies.

Profiles map these roles to their existing section layout. A required section
without a supported, nonredundant contribution is a section-intent gap, not a
license for a duplicated purpose template. An optional empty section is omitted
with a disposition. Numbering/layout cannot determine whether a function is known.

#### 5.3 Detail, paraphrase and disposition

Essentiality is decided at the explicit profile level: omitting the proposition
must not change the reader's understanding of responsibility, organization,
conditions, behavior, result or limits at that level. Not every normative row needs
a descriptive bullet. Do not flatten tables/formulae/procedures into prose; retain
their structured meaning or a supported qualitative claim plus the applicable
detail disposition. Existing normative/table preservation rules remain mandatory.

| Disposition | Acceptance obligation |
| --- | --- |
| Preserved | Link to actual claims in the correct descriptive role, preserving all essential relation/context/dependency semantics. Equivalent paraphrase and many-to-many synthesis are allowed. |
| Justified excluded | Record source span, explicit profile rule and reason. Equivalent duplicates link to their representative and retain all provenance. Nonessential detail may be excluded only without losing its functional effect or restriction. |
| Unresolved | Retain evidence and classify missing approval/context, incomplete or ambiguous source, conflict, unresolved reference or unsupported construction separately. An essential admitted unresolved proposition blocks clean acceptance. Unapproved discovery remains review-only. |

Valid explanatory paraphrase is allowed when the same semantic obligations remain
true. Active/passive realization, role-first wording, coordinated explanations,
approved terminology and resolved references can differ from source phrasing.
Use explicit centrally versioned semantic-preserving realization/equivalence rules
with positive and negative fixtures, not arbitrary synonyms or token overlap.
The independent verifier checks the preserved relationships and scoped context;
it must not demand the source sentence as a contiguous substring. Unrecognized
realizations are unresolved, not certified by resemblance or by the composer.

Treat identifiers as typed references. Preserve exact technically necessary signal,
register, port and state identities; explain their functional role when retained.
An approved readable label may supplement, not silently replace or conflate, an
identity. Do not globally replace separators, lowercase identifiers or expand
abbreviations by guesswork. Omit nonessential encoding only with a profile-level
disposition and preservation of the controlled behavior/restriction elsewhere.

Concise headings identify functions or responsibilities, not pronouns, signal
fragments or copied guards. Section roles must add information rather than repeat
purpose prose. Prose must be grammatical and complete, with no dangling condition,
unfinished predicate, concatenated table dump or synthetic grammatical suffix.
Source identifiers remain exact when technically necessary; readability must not
erase identifier distinctions. Natural prose quality is a separate acceptance
dimension from source linkage and artifact fidelity.

### 6. Independent verification and acceptance

Use existing stage gates and the central validator; no parallel validator authority.
Verify the intact admitted-source inventory against typed propositions/dispositions,
then those propositions and dependencies against claims in actual section-scoped
Markdown and DOCX. Independently authored expected relations and mutation fixtures
must not derive their expected answer from the same composer/projector.

#### 6.1 Semantic-fidelity validation

Derive interpretation obligations from admitted source spans and their supported
context, independently of composer selection. Verify source -> propositions ->
functional claims -> actual section-scoped realizations. Check relation identity,
actor/endpoints/direction, result, guards and dependency scope, polarity, modality,
alternatives, exceptions, quantities/units and profile-approved abstraction.
Validate every retained, excluded and unresolved span/obligation; any source
construction outside the bounded verifier remains an explicit gap.

Contributor presence, exact phrase retention, term counters, recomputed hashes,
model/audit agreement and composer parity may support traceability or artifact
integrity at applicable boundaries, but cannot individually or collectively stand
in for semantic interpretation. A changed relation can retain the same words and
contributors; a valid paraphrase can change the words while preserving the relation.
Prove both cases in tests. Reconstruct output meaning using supported independently
checked realization rules, not a call to the projector to obtain its expected text.

#### 6.2 Publication-quality validation

Check the actual section-scoped Markdown and DOCX against claim/section intent,
independently of semantic-fidelity and format agreement. The same rejection classes
apply to every profile; only abstraction, detail placement and style expectations
differ. Publish deterministic rule IDs, section/claim/span locations and reasons.

| Rejection class | Required failure condition |
| --- | --- |
| Fragmentation | Incomplete predicates/guards, disconnected micro-steps, concatenated fact dumps or atomic entries lacking the claimed functional explanation. |
| Redundancy/tautology | Duplicated purpose across sections, repeated claim content without supported refinement, heading/body repetition or cosmetic reformulation counted as information gain. |
| Misplaced detail | Encoding/instructions dominating a purpose/scope role, necessary restrictions detached from their claim, or operating detail rendered as unsupported organization. |
| Grammar/cohesion | Agreement/tense defects, broken coordination or references, dangling modifiers, synthetic inflections or prose incompatible with its versioned grammatical realization. |
| Misleading headings | A name promises a full lifecycle, algorithm, responsibility or aggregate structure while its claims establish only a narrower behavior. |
| Identifier handling | Altered/conflated identifiers, guessed expansions, raw technical-field lists without functional explanation, or removal of identities essential to the relationship. |
| Requirement-like leakage | Copied requirements with only modality removed, register-write recipes replacing capability explanation, normative wording or source/audit scaffolding in descriptive sections. |

Technical conditions, quantities and identifiers are not forbidden merely for
being detailed: they fail when unintegrated, wrongly placed or misleading at the
profile's level. Likewise, a conditional explanation can be legitimate prose.
Do not implement quality as a list of banned words or an unsupported general
grammar guarantee. Each permitted realization must have bounded deterministic
quality checks and adversarial fixtures; unsupported quality assessment is a gap.

#### 6.3 Materialization and release decision

Separately verify claim placement, identifiers, ordered structured content, links,
tables and Markdown/DOCX equivalence. Literal hashes or token checks can serve this
format boundary without defining the allowed semantic paraphrases.

Report `semantic_fidelity`, `publication_quality` and `materialization` separately
as PASS, FAIL or UNRESOLVED, with findings and supported-construction scope. Clean
release requires all three PASS, complete essential dispositions and valid central
authority binding. Partial output remains explicitly nonaccepted when any essential
obligation is unresolved; a polished paraphrase cannot hide missing meaning, and
exact semantic copying cannot waive publication defects. Profile activation and
broader rollout remain separate explicit execution decisions.

Required mutations include loss/reversal of containment, substitution of the
container with its enclosing block, swapped interaction endpoints, deleted guards,
polarity inversion, AND/OR changes, merged alternatives, optional-to-unconditional
promotion, invented sequence, lost numeric units/operators, unresolved dependency
omission, unsupported extra claims and moving a claim to a normative-only section.
Persisted fact/audit/hash mutations together must not manufacture semantic PASS.

Cross-profile fixtures use generic entities and evidence, covering composition,
intransitive behavior, multi-clause dependencies, contextual references, quantity
and calculation meaning, complete versus incomplete source and conflicting context.
Apply shared mutations to every profile. Paired profile tests must show why local
detail is retained in IPOS but excluded or abstracted in SRS, and why digital and
analog integration remain distinct without weakening common integrity rules.

Release acceptance requires no unresolved essential admitted meaning, no unapproved
or invented claim, complete dispositions, correct profile abstraction/section roles,
readable technical prose and final Markdown/DOCX fidelity. Report source projection,
profile selection, publication quality and materialization separately; an aggregate
test count or valid-empty profile cannot certify another profile's real artifacts.

Add publication regression fixtures for purpose/list tautology, duplicated claims
across sections, isolated field instructions masquerading as functions, misleading
headings, malformed coordinated predicates and identifier separator loss. Include
semantically faithful but badly published prose and well-written but semantically
wrong prose: the checks must reject them for different reasons. Positive fixtures
must accept coherent many-source explanation and valid paraphrase, preserve an
independent complete clause next to an unresolved dependency, and withhold a partial
claim whose unresolved qualifier makes publication misleading. Run these common
fixtures across SRS, DRS, ARS and both IPOS profiles without changing their activation.

### 7. Ordered implementation and rollout

1. **Contract definition (documented here).** Fix shared invariants, typed model,
	profile matrix, essentiality and independent acceptance before implementation.
	Reconcile historical instructions as part of the central contract migration;
	do not use them to preserve conflicting local policy.
2. **Shared model and checks.** Evolve the existing core and audits with explicit
	schema/version handling. Represent clause spans, scoped dependencies, functional
	claims, section plans, realization rules and separate acceptance results. Prove
	partial-meaning preservation and fidelity mutations before changing activation.
3. **Central profile and section obligations.** Encode abstraction/detail/style
	and section intents with claim-level information gain. Bind scope through the
	existing authority resolver. Preserve frozen SRS and established DRS conventions.
4. **Functional-claim synthesis and realization.** Implement compatible many-source
	claims, supported qualitative explanations and semantic-preserving paraphrases
	in the common boundary. Test generic examples without a project catalogue or
	legacy paragraph fallback. Do not compose prose directly from raw atomic facts.
5. **Independent semantic and publication checks.** Implement separate bounded
	checks in existing gates, with negative mutations and independent expected
	relationships. Replace tests that require duplicated templates or only literal
	phrase presence; retain those checks solely where artifact integrity requires.
6. **Adapter and caller reconciliation.** Preserve intact artifact context and
	explicit relations, replace record-wide suppression with dependency-aware
	dispositions, and wire existing generators to the same claims/section results.
	Reconcile conflicting legacy instructions during migration; no ID/name repair
	branches, local selection policy or automatic profile activation.
7. **Real-artifact verification.** Capture preservation baselines, regenerate each
	affected authorized profile at the same selected snapshot and run its full gate
	plus central coherence. Compare supported relationships and explanatory roles
	with the prior baseline, not only names or counts. Require semantic, publication
	and materialization PASS; preserve authority, tables, history and protected data.

The sequence is contract -> claim/dependency model -> profile/section obligations
-> functional synthesis -> independent acceptance checks -> adapters/callers ->
controlled materialization, not repeated local parser patches. Source-authority recovery, if
needed, remains a separately tracked approval-boundary task; it cannot be hidden
inside descriptive redesign. Do not claim rollout completion while a required
profile or essential real-artifact construction remains unverified or blocked.

### Shared-model implementation checkpoint (2026-10-08)

Phase 2 implements the opt-in typed structural model and checks in the existing
`scripts/workflow_routing.py` boundary. It does not replace `DescriptiveFact`,
`run_descriptive_flow`, any adapter or any generator call. No runtime profile was
activated or changed, and no specification, canonical data or snapshot was written.
There is no fallback from the new model into the legacy renderer.

Implemented:

- Immutable typed source spans, Boolean contexts, meanings, propositions,
	dependencies, claims, dispositions and a versioned structure bundle. Source
	spans use exact offsets into intact `NormalizedSourceRecord` text and inherit
	its provenance. Claims bind to existing `SemanticUnit` objects.
- Typed relation identity and direction, intransitive behavior without a fabricated
	object, explicit contexts, optional behavior, polarity, alternatives, qualifiers
	and results. Unsupported relation/context forms are findings, not inferred facts.
- Shared source-span, identity, scope, claim/model equality, dependency linkage and
	cycle, unit ordering and complete span/proposition/dependency coverage checks.
	Missing or changed links cannot be hidden by an audit ID or generic heading.
- Explicit unresolved dispositions remain blocking. At this phase, exclusion is
	supported only for an equivalent duplicate with a preserved representative and
	complete contributor linkage; profile-level detail exclusions await phase 3.
	A preserved disposition cannot account for an unmodeled span.
- A separate derived audit schema `DESCRIPTIVE_STRUCTURE_VERSION = 1.0`, with exact
	profile fingerprint and full typed structure. It leaves the existing document
	contract and runtime audit schemas unchanged. Audit validation uses an externally
	supplied expected structure and rejects changed, missing or extra payload fields;
	no audit deserialization or schema fallback is enabled.

The audit deliberately reports only `typed_model_status = model_valid | blocked`.
It marks source-semantic and final-prose validation `not_implemented`. These checks
verify the supplied model, not whether an adapter interpreted the source correctly
or whether actual Markdown/DOCX prose expresses the claims. Even matching typed
claims and source offsets are not semantic proof. The new dependency cycle check
rejects unmodeled cyclic ordering; iteration/occurrence context must be represented
explicitly before such behavior can be supported, not guessed from a graph.

Verification: 108 existing/new descriptive tests, 9 document-contract tests and
19 SRS downstream-coherence tests pass (136 total). Eleven new test methods cover
composition, intransitive behavior, cross-profile relation mutations, Boolean and
optional context, quantities, exact spans, dependencies, duplicate provenance,
dispositions, versions, audit round trips and unsupported profile/input boundaries.
DRS/ARS checks inspect model integrity without activating their runtime profiles.
The runtime module has no editor diagnostics. Test-module unresolved-import
diagnostics remain in the existing dynamic `sys.path` setup; unittest resolves the
imports and passes. No editor/interpreter configuration was changed.

Next is phase 3: central profile-controlled roles, abstraction and essential-detail
decisions with paired fixtures. Context-preserving source adapters, independent
source interpretation, actual final-prose validation, caller migration and real
artifact regeneration remain later phases. The previous real IPOS semantic blockers
have not been rechecked, relaxed or resolved by this model-only implementation.

### Profile-application implementation checkpoint (2026-10-08)

Phase 3 adds an opt-in application layer in `scripts/workflow_routing.py`, without
changing the existing writing profiles, their fingerprints, activation, adapters
or generators. Five centrally registered immutable policies distinguish SRS,
DRS, ARS, Digital IPOS and Analog IPOS. Domain and hierarchy metadata are explicit;
there is no owner-name, heading, keyword or default-digital classification.

- Canonical purpose/functions/organization/boundaries/limits/operating-concept/power
	roles map to existing profile sections. Containment remains organization, not
	a capability. IPOS requires distinct supported purpose and function roles.
- Profiles declare abstraction targets, admitted domains/layers, omitted detail
	kinds and behavior -> support -> clarification presentation order. This records
	policy; it does not yet transform meanings or compose prose/tables.
- Each proposition has an explicit assessment and deterministic decision with a
	rule, section and abstraction target. No missing/duplicate/extra assessments,
	altered policies or mismatched writing profiles are accepted. Incomplete source,
	unsupported constructions, conflicting context, missing approval and unresolved
	references remain unresolved before any profile exclusion can be proposed.
- Nonessential encoding is omitted only by SRS. Examples/procedures may be omitted
	by each profile, but explicit essential aspects, dependencies, composition,
	conditions, modes, modality, negative meaning, qualifiers and results prevent
	that detail-based omission. DRS/ARS/IPOS retain encoding and engineering detail.
- Versioned application audits retain complete propositions, assessments,
	dependencies, decisions and supplied structure. They rerun the same phase-2
	structural validator; absent/invalid structures or changed inventories block
	acceptance even if a proposition was proposed for profile exclusion. Expected
	inputs are supplied independently; modified audit payloads cannot certify PASS.

The application result is a selection proposal, not a new disposition or publication
path. The existing model still accepts exclusion only for equivalent duplicates;
conversion of profile decisions into projected claims/dispositions belongs to the
adapter/migration phases and must preserve shared coverage integrity. Assessments
are explicit supplied metadata, not verified interpretations of raw source.
`profile_status = policy_valid` means only policy plus supplied-model integrity.
Source-semantic validation, final-prose validation and runtime migration remain
`not_implemented`; no fallback or full semantic PASS is claimed.

Verification: 116 descriptive, 9 document-contract and 19 SRS downstream-coherence
tests PASS (144 total). Eight added test methods cover paired hierarchy/detail and
digital/analog behavior, composition roles, essential qualifiers/dependencies,
unsupported constructions across all profiles, inventory/policy tampering, required
IPOS roles, audit round trips and common integrity under proposed exclusions.
Both touched Python files have no editor diagnostics. No specifications, canonical
data, snapshot, approval, allocation or normative text were written or regenerated.
Earlier Digital IPOS/central semantic blockers remain unrechecked and unresolved.

Local checkpoint: `2026-10-08-top-down-profile-application-phase3`; no Git save.
Next is phase 4: context-preserving artifact-only adapters and independently checked
source assessments, before caller migration, publication checks and regeneration.

## Historical implementation and diagnostic checkpoints

The following text records earlier behavior and decisions. Where it conflicts with
the current top-down redesign, use the current contract above for future work.

IPOS descriptive rendering is deterministic, local-only, and non-authoritative. It uses the complete set of accepted same-block evidence already recorded in the descriptive audit.

For each supported internal function or capability family, the shared renderer:

- preserves every distinct supported responsibility and explicit local interaction;
- deduplicates only equivalent responsibility phrases;
- orders contributors by accepted evidence order;
- omits unsupported relationships and unsafe raw implementation detail; and
- records contributor IDs, deterministic aggregation order, selection mode, and suppression reasons in `descriptive_summary_audit.csv`.

RRF is not used for IPOS descriptive rendering, facet selection, or audit fields. RRF remains restricted to Hybrid RAG retrieval/query fusion and retrieval benchmark paths.

## Shared rollout (2026-09-29)

The same `1.2` role-first materialization and quality checks now apply through
the shared composer and validators to every materialized Digital and Analog IPOS
block. Generation, the IPOS gates, and downstream coherence use the same complete
approved snapshot candidate set; no additional authority inputs or block-specific
rendering rules are introduced. A block with truncated action text, procedural
filler, or a weak standalone title must be reported as failing the descriptive
quality contract even when its traceability and document structure pass.

## Main Controller 1.2 pilot baseline (2026-09-29)

This historical pilot baseline applied to Digital IPOS Main Controller at approved snapshot
`snap-b2e8101b00dc6909feaed885`. Shared final-materialization and validation
rules are in `.github/skills/workflow-stage-gate/SKILL.md`; this record fixes the
pilot identity and output; the later authorized all-block prose rollout supersedes
these artifact hashes. The shared rollout does not alter Stage 2a,
the snapshot candidate universe, or authored requirements.

- `1.2` has 12 function bullets: 52 accepted candidates merged, 4 standalone,
	and 2 intentionally suppressed atomic candidates in the descriptive audit.
- The ALC compensation handoff belongs to PPG FSM, not a standalone function.
	Soft reset (`DDS_STBIO1_1114`) and chopper clock
	(`IPOS_STBIO1_MAIN_CONTROLLER_077`) remain suppressed atomic candidates.
- Standalone function bullets require independent behavior; the shared validator
	rejects raw-identifier headings and incomplete action fragments. Display names
	are readable, openings describe roles, interactions are source-backed, and
	Markdown/DOCX preserve the same audited semantic-unit order.
- SHA-256 of `artifacts/stage6_digital_ipos/blocks/main-controller/digital_ipos_main-controller.md`:
	`6B4B5D3D89F91AA9227AA8A203B183BCF44C7FD1A1DE1D250FFA525B7B79754B`
- SHA-256 of `artifacts/stage6_digital_ipos/blocks/main-controller/descriptive_summary_audit.csv`:
	`CDAD4C078F97A153766AD6AC88AEA7B7417DCE717A98DF55CAB00298B4DFAB05`

The old hashes are retained only for comparison; the current shared renderer
does not reproduce the pre-rollout pilot Markdown from this snapshot. For a
full rollout, gate all blocks without `--block` and run the central downstream
validator against the same snapshot. Regeneration may remain scoped to the
outliers, but scoped gate results cannot substitute for a full gate.

### Full rollout validation

At snapshot `snap-b2e8101b00dc6909feaed885`, all eight Digital block documents
were regenerated with the shared composer. The Analog partition regenerated as
valid-empty (0 requirements, 0 blocks) and its gate passed. Focused descriptive
tests passed (57). The full Digital gate is **blocked** by descriptive quality;
downstream coherence reports `BLOCK_DOWNSTREAM` with six quality findings across
five blocks:

| Digital block | Descriptive quality findings |
| --- | --- |
| ADSP | `Local copy function`; `Operation control and data routing` |
| I2C_SPI_AHB | `Operation control and data routing` |
| PMU | `Local manage function` |
| Sensor-Hub | `Local reset function` |
| Smart FIFO | `State and processing synchronization` |

Main Controller, PAD MUX, and Regmap had no descriptive findings at this point;
the latter two have no accepted 1.2 refinement bullets. No new authority inputs
or block-specific rendering rules are permitted for this repair.

### Five-block quality repair

Only ADSP, I2C_SPI_AHB, PMU, Sensor-Hub, and Smart FIFO were regenerated from
the same approved snapshot. The shared final renderer now names a behavior and
retains its supported guard or destination from accepted local statements. The
six earlier weak summaries became:

| Block | Before | After |
| --- | --- | --- |
| ADSP | `Operation control and data routing` | `Operation start conditions`: quokka_run low, selected OTP bit set, and BOOT initiation |
| ADSP | `Local copy function` | `OTP memory transfer`: OTP memory to registers and regmap to memory |
| I2C_SPI_AHB | `Operation control and data routing` | `Read data preloading`: AHB preload after double-byte address write, ahead of master read |
| PMU | `Local manage function` | `Power-on start-up`: POR release, LDO1V8 turn-on, and clock start-up sequence |
| Sensor-Hub | `Local reset function` | `Register reset on operation start`: registers reset at each new I2C operation |
| Smart FIFO | `State and processing synchronization` | `Memory mode entry`: HMASTER value condition retained |

Sections 1.1 and 1.2 in these five documents now use the inventory function and
I/O as natural introductory prose instead of the earlier `approved macro-purpose`
and `approved ... function` scaffolding. The 58 focused tests and all five scoped
Digital IPOS gates pass. The read-only full downstream check no longer reports
any of the original six quality findings, but remains `BLOCK_DOWNSTREAM` with
six `scope_mismatch_with_block_authority` findings on the unchanged Main
Controller, Pad Mux, and Regmap 1.1/1.2 openings. Those documents were not
regenerated during the five-block repair; Main Controller retained the pilot
hashes at that point. This was a scoped result, not a global PASS.

### All-block natural-prose rollout decision

The approved follow-up decision was to retire the Main Controller pilot freeze
and regenerate only the three remaining outliers (Main Controller, Pad Mux, and
Regmap) against `snap-b2e8101b00dc6909feaed885`. General Rules, the central
workflow execution contract, the orchestrator, and the shared output validator
now require natural technical prose in `1.1` and `1.2` in every current and
future materialized IPOS block. The shared validator independently rejects
approval/process wording even when a document agrees with composer output;
the IPOS gate also checks final DOCX fidelity. No new authority inputs,
block-specific wording rules, or changed candidate decisions were introduced.

The three regenerated documents replace `approved macro-purpose` and `local
scope covers the approved ... function` with inventory-bounded technical
sentences. Pad Mux now preserves the compound `register-map controls` in its
1.2 opening. The current Main Controller SHA-256 values after the Windows
display-name author refresh are:

- Markdown: `64A4256BCD353F44BAA693102B19663BA86414BC29017349ECCACCDEDC8C3F89`
- Descriptive audit: `46231A50CF86466142438A29165448E78FADD2C75FDC8EE24BCC9D7B358101C5`

The pre-author-refresh Markdown hash was
`37E0C4030514B3A982638A4AB758107193078DBB93B5178C5B7FF6CE2ABD2FE3`.

At this snapshot the 60 focused descriptive tests PASS; the full Digital IPOS
gate PASSes (259 requirements, 8 blocks); the Analog IPOS gate PASSes as
valid-empty (0 requirements, 0 blocks); and full read-only downstream coherence
PASSes with zero findings. This is the global rollout result, not a scoped
waiver of the earlier six mismatch findings.

## Structural-integrity diagnostic baseline and finalized plan (2026-10-08)

Status: planning only. No runtime code, tests, generated specifications, approved
data, or snapshots were changed for this assessment. Historical PASS results above
establish the checks run at those dates, not semantic completeness. Implementation
requires separate authorization of this finalized plan.

### Scope and method

This is a general Digital/Analog IPOS descriptive structural-integrity repair.
Main Controller is an initial regression example, never executable policy or scope.
The existing central materialization resolver at snapshot
`snap-b2e8101b00dc6909feaed885` reports eight Digital blocks and zero Analog blocks.
The baseline reads each existing overview, descriptive CSV audit, and materialization
JSON audit, joined to the central block identities. No source PDF was reread and no
generator or gate was run. Analog is valid-empty in this baseline; generic Analog
fixtures are still required before a future rollout.

Candidate counts below are same-label rows in the existing descriptive audit, not
approved normative partition counts. A block-local label alone does not establish
eligibility. Their differences must be reconciled against exact central snapshot
identities, allocations, and source revisions, not hidden by set intersection.
Summary groups exclude the inventory-based introductory sentence.

| Block | Approved IPOS rows | Local audit candidates | Accepted | Accepted but atomic-excluded | Rendered groups | Diagnostic result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| ADSP | 19 | 20 | 4 | 0 | 2 | Confirmed context flattening: BOOT memory-to-register transfer and WRITE regmap-to-memory transfer are merged without their separate operating contexts. Operation-start guards and alternatives are retained in another summary. |
| I2C_SPI_AHB | 15 | 15 | 1 | 0 | 1 | Preload summary retains address-trigger and read-request context. Fourteen local candidates are excluded; complete functional relationships versus legitimate detail exclusions require independent review. |
| Main Controller | 138 | 141 | 58 | 2 | 12 | Confirmed role/composition gap and FIFO guard loss. Source requirement suffix `_008` maps to generated `-018`, not generated `-008`. Two accepted atomic candidates have no summary. |
| Pad Mux | 17 | 17 | 0 | 0 | 0 | Approved mode-selection and routing relationships receive no refinement summary. Sixteen candidates are classified as normative reuse; the DCC candidate is rejected for inventory support. Do not fix possible ownership conflict by reallocation. |
| PMU | 31 | 31 | 1 | 0 | 1 | POR-triggered start-up meaning is retained. Twenty-four normative-reuse and six table/signal exclusions require semantic review; counts alone do not prove loss. |
| Regmap | 8 | 10 | 0 | 0 | 0 | No refinement summaries. The conditional OTP write-protection fact is absent from the overview. Table fragments, procedures, and scope conflicts must be distinguished; do not turn register tables into copied I/O or inferred requirements. |
| Sensor-Hub | 18 | 23 | 1 | 0 | 1 | Operation-start reset summary is retained. The I/O opening reproduces inventory text `Primary sensing input` / `Analog input signal`, inconsistent with the stated digital I2C-master role. This is an upstream context conflict, not permission for a renderer correction. |
| Smart FIFO | 13 | 13 | 2 | 0 | 1 | Two distinct IDs with equivalent text contribute to one guarded memory-mode summary. Eleven exclusions need review; inventory preserves mutually exclusive Unique/Multiple modes. Deduplication must retain both provenance identities. |

Main Controller atomic exclusions are `DDS_STBIO1_1114` (soft-reset procedure) and
`IPOS_STBIO1_MAIN_CONTROLLER_077` (conditional clock/reset timing, with an incomplete
alternative). These observations establish absent descriptive rendering, not that
every procedural micro-step belongs in an overview. Their essential functional
meaning must be assessed independently. Incomplete text must not be completed by
guessing.

### Confirmed shared gaps

1. `stage1_descriptive_evidence.py` examines an overview-heading region and stops
	at the next heading/requirement. It does not generally preserve later block
	descriptions, enclosing owner context, or explicit composition facts. Its
	name-based owner discovery cannot establish approval or ownership.
2. `build_ipos_functional_input` carries inventory fields and requirement tuples,
	not admitted block-local descriptive relations. Separate deduplication of IDs
	and texts can misalign the fallback `zip` and evidence-only audit rows. The
	current nonempty candidate-record path does not prove that fallback defect was
	exercised in this baseline.
3. Structural projection bounds action tails to 100 characters, splits on
	conditions/timing words, and separates actions, paths, and interactions into
	lists. The action-to-condition, actor-to-object, and state-to-effect relations
	can be lost before aggregation. A first-facet candidate is not a complete fact.
4. Flat entity/action-family grouping lacks explicit composition relationships,
	includes heuristic host attribution, and uses name/signal-specific rewrites.
	Combining selections and starts can introduce `then` from grouping rather than
	approved sequence evidence. Input order is not temporal order.
5. Accepted evidence may be suppressed as atomic without an independent essential
	fact disposition. The existing behavior-fragment validator explicitly skips
	atomic candidates. Normative modality and unsupported syntax must not be
	mistaken for lack of descriptive eligibility.
6. Shared normalized records retain projected text rather than an independently
	accounted inventory of source meaning. Semantic units prove contributor and
	rendered-text linkage but not preservation of every essential relation.
7. Overview validation recompares the same composer output. Existing independent
	behavior-fragment checks help with particular constructions but do not cover
	this general problem class. Structural coverage can pass from a name in audit
	evidence or anywhere in Markdown, including normative requirements.
8. The I/O composer removes the word `register` in some contexts without a modeled
	semantic-equivalence decision. Inventory contradictions are not resolved by
	accurate copying. Both transformations and upstream conflicts need diagnostics.

Upstream normative extraction also has a bounded continuation reader in
`generate_stage1_requirements.py`. Whether it caused the observed truncated
snapshot text remains unverified. Trace each suspected truncation through existing
ingestion, canonical revision, approved snapshot, and final output before assigning
a root cause. No recovery may overwrite approved text in this work.

### Essential-fact and disposition contract

An essential descriptive fact is an admitted, source-supported proposition needed
to preserve the block's functional meaning at the explicit IPOS profile level:

- an actor's responsibility, action, affected object, result, or directed interaction;
- an explicit containment/composition or other approved relation and its endpoints;
- a mode, guard, alternative branch, exclusion, negative behavior, or exception
  whose loss would broaden, narrow, invert, or misattribute that proposition;
- an explicit initiation/completion dependency or temporal relation; and
- a quantitative limit, timing bound, calculation, or configuration relationship
  where it determines functional behavior, rather than merely naming an encoding.

Classify facts by this rule, not by project names, IDs, source headings, raw `shall`,
or mandatory FSM labels. Encoding details, examples, and procedural micro-steps
may be omitted only if their functional effects and restrictions remain represented.
Some timing or register detail is essential; its syntactic form is not an exclusion.
Normative modality is removed from prose only, without promoting conditional or
optional behavior to unconditional capability.

Every candidate span and every supported proposition has one audited disposition:

| Disposition | Required evidence and consequence |
| --- | --- |
| Preserved | Link the fact to one or more rendered claims in the appropriate descriptive section; preserve actor, relation, object, polarity, alternatives, conditions, and applicable qualifiers. Paraphrase and many-to-many aggregation are allowed. |
| Excluded | Record an explicit policy reason, source span, and rationale: outside approved owner/profile, redundant equivalent fact linked to its representative, nonfunctional encoding/example detail, or nonessential procedural detail with its functional meaning linked elsewhere. Parser inability, brevity, and normative retention are not valid exclusions for essential meaning. |
| Unresolved | Record unsupported construction, incomplete/ambiguous source, conflicting authority/context, missing approval binding, ambiguous ownership, or unknown relation. Keep the evidence intact. An essential admitted unresolved fact blocks a clean structural-integrity PASS. Unapproved discovery evidence remains a review-only finding, never a rendering requirement. |

Duplicate text preserves all source/revision identities. Different polarity, guards,
modes, branch operators, actors, destinations, or sequence relations are not
duplicates. A fact may span sentences or source pages but must retain exact source
locations. Split facts retain clause/dependency links so reconstruction cannot
invent conjunction, causality, or temporal order.

### Centralized implementation plan

1. **Evidence admission and baseline reconciliation.** The existing central
	downstream contract resolves snapshot, owner labels, allocation, revisions,
	and already approved descriptive context once. Audit every eligible candidate,
	including ones the old parser rejects. Discovery is not approval. Supplementary
	OCR composition is renderable only when existing explicit approval and source
	binding can be proved; otherwise report unresolved approval context. No new
	approval, allocation, descriptive authority, or newest-ingestion fallback.
2. **Extraction preservation.** Extend the existing artifact-only descriptive
	extractor to preserve section hierarchy, source identity/revision, source spans,
	paragraphs, and explicit relations. Preserve unsupported/ambiguous spans for
	audit rather than silently discarding them. Do not read source PDFs downstream
	or infer ownership from entity mentions. Fix ID/text pairing using intact records.
3. **One shared semantic contract.** Reuse `NormalizedSourceRecord`, `SemanticUnit`,
	and the existing `DescriptiveFact`/writing-profile core. Extend only missing
	relation/branch/sequence/span/disposition fields. Use an explicit versioned IPOS
	profile for both domains; do not inherit SRS exclusions or change its rollout.
	No parallel IPOS fact engine, block templates, or new allocation authority.
4. **Bounded generic projection.** Model complete supported clauses with their
	dependencies before lexical cleanup. Record unsupported grammar as a gap.
	Remove relevant name-specific host rules and rewrites from the migrated IPOS
	path; approved vocabulary can classify or label but cannot supply missing facts.
	Preserve role versus behavior, control versus data flow, and directed endpoints.
5. **Compatible aggregation and composition.** Merge only equivalent/compatible
	propositions with preserved guards and alternatives. Emit internal organization
	only for explicit admitted relations. Represent sequence only from an approved
	temporal/dependency proposition; shared subjects, adjacent rows, or presentation
	order never establish `then`. No character/facet-count caps on essential facts.
	Keep natural technical prose, not source mirroring or one bullet per requirement.
6. **Independent validation in existing boundaries.** Build preservation obligations
	from central admitted source records before composer selection. Compare these
	with persisted facts/dispositions and claims in final section-scoped Markdown
	and DOCX. Do not call the composer to decide semantic expectations. Use bounded,
	deterministic construction checks and explicit source-supported equivalence
	rules, not arbitrary natural-language equivalence claims. Unsupported validation
	constructions are unresolved, never automatic PASS. Check source-to-fact and
	fact-to-final-output loss separately, including missing/extra relations and
	strengthened meaning. Names, IDs, contributor presence, and hashes remain
	useful integrity checks, not semantic proof.
7. **Controlled all-block rollout after authorization.** Run focused generic tests,
	central precondition, both IPOS gates, and central coherence at one explicit
	snapshot. Inspect every materialized overview and final DOCX. Regenerate only
	derived IPOS outputs; report irreducible source/context conflicts without
	rewriting authority. Preserve normative text/IDs/Covers, mappings, allocations,
	snapshots/history, approved port sets, and central SysML scope. No SysML or
	unrelated document regeneration is part of this repair.

| Existing file | Planned responsibility |
| --- | --- |
| `scripts/stage1_descriptive_evidence.py` | Artifact extraction and source/context preservation; no authority discovery. |
| `scripts/spec_document_contract.py` | Shared record/fact/claim/disposition relationships and independent materialization obligations. |
| `scripts/workflow_routing.py` | Shared IPOS profile, intact input records, generic projection, compatible aggregation, composition, and descriptive validation. |
| `scripts/validate_downstream_coherence.py` | Single admitted context, exact scope reconciliation, and source-backed semantic completeness checks. Central SysML contract unchanged. |
| `scripts/generate_ipos_specs.py` | Necessary shared-input/audit wiring only; no local semantic policy or selection. |
| Existing stage gate entrypoints, only if needed | Invoke the same shared checks for both IPOS domains; no local validators. |
| `scripts/generate_stage1_requirements.py` | Diagnostic tracing only initially. Any proven approved-text recovery is a separate approval-boundary task, not a silent part of this rollout. |

### Generic and mutation test deliverables

Extend existing tests, not a parallel suite: `test_stage1_descriptive_evidence.py`,
`test_descriptive_summary.py`, `test_spec_document_contract.py`, and central
coherence tests in `test_srs_downstream_coherence.py`. Reuse
`test_ipos_source_port_coverage.py` as an unchanged preservation gate.

- Positive fixtures: generic Digital and Analog owners; composite entities with
  two children and nested composition; conditional transfers; negative effects;
  mutually exclusive modes and OR/AND alternatives; explicit sequence; unordered
  independent actions; cross-page descriptions; passive predicates; multiple
  actions per record; quantitative functional limits; equivalent text under
  distinct IDs; and accepted nonessential implementation-detail exclusions.
- Preserve paraphrases: two differently worded summaries can pass the same
  structured obligations without literal source-to-sentence mirroring. Valid
  aggregation may share a sentence while keeping distinct conditions explicit.
- Mutate relation integrity: delete/invert containment, swap actors or endpoints,
  relabel a behavior as an aggregate role, add an unsupported child, or turn
  co-occurrence into an interaction. Every supported affected obligation fails.
- Mutate conditional meaning: remove a guard/exception, invert polarity, change
  OR to AND, merge incompatible modes, erase a threshold/completion condition,
  or invent `then`. Name and contributor sets remain unchanged during mutations.
- Mutate upstream loss: drop a source clause before fact modeling, force parser
  rejection, split its guard from its action, falsely mark it atomic/nonessential,
  mispair deduplicated IDs/texts, or truncate a long supported predicate. Independent
  source obligations must detect the loss, not rederive the flawed selection.
- Mutate audit/output jointly: alter facts, claims, Markdown, DOCX, and recomputed
  hashes consistently while leaving selected approved inputs unchanged. Semantic
  validation must still fail; audit/composer self-consistency is insufficient.
- Boundary fixtures: ambiguous ownership, absent descriptive approval, conflicting
  revision, incomplete alternative, inventory conflict, cross-block evidence,
  and valid-empty domains. None may create guessed facts, new scope, or approval.

Acceptance: all admitted essential facts have independently verified preservation
or explicit unresolved findings; exclusions satisfy the profile policy; no hidden
atomic exemption or name-presence shortcut remains. Current Main Controller
composition becomes a positive regression only if existing approval is established;
otherwise its correct outcome is an explicit approval-context finding. The baseline
is not a certification that every suppressed candidate is defective or that all
source meaning can be parsed. No tests for this planned implementation have run yet.

### Implementation checkpoint: partial, not rollout completion

Implementation has started following user authorization. The planning-only status
above describes the original diagnostic baseline, not the current code state.

Completed in the existing shared `workflow_routing.py` boundary:

- Preserve local requirement identity/text pairs together, including distinct IDs
	with identical statements; reject incomplete pairs instead of silently mispairing.
- Reject actor/object inversion and name-only coverage in structured paragraph
	validation, and reject added `then` without explicit source support. These are
	bounded checks, not a general temporal or semantic equivalence proof.
- Remove the 100-character structural action-tail cap.
- Preserve inventory input terms instead of silently deleting `register`.
- Do not infer `then` by grouping independent selection/start requirements.

Verification: all 86 descriptive tests, 7 document-contract tests, and 2 source-port
coverage tests pass. Editor diagnostics for the two changed Python files are clean.
The central check at `snap-b2e8101b00dc6909feaed885` returns `BLOCK_DOWNSTREAM`
with 42 findings against existing IPOS artifacts, primarily shared-policy and
normalized-input audit mismatches plus changed scope wording. These are not a
successful semantic-completeness check. No IPOS documents were regenerated in this
checkpoint, and no approved requirements, mappings, allocations, snapshots, or
central SysML scope were changed.

Still required before declaring the documented repair complete: central admitted
context and source reconciliation, preserved extraction spans, IPOS fact-profile
migration, independent source-to-fact and section-scoped final Markdown/DOCX
obligations, essential-fact dispositions without atomic exemptions, the remaining
generic/mutation matrix, and controlled all-block regeneration/gates. The existing
IPOS profile remains inactive; the legacy IPOS aggregation path has not yet been
replaced. Passing these initial tests must not be reported as completion of the
seven-stage implementation plan or certification of all supported source meaning.

### Shared-flow migration and regeneration checkpoint (2026-10-08)

The authorized IPOS migration is now implemented at the existing shared boundary.
`IPOS_DESCRIPTIVE_PROFILE` is active as `ipos-structural-integrity-v1`. Digital and
Analog IPOS call `run_descriptive_flow` through a bounded generic IPOS adapter;
generator changes are domain/input wiring only. Source identity/text pairs and
complete approved statements are retained, including equivalent statements under
distinct IDs. Candidate admission follows the selected snapshot's IPOS owning
target and domain, not an `approved_block` label alone. The existing canonical
descriptive-evidence table contains architecture power-domain context, not admitted
block-local composition evidence; it was not promoted into IPOS authority.

The runtime validator no longer recomposes an expected IPOS overview. It checks
source propositions against persisted facts independently, checks profile/audit
linkage, and then reads the actual overview sections in both final Markdown and
DOCX. Actor/object direction, guards, polarity, alternatives, quantities/operators,
supported temporal text, unsupported extra claims and contributor linkage are
checked within bounded constructions. Typographic quote equivalents are normalized
only for materialization comparisons. Unsupported/incomplete constructions remain
blocking gaps; there is no atomic exemption or name-only normative-section coverage.
The private historical renderer helpers remain solely for explicitly isolated old
regression fixtures, not as a runtime fallback or evidence of migration coverage.

#### Original 42 discrepancies

| Class | Count | Disposition |
| --- | ---: | --- |
| Old refinement shared-policy/audit mismatch | 25 | Replaced by the shared fact-flow audit and regenerated. |
| Normalized input fingerprint/record mismatch | 16 | Rebuilt from intact approved source records; regenerated. |
| Main Controller inventory-bound scope wording mismatch | 1 | Inventory terms preserved in the regenerated scope. |

All 42 original findings are absent from the final all-block check. Eight Digital
IPOS Markdown/DOCX document pairs and their audits were regenerated at unchanged
snapshot `snap-b2e8101b00dc6909feaed885`; Analog was regenerated as valid-empty.
This is not a claim that all descriptive evidence is semantically complete.

#### Verified residuals

| Source projection gap class | Unique records |
| --- | ---: |
| Multiple normative clauses or unsupported non-normative construction | 65 |
| Unsupported/incomplete predicate, including unsupported intransitive form | 25 |
| Ambiguous compound guard/actor boundary | 6 |
| Additional unsupported source proposition | 5 |
| Structured table/formula/procedure construction | 5 |
| Ambiguous guard boundary | 11 |
| Unsupported conditional consequence marker | 4 |
| **Total** | **121** |

Per-block unresolved records: ADSP 6; I2C_SPI_AHB 8; Main Controller 80; PAD MUX 11;
PMU 1; Regmap 7; Sensor-Hub 5; Smart FIFO 3. All 259 approved normative records remain
exactly present; 138 have independently checked descriptive projections. The other
121 retain complete source identity/text and explicit dispositions in each block's
`descriptive_summary_audit.csv`. They are parser/projection findings, not automatic
claims of absent source approval. No unsupported source construction earns a PASS.

The final central result is `BLOCK_DOWNSTREAM`, 251 findings: 121 independent
source-projection findings, 121 corresponding audit gap findings, eight block-level
retained-input materialization findings, and one structural-function coverage
finding. These are overlapping diagnostics, not 251 distinct lost requirements.
Four of five discovered structural functions have source-linked descriptive facts;
the remaining `Main_Controller_FSM` reference is linked to
`IPOS_STBIO1_MAIN_CONTROLLER_008`. That approved source has multiple predicates and
ends in the incomplete clause `(for`; do not invent its completion, reinterpret its
FIFO/time-slot role as aggregate composition, or change its mapping/Covers. Parser
extension and approval-bound source recovery are distinct remaining work items.

The detailed current result is persisted in
`artifacts/validation/downstream_coherence_report.json`; the central CLI prints its
result but does not itself overwrite that file. Earlier stored DRS findings are not
present in this final run; no DRS repair or baseline change was performed.

#### Checks And Preservation

- 97 descriptive tests, nine document-contract tests, 19 central coherence tests,
	and two source-port tests pass (127 total). Historical renderer fixtures are not
	counted as evidence that the new adapter supports their constructions.
- Generic Digital/Analog fixtures and joint fact/audit/output/hash mutations detect
	guard loss, actor inversion, OR-to-AND changes, polarity changes, quantity/operator
	changes, extra children/relations, missing contributors, and claims moved into
	normative sections. Unsupported/incomplete constructions explicitly fail closed.
- Digital IPOS gate: FAIL on unresolved approved source projections. Analog IPOS
	gate: PASS, zero requirements/blocks. No gate or semantic check was weakened.
- All 651 approved source ports appear in both Markdown and DOCX (1,302 checked
	rendered rows). No unexpected final DOCX claim/materialization mismatch remains.
- Normative IDs/text/Covers/snapshot and document version histories are unchanged.
	All 248 protected Stage 1/2/3/4/5 artifacts, including central SysML files/scope,
	are byte-identical across regeneration. Eleven canonical authority tables are
	identical at the field level, excluding only `requirement_allocations.created_at`,
	which the existing ledger synchronization rewrites. All 314 allocation policy
	fields were crosschecked against the immutable snapshot contract without mismatch.
- Changed runtime Python files have no editor diagnostics. Test imports execute
	successfully under unittest; the editor also reported unresolved imports in the
	pre-existing dynamic `sys.path` test setup. No interpreter configuration was changed.
- `git diff --check` passes.

The runtime migration and stale-artifact repair are complete, but clean semantic
acceptance is **not closed**. Resolve the bounded-parser gaps and the approval-bound
incomplete source before claiming complete descriptive coverage. Broader
common-contract generalization is deliberately deferred.