import unittest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from approved_snapshot_resolver import ApprovedResolverError, resolve_complete_authoritative_input
from run_allocation_crosscheck import validate_materialization_manifest
from requirement_corpus import RequirementInput
from snapshot_manager import create_approved_snapshot


class _Connection:
    def __init__(self, rows):
        self.rows = rows

    def execute(self, _query, _params):
        return self

    def fetchall(self):
        return self.rows

    def close(self):
        pass


class ApprovedSnapshotResolverTests(unittest.TestCase):
    def test_new_approval_has_new_snapshot_identity_for_same_material(self):
        connection = MagicMock()
        connection.execute.return_value.fetchone.return_value = {
            "allocation_class": "system_level", "owning_target": "SRS",
            "lineage_mode": "normal_hierarchical", "source_origin_req_ids": "SOURCE-1",
            "hierarchy_parent_req_ids": "",
        }
        profiles = {"vocabulary": {"content_fingerprint": "vocabulary-hash", "revision_number": "1"}}
        with patch("snapshot_manager.connect", return_value=connection), \
                patch("snapshot_manager.resolve_approved_profiles", return_value=profiles), \
                patch("snapshot_manager.record_event"), \
                patch("snapshot_manager.datetime") as clock:
            clock.now.return_value.isoformat.return_value = "2026-01-01T00:00:00.000001+00:00"
            options = {"project_id": "P", "canonical_revision_ids": ["revision-current"],
                       "mapping_ids": ["mapping-approved"], "approved_by": "reviewer",
                       "retrieval": {"version": "1", "hash": "retrieval-hash"}, "semantic_enabled": False}
            first = create_approved_snapshot(Path("."), **options)
            clock.now.return_value.isoformat.return_value = "2026-01-01T00:00:00.000002+00:00"
            second = create_approved_snapshot(Path("."), **options)
        self.assertNotEqual(first, second)
        inserts = [call.args for call in connection.execute.call_args_list if "INSERT INTO snapshots" in call.args[0]]
        self.assertEqual(len(inserts), 2)
        self.assertEqual(inserts[0][1][11], inserts[1][1][11])
        self.assertEqual(inserts[0][1][0], first)
        self.assertEqual(inserts[1][1][0], second)

    def _input(self, snapshot_id, mapping):
        return RequirementInput(
            stage="test",
            snapshot_id=snapshot_id,
            corpus_hash="corpus",
            snapshot_hash="snapshot",
            source_path=Path("canonical.sqlite"),
            rows=({"canonical_id": "req-1"},),
            source_links={"req-1": ("SRC-1",)},
            mapping=mapping,
        )

    def test_explicit_incomplete_snapshot_is_rejected(self):
        incomplete = self._input("bad", {})
        with patch("approved_snapshot_resolver.resolve_authoritative_input", return_value=incomplete):
            with self.assertRaisesRegex(ApprovedResolverError, "bad.*approved mapping set is empty"):
                resolve_complete_authoritative_input(Path("."), "test", project_id="P", snapshot_id="bad")

    def test_no_complete_snapshot_is_rejected(self):
        with patch("canonical_store.connect", return_value=_Connection([])):
            with self.assertRaisesRegex(ApprovedResolverError, "No complete approved snapshot"):
                resolve_complete_authoritative_input(Path("."), "test", project_id="P")

    def test_multiple_complete_snapshots_choose_newest_then_id(self):
        candidates = [
            {"snapshot_id": "older", "approved_at": "2026-09-14T10:00:00Z"},
            {"snapshot_id": "newer-b", "approved_at": "2026-09-15T10:00:00Z"},
            {"snapshot_id": "newer-a", "approved_at": "2026-09-15T10:00:00Z"},
        ]
        inputs = {row["snapshot_id"]: self._input(row["snapshot_id"], {"req-1": "block"}) for row in candidates}
        with patch("canonical_store.connect", return_value=_Connection(candidates)):
            with patch("approved_snapshot_resolver.resolve_authoritative_input", side_effect=lambda *args, **kwargs: inputs[kwargs["snapshot_id"]]):
                selected, record = resolve_complete_authoritative_input(Path("."), "test", project_id="P")
        self.assertEqual(selected.snapshot_id, "newer-b")
        self.assertEqual(record["selected_snapshot_id"], "newer-b")
        self.assertEqual(record["selection_mode"], "deterministic_complete_candidate")

    def test_valid_explicit_snapshot_is_preserved(self):
        valid = self._input("explicit-valid", {"req-1": "block"})
        with patch("approved_snapshot_resolver.resolve_authoritative_input", return_value=valid):
            selected, record = resolve_complete_authoritative_input(
                Path("."), "test", project_id="P", snapshot_id="explicit-valid"
            )
        self.assertEqual(selected.snapshot_id, "explicit-valid")
        self.assertEqual(record["selection_mode"], "explicit")
        self.assertEqual(record["selected_snapshot_id"], "explicit-valid")

    def test_incomplete_latest_snapshot_never_falls_back_to_history(self):
        candidates = [{"snapshot_id": "new", "approved_at": "2026-01-02"},
                      {"snapshot_id": "old", "approved_at": "2026-01-01"}]
        with patch("canonical_store.connect", return_value=_Connection(candidates)), \
                patch("approved_snapshot_resolver.resolve_authoritative_input", return_value=self._input("new", {})) as resolve:
            with self.assertRaisesRegex(ApprovedResolverError, "new.*approved mapping set is empty"):
                resolve_complete_authoritative_input(Path("."), "test", project_id="P")
            resolve.assert_called_once_with(Path("."), "test", project_id="P", snapshot_id="new")

    def test_manifest_records_selection_and_rejections(self):
        manifest = {
            "materialized": True,
            "row_count": 1,
            "selection": {
                "selected_snapshot_id": "good",
                "attempted_snapshots": [
                    {"snapshot_id": "bad", "accepted": False, "reason": "mapping set is empty"},
                    {"snapshot_id": "good", "accepted": True, "reason": "complete"},
                ],
            },
        }
        validate_materialization_manifest(manifest, [{"snapshot_id": "good"}])
        self.assertEqual(manifest["selection"]["selected_snapshot_id"], "good")
        self.assertEqual(manifest["selection"]["attempted_snapshots"][0]["reason"], "mapping set is empty")

    def test_stale_manifest_is_rejected(self):
        manifest = {
            "materialized": True,
            "row_count": 1,
            "selection": {
                "selected_snapshot_id": "old",
                "attempted_snapshots": [{"snapshot_id": "old", "accepted": True}],
            },
        }
        with self.assertRaisesRegex(RuntimeError, "do not match"):
            validate_materialization_manifest(manifest, [{"snapshot_id": "new"}])


if __name__ == "__main__":
    unittest.main()
