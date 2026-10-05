"""Focused tests for generalized RRF fusion."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retrieval.fusion import (  # noqa: E402
    fuse_lexical_normalized,
    fuse_lexical_normalized_semantic,
)


class FusionTests(unittest.TestCase):
    def test_two_channel_wrapper_preserves_ranks_and_scores(self) -> None:
        rows = fuse_lexical_normalized(
            [{"chunk_id": 1, "lexical_score": -2.0}],
            [{"chunk_id": 1, "normalized_score": -1.0}],
            final_top_k=1,
        )
        self.assertEqual(rows[0]["rank_lexical"], 1)
        self.assertEqual(rows[0]["rank_normalized"], 1)
        self.assertAlmostEqual(rows[0]["rrf_score"], 2 / 61)

    def test_three_channel_fusion_exposes_semantic_rank(self) -> None:
        rows = fuse_lexical_normalized_semantic(
            [{"chunk_id": 1, "lexical_score": -2.0}],
            [],
            [{"chunk_id": 1, "semantic_score": 0.91}],
            final_top_k=1,
        )
        self.assertEqual(rows[0]["rank_semantic"], 1)
        self.assertEqual(rows[0]["semantic_score"], 0.91)

    def test_protected_exact_result_cannot_be_demoted(self) -> None:
        rows = fuse_lexical_normalized_semantic(
            [{"chunk_id": 1, "lexical_score": -2.0}],
            [],
            [{"chunk_id": 2, "semantic_score": 0.99}],
            final_top_k=1,
            protected_ids={1},
        )
        self.assertEqual(rows[0]["chunk_id"], 1)


if __name__ == "__main__":
    unittest.main()
