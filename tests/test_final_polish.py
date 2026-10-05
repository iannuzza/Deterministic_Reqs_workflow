import sys
import inspect
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from openpyxl import Workbook

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from report_generation_service import _ordered_fields, _style_data_sheet
from sysml_generation_service import SysMLCompletenessError, validate_snapshot_requirement_coverage
from workflow_gui import (
    SINGLE_STAGE_LABELS,
    SINGLE_STAGE_LABEL_TO_KEY,
    RANGE_STAGE_LABELS,
    RANGE_STAGE_LABEL_TO_KEY,
    WorkflowGUI,
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

    def test_report_sheet_has_filter_freeze_pane_and_table(self):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(["source_req_id", "block", "statement"])
        worksheet.append(["REQ-1", "ADC", "shall sample"])
        _style_data_sheet(worksheet, ["source_req_id", "block", "statement"], 1)
        self.assertEqual(worksheet.freeze_panes, "A2")
        self.assertEqual(worksheet.auto_filter.ref, "A1:C2")
        self.assertEqual(len(worksheet.tables), 1)

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
