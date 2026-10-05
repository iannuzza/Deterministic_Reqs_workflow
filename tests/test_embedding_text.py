"""Focused tests for Step A retrieval data contracts."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retrieval.embedding_text import (  # noqa: E402
    build_block_embedding_text,
    build_requirement_embedding_text,
    canonical_full_text_for_embedding,
    validate_embedding_text,
)
from retrieval.models import IndexedEntity  # noqa: E402


class EmbeddingTextTests(unittest.TestCase):
    def test_canonical_text_is_deterministic_and_labeled(self) -> None:
        kwargs = {
            "entity_type": "block",
            "name": "I2C_SPI_AHB",
            "function": "Translate AHB transactions",
            "inputs": ["Host bus", "configuration data"],
            "outputs": ["Protocol-compliant responses"],
        }
        self.assertEqual(canonical_full_text_for_embedding(**kwargs), canonical_full_text_for_embedding(**kwargs))
        self.assertIn("Entity type: block", canonical_full_text_for_embedding(**kwargs))
        self.assertIn("Name: I2C_SPI_AHB", canonical_full_text_for_embedding(**kwargs))

    def test_entity_specific_builders_preserve_ids_and_technical_terms(self) -> None:
        block_text = build_block_embedding_text(
            {"Block": "Sensor Hub", "Function": "Format ADC samples", "Inputs": "ADC_DATA; FIFO mode"}
        )
        requirement_text = build_requirement_embedding_text(
            {"source_req_id": "DDS_STBIO1_0104", "Requirement": "The ADC shall support clock gating."}
        )
        self.assertIn("Sensor Hub", block_text)
        self.assertIn("FIFO mode", block_text)
        self.assertIn("DDS_STBIO1_0104", requirement_text)
        self.assertIn("clock gating", requirement_text)

    def test_indexed_entity_rejects_empty_embedding_text(self) -> None:
        with self.assertRaises(ValueError):
            IndexedEntity("requirement:x", "requirement", "x", "")

    def test_validation_requires_identity_labels(self) -> None:
        entity = IndexedEntity("block:x", "block", "x", "Entity type: block\nName: x")
        validate_embedding_text(entity)
        invalid = IndexedEntity("block:y", "block", "y", "Name: y")
        with self.assertRaises(ValueError):
            validate_embedding_text(invalid)


if __name__ == "__main__":
    unittest.main()
