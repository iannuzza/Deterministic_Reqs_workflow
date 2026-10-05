import csv
import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from canonical_store import connect, fingerprint
from requirement_corpus import (
    CorpusResolutionError,
    load_approved_input,
    load_sqlite_snapshot_input,
    write_approved_snapshot,
)
from generate_ipos_specs import generate


class RequirementCorpusResolverTests(unittest.TestCase):
    def test_ipos_callable_fails_closed_without_explicit_snapshot_or_legacy_opt_in(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                generate(Path(directory), "digital")

    def _write_csv(self, path: Path, rows: list[dict[str, str]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    def test_integrated_corpus_is_the_single_authoritative_view(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            primary = root / "artifacts/stage1_requirements/requirements_summary.csv"
            integrated = root / "artifacts/stage1_requirements/integrated_requirements.csv"
            row = {
                "id": "CAN-00042",
                "source_req_id": "DDS_STBIO1_0013",
                "requirement_statement": "The controller shall support reset.",
                "source": "primary.pdf",
                "requirement_type": "functional",
            }
            self._write_csv(primary, [{**row, "id": "PRIMARY-ONLY"}])
            self._write_csv(integrated, [row])

            resolved = load_approved_input(root, "migration", allow_legacy=True)

            self.assertEqual(resolved.source_path, integrated)
            self.assertEqual(resolved.rows[0]["id"], "CAN-00042")

    def test_all_downstream_stages_receive_the_same_snapshot_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            corpus = root / "artifacts/stage1_requirements/requirements_summary.csv"
            rows = [{
                "canonical_id": "CAN-00042",
                "id": "CAN-00042",
                "source_req_id": "DDS_STBIO1_0013",
                "source_req_ids": "DDS_STBIO1_0013;IPOS_STBIO1_MAIN_CTRL_5015",
                "requirement_statement": "The controller shall support reset.",
                "source": "primary.pdf",
                "requirement_type": "functional",
                "approved_block": "Main_Controller",
            }]
            self._write_csv(corpus, rows)
            write_approved_snapshot(
                root,
                rows,
                snapshot_id="stage2b_test",
                approved_by="tester",
                mapping_preview_hash="mapping-test",
            )

            inputs = [load_approved_input(root, stage) for stage in ("3", "4", "5", "6", "7")]

            self.assertEqual({item.snapshot_id for item in inputs}, {"stage2b_test"})
            self.assertTrue(all(list(item.rows) == rows for item in inputs))
            self.assertEqual(inputs[0].source_links["CAN-00042"], (
                "DDS_STBIO1_0013",
                "IPOS_STBIO1_MAIN_CTRL_5015",
            ))

    def test_snapshot_rejects_live_corpus_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            corpus = root / "artifacts/stage1_requirements/requirements_summary.csv"
            rows = [{
                "id": "CAN-00042",
                "source_req_id": "DDS_STBIO1_0013",
                "requirement_statement": "The controller shall support reset.",
                "source": "primary.pdf",
                "requirement_type": "functional",
            }]
            self._write_csv(corpus, rows)
            write_approved_snapshot(
                root,
                rows,
                snapshot_id="stage2b_test",
                approved_by="tester",
                mapping_preview_hash="mapping-test",
            )
            self._write_csv(corpus, [{**rows[0], "requirement_statement": "The controller shall support reset and status."}])

            with self.assertRaises(CorpusResolutionError):
                load_approved_input(root, "3")

    def test_ipos_generation_preserves_snapshot_and_upstream_traceability(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            corpus = root / "artifacts/stage1_requirements/requirements_summary.csv"
            source_row = {
                "canonical_id": "CAN-00042",
                "id": "CAN-00042",
                "source_req_id": "DDS_STBIO1_0013",
                "requirement_statement": "The controller shall support reset.",
                "source": "primary.pdf",
                "requirement_type": "functional",
            }
            self._write_csv(corpus, [source_row])
            write_approved_snapshot(
                root,
                [source_row],
                snapshot_id="stage2b_test",
                approved_by="tester",
                mapping_preview_hash="mapping-test",
            )
            self._write_csv(
                root / "artifacts/stage5_drs/drs_traceability_matrix.csv",
                [{
                    "drs_req_id": "DRS-REQ-001",
                    "source_req_id": "DDS_STBIO1_0013",
                    "requirement_statement": "The controller shall support reset.",
                    "owning_block": "Main_Controller",
                }],
            )

            trace_path = generate(root, "digital", legacy=True)

            with trace_path.open("r", encoding="utf-8", newline="") as handle:
                result = next(csv.DictReader(handle))
            self.assertEqual(result["ipos_req_id"], "IPOS-DIG-REQ-001")
            self.assertEqual(result["covers_upstream_req_id"], "DRS-REQ-001")
            self.assertEqual(result["canonical_id"], "CAN-00042")
            self.assertEqual(result["mapped_block"], "Main_Controller")
            self.assertEqual(result["snapshot_id"], "stage2b_test")

    def test_sqlite_snapshot_adapter_requires_selector_and_preserves_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            connection = connect(root)
            connection.executescript(
                """
                INSERT INTO projects(project_id, project_name, created_at) VALUES ('p1', 'Demo', 'now');
                INSERT INTO canonical_requirements(canonical_requirement_id, project_id, source_req_id, current_revision_id, created_at, updated_at)
                VALUES ('CAN-1', 'p1', 'REQ-1', 'REV-1', 'now', 'now');
                INSERT INTO canonical_requirement_revisions(revision_id, canonical_requirement_id, revision_number, requirement_text, content_fingerprint, approved_classification, created_at)
                VALUES ('REV-1', 'CAN-1', 1, 'The controller shall reset.', 'text-hash', 'functional', 'now');
                INSERT INTO source_specs(source_spec_id, project_id, source_name, source_kind, created_at)
                VALUES ('SPEC-1', 'p1', 'primary.pdf', 'primary', 'now');
                INSERT INTO source_revisions(source_revision_id, source_spec_id, revision_number, content_fingerprint, ingestion_timestamp)
                VALUES ('SREV-1', 'SPEC-1', '1', 'source-hash', 'now');
                INSERT INTO requirement_provenance(revision_id, source_spec_id, source_revision_id, source_req_id)
                VALUES ('REV-1', 'SPEC-1', 'SREV-1', 'REQ-1');
                """
            )
            material = {"canonical_revision_ids": ["REV-1"]}
            connection.execute(
                "INSERT INTO snapshots(snapshot_id, project_id, snapshot_kind, status, canonical_revision_set_json, content_fingerprint, approved_at, created_at) VALUES ('snap-1', 'p1', 'mapping', 'approved', '[\"REV-1\"]', ?, '2026-09-08', '2026-09-08')",
                (fingerprint(material),),
            )
            connection.commit()
            connection.close()

            resolved = load_sqlite_snapshot_input(root, "3", snapshot_id="snap-1")
            self.assertEqual(resolved.source_path, root / "data/canonical/canonical_store.sqlite")
            self.assertEqual(resolved.rows[0]["requirement_statement"], "The controller shall reset.")
            self.assertEqual(resolved.source_links["CAN-1"], ("REQ-1",))


if __name__ == "__main__":
    unittest.main()
