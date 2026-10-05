import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from stage1_descriptive_evidence import (
    extract_stage1_descriptive_evidence,
    validate_stage1_descriptive_records,
)


class Stage1DescriptiveEvidenceTests(unittest.TestCase):
    def test_extracts_system_and_unique_runtime_block_scope_with_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source_p001.txt").write_text(
                "1. Contents ........ 1\n"
                "2. System overview\n"
                "The system coordinates approved data movement.\n\n"
                "The Core block manages local processing.\n\n"
                "The Core and I/O blocks exchange data.\n",
                encoding="utf-8",
            )
            records = extract_stage1_descriptive_evidence(
                root / "index.csv", block_names=["Core", "I/O"]
            )

        self.assertEqual([record["scope"] for record in records], ["system", "block_local", "system"])
        self.assertEqual(records[1]["mapped_block"], "Core")
        self.assertIn("page 1", records[0]["source"])
        self.assertEqual(validate_stage1_descriptive_records(records), [])

    def test_rejects_normative_or_linkage_text_in_project_agnostic_records(self):
        findings = validate_stage1_descriptive_records([
            {"statement": "The unit shall operate.", "source": "Stage 1 OCR page 1, line 1", "scope": "system"},
            {"statement": "Context Covers: SRS-REQ-001.", "source": "page 1", "scope": "system"},
        ])
        self.assertIn("stage1_descriptive_record_0_contains_normative_modality", findings)
        self.assertIn("stage1_descriptive_record_1_contains_normative_linkage", findings)


if __name__ == "__main__":
    unittest.main()