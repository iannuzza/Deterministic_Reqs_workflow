import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from stage1_descriptive_evidence import (
    extract_indexed_descriptive_candidates,
    extract_stage1_descriptive_evidence,
    validate_stage1_descriptive_records,
)


class Stage1DescriptiveEvidenceTests(unittest.TestCase):
    def test_indexed_candidates_preserve_sections_spans_without_approval_or_owner(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pages = {
                1: "1. Core\n1.1. Description of the Block\nThis unit coordinates the\n",
                2: "2\nmeasurement signals\n\n1.2. Requirements\n[UNIT_ 004] REQUIREMENT:\nIt shall operate. [END]\n2. Start-Up\n2.1. IP Description\nThis unit generates analog startup signals\n2.2. I/O List\nPort name Direction Type Description\ni_clk input clock\n3. Signal Behavior\nThis is not a hardware block, only a signal behavior.\n",
            }
            for page, text in pages.items():
                (root / f"source_p{page:03d}.txt").write_text(text, encoding="utf-8")
            (root / "unindexed_p003.txt").write_text("4. Description\nUnindexed text must never enter the candidate inventory.", encoding="utf-8")
            with (root / "index.csv").open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["source_file", "page", "text_file"])
                writer.writeheader()
                writer.writerows({"source_file": "source.pdf", "page": page, "text_file": f"source_p{page:03d}.txt"} for page in pages)
            records = extract_indexed_descriptive_candidates(
                root / "index.csv", source_context={"source.pdf": {"source_revision": "2"}},
            )
            self.assertEqual(len(records), 3)
            self.assertEqual(records[0]["statement"], "This unit coordinates the measurement signals")
            self.assertEqual([span["page"] for span in json.loads(records[0]["source_spans_json"])], [1, 2])
            self.assertIn("not a hardware block", records[2]["statement"])
            self.assertEqual(records, extract_indexed_descriptive_candidates(root / "index.csv", source_context={"source.pdf": {"source_revision": "2"}}))
            for record in records:
                self.assertEqual(record["admission_state"], "candidate")
                self.assertEqual(record["source_revision"], "2")
                self.assertNotIn("mapped_block", record)
                self.assertNotIn("shall", record["statement"])
                self.assertEqual(record["content_sha256"], hashlib.sha256(record["statement"].encode("utf-8")).hexdigest())

    def test_nested_requirement_headings_do_not_reactivate_narrative_capture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "extract.txt").write_text(
                "1. Requirements\n1.1. Functional behavior\nThis requirement prose is not narrative input.\n"
                "2. Description\nThis domain supports analog measurement.\n", encoding="utf-8")
            (root / "index.csv").write_text("source_file,page,text_file\nsource.pdf,1,extract.txt\n", encoding="utf-8")
            records = extract_indexed_descriptive_candidates(root / "index.csv")
            self.assertEqual([record["statement"] for record in records], ["This domain supports analog measurement."])

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