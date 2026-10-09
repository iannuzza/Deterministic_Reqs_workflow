import unittest
import sys
import tempfile
import csv
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_downstream_coherence import resolve_sysml_materialization_scope, sysml_materialization_findings, _check_sysml_requirement_coverage, downstream_contract_fingerprint
from generate_architecture_sysml import build_block_model, build_model, build_digital_subsystem_model, build_shared_model, sysml_header
from review_architecture_sysml import _review
from workflow_gui import WorkflowGUI
from approved_snapshot_resolver import ApprovedResolverError


class Stage2SysmlRoleTests(unittest.TestCase):
    def test_gui_snapshot_choice_preserves_workflow_default_and_manual_override(self):
        for bound, choice, requested, resolved in (
            (None, "Latest approved", None, "latest"),
            ("from-2b", "Current workflow snapshot", "from-2b", "from-2b"),
            ("from-2b", "snap-10 | date | reviewer | approved", "snap-10", "snap-10"),
        ):
            with self.subTest(choice=choice):
                gui = object.__new__(WorkflowGUI)
                gui.root = MagicMock()
                gui._activate_popup = MagicMock()
                gui.workflow_snapshot_id = bound
                connection = MagicMock()
                connection.execute.return_value.fetchall.return_value = [
                    {"snapshot_id": f"snap-{number}", "approved_at": "date", "approved_by": "reviewer", "status": "approved"}
                    for number in range(1, 11)
                ]
                with patch("workflow_gui.connect", return_value=connection), \
                        patch("workflow_gui.resolve_complete_snapshot_id", return_value=resolved) as resolve, \
                        patch("workflow_gui.tk.Toplevel") as dialog, patch("workflow_gui.tk.StringVar") as selected, \
                        patch("workflow_gui.ttk.Frame"), patch("workflow_gui.ttk.Label"), \
                        patch("workflow_gui.ttk.Combobox") as combo, patch("workflow_gui.ttk.Button") as button:
                    selected.return_value.get.return_value = choice

                    def confirm():
                        command = next(call.kwargs["command"] for call in button.call_args_list if call.kwargs.get("text") == "Use Snapshot")
                        command()

                    dialog.return_value.wait_window.side_effect = confirm
                    self.assertEqual(gui._snapshot_selector_args(), ["--snapshot-id", resolved])
                    self.assertIn("LIMIT 10", connection.execute.call_args.args[0])
                    self.assertNotIn("status = 'approved'", connection.execute.call_args.args[0])
                    choices = combo.call_args.kwargs["values"]
                    self.assertEqual(len(choices), 12 if bound else 11)
                    self.assertIn("snap-10 | date | reviewer | approved", choices)
                    selected.assert_called_once_with(value="Current workflow snapshot" if bound else "Latest approved")
                    self.assertEqual(resolve.call_args.kwargs["snapshot_id"], requested)
                    self.assertEqual(gui.workflow_snapshot_id, resolved)

    def test_snapshot_selector_shows_impacted_history_without_authorizing_generation(self):
        gui = object.__new__(WorkflowGUI)
        gui.root = MagicMock()
        gui._activate_popup = MagicMock()
        gui.workflow_snapshot_id = "current-approved"
        connection = MagicMock()
        connection.execute.return_value.fetchall.return_value = [
            {"snapshot_id": "older", "approved_at": "date", "approved_by": "reviewer", "status": "impacted"},
        ]
        label = "older | date | reviewer | impacted (history only)"
        with patch("workflow_gui.connect", return_value=connection), \
                patch("workflow_gui.resolve_complete_snapshot_id", side_effect=ApprovedResolverError("impacted snapshot rejected")) as resolve, \
                patch("workflow_gui.tk.Toplevel") as dialog, patch("workflow_gui.tk.StringVar") as selected, \
                patch("workflow_gui.ttk.Frame"), patch("workflow_gui.ttk.Label"), \
                patch("workflow_gui.ttk.Combobox") as combo, patch("workflow_gui.ttk.Button") as button, \
                patch("workflow_gui.messagebox.showerror") as error:
            selected.return_value.get.return_value = label
            dialog.return_value.wait_window.side_effect = lambda: next(
                call.kwargs["command"] for call in button.call_args_list if call.kwargs.get("text") == "Use Snapshot"
            )()
            self.assertIsNone(gui._snapshot_selector_args())
            self.assertIn(label, combo.call_args.kwargs["values"])
            self.assertEqual(resolve.call_args.kwargs["snapshot_id"], "older")
            error.assert_called_once()
            self.assertEqual(gui.workflow_snapshot_id, "current-approved")

    def test_viewer_keeps_2b_binding_and_refreshes_for_next_approval(self):
        gui = object.__new__(WorkflowGUI)
        first = MagicMock()
        first.require_valid.return_value = first
        second = MagicMock()
        second.require_valid.return_value = second
        with patch.object(WorkflowGUI, "_latest_approved_snapshot_id", return_value="unrelated-latest") as latest, \
                patch("workflow_gui.resolve_sysml_materialization_scope", side_effect=[first, second]) as resolve:
            gui.workflow_snapshot_id = "from-2b"
            self.assertIs(gui._get_sysml_materialization_scope(), first)
            self.assertIs(gui._get_sysml_materialization_scope(), first)
            gui.workflow_snapshot_id = "next-2b"
            self.assertIs(gui._get_sysml_materialization_scope(), second)
            self.assertEqual([call.args[1] for call in resolve.call_args_list], ["from-2b", "next-2b"])
            latest.assert_not_called()

    def test_successful_freeze_binds_snapshot_and_refreshes_views(self):
        gui = object.__new__(WorkflowGUI)
        gui._refresh_review_context = MagicMock()
        gui._refresh_work_area_and_traceability = MagicMock()
        gui._refresh_traceability_after_generation = MagicMock()
        gui.append_chat = MagicMock()
        on_ready = MagicMock()
        with patch.object(WorkflowGUI, "_latest_approved_snapshot_id", return_value="new-2b"):
            gui._after_snapshot_freeze(on_ready)
        self.assertEqual(gui.workflow_snapshot_id, "new-2b")
        self.assertEqual(gui._refresh_traceability_after_generation.call_args.kwargs["snapshot_id"], "new-2b")
        gui._refresh_traceability_after_generation.call_args.args[0]()
        self.assertEqual(gui._refresh_work_area_and_traceability.call_count, 2)
        on_ready.assert_called_once()

    def test_busy_is_set_before_worker_starts(self):
        gui = object.__new__(WorkflowGUI)
        gui.is_running = False
        with patch("workflow_gui.threading.Thread") as thread, patch("workflow_gui.messagebox.showwarning") as warning:
            gui._run_command_async(["command"], "first")
            self.assertTrue(gui.is_running)
            gui._run_command_async(["command"], "second")
            thread.assert_called_once()
            warning.assert_called_once()

    def test_generic_downstream_launchers_keep_workflow_snapshot(self):
        gui = object.__new__(WorkflowGUI)
        gui.workflow_snapshot_id = "from-2b"
        gui._run_command_async = MagicMock()
        gui._latest_approved_snapshot_id = MagicMock(return_value="unrelated-latest")
        gui.run_stage_script("6")
        self.assertEqual(gui._run_command_async.call_args.args[0][-2:], ["--snapshot-id", "from-2b"])
        gui.run_stage_script_after("4", MagicMock())
        self.assertEqual(gui._run_command_async.call_args.args[0][-2:], ["--snapshot-id", "from-2b"])
        gui._latest_approved_snapshot_id.assert_not_called()

    def test_missing_snapshot_does_not_crash_gui_sysml_scope(self):
        gui = object.__new__(WorkflowGUI)
        error = ApprovedResolverError("No complete approved snapshot is available. Checked: none")
        with patch("workflow_gui.resolve_sysml_materialization_scope", side_effect=error) as resolve:
            self.assertIsNone(gui._get_sysml_materialization_scope())
            self.assertEqual(gui._concrete_sysml_block_paths(), [])
            self.assertFalse(gui._sysml_block_file_is_concrete(Path("historical.sysml")))
            self.assertEqual(gui.sysml_scope_diagnostic, str(error))
            resolve.assert_called_once()

    def test_missing_snapshot_is_not_a_current_sysml_review(self):
        with patch("workflow_gui.resolve_sysml_materialization_scope", side_effect=ApprovedResolverError("No approved snapshot")):
            self.assertFalse(WorkflowGUI._sysml_review_is_current("unavailable-snapshot"))

    def exercise_gui_widgets(self, root, scope):
        window = tk.Tk()
        window.withdraw()
        try:
            gui = object.__new__(WorkflowGUI)
            gui.sysml_materialization_scope = scope
            gui.sysml_scope_diagnostic = ""
            gui.sysml_selected_block = None
            gui.sysml_selected_connection = None
            gui.sysml_tree = ttk.Treeview(window)
            gui.sysml_hierarchy_tree = ttk.Treeview(window)
            gui.sysml_graph_canvas = tk.Canvas(window)
            gui.sysml_file_choice_var = tk.StringVar(window)
            gui.sysml_file_choice = ttk.Combobox(window, textvariable=gui.sysml_file_choice_var)
            gui.sysml_file_var = tk.StringVar(window)
            gui.sysml_viewer = tk.Text(window)
            gui.work_tabs = MagicMock()
            gui.sysml_architecture_tab = MagicMock()
            with patch("workflow_gui.REPO_ROOT", root), patch("workflow_gui.resolve_sysml_materialization_scope", return_value=scope):
                gui._refresh_sysml_architecture()
                self.assertEqual(set(gui.sysml_file_choice_paths.values()), {block.path for block in scope.blocks})
                for block in scope.blocks:
                    gui.sysml_file_choice_var.set(block.path.relative_to(root).as_posix())
                    gui._on_sysml_file_choice()
                    self.assertEqual(gui.sysml_viewer.get("1.0", "end-1c"), block.path.read_text(encoding="utf-8"))
                    parent = next(item for item in gui.sysml_hierarchy_tree.get_children(gui.sysml_hierarchy_tree.get_children()[0])
                                  if gui.sysml_hierarchy_tree.item(item, "text") == block.target)
                    item = next(item for item in gui.sysml_hierarchy_tree.get_children(parent)
                                if gui.sysml_hierarchy_tree.item(item, "text") == block.name)
                    gui.sysml_hierarchy_tree.selection_set(item)
                    gui._on_sysml_hierarchy_select()
                    self.assertEqual(gui.sysml_file_var.get(), block.path.relative_to(root).as_posix())
                    self.assertEqual(gui.sysml_viewer.get("1.0", "end-1c"), block.path.read_text(encoding="utf-8"))
                window.update_idletasks()
        finally:
            window.destroy()

    def test_real_tk_dropdown_tree_and_source_opening(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, scope, _ = self.materialized_fixture(root)
            self.exercise_gui_widgets(root, scope)

    def materialized_fixture(self, root):
        expected = {}
        for target, slug, name, source_id in (
            ("Digital IPOS", "control-engine", "CONTROL Engine", "SOURCE_001"),
            ("Digital IPOS", "packet-router", "Packet Router", "SOURCE_002"),
            ("Analog IPOS", "signal-front-end", "Signal Front End", "req-3"),
        ):
            stage = "stage6_digital_ipos" if target == "Digital IPOS" else "stage7_analog_ipos"
            output = root / "artifacts" / stage
            directory = output / "blocks" / slug
            directory.mkdir(parents=True)
            (directory / "document.md").write_text("Generated block document", encoding="utf-8")
            matrix = output / "ipos_traceability_matrix.csv"
            fields = ["mapped_block", "source_req_id", "snapshot_id", "ipos_req_id", "requirement_statement"]
            exists = matrix.exists()
            with matrix.open("a", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                if not exists:
                    writer.writeheader()
                writer.writerow(dict(zip(fields, (name, source_id, "selected", source_id, "Complete approved behavior."))))
            expected[source_id] = {"approved_block": name, "owning_target": target}
        contract = SimpleNamespace(snapshot_id="selected", expected=expected)
        scope = resolve_sysml_materialization_scope(root, contract=contract).require_valid()
        inventory = {block.name: {"Function": "Perform approved function."} for block in scope.blocks}
        rows = scope.ipos_rows(root)
        model_dir = root / "artifacts/stage2_mirco_arc/sysml"
        (model_dir / "blocks").mkdir(parents=True)
        header = sysml_header(scope.snapshot_id, scope.fingerprint)
        (model_dir / "shared_definitions.sysml").write_text(header + build_shared_model(), encoding="utf-8")
        (model_dir / "DigitalSubsystem.sysml").write_text(header + build_digital_subsystem_model(inventory, [], [], scope=scope), encoding="utf-8")
        scope.system_path.write_text(header + build_model([], inventory, [], scope=scope), encoding="utf-8")
        for block in scope.blocks:
            block.path.write_text(header + build_block_model(block.name, inventory[block.name], [], [], rows[block.name], scope=scope), encoding="utf-8")
        return contract, scope, model_dir

    def test_scope_parity_generation_validation_review_and_gui(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, scope, model_dir = self.materialized_fixture(root)
            self.assertEqual(sysml_materialization_findings(root, scope), [])
            self.assertEqual(_check_sysml_requirement_coverage(root, contract, contract.expected, scope), [])
            with patch("review_architecture_sysml.read_csv", return_value=[]):
                review = _review(scope.system_path, model_dir, root, root, root, root, root, scope=scope)
            self.assertTrue(all(row["status"] == "PASS" for row in review), review)
            gui = object.__new__(WorkflowGUI)
            gui.sysml_materialization_scope = scope
            gui.sysml_scope_diagnostic = ""
            with patch("workflow_gui.REPO_ROOT", root):
                self.assertEqual(set(gui._concrete_sysml_block_paths()), {block.path for block in scope.blocks})
                self.assertTrue(all(gui._sysml_block_file_is_concrete(block.path) for block in scope.blocks))
            for block in scope.blocks:
                self.assertEqual(scope.block_for_node(block.node).path, block.path)
                self.assertEqual(scope.block_for_label(block.name.swapcase()), block)
            self.assertEqual(scope.snapshot_id, contract.snapshot_id)
            self.assertEqual(scope.fingerprint, downstream_contract_fingerprint(contract))

    def test_central_crosscheck_rejects_extra_models_and_unresolved_references(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, scope, model_dir = self.materialized_fixture(root)
            extra = model_dir / "blocks/inventory_only.sysml"
            extra.write_text("package Unsupported {}", encoding="utf-8")
            digital = model_dir / "DigitalSubsystem.sysml"
            original = digital.read_text(encoding="utf-8")
            digital.write_text(original + "\nprivate import UnknownPackage::*;\npart bad : UndefinedBlock;\n", encoding="utf-8")
            findings = _check_sysml_requirement_coverage(root, contract, contract.expected, scope)
            for code in ("SYSML_STALE_IPOS_BLOCK_FILE", "SYSML_UNRESOLVED_IMPORT", "SYSML_UNRESOLVED_PART"):
                self.assertTrue(any(finding.startswith(code) for finding in findings), findings)
            scope.blocks[0].path.unlink()
            self.assertTrue(any("SYSML_CREATED_IPOS_BLOCK_MISSING" in finding for finding in sysml_materialization_findings(root, scope)))

    def test_gui_canvas_callbacks_open_every_scope_model(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, scope, _ = self.materialized_fixture(root)
            gui = object.__new__(WorkflowGUI)
            gui.sysml_materialization_scope = scope
            gui.sysml_scope_diagnostic = ""
            gui.sysml_selected_block = None
            gui.sysml_selected_connection = None
            gui.work_tabs = MagicMock()
            gui.sysml_architecture_tab = MagicMock()
            gui._select_sysml_file = MagicMock()
            gui._show_sysml_block_details = MagicMock()
            for attribute, draw, tag in (
                ("sysml_graph_canvas", gui._draw_sysml_architecture, "sysml_node"),
                ("sysml_hierarchy_window_canvas", gui._draw_sysml_hierarchy_window, "sysml_hierarchy_node"),
            ):
                canvas = MagicMock()
                setattr(gui, attribute, canvas)
                canvas.find_withtag.return_value = (1,)
                with patch("workflow_gui.REPO_ROOT", root):
                    draw()
                    callback = next(call.args[2] for call in canvas.tag_bind.call_args_list
                                    if call.args[:2] == (tag, "<Button-1>"))
                    for block in scope.blocks:
                        canvas.gettags.return_value = (tag, block.node if tag == "sysml_node" else block.path.as_posix())
                        callback(SimpleNamespace())
                        gui._select_sysml_file.assert_called_with(block.path)
                    emitted_tags = [call.kwargs.get("tags", ()) for call in canvas.create_rectangle.call_args_list]
                    for block in scope.blocks:
                        self.assertIn((tag, block.node if tag == "sysml_node" else block.path.as_posix()), emitted_tags)

    def test_resolved_extra_and_duplicate_parts_are_not_hidden(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, scope, _ = self.materialized_fixture(root)
            text = scope.digital_path.read_text(encoding="utf-8")
            block = next(block for block in scope.blocks if block.target == "Digital IPOS")
            scope.digital_path.write_text(text + f"\npart extra : {block.definition};\npart def InventoryOnly {{}}\n", encoding="utf-8")
            findings = sysml_materialization_findings(root, scope)
            self.assertTrue(any(finding.startswith("SYSML_OUT_OF_SCOPE_PART:") for finding in findings), findings)
            self.assertTrue(any(finding.startswith("SYSML_OUT_OF_SCOPE_PART_DEFINITION:") for finding in findings), findings)
            analog = next(block for block in scope.blocks if block.target == "Analog IPOS")
            text = scope.system_path.read_text(encoding="utf-8")
            declaration = f"part {analog.node.rsplit('.', 1)[-1]} : {analog.definition};"
            text = text.replace(declaration, "").replace("part def TopAnalogArchitecture {", "part def TopAnalogArchitecture {\n" + declaration)
            scope.system_path.write_text(text, encoding="utf-8")
            findings = sysml_materialization_findings(root, scope)
            self.assertIn(f"SYSML_BLOCK_PART_MISSING_OR_DUPLICATE: {analog.name}", findings)

    def test_materialization_scope_reports_missing_and_unapproved_documents(self):
        contract = SimpleNamespace(snapshot_id="selected", expected={
            "SOURCE_001": {"owning_target": "Digital IPOS", "approved_block": "Control Engine"},
        })
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch("validate_downstream_coherence.created_ipos_block_directories", return_value={"unknown": root}):
                scope = resolve_sysml_materialization_scope(root, contract=contract)
            self.assertIn("SYSML_SCOPE_IPOS_DOCUMENT_MISSING: Control Engine", scope.findings)
            self.assertTrue(any("OUT_OF_SCOPE_IPOS" in finding for finding in scope.findings))
            self.assertEqual(scope.blocks[0].name, "Control Engine")

    def test_valid_empty_scope_and_ambiguous_manifest_are_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract = SimpleNamespace(snapshot_id="selected", expected={})
            scope = resolve_sysml_materialization_scope(root, contract=contract).require_valid()
            self.assertEqual(scope.blocks, ())
            self.assertEqual(sysml_materialization_findings(root, scope), [])
            scope.system_path.parent.mkdir(parents=True)
            header = sysml_header(scope.snapshot_id, scope.fingerprint)
            scope.shared_path.write_text(header + build_shared_model(), encoding="utf-8")
            scope.digital_path.write_text(header + build_digital_subsystem_model({}, [], [], scope=scope), encoding="utf-8")
            scope.system_path.write_text(header + build_model([], {}, [], scope=scope), encoding="utf-8")
            self.assertEqual(sysml_materialization_findings(root, scope), [])
            self.assertEqual(list((scope.system_path.parent / "blocks").glob("*.sysml")), [])
            for prefix in ("alpha", "beta"):
                (scope.manifest_path.parent / f"{prefix}_architecture_model_manifest.json").write_text("{}", encoding="utf-8")
            ambiguous = resolve_sysml_materialization_scope(root, contract=contract)
            self.assertTrue(any(finding.startswith("SYSML_MANIFEST_ADDRESS_AMBIGUOUS") for finding in ambiguous.findings))

    def test_stage3_gate_treats_stage2_sysml_review_as_non_blocking(self):
        repo_root = Path(__file__).resolve().parents[1]
        gate = (repo_root / "scripts/run_stage3_srs_gate.py").read_text(encoding="utf-8")
        review_section = gate[gate.index("review_path"):gate.index("print(\"Stage 3 SRS full flow")]
        self.assertIn("non-blocking derived-artifact diagnostic", review_section)
        self.assertNotIn("return 2", review_section)

    def test_rules_define_mapping_and_snapshot_as_authority(self):
        repo_root = Path(__file__).resolve().parents[1]
        rules = (repo_root / ".github/copilot-instructions.md").read_text(encoding="utf-8")
        skill = (repo_root / ".github/skills/workflow-stage-gate/SKILL.md").read_text(encoding="utf-8")
        for text in (rules, skill):
            self.assertIn("sole architectural authority", text)
            self.assertIn("Stage 2 SysML is derived", text)


if __name__ == "__main__":
    unittest.main()