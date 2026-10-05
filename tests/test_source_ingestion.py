import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ingest_source_spec import discover_tag_pattern


class SourceIngestionTests(unittest.TestCase):
    def test_discovers_bracketed_tagged_requirement_family(self):
        pattern = discover_tag_pattern([
            "[IPOS_STBIO1_MAIN_CONTROLLER_ 7096] REQUIREMENT:\nThe controller shall enter operative mode.",
            "[IPOS_STBIO1_MAIN_CONTROLLER_5015] Requirement:\nThe controller shall support reset.",
            "PPG signal description",
        ])
        self.assertEqual(pattern, r"IPOS_STBIO1_MAIN_CONTROLLER_\d+")

    def test_rejects_sources_without_tagged_requirement_headers(self):
        with self.assertRaises(ValueError):
            discover_tag_pattern(["The device shall expose a status register."])


if __name__ == "__main__":
    unittest.main()