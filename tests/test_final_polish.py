import sys
import inspect
import io
import tempfile
import tkinter as tk
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tkinter import ttk
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from openpyxl import Workbook, load_workbook

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from report_generation_service import _ordered_fields, _style_data_sheet
from sysml_generation_service import SysMLCompletenessError, validate_snapshot_requirement_coverage
from workflow_gui import (
    SINGLE_STAGE_LABELS,
    SINGLE_STAGE_LABEL_TO_KEY,
    RANGE_STAGE_LABELS,
    RANGE_STAGE_LABEL_TO_KEY,
    WorkflowGUI,
    WorkflowDiagramRenderer,
    WORKFLOW_NODE_MEANINGS,
    format_gui_review_context,
    build_gui_review_context,
    WORKFLOW_DIAGRAM_NODES,
    WORKFLOW_DIAGRAM_EDGES,
    compact_workflow_scrollregion,
    compact_workflow_node_y,
    responsive_layout_scale,
    scale_window_geometry,
)
from workflow_cli import STAGE_ORDER, build_parser, cmd_validate
from generate_stage2_specs import (
    _cascade_previous_concrete_owners,
    _ensure_previous_concrete_owner_defs,
    _is_generic_source_paragraph,
    _preview_blocks_for_requirement,
    _read_previous_blocks_by_requirement,
    _read_profile_source_section_aliases,
    _read_source_matrix_edges,
    _write_mapping_preview_markdown,
)
from generate_stage1_requirements import _source_section_owner
from generate_architecture_sysml import is_concrete_block
from run_stage2_micro_arch_and_crosscheck import (
    _ensure_interaction_blocks,
    _entity_kind,
    _is_concrete_block,
    _link_interaction_requirements_to_blocks,
    _map_blocks,
    _explicit_target_block,
)
from run_stage6_digital_ipos_gate import _run_activity
from generate_ipos_specs import _convert_ipos_markdown_to_docx


class FinalPolishTests(unittest.TestCase):
    def test_open_validation_report_uses_read_only_viewer_without_file_association(self):
        root = tk.Tk()
        root.withdraw()
        try:
            gui = object.__new__(WorkflowGUI)
            gui.root = root
            gui._set_responsive_geometry = MagicMock()
            result = {"selected_snapshot_id": "snapshot-test", "findings": ["SRS_STALE_CONTRACT_FINGERPRINT"]}

            def descendants(widget):
                for child in widget.winfo_children():
                    yield child
                    yield from descendants(child)

            with tempfile.TemporaryDirectory() as temporary_dir:
                repo_root = Path(temporary_dir)
                report_path = repo_root / "artifacts/validation/downstream_coherence_report.json"
                with patch("workflow_gui.REPO_ROOT", repo_root), \
                        patch("workflow_gui.DOWNSTREAM_VALIDATION_REPORT_PATH", report_path), \
                        patch("validate_downstream_coherence.validate", return_value=result), \
                        patch("workflow_gui.os.startfile", create=True) as startfile, \
                        patch("workflow_gui.messagebox.showerror") as showerror:
                    gui._show_downstream_block_dialog([], ["python", "workflow_cli.py", "run", "--stage", "3"])
                    dialog = next(child for child in root.winfo_children() if isinstance(child, tk.Toplevel))
                    diagnostic_viewer = next(child for child in descendants(dialog) if isinstance(child, tk.Text))
                    diagnostic_text = diagnostic_viewer.get("1.0", "end-1c")
                    self.assertIn("snapshot-test", diagnostic_text)
                    self.assertIn("SRS_STALE_CONTRACT_FINGERPRINT", diagnostic_text)
                    self.assertIn("python workflow_cli.py run --stage 3", diagnostic_text)
                    self.assertEqual(diagnostic_viewer.cget("state"), tk.DISABLED)
                    self.assertTrue(diagnostic_viewer.bind("<Control-c>"))
                    self.assertTrue(diagnostic_viewer.bind("<Button-3>"))
                    diagnostic_viewer.tag_add(tk.SEL, "1.0", "end-1c")
                    gui._copy_text_selection(diagnostic_viewer)
                    self.assertEqual(root.clipboard_get(), diagnostic_text)
                    diagnostic_viewer.insert("1.0", "unwanted edit")
                    self.assertEqual(diagnostic_viewer.get("1.0", "end-1c"), diagnostic_text)
                    open_button = next(child for child in descendants(dialog) if isinstance(child, ttk.Button) and child.cget("text") == "Open validation report")
                    open_button.invoke()
                    report_dialog = next(child for child in dialog.winfo_children() if isinstance(child, tk.Toplevel))
                    viewer = next(child for child in descendants(report_dialog) if isinstance(child, tk.Text))
                    self.assertEqual(viewer.get("1.0", "end-1c"), report_path.read_text(encoding="utf-8"))
                    self.assertEqual(viewer.cget("state"), tk.DISABLED)
                    self.assertTrue(viewer.bind("<Control-c>"))
                    self.assertTrue(viewer.bind("<Button-3>"))
                    viewer.tag_add(tk.SEL, "1.0", "end-1c")
                    gui._copy_text_selection(viewer)
                    self.assertEqual(root.clipboard_get(), viewer.get("1.0", "end-1c"))
                    self.assertEqual(root.grab_current(), report_dialog)
                    viewer.insert("1.0", "unwanted edit")
                    self.assertNotIn("unwanted edit", viewer.get("1.0", "end-1c"))
                    close_button = next(child for child in descendants(report_dialog) if isinstance(child, ttk.Button) and child.cget("text") == "Close")
                    close_button.invoke()
                    self.assertEqual(root.grab_current(), dialog)
                    startfile.assert_not_called()
                    showerror.assert_not_called()
                    report_path.unlink()
                    open_button.invoke()
                    showerror.assert_called_once()
                    self.assertFalse(any(isinstance(child, tk.Toplevel) for child in dialog.winfo_children()))
        finally:
            root.update_idletasks()
            root.destroy()

    def test_gui_stage_run_tracks_all_executable_stages_and_failure(self):
        stages = ("0", "1", "2", "2a", "3", "4", "5", "6", "7")
        for stage in stages:
            with self.subTest(stage=stage):
                gui = object.__new__(WorkflowGUI)
                gui.is_running = False
                gui.root = MagicMock()
                gui.root.after.side_effect = lambda delay, callback, *args: callback(*args)
                for method in ("_set_status", "clear_stage_failure", "set_active_stage", "append_log", "append_chat", "set_stage_failure"):
                    setattr(gui, method, MagicMock())
                process = MagicMock()
                process.stdout = [
                    f"[2026-10-06 13:00:00] Stage {stage.upper()} run 1/1\n",
                    "Stage 1.4 legacy substep; references Stage 3 and Stage 7\n",
                    f"[2026-10-06 13:00:01] STOP at stage {stage} (exit=1)\n",
                ]
                process.wait.return_value = 1
                with patch("workflow_gui.threading.Thread") as thread, \
                        patch("workflow_gui.subprocess.Popen", return_value=process):
                    thread.side_effect = lambda **kwargs: SimpleNamespace(start=kwargs["target"])
                    gui._run_command_async(["python", "workflow_cli.py", "run"], "Stage range")
                self.assertEqual([call.args[0] for call in gui.set_active_stage.call_args_list], [None, stage, None])
                self.assertEqual([call.args[0] for call in gui.clear_stage_failure.call_args_list], [None, stage])
                gui.set_stage_failure.assert_called_once()
                self.assertEqual(gui.set_stage_failure.call_args.args[0], stage)
                self.assertEqual(gui.set_active_stage.call_args.args, (None,))
                self.assertFalse(gui.is_running)

    def test_gui_stage_range_stays_on_stage_that_fails(self):
        gui = object.__new__(WorkflowGUI)
        gui.is_running = False
        gui.root = MagicMock()
        gui.root.after.side_effect = lambda delay, callback, *args: callback(*args)
        for method in ("_set_status", "clear_stage_failure", "set_active_stage", "append_log", "append_chat", "set_stage_failure"):
            setattr(gui, method, MagicMock())
        process = MagicMock()
        process.stdout = [
            "[2026-10-06 13:00:00] Stage 5 run 1/1\n",
            "[2026-10-06 13:00:01] Stage 6 Digital IPOS run 1/1\n",
            "[2026-10-06 13:00:02] Stage 7 Analog IPOS run 1/1\n",
            "ERROR: Stage 7 failed; Stage 3 artifact missing\n",
            "[2026-10-06 13:00:03] STOP at stage 7 (exit=3)\n",
        ]
        process.wait.return_value = 3
        with patch("workflow_gui.threading.Thread") as thread, \
                patch("workflow_gui.subprocess.Popen", return_value=process) as popen:
            thread.side_effect = lambda **kwargs: SimpleNamespace(start=kwargs["target"])
            gui._run_command_async(["python", "workflow_cli.py", "run"], "Stages 5-7", stage="5")
        self.assertEqual([call.args[0] for call in gui.set_active_stage.call_args_list], ["5", "5", "6", "7", None])
        self.assertEqual(gui.set_stage_failure.call_args.args[0], "7")
        self.assertEqual(popen.call_count, 1)
        self.assertEqual(popen.call_args.kwargs["env"]["PYTHONUNBUFFERED"], "1")

    def test_full_workflow_diagram_retains_failure_after_run_and_redraw(self):
        root = tk.Tk()
        try:
            frame = ttk.Frame(root)
            frame.pack(fill=tk.BOTH, expand=True)
            renderer = WorkflowDiagramRenderer(frame)
            for stage, node_id in (("2", "s2"), ("2a", "s2a"), ("7", "stage7")):
                with self.subTest(stage=stage):
                    renderer.set_stage_failures({})
                    renderer.set_active_stage(stage)
                    rect = renderer.node_items[node_id][0]
                    self.assertEqual(renderer.canvas.itemcget(rect, "fill"), renderer.COLORS["active"]["fill"])
                    renderer.set_stage_failures({stage: "Gate failed"})
                    renderer.set_active_stage(None)
                    renderer.refresh()
                    rect = renderer.node_items[node_id][0]
                    self.assertEqual(renderer.canvas.itemcget(rect, "fill"), renderer.COLORS["failed"]["fill"])
                    renderer.set_stage_failures({})
                    renderer.set_active_stage(stage)
                    self.assertEqual(renderer.canvas.itemcget(rect, "fill"), renderer.COLORS["active"]["fill"])
        finally:
            root.destroy()

    def test_standalone_analog_ipos_sets_diagram_stage(self):
        gui = object.__new__(WorkflowGUI)
        gui._snapshot_selector_args = MagicMock(return_value=["--use-latest-approved"])
        gui._run_command_async = MagicMock()
        gui.run_stage_cli("7")
        self.assertEqual(gui._run_command_async.call_args.kwargs["stage"], "7")

    def test_gui_layout_scales_to_screen_and_preserves_saved_position(self):
        self.assertEqual(responsive_layout_scale(1024, 600), 0.72)
        self.assertEqual(responsive_layout_scale(1440, 900), 1.0)
        self.assertEqual(responsive_layout_scale(3840, 2160), 1.25)
        self.assertEqual(scale_window_geometry("1200x800+40+60", 0.8), "960x640+40+60")
        self.assertEqual(scale_window_geometry("invalid", 1.2), "invalid")

    def test_secondary_window_geometry_is_scaled_and_screen_bounded(self):
        class WindowStub:
            geometry_value = None
            minimum = None

            def winfo_screenwidth(self):
                return 800

            def winfo_screenheight(self):
                return 600

            def geometry(self, value):
                self.geometry_value = value

            def minsize(self, width, height):
                self.minimum = (width, height)

        gui = WorkflowGUI.__new__(WorkflowGUI)
        gui.layout_scale = 1.25
        window = WindowStub()
        gui._set_responsive_geometry(window, 1100, 800, 640, 480)
        self.assertEqual(window.geometry_value, "752x540")
        self.assertEqual(window.minimum, (752, 540))

    def test_stage6_execution_log_marks_activity_and_run_boundaries(self):
        class LogStub:
            def __init__(self):
                self.entries = []

            def insert(self, index, text, tags):
                self.entries.append((index, text, tags))

            def see(self, _index):
                pass

        gui = WorkflowGUI.__new__(WorkflowGUI)
        gui.log = LogStub()
        gui._append_log_ui("[IPOS_ACTIVITY] START | 2026-09-25T10:00:00+02:00 | Generate IPOS block")
        gui._append_log_ui("=== START Stage 6 Digital IPOS | start=2026-09-25T10:00:00+02:00 ===")
        self.assertEqual(gui.log.entries[0][2], ("ipos_activity",))
        self.assertEqual(gui.log.entries[1][2], ("ipos_run_boundary",))

    def test_stage6_runner_emits_timestamped_activity_start_and_end(self):
        output = io.StringIO()
        with redirect_stdout(output):
            result = _run_activity("Validate Digital IPOS gate", lambda: SimpleNamespace(returncode=0))
        self.assertEqual(result.returncode, 0)
        self.assertRegex(output.getvalue(), r"\[IPOS_ACTIVITY\] START \| \d{4}-\d{2}-\d{2}T")
        self.assertRegex(output.getvalue(), r"\[IPOS_ACTIVITY\] END \| \d{4}-\d{2}-\d{2}T")
        self.assertIn("exit=0", output.getvalue())

    def test_ipos_pandoc_error_includes_stderr_and_office_lock_guidance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "digital_ipos_main-controller.docx"
            lock = root / "~$gital_ipos_main-controller.docx"
            lock.write_text("lock", encoding="utf-8")
            result = SimpleNamespace(returncode=1, stdout="", stderr="Permission denied")
            with patch("generate_ipos_specs.subprocess.run", return_value=result):
                with self.assertRaisesRegex(RuntimeError, "Permission denied") as error:
                    _convert_ipos_markdown_to_docx(root / "input.md", root / "template.docx", output, root)
            self.assertIn(str(lock), str(error.exception))
            self.assertIn("remove the stale lock", str(error.exception))

    def test_validate_all_runs_diagram_rendering_crosscheck_after_stage_gates(self):
        args = build_parser().parse_args(["validate", "--all", "--snapshot-id", "snapshot-test"])
        invoked = []

        def run_script(_repo_root, script, _dry_run):
            invoked.append(script)
            return 0

        def run_snapshot_script(_repo_root, command, _dry_run):
            invoked.append(command[0])
            return 0

        with tempfile.TemporaryDirectory() as temp_root:
            with patch("workflow_cli._resolve_workflow_snapshot", return_value="snapshot-test"), \
                    patch("workflow_cli._require_downstream_coherence"), \
                    patch("workflow_cli._log_manifest"), \
                    patch("workflow_cli._run_python", side_effect=run_script), \
                    patch("workflow_cli._run_python_cmd", side_effect=run_snapshot_script):
                result = cmd_validate(args, Path(temp_root))

        self.assertEqual(result, 0)
        self.assertEqual(invoked[-1], "scripts/validate_workflow_diagram_rendering.py")
        self.assertEqual(len(invoked), len(STAGE_ORDER) + 1)

    def test_entity_kind_controls_architecture_hierarchy_membership(self):
        block_defs = {
            "Concrete": {"entity_kind": "concrete_block"},
            "Boundary": {"entity_kind": "interface"},
            "Unassigned": {"entity_kind": "unassigned"},
        }
        self.assertEqual(_entity_kind("Boundary", block_defs), "interface")
        self.assertTrue(_is_concrete_block("Concrete", block_defs))
        self.assertFalse(_is_concrete_block("Boundary", block_defs))
        self.assertFalse(is_concrete_block("Boundary", {"Entity kind": "interface"}))

    def test_interaction_endpoint_does_not_synthesize_a_block(self):
        block_defs = {"Concrete": {"entity_kind": "concrete_block"}, "Unassigned": {"entity_kind": "unassigned"}}
        augmented = _ensure_interaction_blocks(
            block_defs,
            {},
            [{"From block": "ISPU debug", "To block": "Concrete"}],
        )
        self.assertNotIn("ISPU debug", augmented)

    def test_report_fields_put_requirement_and_hierarchy_columns_first(self):
        fields = _ordered_fields([
            {"notes": "n", "block": "ADC", "source_req_id": "REQ-1", "statement": "shall"}
        ])
        self.assertEqual(fields[:3], ["source_req_id", "block", "statement"])

    def test_gui_stage_range_dispatches_one_cli_command(self):
        gui = object.__new__(WorkflowGUI)
        gui._run_command_async = MagicMock()
        gui._snapshot_selector_args = MagicMock(return_value=["--snapshot-id", "approved-test"])
        for start, end in (("0", "2"), ("2a", "5"), ("3", "7"), ("6", "7")):
            with self.subTest(start=start, end=end):
                gui._run_command_async.reset_mock()
                gui._snapshot_selector_args.reset_mock()
                gui.from_stage_var = SimpleNamespace(get=lambda: next(label for label, key in RANGE_STAGE_LABEL_TO_KEY.items() if key == start))
                gui.to_stage_var = SimpleNamespace(get=lambda: next(label for label, key in RANGE_STAGE_LABEL_TO_KEY.items() if key == end))
                gui.run_stage_range_cli()
                gui._run_command_async.assert_called_once()
                command = gui._run_command_async.call_args.args[0]
                self.assertEqual(Path(command[1]).name, "workflow_cli.py")
                args = build_parser().parse_args(command[2:])
                self.assertEqual(args.from_stage, start)
                self.assertEqual(args.to_stage, end)
                if end == "2":
                    gui._snapshot_selector_args.assert_not_called()
                    self.assertIsNone(args.snapshot_id)
                else:
                    gui._snapshot_selector_args.assert_called_once()
                    self.assertEqual(args.snapshot_id, "approved-test")
                self.assertEqual(gui._run_command_async.call_args.kwargs["approval_after_success"], end == "2")

    def test_gui_stage_range_preserves_approval_and_order_guards(self):
        gui = object.__new__(WorkflowGUI)
        gui.root = None
        gui._run_command_async = MagicMock()
        with patch("workflow_gui.messagebox.showinfo") as approval, \
                patch("workflow_gui.messagebox.showwarning") as invalid:
            gui.run_stage_range("0", "7")
            approval.assert_called_once()
            gui.run_stage_range("5", "3")
            invalid.assert_called_once()
        gui._run_command_async.assert_not_called()

    def test_report_sheet_has_filter_freeze_pane_and_table(self):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(["source_req_id", "block", "statement"])
        worksheet.append(["REQ-1", "ADC", "shall sample"])
        _style_data_sheet(worksheet, ["source_req_id", "block", "statement"], 1)
        with io.BytesIO() as buffer:
            workbook.save(buffer)
            buffer.seek(0)
            worksheet = load_workbook(buffer).active
        self.assertEqual(worksheet.freeze_panes, "A2")
        self.assertEqual(len(worksheet.tables), 1)
        table = worksheet.tables["ReportData"]
        self.assertEqual(table.ref, "A1:C2")
        self.assertIsNotNone(table.autoFilter)
        self.assertEqual(table.autoFilter.ref, "A1:C2")

    def test_sysml_hierarchy_source_scrollbar_survives_resize(self):
        root = tk.Tk()
        root.withdraw()
        self.addCleanup(root.destroy)
        gui = object.__new__(WorkflowGUI)
        gui.root = root
        with patch.object(gui, "_set_responsive_geometry"), \
                patch.object(gui, "_bind_button_help"), \
                patch.object(gui, "_bind_copy_support"), \
                patch.object(gui, "_draw_sysml_hierarchy_window"):
            gui._open_sysml_hierarchy_window()
        text = gui.sysml_hierarchy_details
        scrollbar = next(child for child in text.master.winfo_children() if isinstance(child, ttk.Scrollbar))
        port_canvas = gui.sysml_hierarchy_port_canvas
        port_scrollbar = next(child for child in port_canvas.master.winfo_children() if isinstance(child, ttk.Scrollbar))
        port_canvas.configure(scrollregion=(0, 0, 620, 3000))
        text.configure(state=tk.NORMAL)
        text.insert("1.0", "SysML source line\n" * 200)
        text.configure(state=tk.DISABLED)
        details_pane = text.master.master
        self.assertIsInstance(details_pane, ttk.Panedwindow)
        self.assertEqual(str(details_pane.cget("orient")), tk.HORIZONTAL)
        self.assertEqual(len(details_pane.panes()), 2)
        for geometry in ("1100x700", "620x420"):
            with self.subTest(geometry=geometry):
                gui.sysml_hierarchy_window.geometry(geometry)
                root.update()
                details_pane.sashpos(0, int(details_pane.winfo_width() * 0.3))
                root.update()
                self.assertTrue(port_scrollbar.winfo_ismapped())
                self.assertGreater(port_scrollbar.winfo_width(), 1)
                self.assertLessEqual(port_scrollbar.winfo_x() + port_scrollbar.winfo_width(), port_canvas.master.winfo_width())
                initial_port_width = gui.sysml_hierarchy_port_canvas.winfo_width()
                initial_text_width = text.winfo_width()
                details_pane.sashpos(0, int(details_pane.winfo_width() * 0.7))
                root.update()
                self.assertGreater(gui.sysml_hierarchy_port_canvas.winfo_width(), initial_port_width)
                self.assertLess(text.winfo_width(), initial_text_width)
                self.assertTrue(scrollbar.winfo_ismapped())
                self.assertGreater(scrollbar.winfo_width(), 1)
                self.assertGreater(scrollbar.winfo_height(), 1)
                self.assertGreater(text.winfo_width(), 1)
                self.assertLessEqual(scrollbar.winfo_x() + scrollbar.winfo_width(), text.master.winfo_width())
                text.yview_moveto(0)
                root.update()
                self.assertEqual(scrollbar.get()[0], 0)
                root.tk.call(scrollbar.cget("command"), "moveto", 1.0)
                root.update()
                self.assertGreater(text.yview()[0], 0)
                self.assertGreater(scrollbar.get()[0], 0)
                self.assertTrue(port_scrollbar.winfo_ismapped())
                self.assertGreater(port_scrollbar.winfo_width(), 1)
                self.assertGreater(port_scrollbar.winfo_height(), 1)
                self.assertLessEqual(port_scrollbar.winfo_x() + port_scrollbar.winfo_width(), port_canvas.master.winfo_width())
                port_canvas.yview_moveto(0)
                root.update()
                self.assertEqual(port_scrollbar.get()[0], 0)
                root.tk.call(port_scrollbar.cget("command"), "moveto", 1.0)
                root.update()
                self.assertGreater(port_canvas.yview()[0], 0)
                self.assertGreater(port_scrollbar.get()[0], 0)

    def test_gui_context_is_deterministic_without_display(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_gui_review_context(root)
            rendered = format_gui_review_context(context)
            self.assertIn("Snapshot: unavailable", rendered)
            self.assertIn("blocked: no complete approved snapshot/materialization", rendered)
            self.assertIn("Authority scanner: not run", rendered)

    def test_architecture_approval_dialog_stays_open_for_stage2b(self):
        source = inspect.getsource(WorkflowGUI._show_architecture_profile_approval_dialog)
        self.assertIn("1. Open Architecture Map in Excel (orange button): review/change, save, and close the Excel file.", source)
        self.assertIn("2. Enable Gate from Workbook (green button).", source)
        self.assertIn("3. Run Stage 2A.", source)
        self.assertIn("4. After Stage 2A passes, Freeze Stage 2B Snapshot.", source)
        self.assertLess(source.index('text="Freeze Stage 2B Snapshot"'), source.index('text="Run Stage 2A"'))
        stage2a_handler = source.split("def run_stage2a_after_approval", 1)[1].split("def freeze_stage2b_snapshot", 1)[0]
        self.assertIn('self.run_stage_cli("2a")', stage2a_handler)
        self.assertNotIn("close_dialog()", stage2a_handler)
        snapshot_handler = source.split("def freeze_stage2b_snapshot", 1)[1].split("def approve_all_mapping_rows", 1)[0]
        self.assertIn("close_dialog()", snapshot_handler)

    def test_workflow_graph_exposes_bootstrap_snapshot_reports_and_sysml(self):
        labels = " ".join(node["label"] for node in WORKFLOW_DIAGRAM_NODES)
        self.assertIn("Bootstrap", labels)
        self.assertIn("Snapshot", labels)
        self.assertIn("XLSX", labels)
        self.assertIn("SysML", labels)

    def test_new_workflow_nodes_have_hover_descriptions(self):
        for node_id in ("s2b", "s2c", "s2d", "s2e", "reports", "sysml"):
            self.assertTrue(WORKFLOW_NODE_MEANINGS[node_id])

    def test_sysml_attribute_parser_reads_typed_escaped_description(self):
        source = 'attribute description : String = "Full \\"quoted\\" description";'
        self.assertEqual(WorkflowGUI._sysml_attribute_value(source, "description"), 'Full "quoted" description')

    def test_button_help_popups_close_when_pointer_leaves(self):
        bind_source = inspect.getsource(WorkflowGUI._bind_button_help)
        show_source = inspect.getsource(WorkflowGUI._show_hover_help)
        self.assertIn('button.bind("<Enter>"', bind_source)
        self.assertIn('button.bind("<Leave>"', bind_source)
        self.assertIn('self._hide_hover_help()', bind_source)
        self.assertNotIn("after(2200", show_source)
        self.assertIn("self._close_popup()", show_source)
        self.assertIn("self._activate_popup(popup, \"hover\")", show_source)
        self.assertIn("self.help_popup_owner_widget = event.widget", show_source)

    def test_concrete_source_owner_wins_over_generic_paragraph_terms(self):
        block_defs = {"Control Block": {}, "Unassigned": {}}
        row = {
            "source": "Section 1.2 Requirements (under Section 1.1 Control Block), paragraph 001",
            "source_section_owner": "Control Block",
        }
        self.assertFalse(_is_generic_source_paragraph(row, block_defs))
        self.assertEqual(_preview_blocks_for_requirement(row, [], block_defs), ["Control Block"])

    def test_concrete_candidates_win_before_generic_source_context(self):
        block_defs = {"Regmap": {"function": "register map"}, "Unassigned": {}}
        ontology_links = {
            f"REQ-{index}": [
                {
                    "role": "Regmap",
                    "related_role": "",
                    "relation_type": "supports",
                    "function_or_property_evidence": "register address range",
                }
            ]
            for index in range(3000, 3007)
        }
        for index in range(3000, 3007):
            row = {
                "source_req_id": f"REQ-{index}",
                "source": "Section 13.4.1 Register Map (under Section 13.4 Register Map), paragraph 001",
                "requirement_statement": "register address range",
                "category": "Digital",
                "requirement_type": "other",
            }
            self.assertEqual(
                _map_blocks(row, {}, block_defs, {}, ontology_links),
                ["Regmap"],
            )
            self.assertEqual(
                _preview_blocks_for_requirement(row, ["Regmap"], block_defs),
                ["Regmap"],
            )

    def test_configured_source_alias_wins_without_ontology_candidate(self):
        row = {
            "source": "Section 13.4.1 STBIO1 Register Map (under Section 13.4 STBIO1 Register Map), paragraph 034",
        }
        self.assertEqual(
            _preview_blocks_for_requirement(
                row,
                [],
                {"Regmap": {}, "Unassigned": {}},
                {"Regmap": ["Register Map"]},
            ),
            ["Regmap"],
        )

    def test_source_paragraph_is_last_resort_context(self):
        block_defs = {"Register Block": {}, "Unassigned": {}}
        source_only = {
            "source": "Section 7.1 Operating mode (under Section 7 Control), paragraph 004",
        }
        self.assertEqual(
            _preview_blocks_for_requirement(source_only, [], block_defs),
            ["Operating mode"],
        )

        concrete = dict(source_only)
        concrete["source_section_owner"] = "Register Block"
        self.assertEqual(
            _preview_blocks_for_requirement(concrete, [], block_defs),
            ["Register Block"],
        )

    def test_adc_dft_test_paragraph_stays_source_context_until_approved(self):
        block_defs = {"ADC": {}, "Regmap": {}, "Unassigned": {}}
        source = (
            "Section 18.3 ADC TEST LOW NOISE "
            "(under Section 18 Digital DFT), paragraph 006 (page 160)"
        )
        self.assertEqual(
            _source_section_owner(source, {"ADC": ["ADC"], "Regmap": ["Regmap"]}),
            "",
        )
        for requirement_id in ("DDS_STBIO1_0701", "DDS_STBIO1_0702"):
            row = {
                "source_req_id": requirement_id,
                "source": source,
                "requirement_statement": "Enable ADC TEST LOW NOISE by register writes.",
                "source_section_owner": "ADC",
            }
            self.assertEqual(
                _preview_blocks_for_requirement(row, ["ADC", "Regmap"], block_defs),
                ["ADC TEST LOW NOISE"],
            )
            self.assertEqual(
                _map_blocks(row, {}, block_defs, {}, {}, []),
                ["Unassigned"],
            )

    def test_configured_interaction_requirement_maps_to_declared_endpoints(self):
        block_to_requirements = {
            "Source Block": [],
            "Destination Block": [],
        }
        block_defs = {"Source Block": {}, "Destination Block": {}, "Unassigned": {}}
        interaction_rows = [
            {
                "From block": "Source Block",
                "To block": "Destination Block",
                "Requirement IDs": "REQ-CONNECTION",
            }
        ]
        _link_interaction_requirements_to_blocks(
            block_to_requirements,
            block_defs,
            interaction_rows,
        )
        self.assertEqual(block_to_requirements, {
            "Source Block": ["REQ-CONNECTION"],
            "Destination Block": ["REQ-CONNECTION"],
        })
        row = {
            "source_req_id": "REQ-CONNECTION",
            "source": "Section 4.1 Connection Matrix (under Section 4 Interconnect), paragraph 002",
            "requirement_statement": "Source Block connects to Destination Block",
        }
        self.assertEqual(
            _map_blocks(row, {}, block_defs, {}, {}, interaction_rows),
            ["Source Block", "Destination Block"],
        )

    def test_source_matrix_rows_do_not_get_single_preview_owner(self):
        row = {
            "source_req_id": "REQ-MATRIX",
            "source": "Section 4.1 XBAR Connection Matrix (under Section 4 Interconnect)",
            "requirement_statement": "Source Block connects to Destination Block",
        }
        self.assertEqual(
            _preview_blocks_for_requirement(
                row,
                ["Destination Block"],
                {"Regmap": {}, "Destination Block": {}, "Unassigned": {}},
                {},
                {"REQ-MATRIX": ["Source Block", "Destination Block"]},
            ),
            ["Unassigned"],
        )

    def test_connection_matrix_context_is_safe_without_edge_ledger(self):
        row = {
            "source_req_id": "REQ-MATRIX",
            "source": "Section 4.1 XBAR Connection Matrix",
            "requirement_statement": "Source Block connects to Destination Block",
        }
        self.assertEqual(
            _preview_blocks_for_requirement(
                row,
                ["Regmap"],
                {"Regmap": {}, "Unassigned": {}},
            ),
            ["Unassigned"],
        )

    def test_explicit_to_target_beats_incidental_adc_term(self):
        row = {
            "requirement_statement": "Configure ADC calibration. [TO: IPOS_MAIN_CTRL]",
        }
        block_defs = {"ADC": {}, "Main Controller": {}, "Unassigned": {}}
        aliases = {"Main Controller": ["IPOS_MAIN_CTRL"]}
        self.assertEqual(_explicit_target_block(row, block_defs, aliases), "Main Controller")
        self.assertEqual(
            _map_blocks(row, {"ADC": ["adc"]}, block_defs, aliases, {}, []),
            ["Main Controller"],
        )

    def test_mapping_preview_markdown_is_derived_from_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "architecture_mapping_preview.csv"
            csv_path.write_text(
                "candidate_block,requirement_id\nADC,REQ-1\nUnassigned,REQ-2\n",
                encoding="utf-8",
            )
            _write_mapping_preview_markdown(csv_path)
            markdown = csv_path.with_suffix(".md").read_text(encoding="utf-8")
            self.assertIn("| ADC | 1 | REQ-1 |", markdown)
            self.assertIn("| Unassigned | 1 | REQ-2 |", markdown)

    def test_ambiguous_ontology_roles_do_not_create_single_block_owner(self):
        block_defs = {
            "Register Block": {"function": "register access"},
            "Source Block": {"function": "source endpoint"},
            "Destination Block": {"function": "destination endpoint"},
            "Unassigned": {},
        }
        row = {
            "source_req_id": "REQ-MATRIX",
            "source": "Section 4.1 Connection Matrix (under Section 4 Interconnect), paragraph 002",
            "requirement_statement": "Source Block connects to Destination Block",
            "category": "Digital",
            "requirement_type": "functional",
        }
        ontology_links = {
            "REQ-MATRIX": [
                {
                    "role": "Register Block",
                    "related_role": "Source Block; Destination Block",
                    "relation_type": "supports",
                    "function_or_property_evidence": "connection matrix participants",
                }
            ]
        }
        self.assertEqual(
            _map_blocks(row, {}, block_defs, {}, ontology_links),
            ["Unassigned"],
        )

    def test_previous_traceability_reader_accepts_current_and_legacy_schemas(self):
        with tempfile.TemporaryDirectory() as directory:
            current_path = Path(directory) / "current.csv"
            current_path.write_text("source_req_id,block\nREQ-1,Existing Block\n", encoding="utf-8")
            legacy_path = Path(directory) / "legacy.csv"
            legacy_path.write_text("Requirement ID,Block(s)\nREQ-2,Legacy Block\n", encoding="utf-8")
            self.assertEqual(_read_previous_blocks_by_requirement(current_path), {"REQ-1": "Existing Block"})
            self.assertEqual(_read_previous_blocks_by_requirement(legacy_path), {"REQ-2": "Legacy Block"})

    def test_previous_concrete_owner_cascades_over_generated_candidate(self):
        preview_owner_ids = {"Generated Candidate": ["REQ-1"], "Existing Block": []}
        cascaded = _cascade_previous_concrete_owners(
            preview_owner_ids,
            {"REQ-1": "Existing Block"},
            {"Generated Candidate": {}, "Existing Block": {}, "Unassigned": {}},
        )
        self.assertEqual(cascaded, 1)
        self.assertEqual(preview_owner_ids["Generated Candidate"], [])
        self.assertEqual(preview_owner_ids["Existing Block"], ["REQ-1"])

    def test_previous_concrete_owner_def_is_added_when_profile_lacks_it(self):
        block_defs = {"Generated Candidate": {}, "Unassigned": {}}
        added = _ensure_previous_concrete_owner_defs(block_defs, {"REQ-1": "Existing Block"})
        self.assertEqual(added, 1)
        self.assertIn("Existing Block", block_defs)
        self.assertIn("approved upstream traceability", block_defs["Existing Block"]["function"])

    def test_gui_stage_menu_exposes_strengthened_workflow(self):
        keys = {SINGLE_STAGE_LABEL_TO_KEY[label] for label in SINGLE_STAGE_LABELS}
        self.assertEqual(
            keys,
            {"0", "1", "2", "2a", "2f", "3", "4", "5", "6", "7", "arch-compare", "regenerate_workbook"},
        )
        self.assertNotIn("S2B - Merge Impact Analysis", SINGLE_STAGE_LABELS)
        self.assertNotIn("S2H - Immutable Approved Snapshot", SINGLE_STAGE_LABELS)
        self.assertIn("Stage 6 - Digital IPOS", SINGLE_STAGE_LABELS)
        self.assertIn("Stage 7 - Analog IPOS", SINGLE_STAGE_LABELS)
        self.assertEqual(SINGLE_STAGE_LABELS[-1], "Optional Architecture Comparison")
        self.assertEqual(SINGLE_STAGE_LABEL_TO_KEY["Stage 6 - Digital IPOS"], "6")
        self.assertEqual(SINGLE_STAGE_LABEL_TO_KEY["Optional Architecture Comparison"], "arch-compare")
        labels_by_id = {node["id"]: node["label"] for node in WORKFLOW_DIAGRAM_NODES}
        self.assertIn("ARS", labels_by_id["stage4"])
        self.assertIn("DRS", labels_by_id["stage5"])
        self.assertIn("Digital IPOS", labels_by_id["stage6"])
        self.assertIn("Optional", labels_by_id["arch_compare"])
        edge_pairs = {(source, target) for source, target, _kind in WORKFLOW_DIAGRAM_EDGES}
        self.assertIn(("stage4", "stage5"), edge_pairs)
        self.assertIn(("stage5", "stage6"), edge_pairs)
        self.assertIn(("stage6", "stage7"), edge_pairs)
        self.assertIn(("stage5", "arch_compare"), edge_pairs)
        self.assertNotIn(("stage4", "arch_compare"), edge_pairs)
        self.assertNotIn(("stage3", "stage5"), edge_pairs)
        range_keys = {RANGE_STAGE_LABEL_TO_KEY[label] for label in RANGE_STAGE_LABELS}
        self.assertEqual(range_keys, set(STAGE_ORDER))
        self.assertNotIn("arch-compare", range_keys)

    def test_compact_workflow_scrollregion_contains_rightmost_content(self):
        bounds = (0, 0, 1576, 255)
        scrollregion = compact_workflow_scrollregion(bounds, margin=16)
        self.assertEqual(scrollregion, (-16, -16, 1592, 271))

    def test_compact_workflow_labels_fit_boxes_at_every_zoom(self):
        root = tk.Tk()
        root.withdraw()
        try:
            gui = object.__new__(WorkflowGUI)
            gui.diagram_canvas = tk.Canvas(root)
            gui._bind_stage_click = MagicMock()
            gui._refresh_stage_styles = MagicMock()
            stage_font_sizes = {}
            for display_scale in (1.0, 1.5, 2.0):
                root.tk.call("tk", "scaling", display_scale)
                for zoom_step in range(6, 21):
                    zoom = zoom_step / 10
                    gui.compact_workflow_zoom = zoom
                    gui._draw_compact_workflow_graph()
                    for node in WORKFLOW_DIAGRAM_NODES:
                        with self.subTest(scale=display_scale, zoom=zoom, node=node["id"]):
                            items = gui.diagram_canvas.find_withtag(node["id"])
                            rectangle = next(item for item in items if gui.diagram_canvas.type(item) == "rectangle")
                            label = next(item for item in items if gui.diagram_canvas.type(item) == "text")
                            box = gui.diagram_canvas.coords(rectangle)
                            bounds = gui.diagram_canvas.bbox(label)
                            padding = 5 * zoom
                            self.assertGreaterEqual(bounds[0], box[0] + padding)
                            self.assertGreaterEqual(bounds[1], box[1] + padding)
                            self.assertLessEqual(bounds[2], box[2] - padding)
                            self.assertLessEqual(bounds[3], box[3] - padding)
                            self.assertEqual(gui.diagram_canvas.itemcget(label, "text"), node["label"])
                            self.assertAlmostEqual(box[2] - box[0], (112 if node["kind"] == "main" else 150) * zoom)
                    if display_scale == 1.0 and zoom in (0.6, 2.0):
                        stage_font_sizes[zoom] = int(root.tk.splitlist(gui.diagram_canvas.itemcget(gui.stage_labels["0"], "font"))[1])
            self.assertGreater(stage_font_sizes[2.0], stage_font_sizes[0.6])
        finally:
            root.update_idletasks()
            root.destroy()

    def test_full_workflow_labels_fit_boxes_at_display_scales(self):
        root = tk.Tk()
        root.withdraw()
        try:
            renderer = WorkflowDiagramRenderer(ttk.Frame(root))
            for display_scale in (1.0, 1.5, 2.0):
                root.tk.call("tk", "scaling", display_scale)
                renderer.refresh()
                for node_id, (rectangle, label) in renderer.node_items.items():
                    with self.subTest(scale=display_scale, node=node_id):
                        box = renderer.canvas.coords(rectangle)
                        bounds = renderer.canvas.bbox(label)
                        self.assertGreaterEqual(bounds[0], box[0] + 5)
                        self.assertGreaterEqual(bounds[1], box[1] + 5)
                        self.assertLessEqual(bounds[2], box[2] - 5)
                        self.assertLessEqual(bounds[3], box[3] - 5)
        finally:
            root.update_idletasks()
            root.destroy()

    def test_compact_workflow_keeps_digital_and_analog_ipos_on_distinct_rows(self):
        nodes = {node["id"]: node for node in WORKFLOW_DIAGRAM_NODES}
        self.assertGreaterEqual(
            compact_workflow_node_y(nodes["stage7"]) - compact_workflow_node_y(nodes["stage6"]),
            42,
        )
        self.assertNotEqual(
            compact_workflow_node_y(nodes["stage4"]),
            compact_workflow_node_y(nodes["stage5"]),
        )

    def test_cli_separates_digital_ipos_from_architecture_comparison(self):
        parser = build_parser()
        digital_args = parser.parse_args(["run", "--stage", "6"])
        comparison_args = parser.parse_args([
            "arch-compare", "--project-to-compare", "sibling-project",
        ])
        self.assertEqual(digital_args.command, "run")
        self.assertEqual(digital_args.stage, "6")
        self.assertFalse(hasattr(digital_args, "project_to_compare"))
        self.assertEqual(comparison_args.command, "arch-compare")
        self.assertEqual(comparison_args.project_to_compare, "sibling-project")

    def test_sysml_coverage_fails_for_omitted_block_requirement(self):
        snapshot = SimpleNamespace(
            rows=({"canonical_id": "CAN-1", "source_req_id": "REQ-1"},),
            source_links={"CAN-1": ("REQ-1",)},
            mapping={"CAN-1": "ADC"},
        )
        with self.assertRaises(SysMLCompletenessError):
            validate_snapshot_requirement_coverage(snapshot, [], {"ADC": []})

    def test_sysml_coverage_accepts_full_block_requirement(self):
        snapshot = SimpleNamespace(
            rows=({"canonical_id": "CAN-1", "source_req_id": "REQ-1"},),
            source_links={"CAN-1": ("REQ-1",)},
            mapping={"CAN-1": "ADC"},
        )
        result = validate_snapshot_requirement_coverage(
            snapshot,
            [],
            {"ADC": [{"source_req_id": "REQ-1"}]},
        )
        self.assertEqual(result["missing_by_block"], {})


if __name__ == "__main__":
    unittest.main()
