import csv
import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from canonical_store import connect
from impact_analysis import analyze_merge
from merge_engine import merge_staging_batch, register_staged_ingestion
from workflow_states import history, transition


class Step3WorkflowTests(unittest.TestCase):
    def _write_csv(self, path: Path, fields, rows):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def _ingestion(self, root: Path, *, ingestion_id="supplement_001", source_revision="2.0", text="The controller shall report status.", category="new", decision="approved") -> Path:
        ingestion = root / f"artifacts/source_ingestion/{ingestion_id}"
        ingestion.mkdir(parents=True)
        (ingestion / "source_metadata.json").write_text(json.dumps({
            "ingestion_id": ingestion_id,
            "source_spec": "supplement.pdf",
            "source_revision": source_revision,
            "source_scope": "digital",
            "target_scope": "Main_Controller",
        }), encoding="utf-8")
        fields = ["staged_id", "source_req_id", "requirement_statement", "source_page", "source_chunk_id"]
        self._write_csv(ingestion / "normalized_requirements.csv", fields, [{
            "staged_id": f"{ingestion_id}:REQ-1",
            "source_req_id": "REQ-1",
            "requirement_statement": text,
            "source_page": "4",
            "source_chunk_id": "p004:l2",
        }])
        review_fields = fields + ["classification", "review_decision", "match_reason", "reviewer_notes"]
        self._write_csv(ingestion / "comparison_results.csv", review_fields, [{
            "staged_id": f"{ingestion_id}:REQ-1",
            "source_req_id": "REQ-1",
            "requirement_statement": text,
            "source_page": "4",
            "source_chunk_id": "p004:l2",
            "classification": category,
            "review_decision": decision,
            "match_reason": "test",
            "reviewer_notes": "",
        }])
        return ingestion

    def test_transitions_are_persisted_and_loopback_preserves_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transition(root, entity_type="batch", entity_id="b1", target="ingested", actor="test")
            transition(root, entity_type="batch", entity_id="b1", target="parsed", actor="test")
            transition(root, entity_type="batch", entity_id="b1", target="classified", actor="test")
            transition(root, entity_type="batch", entity_id="b1", target="under_review", actor="test")
            transition(root, entity_type="batch", entity_id="b1", target="needs_rework", actor="test", reason="ambiguous classification")
            transition(root, entity_type="batch", entity_id="b1", target="under_review", actor="test", reason="corrected")
            states = [row["to_state"] for row in history(root, entity_type="batch", entity_id="b1")]
            self.assertEqual(states, ["ingested", "parsed", "classified", "under_review", "needs_rework", "under_review"])

    def test_approved_new_requirement_creates_canonical_revision_and_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestion = self._ingestion(root)
            staging_batch = register_staged_ingestion(root, ingestion)
            impact = analyze_merge(root, project_id=root.name, staging_batch_id=staging_batch)
            result = merge_staging_batch(root, project_id=root.name, staging_batch_id=staging_batch, approved_by="reviewer")
            connection = connect(root)
            canonical = connection.execute("SELECT canonical_requirement_id FROM canonical_requirements").fetchone()
            provenance = connection.execute("SELECT source_req_id FROM requirement_provenance").fetchone()
            connection.close()
            self.assertEqual(impact.risk, "safe")
            self.assertEqual(result["regeneration_scope"], "partial")
            self.assertIsNotNone(canonical)
            self.assertEqual(provenance[0], "REQ-1")

    def test_same_id_different_text_is_conflict_and_cannot_merge_without_winner(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = self._ingestion(root, text="The controller shall report status.")
            batch_one = register_staged_ingestion(root, first)
            merge_staging_batch(root, project_id=root.name, staging_batch_id=batch_one, approved_by="reviewer")
            second = self._ingestion(root, ingestion_id="supplement_002", source_revision="3.0", text="The controller shall report status and error.")
            (second / "source_metadata.json").write_text(json.dumps({"ingestion_id": "supplement_002", "source_spec": "supplement.pdf", "source_revision": "3.0", "source_scope": "digital"}), encoding="utf-8")
            batch_two = register_staged_ingestion(root, second)
            connection = connect(root)
            row = connection.execute("SELECT review_decision FROM staged_requirements WHERE staging_batch_id = ?", (batch_two,)).fetchone()
            connection.close()
            self.assertEqual(row[0], "approval_required")
            with self.assertRaises(PermissionError):
                merge_staging_batch(root, project_id=root.name, staging_batch_id=batch_two, approved_by="reviewer")


if __name__ == "__main__":
    unittest.main()
