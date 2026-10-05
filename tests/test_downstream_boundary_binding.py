import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from run_allocation_crosscheck import validate_materialization_manifest
from traceability_hierarchy_coverage import write_hierarchy_coverage_report


ROOT = Path(__file__).resolve().parents[1]


class DownstreamBoundaryBindingTests(unittest.TestCase):
    def _source(self, filename):
        return (ROOT / "scripts" / filename).read_text(encoding="utf-8-sig")

    def _called_names(self, source, filename):
        tree = ast.parse(source, filename=filename)
        return {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }

    def test_validators_reports_and_crosscheck_use_complete_selector(self):
        files = (
            "validate_stage3_srs_gate.py",
            "validate_stage4_ars_gate.py",
            "validate_stage5_drs_gate.py",
            "validate_ipos_gate.py",
            "generate_snapshot_reports.py",
            "report_generation_service.py",
            "run_allocation_crosscheck.py",
        )
        for filename in files:
            source = self._source(filename)
            names = self._called_names(source, filename)
            self.assertIn("resolve_complete_authoritative_input", names, filename)
            self.assertNotIn("resolve_authoritative_input", names, filename)

    def test_gui_uses_selector_and_not_snapshot_discovery(self):
        source = self._source("workflow_gui.py")
        function_source = inspect.getsource(__import__("workflow_gui").build_gui_review_context)
        self.assertIn("resolve_complete_authoritative_input", function_source)
        self.assertIn("read_csv", function_source)
        self.assertNotIn("status IN ('approved', 'impacted')", function_source)
        self.assertNotIn("FROM snapshots", function_source)
        self.assertNotIn("resolve_authoritative_input", source)

    def test_hierarchy_coverage_uses_ledger_selector(self):
        source = inspect.getsource(write_hierarchy_coverage_report)
        self.assertIn("resolve_complete_authoritative_input", source)
        self.assertIn("requirement_allocation_ledger.csv", source)
        self.assertNotIn("requirements_summary.csv", source)

    def test_manifest_requires_selected_snapshot_and_matching_rows(self):
        with self.assertRaisesRegex(RuntimeError, "materialization.*marked complete"):
            validate_materialization_manifest({}, [])
        manifest = {
            "materialized": True,
            "row_count": 1,
            "selection": {
                "selected_snapshot_id": "snap-good",
                "attempted_snapshots": [{"snapshot_id": "snap-good", "accepted": True}],
            },
        }
        with self.assertRaisesRegex(RuntimeError, "do not match"):
            validate_materialization_manifest(manifest, [{"snapshot_id": "snap-other"}])
        with self.assertRaisesRegex(RuntimeError, "zero ledger rows"):
            validate_materialization_manifest(manifest, [])

    def test_crosscheck_actual_targets_are_ledger_based(self):
        source = self._source("run_allocation_crosscheck.py")
        actual_targets = source.split("def _actual_targets", 1)[1].split("def validate_materialization_manifest", 1)[0]
        self.assertIn("actual_downstream_targets", actual_targets)
        self.assertNotIn("MATRICES", actual_targets)


if __name__ == "__main__":
    unittest.main()
