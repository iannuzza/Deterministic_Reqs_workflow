"""Focused tests for deterministic retrieval benchmark metrics."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.benchmark_rag_retrieval import BenchmarkCase, benchmark_mode  # noqa: E402
from scripts.query_rag_index import _requirement_id_mapping_check  # noqa: E402


class BenchmarkTests(unittest.TestCase):
    def test_metrics_measure_expected_ids(self) -> None:
        cases = [BenchmarkCase("clock", ("a",), "technical")]
        result = benchmark_mode(
            queries=cases,
            query_fn=lambda _query, _top_k: [{"entity_id": "a"}, {"entity_id": "b"}],
            mode="hybrid-semantic",
        )
        self.assertEqual(result.case_count, 1)
        self.assertEqual(result.recall_at_1, 1.0)
        self.assertEqual(result.recall_at_5, 1.0)
        self.assertEqual(result.mean_reciprocal_rank, 1.0)

    def test_requirement_id_audit_reports_stage1_owner(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = _requirement_id_mapping_check(
            root,
            "DDS_STBIO1_0104",
            [{"chunk_id": 151, "chunk_text": "DDS_STBIO1_0104 power-on POR"}],
        )
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["checks"][0]["expected_owner"], "PMU")


if __name__ == "__main__":
    unittest.main()
