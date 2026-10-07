import sys
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import generate_stage1_requirements as stage1


class Stage1ArchitectureFunctionalityTests(unittest.TestCase):
    def test_split_tagged_header_preserves_page_line_indices(self):
        lines = ["[TEST_REQ_", "001] Requirement The controller shall retain configuration.", "[End]", "Trailing source text."]
        normalized = stage1._normalize_tagged_header_lines(lines)
        self.assertEqual(len(normalized), len(lines))
        self.assertEqual(normalized[1], "")
        self.assertEqual(normalized[2:], lines[2:])
        self.assertEqual(lines[0], "[TEST_REQ_")
        self.assertEqual(stage1._normalize_tagged_header_lines(normalized), normalized)

    def test_tagged_extraction_after_split_header_keeps_original_indices(self):
        lines = [
            "[TEST_REQ_",
            "001] Requirement The controller shall retain configuration.",
            "[End]",
            "[TEST_REQ_002] Requirement The sensor shall sample the input.",
            "[End]",
            "Trailing source text.",
        ]
        pattern = re.compile(r"^\[(?P<reqid>TEST_REQ_\d+)\]\s*Requirement\s*(?P<body>.*)$")
        with patch.object(stage1, "REQ_ID_TAGGED_START_RE", pattern), \
                patch.object(stage1, "TAG_TERMINATOR", "[End]"):
            first, consumed = stage1._extract_tagged_reqid_candidate(lines, 0, 7)
            self.assertEqual(first.source_req_id, "TEST_REQ_001")
            self.assertEqual(first.statement, "The controller shall retain configuration.")
            self.assertEqual(consumed, 2)
            second, consumed = stage1._extract_tagged_reqid_candidate(lines, consumed + 1, 7)
            self.assertEqual(second.source_req_id, "TEST_REQ_002")
            self.assertEqual(second.statement, "The sensor shall sample the input.")
            self.assertEqual(second.source, "Paragraph 004 (page 7)")
            self.assertEqual(consumed, 4)
            trailing, consumed = stage1._extract_tagged_reqid_candidate(lines, consumed + 1, 7)
            self.assertIsNone(trailing)
            self.assertEqual(consumed, 5)

    def test_missing_terminator_stops_before_next_tagged_requirement(self):
        lines = [
            "[TEST_REQ_001] Requirement: The user shall configure the slot duration.",
            "2. SELECT CHANNEL:",
            "[TEST_REQ_002] Requirement: The user shall select the active channel.",
            "[End]",
        ]
        pattern = re.compile(r"^\[(?P<reqid>TEST_REQ_\d+)\]\s*Requirement:\s*(?P<body>.*)$")
        with patch.object(stage1, "REQ_ID_TAGGED_START_RE", pattern), \
                patch.object(stage1, "TAG_TERMINATOR", "[End]"):
            first, consumed = stage1._extract_tagged_reqid_candidate(lines, 0, 7)
            self.assertEqual(first.statement, "The user shall configure the slot duration.")
            self.assertEqual(consumed, 1)
            second, consumed = stage1._extract_tagged_reqid_candidate(lines, consumed + 1, 7)
            self.assertEqual(second.source_req_id, "TEST_REQ_002")
            self.assertEqual(second.statement, "The user shall select the active channel.")
            self.assertEqual(consumed, 3)

    def test_missing_terminator_preserves_body_until_split_next_page_header(self):
        lines = [
            "[TEST_REQ_001] Requirement: The user shall configure each frame:",
            "1.1 PARAMETERS:",
            "The user shall set the sampling period.",
        ]
        continuation = [
            "The user shall set the gain.",
            "2. SELECT CHANNEL:",
            "[TEST_REQ_",
            "002] Requirement: The user shall select the active channel.",
            "[End]",
        ]
        pattern = re.compile(r"^\[(?P<reqid>TEST_REQ_\d+)\]\s*Requirement:\s*(?P<body>.*)$")
        with patch.object(stage1, "REQ_ID_TAGGED_START_RE", pattern), \
                patch.object(stage1, "TAG_TERMINATOR", "[End]"):
            candidate, consumed = stage1._extract_tagged_reqid_candidate(lines, 0, 7, continuation)
            self.assertIn("1.1 PARAMETERS:", candidate.statement)
            self.assertIn("The user shall set the gain.", candidate.statement)
            self.assertNotIn("SELECT CHANNEL", candidate.statement)
            self.assertNotIn("TEST_REQ_002", candidate.statement)
            self.assertEqual(consumed, 4)

    def test_missing_terminator_stops_at_next_section_preserving_child_content(self):
        lines = [
            "1. FRAME CONFIGURATION:",
            "[TEST_REQ_001] Requirement: The user shall configure each frame:",
            "1.1 PARAMETERS:",
            "1. The user shall set the sampling period.",
        ]
        continuation = [
            "The user shall set the gain.",
            "2. UNRELATED SECTION",
            "Unrelated controller architecture and register descriptions.",
        ]
        pattern = re.compile(r"^\[(?P<reqid>TEST_REQ_\d+)\]\s*Requirement:\s*(?P<body>.*)$")
        with patch.object(stage1, "REQ_ID_TAGGED_START_RE", pattern), \
                patch.object(stage1, "TAG_TERMINATOR", "[End]"):
            candidate, consumed = stage1._extract_tagged_reqid_candidate(lines, 1, 7, continuation)
            self.assertIn("1.1 PARAMETERS:", candidate.statement)
            self.assertIn("1. The user shall set the sampling period.", candidate.statement)
            self.assertIn("The user shall set the gain.", candidate.statement)
            self.assertNotIn("UNRELATED", candidate.statement)
            self.assertNotIn("Unrelated controller", candidate.statement)
            self.assertEqual(consumed, 4)

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