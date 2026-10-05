# Retrieval and Mapping Flow Evaluation

Date: 2026-09-14 10:14:54
Cases: 10; semantic resources: available.

## Causal Boundary
- Ordinary RAG is scored on source chunks only.
- Approved structured evidence and low-power audits are not credited to RAG retrieval.
- Stage 2 mapping and hierarchy assignment are scored separately and held constant across retrieval modes.
- Rendering usefulness measures preservation of configured source attributes in generated SRS text.

## Overall Retrieval Results
| Mode | R@1 | R@5 | R@10 | P@5 | MRR | nDCG@10 | Noise@10 | Structured hit | Scope | Attributes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lexical | 0.700 | 0.700 | 0.700 | 0.567 | 0.700 | 0.655 | 0.000 | 0.700 | 0.700 | 0.700 |
| normalized | 1.000 | 1.000 | 1.000 | 0.380 | 1.000 | 0.931 | 0.020 | 1.000 | 1.000 | 0.967 |
| hybrid | 1.000 | 1.000 | 1.000 | 0.400 | 1.000 | 0.973 | 0.020 | 1.000 | 1.000 | 0.967 |
| hybrid-semantic | 0.800 | 1.000 | 1.000 | 0.280 | 0.883 | 0.890 | 0.010 | 1.000 | 1.000 | 0.967 |

## Evidence Class Results
| Mode | Evidence class | Cases | R@10 | Attributes | Scope |
| --- | --- | ---: | ---: | ---: | ---: |
| lexical | free-prose | 3 | 0.333 | 0.333 | 0.333 |
| lexical | structured | 4 | 0.750 | 0.750 | 0.750 |
| lexical | semi-structured | 3 | 1.000 | 1.000 | 1.000 |
| normalized | free-prose | 3 | 1.000 | 0.889 | 1.000 |
| normalized | structured | 4 | 1.000 | 1.000 | 1.000 |
| normalized | semi-structured | 3 | 1.000 | 1.000 | 1.000 |
| hybrid | free-prose | 3 | 1.000 | 0.889 | 1.000 |
| hybrid | structured | 4 | 1.000 | 1.000 | 1.000 |
| hybrid | semi-structured | 3 | 1.000 | 1.000 | 1.000 |
| hybrid-semantic | free-prose | 3 | 1.000 | 0.889 | 1.000 |
| hybrid-semantic | structured | 4 | 1.000 | 1.000 | 1.000 |
| hybrid-semantic | semi-structured | 3 | 1.000 | 1.000 | 1.000 |

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
| normalized | low_power_coordination | 1 | 1.000 | 1.000 | 0.000 |
| normalized | power_domains | 2 | 1.000 | 1.000 | 0.100 |
| normalized | operating_modes_power_states | 1 | 1.000 | 1.000 | 0.000 |
| normalized | sequencing_control_ownership | 2 | 1.000 | 1.000 | 0.000 |
| normalized | retention_isolation_restore | 1 | 1.000 | 1.000 | 0.000 |
| normalized | requirement_block_mapping | 1 | 1.000 | 1.000 | 0.000 |
| normalized | structured_architectural_evidence | 1 | 1.000 | 1.000 | 0.000 |
| normalized | low_power_entry_exit | 1 | 1.000 | 0.667 | 0.000 |
| hybrid | low_power_coordination | 1 | 1.000 | 1.000 | 0.000 |
| hybrid | power_domains | 2 | 1.000 | 1.000 | 0.100 |
| hybrid | operating_modes_power_states | 1 | 1.000 | 1.000 | 0.000 |
| hybrid | sequencing_control_ownership | 2 | 1.000 | 1.000 | 0.000 |
| hybrid | retention_isolation_restore | 1 | 1.000 | 1.000 | 0.000 |
| hybrid | requirement_block_mapping | 1 | 1.000 | 1.000 | 0.000 |
| hybrid | structured_architectural_evidence | 1 | 1.000 | 1.000 | 0.000 |
| hybrid | low_power_entry_exit | 1 | 1.000 | 0.667 | 0.000 |
| hybrid-semantic | low_power_coordination | 1 | 1.000 | 1.000 | 0.000 |
| hybrid-semantic | power_domains | 2 | 1.000 | 1.000 | 0.050 |
| hybrid-semantic | operating_modes_power_states | 1 | 1.000 | 1.000 | 0.000 |
| hybrid-semantic | sequencing_control_ownership | 2 | 1.000 | 1.000 | 0.000 |
| hybrid-semantic | retention_isolation_restore | 1 | 1.000 | 1.000 | 0.000 |
| hybrid-semantic | requirement_block_mapping | 1 | 1.000 | 1.000 | 0.000 |
| hybrid-semantic | structured_architectural_evidence | 1 | 1.000 | 1.000 | 0.000 |
| hybrid-semantic | low_power_entry_exit | 1 | 1.000 | 0.667 | 0.000 |

## Downstream Mapping and Hierarchy
| Measure | Result |
| --- | ---: |
| Candidate mapping accuracy before review | 0.981 |
| Final requirement-to-block accuracy | 0.968 |
| Requirement-to-hierarchy accuracy | 0.968 |
| Digital/analog/system classification accuracy at review boundary | 1.000 |
| Top-level vs block-local error rate | 0.000 |

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
- Structured low-power records are selected and scoped by `low_power_descriptive.py` and its audit CSVs; semantic retrieval does not repair rows rejected by topic limits or scope filters.
- Semantic widening is candidate-only, so it cannot change approved Stage 2 ownership or hierarchy assignment.

## Semantic Delta
- Hybrid-semantic minus hybrid attribute-preservation delta: +0.000.
- Hybrid-semantic minus hybrid Recall@10 delta: +0.000.
- Hybrid-semantic minus hybrid noise delta: -0.010.
- Hybrid-semantic minus hybrid scope delta: +0.000.

## Recommendation
- Overall: **retain hybrid baseline; reject global semantic retrieval**.
- Topic-specific: retain deterministic hybrid for structured power-domain tables, operating-mode records, protocol evidence, and exact IDs; only gate semantic widening to topics with a positive attribute-preserving gain and no scope/noise regression.
- Current evidence does not justify a global transformer step. Upstream structured-evidence preservation, topic output limits, and mapping/hierarchy quality remain separate controls.
