import sys
import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from pre_freeze_coherence_gate import classify_warning, gate_decision
from pre_freeze_coherence_gate import authority_fingerprint
from freeze_stage2b_snapshot import freeze


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


class FreezeValidationRefreshTests(unittest.TestCase):
    def _report(self, root, *, errors=0, findings=None):
        return {"result": "FAIL" if errors else "PASS", "counts": {"ERROR": errors},
                "authority_fingerprint": authority_fingerprint(root), "findings": findings or []}

    def test_stale_pass_is_revalidated_before_approval_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "artifacts/validation/source_to_stage2b_coherence.json"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(json.dumps({"result": "PASS", "counts": {"ERROR": 0}, "authority_fingerprint": "stale"}), encoding="utf-8")
            refreshed = self._report(root)
            with patch("freeze_stage2b_snapshot.validate_source_coherence", return_value=refreshed) as validate, \
                    patch("freeze_stage2b_snapshot.validate_approval_evidence", side_effect=RuntimeError("approval boundary")) as approval, \
                    patch("freeze_stage2b_snapshot._register_approved_profiles") as register, \
                    patch("freeze_stage2b_snapshot.create_approved_snapshot") as snapshot:
                with self.assertRaisesRegex(RuntimeError, "approval boundary"):
                    freeze(root, "reviewer")
                validate.assert_called_once_with(root)
                approval.assert_called_once()
                register.assert_not_called()
                snapshot.assert_not_called()
            self.assertEqual(json.loads(report_path.read_text(encoding="utf-8")), refreshed)
            gate = json.loads(report_path.with_name("pre_freeze_coherence_gate.json").read_text(encoding="utf-8"))
            self.assertEqual(gate["decision"], "GO_ON")
            self.assertTrue(gate["authority_fingerprint_matches"])

    def test_new_errors_replace_old_pass_and_block_authority_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "artifacts/validation/source_to_stage2b_coherence.json"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(json.dumps(self._report(root)), encoding="utf-8")
            refreshed = self._report(root, errors=1, findings=[{"severity": "ERROR", "category": "canonical", "message": "Missing approved revision"}])
            with patch("freeze_stage2b_snapshot.validate_source_coherence", return_value=refreshed), \
                    patch("freeze_stage2b_snapshot.validate_approval_evidence") as approval, \
                    patch("freeze_stage2b_snapshot.connect") as connection, \
                    patch("freeze_stage2b_snapshot.create_approved_snapshot") as snapshot:
                with self.assertRaisesRegex(RuntimeError, "STOP_BEFORE_PHASE2"):
                    freeze(root, "reviewer")
                approval.assert_not_called()
                connection.assert_not_called()
                snapshot.assert_not_called()
            self.assertEqual(json.loads(report_path.read_text(encoding="utf-8"))["result"], "FAIL")

    def test_revalidation_does_not_bypass_warning_blockers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            refreshed = self._report(root, findings=[{"severity": "WARNING", "category": "hierarchical_placement", "message": "Unresolved hierarchy_parent_req_ids"}])
            with patch("freeze_stage2b_snapshot.validate_source_coherence", return_value=refreshed), \
                    patch("freeze_stage2b_snapshot.connect") as connection:
                with self.assertRaisesRegex(RuntimeError, "STOP_BEFORE_STAGE2B_FREEZE"):
                    freeze(root, "reviewer")
                connection.assert_not_called()

    def test_authority_change_after_validation_still_blocks_freeze(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            refreshed = self._report(root)

            def validate_then_change_authority(repo_root):
                mapping = repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
                mapping.parent.mkdir(parents=True)
                mapping.write_text("changed authority", encoding="utf-8")
                return refreshed

            with patch("freeze_stage2b_snapshot.validate_source_coherence", side_effect=validate_then_change_authority), \
                    patch("freeze_stage2b_snapshot.connect") as connection:
                with self.assertRaisesRegex(RuntimeError, "STOP_BEFORE_PHASE2"):
                    freeze(root, "reviewer")
                connection.assert_not_called()

    def test_freeze_binds_only_current_revisions_and_approved_mappings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            connection = MagicMock()
            queries = []

            def current_authority_query(query, parameters):
                self.assertNotIn("snapshots", query.casefold())
                queries.append(query)
                cursor = MagicMock()
                if "FROM canonical_requirements" in query:
                    self.assertIn("current_revision_id IS NOT NULL", query)
                    cursor.fetchall.return_value = [("current-revision",)]
                else:
                    self.assertIn("FROM architecture_mappings", query)
                    self.assertIn("lifecycle_state = 'approved'", query)
                    cursor.fetchall.return_value = [("current-approved-mapping",)]
                return cursor

            connection.execute.side_effect = current_authority_query
            with patch("freeze_stage2b_snapshot.validate_source_coherence", return_value=self._report(root)), \
                    patch("freeze_stage2b_snapshot.validate_approval_evidence", return_value=[]), \
                    patch("freeze_stage2b_snapshot.validate_pre_freeze_coverage", return_value={"status": "pass"}), \
                    patch("freeze_stage2b_snapshot._register_approved_profiles"), \
                    patch("freeze_stage2b_snapshot.connect", return_value=connection), \
                    patch("freeze_stage2b_snapshot.create_approved_snapshot", return_value="new-snapshot") as create, \
                    patch("builtins.print"):
                freeze(root, "reviewer")
            self.assertEqual(len(queries), 2)
            create.assert_called_once()
            self.assertEqual(create.call_args.kwargs["canonical_revision_ids"], ["current-revision"])
            self.assertEqual(create.call_args.kwargs["mapping_ids"], ["current-approved-mapping"])
            self.assertEqual(create.call_args.kwargs["approved_by"], "reviewer")


if __name__ == "__main__":
    unittest.main()