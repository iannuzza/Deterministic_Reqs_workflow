# Deterministic Semantic Retrieval Benchmark Report

Date: 2026-09-04

Project: `STBIO`

Report identity is read from the active `config/project_context.json` `project_name`; retrieval and benchmark logic remains project-agnostic.

Project-specific benchmark cases: `config/retrieval_benchmark_cases.json`. The cases are based on the active source specification and current RAG index; their labels must be reviewed when either artifact is regenerated.

The authoritative live selection report is written to `artifacts/rag_DDS_STBIO1/retrieval_benchmark_report.json`, with the selected mode persisted in `config/retrieval_selection.json`. Every benchmark run overwrites both files with the final method decision and the result data that motivated it.

Latest automated selection: `hybrid`. The project benchmark passed label validation, but no non-fallback method passed all selection gates: semantic methods regressed exact-ID Recall@1 and all measured methods exceeded the configured latency thresholds. The current live timings include query-process startup because the benchmark invokes the CLI per query; use them as workflow wall-clock measurements until an in-process benchmark adapter is added.

## Purpose

This report records the first benchmark of the optional deterministic semantic retrieval channel against the existing retrieval modes.

The semantic channel uses a dependency-free local hash embedding baseline. It is deterministic and offline, but it is not a production-quality language embedding model. No LLM, network call, or external AI service was used.

## Compared Modes

| Mode | Implementation |
|---|---|
| Lexical | SQLite FTS5 search over original chunk text |
| Normalized | SQLite FTS5 search over controlled vocabulary and normalized terms |
| Old hybrid | Reciprocal Rank Fusion of lexical and normalized channels |
| New hybrid + semantic cosine | RRF of lexical, normalized, and semantic cosine channels |
| Semantic cosine | Exact cosine search over the local semantic index, used as a diagnostic reference |

## Test Environment

- Source index: `artifacts/rag_DDS_STBIO1/rag_index.sqlite`
- Existing indexed chunks: 376
- Semantic entity records: 610
- Semantic backend: exact cosine similarity
- Test embedding: deterministic `LocalHashEmbeddingModel`, 256 dimensions
- Retrieval date: 2026-09-04
- Query result depth: top 10 for metric calculation
- RRF constant: 60

## Representative Queries

| Category | Query | Expected relevant chunk IDs |
|---|---|---|
| Exact requirement ID | `DDS_STBIO1_0104` | 151 |
| Acronym/protocol | `I2C SPI AHB interface` | 139, 266, 267 |
| Synonym/paraphrase | `startup power sequencing` | 59, 67, 243 |
| Sparse description | `FIFO depth` | 260, 286, 290 |
| Mixed engineering query | `clock gating` | 140, 154 |

The relevance sets are manually curated benchmark labels for this initial evaluation. They should be expanded and reviewed before a production rollout gate is established.

## Benchmark Results

Metrics are calculated across the five representative query cases.

| Mode | Recall@1 | Recall@5 | Recall@10 | MRR | Mean latency | p95 latency |
|---|---:|---:|---:|---:|---:|---:|
| Lexical | 0.800 | 0.800 | 0.800 | 0.800 | 0.26 ms | 0.32 ms |
| Normalized | 1.000 | 1.000 | 1.000 | 1.000 | 2.86 ms | 3.80 ms |
| Old hybrid | 1.000 | 1.000 | 1.000 | 1.000 | 1.23 ms | 1.47 ms |
| New hybrid + semantic cosine | 0.600 | 0.800 | 1.000 | 0.700 | 24.62 ms | 25.58 ms |
| Semantic cosine only | 0.400 | 0.400 | 0.400 | 0.400 | 23.15 ms | 24.14 ms |

## Manual Top-k Delta Review

### Exact requirement ID

Query: `DDS_STBIO1_0104`

- Lexical, normalized, and old hybrid all returned chunk `151` first.
- Semantic cosine ranked the requirement entity `requirement:DDS_STBIO1_0104` first when all entity types were considered.
- After filtering to chunks, semantic results were `131, 86, 328, 143, 325`; the expected evidence chunk `151` was not in the semantic top five.
- Finding: exact identifiers must remain primarily lexical/normalized. Semantic retrieval must not displace exact-term evidence.

### Acronym and protocol query

Query: `I2C SPI AHB interface`

- Old hybrid: `139, 267, 266, 314, 261`.
- Semantic chunk results: `139, 294, 293, 283`.
- Mixed semantic results included `block:SPI interface` and `block:I2C interface` before some source chunks.
- Finding: semantic retrieval recognizes protocol concepts but has wrong-entity bias when blocks and evidence chunks share one ranking space.

### Synonym or paraphrase query

Query: `startup power sequencing`

- Lexical returned no results.
- Normalized and old hybrid returned `59, 67, 340, 243, 238`.
- Semantic chunk results were `100, 167, 99, 125`.
- Finding: the local hash baseline did not provide reliable semantic paraphrase retrieval. This is an embedding-quality limitation, not evidence that semantic retrieval is ineffective in principle.

### Sparse description query

Query: `FIFO depth`

- Old hybrid: `286, 260, 91, 38, 291`.
- Semantic chunk results: `290, 287, 285, 286, 332`.
- Semantic retrieval found several FIFO-related chunks but changed the ordering and omitted expected chunk `260` from the top five.
- Finding: sparse technical descriptions need stronger embeddings and likely exact-term boosts.

### Mixed engineering query

Query: `clock gating`

- Old hybrid: `140, 154, 303, 138, 142`.
- Semantic chunk results: `143, 305, 142, 303, 145`.
- Finding: semantic results were related to clock and control content but did not preserve the strongest existing evidence ordering.

## Failure Clusters

### Synonyms and paraphrases

The hash embedding does not model meaning or synonyms. Queries such as `startup power sequencing` therefore retrieve broad lexical neighbors or unrelated technical sections. A fixed local sentence-embedding model is required for this category.

### Acronyms

Acronyms are handled well by lexical and normalized retrieval because exact tokens are preserved. Semantic retrieval can broaden the result set, but acronym expansion must remain controlled and source-backed.

### Sparse descriptions

Short descriptions such as `FIFO depth` contain too little context for the hash baseline. Exact lexical matches and approved vocabulary expansions should remain strong retrieval signals for sparse technical queries; neither replaces canonical SQLite authority, source evidence, or approved snapshot decisions.

### Wrong entity bias

The semantic index currently contains blocks, functions, requirements, interfaces, and chunks in one ranking space. Non-chunk entities can outrank source evidence. Entity-type filtering or separate semantic namespaces are required before semantic results can be used directly as evidence retrieval.

## Current Rollout Decision

The new semantic channel is **not ready to become the default**.

Keep these behaviors:

- `lexical`: unchanged
- `normalized`: unchanged
- `hybrid`: unchanged and remains the fallback legacy behavior
- `auto`: default query mode; reads the latest benchmark selection and falls back to `hybrid` when selection evidence is unavailable or fails policy
- `semantic`: opt-in diagnostic mode
- `hybrid-semantic`: opt-in experimental mode with graceful fallback

When `lexical`, `normalized`, or legacy `hybrid` returns no rows, the query CLI performs one automatic incremental semantic recovery attempt when local semantic resources are available. It runs chunk-scoped `semantic` retrieval and records `Automatic semantic fallback: used` in the output. Use `--no-semantic-fallback` to disable this recovery for a specific legacy query. Unavailable or incompatible semantic resources leave the legacy empty result unchanged.

Queries containing a source requirement ID also receive a `Requirement-ID Mapping Check`. The check reads the expected owner from the Stage 1 catalog, verifies whether returned evidence contains the queried ID, and reports `pass` or `review`. It is an audit signal only; it never changes deterministic ownership or architecture approval.

## Blocking Work Before Production Rollout

1. Provision and verify one fixed local sentence-embedding model without network access.
2. Separate or filter semantic result namespaces so evidence chunks are not mixed indiscriminately with blocks, functions, requirements, and interfaces.
3. Rerun the benchmark using the production local model.
4. Expand relevance labels across exact IDs, acronyms, paraphrases, sparse descriptions, interfaces, and mixed entity queries.
5. Tune semantic participation in RRF and require no regression against old hybrid on exact-ID and acronym cases.
6. Implement and benchmark an ANN backend only if exact cosine latency is unacceptable at the final entity count.
7. Connect the benchmark CLI directly to live `lexical`, `normalized`, `hybrid`, and `hybrid-semantic` execution.

## Test Plan

### Unit tests

- `IndexedEntity` rejects empty IDs, types, names, and embedding text.
- Canonical embedding text is deterministic and labeled.
- Block, function, requirement, interface, and chunk text builders preserve technical identifiers.
- Local hash embeddings are deterministic.
- Embedding dimensions are validated.
- Exact cosine ranking is correct on controlled vectors.
- Zero vectors return no semantic results safely.
- Semantic index save/load preserves results.
- Corrupt or incompatible manifests fail clearly.
- Two-channel RRF preserves the legacy wrapper behavior.
- Three-channel RRF records semantic rank and score.
- Benchmark metrics correctly calculate Recall@k and MRR.

### Integration tests

- Legacy lexical queries run without a semantic index.
- Legacy normalized queries run without a semantic model.
- Legacy hybrid ranking remains unchanged.
- Semantic mode loads only local resources.
- Semantic mode reports a clear failure when its index or model is unavailable.
- Hybrid-semantic falls back to lexical plus normalized retrieval when semantic resources are unavailable.
- Query output exposes channel ranks and scores.
- Semantic index build collects available entities and persists a manifest.

### Offline and security checks

- No network calls are made during semantic index build or query.
- The configured production model path must exist locally.
- No model download fallback is permitted.
- Model fingerprint and embedding dimension must match the semantic index manifest.
- Source text and provenance remain available alongside normalized or embedded representations.
- Semantic retrieval cannot modify requirement ownership or architecture approval decisions.

### Benchmark rollout gate

A production semantic rollout should require:

- no Recall@k or MRR regression for exact-ID and acronym queries versus old hybrid
- measurable improvement for reviewed paraphrase queries
- acceptable mean and p95 latency
- reproducible results across repeated runs
- a recorded model fingerprint and semantic-index manifest
- manual inspection of top-k deltas for every failure cluster

## Validation Performed

### Focused Retrieval Test Evidence

Command:

```powershell
python -m unittest tests.test_embedding_text tests.test_semantic_index tests.test_fusion tests.test_benchmark
```

Recorded result:

```text
Ran 12 tests in 0.070s
OK
```

| Suite | Test | Evidence verified | Result |
|---|---|---|---|
| `test_embedding_text` | `test_canonical_text_is_deterministic_and_labeled` | Canonical embedding text is repeatable and includes entity identity labels. | PASS |
| `test_embedding_text` | `test_entity_specific_builders_preserve_ids_and_technical_terms` | Block and requirement builders preserve names, technical terms, source IDs, and clock-gating text. | PASS |
| `test_embedding_text` | `test_indexed_entity_rejects_empty_embedding_text` | Empty embedding text is rejected by the indexed-entity contract. | PASS |
| `test_embedding_text` | `test_validation_requires_identity_labels` | Embedding text validation requires entity-type and name labels. | PASS |
| `test_semantic_index` | `test_build_search_and_round_trip` | Exact-cosine index builds, ranks the expected result, and preserves results after save/load. | PASS |
| `test_semantic_index` | `test_invalid_top_k_is_rejected` | Invalid semantic search depth is rejected. | PASS |
| `test_semantic_index` | `test_semantic_search_filters_entity_types_and_reranks` | Chunk-scoped semantic search excludes block entities and returns semantic rank metadata. | PASS |
| `test_fusion` | `test_two_channel_wrapper_preserves_ranks_and_scores` | Legacy lexical/normalized RRF ranks and score behavior are preserved. | PASS |
| `test_fusion` | `test_three_channel_fusion_exposes_semantic_rank` | Three-channel fusion exposes semantic rank and score. | PASS |
| `test_fusion` | `test_protected_exact_result_cannot_be_demoted` | Protected exact evidence cannot be displaced by a semantic-only result. | PASS |
| `test_benchmark` | `test_metrics_measure_expected_ids` | Recall@1, Recall@5, and MRR calculate correctly for expected IDs. | PASS |
| `test_benchmark` | `test_requirement_id_audit_reports_stage1_owner` | Requirement-ID audit reports `DDS_STBIO1_0104` expected owner as `PMU`. | PASS |

- Focused retrieval tests: **12 passed**.
- Workflow integration: `workflow_cli.py run --stage 0` or a range beginning at Stage 0 executes the focused 12-test suite once before Stage 0 and stops if it fails. Stage 1-5-only runs do not execute these checks. The result is logged as `kind: retrieval_tests` in `artifacts/orchestrator/workflow_cli_runs.jsonl`.
- Project selection integration: after the tests pass, the workflow runs the five project-specific cases across all retrieval modes. A candidate must pass labels, latency thresholds, and exact-ID protection; otherwise `hybrid` is persisted as the selected mode.
- New and modified Python modules compiled successfully.
- Offline semantic index build and reload: passed with 610 entities.
- Legacy hybrid query: passed.
- Hybrid-semantic missing-index fallback: passed.
- Benchmark correction: the final metrics use the actual three-channel RRF implementation, not the earlier mistaken two-channel callable.
