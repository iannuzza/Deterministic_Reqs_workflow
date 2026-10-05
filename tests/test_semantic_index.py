"""Focused tests for the exact cosine semantic index."""

from __future__ import annotations

import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retrieval.embeddings import LocalHashEmbeddingModel  # noqa: E402
from retrieval.models import IndexedEntity  # noqa: E402
from retrieval.semantic_index import ExactCosineIndex, semantic_search  # noqa: E402


class SemanticIndexTests(unittest.TestCase):
    def test_build_search_and_round_trip(self) -> None:
        model = LocalHashEmbeddingModel(dimension=64)
        entities = [
            IndexedEntity("requirement:a", "requirement", "a", "Entity type: requirement\nName: a\nRequirement: clock gating"),
            IndexedEntity("requirement:b", "requirement", "b", "Entity type: requirement\nName: b\nRequirement: temperature limit"),
        ]
        index = ExactCosineIndex()
        index.build(entities, model)
        results = index.search(model.embed_query("clock gating"), 2)
        self.assertEqual(results[0].entity_id, "requirement:a")
        self.assertGreaterEqual(results[0].semantic_score, results[1].semantic_score)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "semantic"
            index.save(path)
            loaded = ExactCosineIndex.load(path)
            self.assertEqual([item.entity_id for item in loaded.search(model.embed_query("clock gating"), 2)], [item.entity_id for item in results])

    def test_invalid_top_k_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ExactCosineIndex().search([], 0)

    def test_semantic_search_filters_entity_types_and_reranks(self) -> None:
        model = LocalHashEmbeddingModel(dimension=64)
        entities = [
            IndexedEntity("block:a", "block", "a", "Entity type: block\nName: a\nFunction: clock gating"),
            IndexedEntity("chunk:z", "chunk", "z", "Entity type: chunk\nName: z\nRequirement: clock gating"),
        ]
        index = ExactCosineIndex()
        index.build(entities, model)
        results = semantic_search(query="clock gating", top_k=1, index=index, embedding_model=model, entity_types={"chunk"})
        self.assertEqual(results[0].entity_id, "chunk:z")
        self.assertEqual(results[0].rank_semantic, 1)


if __name__ == "__main__":
    unittest.main()
