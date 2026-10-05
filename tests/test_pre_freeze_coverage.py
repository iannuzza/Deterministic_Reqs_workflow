import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from canonical_store import connect
from pre_freeze_coverage import validate_pre_freeze_coverage


class PreFreezeCoverageTests(unittest.TestCase):
    project_id = "STBIO"
    primary_source = "DDS_STBIO1.pdf"
    supplementary_source = "IPOS_MAIN_CTRL.pdf"

    def _write_review(self, root, rows):
        path = root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        fields = ["requirement_id", "review_decision", "supplementary_source_spec"]
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


if __name__ == "__main__":
    unittest.main()
