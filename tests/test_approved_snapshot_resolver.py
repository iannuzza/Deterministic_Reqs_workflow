import unittest
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from approved_snapshot_resolver import ApprovedResolverError, resolve_complete_authoritative_input
from run_allocation_crosscheck import validate_materialization_manifest
from requirement_corpus import RequirementInput


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
