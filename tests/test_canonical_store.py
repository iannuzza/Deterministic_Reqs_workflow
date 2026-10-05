import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from canonical_store import (
    SCHEMA_VERSION,
    canonical_db_path,
    connect,
    create_snapshot_id,
    fingerprint,
    resolve_snapshot,
    snapshot_material,
    validate_approval_state,
    validate_lifecycle_transition,
    validate_workflow_state,
)


class CanonicalStoreTests(unittest.TestCase):
    def test_migration_is_idempotent_and_creates_authoritative_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            connection = connect(root)
            connection.close()
            second = connect(root)
            tables = {row[0] for row in second.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
            migrations = [tuple(row) for row in second.execute("SELECT version, name FROM schema_migrations ORDER BY version")]
            second.close()

            self.assertEqual(
                migrations,
                [
                    (1, "initial_workflow_model"),
                    (2, "workflow_transition_history"),
                    (3, "stage2_descriptive_evidence"),
                    (4, "requirement_allocation_lineage"),
                    (SCHEMA_VERSION, "approved_allocation_metadata"),
                ],
            )
            self.assertIn("canonical_requirements", tables)
            self.assertIn("staged_requirements", tables)
            self.assertIn("snapshots", tables)
            self.assertEqual(canonical_db_path(root), root / "data/canonical/canonical_store.sqlite")

    def test_supplementary_conflicts_and_provenance_are_representable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            connection = connect(root)
            connection.executescript(
                """
                INSERT INTO projects(project_id, project_name, created_at) VALUES ('p1', 'Demo', '2026-09-08T00:00:00+00:00');
                INSERT INTO source_specs(source_spec_id, project_id, source_name, source_kind, source_scope, target_scope, applies_to_blocks_json, applies_to_architecture_layer, created_at)
                VALUES ('spec-a', 'p1', 'primary.pdf', 'primary', 'system', 'controller', '[\"Main_Controller\"]', 'digital', '2026-09-08T00:00:00+00:00');
                INSERT INTO source_specs(source_spec_id, project_id, source_name, source_kind, source_scope, target_scope, applies_to_blocks_json, applies_to_architecture_layer, created_at)
                VALUES ('spec-b', 'p1', 'supplement.pdf', 'supplementary', 'block', 'controller', '[\"Main_Controller\"]', 'digital', '2026-09-08T00:00:00+00:00');
                INSERT INTO source_revisions(source_revision_id, source_spec_id, revision_number, revision_date, content_fingerprint, ingestion_timestamp)
                VALUES ('rev-a', 'spec-a', '1.0', '2026-01-01', 'hash-a', '2026-09-08T00:00:00+00:00');
                INSERT INTO source_revisions(source_revision_id, source_spec_id, revision_number, revision_date, content_fingerprint, ingestion_timestamp)
                VALUES ('rev-b', 'spec-b', '2.0', '2026-09-07', 'hash-b', '2026-09-08T00:01:00+00:00');
                INSERT INTO ingestion_batches(ingestion_batch_id, project_id, batch_kind, started_at) VALUES ('ib-1', 'p1', 'supplementary', '2026-09-08T00:00:00+00:00');
                INSERT INTO staging_batches(staging_batch_id, ingestion_batch_id, workflow_state, created_at) VALUES ('sb-1', 'ib-1', 'S2_DETERMINISTIC_CLASSIFICATION', '2026-09-08T00:00:00+00:00');
                """
            )
            rows = [
                ("staged-a", "rev-a", "The controller shall reset.", "approved"),
                ("staged-b", "rev-b", "The controller shall reset and report status.", "approval_required"),
            ]
            for staged_id, revision_id, text, decision in rows:
                connection.execute(
                    """INSERT INTO staged_requirements(
                    staged_id, staging_batch_id, source_revision_id, source_req_id, requirement_text,
                    proposed_classification, classification_reason, classification_method,
                    classification_confidence, review_comment, review_decision, content_fingerprint)
                    VALUES (?, 'sb-1', ?, 'REQ-1', ?, 'functional', 'rule', 'deterministic', 0.9, '', ?, ?)""",
                    (staged_id, revision_id, text, decision, fingerprint({"text": text})),
                )
            connection.commit()
            result = connection.execute("SELECT COUNT(*) FROM staged_requirements WHERE source_req_id = 'REQ-1'").fetchone()[0]
            revisions = connection.execute("SELECT COUNT(*) FROM source_revisions").fetchone()[0]
            connection.close()

            self.assertEqual(result, 2)
            self.assertEqual(revisions, 2)

    def test_snapshot_requires_explicit_selector_and_approved_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            connection = connect(root)
            connection.execute("INSERT INTO projects(project_id, project_name, created_at) VALUES ('p1', 'Demo', 'now')")
            material = snapshot_material(["rev-1"], ["map-1"], {"taxonomy": "tax-hash"}, {"config": "cfg-hash"}, False)
            snapshot_id = create_snapshot_id(material)
            connection.execute(
                "INSERT INTO snapshots(snapshot_id, project_id, snapshot_kind, canonical_revision_set_json, content_fingerprint, created_at) VALUES (?, 'p1', 'mapping', ?, ?, 'now')",
                (snapshot_id, json.dumps(["rev-1"]), fingerprint(material)),
            )
            connection.commit()
            with self.assertRaises(ValueError):
                resolve_snapshot(connection)
            with self.assertRaises(PermissionError):
                resolve_snapshot(connection, snapshot_id=snapshot_id)
            connection.execute("UPDATE snapshots SET status = 'approved', approved_at = '2026-09-08T00:00:00+00:00' WHERE snapshot_id = ?", (snapshot_id,))
            connection.commit()
            self.assertEqual(resolve_snapshot(connection, snapshot_id=snapshot_id)["snapshot_id"], snapshot_id)
            self.assertEqual(resolve_snapshot(connection, use_latest_approved=True)["snapshot_id"], snapshot_id)
            connection.close()

    def test_validation_keeps_lifecycle_and_semantic_approval_separate(self):
        validate_lifecycle_transition("staged", "under_review")
        validate_approval_state("approval_required")
        validate_workflow_state("S2H_APPROVED_MAPPING_SNAPSHOT")
        with self.assertRaises(ValueError):
            validate_lifecycle_transition("approved", "staged")
        with self.assertRaises(ValueError):
            validate_approval_state("not-a-state")


if __name__ == "__main__":
    unittest.main()
