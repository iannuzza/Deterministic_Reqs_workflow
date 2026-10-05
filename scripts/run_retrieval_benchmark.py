#!/usr/bin/env python3
"""Run the project-specific retrieval benchmark and select a safe mode."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from benchmark_rag_retrieval import BenchmarkCase, benchmark_mode, load_benchmark_cases

MODES = ("lexical", "normalized", "hybrid", "semantic", "hybrid-semantic")
FALLBACK_MODE = "hybrid"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_path(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _parse_chunk_ids(path: Path) -> list[str]:
    return re.findall(r"^- chunk_id: (.+)$", path.read_text(encoding="utf-8"), flags=re.MULTILINE)


def _query_mode(root: Path, context: dict, mode: str, query: str, top_k: int, output: Path) -> list[dict]:
    command = [
        sys.executable,
        "scripts/query_rag_index.py",
        "--query",
        query,
        "--mode",
        mode,
        "--top-k",
        str(top_k),
        "--db-path",
        str(_resolve_path(root, str(context["rag_db_path"]))),
        "--output",
        str(output),
    ]
    completed = subprocess.run(command, cwd=root, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError((completed.stdout + completed.stderr).strip() or f"query failed for {mode}")
    query_output = output.read_text(encoding="utf-8")
    if mode in {"semantic", "hybrid-semantic"} and "- Semantic status: unavailable" in query_output:
        raise RuntimeError("semantic resources unavailable")
    return [{"entity_id": item} for item in _parse_chunk_ids(output)]


def _validate_labels(root: Path, context: dict, cases: list[BenchmarkCase]) -> list[str]:
    errors: list[str] = []
    db_path = _resolve_path(root, str(context["rag_db_path"]))
    with sqlite3.connect(db_path) as connection:
        available_chunks = {str(row[0]) for row in connection.execute("SELECT id FROM chunks")}
    for case in cases:
        if not case.expected_entity_ids:
            errors.append(f"{case.query}: no expected entity IDs")
        missing = sorted(set(case.expected_entity_ids) - available_chunks)
        if missing:
            errors.append(f"{case.query}: missing chunk IDs {', '.join(missing)}")
    return errors


def _result_dict(result) -> dict:
    return {
        "mode": result.mode,
        "case_count": result.case_count,
        "recall_at_1": result.recall_at_1,
        "recall_at_5": result.recall_at_5,
        "recall_at_10": result.recall_at_10,
        "mrr": result.mean_reciprocal_rank,
        "mean_latency_ms": result.mean_latency_ms,
        "p95_latency_ms": result.p95_latency_ms,
    }


def run_benchmark(root: Path, context_path: Path, cases_path: Path, output_path: Path, selection_path: Path) -> dict:
    context = _load_json(context_path)
    cases = load_benchmark_cases(cases_path)
    label_errors = _validate_labels(root, context, cases)
    benchmark_config = _load_json(cases_path).get("benchmark", {})
    max_mean = float(benchmark_config.get("max_mean_latency_ms", 100.0))
    max_p95 = float(benchmark_config.get("max_p95_latency_ms", 250.0))
    results: list[dict] = []
    with tempfile.TemporaryDirectory() as directory:
        for mode in MODES:
            try:
                result = benchmark_mode(
                    queries=cases,
                    query_fn=lambda query, top_k, selected_mode=mode: _query_mode(
                        root, context, selected_mode, query, top_k, Path(directory) / f"{selected_mode}.md"
                    ),
                    mode=mode,
                    top_k=int(_load_json(cases_path).get("top_k", 10)),
                )
                row = _result_dict(result)
            except (OSError, RuntimeError, ValueError) as exc:
                row = {"mode": mode, "status": "unavailable", "error": str(exc)}
            results.append(row)

    baseline = next((row for row in results if row["mode"] == FALLBACK_MODE and "recall_at_1" in row), None)
    exact_case = next((case for case in cases if case.category == "exact_requirement_id"), None)
    candidates: list[dict] = []
    for row in results:
        row["status"] = row.get("status", "measured")
        row["passes_latency"] = row.get("mean_latency_ms", float("inf")) <= max_mean and row.get("p95_latency_ms", float("inf")) <= max_p95
        row["passes_exact_id"] = True
        if exact_case is not None and baseline is not None:
            row["passes_exact_id"] = row.get("recall_at_1", 0.0) >= baseline.get("recall_at_1", 0.0)
        row["passes_benchmark"] = not label_errors and row.get("status") == "measured" and row.get("recall_at_1", 0.0) >= 0.0 and row.get("passes_latency", False) and row.get("passes_exact_id", False)
        if row["passes_benchmark"]:
            candidates.append(row)

    selected = FALLBACK_MODE
    if not label_errors and candidates:
        selected = max(candidates, key=lambda row: (row.get("mrr", 0.0), row.get("recall_at_10", 0.0), -row.get("mean_latency_ms", float("inf"))))["mode"]
    decision_evidence = []
    baseline_recall_at_1 = baseline.get("recall_at_1") if baseline else None
    for row in results:
        reasons = []
        if label_errors:
            reasons.append("invalid benchmark labels")
        if row.get("status") != "measured":
            reasons.append("retrieval mode unavailable")
        if not row.get("passes_latency", False):
            reasons.append("latency threshold failed")
        if not row.get("passes_exact_id", False):
            reasons.append("exact-ID recall regressed")
        decision_evidence.append(
            {
                "mode": row.get("mode"),
                "status": row.get("status"),
                "recall_at_1": row.get("recall_at_1"),
                "recall_at_5": row.get("recall_at_5"),
                "recall_at_10": row.get("recall_at_10"),
                "mrr": row.get("mrr"),
                "mean_latency_ms": row.get("mean_latency_ms"),
                "p95_latency_ms": row.get("p95_latency_ms"),
                "passes_labels": not bool(label_errors),
                "passes_latency": row.get("passes_latency", False),
                "passes_exact_id": row.get("passes_exact_id", False),
                "passes_benchmark": row.get("passes_benchmark", False),
                "failure_reasons": reasons,
            }
        )
    if selected == FALLBACK_MODE:
        decision_reason = "; ".join(
            [
                "no non-fallback method passed all selection gates",
                f"fallback={FALLBACK_MODE}",
                f"exact_id_baseline_recall_at_1={baseline_recall_at_1}",
                f"label_errors={len(label_errors)}",
            ]
        )
    else:
        decision_reason = f"{selected} passed labels, latency, exact-ID, and benchmark gates"
    selection = {
        "project_name": context.get("project_name", root.name),
        "final_method_decision": selected,
        "selected_mode": selected,
        "fallback_mode": FALLBACK_MODE,
        "selection_reason": "benchmark_pass" if selected != FALLBACK_MODE else "fallback_to_legacy_hybrid",
        "decision_reason": decision_reason,
        "decision_evidence": {
            "benchmark_case_count": len(cases),
            "benchmark_labels_valid": not bool(label_errors),
            "exact_id_baseline_mode": FALLBACK_MODE,
            "exact_id_baseline_recall_at_1": baseline_recall_at_1,
            "candidate_modes_passing_all_gates": [row.get("mode") for row in candidates],
            "per_mode": decision_evidence,
        },
        "label_errors": label_errors,
        "thresholds": {"max_mean_latency_ms": max_mean, "max_p95_latency_ms": max_p95},
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"project_name": selection["project_name"], "selection": selection, "results": results}, indent=2) + "\n", encoding="utf-8")
    selection_path.parent.mkdir(parents=True, exist_ok=True)
    selection_path.write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"project_name": selection["project_name"], "selected_mode": selected, "results": results}, indent=2))
    return selection


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the active project's live retrieval benchmark")
    parser.add_argument("--project-context", type=Path, default=Path("config/project_context.json"))
    parser.add_argument("--cases", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--selection", type=Path, default=None)
    args = parser.parse_args()
    root = Path.cwd()
    context = _load_json(args.project_context)
    cases_path = args.cases or _resolve_path(root, str(context.get("retrieval_benchmark_cases_path", "config/retrieval_benchmark_cases.json")))
    output_path = args.output or _resolve_path(root, str(context.get("retrieval_benchmark_report_path", "artifacts/rag/retrieval_benchmark_report.json")))
    selection_path = args.selection or _resolve_path(root, str(context.get("retrieval_selection_path", "config/retrieval_selection.json")))
    run_benchmark(root, args.project_context, cases_path, output_path, selection_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
