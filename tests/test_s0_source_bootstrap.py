import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from canonical_store import connect
from s0_source_bootstrap import approve_candidate, assess_source, persist_candidate


class S0SourceBootstrapTests(unittest.TestCase):
    def _context(self):
        return {"requirement_id_rules": {"table_req_id_patterns": [r"DDS_STBIO1_\d+"]}}

    def test_tagged_source_proposes_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.html"
            source.write_text("<p>[DDS_STBIO1_0001] Requirement: The block shall reset.</p>", encoding="utf-8")
            result = assess_source(source, self._context())
            self.assertEqual(result.status, "tagged")
            self.assertEqual(result.proposed_prefix, "DDS_STBIO1")
            self.assertEqual(result.tagged_count, 1)

    def test_table_header_variants_are_detected_without_auto_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.html"
            source.write_text("<table><tr><th>Requirement ID</th><th>Text</th></tr><tr><td>DDS_STBIO1_0002</td><td>The block shall start.</td></tr></table>", encoding="utf-8")
            result = assess_source(source, self._context())
            self.assertEqual(result.status, "ambiguous")
            self.assertEqual(result.proposed_prefix, "DDS_STBIO1")
            self.assertEqual(result.table_id_count, 1)
            self.assertTrue(result.evidence)

    def test_candidate_is_persisted_pending(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.html"
            source.write_text("No requirement IDs are present.", encoding="utf-8")
            assessment = assess_source(source, self._context())
            profile_id = persist_candidate(root, project_id="p1", assessment=assessment, actor="tester")
            connection = connect(root)
            row = connection.execute("SELECT lifecycle_state, approval_state, profile_payload_json FROM profile_revisions WHERE profile_revision_id = ?", (profile_id,)).fetchone()
            events = connection.execute("SELECT event_type FROM audit_events WHERE entity_id = ?", (profile_id,)).fetchall()
            connection.close()
            self.assertEqual(tuple(row[:2]), ("staged", "pending"))
            self.assertEqual(json.loads(row[2])["status"], "untagged")
            self.assertEqual(events[0][0], "source_imported")

    def test_candidate_requires_explicit_approval_before_becoming_authoritative(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.html"
            source.write_text("[DDS_STBIO1_0001] Requirement: The block shall reset.", encoding="utf-8")
            profile_id = persist_candidate(root, project_id="p1", assessment=assess_source(source, self._context()), actor="tester")
            connection = connect(root)
            self.assertEqual(tuple(connection.execute("SELECT lifecycle_state, approval_state FROM profile_revisions WHERE profile_revision_id = ?", (profile_id,)).fetchone()), ("staged", "pending"))
            connection.close()
            approve_candidate(root, profile_id=profile_id, actor="reviewer", approved_prefix="DDS_STBIO1")
            connection = connect(root)
            self.assertEqual(tuple(connection.execute("SELECT lifecycle_state, approval_state FROM profile_revisions WHERE profile_revision_id = ?", (profile_id,)).fetchone()), ("approved", "approved"))
            self.assertEqual(connection.execute("SELECT event_type FROM audit_events WHERE entity_id = ? ORDER BY event_id DESC LIMIT 1", (profile_id,)).fetchone()[0], "review_approved")
            connection.close()


if __name__ == "__main__":
    unittest.main()
