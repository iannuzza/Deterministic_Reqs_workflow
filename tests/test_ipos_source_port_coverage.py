import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_downstream_coherence import _check_ipos_source_port_coverage
from validate_downstream_coherence import _check_sysml_artifacts, resolve_downstream_contract


class IposSourcePortCoverageTests(unittest.TestCase):
    def test_all_materialized_ipos_blocks_match_approved_source_ports(self):
        findings, summary = _check_ipos_source_port_coverage(Path(__file__).resolve().parents[1])
        self.assertEqual(findings, [])
        self.assertGreater(summary["expected_rows"], 0)
        self.assertEqual(summary["expected_rows"] * 2, summary["checked_rows"])

    def test_system_ports_are_checked_against_system_sysml(self):
        repo_root = Path(__file__).resolve().parents[1]
        contract = resolve_downstream_contract(repo_root, "snap-b2e8101b00dc6909feaed885")
        findings, summary = _check_sysml_artifacts(repo_root, contract.expected)
        self.assertNotIn("SYSML_PORT_MISSING: STBIOSystem: AV1V8", findings)
        self.assertGreaterEqual(summary["approved_port_rows_checked"], 48)


if __name__ == "__main__":
    unittest.main()