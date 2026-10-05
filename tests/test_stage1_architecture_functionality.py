import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import generate_stage1_requirements as stage1


class Stage1ArchitectureFunctionalityTests(unittest.TestCase):
    def test_power_concept_is_detected_deterministically(self):
        self.assertTrue(stage1.POWER_MANAGEMENT_CONCEPT_RE.search("retention domain"))
        self.assertTrue(stage1.POWER_MANAGEMENT_CONCEPT_RE.search("power island"))
        self.assertFalse(stage1.POWER_MANAGEMENT_CONCEPT_RE.search("sensor calibration"))

    def test_configured_power_owner_does_not_invent_a_block(self):
        self.assertEqual(
            stage1._configured_power_management_owner(
                {"Digital Controller": ["controller"], "Unassigned": []}
            ),
            "",
        )
        self.assertEqual(
            stage1._configured_power_management_owner(
                {"Power Management Unit": [], "Unassigned": []}
            ),
            "Power Management Unit",
        )

    def test_full_spec_function_sentence_keeps_source_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            text_path = Path(directory) / "page.txt"
            text_path.write_text(
                "The power domain controls retention behavior and isolation.\n",
                encoding="utf-8",
            )
            candidates = stage1._extract_functional_sentence_candidates(
                text_path.read_text(encoding="utf-8").splitlines(), 7
            )
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].source, "Paragraph 001 (page 7)")
        self.assertIn("power domain", candidates[0].statement.lower())

    def test_architecture_capability_definition_is_detected(self):
        statement = "The sensor hub subsystem provides trigger control and data collection."
        self.assertTrue(stage1._looks_like_architecture_capability(statement))
        self.assertFalse(stage1._looks_like_architecture_capability("This document describes the project."))


if __name__ == "__main__":
    unittest.main()