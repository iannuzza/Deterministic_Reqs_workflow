import unittest
from pathlib import Path


class Stage2SysmlRoleTests(unittest.TestCase):
    def test_stage3_gate_treats_stage2_sysml_review_as_non_blocking(self):
        repo_root = Path(__file__).resolve().parents[1]
        gate = (repo_root / "scripts/run_stage3_srs_gate.py").read_text(encoding="utf-8")
        review_section = gate[gate.index("review_path"):gate.index("print(\"Stage 3 SRS full flow")]
        self.assertIn("non-blocking derived-artifact diagnostic", review_section)
        self.assertNotIn("return 2", review_section)

    def test_rules_define_mapping_and_snapshot_as_authority(self):
        repo_root = Path(__file__).resolve().parents[1]
        rules = (repo_root / ".github/copilot-instructions.md").read_text(encoding="utf-8")
        skill = (repo_root / ".github/skills/workflow-stage-gate/SKILL.md").read_text(encoding="utf-8")
        for text in (rules, skill):
            self.assertIn("sole architectural authority", text)
            self.assertIn("Stage 2 SysML is derived", text)


if __name__ == "__main__":
    unittest.main()