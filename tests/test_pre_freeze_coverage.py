import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from canonical_store import connect
from pre_freeze_coverage import validate_pre_freeze_coverage
import validate_source_to_stage2b_coherence as source_coherence


class PreFreezeCoverageTests(unittest.TestCase):
    project_id = "STBIO"
    primary_source = "DDS_STBIO1.pdf"
    supplementary_source = "IPOS_MAIN_CTRL.pdf"

    def _write_review(self, root, rows):
        path = root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        fields = ["requirement_id", "review_decision", "supplementary_source_spec", "supplementary_staged_id"]
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def _write_context(self, root, exclusions=None):
        path = root / "config/project_context.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "project_name": self.project_id,
            "source_spec_path": "specs/" + self.primary_source,
            "pre_freeze_approved_exclusions": exclusions or [],
        }), encoding="utf-8")

    def _add_source(self, connection, source_name, source_kind, source_id):
        connection.execute(
            """INSERT INTO source_specs(
                source_spec_id, project_id, source_name, source_kind, created_at)
                VALUES (?, ?, ?, ?, ?)""",
            (source_id, self.project_id, source_name, source_kind, "2026-01-01T00:00:00+00:00"),
        )
        connection.execute(
            """INSERT INTO source_revisions(
                source_revision_id, source_spec_id, revision_number, content_fingerprint, ingestion_timestamp)
                VALUES (?, ?, '1', ?, ?)""",
            ("rev-" + source_id, source_id, "hash-" + source_id, "2026-01-01T00:00:00+00:00"),
        )

    def _add_canonical_requirement(self, connection, source_name, source_id, requirement_id, merged=True):
        revision_id = "rev-" + source_id
        canonical_id = "canonical-" + requirement_id
        canonical_revision_id = "canonical-revision-" + requirement_id
        connection.execute(
            """INSERT INTO canonical_requirements(
                canonical_requirement_id, project_id, source_req_id, current_revision_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)""",
            (canonical_id, self.project_id, requirement_id, canonical_revision_id, "2026-01-01T00:00:00+00:00", "2026-01-01T00:00:00+00:00"),
        )
        connection.execute(
            """INSERT INTO canonical_requirement_revisions(
                revision_id, canonical_requirement_id, revision_number, requirement_text, content_fingerprint, created_at)
                VALUES (?, ?, 1, ?, ?, ?)""",
            (canonical_revision_id, canonical_id, "The system shall satisfy " + requirement_id, "hash-" + requirement_id, "2026-01-01T00:00:00+00:00"),
        )
        connection.execute(
            """INSERT INTO requirement_provenance(
                revision_id, source_spec_id, source_revision_id, source_req_id)
                VALUES (?, ?, ?, ?)""",
            (canonical_revision_id, source_id, revision_id, requirement_id),
        )
        if merged:
            ingestion_id = "ingestion-" + source_id
            staging_id = "staging-" + source_id
            connection.execute(
                "INSERT INTO ingestion_batches(ingestion_batch_id, project_id, batch_kind, started_at) VALUES (?, ?, 'source', ?)",
                (ingestion_id, self.project_id, "2026-01-01T00:00:00+00:00"),
            )
            connection.execute(
                "INSERT INTO staging_batches(staging_batch_id, ingestion_batch_id, workflow_state, created_at) VALUES (?, ?, 'S2D_NON_DESTRUCTIVE_MERGE', ?)",
                (staging_id, ingestion_id, "2026-01-01T00:00:00+00:00"),
            )
            connection.execute(
                """INSERT INTO source_integration_records(
                    integration_record_id, source_spec_id, source_revision_id, ingestion_batch_id, staging_batch_id, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                ("integration-" + source_id, source_id, revision_id, ingestion_id, staging_id, "2026-01-01T00:00:00+00:00"),
            )
            connection.execute(
                """INSERT INTO merge_operations(
                    merge_operation_id, project_id, staging_batch_id, decision, approved_by, started_at, completed_at)
                    VALUES (?, ?, ?, 'approved', 'test', ?, ?)""",
                ("merge-" + source_id, self.project_id, staging_id, "2026-01-01T00:00:00+00:00", "2026-01-01T00:01:00+00:00"),
            )

    def _setup(self, rows, sources, exclusions=None):
        root = Path(self.directory)
        self._write_context(root, exclusions)
        self._write_review(root, rows)
        connection = connect(root)
        connection.execute(
            "INSERT INTO projects(project_id, project_name, created_at) VALUES (?, ?, ?)",
            (self.project_id, self.project_id, "2026-01-01T00:00:00+00:00"),
        )
        for source_name, source_kind, source_id, requirement_ids, merged in sources:
            self._add_source(connection, source_name, source_kind, source_id)
            for requirement_id in requirement_ids:
                self._add_canonical_requirement(connection, source_name, source_id, requirement_id, merged)
        connection.commit()
        connection.close()
        return root

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.directory = self.temp_directory.name

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_mixed_sources_pass_only_after_both_are_registered_and_merged(self):
        rows = [
            {"requirement_id": "DDS-1", "review_decision": "approved", "supplementary_source_spec": ""},
            {"requirement_id": "IPOS-1", "review_decision": "reassigned", "supplementary_source_spec": self.supplementary_source},
        ]
        root = self._setup(rows, [
            (self.primary_source, "primary", "spec-primary", ["DDS-1"], True),
            (self.supplementary_source, "supplementary", "spec-supplementary", ["IPOS-1"], True),
        ])
        manifest = validate_pre_freeze_coverage(root, project_id=self.project_id)
        self.assertEqual(manifest["status"], "pass")
        self.assertEqual(manifest["canonical_counts_by_source"], {self.primary_source: 1, self.supplementary_source: 1})

    def test_missing_primary_registration_is_rejected(self):
        rows = [{"requirement_id": "DDS-1", "review_decision": "approved", "supplementary_source_spec": ""}]
        root = self._setup(rows, [])
        with self.assertRaisesRegex(RuntimeError, "missing canonical source registration"):
            validate_pre_freeze_coverage(root, project_id=self.project_id)
        manifest = json.loads((root / "artifacts/traceability_reports/pre_freeze_canonical_coverage.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "fail")

    def test_registered_source_without_completed_merge_is_rejected(self):
        rows = [{"requirement_id": "DDS-1", "review_decision": "approved", "supplementary_source_spec": ""}]
        root = self._setup(rows, [(self.primary_source, "primary", "spec-primary", ["DDS-1"], False)])
        with self.assertRaisesRegex(RuntimeError, "missing completed canonical merge"):
            validate_pre_freeze_coverage(root, project_id=self.project_id)

    def test_excluded_approved_requirement_is_reported_and_allowed(self):
        rows = [{"requirement_id": "DDS-1", "review_decision": "approved", "supplementary_source_spec": ""}]
        root = self._setup(rows, [], exclusions=["DDS-1"])
        manifest = validate_pre_freeze_coverage(root, project_id=self.project_id)
        self.assertEqual(manifest["status"], "pass")
        self.assertEqual(manifest["explicit_approved_exclusions"], ["DDS-1"])
        self.assertEqual(manifest["expected_in_scope_source_specs"], [])

    def _assert_pre_freeze_uses_current_source_without_snapshot_reads(self, source_kind, *, merge_approved=True):
        source_name = "current-source.pdf"
        requirement_id = "CURRENT-REQ-1"
        root = self._setup(
            [{"requirement_id": requirement_id, "review_decision": "approved",
                            "supplementary_source_spec": source_name if source_kind == "supplementary" else "",
                            "supplementary_staged_id": "other-approved-source" if source_kind == "primary" else ""}],
            [(source_name if source_kind == "supplementary" else self.primary_source,
              source_kind, "spec-current", [requirement_id], True)],
        )
        active_path = root / "artifacts/source_ingestion/spec-current"
        active_path.mkdir(parents=True)
        metadata = {
            "ingestion_id": "spec-current", "source_kind": source_kind,
            "source_spec": source_name if source_kind == "supplementary" else self.primary_source,
            "source_revision": "1", "source_revision_date": "2026-01-01",
            "staged_at": "2026-01-01T00:00:00+00:00",
        }
        if source_kind == "primary":
            del metadata["source_revision_date"]
            del metadata["staged_at"]
        (active_path / "source_metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
        connection = connect(root)
        connection.execute(
            "INSERT INTO staged_requirements(staged_id, staging_batch_id, source_revision_id, source_req_id, requirement_text, content_fingerprint) VALUES (?, ?, ?, ?, ?, ?)",
            ("staged-current", "staging-spec-current", "rev-spec-current", requirement_id,
             "The system shall satisfy " + requirement_id, "hash-current"),
        )
        if not merge_approved:
            connection.execute("UPDATE merge_operations SET decision = 'pending', completed_at = NULL")
            (active_path / "merge_manifest.json").write_text(json.dumps({"status": "completed"}), encoding="utf-8")
        connection.commit()
        connection.close()
        read_rows = source_coherence._rows
        queries = []

        def current_authority_only(connection, query, parameters=()):
            self.assertNotIn("snapshots", query.casefold())
            queries.append(query)
            return read_rows(connection, query, parameters)

        with patch.object(source_coherence, "_rows", side_effect=current_authority_only):
            report = source_coherence.validate(root)
        self.assertTrue(any("canonical_requirements" in query for query in queries))
        self.assertTrue(any("merge_operations" in query for query in queries))
        self.assertFalse(any(finding["category"] == "stage2b" for finding in report["findings"]))
        self.assertFalse(any(finding["category"] in {"revision", "stale_state", "active_batch"} and finding["severity"] == "ERROR" for finding in report["findings"]))
        merge_findings = [finding for finding in report["findings"] if finding["category"] == "merge_readiness"]
        if merge_approved:
            self.assertEqual(merge_findings, [])
            self.assertEqual(validate_pre_freeze_coverage(root, project_id=self.project_id)["status"], "pass")
        else:
            self.assertTrue(any(finding["severity"] == "ERROR" for finding in merge_findings))

    def test_new_primary_pre_freeze_does_not_read_previous_snapshots(self):
        self._assert_pre_freeze_uses_current_source_without_snapshot_reads("primary")

    def test_new_supplementary_pre_freeze_does_not_read_previous_snapshots(self):
        self._assert_pre_freeze_uses_current_source_without_snapshot_reads("supplementary")

    def test_manifest_cannot_approve_an_incomplete_canonical_merge(self):
        self._assert_pre_freeze_uses_current_source_without_snapshot_reads("supplementary", merge_approved=False)

    def test_new_primary_is_not_shadowed_by_old_supplementary_batch(self):
        root = Path(self.directory)
        for batch_id, kind, staged_at in (
            ("old-supplementary", "supplementary", "2026-01-01T00:00:00+00:00"),
            ("new-primary", "primary", "2026-01-02T00:00:00+00:00"),
        ):
            batch = root / "artifacts/source_ingestion" / batch_id
            batch.mkdir(parents=True)
            (batch / "source_metadata.json").write_text(json.dumps({
                "ingestion_id": batch_id, "source_kind": kind, "staged_at": staged_at,
                "source_revision": "1", "source_revision_date": "2026-01-01",
            }), encoding="utf-8")
        active_path, metadata = source_coherence._discover_batches(root, [])
        self.assertEqual(active_path.name, "new-primary")
        self.assertEqual(metadata["source_kind"], "primary")


if __name__ == "__main__":
    unittest.main()
