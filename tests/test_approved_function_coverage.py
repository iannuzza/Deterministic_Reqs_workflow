import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_downstream_coherence import _check_approved_function_coverage


class ApprovedFunctionCoverageTests(unittest.TestCase):
    def _contract(self):
        requirements = [
            {
                "canonical_id": "CAN-ONE",
                "source_req_id": "REQ-ONE",
                "requirement_statement": "When ALPHA_FSM is active, the controller shall control data flow.",
            },
            {
                "canonical_id": "CAN-TWO",
                "source_req_id": "REQ-TWO",
                "requirement_statement": "When BETA Phases is active, the controller shall process data.",
            },
        ]
        allocation = {
            "CAN-ONE": {"owning_target": "Digital IPOS", "approved_block": "Block A"},
            "CAN-TWO": {"owning_target": "Digital IPOS", "approved_block": "Block A"},
        }
        expected = {
            row["source_req_id"]: {**allocation[row["canonical_id"]], "canonical_id": row["canonical_id"]}
            for row in requirements
        }
        return SimpleNamespace(requirement_input=SimpleNamespace(rows=requirements), expected=expected)

    def test_missing_approved_structural_function_blocks_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            block = root / "artifacts/stage6_digital_ipos/blocks/block-a"
            block.mkdir(parents=True)
            (block / "block_a.md").write_text("## 1. Block overview\n**ALPHA_FSM.** Present.\n", encoding="utf-8")
            findings, summary = _check_approved_function_coverage(root, self._contract())
        self.assertEqual(summary["expected"], 2)
        self.assertEqual(summary["present"], 1)
        self.assertEqual(len(findings), 1)
        self.assertIn("APPROVED_FUNCTION_MISSING_FROM_GENERATED_SPEC", findings[0])
        self.assertIn("BETA Phases", findings[0])

    def test_separator_variants_are_accepted_as_the_same_function(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            block = root / "artifacts/stage6_digital_ipos/blocks/block-a"
            block.mkdir(parents=True)
            (block / "block_a.md").write_text(
                "## 1. Block overview\n**ALPHA FSM.** Present.\n**BETA_Phases.** Present.\n",
                encoding="utf-8",
            )
            findings, summary = _check_approved_function_coverage(root, self._contract())
        self.assertFalse(findings)
        self.assertEqual(summary["expected"], summary["present"])


if __name__ == "__main__":
    unittest.main()