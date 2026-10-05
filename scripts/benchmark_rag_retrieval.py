#!/usr/bin/env python3
"""Benchmark deterministic retrieval callables without external services."""

from __future__ import annotations

import argparse
import json
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


@dataclass(frozen=True)
class BenchmarkCase:
    query: str
    expected_entity_ids: tuple[str, ...]
    category: str = ""


@dataclass(frozen=True)
class BenchmarkResult:
    mode: str
    case_count: int
    recall_at_1: float
    recall_at_5: float
    recall_at_10: float
    mean_reciprocal_rank: float
    mean_latency_ms: float
    p95_latency_ms: float


def load_project_name(path: Path) -> str:
    """Read the active project identity for report metadata only."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    project_name = str(payload.get("project_name", "")).strip()
    if not project_name:
        raise ValueError(f"project_name is missing from {path}")
    return project_name


def load_benchmark_cases(path: Path) -> list[BenchmarkCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("cases", payload) if isinstance(payload, dict) else payload
    return [BenchmarkCase(str(row["query"]), tuple(str(item) for item in row["expected_entity_ids"]), str(row.get("category", ""))) for row in rows]


def _ids(row: object) -> str:
    if isinstance(row, dict):
        return str(row.get("entity_id", row.get("chunk_id", "")))
    return str(getattr(row, "entity_id", ""))


def benchmark_mode(
    *,
    queries: Sequence[BenchmarkCase],
    query_fn: Callable[[str, int], list[object]],
    mode: str,
    top_k: int = 10,
) -> BenchmarkResult:
    latencies: list[float] = []
    hits = {1: 0, 5: 0, 10: 0}
    reciprocal_ranks: list[float] = []
    for case in queries:
        started = time.perf_counter()
        results = query_fn(case.query, top_k)
        latencies.append((time.perf_counter() - started) * 1000.0)
        result_ids = [_ids(item) for item in results]
        expected = set(case.expected_entity_ids)
        first_rank = next((rank for rank, item_id in enumerate(result_ids, start=1) if item_id in expected), None)
        reciprocal_ranks.append(1.0 / first_rank if first_rank else 0.0)
        for limit in hits:
            if expected.intersection(result_ids[:limit]):
                hits[limit] += 1
    count = len(queries)
    if not count:
        raise ValueError("benchmark requires at least one case")
    ordered = sorted(latencies)
    p95_index = min(len(ordered) - 1, max(0, int(len(ordered) * 0.95) - 1))
    return BenchmarkResult(mode, count, hits[1] / count, hits[5] / count, hits[10] / count, statistics.mean(reciprocal_ranks), statistics.mean(latencies), ordered[p95_index])


def compare_modes(*, benchmark_cases: Sequence[BenchmarkCase], query_functions: dict[str, Callable[[str, int], list[object]]], top_k: int = 10) -> list[BenchmarkResult]:
    return [benchmark_mode(queries=benchmark_cases, query_fn=query_fn, mode=mode, top_k=top_k) for mode, query_fn in query_functions.items()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark retrieval callables supplied by a Python integration")
    parser.add_argument("benchmark_cases", type=Path)
    parser.add_argument("--project-context", type=Path, default=Path("config/project_context.json"))
    args = parser.parse_args()
    cases = load_benchmark_cases(args.benchmark_cases)
    project_name = load_project_name(args.project_context)
    print(json.dumps({"project_name": project_name, "case_count": len(cases), "modes": ["hybrid", "hybrid-semantic"]}, indent=2))
    print("Provide query functions through compare_modes(...) from an integration or test harness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
