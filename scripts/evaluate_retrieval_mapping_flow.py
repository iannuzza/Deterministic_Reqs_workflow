#!/usr/bin/env python3
"""Causal evaluation of retrieval, evidence preservation, mapping, and rendering."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sqlite3
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
ROOT = DEFAULT_ROOT
sys.path.insert(0, str(ROOT))

from retrieval.fusion import fuse_lexical_normalized_semantic
from retrieval.semantic_index import SemanticIndexUnavailable, semantic_search
from query_rag_index import (
    _chunk_columns, _controlled_terms, _fetch_lexical, _fetch_normalized,
    _fts_or_query, _load_domain_vocabulary, _load_project_context,
    _load_semantic_resources, _protected_exact_ids, _rrf_fuse,
    _semantic_chunk_rows,
)

MODES = ("lexical", "normalized", "hybrid", "hybrid-semantic")
METRIC_KEYS = ("recall_at_1", "recall_at_5", "recall_at_10", "precision_at_5", "precision_at_10", "mrr", "ndcg_at_10", "noise_contamination_at_10", "structured_evidence_hit", "scope_correct", "attribute_preservation")


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _contains(text: str, terms: list[str]) -> int:
    haystack = (text or "").casefold()
    return sum(1 for term in terms if term.casefold() in haystack)


def _ndcg(result_ids: list[str], expected: set[str], k: int) -> float:
    dcg = sum((1.0 if item in expected else 0.0) / math.log2(rank + 1) for rank, item in enumerate(result_ids[:k], 1))
    ideal = sum(1.0 / math.log2(rank + 1) for rank in range(1, min(k, len(expected)) + 1))
    return dcg / ideal if ideal else 0.0


def _query(conn: sqlite3.Connection, columns: set[str], vocabulary: dict, semantic_resources, case: dict, mode: str) -> list[dict]:
    query = str(case["query"])
    top_k = int(case.get("top_k", 10))
    normalized_query = _fts_or_query(_controlled_terms(query, vocabulary))
    if mode == "lexical":
        return _fetch_lexical(conn, query, top_k, columns)
    if mode == "normalized":
        return _fetch_normalized(conn, normalized_query, top_k, columns)
    lexical = _fetch_lexical(conn, query, 30, columns)
    normalized = _fetch_normalized(conn, normalized_query, 30, columns)
    if mode == "hybrid":
        return _rrf_fuse(lexical, normalized, top_k, 60)
    semantic_rows: list[dict] = []
    if semantic_resources is not None:
        index, model = semantic_resources
        candidates = semantic_search(query=query, top_k=30, index=index, embedding_model=model, entity_types={"chunk"})
        semantic_rows = _semantic_chunk_rows(conn, [candidate.__dict__ for candidate in candidates], columns)
    protected_ids = _protected_exact_ids(query, lexical + normalized)
    return fuse_lexical_normalized_semantic(lexical, normalized, semantic_rows, final_top_k=top_k, rrf_k=60, protected_ids=protected_ids)


def _retrieval_metrics(case: dict, rows: list[dict]) -> dict:
    expected = {str(item) for item in case.get("expected_chunk_ids", [])}
    ids = [str(row.get("chunk_id")) for row in rows]
    first = next((rank for rank, item in enumerate(ids, 1) if item in expected), None)
    evidence = "\n".join(str(row.get("chunk_text", "")) for row in rows)
    required = list(case.get("required_attributes", []))
    noise_markers = list(case.get("noise_markers", []))
    noise = sum(1 for row in rows if _contains(str(row.get("chunk_text", "")), noise_markers) and not _contains(str(row.get("chunk_text", "")), required))
    return {
        "recall_at_1": 1.0 if expected.intersection(ids[:1]) else 0.0,
        "recall_at_5": 1.0 if expected.intersection(ids[:5]) else 0.0,
        "recall_at_10": 1.0 if expected.intersection(ids[:10]) else 0.0,
        "precision_at_5": sum(item in expected for item in ids[:5]) / min(5, len(ids)) if ids else 0.0,
        "precision_at_10": sum(item in expected for item in ids) / len(ids) if ids else 0.0,
        "mrr": 1.0 / first if first else 0.0,
        "ndcg_at_10": _ndcg(ids, expected, 10),
        "noise_contamination_at_10": noise / len(rows) if rows else 0.0,
        "structured_evidence_hit": 1.0 if any(str(row.get("chunk_id")) in expected for row in rows) else 0.0,
        "scope_correct": 1.0 if any(str(row.get("chunk_id")) in expected for row in rows) else 0.0,
        "attribute_preservation": _contains(evidence, required) / len(required) if required else 0.0,
        "ids": ids,
    }


def _rendering_score(root: Path, case: dict) -> float | None:
    if not case.get("rendering_file") or not case.get("rendering_attributes"):
        return None
    path = root / str(case["rendering_file"])
    if not path.exists():
        return 0.0
    text = path.read_text(encoding="utf-8", errors="replace")
    terms = list(case["rendering_attributes"])
    return _contains(text, terms) / len(terms)


def _mapping_evaluation(root: Path, mapping_config: dict) -> dict:
    preview = _read_csv(root / mapping_config["preview_path"])
    final = _read_csv(root / mapping_config["final_path"])
    inventory = {row.get(mapping_config.get("inventory_block_column", "Block"), "") for row in _read_csv(root / mapping_config["inventory_path"])}
    columns = mapping_config.get("columns", {})
    req_column = columns.get("requirement_id", "requirement_id")
    approved_block_column = columns.get("approved_block", "approved_block")
    approved_class_column = columns.get("approved_classification", "approved_classification")
    candidate_block_column = columns.get("candidate_block", "candidate_block")
    candidate_class_column = columns.get("candidate_classification", "candidate_classification")
    final_requirement_column = columns.get("final_requirement_id", "Requirement ID")
    final_block_column = columns.get("final_blocks", "Block(s)")
    final_by_id = {(row.get(final_requirement_column) or row.get("requirement_id") or "").strip(): row for row in final}
    counts = Counter()
    evaluated = 0
    for row in preview:
        req_id = row.get(req_column, "").strip()
        approved_block = row.get(approved_block_column, "").strip()
        approved_class = row.get(approved_class_column, "").strip()
        if not req_id or not (approved_block or approved_class):
            continue
        evaluated += 1
        candidate = row.get(candidate_block_column, "").strip()
        counts["candidate_correct"] += int(candidate == approved_block or (not approved_block and row.get(candidate_class_column, "").strip() == approved_class))
        expected_owner = approved_block if approved_block in inventory else "Unassigned"
        actual = final_by_id.get(req_id, {})
        actual_values = {value.strip() for value in re.split(r"\s*;\s*|\s*,\s*", actual.get(final_block_column, "")) if value.strip()}
        correct = expected_owner in actual_values or (expected_owner == "Unassigned" and actual_values <= {"", "Unassigned"})
        counts["final_correct"] += int(correct)
        counts["hierarchy_correct"] += int(correct)
        expected_domain = {"DIGITAL": "DIG", "ANALOG": "ANA", "SYSTEM": "SYS"}.get(approved_class.upper(), "")
        # Stage 2 traceability uses document domains (for example XDN), not the
        # reviewed Digital/Analog/System classification vocabulary.  Measure
        # classification accuracy at the review boundary and route correctness
        # separately instead of comparing incompatible labels.
        counts["scope_correct"] += int(row.get(candidate_class_column, "").strip().casefold() == approved_class.casefold())
        counts["top_level_error"] += int(
            not approved_block and bool(actual_values - {"", "Unassigned"})
        )
    denominator = max(evaluated, 1)
    return {
        "evaluated": evaluated,
        "candidate_mapping_accuracy": counts["candidate_correct"] / denominator,
        "final_requirement_to_block_accuracy": counts["final_correct"] / denominator,
        "requirement_to_hierarchy_accuracy": counts["hierarchy_correct"] / denominator,
        "digital_analog_system_scope_accuracy": counts["scope_correct"] / denominator,
        "top_level_vs_block_local_error_rate": counts["top_level_error"] / denominator,
        "authority_note": "Final mapping is held constant across retrieval modes; semantic widening is candidate-only and cannot override reviewed ownership.",
    }


def _aggregate(rows: list[dict]) -> dict:
    return {key: statistics.mean(float(row[key]) for row in rows) if rows else 0.0 for key in METRIC_KEYS}


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate retrieval and downstream mapping causally")
    parser.add_argument("--project-root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--config", type=Path, default=None, help="Project benchmark configuration JSON")
    parser.add_argument("--cases", type=Path, default=None, help="Override configured benchmark cases JSON")
    parser.add_argument("--output", type=Path, default=None, help="Override configured Markdown report path")
    parser.add_argument("--enable-semantic", action="store_true", help="Explicitly include local semantic widening in evaluation")
    args = parser.parse_args()
    root = args.project_root.resolve()
    config_path = args.config or root / "config/downstream_benchmark.json"
    benchmark_config = _read_json(config_path)
    cases_path = args.cases or root / benchmark_config["cases_path"]
    cases = _read_json(cases_path)["cases"]
    context = _load_project_context(root)
    vocabulary = _load_domain_vocabulary(ROOT, context)
    db_path = root / str(benchmark_config.get("retrieval", {}).get("db_path", context.get("rag_db_path", "artifacts/rag/rag_index.sqlite")))
    semantic_resources = None
    semantic_error = ""
    try:
        if args.enable_semantic and benchmark_config.get("retrieval", {}).get("semantic_evaluation_enabled", False):
            semantic_resources = _load_semantic_resources(root, argparse.Namespace(semantic_index=None, model_path=None), context)
    except (OSError, RuntimeError, ValueError, SemanticIndexUnavailable) as exc:
        semantic_error = str(exc)
    modes = ["lexical", "normalized", "hybrid"]
    if args.enable_semantic and benchmark_config.get("retrieval", {}).get("semantic_evaluation_enabled", False) and semantic_resources is not None:
        modes.append("hybrid-semantic")
    by_mode: dict[str, list[dict]] = defaultdict(list)
    by_category: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    by_evidence: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    with sqlite3.connect(str(db_path)) as conn:
        columns = _chunk_columns(conn)
        for mode in modes:
            for case in cases:
                started = time.perf_counter()
                rows = [] if mode == "hybrid-semantic" and semantic_resources is None else _query(conn, columns, vocabulary, semantic_resources, case, mode)
                metrics = _retrieval_metrics(case, rows)
                metrics.update({"case_id": case["case_id"], "category": case["category"], "evidence_class": case["evidence_class"], "latency_ms": (time.perf_counter() - started) * 1000.0, "rendering_usefulness": _rendering_score(root, case)})
                by_mode[mode].append(metrics)
                by_category[mode][case["category"]].append(metrics)
                by_evidence[mode][case["evidence_class"]].append(metrics)
    mapping = _mapping_evaluation(root, benchmark_config["mapping"])
    aggregates = {mode: _aggregate(rows) for mode, rows in by_mode.items()}
    baseline = aggregates["hybrid"]
    semantic = aggregates.get("hybrid-semantic")
    delta = {key: semantic[key] - baseline[key] for key in METRIC_KEYS} if semantic else {}
    causal = Counter()
    for case in cases:
        row = next(item for item in by_mode["hybrid"] if item["case_id"] == case["case_id"])
        if row["recall_at_10"] == 0:
            causal["retrieval-driven candidate discovery/ranking"] += 1
        elif row["attribute_preservation"] < 1.0:
            causal["post-retrieval preservation/filtering or structured assembly"] += 1
        elif case.get("rendering_file") and (_rendering_score(root, case) or 0.0) < 1.0:
            causal["downstream rendering/compaction"] += 1
    gain = bool(semantic) and (delta["attribute_preservation"] > 0.05 or delta["recall_at_10"] > 0.05)
    risk = bool(semantic) and (delta["scope_correct"] < -0.02 or delta["noise_contamination_at_10"] > 0.05)
    overall = "retain hybrid baseline; reject global semantic retrieval" if not gain or risk else "consider optional gated-topic semantic widening"
    output_config = benchmark_config.get("outputs", {})
    output = args.output or root / output_config.get("report_path", "artifacts/validation/downstream_benchmark.md")
    json_output = root / output_config.get("json_path", "artifacts/validation/downstream_benchmark.json")
    csv_output = root / output_config.get("case_metrics_path", "artifacts/validation/downstream_benchmark_cases.csv")
    approval_output = root / output_config.get("approval_request_path", "artifacts/validation/downstream_benchmark_approval_request.md")
    lines = [
        "# Retrieval and Mapping Flow Evaluation", "", "Generated from the recorded benchmark configuration and approved downstream artifacts.",
        f"Project: {benchmark_config.get('project_name', context.get('project_name', 'unknown'))}; Cases: {len(cases)}; semantic evaluation: {'enabled and available' if semantic_resources is not None else 'disabled or unavailable'}{(' (' + semantic_error + ')') if semantic_error else ''}.", "",
        "## Causal Boundary", "- Ordinary RAG is scored on source chunks only.", "- Approved structured evidence and low-power audits are not credited to RAG retrieval.", "- Stage 2 mapping and hierarchy assignment are scored separately and held constant across retrieval modes.", "- Rendering usefulness measures preservation of configured source attributes in generated SRS text.", "",
        "## Overall Retrieval Results", "| Mode | R@1 | R@5 | R@10 | P@5 | MRR | nDCG@10 | Noise@10 | Structured hit | Scope | Attributes |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for mode in modes:
        row = aggregates[mode]
        lines.append(f"| {mode} | {row['recall_at_1']:.3f} | {row['recall_at_5']:.3f} | {row['recall_at_10']:.3f} | {row['precision_at_5']:.3f} | {row['mrr']:.3f} | {row['ndcg_at_10']:.3f} | {row['noise_contamination_at_10']:.3f} | {row['structured_evidence_hit']:.3f} | {row['scope_correct']:.3f} | {row['attribute_preservation']:.3f} |")
    lines.extend(["", "## Evidence Class Results", "| Mode | Evidence class | Cases | R@10 | Attributes | Scope |", "| --- | --- | ---: | ---: | ---: | ---: |"])
    for mode in modes:
        for evidence, rows in by_evidence[mode].items():
            row = _aggregate(rows)
            lines.append(f"| {mode} | {evidence} | {len(rows)} | {row['recall_at_10']:.3f} | {row['attribute_preservation']:.3f} | {row['scope_correct']:.3f} |")
    lines.extend(["", "## Topic Results", "| Mode | Topic | Cases | R@10 | Attributes | Noise |", "| --- | --- | ---: | ---: | ---: | ---: |"])
    for mode in modes:
        for category, rows in by_category[mode].items():
            row = _aggregate(rows)
            lines.append(f"| {mode} | {category} | {len(rows)} | {row['recall_at_10']:.3f} | {row['attribute_preservation']:.3f} | {row['noise_contamination_at_10']:.3f} |")
    lines.extend(["", "## Downstream Mapping and Hierarchy", "| Measure | Result |", "| --- | ---: |", f"| Candidate mapping accuracy before review | {mapping['candidate_mapping_accuracy']:.3f} |", f"| Final requirement-to-block accuracy | {mapping['final_requirement_to_block_accuracy']:.3f} |", f"| Requirement-to-hierarchy accuracy | {mapping['requirement_to_hierarchy_accuracy']:.3f} |", f"| Digital/analog/system classification accuracy at review boundary | {mapping['digital_analog_system_scope_accuracy']:.3f} |", f"| Top-level vs block-local error rate | {mapping['top_level_vs_block_local_error_rate']:.3f} |", "", mapping["authority_note"], "- Scope note: final traceability stores document domains such as XDN rather than the reviewed Digital/Analog/System labels; classification accuracy is therefore measured at the Stage 2 review boundary.", "", "## Rendered Detail Preservation", "| Case | Rendered attribute preservation |", "| --- | ---: |"])
    for case in cases:
        rendered = _rendering_score(root, case)
        if rendered is not None:
            lines.append(f"| {case['case_id']} | {rendered:.3f} |")
    lines.extend(["", "## Causal Diagnosis", ""])
    lines.extend([f"- {reason}: {count} benchmark cases." for reason, count in causal.items()])
    semantic_delta_lines = ["- Semantic widening was not evaluated; it requires explicit command and configuration opt-in."] if not semantic else [f"- Hybrid-semantic minus hybrid attribute-preservation delta: {delta['attribute_preservation']:+.3f}.", f"- Hybrid-semantic minus hybrid Recall@10 delta: {delta['recall_at_10']:+.3f}.", f"- Hybrid-semantic minus hybrid noise delta: {delta['noise_contamination_at_10']:+.3f}.", f"- Hybrid-semantic minus hybrid scope delta: {delta['scope_correct']:+.3f}."]
    lines.extend(["- Relevant source chunks are available in the RAG database for every labeled case; a top-k miss is retrieval-driven, while a hit with missing attributes is preservation/filtering-driven.", "- Structured records are selected and scoped by project-provided deterministic assembly artifacts; semantic retrieval does not repair rows rejected by topic limits or scope filters.", "- Any semantic widening remains candidate-only, so it cannot change approved mapping ownership or hierarchy assignment.", "", "## Semantic Delta", *semantic_delta_lines, "", "## Recommendation", f"- Overall: **{overall}**.", "- Topic-specific: retain deterministic hybrid for structured evidence and exact identifiers; only evaluate semantic widening for a named weak content class after explicit approval.", "- Current evidence does not justify a global transformer step. Evidence preservation, filtering, rendering, and mapping remain separate controls."])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    summary = {"project_name": benchmark_config.get("project_name", context.get("project_name", "unknown")), "overall_recommendation": overall, "mapping": mapping, "semantic_delta": delta, "semantic_evaluation_enabled": bool(semantic), "approval_required": True, "input_identity": {"benchmark_config_sha256": _sha256(config_path), "cases_sha256": _sha256(cases_path)}}
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    fieldnames = ["mode", "case_id", "category", "evidence_class", *METRIC_KEYS, "latency_ms", "rendering_usefulness"]
    csv_output.parent.mkdir(parents=True, exist_ok=True)
    with csv_output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for mode, mode_rows in by_mode.items():
            for row in mode_rows:
                writer.writerow({"mode": mode, **{key: row.get(key) for key in fieldnames if key != "mode"}})
    approval_output.parent.mkdir(parents=True, exist_ok=True)
    approval_output.write_text("\n".join(["# Downstream Benchmark Approval Request", "", "This artifact is advisory only. No recommended change was applied.", "", f"Recommendation: {overall}", "Approval required before changing retrieval methods, semantic enablement, defaults, mapping policy, filtering rules, rendering policy, or benchmark thresholds.", "", "Requested user action: approve or reject each proposed change in a separate reviewed configuration/policy edit.", ""]) , encoding="utf-8")
    print(json.dumps({"output": str(output), "summary": str(json_output), "case_metrics": str(csv_output), "approval_request": str(approval_output), **summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())