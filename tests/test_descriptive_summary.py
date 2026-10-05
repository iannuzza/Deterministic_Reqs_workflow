import csv
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from workflow_routing import (
    DESCRIPTIVE_MODE_TOPIC_SPECS,
    DESCRIPTIVE_POWER_TOPIC_SPECS,
    DESCRIPTIVE_DIGITAL_TOPIC_SPECS,
    assign_ipos_descriptive_topic,
    assemble_descriptive_summary,
    build_ipos_functional_input,
    compose_ipos_overview,
    compose_technical_block_purpose,
    compose_drs_interaction_summary,
    compose_drs_role_summary,
    drs_section_prose_findings,
    document_author_name,
    validate_document_author_fields,
    project_architecture_interactions,
    project_architecture_interfaces,
    summarize_architecture_interactions,
    validate_drs_block_descriptions,
    _ipos_aggregate_responsibility,
    _ipos_evidence_summary,
    validate_ipos_descriptive_output,
    write_ipos_descriptive_audit,
    write_descriptive_audit,
)
from low_power_descriptive import (
    architecture_records_from_function_rows,
    assemble_low_power_descriptive,
    is_drs_top_level_record,
    power_domain_records_from_ocr,
    read_selected_low_power_audit,
    write_low_power_audit,
)
from ipos_semantic_normalizer import detail_evidence_facets, compose_detail_groups
from generate_ipos_specs import approved_snapshot_candidate_rows
from run_srs_gen_spec_agent import _render_srs_low_power_section
from run_drs_gen_spec_agent import (
    BlockInfo, _drs_block_relationships, _drs_descriptive_blocks, _drs_intro_rows,
    _drs_function_summary, _drs_power_domain_rows, _drs_topic_narrative, _drs_shared_facet_rows,
    _drs_domain_function_sentence, _drs_clock_path_rows, _drs_clock_path_markdown_row, _drs_sync_connection_rows,
    _drs_power_clock_routes, _drs_power_reset_outputs, _drs_section_interaction_summary,
    _drs_clock_section_summary, _render_approved_port_table, validate_drs_descriptive_artifacts,
    _drs_rendered_prose_findings, _drs_top_level_overview,
    _drs_processing_summary,
)


class DescriptiveSummaryTests(unittest.TestCase):
    def test_drs_top_level_overview_breaks_long_description_into_short_paragraphs(self):
        overview = _drs_top_level_overview(
            [("Sensor", "FIFO", "sample data"), ("Host", "Regmap", "SPI host transactions")],
            ["The device integrates ECG and PPG.", "The source describes an embedded engine."],
        )
        paragraphs = overview.split("\n\n")
        self.assertEqual(len(paragraphs), 3)
        self.assertTrue(all(len(re.findall(r"(?<=[.!?])(?:\s|$)", paragraph)) <= 2 for paragraph in paragraphs))
        self.assertIn("The device integrates ECG and PPG.", overview)
        self.assertIn("The source material does not define a separate application role.", overview)

    def test_drs_section_quality_rejects_process_and_counts_in_both_formats(self):
        for prose in ("Approved integration evidence groups the exchanges.",
                      "Approved block functions identify Storage.",
                      "Approved clock routes reach destinations.",
                      "The fabric connects 4 source endpoints across 8 paths.",
                      "The architecture also records a status exchange."):
            with self.subTest(prose=prose):
                self.assertTrue(drs_section_prose_findings(prose))
                markdown = "## 3. Top Level Overview\n" + prose
                document = ET.fromstring(
                    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                    '<w:body><w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
                    '<w:r><w:t>3. Top Level Overview</w:t></w:r></w:p>'
                    '<w:p><w:r><w:t>' + prose + '</w:t></w:r></w:p></w:body></w:document>'
                )
                findings = _drs_rendered_prose_findings(markdown, document)
                self.assertTrue(any(":markdown:3:" in finding for finding in findings))
                self.assertTrue(any(":docx:3:" in finding for finding in findings))
        self.assertEqual(drs_section_prose_findings("The fabric distributes 16 MHz clocks without clock gating."), [])
        self.assertEqual(_drs_rendered_prose_findings("## 6. Requirement catalog\nThe unit shall operate.\n"), [])

    def test_drs_section_grouping_preserves_edges_and_runtime_names(self):
        rows = [("Producer", "Consumer", "samples"), ("Producer", "Monitor", "samples"),
                ("Peer", "Consumer", "samples"), ("Peer", "Monitor", "samples"),
                ("Host", "Consumer", "register writes")]
        original = list(rows)
        summary = compose_drs_interaction_summary(rows + rows)
        self.assertEqual(summary, compose_drs_interaction_summary(rows))
        self.assertIn("Producer and Peer provide samples to Consumer and Monitor.", summary)
        self.assertIn("Host provides register writes to Consumer.", summary)
        self.assertNotIn("writes to Consumer and Monitor", summary)
        self.assertEqual(rows, original)
        renamed = [(source.replace("Producer", "Capture"), target, exchange) for source, target, exchange in rows]
        self.assertEqual(compose_drs_interaction_summary(renamed), summary.replace("Producer", "Capture"))
        role = compose_drs_role_summary([("Capture", "Perform sample filtering, and write results to memory.")], ("filtering", "results"))
        self.assertIn("Capture performs sample filtering.", role)
        self.assertIn("Capture writes results to memory.", role)
        self.assertEqual(drs_section_prose_findings(role), [])
        coordinated = compose_drs_role_summary([
            ("Control", "Generate and receive control signals, perform filtering, and write results."),
            ("Bridge", "Accept requests and translate them into bus transactions."),
        ], ())
        self.assertIn("Control generates and receives control signals.", coordinated)
        self.assertIn("Control performs filtering.", coordinated)
        self.assertIn("Bridge accepts requests and translates them into bus transactions.", coordinated)
        self.assertNotIn("signals, perform", coordinated)
        missing_role = _drs_processing_summary([], [("Compute", "Storage", "bus connection")])
        self.assertTrue(missing_role.startswith("Compute connects to Storage through bus."))
        self.assertTrue(missing_role.endswith("Processing behavior: need clarification."))

    def test_drs_section_synthesis_groups_approved_exchanges_without_promoting_endpoints(self):
        rows = [("Source A", "Sink A", "digital samples"),
                ("Source B", "Sink B", "FIFO watermark flags"),
                ("Host", "Registers", "SPI register transactions"),
                ("Unit", "Endpoint", "XBAR connection")]
        summary = _drs_section_interaction_summary(rows)
        self.assertIn("Source A provides digital samples to Sink A", summary)
        self.assertIn("Host provides SPI register transactions to Registers", summary)
        self.assertIn("Unit connects to Endpoint through XBAR", summary)
        self.assertNotIn("Source A -> Sink A", summary)
        self.assertNotIn("approved", summary.lower())
        self.assertNotRegex(summary, r"\d+ (?:paths|source endpoints|destinations|interconnect links)")
        self.assertNotIn("Endpoint block", summary)
        self.assertIn("need clarification", _drs_section_interaction_summary([]))
        clock_summary = _drs_clock_section_summary([
            ("REQ-1", "u_power.clock", "u_core.clk", "16 MHz", "Not gated"),
            ("REQ-2", "need clarification", "need clarification", "32 kHz", "Gated"),
        ])
        self.assertIn("16 MHz", clock_summary)
        self.assertIn("32 kHz", clock_summary)
        self.assertIn("without clock gating", clock_summary)
        self.assertIn("need clarification", clock_summary)
        self.assertNotIn("approved", clock_summary.lower())
        self.assertNotIn("route(s)", clock_summary)

    def test_drs_shared_facets_and_power_routes_preserve_evidence_boundary(self):
        storage = BlockInfo("Store", "Provide FIFO storage and AHB/memory access in mutually exclusive modes.", "", "", "", "concrete_block")
        power = BlockInfo("Power", "Sequence boot clocks and reset.", "", "", "", "concrete_block")
        facets = dict(_drs_shared_facet_rows([storage, power], [("Host", "Store", "XBAR connection")]))
        self.assertIn("Store", facets["Shared-resource ownership"])
        self.assertNotIn("Provide FIFO storage", facets["Shared-resource ownership"])
        self.assertIn("Concurrent-access ordering policy: need clarification", facets["Register and memory access coordination"])
        for unsupported in ("Flow control and backpressure", "Synchronization", "Latency and bandwidth"):
            self.assertEqual(facets[unsupported], "need clarification")
        paths = [("REQ-1", "top.u_power.clock", "top.core.clock", "16 MHz", "Not gated"),
                 ("REQ-2", "need clarification", "need clarification", "16 MHz", "Gated")]
        self.assertEqual(_drs_power_clock_routes(paths, [power]), paths[:1])
        ports = [{"Owner": "Power", "Port name": "resetn_core", "Direction": "output",
                  "Type / details": "reset core", "Source page": "41", "Ownership status": "approved"},
                 {"Owner": "Other", "Port name": "resetn_io", "Direction": "output",
                  "Type / details": "reset io", "Source page": "42", "Ownership status": "approved"}]
        self.assertEqual(_drs_power_reset_outputs(ports, [power]), [("Power", "resetn_core", "reset core", "41")])

    def test_drs_clock_paths_require_approved_explicit_routes(self):
        route = {
            "source_req_id": "REQ-1", "approved_classification": "Digital", "lifecycle_state": "approved",
            "requirement_statement": "The top.pmu.clock signal shall be connected to the top.core.clock signal, with frequency 16 MHz and with clock gating top.pmu.enable.",
        }
        self.assertEqual(_drs_clock_path_rows([route]), [
            ("REQ-1", "top.pmu.clock", "top.core.clock", "16 MHz", "Gated; control expression: top.pmu.enable")
        ])
        split_control = {**route, "requirement_statement": route["requirement_statement"].replace(
            "top.pmu.enable", "top.u_pm u.enable | ~top.u_p ad_mux.scan_enable")}
        self.assertEqual(_drs_clock_path_rows([split_control])[0][4],
                         "Gated; control expression: top.u_pm u.enable | ~top.u_p ad_mux.scan_enable; signal spelling: need clarification")
        self.assertIn(r"u.enable \| ~top", _drs_clock_path_markdown_row(_drs_clock_path_rows([split_control])[0]))
        without_control = {**route, "requirement_statement": route["requirement_statement"].replace(
            " top.pmu.enable", "")}
        self.assertEqual(_drs_clock_path_rows([without_control])[0][4], "Gated; control expression: need clarification")
        ungated = {**route, "requirement_statement": route["requirement_statement"].replace(
            "with clock gating top.pmu.enable", "without clock gating")}
        self.assertEqual(_drs_clock_path_rows([ungated])[0][4], "Not gated")
        malformed = {**route, "requirement_statement": route["requirement_statement"].replace("top.core.clock", "top.u.core.clock")}
        self.assertEqual(_drs_clock_path_rows([malformed])[0][1:3], ("need clarification", "need clarification"))
        self.assertEqual(_drs_clock_path_rows([{**route, "lifecycle_state": "staged"},
                                               {**route, "requirement_statement": "A clock might reach core."}]), [])
        sync = {**route, "requirement_statement": "The u_p\nmu.resetn_32k_main_ctrl signal shall be connected to the top.i_rstn_sync\n_32 signal."}
        ports = [
            {"Owner": "Power", "Port name": "resetn_32k_main_ctrl", "Direction": "output", "Ownership status": "approved"},
            {"Owner": "Controller", "Port name": "i_rstn_sync_32", "Direction": "input", "Ownership status": "approved"},
        ]
        self.assertEqual(_drs_sync_connection_rows([sync], ports),
                         [("REQ-1", "Power.resetn_32k_main_ctrl", "Controller.i_rstn_sync_32")])
        truncated = {**sync, "requirement_statement": "The u_p signal shall be connected to the mu.resetn_32k_main_ctrlu_top.i_rstn_sync_32 signal."}
        self.assertEqual(_drs_sync_connection_rows([truncated], ports),
                 [("REQ-1", "Power.resetn_32k_main_ctrl", "Controller.i_rstn_sync_32")])
        self.assertEqual(_drs_sync_connection_rows([sync], ports[:1]),
                         [("REQ-1", "Power.resetn_32k_main_ctrl", "need clarification")])
        self.assertEqual(_drs_sync_connection_rows([{**sync, "lifecycle_state": "staged"}], ports), [])

    def test_drs_function_and_topic_summaries_do_not_promote_trace_only_roles(self):
        trace_only = BlockInfo("Core", "Represent the digital architecture block described by Stage 2 interaction evidence.", "", "", "", "concrete_block")
        power = BlockInfo("Power unit", "Sequence POR, clock-ready signaling, and digital reset for power modes.", "", "", "", "concrete_block")
        storage = BlockInfo("Store", "Provide FIFO storage in mutually exclusive modes.", "", "", "", "concrete_block")
        self.assertIn("need clarification", _drs_function_summary(trace_only, []))
        self.assertIn("An interrupt triggers Core wake-up", _drs_function_summary(trace_only, ["To wake up the Core, trigger an interrupt."]))
        self.assertNotIn("Core", _drs_topic_narrative("Power and clock islands", [trace_only, power, storage]))
        self.assertIn("Power unit", _drs_topic_narrative("Power and clock islands", [trace_only, power, storage]))
        self.assertIn("mutually exclusive", _drs_topic_narrative("Arbitration and control", [trace_only, power, storage]))

    @unittest.skipUnless(os.name == "nt", "Windows display-name API")
    def test_document_author_follows_current_windows_user(self):
        for full_name in ("First User", "Second User"):
            def display_name(_format, buffer, _length):
                buffer.value = full_name
                return 1

            with patch("ctypes.windll.secur32", SimpleNamespace(GetUserNameExW=display_name)):
                self.assertEqual(document_author_name(), full_name)

        with patch("ctypes.windll.secur32", SimpleNamespace(GetUserNameExW=lambda *_args: 0)):
            with self.assertRaisesRegex(RuntimeError, "full display name is unavailable"):
                document_author_name()

    def test_document_author_validator_rejects_mismatched_title(self):
        markdown_path = Path(__file__).resolve().parents[1] / "artifacts/stage5_drs/digital_requirements_specification.md"
        self.assertEqual(validate_document_author_fields(markdown_path), [])
        original_read_text = Path.read_text

        def changed_author(path, *args, **kwargs):
            content = original_read_text(path, *args, **kwargs)
            return content.replace("Author: " + document_author_name(), "Author: Different User") if path == markdown_path else content

        with patch.object(Path, "read_text", changed_author):
            self.assertIn(f"document_history_author_mismatch:{markdown_path}", validate_document_author_fields(markdown_path))

    def test_drs_domain_projection_and_block_relationships_use_structured_evidence(self):
        records = [{
            "evidence_kind": "power_domain",
            "statement": "PD_TEST: Included block(s): core. Domain type: Retention. Control mode: firmware. • Function: Preserves state. • Characteristics: Idle.",
        }, {
            "evidence_kind": "architecture",
            "statement": "PD_FALSE: Included block(s): core. Domain type: Switchable. Control mode: SW. • Function: Invalid.",
        }]
        self.assertEqual(_drs_power_domain_rows(records), [("PD_TEST", "Retention", "firmware", "Preserves state")])
        self.assertEqual(_drs_domain_function_sentence("PD_TEST", "Preserves state"), "PD_TEST has the documented function: Preserves state.")
        self.assertEqual(_drs_domain_function_sentence("PD_SUPPLY", "power supply to memory"), "PD_SUPPLY supplies power to memory.")
        interactions = [("Block A", "Regmap", "configuration writes"), ("ISPU", "Block A", "sample ready")]
        self.assertEqual(_drs_block_relationships("Block A", interactions),
                         "to Regmap (configuration writes); from ISPU (sample ready)")
        self.assertIn("need clarification", _drs_block_relationships("Other block", interactions))

    def test_drs_central_validator_rejects_missing_power_table(self):
        root = Path(__file__).resolve().parents[1]
        markdown_path = root / "artifacts/stage5_drs/digital_requirements_specification.md"
        self.assertEqual(validate_drs_descriptive_artifacts(root), [])
        original_read_text = Path.read_text

        def without_domain_table(path, *args, **kwargs):
            content = original_read_text(path, *args, **kwargs)
            return content.replace("| Domain | Type | Control | Function |", "") if path == markdown_path else content

        with patch.object(Path, "read_text", without_domain_table):
            self.assertIn("drs_power_domain_table_missing", validate_drs_descriptive_artifacts(root))

        def without_block_heading(path, *args, **kwargs):
            content = original_read_text(path, *args, **kwargs)
            return content.replace("#### **Smart FIFO** {#smart-fifo}", "") if path == markdown_path else content

        with patch.object(Path, "read_text", without_block_heading):
            self.assertIn("drs_digital_function_missing:Smart FIFO", validate_drs_descriptive_artifacts(root))

        def without_clock_summary(path, *args, **kwargs):
            content = original_read_text(path, *args, **kwargs)
            if path == markdown_path:
                content = re.sub(r"The clock network distributes [^\n]+", "Clock summary removed.", content)
            return content

        with patch.object(Path, "read_text", without_clock_summary):
            self.assertIn("drs_clock_section_summary_missing", validate_drs_descriptive_artifacts(root))

        def without_shared_and_clock(path, *args, **kwargs):
            content = original_read_text(path, *args, **kwargs)
            return content.replace("Flow control and backpressure: need clarification", "").replace(
                "Clock-path endpoints requiring clarification: DDS_STBIO1_2024.", "") if path == markdown_path else content

        with patch.object(Path, "read_text", without_shared_and_clock):
            findings = validate_drs_descriptive_artifacts(root)
            self.assertIn("drs_shared_facet_missing:Flow control and backpressure", findings)
            self.assertIn("drs_power_clock_endpoint_boundary_missing", findings)

        def altered_clock_control(path, *args, **kwargs):
            content = original_read_text(path, *args, **kwargs)
            return content.replace("u.adsp_run \\|", "u.changed_gate \\|") if path == markdown_path else content

        with patch.object(Path, "read_text", altered_clock_control):
            findings = validate_drs_descriptive_artifacts(root)
            self.assertIn("drs_power_clock_route_missing:DDS_STBIO1_1022", findings)
            self.assertIn("drs_clock_path_missing:DDS_STBIO1_1022", findings)

    def test_drs_intro_uses_only_structured_approved_interactions(self):
        entries = [
            "Interaction: PMU -> Main Controller (power/clock status; mode transition)",
            "Interaction: PMU -> Main Controller (power/clock status; duplicate note)",
            "Interaction: SPI interface -> Regmap (SPI register transactions; host access)",
            "Interaction: Regmap -> FIFO (XBAR connection; source-derived cell)",
            "An unsupported requirement shall not be copied.",
        ]
        rows = project_architecture_interactions(entries)
        self.assertEqual(rows, [
            ("PMU", "Main Controller", "power/clock status"),
            ("SPI interface", "Regmap", "SPI register transactions"),
            ("Regmap", "FIFO", "XBAR connection"),
        ])
        self.assertIn("PMU provides power/clock status to Main Controller", summarize_architecture_interactions(rows))
        self.assertEqual(summarize_architecture_interactions([("ADSP", "Regmap", "XBAR connection")]),
                 "ADSP connects to Regmap through XBAR connection.")
        self.assertNotIn("shall", summarize_architecture_interactions(rows))
        sections = _drs_intro_rows(entries)
        self.assertIn(rows[0], sections["4.6 Digital performance requirements"])
        self.assertIn(rows[1], sections["4.3 Register and configuration requirements"])
        self.assertIn(rows[1], sections["4.4 Interface and communication requirements"])
        self.assertNotIn(rows[2], sections["4.3 Register and configuration requirements"])
        self.assertNotIn(rows[2], sections["4.5 Data-path and buffering requirements"])
        self.assertIn(rows[2], _drs_intro_rows(entries, {"Regmap"})["7. Interfaces and mixed-signal interactions"])
        self.assertNotIn("IRQ logic", str(sections))
        self.assertEqual(project_architecture_interfaces([
            "Approved interface VDD owned by PMU: Core supply",
            "Approved interface VDD owned by PMU: Core supply",
        ]), [("VDD", "PMU", "Core supply")])

    def test_drs_block_descriptions_use_approved_concrete_inventory_only(self):
        blocks = [
            BlockInfo("Block A", "Route digital samples.", "", "", "", "concrete_block"),
            BlockInfo("Control logic", "Route digital samples.", "", "", "", "logic_context"),
        ]
        selected = _drs_descriptive_blocks(blocks, [], {})
        self.assertEqual([block.name for block in selected], ["Block A"])
        self.assertEqual(
            compose_technical_block_purpose(selected[0].name, selected[0].function),
            "The Block A block is designed to route digital samples.",
        )

    def test_drs_block_validator_requires_provenance_and_tabular_ports(self):
        sentence = "The Block A block is designed to route digital samples."
        markdown = (
            "### **4.1 Digital block list** {#41-digital-block-list}\n"
            "The digital subsystem includes Block A.\n"
            "## 9. Top-level integration requirements\n"
            "### **9.1 Block A** {#91-block-a}\n" + sentence + "\n\n"
            "| Port name | Direction | Type / details | Source page |\n"
            "|---|---|---|---|\n| SDA | input | pad signal | 42 |\n"
        )
        blocks = [{"name": "Block A", "function": "Route digital samples."}]
        audit = [{
            "section": "DRS digital block descriptions", "mapped_block": "Block A",
            "source_evidence": "Route digital samples.", "statement": sentence,
            "source": "artifacts/stage2_mirco_arc/block_inventory.csv",
            "scope_decision": "approved_concrete_block", "output_order": "1",
        }]
        ports = [{"Owner": "Block A", "Ownership status": "approved", "Port name": "SDA",
                  "Direction": "input", "Type / details": "pad signal", "Source page": "42"}]
        self.assertEqual(validate_drs_block_descriptions(markdown, blocks, audit, ports), [])
        self.assertEqual(_render_approved_port_table(ports)[-1], "| SDA | input | pad signal | 42 |")
        variants = (
            (markdown.replace("| SDA | input | pad signal | 42 |", "- Port name: SDA"), "drs_port_name_bullet_list"),
            (markdown + "### **9.2 Control logic** {#92-control-logic}\nUnapproved text.\n", "unapproved_drs_block_paragraph"),
            (markdown.replace(sentence, "General functional description: approved digital function"),
             "description_uses_internal_process_language"),
        )
        for changed, expected in variants:
            with self.subTest(expected=expected):
                self.assertIn(expected, " ".join(validate_drs_block_descriptions(changed, blocks, audit, ports)))
        self.assertIn("drs_block_description_provenance_mismatch", " ".join(
            validate_drs_block_descriptions(markdown, blocks, [audit[0] | {"source_evidence": "other"}], ports)
        ))

    def test_ipos_evidence_summary_restores_names_and_guards_from_accepted_statements(self):
        cases = (
            (
                ("A new operation shall start only when quokka_run is low, and one between OTP_TEST bit, OTP_WRITE bit or OTP_BOOT bit is written to 1",
                 "To perform a BOOT routine, OTP_BOOT bit shall be written when quokka_run is low."),
                "Operation start conditions", ("quokka_run is low", "OTP_BOOT initiates the BOOT routine"),
            ),
            (
                ("During boot, the ADSP shall copy the content of the OTP memory into the OTP registers, following the access procedure.",
                 "During WRITE, the ADSP shall copy the content of the OTP regmap into the OTP memory, following the burn procedure."),
                "OTP memory transfer", ("OTP memory to OTP registers", "OTP regmap to OTP memory"),
            ),
            (
                ("A double byte write access to the address 0x68-0x6f shall start the data preload from AHB in order to have the internal fifo not empty when the read request will be done by the master.",),
                "Read data preloading", ("0x68-0x6f", "AHB", "master read request"),
            ),
            (
                ("At the release of the POR signal from the analog domain, the controller shall manage the turn-on of the LDO1V8 and starts clocks Start-Up Sequence (reported in spec).",),
                "Power-on start-up", ("POR", "LDO1V8", "clock start-up sequence"),
            ),
            (
                ("All the SENSOR_HUB_x registers shall be reset every time a new I2C operation starts.",),
                "Register reset on operation start", ("SENSOR_HUB_x registers", "I2C operation"),
            ),
            (
                ("If input signal HMASTER is set to 0 or 1, the FIFO Controller shall enter Memory mode.",),
                "Memory mode entry", ("HMASTER", "0 or 1"),
            ),
        )
        for statements, expected_title, fragments in cases:
            with self.subTest(title=expected_title):
                title, description = _ipos_evidence_summary([
                    {"candidate_evidence_statement": statement} for statement in statements
                ])
                self.assertEqual(title, expected_title)
                for fragment in fragments:
                    self.assertIn(fragment, description)

    def test_snapshot_candidates_include_approved_architecture_text_without_normative_promotion(self):
        snapshot = SimpleNamespace(source_path=Path("approved.csv"), rows=[
            {"source_req_id": "LOCAL", "requirement_statement": "Local approved behavior."},
            {"source_req_id": "ARCH", "requirement_statement": "Approved architecture behavior."},
            {"source_req_id": "OTHER", "requirement_statement": "Another block's behavior."},
        ])

        class Contract:
            def allocation(self, source_id):
                return {"approved_block": "Block A" if source_id != "OTHER" else "Block B"}

        candidates = approved_snapshot_candidate_rows(snapshot, Contract())
        self.assertEqual([row["source_req_id"] for row in candidates if row["mapped_block"] == "Block A"],
                         ["LOCAL", "ARCH"])
        self.assertEqual(candidates[1]["requirement_statement"], "Approved architecture behavior.")

    def test_detail_projection_keeps_multiple_actions_and_conditions_without_name_rules(self):
        statement = "When the channel is active, the Sample_FSM shall sample incoming data and store processed results."
        facets, _rejected = detail_evidence_facets(statement, "")
        self.assertEqual(len(facets), 2)
        self.assertIn("Samples incoming data", facets[0]["text"])
        self.assertIn("Stores processed results", facets[1]["text"])
        self.assertTrue(all("when the channel is active" in facet["text"] for facet in facets))
        renamed, _rejected = detail_evidence_facets(statement.replace("Sample_FSM", "Other_FSM"), "")
        self.assertEqual(facets, renamed)

    def test_detail_groups_do_not_invent_peer_interactions(self):
        rows = [{"decision": "accepted_candidate", "candidate_evidence_requirement_id": "REQ-1",
                 "candidate_evidence_statement": "The Sample_FSM shall sample incoming data.",
                 "candidate_refinement": "Samples incoming data."}]
        summary = compose_detail_groups(rows)
        self.assertEqual(len(summary), 1)
        self.assertNotIn("Interacts with", summary[0])
        self.assertEqual(rows[0]["summary_group_contributor_ids"], "REQ-1")

    def test_ipos_composer_is_inventory_bound_and_always_populates_sections(self):
        record = build_ipos_functional_input(
            "Block A",
            {"Function": "Store samples.", "Inputs": "samples", "Outputs": "status"},
            [{"mapped_block": "Block A", "source_req_id": "REQ-A", "requirement_statement": "The block shall store samples."}],
            domain="digital",
            provenance=("approved snapshot", "block_inventory.csv"),
        )
        sections, audit = compose_ipos_overview(record)
        self.assertTrue(sections["functionality"])
        self.assertTrue(sections["scope"])
        self.assertEqual(audit[0]["derivation_mode"], "direct_function")
        self.assertEqual(audit[1]["derivation_mode"], "function_plus_io_scope")
        self.assertEqual(audit[2]["decision"], "suppressed")
        self.assertNotIn("shall", " ".join(sections["scope"]).casefold())
        self.assertNotIn("register", " ".join(sections["scope"]).casefold())

    def test_ipos_scope_preserves_register_map_compound(self):
        record = build_ipos_functional_input(
            "Block A", {"Function": "Route device signals", "Inputs": "Mode selection, register-map controls",
                        "Outputs": "Routed signals"}, [],
        )
        sections, _audit = compose_ipos_overview(record)
        self.assertIn("register-map controls", sections["scope"][0])
        self.assertNotIn("-map controls", sections["scope"][0].replace("register-map", ""))

    def test_ipos_composer_does_not_use_other_block_or_drs_prose(self):
        record = build_ipos_functional_input(
            "Block A",
            {"Function": "Manage local buffering.", "Inputs": "samples", "Outputs": "buffered data"},
            [{"mapped_block": "Block B", "source_req_id": "REQ-B", "requirement_statement": "The DRS says to process ECG."}],
        )
        sections, audit = compose_ipos_overview(record)
        rendered = " ".join(sections["functionality"] + sections["scope"])
        self.assertNotIn("ECG", rendered)
        candidate = next(item for item in audit if item.get("candidate_evidence_statement"))
        self.assertEqual(candidate["decision"], "suppressed_due_to_cross_block_risk")

    def test_same_block_supported_refinement_is_rendered_and_audited(self):
        row = {
            "mapped_block": "Block A", "source_req_id": "REQ-A",
            "requirement_statement": "The block shall sample incoming data and store processed results.",
        }
        record = build_ipos_functional_input(
            "Block A",
            {"Function": "Acquire and process incoming data", "Inputs": "incoming data", "Outputs": "processed results"},
            [row], domain="digital", provenance=("approved snapshot", "block_inventory.csv"),
        )
        sections, audit = compose_ipos_overview(record)
        candidate = next(item for item in audit if item.get("candidate_refinement"))
        self.assertEqual(candidate["decision"], "accepted_candidate")
        self.assertEqual(candidate["target_section"], "supported_functions_and_scope")
        self.assertEqual(candidate["supporting_local_requirement_ids"], "REQ-A")
        self.assertIn(candidate["rendered_summary"], sections["scope"])
        self.assertTrue(candidate["rendered_summary"].startswith("**Local data processing."))
        self.assertNotIn("Supports approved", candidate["candidate_refinement"])
        self.assertIn("incoming data", candidate["candidate_refinement"])
        self.assertTrue(candidate["output_order"])

    def test_ipos_refinement_preserves_action_object_and_safe_context(self):
        rows = [
            {
                "mapped_block": "Block A", "source_req_id": "SAMPLE",
                "requirement_statement": "When the channel is selected, the controller shall sample incoming ECG data.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "WRITE",
                "requirement_statement": "The controller shall write processed results to the output buffer.",
            },
        ]
        record = build_ipos_functional_input(
            "Block A",
            {
                "Function": "Acquire and process sampled data",
                "Inputs": "channel configuration and sampled data",
                "Outputs": "processed results and output buffer",
            },
            rows,
        )
        sections, audit = compose_ipos_overview(record)
        candidates = {
            row["candidate_evidence_requirement_id"]: row["candidate_refinement"]
            for row in audit if row.get("candidate_evidence_statement")
        }
        self.assertIn("Samples incoming ECG data when the channel is selected.", candidates["SAMPLE"])
        self.assertIn("Writes processed results to output buffer.", candidates["WRITE"])
        self.assertNotEqual(candidates["SAMPLE"], candidates["WRITE"])
        rendered = {
            row["candidate_evidence_requirement_id"]: row["rendered_summary"]
            for row in audit if row.get("decision") == "accepted_candidate"
        }
        self.assertIn("Samples incoming ECG data", rendered["SAMPLE"])
        self.assertIn("Stores processed results to output buffer", rendered["WRITE"])

    def test_conflicts_require_the_same_action_and_target(self):
        inventory = {"Function": "Acquire incoming data", "Inputs": "incoming data", "Outputs": "output memory"}
        rows = [
            {"mapped_block": "Block A", "source_req_id": "STORE", "requirement_statement": "The controller shall store incoming data in output memory."},
            {"mapped_block": "Block A", "source_req_id": "SAMPLE", "requirement_statement": "The controller shall not sample incoming data in output memory."},
        ]
        _sections, audit = compose_ipos_overview(build_ipos_functional_input("Block A", inventory, rows))
        decisions = {row["candidate_evidence_requirement_id"]: row["decision"] for row in audit if row.get("candidate_evidence_statement")}
        self.assertEqual(decisions, {"STORE": "accepted_candidate", "SAMPLE": "accepted_candidate"})

    def test_ipos_projection_omits_parameter_only_and_unparsed_predicates(self):
        rows = [
            {
                "mapped_block": "Block A", "source_req_id": "TIMING",
                "requirement_statement": "The user shall configure time slot duration in the operation register.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "VERB",
                "requirement_statement": "The controller shall change state after setting the mode register.",
            },
        ]
        record = build_ipos_functional_input(
            "Block A",
            {"Function": "Manage sampled data", "Inputs": "configuration and samples", "Outputs": "control state"},
            rows,
        )
        sections, audit = compose_ipos_overview(record)
        candidates = [row for row in audit if row.get("candidate_evidence_statement")]
        self.assertFalse(any(row["candidate_refinement"] for row in candidates))
        self.assertFalse(any("time slot" in item.casefold() or "mode register" in item.casefold() for item in sections["scope"]))

    def test_ipos_channel_refinements_use_configuration_boundary_and_keep_distinct_targets(self):
        rows = [
            {
                "mapped_block": "Block A", "source_req_id": "CHANNEL-A",
                "requirement_statement": "The user shall select the active channel, in this case CH_A_SEL.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "CHANNEL-B",
                "requirement_statement": "The user shall select the active channel, in this case CH_B_SEL.",
            },
        ]
        record = build_ipos_functional_input(
            "Block A",
            {"Function": "Process sampled data", "Inputs": "configuration settings", "Outputs": "processed results"},
            rows,
        )
        sections, audit = compose_ipos_overview(record)
        candidates = [row for row in audit if row.get("decision") == "accepted_candidate"]
        summaries = {row["candidate_evidence_requirement_id"]: row["candidate_refinement"] for row in candidates}
        self.assertEqual(len(summaries), 2)
        self.assertIn("CH A", summaries["CHANNEL-A"])
        self.assertIn("CH B", summaries["CHANNEL-B"])
        self.assertNotEqual(summaries["CHANNEL-A"], summaries["CHANNEL-B"])
        rendered_groups = {row["rendered_summary"] for row in candidates if row.get("rendered_summary")}
        self.assertEqual(len(rendered_groups), 1)
        self.assertEqual(len(sections["scope"]), 2)
        self.assertIn("CH A", next(iter(rendered_groups)))
        self.assertIn("CH B", next(iter(rendered_groups)))

    def test_ipos_refinement_grouping_is_bounded_and_preserves_provenance(self):
        rows = [
            {"mapped_block": "Block A", "source_req_id": "ONE", "requirement_statement": "The user shall select the active channel, in this case CH_A_SEL."},
            {"mapped_block": "Block A", "source_req_id": "TWO", "requirement_statement": "The user shall select the active channel, in this case CH_B_SEL."},
            {"mapped_block": "Block A", "source_req_id": "THREE", "requirement_statement": "The controller shall write processed results to the output buffer."},
        ]
        sections, audit = compose_ipos_overview(build_ipos_functional_input(
            "Block A", {"Function": "Process sampled data", "Inputs": "configuration settings", "Outputs": "processed results and output buffer"}, rows,
        ))
        accepted = [row for row in audit if row.get("decision") == "accepted_candidate"]
        self.assertLess(len(sections["scope"]) - 1, len(accepted))
        selection_rows = [row for row in accepted if row["candidate_evidence_requirement_id"] in {"ONE", "TWO"}]
        self.assertEqual({row["summary_group_id"] for row in selection_rows}, {"local-scope-01"})
        self.assertTrue(all(row["rendered_summary"].startswith("**Local configuration.") for row in selection_rows))
        self.assertTrue(all(row["candidate_evidence_requirement_id"] in row["summary_group_contributor_ids"] for row in accepted))

    def test_ipos_refinement_grouping_keeps_distinct_actions_separate(self):
        rows = [
            {"mapped_block": "Block A", "source_req_id": "SAMPLE", "requirement_statement": "The controller shall sample incoming data."},
            {"mapped_block": "Block A", "source_req_id": "WRITE", "requirement_statement": "The controller shall write processed results to the output buffer."},
        ]
        sections, _audit = compose_ipos_overview(build_ipos_functional_input(
            "Block A", {"Function": "Acquire and process incoming data", "Inputs": "incoming data", "Outputs": "processed results and output buffer"}, rows,
        ))
        self.assertTrue(any(entry.startswith("**Local data processing.") for entry in sections["scope"]))
        self.assertTrue(any(entry.startswith("**Operation control and data routing.") for entry in sections["scope"]))

    def test_ipos_refinement_groups_source_exact_fsm_macro_subfunctions(self):
        rows = [
            {
                "mapped_block": "Block A", "source_req_id": "DEVICE",
                "requirement_statement": "When Device_FSM FSM is active, the controller shall control sampled data.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "ELAB",
                "requirement_statement": "When ELAB_FSM is active, the controller shall process sampled data.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "ADC",
                "requirement_statement": "When ADC_Phases is active, the ADC start signal shall stay high.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "PPG",
                "requirement_statement": "When PPG_FSM is active, the PPG output shall be high.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "PPG-VARIANT",
                "requirement_statement": "When PPG FSM is active, the PPG output shall be high.",
            },
        ]
        sections, audit = compose_ipos_overview(build_ipos_functional_input(
            "Block A",
            {"Function": "Control and process sampled data", "Inputs": "sampled data", "Outputs": "control state"},
            rows,
        ))
        summaries = sections["scope"][1:]
        self.assertEqual(len(summaries), 4)
        self.assertTrue(any(summary.startswith("**Device FSM.") for summary in summaries))
        self.assertTrue(any(summary.startswith("**ELAB FSM.") for summary in summaries))
        self.assertTrue(any(summary.startswith("**ADC phases.") for summary in summaries))
        self.assertEqual(sum(summary.startswith("**PPG FSM.") for summary in summaries), 1)
        self.assertTrue(all(summary.count("\n") <= 1 for summary in summaries))
        self.assertTrue(any("ADC start" in summary for summary in summaries))
        self.assertTrue(any("PPG output" in summary for summary in summaries))
        accepted = [row for row in audit if row.get("decision") == "accepted_candidate"]
        self.assertEqual(
            {row["summary_group_id"] for row in accepted},
            {"local-scope-01", "local-scope-02", "local-scope-03", "local-scope-04"},
        )
        structural_rows = [row for row in accepted if row.get("structural_facets_json")]
        self.assertTrue(all(row["structural_selected_evidence_ids"] for row in structural_rows))

    def test_structural_aggregation_uses_all_accepted_same_block_facets(self):
        rows = [
            {"mapped_block": "Block A", "source_req_id": "ONE", "requirement_statement": "When ADC_Phases is active, the controller shall start ADC sampling."},
            {"mapped_block": "Block A", "source_req_id": "TWO", "requirement_statement": "When ADC_Phases is active, the controller shall wait for i_ADC_EOC."},
        ]
        sections, audit = compose_ipos_overview(
            build_ipos_functional_input(
                "Block A", {"Function": "Control sampled data", "Inputs": "sampled data", "Outputs": "control state"}, rows,
            ),
        )
        summary = next(item for item in sections["scope"] if item.startswith("**ADC phases."))
        self.assertIn("Starts ADC sampling", summary)
        self.assertIn("ADC conversion completion", summary)
        structural = [row for row in audit if row.get("structural_entity_display") == "ADC_Phases"]
        self.assertEqual(structural[0]["structural_selected_evidence_ids"], "ONE; TWO")
        self.assertEqual([row["structural_aggregation_order"] for row in structural], ["1", "2"])

    def test_deterministic_aggregation_uses_all_accepted_entity_evidence(self):
        rows = [
            {
                "mapped_block": "Block A", "source_req_id": "ELAB-ONE",
                "requirement_statement": "When ELAB_FSM is active, the controller shall process ECG samples in PPG phase and wait for Device_FSM.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "ELAB-TWO",
                "requirement_statement": "When ELAB FSM is active, the controller shall sequence BIA samples in ECG phase.",
            },
        ]
        sections, audit = compose_ipos_overview(
            build_ipos_functional_input(
                "Block A",
                {"Function": "Process sampled data", "Inputs": "sampled data", "Outputs": "control state"},
                rows,
            ),
        )
        summary = next(item for item in sections["scope"] if item.startswith("**ELAB FSM."))
        self.assertIn("processes ECG samples", summary)
        self.assertIn("sequences BIA samples", summary)
        self.assertIn("Interacts with Device FSM", summary)
        self.assertNotIn("PPG phase", summary)
        self.assertNotIn("local acquisition and processing sequence", summary)
        self.assertNotIn("Provides", summary)
        structural = [row for row in audit if row.get("structural_entity_display") == "ELAB_FSM"]
        self.assertTrue(all(row["structural_selection_mode"] == "deterministic_aggregation" for row in structural))
        self.assertTrue(all(row["structural_selected_evidence_ids"] == "ELAB-ONE; ELAB-TWO" for row in structural))

    def test_deterministic_aggregation_reports_explicit_block_and_signal_dependencies(self):
        rows = [{
            "mapped_block": "Block A", "source_req_id": "ADC-ONE",
            "requirement_statement": "When ADC_Phases is in acquisition phase, the controller shall wait for i_ADC_EOC from the ADC block.",
        }]
        sections, _audit = compose_ipos_overview(
            build_ipos_functional_input(
                "Block A",
                {"Function": "Process sampled data", "Inputs": "sampled data", "Outputs": "control state"},
                rows,
            ),
        )
        summary = next(item for item in sections["scope"] if item.startswith("**ADC phases."))
        self.assertIn("Interacts with ADC block", summary)
        self.assertNotIn("i_ADC_EOC", summary)

    def test_aggregation_merges_channel_setup_with_measurement_start_and_omits_interaction_filler(self):
        rows = [
            {
                "mapped_block": "Block A", "source_req_id": "CONFIG",
                "requirement_statement": "The user shall select ECG0, BIA, GSR, PPG, and ECG1 ECG2 channels and Data Storage Mode.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "START",
                "requirement_statement": "The user shall start measurement.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "GSR-AVG",
                "requirement_statement": "The average block shall perform the average on 16 sample acquisition for GSR.",
            },
        ]
        sections, _audit = compose_ipos_overview(
            build_ipos_functional_input(
                "Block A",
                {"Function": "Control measurements", "Inputs": "configuration and samples", "Outputs": "measurement results"},
                rows,
            ),
        )
        summaries = [item for item in sections["scope"] if item.startswith("**")]
        setup = next(item for item in summaries if item.startswith("**Measurement setup and initiation."))
        averaging = next(item for item in summaries if "16 samples for GSR" in item)
        self.assertIn("ECG0", setup)
        self.assertIn("Data Storage Mode", setup)
        self.assertIn("then starts measurement", setup)
        self.assertNotIn("No direct dependency", "\n".join(summaries))
        self.assertNotIn("Local configuration.", "\n".join(summaries))
        self.assertNotIn("Operation control and data routing.", "\n".join(summaries))
        self.assertIn("Averages 16 samples for GSR", averaging)

    def test_approved_gsr_formula_and_cds_averages_remain_in_summary(self):
        rows = [
            {"mapped_block": "Block A", "source_req_id": "INTERVAL", "requirement_statement":
             "The i_m_sensor shall define how many time slots pass between two sensor acquisitions following this formula: sensor_data = time_slot 2 * m_sensor"},
            {"mapped_block": "Block A", "source_req_id": "CDS", "requirement_statement":
             "If en_sensor_cds is set high the SENSOR_SNS and SENSOR_CDS shall be sampled 16 times, then mediated to get one value for each of them, and then the final result shall be the subtraction between SENSOR_SNS and SENSOR_CDS."},
            {"mapped_block": "Block A", "source_req_id": "AVERAGE", "requirement_statement":
             "The average block shall perform the average on 16 sample acquisition for sensor."},
        ]
        sections, audit = compose_ipos_overview(build_ipos_functional_input(
            "Block A", {"Function": "Control sensor acquisition", "Inputs": "configuration and samples", "Outputs": "measurement results"}, rows,
        ))
        summary = " ".join(sections["scope"]).casefold()
        for meaning in ("time slots between two sensor acquisitions", "without resolving its arithmetic",
                        "16 acquisitions of sensor sns and sensor cds", "subtracts their averaged values",
                        "16 samples for sensor"):
            self.assertIn(meaning, summary)
        self.assertEqual(
            {row["candidate_evidence_requirement_id"] for row in audit if row.get("decision") == "accepted_candidate"},
            {"INTERVAL", "CDS", "AVERAGE"},
        )

    def test_approved_procedure_name_is_not_reduced_to_following_steps(self):
        statement = (
            "To perform a SOFT Reset procedure, the user shall perform the following steps: "
            "1. If Mode Operation has been set to 1, reset it to 0 "
            "2. Set the Soft Reset bit to 0 for at least 1 ms "
            "3. Set the Soft Reset bit to 1 "
            "4. Wait for Device Status to reach IDLE"
        )
        sections, audit = compose_ipos_overview(build_ipos_functional_input(
            "Block A", {"Function": "Control reset", "Inputs": "reset settings", "Outputs": "device status"},
            [{"mapped_block": "Block A", "source_req_id": "RESET", "requirement_statement": statement}],
        ))
        candidate = next(row for row in audit if row.get("candidate_evidence_requirement_id") == "RESET")
        self.assertEqual(candidate["decision"], "accepted_candidate")
        self.assertEqual(candidate["materialization_status"], "suppressed_atomic")
        self.assertNotIn("following steps", " ".join(sections["scope"]).casefold())
        self.assertEqual(candidate["candidate_evidence_statement"], statement)

    def test_prose_before_table_and_explicit_clamp_remain_eligible(self):
        rows = [
            {"mapped_block": "Block A", "source_req_id": "PPG", "requirement_statement":
             "Once the PPG Raw Data and PPG Noise reach the average value, depending on the ALC Mask bit value, the two accumulated shall be subtracted and final results shall be computed as follow: Table 18: PPG Result Table"},
            {"mapped_block": "Block A", "source_req_id": "FRAMES", "requirement_statement":
             "After the last repetition has been accumulated, the data output shall be obtained dividing by the number of repeated frames the accumulated data to obtain a 20 bit data. Table 20: Frame results"},
            {"mapped_block": "Block A", "source_req_id": "CLAMP", "requirement_statement":
             "If the user set a value greater than 1024 into ones of the m_channel, the value shall clamp at 1024 (check the input i_m_ecg"},
        ]
        sections, audit = compose_ipos_overview(build_ipos_functional_input(
            "Block A", {"Function": "Process PPG and frame data", "Inputs": "configuration and sampled data", "Outputs": "results"}, rows,
        ))
        summary = " ".join(sections["scope"]).casefold()
        for meaning in ("ppg raw data and ppg noise", "alc mask", "number of repetitions", "20-bit", "1024"):
            self.assertIn(meaning, summary)
        self.assertEqual(
            {row["candidate_evidence_requirement_id"] for row in audit if row.get("decision") == "accepted_candidate"},
            {"PPG", "FRAMES", "CLAMP"},
        )

    def test_explicit_ordered_state_progression_is_not_lost(self):
        statement = (
            "When wave velocity mode is selected and the device FSM is in WAIT_SU, "
            "the Elaboration FSM shall go into the TIMER BUFFER State and then into the PPG ALC STORAGE"
        )
        sections, audit = compose_ipos_overview(build_ipos_functional_input(
            "Block A", {"Function": "Control PPG elaboration", "Inputs": "wave velocity mode", "Outputs": "control state"},
            [{"mapped_block": "Block A", "source_req_id": "TRANSITION", "requirement_statement": statement}],
        ))
        candidate = next(row for row in audit if row.get("candidate_evidence_requirement_id") == "TRANSITION")
        self.assertEqual(candidate["decision"], "accepted_candidate")
        self.assertEqual(candidate["materialization_status"], "suppressed_atomic")
        self.assertNotIn("TIMER BUFFER then PPG ALC STORAGE".casefold(), " ".join(sections["scope"]).casefold())

    def test_orphaned_ppg_handoff_does_not_become_a_standalone_function(self):
        statement = (
            "When in ALC Compensation, the PPG shall wait that the rise of "
            "i_end_compensation signal from the ALC Compensation block to go into "
            "the RX_Start_UP state. This shall happen in OPERATIVE."
        )
        sections, audit = compose_ipos_overview(build_ipos_functional_input(
            "Block A", {"Function": "Control PPG", "Inputs": "PPG samples", "Outputs": "PPG state"},
            [{"mapped_block": "Block A", "source_req_id": "HANDOFF", "requirement_statement": statement}],
        ))
        candidate = next(row for row in audit if row.get("candidate_evidence_requirement_id") == "HANDOFF")
        self.assertEqual(candidate["materialization_status"], "suppressed_atomic")
        self.assertNotIn("handoff", " ".join(sections["scope"]).casefold())

    def test_state_entry_does_not_fold_prior_state_into_destination(self):
        from workflow_routing import _ipos_refinement_parts

        statement = (
            "When only GSR is selected, if i_m_gsr is greater than 0, the Device FSM "
            "shall go in SLEEP after the IDLE State and shall go back in Operative State "
            "only when the measurement runs."
        )
        action, destination, _qualifier, _negative = _ipos_refinement_parts(statement)
        self.assertNotIn("SLEEP after the IDLE", destination)
        self.assertNotIn("Operative state", destination)

    def test_return_from_sleep_keeps_following_guard(self):
        from workflow_routing import _ipos_refinement_parts

        statement = (
            "When in Sleep Mode, the device shall go back to the Operative State "
            "if no error (o_error_irq stuck at 0) occurs and all the operations are ended."
        )
        action, destination, _qualifier, _negative = _ipos_refinement_parts(statement)
        self.assertEqual(action, "enter")
        self.assertIn("Operative state when in Sleep Mode if no error", destination)
        self.assertIn("all the operations are ended", destination)
        self.assertNotIn("the device if", destination)

    def test_control_effects_preserve_condition_reset_and_timed_step(self):
        rows = [
            {"mapped_block": "Block A", "source_req_id": "FLAG", "requirement_statement":
             "In case the samples are equal to 0x8000 or 0x7FFF for at least half of the selected average, "
             "o_saturation_flag shall be set to 1 and shall go to 0 at the start of the next frame or frame repetition."},
            {"mapped_block": "Block A", "source_req_id": "CLOCK", "requirement_statement":
             "When ECG, BIA or GSR is sampled, i_ADC_en is equal to 1, the o_ADC_clk_en shall be set to 1."},
            {"mapped_block": "Block A", "source_req_id": "GSR", "requirement_statement":
             "If en_gsr_cds is set low [bit 3 of GSR_CTRL], the gsr_curr_on shall set high in every time slot"},
            {"mapped_block": "Block A", "source_req_id": "STEP", "requirement_statement":
             "When the input signal o_Tx_preset is set to 1, the o_Tx_Vref shall increment the first step "
             "at value i_N_start at a time i_T_preset."},
        ]
        sections, audit = compose_ipos_overview(build_ipos_functional_input(
            "Block A", {"Function": "Control sampling and outputs", "Inputs": "samples and timing control", "Outputs": "control state and data"}, rows,
        ))
        summary = " ".join(sections["scope"]).casefold()
        for meaning in ("saturation flag", "at least half", "clears at the start of the next frame",
                        "adc clk en", "ecg, bia or gsr is sampled", "gsr curr on", "every time slot",
                        "tx vref", "n start", "t preset"):
            self.assertIn(meaning, summary)
        self.assertEqual(
            {row["candidate_evidence_requirement_id"] for row in audit if row.get("decision") == "accepted_candidate"},
            {"FLAG", "CLOCK", "GSR", "STEP"},
        )
        summaries = {row["candidate_evidence_requirement_id"]: row["rendered_summary"] for row in audit if row.get("decision") == "accepted_candidate"}
        self.assertNotEqual(summaries["FLAG"], summaries["CLOCK"])

    def test_structural_summary_does_not_split_a_state_path_list(self):
        from workflow_routing import _ipos_structural_aggregate_summary

        members = [{"candidate_evidence_requirement_id": "PPG", "candidate_evidence_statement":
                    "When PPG_FSM is in Measurement state, it shall stay in this state until the rise of i_end_average. "
                    "When PPG_FSM is in Rising Ramp state, it shall stay until Rising Time ends. "
                    "When PPG_FSM is in Falling Ramp state, it shall stay until Falling Time ends. "
                    "When PPG_FSM is in SECOND ALC SAMPLES state, it shall wait for ADC completion."}]
        summary, _facets, _reason = _ipos_structural_aggregate_summary("PPG_FSM", members)
        self.assertNotIn("\n  SECOND ALC SAMPLES paths.", summary)

    def test_aggregation_device_lifecycle_and_elaboration_summary_keep_all_paths_and_relations(self):
        rows = [
            {
                "mapped_block": "Block A", "source_req_id": "DEVICE-BOOT",
                "requirement_statement": "When Device_FSM is in BOOT state, it shall wait for i_quokka_boot_end and then go to IDLE state, with clock generated from Clock generator block.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "DEVICE-OPERATIVE",
                "requirement_statement": "When Device_FSM is in IDLE state, it shall enter WAIT_SU state and OPERATIVE state.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "DEVICE-SLEEP-ERROR",
                "requirement_statement": "When Device_FSM is in OPERATIVE state, it shall enter SLEEP state and ERROR state, and raise o_error_time_slot to Digital_Top when the time slot expires.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "ELAB-ECG",
                "requirement_statement": "When ELAB_FSM is in ECG state, it shall process ECG samples and set ADC_Mux output for ADC PHASE acquisition.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "ELAB-PPG",
                "requirement_statement": "When ELAB_FSM is in PPG state, it shall wait for PPG_START_UP_TIME and start PPG operation for the selected frame.",
            },
            {
                "mapped_block": "Block A", "source_req_id": "ELAB-BIA",
                "requirement_statement": "When ELAB_FSM is in BIA state, it shall sequence BIA samples and enable ADC acquisition.",
            },
        ]
        sections, _audit = compose_ipos_overview(
            build_ipos_functional_input(
                "Block A",
                {"Function": "Control local measurements", "Inputs": "configuration and samples", "Outputs": "measurement data"},
                rows,
            ),
        )
        device = next(item for item in sections["scope"] if item.startswith("**Device FSM."))
        elaboration = next(item for item in sections["scope"] if item.startswith("**ELAB FSM."))
        device_casefold = device.casefold()
        for state in ("Boot", "Idle", "start-up", "Operative", "Sleep", "Error"):
            self.assertIn(state.casefold(), device_casefold)
        self.assertIn("ADSP boot completion", device)
        self.assertIn("Digital Top error interrupt", device)
        self.assertIn("ECG", elaboration)
        self.assertIn("BIA", elaboration)
        self.assertIn("PPG", elaboration)
        self.assertIn("ADC phase acquisition", elaboration)
        self.assertIn("PPG operation control", elaboration)
        self.assertNotIn("i_quokka_boot_end", device)
        self.assertNotIn("ADC_Mux", elaboration)

    def test_aggregation_responsibility_keeps_all_accepted_action_phrases(self):
        summary = _ipos_aggregate_responsibility(
            [
                "Processes ECG samples",
                "Sequences BIA samples",
                "Starts PPG operation",
                "Enables ADC acquisition",
            ],
            [],
        )
        for phrase in ("Processes ECG samples", "sequences BIA samples", "starts PPG operation", "Enables ADC acquisition"):
            self.assertIn(phrase.casefold(), summary.casefold())

    def test_structural_aggregation_renders_supported_responsibility_without_interaction(self):
        rows = [{
            "mapped_block": "Block A", "source_req_id": "ELAB-ONE",
            "requirement_statement": "When ELAB_FSM is active, the controller shall process sampled data.",
        }]
        sections, audit = compose_ipos_overview(
            build_ipos_functional_input(
                "Block A",
                {"Function": "Process sampled data", "Inputs": "sampled data", "Outputs": "control state"},
                rows,
            ),
        )
        self.assertTrue(any(item.startswith("**ELAB FSM.") for item in sections["scope"]))
        structural = next(row for row in audit if row.get("structural_entity_display") == "ELAB_FSM")
        self.assertEqual(structural["structural_summary_status"], "selected")
        self.assertEqual(structural["structural_summary_reason"], "deterministic aggregation")

    def test_ipos_validator_rejects_requirement_expansion_and_boilerplate(self):
        rows = [
            {"mapped_block": "Block A", "source_req_id": "ONE", "requirement_statement": "The user shall select the active channel, in this case CH_A_SEL."},
            {"mapped_block": "Block A", "source_req_id": "TWO", "requirement_statement": "The user shall select the active channel, in this case CH_B_SEL."},
            {"mapped_block": "Block A", "source_req_id": "THREE", "requirement_statement": "The user shall select the active channel, in this case CH_C_SEL."},
        ]
        record = build_ipos_functional_input(
            "Block A", {"Function": "Process sampled data", "Inputs": "configuration settings", "Outputs": "processed results"}, rows,
        )
        sections, audit = compose_ipos_overview(record)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown_path = root / "ipos.md"
            audit_path = root / "descriptive_summary_audit.csv"
            markdown_path.write_text(
                "## 1. Block overview\n\n### 1.1 Functionality\n\n" + sections["functionality"][0]
                + "\n\n### 1.2 Supported functions and scope\n\n- " + sections["scope"][0]
                + "\n- Supports approved local operations.\n\n## 2. Source I/O\n", encoding="utf-8",
            )
            for index, row in enumerate(audit):
                if row.get("decision") == "accepted_candidate":
                    row["summary_group_id"] = f"expanded-{index}"
                    row["rendered_summary"] = row["candidate_refinement"]
                    row["summary_group_contributor_ids"] = row["candidate_evidence_requirement_id"]
            write_ipos_descriptive_audit(audit_path, audit)
            findings = validate_ipos_descriptive_output(
                markdown_path, audit_path, "Block A", [row["requirement_statement"] for row in rows],
                [row["source_req_id"] for row in rows], DESCRIPTIVE_DIGITAL_TOPIC_SPECS, record,
            )
        joined = " ".join(findings)
        self.assertIn("requirement_by_requirement_scope_expansion", joined)
        self.assertIn("generic_action_family_placeholder", joined)

    def test_dry_run_rejects_table_signal_cross_block_conflict_and_normative_only_evidence(self):
        inventory = {"Function": "Store incoming data", "Inputs": "incoming data", "Outputs": "output memory"}
        cases = (
            ([{"mapped_block": "Block A", "source_req_id": "TABLE", "requirement_statement": "The block shall route values as shown in the following table."}], "suppressed_due_to_table_or_signal_only_evidence"),
            ([{"mapped_block": "Block A", "source_req_id": "SIGNALS", "requirement_statement": "ECG, PPG, GSR"}], "suppressed_due_to_table_or_signal_only_evidence"),
            ([{"mapped_block": "Block B", "source_req_id": "OTHER", "requirement_statement": "The block shall store incoming data in output memory."}], "suppressed_due_to_cross_block_risk"),
            ([{"mapped_block": "Block A", "source_req_id": "NORM", "requirement_statement": "The block shall comply with its assigned parameters."}], "suppressed_due_to_normative_reuse"),
        )
        for rows, expected in cases:
            with self.subTest(expected=expected):
                record = build_ipos_functional_input("Block A", inventory, rows)
                _sections, audit = compose_ipos_overview(record)
                candidate = next(item for item in audit if item.get("candidate_evidence_statement"))
                self.assertEqual(candidate["decision"], expected)

        bounded = build_ipos_functional_input(
            "Block A",
            {"Function": "Acquire incoming data", "Inputs": "incoming data", "Outputs": "status"},
            [{"mapped_block": "Block A", "source_req_id": "BOUNDED", "requirement_statement": "The block shall sample incoming data."}],
        )
        bounded_sections, bounded_audit = compose_ipos_overview(bounded)
        bounded_candidate = next(item for item in bounded_audit if item.get("candidate_evidence_statement"))
        self.assertEqual(bounded_candidate["decision"], "accepted_candidate")
        self.assertIn(bounded_candidate["rendered_summary"], bounded_sections["scope"])

        conflict_rows = [
            {"mapped_block": "Block A", "source_req_id": "POS", "requirement_statement": "The block shall store incoming data in output memory."},
            {"mapped_block": "Block A", "source_req_id": "NEG", "requirement_statement": "The block shall not store incoming data in output memory."},
        ]
        _sections, conflict_audit = compose_ipos_overview(build_ipos_functional_input("Block A", inventory, conflict_rows))
        self.assertEqual(
            {item["decision"] for item in conflict_audit if item.get("candidate_evidence_statement")},
            {"suppressed_due_to_conflict"},
        )

    def test_conditional_passive_set_retains_functional_effect_and_transition(self):
        inventory = {"Function": "Control acquisition", "Inputs": "sampled data", "Outputs": "control state"}
        statement = (
            "When in FIRST_SAMPLES state, when i_end_average is set to 1, "
            "the o_start_ramp signal shall be set high to start the rising of the ramp "
            "and go into the RISING_RAMP state."
        )
        record = build_ipos_functional_input(
            "Block A", inventory,
            [{"mapped_block": "Block A", "source_req_id": "TRANSITION", "requirement_statement": statement},
             {"mapped_block": "Block A", "source_req_id": "BARE", "requirement_statement":
              "When in READY state, when i_go is set to 1, the o_flag signal shall be set high."}],
        )
        sections, audit = compose_ipos_overview(record)
        transition = next(item for item in audit if item.get("candidate_evidence_requirement_id") == "TRANSITION")
        bare = next(item for item in audit if item.get("candidate_evidence_requirement_id") == "BARE")
        self.assertEqual(transition["decision"], "accepted_candidate")
        summary = transition["rendered_summary"].casefold()
        for meaning in ("rising of ramp", "rising ramp state", "end average is set to 1", "first samples state"):
            self.assertIn(meaning, summary)
        self.assertIn(transition["rendered_summary"], sections["scope"])
        self.assertEqual(bare["decision"], "suppressed_due_to_normative_reuse")

    def test_approved_acquisition_interval_survives_define_and_time_filters(self):
        inventory = {"Function": "Control acquisition", "Inputs": "configuration settings", "Outputs": "control state"}
        rows = [
            {"mapped_block": "Block A", "source_req_id": "INTERVAL", "requirement_statement":
             "The i_m_sensor [SENSOR_FREQ] shall define how many time slots pass between two sensor acquisitions following this formula: unreadable"},
            {"mapped_block": "Block A", "source_req_id": "UNSUPPORTED", "requirement_statement":
             "The block shall define the configuration."},
        ]
        sections, audit = compose_ipos_overview(build_ipos_functional_input("Block A", inventory, rows))
        interval = next(item for item in audit if item.get("candidate_evidence_requirement_id") == "INTERVAL")
        unsupported = next(item for item in audit if item.get("candidate_evidence_requirement_id") == "UNSUPPORTED")
        self.assertEqual(interval["decision"], "accepted_candidate")
        self.assertIn("time slots between two sensor acquisitions", interval["rendered_summary"])
        self.assertIn(interval["rendered_summary"], sections["scope"])
        self.assertNotIn("unreadable", " ".join(sections["scope"]))
        self.assertEqual(unsupported["decision"], "suppressed_due_to_normative_reuse")

    def test_digital_and_analog_use_identical_dry_run_classification(self):
        row = {"mapped_block": "Block A", "source_req_id": "REQ-A", "requirement_statement": "The block shall sample incoming data and store processed results."}
        inventory = {"Function": "Acquire and process incoming data", "Inputs": "incoming data", "Outputs": "processed results"}
        decisions = []
        for domain in ("digital", "analog"):
            record = build_ipos_functional_input("Block A", inventory, [row], domain=domain)
            _sections, audit = compose_ipos_overview(record)
            decisions.append((audit[-1]["decision"], audit[-1]["candidate_refinement"]))
        self.assertEqual(decisions[0], decisions[1])

    def test_global_candidate_audit_keeps_cross_block_evidence_suppressed(self):
        local_row = {
            "mapped_block": "Block A", "source_req_id": "REQ-A",
            "requirement_statement": "The controller shall sample incoming data and store processed results in the local output buffer.",
        }
        other_block_row = {
            "mapped_block": "Block B", "source_req_id": "REQ-B",
            "requirement_statement": "The controller shall sample incoming data and store processed results in the local output buffer.",
        }
        candidate_rows = [local_row, other_block_row]
        record = build_ipos_functional_input(
            "Block A",
            {"Function": "Acquire and process incoming data", "Inputs": "incoming data", "Outputs": "processed results"},
            candidate_rows,
            domain="digital",
            candidate_requirement_rows=candidate_rows,
        )

        _sections, audit = compose_ipos_overview(record)
        candidates = {
            item["candidate_evidence_requirement_id"]: item
            for item in audit
            if item.get("candidate_evidence_statement")
        }

        self.assertEqual(record.local_requirement_ids, ("REQ-A",))
        self.assertEqual(candidates["REQ-A"]["decision"], "accepted_candidate")
        self.assertEqual(candidates["REQ-B"]["decision"], "suppressed_due_to_cross_block_risk")
        self.assertEqual(candidates["REQ-B"]["supporting_local_requirement_ids"], "")

    def test_shared_validator_rejects_loss_of_accepted_candidate(self):
        row = {"mapped_block": "Block A", "source_req_id": "REQ-A", "requirement_statement": "The block shall sample incoming data and store processed results."}
        record = build_ipos_functional_input(
            "Block A",
            {"Function": "Acquire and process incoming data", "Inputs": "incoming data", "Outputs": "processed results"},
            [row], provenance=("approved snapshot", "block_inventory.csv"),
        )
        sections, audit = compose_ipos_overview(record)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown_path = root / "ipos.md"
            audit_path = root / "descriptive_summary_audit.csv"
            markdown_path.write_text(
                "## 1. Block overview\n\n### 1.1 Functionality\n\n" + sections["functionality"][0]
                + "\n\n### 1.2 Supported functions and scope\n\n"
                + "\n".join("- " + item for item in sections["scope"])
                + "\n\n## 2. Source I/O\n", encoding="utf-8",
            )
            write_ipos_descriptive_audit(audit_path, audit)
            findings = validate_ipos_descriptive_output(
                markdown_path, audit_path, "Block A", [row["requirement_statement"]], ["REQ-A"],
                DESCRIPTIVE_DIGITAL_TOPIC_SPECS, record,
            )
            self.assertEqual(findings, [])
            with audit_path.open("r", encoding="utf-8", newline="") as handle:
                audit_rows = list(csv.DictReader(handle))
                fieldnames = list(audit_rows[0])
            candidate = next(item for item in audit_rows if item.get("candidate_evidence_requirement_id") == "REQ-A")
            candidate["rendered_summary"] = "**Operation control and data routing.** Starts only."
            with audit_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(audit_rows)
            findings = validate_ipos_descriptive_output(
                markdown_path, audit_path, "Block A", [row["requirement_statement"]], ["REQ-A"],
                DESCRIPTIVE_DIGITAL_TOPIC_SPECS, record,
            )
            self.assertIn("low_quality_subfunction_summary:Operation control and data routing", " ".join(findings))
            write_ipos_descriptive_audit(audit_path, audit)
            markdown_path.write_text(markdown_path.read_text(encoding="utf-8").replace(
                "- " + audit[-1]["rendered_summary"] + "\n", ""
            ), encoding="utf-8")
            findings = validate_ipos_descriptive_output(
                markdown_path, audit_path, "Block A", [row["requirement_statement"]], ["REQ-A"],
                DESCRIPTIVE_DIGITAL_TOPIC_SPECS, record,
            )
        self.assertIn("accepted_refinement_group_missing_from_rendered_scope", " ".join(findings))

    def test_ipos_validator_rejects_governance_prose_in_final_overview(self):
        record = build_ipos_functional_input(
            "Block A", {"Function": "Route samples", "Inputs": "incoming samples", "Outputs": "routed samples"},
            [], provenance=("approved snapshot",),
        )
        sections, audit = compose_ipos_overview(record)
        with tempfile.TemporaryDirectory() as directory:
            markdown_path = Path(directory) / "ipos.md"
            audit_path = Path(directory) / "descriptive_summary_audit.csv"
            write_ipos_descriptive_audit(audit_path, audit)
            for legacy_text in (
                "The block provides this approved macro-purpose: route samples.",
                "The local scope covers the approved Block A function, accepting incoming samples.",
                "The block uses approved functional evidence to route samples.",
                "The block provides approved signal handling for routed samples.",
            ):
                with self.subTest(legacy_text=legacy_text):
                    markdown_path.write_text(
                        "## 1. Block overview\n\n### 1.1 Functionality\n\n" + legacy_text
                        + "\n\n### 1.2 Supported functions and scope\n\n- " + sections["scope"][0]
                        + "\n\n## 2. Source I/O\n", encoding="utf-8",
                    )
                    findings = validate_ipos_descriptive_output(
                        markdown_path, audit_path, "Block A", [], [], DESCRIPTIVE_DIGITAL_TOPIC_SPECS, record,
                    )
                    self.assertTrue(any("description_uses_internal_process_language" in finding for finding in findings))

    def test_validator_rejects_raw_standalone_heading(self):
        statement = "The controller shall write processed results to the FIFO with a dedicated tag."
        record = build_ipos_functional_input(
            "Block A", {"Function": "Store results", "Inputs": "processed results", "Outputs": "FIFO data"},
            [{"mapped_block": "Block A", "source_req_id": "STORE", "requirement_statement": statement}],
            provenance=("approved snapshot",),
        )
        sections, audit = compose_ipos_overview(record)
        with tempfile.TemporaryDirectory() as directory:
            markdown_path = Path(directory) / "ipos.md"
            audit_path = Path(directory) / "descriptive_summary_audit.csv"
            markdown_path.write_text(
                "## 1. Block overview\n\n### 1.1 Functionality\n\n" + sections["functionality"][0]
                + "\n\n### 1.2 Supported functions and scope\n\n"
                + "\n".join("- " + item for item in sections["scope"])
                + "\n\n## 2. Source I/O\n", encoding="utf-8",
            )
            write_ipos_descriptive_audit(audit_path, audit)
            with audit_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
                fieldnames = list(rows[0])
            candidate = next(row for row in rows if row.get("candidate_evidence_requirement_id") == "STORE")
            self.assertEqual(candidate["materialization_status"], "standalone")
            candidate["rendered_summary"] = "**raw_signal_name.** Enables output when set."
            with audit_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            findings = validate_ipos_descriptive_output(
                markdown_path, audit_path, "Block A", [statement], ["STORE"],
                DESCRIPTIVE_DIGITAL_TOPIC_SPECS, record,
            )
        self.assertIn("low_quality_standalone_summary:STORE", " ".join(findings))

    def test_validator_fails_when_parser_silently_suppresses_supported_reset_behavior(self):
        statement = (
            "In case the sampled data reach the threshold, o_saturation_flag shall be set to 1 "
            "and shall go to 0 at the start of the next frame."
        )
        record = build_ipos_functional_input(
            "Block A", {"Function": "Control sampling", "Inputs": "sampled data", "Outputs": "control outputs"},
            [{"mapped_block": "Block A", "source_req_id": "FLAG", "requirement_statement": statement}],
            provenance=("approved snapshot",),
        )
        with patch("workflow_routing._ipos_refinement_candidate", return_value=""):
            sections, audit = compose_ipos_overview(record)
            with tempfile.TemporaryDirectory() as directory:
                markdown_path = Path(directory) / "ipos.md"
                audit_path = Path(directory) / "descriptive_summary_audit.csv"
                markdown_path.write_text(
                    "## 1. Block overview\n\n### 1.1 Functionality\n\n" + sections["functionality"][0]
                    + "\n\n### 1.2 Supported functions and scope\n\n"
                    + "\n".join("- " + item for item in sections["scope"])
                    + "\n\n## 2. Source I/O\n", encoding="utf-8",
                )
                write_ipos_descriptive_audit(audit_path, audit)
                findings = validate_ipos_descriptive_output(
                    markdown_path, audit_path, "Block A", [statement], ["FLAG"],
                    DESCRIPTIVE_DIGITAL_TOPIC_SPECS, record,
                )
        self.assertIn("approved_behavior_missing_from_scope:FLAG:saturation flag", " ".join(findings))

    def test_ipos_subfunction_summary_has_title_purpose_context_and_provenance(self):
        rows = [
            {"mapped_block": "Block A", "source_req_id": "SELECT", "requirement_statement": "The user shall select the active channel, in this case CH_A_SEL."},
            {"mapped_block": "Block A", "source_req_id": "WRITE", "requirement_statement": "The controller shall write processed results to the output buffer."},
        ]
        sections, audit = compose_ipos_overview(build_ipos_functional_input(
            "Block A", {"Function": "Process sampled data", "Inputs": "configuration settings and sampled data", "Outputs": "processed results and output buffer"}, rows,
        ))
        summaries = sections["scope"][1:]
        self.assertTrue(all(summary.startswith("**") and summary.count("\n") <= 1 for summary in summaries))
        self.assertTrue(all("No direct dependency" not in summary for summary in summaries))
        accepted = [row for row in audit if row.get("decision") == "accepted_candidate"]
        self.assertTrue(all(row["rendered_summary"] in summaries for row in accepted))
        self.assertTrue(all(row["candidate_evidence_requirement_id"] in row["summary_group_contributor_ids"] for row in accepted))

    def test_workflow_rule_states_end_to_end_contract_without_project_examples(self):
        rule_path = Path(__file__).resolve().parents[1] / ".github/skills/workflow-stage-gate/SKILL.md"
        text = rule_path.read_text(encoding="utf-8")
        rule_lines = text.splitlines()
        contract_start = next(index for index, line in enumerate(rule_lines) if "materialized IPOS Block Overviews" in line)
        contract = " ".join(" ".join(rule_lines[contract_start:contract_start + 16]).casefold().split())
        for required in (
            "approved snapshot", "function`, `inputs`, and `outputs", "same-block approved ipos requirement evidence",
            "acronyms alone", "signal lists alone", "i/o names alone", "tables alone", "ordered semantic units",
            "non-normative", "ownership", "responsibility", "system-level behavior", "suppressed candidate",
            "preserves its supported action and object", "generic action-family placeholder",
        ):
            self.assertIn(required, contract)
        project_vocabulary = r"main controller|smart fifo|\becg\b|\bbia\b|\bppg\b|\bgsr\b"
        self.assertNotRegex(text.casefold(), project_vocabulary)
        rule_start = next(index for index, line in enumerate(rule_lines) if "Shared IPOS refinement-audit input contract" in line)
        rule_end = next((index for index in range(rule_start + 1, len(rule_lines)) if rule_lines[index].startswith("- ")), len(rule_lines))
        shared_audit_rule = " ".join(rule_lines[rule_start:rule_end]).casefold()
        self.assertIn("identical complete candidate-requirement set", shared_audit_rule)
        self.assertIn("parity tests for both ipos domains", shared_audit_rule)

        orchestrator_path = Path(__file__).resolve().parents[1] / ".github/agents/workflow-orchestrator.agent.md"
        orchestrator = orchestrator_path.read_text(encoding="utf-8").casefold()
        self.assertNotRegex(orchestrator, project_vocabulary)
        self.assertIn("identical complete snapshot-scoped candidate-requirement set", orchestrator)
        self.assertIn("cross-block candidates are audit-only suppressed findings", orchestrator)

    def test_valid_empty_ipos_input_does_not_force_sections(self):
        record = build_ipos_functional_input(
            "Empty", {"Function": "", "Inputs": "", "Outputs": ""}, materialized=False
        )
        sections, audit = compose_ipos_overview(record)
        self.assertEqual(sections["functionality"], [])
        self.assertEqual(sections["scope"], [])
        self.assertEqual(audit, [])

    def test_ipos_scope_validator_rejects_content_outside_evidence_projection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown_path = root / "ipos.md"
            audit_path = root / "descriptive_summary_audit.csv"
            markdown_path.write_text(
                "## 1. Block overview\n\n"
                "### 1.2 Supported functions and scope\n\n"
                "- **SPI handling:** Supports serial-interface transactions.\n\n"
                "## 2. Source I/O\n",
                encoding="utf-8",
            )
            empty_assembly = assemble_descriptive_summary(
                [], DESCRIPTIVE_DIGITAL_TOPIC_SPECS, include_general=False,
                summary_only=True, ipos_topic_mode=True,
            )
            write_descriptive_audit(audit_path, empty_assembly, section="IPOS overview")
            findings = validate_ipos_descriptive_output(
                markdown_path, audit_path, "Control Block",
                ["The block controls I2C transactions."], [],
                DESCRIPTIVE_DIGITAL_TOPIC_SPECS,
            )
        self.assertTrue(any("does not match the deterministic projection" in finding for finding in findings))

    def test_normative_evidence_is_retained_as_descriptive_provenance(self):
        assembly = assemble_descriptive_summary(
            [{"statement": "The controller shall enter standby state.", "source": "approved:req-1"}],
            DESCRIPTIVE_MODE_TOPIC_SPECS,
        )
        self.assertIn("Modes and transitions", assembly.topics)
        self.assertNotIn("approved:req-1", assembly.topics["Modes and transitions"][0])
        self.assertNotIn("(source=", assembly.topics["Modes and transitions"][0])
        self.assertEqual(assembly.audit[0]["normative_evidence"], "yes")
        self.assertEqual(assembly.audit[0]["decision"], "selected")
        self.assertNotIn("Approved evidence:", assembly.topics["Modes and transitions"][0])
        self.assertNotIn("(source=", assembly.topics["Modes and transitions"][0])
        self.assertEqual(assembly.audit[0]["source"], "approved:req-1")

    def test_duplicate_and_limit_decisions_are_audited(self):
        records = [
            {"statement": "Standby mode uses a clock.", "source": "a"},
            {"statement": "Standby mode uses a clock.", "source": "a"},
            {"statement": "Sleep mode uses a clock.", "source": "b"},
        ]
        assembly = assemble_descriptive_summary(
            records, DESCRIPTIVE_MODE_TOPIC_SPECS, max_items_per_topic=1
        )
        reasons = [row["reason"] for row in assembly.audit]
        self.assertIn("duplicate descriptive evidence", reasons)
        self.assertIn("topic output limit", reasons)
        self.assertEqual(len(assembly.topics["Modes and transitions"]), 1)

    def test_empty_topics_are_omitted_by_default(self):
        assembly = assemble_descriptive_summary(
            [{"statement": "A calibration reference exists.", "source": "approved:context"}],
            DESCRIPTIVE_POWER_TOPIC_SPECS,
            include_general=False,
        )
        self.assertNotIn("Power states and sequencing", assembly.topics)
        self.assertEqual(assembly.topics, {})

    def test_power_domain_categories_use_approved_descriptive_signals(self):
        assembly = assemble_descriptive_summary(
            [
                {"statement": "The retention domain preserves register state when the main logic is powered down.", "source": "approved:power-1"},
                {"statement": "The power domain is enabled after the supply rail is stable.", "source": "approved:power-2"},
            ],
            DESCRIPTIVE_POWER_TOPIC_SPECS,
            include_general=False,
        )
        self.assertIn("Supply-Domain Relationships", assembly.topics)
        self.assertIn("Retention, Standby, Sleep, and Active Behavior", assembly.topics)
        self.assertTrue(all("Approved evidence:" not in item for items in assembly.topics.values() for item in items))
        self.assertEqual({row["source"] for row in assembly.audit if row["decision"] == "selected"}, {"approved:power-1", "approved:power-2"})

    def test_audit_is_reproducible_and_reviewable(self):
        records = [
            {"statement": "The power domain supports retention.", "source": "approved:req-2"},
            {"statement": "The block contains shared memory.", "source": "approved:block-1"},
        ]
        first = assemble_descriptive_summary(records, DESCRIPTIVE_POWER_TOPIC_SPECS)
        second = assemble_descriptive_summary(records, DESCRIPTIVE_POWER_TOPIC_SPECS)
        self.assertEqual(first, second)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.csv"
            write_descriptive_audit(path, first, section="Power States")
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["section"], "Power States")
            self.assertIn("assignment_reason", rows[0])
            self.assertIn("output_order", rows[0])

    def test_ipos_topic_assignment_uses_functional_evidence_not_provenance(self):
        assignment = assign_ipos_descriptive_topic(
            "The controller sequences clock reset release and power-island enable.",
            DESCRIPTIVE_DIGITAL_TOPIC_SPECS,
        )
        self.assertEqual(assignment["topic"], "Power and clock islands")
        metadata_only = assemble_descriptive_summary(
            [{
                "summary": "Metadata-only entry",
                "statement": "Metadata-only entry",
                "source": "power clock island provenance",
                "functional_evidence": "",
            }],
            DESCRIPTIVE_DIGITAL_TOPIC_SPECS,
            include_general=False,
            summary_only=True,
            ipos_topic_mode=True,
        )
        self.assertEqual(metadata_only.topics, {})
        self.assertEqual(metadata_only.audit[0]["reason"], "no functional topic evidence")

    def test_ipos_topic_assignment_omits_ambiguous_functional_evidence(self):
        assembly = assemble_descriptive_summary(
            [{
                "summary": "Ambiguous entry",
                "statement": "Ambiguous entry",
                "source": "approved provenance",
                "functional_evidence": "clock reset",
            }],
            (("Clock", ("clock",)), ("Reset", ("reset",))),
            include_general=False,
            summary_only=True,
            ipos_topic_mode=True,
        )
        self.assertEqual(assembly.topics, {})
        self.assertEqual(assembly.audit[0]["reason"], "ambiguous functional topic evidence")

    def test_low_power_assembly_is_scope_filtered_and_config_driven(self):
        repo_root = Path(__file__).resolve().parents[1]
        grouped, audit = assemble_low_power_descriptive(
            [
                {
                    "statement": "The retention domain preserves register state when the main logic is powered down.",
                    "source": "approved:architecture",
                    "scope": "architecture",
                    "domain": "system",
                },
                {
                    "statement": "Ultra-low-power hardware is a state-of-the-art feature.",
                    "source": "approved:marketing",
                    "scope": "architecture",
                    "domain": "system",
                },
                {
                    "statement": "The analog bias domain enters sleep and restores on wake-up.",
                    "source": "approved:analog",
                    "scope": "architecture",
                    "domain": "analog",
                },
            ],
            repo_root=repo_root,
            profile="srs",
        )
        self.assertIn("Power-domain architecture", grouped)
        self.assertNotIn("Ultra-low-power hardware is a state-of-the-art feature.", grouped["Power-domain architecture"])
        self.assertEqual(
            next(row["reason"] for row in audit if row["source"] == "approved:marketing"),
            "excluded phrase: state-of-the-art feature",
        )
        self.assertEqual(
            next(row["reason"] for row in audit if row["source"] == "approved:analog"),
            "eligible descriptive evidence",
        )

    def test_low_power_domain_scope_excludes_block_local_drs_evidence(self):
        repo_root = Path(__file__).resolve().parents[1]
        grouped, audit = assemble_low_power_descriptive(
            [{"statement": "The retention domain preserves state.", "source": "block-local", "scope": "block_local", "domain": "digital"}],
            repo_root=repo_root,
            profile="drs",
        )
        self.assertEqual(grouped, {})
        self.assertEqual(audit[0]["reason"], "scope not allowed")

    def test_drs_top_level_predicate_rejects_block_local_evidence(self):
        self.assertFalse(is_drs_top_level_record({"scope": "block_local", "domain": "digital"}))
        self.assertTrue(is_drs_top_level_record({"scope": "integration", "domain": "digital"}))

    def test_function_rows_preserve_system_scope_and_reject_block_scope(self):
        records = architecture_records_from_function_rows([
            (
                "The retention domain preserves register state when powered down.",
                "architecture_function; source=Section 10.2, paragraph 011 (page 32)",
                "System",
            ),
            (
                "The local block enters retention mode.",
                "architecture_function; source=Section 17.2, paragraph 052 (page 157)",
                "BIST Controller",
            ),
        ])
        self.assertEqual(records[0]["scope"], "architecture")
        self.assertEqual(records[0]["source"], "Section 10.2, paragraph 011 (page 32)")
        self.assertEqual(records[1]["scope"], "block_local")

    def test_selected_low_power_audit_is_the_only_downstream_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "descriptive_low_power_audit.csv"
            write_low_power_audit(path, [
                {
                    "decision": "selected",
                    "statement": "The power domain can be powered independently.",
                    "source": "Section 10.2",
                    "scope": "architecture",
                    "domain": "system",
                },
                {
                    "decision": "rejected",
                    "statement": "The local block enters retention.",
                    "source": "Section 17.2",
                    "scope": "block_local",
                    "domain": "BIST Controller",
                },
            ])
            records = read_selected_low_power_audit(path)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["scope"], "architecture")
        self.assertEqual(records[0]["source"], "Section 10.2")

    def test_power_domain_evidence_preserves_names_attributes_and_provenance(self):
        records = power_domain_records_from_ocr(Path(__file__).resolve().parents[1])
        combined = "\n".join(row["statement"] for row in records)
        self.assertIn("PD_TOP1V2", combined)
        self.assertIn("PD_STREDL", combined)
        self.assertIn("PD_TOP3V3", combined)
        self.assertIn("OTP memory block", combined)
        self.assertNotIn("PUMP_85AL05_2: Included block(s)", combined)
        self.assertNotIn("ca_fifo_bist_c", combined)
        self.assertNotIn("ca_qk_bist_c", combined)
        self.assertNotIn("ca_qk_rom_bist", combined)
        self.assertNotIn("ta_afe_bist_ctrl", combined)
        self.assertNotIn("u_ca_fifo_bist_c", combined)
        self.assertIn("Switchable", combined)
        self.assertIn("Never powered down", combined)
        self.assertTrue(all("Stage 1 OCR power-domain" in row["source"] for row in records))

    def test_version_history_and_signal_level_rows_are_rejected(self):
        grouped, audit = assemble_low_power_descriptive(
            [
                {"statement": "Version History: added Power Domain.", "source": "Section 0.1 Version History", "scope": "architecture", "domain": "system"},
                {"statement": "ca_stredl_bist_c_sif_reg_e enables a local test path.", "source": "Section 18", "scope": "architecture", "domain": "system"},
            ],
            repo_root=Path(__file__).resolve().parents[1],
            profile="srs",
        )
        self.assertEqual(grouped, {})
        self.assertIn("excluded phrase: version history", [row["reason"] for row in audit])
        self.assertIn("signal-level detail not eligible for top-level descriptive text", [row["reason"] for row in audit])

    def test_srs_low_power_renderer_has_one_domain_section_and_clarifies_missing_sequence(self):
        lines = []
        _render_srs_low_power_section(
            lines,
            [{"statement": "PD_STREDL: Domain type: Switchable. Control mode: SW.", "source": "approved", "scope": "architecture", "domain": "power", "evidence_kind": "power_domain"}],
            repo_root=Path(__file__).resolve().parents[1],
        )
        rendered = "\n".join(lines)
        self.assertEqual(rendered.count("#### Power-domain architecture"), 1)
        self.assertIn("Entry / power-up:", rendered)
        self.assertIn("Wake-up / restore:", rendered)
        self.assertIn("no retention, state-restore, or wake-up timing is specified", rendered)


if __name__ == "__main__":
    unittest.main()
