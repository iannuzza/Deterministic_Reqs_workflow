# Retrieval and Mapping Flow Evaluation

Generated from the recorded benchmark configuration and approved downstream artifacts.
Project: STBIO; Cases: 13; semantic evaluation: disabled or unavailable.

## Causal Boundary
- Ordinary RAG is scored on source chunks only.
- Approved structured evidence and low-power audits are not credited to RAG retrieval.
- Stage 2 mapping and hierarchy assignment are scored separately and held constant across retrieval modes.
- Rendering usefulness measures preservation of configured source attributes in generated SRS text.

## Overall Retrieval Results
| Mode | R@1 | R@5 | R@10 | P@5 | MRR | nDCG@10 | Noise@10 | Structured hit | Scope | Attributes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lexical | 0.769 | 0.769 | 0.769 | 0.667 | 0.769 | 0.735 | 0.000 | 0.769 | 0.769 | 0.769 |
| normalized | 1.000 | 1.000 | 1.000 | 0.338 | 1.000 | 0.947 | 0.015 | 1.000 | 1.000 | 0.974 |
| hybrid | 1.000 | 1.000 | 1.000 | 0.354 | 1.000 | 0.979 | 0.015 | 1.000 | 1.000 | 0.974 |

## Evidence Class Results
| Mode | Evidence class | Cases | R@10 | Attributes | Scope |
| --- | --- | ---: | ---: | ---: | ---: |
| lexical | free-prose | 6 | 0.667 | 0.667 | 0.667 |
| lexical | structured | 4 | 0.750 | 0.750 | 0.750 |
| lexical | semi-structured | 3 | 1.000 | 1.000 | 1.000 |
| normalized | free-prose | 6 | 1.000 | 0.944 | 1.000 |
| normalized | structured | 4 | 1.000 | 1.000 | 1.000 |
| normalized | semi-structured | 3 | 1.000 | 1.000 | 1.000 |
| hybrid | free-prose | 6 | 1.000 | 0.944 | 1.000 |
| hybrid | structured | 4 | 1.000 | 1.000 | 1.000 |
| hybrid | semi-structured | 3 | 1.000 | 1.000 | 1.000 |

## Topic Results
| Mode | Topic | Cases | R@10 | Attributes | Noise |
| --- | --- | ---: | ---: | ---: | ---: |
| lexical | low_power_coordination | 1 | 1.000 | 1.000 | 0.000 |
| lexical | power_domains | 2 | 0.500 | 0.500 | 0.000 |
| lexical | operating_modes_power_states | 1 | 1.000 | 1.000 | 0.000 |
| lexical | sequencing_control_ownership | 2 | 1.000 | 1.000 | 0.000 |
| lexical | retention_isolation_restore | 1 | 0.000 | 0.000 | 0.000 |
| lexical | requirement_block_mapping | 1 | 1.000 | 1.000 | 0.000 |
| lexical | structured_architectural_evidence | 1 | 1.000 | 1.000 | 0.000 |
| lexical | low_power_entry_exit | 1 | 0.000 | 0.000 | 0.000 |
| lexical | multi_block_test_control_ownership | 3 | 1.000 | 1.000 | 0.000 |
| normalized | low_power_coordination | 1 | 1.000 | 1.000 | 0.000 |
| normalized | power_domains | 2 | 1.000 | 1.000 | 0.100 |
| normalized | operating_modes_power_states | 1 | 1.000 | 1.000 | 0.000 |
| normalized | sequencing_control_ownership | 2 | 1.000 | 1.000 | 0.000 |
| normalized | retention_isolation_restore | 1 | 1.000 | 1.000 | 0.000 |
| normalized | requirement_block_mapping | 1 | 1.000 | 1.000 | 0.000 |
| normalized | structured_architectural_evidence | 1 | 1.000 | 1.000 | 0.000 |
| normalized | low_power_entry_exit | 1 | 1.000 | 0.667 | 0.000 |
| normalized | multi_block_test_control_ownership | 3 | 1.000 | 1.000 | 0.000 |
| hybrid | low_power_coordination | 1 | 1.000 | 1.000 | 0.000 |
| hybrid | power_domains | 2 | 1.000 | 1.000 | 0.100 |
| hybrid | operating_modes_power_states | 1 | 1.000 | 1.000 | 0.000 |
| hybrid | sequencing_control_ownership | 2 | 1.000 | 1.000 | 0.000 |
| hybrid | retention_isolation_restore | 1 | 1.000 | 1.000 | 0.000 |
| hybrid | requirement_block_mapping | 1 | 1.000 | 1.000 | 0.000 |
| hybrid | structured_architectural_evidence | 1 | 1.000 | 1.000 | 0.000 |
| hybrid | low_power_entry_exit | 1 | 1.000 | 0.667 | 0.000 |
| hybrid | multi_block_test_control_ownership | 3 | 1.000 | 1.000 | 0.000 |

## Downstream Mapping and Hierarchy
| Measure | Result |
| --- | ---: |
| Candidate mapping accuracy before review | 1.000 |
| Final requirement-to-block accuracy | 0.841 |
| Requirement-to-hierarchy accuracy | 0.841 |
| Digital/analog/system classification accuracy at review boundary | 1.000 |
| Top-level vs block-local error rate | 0.150 |

Final mapping is held constant across retrieval modes; semantic widening is candidate-only and cannot override reviewed ownership.
- Scope note: final traceability stores document domains such as XDN rather than the reviewed Digital/Analog/System labels; classification accuracy is therefore measured at the Stage 2 review boundary.

## Rendered Detail Preservation
| Case | Rendered attribute preservation |
| --- | ---: |
| power-domain-table | 1.000 |
| power-domain-descriptions | 1.000 |
| low-power-operating-modes | 0.750 |
| boot-power-sequence | 0.750 |

## Causal Diagnosis

- downstream rendering/compaction: 2 benchmark cases.
- post-retrieval preservation/filtering or structured assembly: 1 benchmark cases.
- Relevant source chunks are available in the RAG database for every labeled case; a top-k miss is retrieval-driven, while a hit with missing attributes is preservation/filtering-driven.
- Structured records are selected and scoped by project-provided deterministic assembly artifacts; semantic retrieval does not repair rows rejected by topic limits or scope filters.
- Any semantic widening remains candidate-only, so it cannot change approved mapping ownership or hierarchy assignment.

## Semantic Delta
- Semantic widening was not evaluated; it requires explicit command and configuration opt-in.

## Recommendation
- Overall: **retain hybrid baseline; reject global semantic retrieval**.
- Topic-specific: retain deterministic hybrid for structured evidence and exact identifiers; only evaluate semantic widening for a named weak content class after explicit approval.
- Current evidence does not justify a global transformer step. Evidence preservation, filtering, rendering, and mapping remain separate controls.
