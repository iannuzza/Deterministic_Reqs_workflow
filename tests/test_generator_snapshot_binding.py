import ast
from importlib import import_module
import sys
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from approved_snapshot_resolver import ApprovedResolverError, resolve_complete_authoritative_input
from requirement_corpus import RequirementInput
from workflow_routing import document_version_for_snapshot, document_version_history_markdown, validate_document_author_fields
from docx import Document
from spec_document_contract import drs_document_events, drs_table_inventory


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_FILES = (
    "run_srs_gen_spec_agent.py",
    "run_drs_gen_spec_agent.py",
    "run_ars_gen_spec_agent.py",
    "generate_ipos_specs.py",
)


class GeneratorSnapshotBindingTests(unittest.TestCase):
    def test_retired_drs_shortcut_is_unavailable_in_gui_cli_and_stage_wrapper(self):
        workflow_cli = import_module("workflow_cli")
        run_stage5_drs_gate = import_module("run_stage5_drs_gate")
        run_drs_gen_spec_agent = import_module("run_drs_gen_spec_agent")
        workflow_gui = import_module("workflow_gui")
        self.assertFalse(hasattr(workflow_gui.WorkflowGUI, "run_stage5_after_stage2a"))
        self.assertNotIn("S5 after S2a", (ROOT / "scripts/workflow_gui.py").read_text(encoding="utf-8-sig"))
        with patch("sys.stderr"):
            with self.assertRaises(SystemExit) as rejected:
                workflow_cli.build_parser().parse_args(["drs-after-stage2a"])
            self.assertEqual(rejected.exception.code, 2)
            for module in (run_stage5_drs_gate, run_drs_gen_spec_agent):
                with self.subTest(module=module.__name__), \
                        patch.object(sys, "argv", [module.__name__, "--requirements-only", "--snapshot-id", "approved"]):
                    with self.assertRaises(SystemExit) as rejected:
                        module.main()
                    self.assertEqual(rejected.exception.code, 2)
        generator_source = (ROOT / "scripts/run_drs_gen_spec_agent.py").read_text(encoding="utf-8-sig")
        self.assertNotIn("requirements_only", generator_source)
        for relative_path in (
            "README.md", "docs/cli-quick-card.md", "docs/orchestration-spec.md",
            "docs/workflow-diagram.md", ".github/copilot-instructions.md",
            ".github/skills/workflow-stage-gate/SKILL.md", "local_memory/environment.md",
        ):
            with self.subTest(document=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8-sig")
                self.assertNotIn("drs-after-stage2a", text)
                self.assertNotIn("Stage 2A-to-DRS", text)
                self.assertNotIn("approved forward shortcut", text)
        self.assertNotIn(("s2a", "stage5", "main"), workflow_gui.WORKFLOW_DIAGRAM_EDGES)
        diagram = (ROOT / "docs/workflow-diagram.md").read_text(encoding="utf-8-sig")
        self.assertNotIn("S2A -.->", diagram)
        self.assertIn("Stage 6<br>Digital IPOS", diagram)
        self.assertIn("Stage 7<br>Analog IPOS", diagram)
        self.assertNotIn("Stage 4 skipped", diagram)
        args = workflow_cli.build_parser().parse_args(["run", "--stage", "5", "--snapshot-id", "approved"])
        self.assertEqual(args.stage, "5")

    def test_spec_generator_preflight_checks_inputs_before_writing_outputs(self):
        for filename in GENERATOR_FILES:
            tree = ast.parse((ROOT / "scripts" / filename).read_text(encoding="utf-8-sig"))
            entrypoint = "generate" if filename == "generate_ipos_specs.py" else "main"
            main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == entrypoint)
            calls = sorted(
                (node.lineno, node.func.id)
                for node in ast.walk(main)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in {"resolve_complete_authoritative_input", "validate_generation_inputs", "validate_generated_drs", "validate_downstream_coherence"}
            )
            self.assertEqual([name for _, name in calls[:2]],
                             ["resolve_complete_authoritative_input", "validate_generation_inputs"], filename)
            if filename == "run_drs_gen_spec_agent.py":
                self.assertEqual(calls[-1][1], "validate_generated_drs")

    def test_ipos_stage_wrappers_resolve_latest_once_and_pin_every_command(self):
        import run_stage6_digital_ipos_gate
        import run_stage7_analog_ipos_gate
        for module in (run_stage6_digital_ipos_gate, run_stage7_analog_ipos_gate):
            with self.subTest(module=module.__name__), \
                    patch.object(sys, "argv", [module.__name__, "--use-latest-approved"]), \
                    patch("approved_snapshot_resolver.resolve_complete_snapshot_id", return_value="bound-snapshot") as resolve, \
                    patch.object(run_stage7_analog_ipos_gate, "resolve_complete_snapshot_id", resolve), \
                    patch.object(module.subprocess, "run", return_value=SimpleNamespace(returncode=0)) as run, \
                    patch("builtins.print"):
                self.assertEqual(module.main(), 0)
                resolve.assert_called_once()
                commands = [call.args[0] for call in run.call_args_list]
                for command in (commands[0], commands[-1]):
                    self.assertNotIn("--use-latest-approved", command)
                    selector = command.index("--snapshot-id")
                    self.assertEqual(command[selector + 1], "bound-snapshot")

    def test_ars_wrapper_generates_even_without_analog_category_heuristic(self):
        import run_stage4_ars_gate
        with patch.object(sys, "argv", ["run_stage4_ars_gate", "--snapshot-id", "bound-snapshot"]), \
                patch.object(run_stage4_ars_gate, "resolve_complete_snapshot_id", return_value="bound-snapshot"), \
                patch.object(run_stage4_ars_gate, "_has_analog_requirement_id", side_effect=AssertionError("category heuristic")), \
                patch.object(run_stage4_ars_gate, "_run", return_value=0) as run, \
                patch("builtins.print"):
            self.assertEqual(run_stage4_ars_gate.main(), 0)
            self.assertEqual(run.call_count, 2)
            for call in run.call_args_list:
                self.assertEqual(call.args[2][-2:], ["--snapshot-id", "bound-snapshot"])

    def test_digital_ipos_refresh_does_not_require_future_analog_or_sysml_outputs(self):
        import run_stage6_digital_ipos_gate as wrapper
        with patch.object(sys, "argv", ["run_stage6_digital_ipos_gate", "--snapshot-id", "bound-snapshot", "--regenerate-downstream"]), \
                patch.object(wrapper.subprocess, "run", return_value=SimpleNamespace(returncode=0)), \
                patch.object(wrapper, "validate_generation_inputs", return_value={"decision": "PASS", "finding_count": 0}) as validate, \
                patch("builtins.print"):
            self.assertEqual(wrapper.main(), 0)
            validate.assert_called_once_with(ROOT, "bound-snapshot", upstream_stages=("SRS", "DRS", "Digital IPOS"))

    def test_cli_full_spec_range_pins_snapshot_for_every_runner_and_gate(self):
        import workflow_cli
        args = workflow_cli.build_parser().parse_args([
            "run", "--from-stage", "3", "--to-stage", "7", "--use-latest-approved",
        ])
        with patch.object(workflow_cli, "resolve_complete_snapshot_id", return_value="bound-snapshot") as resolve, \
                patch("validate_downstream_coherence.validate_generation_inputs", return_value={"decision": "PASS"}), \
                patch.object(workflow_cli, "_run_retrieval_tests", return_value=0), \
                patch.object(workflow_cli, "_run_python_cmd", return_value=0) as run, \
                patch.object(workflow_cli, "_log_manifest"), patch("builtins.print"):
            self.assertEqual(workflow_cli.cmd_run(args, ROOT), 0)
            resolve.assert_called_once()
            commands = [call.args[1] for call in run.call_args_list]
            expected = []
            for stage_key in ("3", "4", "5", "6", "7"):
                stage = workflow_cli.STAGES[stage_key]
                expected.extend([
                    [stage.runner, *stage.runner_args, "--snapshot-id", "bound-snapshot"],
                    [stage.validator, *stage.validator_args, "--snapshot-id", "bound-snapshot"],
                ])
            self.assertEqual(commands, expected)

    def test_history_changes_only_for_new_snapshot_and_preserves_prior_rows(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "spec.md"
            previous = []
            previous_snapshot = ""
            for snapshot, run_date, author, expected_version in (
                ("snap-1", "2026-01-01", "First Author", "0.1"),
                ("snap-1", "2026-01-02", "Second Author", "0.1"),
                ("snap-1", "2026-01-02", "Second Author", "0.1"),
                ("snap-2", "2026-01-03", "Third Author", "0.2"),
                ("snap-2", "2026-01-04", "Fourth Author", "0.2"),
                ("snap-3", "2026-01-05", "Fifth Author", "0.3"),
            ):
                with self.subTest(snapshot=snapshot, date=run_date, author=author):
                    version = document_version_for_snapshot(output, snapshot)
                    self.assertEqual(version, expected_version)
                    history = document_version_history_markdown(output, snapshot, version, run_date, f"Snapshot {snapshot} generated", author)
                    output.write_text(f"Snapshot ID: {snapshot}\nAuthor: {author}\n\n#### Table 1. Version history\n" + "\n".join(history), encoding="utf-8")
                    rows = drs_table_inventory(drs_document_events(output))[0]["rows"][1:]
                    if snapshot == previous_snapshot:
                        self.assertEqual(rows, previous)
                    else:
                        self.assertEqual(rows[:-1], previous)
                        self.assertEqual(rows[-1], [version, run_date, f"Snapshot {snapshot} generated", author])
                    document = Document()
                    document.core_properties.author = author
                    document.save(output.with_suffix(".docx"))
                    self.assertEqual(validate_document_author_fields(output), [])
                    previous = rows
                    previous_snapshot = snapshot
            self.assertEqual(len(previous), 3)

    def test_history_rejects_missing_or_duplicate_table(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "spec.md"
            for content in ("# Existing document without history", "\n\n".join(["| Version | Date | Description | Author |\n|---|---|---|---|\n| 0.1 | today | baseline | author |"] * 2)):
                output.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    document_version_history_markdown(output, "snap-1", "0.1", "today", "run", "author")

    def test_document_version_increments_only_when_snapshot_changes(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "spec.md"
            self.assertEqual(document_version_for_snapshot(output, "snap-1"), "0.1")
            output.write_text(
                "Snapshot ID: snap-1\n| Version | Date | Description | Author |\n| 0.1 | today | baseline | test |\n",
                encoding="utf-8",
            )
            self.assertEqual(document_version_for_snapshot(output, "snap-1"), "0.1")
            self.assertEqual(document_version_for_snapshot(output, "snap-2"), "0.2")

    def test_generators_use_only_complete_selector(self):
        for filename in GENERATOR_FILES:
            source = (ROOT / "scripts" / filename).read_text(encoding="utf-8-sig")
            tree = ast.parse(source, filename=filename)
            calls = [
                node.func.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            ]
            self.assertIn("resolve_complete_authoritative_input", calls, filename)
            legacy_calls = [
                node.func.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in {"resolve_authoritative_input", "load_approved_input"}
            ]
            self.assertEqual(legacy_calls, [], filename)

    def test_generators_share_snapshot_history_renderer(self):
        for filename in GENERATOR_FILES:
            tree = ast.parse((ROOT / "scripts" / filename).read_text(encoding="utf-8-sig"), filename=filename)
            calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "document_version_history_markdown"]
            self.assertEqual(len(calls), 1, filename)
            self.assertEqual(len(calls[0].args), 6, filename)

    def test_ipos_snapshot_format_preserves_history_until_snapshot_changes(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "block.md"
            history = document_version_history_markdown(output, "snap-1", "0.1", "2026-01-01", "Snapshot snap-1 baseline", "Original Author")
            output.write_text("- Snapshot: `snap-1`\n\n#### Table 1. Version history\n" + "\n".join(history), encoding="utf-8")
            self.assertEqual(document_version_history_markdown(output, "snap-1", "0.1", "2026-01-02", "rerun", "Another Author"), history)
            self.assertEqual(document_version_for_snapshot(output, "snap-2"), "0.2")
            updated = document_version_history_markdown(output, "snap-2", "0.2", "2026-01-03", "Snapshot snap-2 baseline", "New Author")
            self.assertEqual(updated[:-1], history)
            self.assertIn("0.2 | 2026-01-03", updated[-1])

    def test_incomplete_and_empty_selection_fail_before_generation(self):
        incomplete = RequirementInput(
            stage="test", snapshot_id="incomplete", corpus_hash="c", snapshot_hash="s",
            source_path=Path("canonical.sqlite"), rows=({"canonical_id": "req-1"},),
            source_links={}, mapping={},
        )
        with patch("approved_snapshot_resolver.resolve_authoritative_input", return_value=incomplete):
            with self.assertRaisesRegex(ApprovedResolverError, "incomplete.*mapping set is empty"):
                resolve_complete_authoritative_input(Path("."), "test", project_id="P", snapshot_id="incomplete")

        class EmptyConnection:
            def execute(self, _query, _params):
                return self

            def fetchall(self):
                return []

            def close(self):
                pass

        with patch("canonical_store.connect", return_value=EmptyConnection()):
            with self.assertRaisesRegex(ApprovedResolverError, "No complete approved snapshot"):
                resolve_complete_authoritative_input(Path("."), "test", project_id="P")

    def test_selected_snapshot_id_is_propagated_to_ledger(self):
        selected = RequirementInput(
            stage="test", snapshot_id="selected", corpus_hash="c", snapshot_hash="s",
            source_path=Path("canonical.sqlite"), rows=({"canonical_id": "req-1"},),
            source_links={}, mapping={"req-1": "block"},
        )
        with patch("approved_snapshot_resolver.resolve_authoritative_input", return_value=selected):
            resolved, record = resolve_complete_authoritative_input(
                Path("."), "test", project_id="P", snapshot_id="selected"
            )
        self.assertEqual(resolved.snapshot_id, "selected")
        self.assertEqual(record["selected_snapshot_id"], "selected")


if __name__ == "__main__":
    unittest.main()