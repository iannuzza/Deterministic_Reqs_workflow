import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from canonical_store import connect
from run_srs_crosscheck_agent import _validate_srs_allocation_scope
from run_srs_gen_spec_agent import (
    Requirement,
    _block_navigation_target,
    _build_heading_registry,
    _deduplicate_authored_requirement_blocks,
    _is_srs_allocated,
    _read_snapshot_srs_allocations,
    _rewrite_internal_links,
    _terminate_authored_requirement_blocks,
)
from allocation_ledger import build_source_ledger


class SrsIntegrityPolicyTests(unittest.TestCase):
    def _allocation_db(self, root, rows):
        connection = connect(root)
        connection.execute(
            "INSERT INTO projects(project_id, project_name, created_at) VALUES ('P', 'P', '2026-01-01T00:00:00+00:00')"
        )
        for req_id, target in rows:
            connection.execute(
                """INSERT INTO requirement_allocations(
                    allocation_id, project_id, req_id, source_type, spec_level,
                    owning_target, requirement_class, lineage_mode, coverage_status,
                    snapshot_id, created_at)
                    VALUES (?, 'P', ?, 'primary', ?, ?, 'system_level',
                            'normal_hierarchical', 'covered', 'snap-1', ?)""",
                ("allocation-" + req_id, req_id, target, target, "2026-01-01T00:00:00+00:00"),
            )
        connection.commit()
        connection.close()

    def test_srs_placement_uses_allocation_target_not_source_id_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._allocation_db(root, [("DDS_STBIO1_0013", "SRS"), ("IPOS_MAIN_CTRL_0001", "DRS")])
            allocations = _read_snapshot_srs_allocations(
                root,
                project_id="P",
                snapshot_id="snap-1",
                requirement_ids={"DDS_STBIO1_0013", "IPOS_MAIN_CTRL_0001"},
            )
            primary = Requirement("DDS_STBIO1_0013", "SYS", "shall", "", "", "")
            supplementary = Requirement("IPOS_MAIN_CTRL_0001", "DIG", "shall", "", "", "")
            self.assertTrue(_is_srs_allocated(primary, allocations))
            self.assertFalse(_is_srs_allocated(supplementary, allocations))

    def test_missing_allocation_rows_fail_explicitly(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._allocation_db(root, [("REQ-1", "SRS")])
            with self.assertRaisesRegex(RuntimeError, "do not match selected snapshot"):
                _read_snapshot_srs_allocations(
                    root,
                    project_id="P",
                    snapshot_id="snap-1",
                    requirement_ids={"REQ-1", "REQ-2"},
                )

    def test_zero_allocation_rows_fail_explicitly(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            connect(root).close()
            with self.assertRaisesRegex(RuntimeError, "non-empty allocation rows"):
                _read_snapshot_srs_allocations(
                    root,
                    project_id="P",
                    snapshot_id="snap-1",
                    requirement_ids={"REQ-1"},
                )

    def test_duplicate_authored_blocks_are_removed_but_distinct_ids_remain(self):
        lines = [
            "**[SRS-REQ-001] Requirement:**",
            "First.",
            "**[SRS-REQ-002] Requirement:**",
            "Second.",
            "**[SRS-REQ-001] Requirement:**",
            "Duplicate.",
        ]
        result = _deduplicate_authored_requirement_blocks(lines)
        self.assertEqual(result.count("**[SRS-REQ-001] Requirement:**"), 1)
        self.assertEqual(result.count("**[SRS-REQ-002] Requirement:**"), 1)
        self.assertNotIn("Duplicate.", result)

    def test_duplicate_blocks_are_removed_after_authored_normalization(self):
        normalized = _terminate_authored_requirement_blocks([
            "[SRS-REQ-001] Requirement:",
            "First.",
            "[SRS-REQ-001] Requirement:",
            "Duplicate.",
        ])
        result = _deduplicate_authored_requirement_blocks(normalized)
        self.assertEqual(result.count("**[SRS-REQ-001] Requirement:**"), 1)
        self.assertNotIn("Duplicate.", result)

    def test_duplicate_heading_titles_resolve_to_final_registry_anchor(self):
        registry = _build_heading_registry([
            "## First {#same}",
            "## Second {#same}",
        ])
        rewritten, resolved, non_links = _rewrite_internal_links(
            ["[first](#same)", "[missing](#does-not-exist)"], registry
        )
        self.assertEqual(registry[0][2], "same")
        self.assertEqual(registry[1][2], "same-1")
        self.assertEqual(rewritten[0], "[first](#same)")
        self.assertEqual(rewritten[1], "N/A")
        self.assertEqual((resolved, non_links), (1, 1))

    def test_final_registry_rewrite_removes_links_to_missing_rendered_headings(self):
        registry = _build_heading_registry(["## Rendered heading {#rendered-heading}"])
        rewritten, resolved, non_links = _rewrite_internal_links(
            ["[Rendered](#rendered-heading)", "[Not emitted](#not-emitted)"], registry
        )
        self.assertEqual(rewritten, ["[Rendered](#rendered-heading)", "N/A"])
        self.assertEqual((resolved, non_links), (1, 1))

    def test_disabled_block_navigation_is_plain_text(self):
        self.assertEqual(_block_navigation_target("91-sensor-hub", False), "N/A")
        self.assertEqual(_block_navigation_target("91-sensor-hub", True), "[Jump](#91-sensor-hub)")

    def test_stage3_partition_requires_srs_rows_once_but_allows_downstream_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._allocation_db(root, [("REQ-S", "SRS"), ("REQ-D", "DRS"), ("REQ-A", "ARS")])
            manifest_path = root / "artifacts/traceability_reports/requirement_allocation_materialization.json"
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(json.dumps({"snapshot_id": "snap-1", "row_count": 3}), encoding="utf-8")
            findings = _validate_srs_allocation_scope(
                root,
                project_id="P",
                snapshot_id="snap-1",
                snapshot_ids={"REQ-S", "REQ-D", "REQ-A"},
                trace_source_ids=["REQ-S"],
            )
            self.assertEqual(findings, [])

    def test_stage3_partition_reports_missing_srs_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._allocation_db(root, [("REQ-S", "SRS")])
            manifest_path = root / "artifacts/traceability_reports/requirement_allocation_materialization.json"
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(json.dumps({"snapshot_id": "snap-1", "row_count": 1}), encoding="utf-8")
            findings = _validate_srs_allocation_scope(
                root,
                project_id="P",
                snapshot_id="snap-1",
                snapshot_ids={"REQ-S"},
                trace_source_ids=[],
            )
            self.assertTrue(any("exactly once" in finding for finding in findings))

    def test_ledger_maps_canonical_snapshot_ids_to_source_ids(self):
        rows = build_source_ledger(
            [{
                "canonical_id": "can-1",
                "source_req_id": "DDS_STBIO1_0013",
                "requirement_statement": "The ADSP shall write the register.",
                "approved_classification": "Digital",
            }],
            [{"Requirement ID": "DDS_STBIO1_0013", "approved_block": "ADSP"}],
            snapshot_id="snap-1",
            allocation_rows=[{
                "source_req_id": "DDS_STBIO1_0013",
                "allocation_class": "block_local_digital",
                "owning_target": "Digital IPOS",
                "lineage_mode": "normal_hierarchical",
                "source_origin_req_ids": "DDS_STBIO1_0013",
            }],
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["owning_block"], "ADSP")
        self.assertEqual(rows[0]["owning_target"], "Digital IPOS")

    def test_block_owner_does_not_override_authoritative_srs_or_drs_target(self):
        source = [{
            "source_req_id": "REQ-S",
            "requirement_statement": "The system shall coordinate blocks.",
            "approved_classification": "System",
        }]
        mapping = [{"Requirement ID": "REQ-S", "approved_block": "Main Controller"}]
        for allocation_class, target in (("system_level", "SRS"), ("top_digital_architecture", "DRS")):
            rows = build_source_ledger(
                source,
                mapping,
                snapshot_id="snap-1",
                allocation_rows=[{
                    "source_req_id": "REQ-S",
                    "allocation_class": allocation_class,
                    "owning_target": target,
                    "lineage_mode": "normal_hierarchical",
                    "source_origin_req_ids": "REQ-S",
                }],
            )
            self.assertEqual(rows[0]["owning_target"], target)
            self.assertEqual(rows[0]["owning_block"], "Main Controller")

    def test_missing_authoritative_allocation_metadata_fails(self):
        with self.assertRaisesRegex(ValueError, "authoritative allocation metadata"):
            build_source_ledger(
                [{"source_req_id": "REQ-1", "requirement_statement": "shall", "approved_classification": "Digital"}],
                [{"Requirement ID": "REQ-1", "approved_block": "ADSP"}],
                snapshot_id="snap-1",
                allocation_rows=[],
            )


if __name__ == "__main__":
    unittest.main()
