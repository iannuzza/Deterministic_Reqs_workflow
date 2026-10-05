import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from pre_freeze_coherence_gate import classify_warning, gate_decision


class PreFreezeCoherenceGateTests(unittest.TestCase):
    def test_hierarchy_proxy_blocks_freeze(self):
        finding = {"category": "hierarchical_placement", "message": "Generic approved_block may be acting as ownership proxy"}
        self.assertEqual(classify_warning(finding), "BLOCK_BEFORE_STAGE2B_FREEZE")

    def test_stale_batch_is_hardening_only(self):
        finding = {"category": "stale_state", "message": "Historical/superseded ingestion batch coexists with active batch"}
        self.assertEqual(classify_warning(finding), "HARDEN_LATER")

    def test_decision_rules(self):
        self.assertEqual(gate_decision([], phase1_pass=False, fingerprint_matches=True), "STOP_BEFORE_PHASE2")
        self.assertEqual(gate_decision(["BLOCK_BEFORE_STAGE2B_FREEZE"], phase1_pass=True, fingerprint_matches=True), "STOP_BEFORE_STAGE2B_FREEZE")
        self.assertEqual(gate_decision(["BLOCK_BEFORE_DOWNSTREAM"], phase1_pass=True, fingerprint_matches=True), "GO_ON_WITH_DOWNSTREAM_BLOCKERS")
        self.assertEqual(gate_decision(["INFO_ONLY", "HARDEN_LATER"], phase1_pass=True, fingerprint_matches=True), "GO_ON")


if __name__ == "__main__":
    unittest.main()