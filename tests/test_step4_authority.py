import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from approved_profile_resolver import ProfileResolutionError
from approved_snapshot_resolver import ApprovedResolverError, resolve_authoritative_input
from audit_log import record_event
from canonical_store import connect, fingerprint
from conflict_review_service import build_conflict_report
from rollback_service import rollback_requirement_revision, supersede_snapshot
from snapshot_manager import SnapshotError, create_approved_snapshot, resolve_approved_snapshot


class Step4AuthorityTests(unittest.TestCase):
    def _base(self, root: Path):
        connection = connect(root)
        connection.executescript(
            """
            INSERT INTO projects(project_id, project_name, created_at) VALUES ('p1', 'Demo', 'now');
            INSERT INTO source_specs(source_spec_id, project_id, source_name, source_kind, created_at) VALUES ('spec-1', 'p1', 'source.pdf', 'primary', 'now');
            INSERT INTO source_revisions(source_revision_id, source_spec_id, revision_number, revision_date, content_fingerprint, ingestion_timestamp) VALUES ('srev-1', 'spec-1', '1', '2026-01-01', 'source-hash', 'now');
            INSERT INTO ingestion_batches(ingestion_batch_id, project_id, batch_kind, started_at) VALUES ('ib-1', 'p1', 'supplementary', 'now');
            INSERT INTO staging_batches(staging_batch_id, ingestion_batch_id, workflow_state, created_at) VALUES ('sb-1', 'ib-1', 'S2_DETERMINISTIC_CLASSIFICATION', 'now');
            INSERT INTO canonical_requirements(canonical_requirement_id, project_id, source_req_id, current_revision_id, created_at, updated_at) VALUES ('can-1', 'p1', 'REQ-1', 'rev-1', 'now', 'now');
            INSERT INTO canonical_requirement_revisions(revision_id, canonical_requirement_id, revision_number, requirement_text, content_fingerprint, approved_classification, created_at) VALUES ('rev-1', 'can-1', 1, 'The controller shall reset.', 'req-hash', 'functional', 'now');
            INSERT INTO requirement_provenance(revision_id, source_spec_id, source_revision_id, source_req_id) VALUES ('rev-1', 'spec-1', 'srev-1', 'REQ-1');
            """
        )
        for kind in ("vocabulary", "taxonomy", "architecture"):
            payload = json.dumps({"kind": kind, "version": "1"})
            connection.execute(
                "INSERT INTO profile_revisions(profile_revision_id, project_id, profile_kind, profile_name, revision_number, profile_payload_json, content_fingerprint, lifecycle_state, approval_state, approved_by, approved_at, created_at) VALUES (?, 'p1', ?, ?, '1', ?, ?, 'approved', 'approved', 'tester', '2026-09-08', '2026-09-08')",
                (f"profile-{kind}", kind, kind, payload, fingerprint({"kind": kind, "version": "1"})),
            )
        connection.commit()
        connection.close()

    def test_snapshot_is_deterministic_and_requires_approved_profiles(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._base(root)
            first = create_approved_snapshot(root, project_id="p1", canonical_revision_ids=["rev-1"], mapping_ids=[], approved_by="tester", retrieval={"version": "1", "hash": "r"}, semantic_enabled=False)
            second = create_approved_snapshot(root, project_id="p1", canonical_revision_ids=["rev-1"], mapping_ids=[], approved_by="tester", retrieval={"version": "1", "hash": "r"}, semantic_enabled=False)
            self.assertEqual(first, second)
            self.assertEqual(resolve_approved_snapshot(root, snapshot_id=first)["status"], "approved")

    def test_impacted_snapshot_is_rejected_and_supersession_is_tracked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._base(root)
            snapshot_id = create_approved_snapshot(root, project_id="p1", canonical_revision_ids=["rev-1"], mapping_ids=[], approved_by="tester", retrieval={"version": "1", "hash": "r"}, semantic_enabled=False)
            connection = connect(root)
            connection.execute("UPDATE snapshots SET status = 'impacted' WHERE snapshot_id = ?", (snapshot_id,))
            connection.commit()
            connection.close()
            with self.assertRaises(SnapshotError):
                resolve_approved_snapshot(root, snapshot_id=snapshot_id)
            rollback_id = supersede_snapshot(root, project_id="p1", snapshot_id=snapshot_id, actor="tester", reason="superseded by new evidence")
            self.assertTrue(rollback_id.startswith("rollback-"))

    def test_audit_event_exports_jsonl_and_requirement_rollback_preserves_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._base(root)
            event_id = record_event(root, event_type="report_generated", entity_type="report", entity_id="report-1", message="test", project_id="p1")
            rollback_id = rollback_requirement_revision(root, project_id="p1", canonical_requirement_id="can-1", target_revision_id="rev-1", actor="tester", reason="restore approved revision")
            self.assertGreater(event_id, 0)
            self.assertTrue(rollback_id.startswith("rollback-"))
            self.assertTrue((root / "artifacts/audit/events.jsonl").exists())
            connection = connect(root)
            self.assertGreater(connection.execute("SELECT COUNT(*) FROM rollback_records").fetchone()[0], 0)
            connection.close()

    def test_resolver_rejects_missing_approved_snapshot_context(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ApprovedResolverError):
                resolve_authoritative_input(root, "3", project_id="p1", snapshot_id="missing")

    def test_conflict_report_preserves_versions_and_proposed_latest_winner(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._base(root)
            connection = connect(root)
            connection.execute("INSERT INTO source_revisions(source_revision_id, source_spec_id, revision_number, revision_date, content_fingerprint, ingestion_timestamp) VALUES ('srev-2', 'spec-1', '2', '2026-09-01', 'source-hash-2', 'now')")
            connection.execute("INSERT INTO staged_requirements(staged_id, staging_batch_id, source_revision_id, source_req_id, requirement_text, proposed_classification, review_decision, content_fingerprint) VALUES ('stage-1', 'sb-1', 'srev-1', 'REQ-1', 'Old text.', 'conflict', 'approval_required', 'a')")
            connection.execute("INSERT INTO staged_requirements(staged_id, staging_batch_id, source_revision_id, source_req_id, requirement_text, proposed_classification, review_decision, content_fingerprint) VALUES ('stage-2', 'sb-1', 'srev-2', 'REQ-1', 'New text.', 'conflict', 'approval_required', 'b')")
            connection.commit()
            connection.close()
            report = build_conflict_report(root, project_id="p1", staging_batch_id="sb-1")
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(payload["conflicts"][0]["default_proposed_winner"], "stage-2")
            self.assertEqual(payload["conflicts"][0]["approval_status"], "approval_required")


if __name__ == "__main__":
    unittest.main()
