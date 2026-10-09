import ast
import inspect
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from run_allocation_crosscheck import validate_materialization_manifest
from traceability_hierarchy_coverage import write_hierarchy_coverage_report


ROOT = Path(__file__).resolve().parents[1]


class DownstreamBoundaryBindingTests(unittest.TestCase):
    def test_generation_preflight_checks_inputs_without_resolving_old_outputs(self):
        from validate_downstream_coherence import validate_generation_inputs
        contract = SimpleNamespace(snapshot_id="new-approved", requirement_input=object(), expected={}, selection={})
        for ledger_findings in ([], ["LEDGER_STALE"]):
            with self.subTest(ledger_findings=ledger_findings), \
                    patch("validate_downstream_coherence.resolve_downstream_contract", return_value=contract) as resolve, \
                    patch("validate_downstream_coherence._check_snapshot_and_allocations", return_value=[]), \
                    patch("validate_downstream_coherence._check_ledger", return_value=ledger_findings), \
                    patch("validate_downstream_coherence._check_generator_inference", return_value=[]), \
                    patch("validate_downstream_coherence._check_srs_artifact_coherence", side_effect=AssertionError("old output read")):
                result = validate_generation_inputs(ROOT, "new-approved")
                resolve.assert_called_once_with(ROOT, "new-approved")
                self.assertEqual(result["selected_snapshot_id"], "new-approved")
                self.assertEqual(result["decision"], "BLOCK_DOWNSTREAM" if ledger_findings else "PASS")

    def test_cli_preflight_uses_central_generation_inputs_and_preserves_blocking(self):
        from workflow_cli import _require_downstream_coherence
        for decision in ("PASS", "BLOCK_DOWNSTREAM"):
            with self.subTest(decision=decision), \
                    patch("validate_downstream_coherence.validate_generation_inputs", return_value={"decision": decision, "finding_count": 1}) as validate_inputs, \
                    patch("validate_downstream_coherence.validate", side_effect=AssertionError("full output validation before generation")):
                if decision == "PASS":
                    _require_downstream_coherence(ROOT, "new-approved")
                else:
                    with self.assertRaisesRegex(RuntimeError, "blocked workflow"):
                        _require_downstream_coherence(ROOT, "new-approved")
                validate_inputs.assert_called_once_with(ROOT, "new-approved")

    def test_generation_preflight_rejects_stale_upstream_with_central_trace_check(self):
        from validate_downstream_coherence import validate_generation_inputs
        contract = SimpleNamespace(snapshot_id="new-approved", requirement_input=object(), expected={}, selection={})
        for trace_findings in ([], ["DRS_TRACE_STALE"]):
            with self.subTest(trace_findings=trace_findings), \
                    patch("validate_downstream_coherence.resolve_downstream_contract", return_value=contract), \
                    patch("validate_downstream_coherence._check_snapshot_and_allocations", return_value=[]), \
                    patch("validate_downstream_coherence._check_ledger", return_value=[]), \
                    patch("validate_downstream_coherence._check_generator_inference", return_value=[]), \
                    patch("validate_downstream_coherence._read_csv", return_value=([], [])), \
                    patch("validate_downstream_coherence._check_trace_artifact", return_value=trace_findings) as trace, \
                    patch.object(Path, "exists", return_value=True):
                result = validate_generation_inputs(ROOT, "new-approved", upstream_stages=("DRS",))
                self.assertEqual(trace.call_args.args[0], "DRS")
                self.assertEqual(trace.call_args.args[4], "new-approved")
                self.assertEqual(result["decision"], "BLOCK_DOWNSTREAM" if trace_findings else "PASS")

    def test_drs_completion_checks_current_drs_without_reading_future_ipos(self):
        from validate_downstream_coherence import validate_generated_drs
        contract = SimpleNamespace(expected={})
        for drs_findings in ([], ["DRS_TRACE_STALE"]):
            with self.subTest(drs_findings=drs_findings), \
                    patch("validate_downstream_coherence.validate_generation_inputs", side_effect=lambda *_: {"findings": []}), \
                    patch("validate_downstream_coherence.resolve_downstream_contract", return_value=contract), \
                    patch("validate_downstream_coherence._check_srs_artifact_coherence", return_value=[]), \
                    patch("validate_downstream_coherence._read_csv", return_value=([], [])), \
                    patch("validate_downstream_coherence._check_trace_artifact", return_value=drs_findings) as trace, \
                    patch("validate_downstream_coherence.validate_drs_document_contract", return_value=[]), \
                    patch("run_drs_gen_spec_agent.validate_drs_descriptive_artifacts", return_value=[]), \
                    patch("validate_downstream_coherence.validate_document_author_fields", return_value=[]), \
                    patch("validate_downstream_coherence._check_ipos_descriptive_policy", side_effect=AssertionError("future IPOS read")), \
                    patch.object(Path, "exists", return_value=True):
                result = validate_generated_drs(ROOT, "new-approved")
                self.assertEqual(trace.call_args.args[0], "DRS")
                self.assertEqual(trace.call_args.args[4], "new-approved")
                self.assertEqual(result["decision"], "BLOCK_DOWNSTREAM" if drs_findings else "PASS")

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
