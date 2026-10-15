"""Collect review-only specification issues without changing authority or gates."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import generate_ipos_specs as ipos
from spec_document_contract import PUBLICATION_REVIEW_MARKERS, drs_document_events
from workflow_routing import (
    approved_snapshot_candidate_rows, build_ipos_claim_plan,
    build_ipos_functional_input, ipos_claim_preflight_findings,
    retrieve_descriptive_identifier_support, IPOS_DESCRIPTIVE_PROFILE,
    _ipos_evidence_semantic_findings, _ipos_top_level_modals,
    _ipos_comma_less_guard_boundary, _ipos_source_text,
    DESCRIPTIVE_OBLIGATION_POLICY_VERSION,
)


CONCLUSIONS = frozenset({
    "Need clarification", "Functionality not clear from approved source",
    "Source-model relationship needs review", "Structured evidence not sufficiently recoverable",
    "Candidate clarification proposal for user review",
    "No source clarification needed", "Report-only observation", "Artifact alignment required",
})
PUBLICATION_MARKERS = re.compile(
    r"\b(?:need clarification|requires? clarification|not specified|not described|"
    r"TBD-\d+|insufficient|unresolved)\b", re.I,
)
DOCUMENTS = {
    "3": ("SRS", "stage3_srs", "system_requirements_specification.md"),
    "4": ("ARS", "stage4_ars", "analog_requirements_specification.md"),
    "5": ("DRS", "stage5_drs", "digital_requirements_specification.md"),
}


def issue(document_type, location, references, blocker_class, explanation, sources):
    conclusion = "Need clarification"
    if "relationship_changed" in blocker_class:
        conclusion = "Source-model relationship needs review"
    elif "structured/table/procedure" in blocker_class:
        conclusion = "Structured evidence not sufficiently recoverable"
    return {
        "document_type": document_type, "location": location,
        "requirement_or_context_references": list(references),
        "blocker_class": blocker_class, "explanation": explanation,
        "source_references": list(sources), "conclusion": conclusion,
        "user_review_only": True,
    }


def collect_csv_issues(path, document_type, repo_root):
    findings = []
    relative = path.relative_to(repo_root).as_posix()
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for index, row in enumerate(csv.DictReader(handle), 1):
            decision = row.get("decision", "").strip()
            if decision in {"selected", "retained", "preserved"}:
                continue
            reference = f"{relative}:data-record:{index}"
            references = [row[key] for key in ("source_record_id", "source_req_id", "fact_id", "unit_id")
                          if row.get(key)] or [reference]
            sources = [reference, *[row[key] for key in ("source", "source_evidence") if row.get(key)]]
            finding = issue(document_type, row.get("section") or row.get("topic") or relative,
                            references, "audit_" + (decision or "unclassified"),
                            row.get("reason") or "Audit contributor has no rendered disposition.", sources)
            finding["audit_decision"] = decision
            finding["source_excerpt"] = row.get("statement", "")
            findings.append(finding)
    return findings


def collect_publication_issues(path, document_type, repo_root, source_ids):
    findings = []
    section = "Document"
    relative = path.relative_to(repo_root).as_posix()
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("#"):
            section = line.lstrip("# ").strip()
            continue
        if not PUBLICATION_MARKERS.search(line):
            continue
        references = [identity for identity in source_ids
                      if re.search(r"(?<![\w-])" + re.escape(identity) + r"(?![\w-])", line)]
        findings.append(issue(document_type, f"{section}; line {number}", references or [f"{relative}#L{number}"],
                              "inline_review_or_uncertainty_marker",
                              "Rendered text contains a review or uncertainty marker; it does not meet the requested clean-publication constraint.",
                              [f"{relative}#L{number}"]))
        findings[-1]["rendered_excerpt"] = line
    return findings


def collect_plan_disposition_issues(plan, document_type, block):
    records = {record.record_id: record for record in plan.evidence.records}
    covered = {(context.reason, context.spans) for context in plan.evidence.unresolved_contexts}
    findings = []
    for disposition in plan.dispositions:
        if disposition.decision == "preserved" or (disposition.reason, disposition.spans) in covered:
            continue
        finding = issue(document_type, f"{block}: descriptive disposition",
                        disposition.proposition_ids or tuple(span.record_id for span in disposition.spans),
                        disposition.reason,
                        "The shared claim plan did not preserve this descriptive contribution: " + disposition.decision + ".",
                        [value for span in disposition.spans for value in records[span.record_id].provenance])
        finding["disposition"] = disposition.decision
        finding["source_spans"] = [{"record_id": span.record_id, "start": span.start, "end": span.end, "text": span.text}
                                   for span in disposition.spans]
        findings.append(finding)
    return findings


def observe_ipos_block_publication(repo_root, domain, block, snapshot_id, run_start, *, require_run_freshness=True):
    folder = repo_root / ipos.CONFIG[domain]["output_dir"] / "blocks" / ipos._block_slug(block)
    markdown = folder / ipos._block_markdown_name(domain, block)
    artifacts = (markdown, markdown.with_suffix(".docx"))
    if any(not path.is_file() or (require_run_freshness and path.stat().st_mtime < datetime.fromisoformat(run_start).timestamp())
           for path in artifacts):
        return {"publication_status": "NOT_REGENERATED_IN_THIS_RUN"}
    command = [sys.executable, "-B", str(repo_root / "scripts/validate_ipos_gate.py"),
               "--kind", domain, "--snapshot-id", snapshot_id, "--block", block]
    result = subprocess.run(command, cwd=repo_root, capture_output=True, text=True, check=False)
    state = {"publication_status": "FAIL_EXISTING_BLOCK_GATE" if result.returncode else "PASS",
             "validation_command": command, "validation_exit_code": result.returncode,
             "validation_output": result.stdout + result.stderr,
             "observed_at": datetime.now().astimezone().isoformat()}
    if result.returncode:
        return state
    markers = []
    for path in artifacts:
        for event in drs_document_events(path):
            values = [cell for row in event["rows"] for cell in row] if event["kind"] == "table" else [event["text"]]
            markers.extend(path.name + ": " + value for value in values if PUBLICATION_REVIEW_MARKERS.search(value))
    if markers:
        state.update(publication_status="FAIL_INLINE_MARKERS", marker_findings=markers)
    else:
        state["requested_marker_free_publication"] = "NO_MARKERS_DETECTED"
    state["artifact_hashes"] = {path.relative_to(repo_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in artifacts}
    return state


def generate_report(repo_root, snapshot_id, run_start):
    context = json.loads((repo_root / "config/project_context.json").read_text(encoding="utf-8"))
    snapshot, _selection = ipos.resolve_complete_authoritative_input(
        repo_root, "6", project_id=str(context.get("project_name") or repo_root.name), snapshot_id=snapshot_id,
    )
    contract = ipos.resolve_downstream_contract(repo_root, snapshot.snapshot_id)
    manifest = repo_root / "artifacts/orchestrator/workflow_cli_runs.jsonl"
    events = [json.loads(line) for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()]
    events = [event for event in events if event.get("ts", "") >= run_start]
    source_ids = [row["source_req_id"] for row in snapshot.rows if row.get("source_req_id")]
    report = {
        "schema_version": 1, "snapshot_id": snapshot.snapshot_id, "run_start": run_start,
        "user_review_only": True, "authority": False, "gate_override": False,
        "notice": "Advisory only. No approval, allocation, source rewrite or publication acceptance is created. Excluded out-of-scope evidence is not evidence of source damage. Conclusions are review labels, not authority decisions.",
        "allowed_conclusions": sorted(CONCLUSIONS), "workflow_events": events,
        "documents": [], "issues": [],
    }
    for stage, (document_type, directory, filename) in DOCUMENTS.items():
        validators = [event for event in events if event.get("stage") == stage and event.get("kind") == "validator"]
        passed = bool(validators) and validators[-1].get("exit_code") == 0
        folder = repo_root / "artifacts" / directory
        markdown = folder / filename
        state = {"document_type": document_type, "stage": stage,
                 "gate_status": "PASS" if passed else "NOT_VERIFIED_IN_THIS_RUN"}
        report["documents"].append(state)
        if not passed:
            report["issues"].append(issue(document_type, directory, [snapshot.snapshot_id], "generation_not_verified",
                                          "No successful stage validator was recorded in the selected run window; existing documents are not certified by this report.",
                                          [manifest.relative_to(repo_root).as_posix()]))
            continue
        state["artifact_hashes"] = {path.relative_to(repo_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                                    for path in (markdown, markdown.with_suffix(".docx"))}
        for audit in sorted(folder.glob("descriptive*audit.csv")):
            report["issues"].extend(collect_csv_issues(audit, document_type, repo_root))
        for audit in sorted(folder.glob("descriptive*audit.json")):
            payload = json.loads(audit.read_text(encoding="utf-8"))
            if payload.get("snapshot_id") not in {None, snapshot.snapshot_id}:
                raise ValueError("Descriptive audit snapshot mismatch: " + str(audit))
            for index, omission in enumerate(payload.get("omissions", []), 1):
                finding = issue(document_type, omission["location"],
                                [f"{audit.relative_to(repo_root).as_posix()}:omissions:{index}"],
                                omission["reason"], "The existing presentation path omitted review-only or unsupported descriptive text; supported independent text was retained.",
                                [audit.relative_to(repo_root).as_posix(), *omission["source_references"]])
                finding["source_excerpt"] = omission["original"]
                finding["retained_excerpt"] = omission["retained"]
                report["issues"].append(finding)
            for index, finding in enumerate(payload.get("review_findings", []), 1):
                report["issues"].append(issue(document_type, audit.relative_to(repo_root).as_posix(),
                                              [f"review_findings:{index}"], "descriptive_review_finding",
                                              finding if isinstance(finding, str) else json.dumps(finding, ensure_ascii=True),
                                              [audit.relative_to(repo_root).as_posix()]))
        publication = collect_publication_issues(markdown, document_type, repo_root, source_ids)
        report["issues"].extend(publication)
        state["requested_marker_free_publication"] = "FAIL" if publication else "NO_MARKERS_DETECTED"
    for domain, config in ipos.CONFIG.items():
        document_type = "Digital IPOS" if domain == "digital" else "Analog IPOS"
        stage = "6" if domain == "digital" else "7"
        candidates = approved_snapshot_candidate_rows(snapshot, contract, domain=domain)
        names = sorted({row["mapped_block"] for row in candidates})
        state = {"document_type": document_type, "stage": stage,
                 "requirements": len(candidates), "scope": "MATERIALIZED_SCOPE" if candidates else "VALID_EMPTY",
                 "generation_status": "NOT_RUN", "blocks": []}
        report["documents"].append(state)
        runs = [event for event in events if event.get("stage") == stage and event.get("kind") == "runner"]
        if runs:
            state["generation_status"] = "RUNNER_PASS" if runs[-1].get("exit_code") == 0 else "BLOCKED"
        if not runs:
            report["issues"].append(issue(document_type, config["output_dir"], [snapshot.snapshot_id], "stage_not_executed",
                                          "No whole-stage runner was recorded in this window. Any verified block outputs are reported separately and do not complete the stage. A valid-empty allocation is not a generation or validation result.",
                                          [manifest.relative_to(repo_root).as_posix()]))
        for name in names:
            rows = [row for row in candidates if row["mapped_block"] == name]
            functional = build_ipos_functional_input(
                name, ipos._block_inventory_record(repo_root, name), rows, domain=domain, materialized=True,
                provenance=("approved snapshot", "artifacts/stage2_mirco_arc/block_inventory.csv"),
                candidate_requirement_rows=candidates,
            )
            plan = build_ipos_claim_plan(functional)
            findings = ipos_claim_preflight_findings(functional)
            block_state = {"block": name, "requirements": len(rows),
                           "preflight": "BLOCKED" if findings else "PASS", "publication_not_certified": True,
                           "unresolved_contexts": len(plan.evidence.unresolved_contexts),
                           "publication_status": "BLOCKED_NOT_PUBLISHED"}
            if not findings:
                block_state.update(observe_ipos_block_publication(repo_root, domain, name, snapshot.snapshot_id, run_start))
                block_state["publication_not_certified"] = block_state["publication_status"] != "PASS"
                if block_state["publication_status"].startswith("FAIL"):
                    report["issues"].append(issue(document_type, name, [snapshot.snapshot_id], "block_publication_failed",
                                                  block_state.get("validation_output", "") + "\n" + "\n".join(block_state.get("marker_findings", [])),
                                                  ["scripts/validate_ipos_gate.py"]))
            state["blocks"].append(block_state)
            records = {record.record_id: record for record in plan.evidence.records}
            for unresolved in plan.evidence.unresolved_contexts:
                finding = issue(document_type, f"{name}: descriptive claim preflight", [unresolved.context_id],
                                unresolved.reason, "Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract.",
                                [value for span in unresolved.spans for value in records[span.record_id].provenance])
                finding["source_spans"] = [{"record_id": span.record_id, "start": span.start, "end": span.end, "text": span.text}
                                           for span in unresolved.spans]
                report["issues"].append(finding)
            report["issues"].extend(collect_plan_disposition_issues(plan, document_type, name))
            for finding in findings:
                linked = [identity for identity in records if identity in finding]
                sources = [source for identity in linked for source in records[identity].provenance]
                report["issues"].append(issue(document_type, f"{name}: shared preflight", linked or [name], finding,
                                              "The existing shared preflight returned this finding; no override or source correction was applied.",
                                              sources or [str(snapshot.source_path), "scripts/workflow_routing.py"]))
        if any(block["publication_status"] == "PASS" for block in state["blocks"]) and not runs:
            state["generation_status"] = "PARTIAL_BLOCKS_VALIDATED"
    report["issue_counts_by_document"] = dict(Counter(value["document_type"] for value in report["issues"]))
    report["issue_count"] = len(report["issues"])
    for index, finding in enumerate(report["issues"], 1):
        finding["issue_id"] = f"REVIEW-{index:04d}"
        if finding["conclusion"] not in CONCLUSIONS:
            raise ValueError("Unsupported review conclusion")
    return report


def descriptive_blocker_notes(reason, spans, block, records):
    text = " ".join(span.text.strip() for span in spans)
    already_stated = "The approved excerpt states: " + text
    missing = "Not determined. This finding does not establish that the specification lacks a signal, register, value or applicability condition."
    user_action = "Do not add guessed details. Check the cited approved context before treating this finding as a request to amend the specification."
    mechanism = "The current projection or claim plan cannot establish a validated descriptive relationship. This is not proof of missing source information."
    information = "Signal/register completeness has not been established across the approved sources. Do not interpret this parser/model finding as a source-wide absence."
    resolution = "Review the exact admitted relationship and context, then use a shared adapter or profile correction with independent fidelity checks. Do not infer missing detail or relax gates."
    if "unsupported multi-clause or non-normative construction" in reason and not re.search(r"\b(?:shall|must)\b", text, re.I):
        mechanism = "The approved span has no shall/must marker, so the current normative-clause adapter rejects it before descriptive interpretation. Admission is separate from grammatical projection."
        resolution = "Support the attested descriptive grammar in the shared adapter and its independent source checker, preserving every condition and coordinated effect. No new approval is implied or required merely by this parser limitation."
        missing = "The absence of shall/must is not missing technical information or missing approval. The program must interpret the already approved descriptive wording; no source-wide information gap has been established."
        user_action = "Do not insert shall/must just to satisfy the parser. Fix shared grammatical projection; ask for extra technical detail only if the intended description actually requires it."
    if "no_supported_claim" in reason and re.match(r"^Select\s+how\b", text, re.I):
        mechanism = "The parser treats the procedural Select how phrase as a subject; the shared functional-scope filter excludes that malformed interpretation, leaving no supported claim."
        information = "This instruction alone does not establish the selection actor or a controlling signal/register field. Do not infer a fixed setting; concrete implementation bindings need their own approved support, but are not automatically required for qualitative prose."
        resolution = "Interpret the procedural selection relationship through a shared adapter with the correct configuration role. Preserve source meaning and verify procedure boundaries instead of bypassing the filter."
        missing = "The selection actor and controlling signal/register field are not specified by this excerpt. They are possible implementation-detail questions, not prerequisites for saying that a count can be selected. Their absence elsewhere has not been established."
        user_action = "For qualitative prose, repair the interpretation of the selection instruction. For implementation-level prose, locate approved evidence identifying the selector and the allowed settings; request clarification only if that evidence is absent."
        if re.search(r"\s\d+[.]?\s*$", text) and any(re.search(r"\bas\s+follows\s*:\s*1[.]", records[span.record_id].text, re.I) for span in spans):
            information += " The trailing numeral may be a procedure-step marker; verify the admitted layout before treating it as a technical value."
            missing += " A fixed numeric setting cannot be taken from the trailing numeral until procedure numbering is verified."
    if "unsupported relative-clause subject" in reason:
        mechanism = "The parser uses the first shall/must to split subject from action. Here that modal is inside a relative clause, so the preceding descriptive relationship is incorrectly treated as a subject and rejected."
        resolution = "Interpret the main descriptive relationship and the embedded clause separately, retaining their link. Resolve demonstrative references only from unambiguous approved context; do not invent an antecedent."
        user_action = "Check the preceding approved sentence for the referenced signal before requesting a new signal name. If the reference is supported there, fix the shared reference/relative-clause adapter rather than amend the specification."
        if re.match(r"^This\s+signal\b", text, re.I) and spans:
            prefix = _ipos_source_text(records[spans[0].record_id].text[:spans[0].start]).strip()
            previous = re.split(r"(?<=[.!?])\s+", prefix)[-1] if prefix else ""
            identifiers = tuple(dict.fromkeys(re.findall(r"\b[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+\b", previous)))
            if previous:
                already_stated += " Preceding approved sentence: " + previous
            if len(identifiers) == 1:
                information = "The preceding approved sentence already names " + identifiers[0] + ". This is available same-record antecedent evidence, not a missing signal name or an invented register binding. The reference still needs validated interpretation."
                missing = "No missing signal name is established for this relationship: " + identifiers[0] + " is already in the preceding approved sentence. Preserve any stated range and the output signal in the excerpt. The blocker is the program's reference/relative-clause interpretation, not evidence that these details are absent."
    if re.search(r"\b(?:proper|appropriate|corresponding)\s+flag\b", text, re.I):
        information = "The generic flag reference alone does not identify the concrete signal, register or bit binding. Check approved same-block context before requesting clarification. Generic supported behavior can be described without inventing that binding. Source-wide absence has not been established."
        missing = "The exact flag signal or register/bit is not named by the generic flag reference. That detail is needed only if the output must name the implementation binding; it is not needed to describe the stated behavior generically. No source-wide absence has been established."
        user_action = "For a generic description, retain the stated condition and effects without inventing a flag name. For implementation detail, find the approved flag binding first; if it is not documented, ask the specification author which signal or register bit represents that flag."
    return {
        "what_spec_already_states": already_stated,
        "missing_from_spec": missing,
        "user_action": user_action,
        "blocking_mechanism": mechanism,
        "signal_register_information": information,
        "application_scope": "Approved block-local scope: " + block + ". Apply only to the behavior and conditions stated in the cited source spans. Do not infer a responsible sub-block, register, mode or broader applicability.",
        "required_resolution": resolution,
    }


DESCRIPTIVE_ISSUE_CATEGORIES = (
    "recoverable by a bounded shared interpretation fix",
    "non-prose content wrongly blocking descriptive generation",
    "missing information or clarification needed",
    "source-model relationship review needed",
    "essential unresolved descriptive blocker",
    "non-essential unresolved item that must be omitted and reported",
)


REPORT_NOTE_SCHEMA_VERSION = "decision-oriented-issue-notes-v1"
REPORT_BLOCKING_STATUSES = ("blocking", "non-blocking", "report-only")
REPORT_ISSUE_CLASSES = {
    "parser_or_projection_limitation": "Approved text is present; its grammatical or functional relationship is not correctly represented. This is not demonstrated source absence.",
    "missing_source_information": "A specifically identified item is demonstrably absent in the cited approved scope; the missing item and scope must be stated explicitly.",
    "non_prose_misclassification": "Structured content was incorrectly treated as a prose obligation; its existing non-prose output path preserves it.",
    "source_model_relationship_review": "The source checker found a relationship mismatch; affected meaning must not be published until safely reconciled.",
    "stale_alignment": "Existing generated claims, audits or artifacts do not match the currently applied contract; this is not missing technical meaning.",
    "essential_descriptive_blocker": "A required descriptive section or its explicit dependency cannot be supplied from supported approved meaning.",
    "source_information_not_established": "A bounded review has not established a named behavior or qualifier. Neither true source absence nor a parser-only cause is proven.",
    "intentional_exclusion": "Evidence is deliberately excluded by admitted scope or information-gain rules; exclusion is not source damage.",
    "publication_quality_violation": "Rendered text or presentation violates an existing publication rule; no new technical requirement is implied.",
    "historical_observation": "A preserved prior diagnostic has no demonstrated active blocking effect; its exact evidence remains available for review.",
}
REPORT_CLARIFICATION_TYPES = (
    "make_actor_explicit", "clarify_condition_or_guard", "clarify_timing_or_qualification",
    "clarify_output_generation", "split_overloaded_sentence", "clarify_structured_table_meaning",
    "review_source_model_relationship", "none",
)
REPORT_NOTE_FIELDS = (
    "blocking_status", "issue_class", "missing_or_unresolved_information",
    "user_clarification_needed", "clarification_type",
)


def report_note_schema_definition():
    return {"version": REPORT_NOTE_SCHEMA_VERSION, "required_fields": list(REPORT_NOTE_FIELDS),
            "blocking_status_values": list(REPORT_BLOCKING_STATUSES), "issue_classes": REPORT_ISSUE_CLASSES,
            "clarification_type_values": list(REPORT_CLARIFICATION_TYPES),
            "rules": ["Every issue also requires a reader-facing blocking_reason.",
                      "Only an explicitly confirmed, scoped absence may be classified as missing_source_information.",
                      "Unestablished information is not automatically missing source information.",
                      "If user clarification is not actually required, both user_clarification_needed and clarification_type are none.",
                      "Parser fixes, source clarification, structured routing and stale-artifact alignment are separate decisions.",
                      "Historical observations do not override current artifact gates or create approval authority."]}


def populate_report_issue_notes(value, *, historical=False):
    reason = value.get("reason", value.get("blocker_class", ""))
    category = value.get("problem_category", "")
    notes = value.get("diagnostic_notes", {})
    source = " ".join(span["text"] for span in value.get("source_spans", ())) or value.get("source_excerpt", "")
    confirmed = value.get("confirmed_missing_information", "")
    clarification, clarification_type = "none", "none"
    if value.get("current_failure_layer") == "semantic_fidelity":
        issue_class = "parser_or_projection_limitation"
        information = "Approved meaning is present in the cited structured claims, but their candidate paragraphs or assembled section do not pass the current independent final-text fidelity check. Exact findings: " + reason + ". This is a current descriptive realization/readback failure, not demonstrated missing source information. The failed candidate is not published."
    elif re.search(r"(?:stale|not_regenerated|audit_invalid_or_changed|audit_changed|omission_audit_coverage|artifact_missing|materialization.*changed)", reason, re.I):
        issue_class = "stale_alignment"
        information = "The recorded artifact or audit does not match the currently applied contract. Approved technical meaning is not shown to be missing; alignment must be restored before the existing publication gate can pass. Finding: " + reason
    elif value.get("source_model_findings") or category == DESCRIPTIVE_ISSUE_CATEGORIES[3] or "relationship_changed" in reason:
        issue_class = "source_model_relationship_review"
        information = "Approved source meaning is present, but the projected relationship did not preserve it. Affected meaning is withheld rather than passed through. No missing source information is established. Findings: " + "; ".join(value.get("source_model_findings") or [reason])
        if not historical and value.get("source_model_user_review_required"):
            clarification = "Review the cited approved relationship against the withheld model; confirm the intended relationship without rewriting approved source merely to fit the parser."
            clarification_type = "review_source_model_relationship"
    elif category == DESCRIPTIVE_ISSUE_CATEGORIES[1] or reason.startswith("nonprose_output_path:"):
        issue_class = "non_prose_misclassification"
        path = value.get("output_path", reason.partition(":")[2])
        information = "Approved content is present as structured " + (path or "non-prose") + " evidence. It does not require an additional descriptive paragraph and remains in its existing exact output path. No missing technical information is established."
    elif confirmed:
        issue_class = "missing_source_information"
        information = confirmed + " Scope: " + value["confirmed_missing_scope"] + ". This finding is limited to that approved scope, not every source."
        clarification = value["confirmed_user_clarification"]
        clarification_type = value["confirmed_clarification_type"]
    elif category == DESCRIPTIVE_ISSUE_CATEGORIES[4] or value.get("essential"):
        issue_class = "essential_descriptive_blocker"
        information = "Supported approved meaning cannot currently supply the required descriptive obligation or its explicit dependency. Exact unresolved obligation: " + reason + ". This alone does not establish source absence; source amendment is not requested until the approved context has been checked."
    elif value.get("approved_port") or category == DESCRIPTIVE_ISSUE_CATEGORIES[2]:
        issue_class = "source_information_not_established"
        dimensions = ", ".join(value.get("assessment", {}).get("review_dimensions", ())) or reason
        stated = value.get("approved_port", {}).get("Type / details", "")
        information = ("The approved catalog already states: " + stated + ". " if stated else "") + "The bounded approved-scope review has not established " + dimensions + ". " + value.get("unresolved_or_missing_information", "No complete, uniquely bound relationship has been demonstrated.") + " This is not a confirmed missing-source finding. No user clarification is required until the cited context is checked."
    elif re.search(r"(?:excluded|equivalent|out.of.scope|scope_exclusion|duplicate)", reason, re.I):
        issue_class = "intentional_exclusion"
        information = "This contributor is intentionally excluded by scope or information-gain policy, not rejected as damaged or missing source text. Exact exclusion: " + reason + ". " + value.get("explanation", "")
    elif re.search(r"(?:inline_review|publication|layout|marker)", reason, re.I):
        issue_class = "publication_quality_violation"
        information = "The finding concerns rendered wording or presentation, not absent technical behavior. Exact publication defect: " + reason + ". " + value.get("explanation", "")
    elif source or category in {DESCRIPTIVE_ISSUE_CATEGORIES[0], DESCRIPTIVE_ISSUE_CATEGORIES[5]}:
        issue_class = "parser_or_projection_limitation"
        if value.get("recovery_status") == "validated_shared_interpretation":
            information = "Approved meaning is present and has been recovered by the bounded shared interpretation, with source identifiers, quantities and dependency linkage preserved. No source information is missing for this recovered relationship."
        elif re.match(r"^Select\s+how\b", source, re.I):
            information = "The approved procedure explicitly instructs selection of a repetition count. The program incorrectly treats that instruction as a subject. The procedural actor and numeric list boundaries are not a justified fixed setting; repair shared interpretation, not the approved source."
        elif re.fullmatch(r"If\s+.+?\s+is\s+\w+\s+and\s+.+?\s+is\s+\w+[.]?", source, re.I):
            information = "Approved meaning is present: the cited condition causes both stated effects. The adapter rejects this descriptive wording without shall/must before representing the coordinated effects. This is an interpretive limitation, not missing source information; do not add normative words or invent a concrete flag binding."
        else:
            information = "Approved text is present, but the program has not established its complete subject/action/object relationship and required context. " + notes.get("blocking_mechanism", value.get("explanation", "Exact projection finding: " + reason)) + " This is a projection result, not proof of missing source information. Exact finding: " + reason
    else:
        issue_class = "historical_observation"
        information = "The prior diagnostic does not establish a current technical-information gap or a current required-section failure. Exact recorded finding: " + reason + ". " + value.get("explanation", "Its original context references remain preserved for review.")
    status = "report-only" if historical or value.get("approved_port") or issue_class == "historical_observation" else "blocking" if value.get("blocking") else "non-blocking"
    if historical:
        clarification, clarification_type = "none", "none"
        why = "Historical diagnostic retained for traceability, not an active veto in the current flow. Current block preflight and existing-artifact gate results are reported separately."
    elif status == "report-only":
        why = "Completeness review only: no dependency on an essential descriptive section has been established. It does not block this flow; existing source-I/O and publication gates still apply."
    elif status == "blocking":
        why = ("A currently retained descriptive paragraph or assembled section fails independent fidelity verification. It must not be published blindly, even if its approved source is eligible. Resolve the exact final-text mismatch under shared rules and repeat the clean probe; no source clarification or gate waiver is justified by this failure alone."
               if value.get("current_failure_layer") == "semantic_fidelity" else
               "The current generated document/audit linkage fails the existing artifact gate because it is not aligned with the active contract. Publication remains blocked until artifacts are safely aligned and revalidated; this report-only step does not regenerate them or waive the gate."
               if issue_class == "stale_alignment" else
               "This unresolved obligation affects a required descriptive section or its explicit dependency. Clean generation cannot proceed with that meaning unresolved; it must not be guessed or published as uncertain text.")
    elif issue_class == "non_prose_misclassification":
        why = "The content is preserved by its non-prose output path. There is no missing required paragraph, so this item does not block descriptive generation."
    elif value.get("recovery_status") == "validated_shared_interpretation":
        why = "The supported shared recovery resolves this relationship. It does not block descriptive preflight; actual documents still require the unchanged final gate."
    else:
        why = "The affected detail is independent and non-essential; it is withheld and reported, while supported required-section content may proceed. No wrongly interpreted fact is accepted. Existing artifact gates can still block publication."
    value.update(blocking_status=status, issue_class=issue_class, missing_or_unresolved_information=information,
                 user_clarification_needed=clarification, clarification_type=clarification_type,
                 blocking_reason=why, note_schema_version=REPORT_NOTE_SCHEMA_VERSION)
    if "blocking" in value and value["blocking"] != (status == "blocking"):
        value["previous_recorded_blocking"] = value["blocking"]
    value["blocking"] = status == "blocking"
    if historical:
        value["historical_only"] = True
    validate_report_issue_notes(value)


def validate_report_issue_notes(value):
    if any(not isinstance(value.get(field), str) or not value[field].strip() for field in (*REPORT_NOTE_FIELDS, "blocking_reason")):
        raise ValueError("Missing or empty fixed report-note field")
    if (value["blocking_status"] not in REPORT_BLOCKING_STATUSES or value["issue_class"] not in REPORT_ISSUE_CLASSES
            or value["clarification_type"] not in REPORT_CLARIFICATION_TYPES):
        raise ValueError("Unknown centralized report-note value")
    if (value["user_clarification_needed"] == "none") != (value["clarification_type"] == "none"):
        raise ValueError("Clarification need/type mismatch")
    if value["issue_class"] == "missing_source_information" and not all(value.get(field) for field in (
            "confirmed_missing_information", "confirmed_missing_scope", "confirmed_user_clarification", "confirmed_clarification_type")):
        raise ValueError("Source absence must be explicitly confirmed and scoped")


def report_issue_note_markdown(value):
    validate_report_issue_notes(value)
    return ["**" + field + ":** " + markdown_literal(value[field]) for field in REPORT_NOTE_FIELDS] + [
        "**Why this status applies:** " + markdown_literal(value["blocking_reason"]), ""]


def report_note_schema_markdown():
    lines = ["## Fixed Issue-Note Structure", "", "Schema: " + REPORT_NOTE_SCHEMA_VERSION, "",
             "All current and historical issue entries carry the same fixed fields. A historical observation cannot override current gate results.", "",
             "| Field | Definition |", "| --- | --- |",
             "| blocking_status | blocking, non-blocking, or report-only; the reason is stated for the current flow. |",
             "| issue_class | A closed, centrally defined failure-mode class, listed below. |",
             "| missing_or_unresolved_information | Exact missing or unresolved information; distinguish approved meaning from interpretation failure. |",
             "| user_clarification_needed | none, or the exact user-facing clarification actually required. |",
             "| clarification_type | A closed clarification action, or none when no user clarification is needed. |", "",
             "Clarification types: " + ", ".join(REPORT_CLARIFICATION_TYPES) + ".", ""]
    lines.extend("- " + name + ": " + definition for name, definition in REPORT_ISSUE_CLASSES.items())
    return lines + [""]


def classify_descriptive_review_item(value):
    reason = value["reason"].removeprefix("omitted_nonessential:")
    text = " ".join(span["text"] for span in value.get("source_spans", ()))
    if value.get("source_model_findings"):
        return DESCRIPTIVE_ISSUE_CATEGORIES[3]
    if reason.startswith("nonprose_output_path:"):
        return DESCRIPTIVE_ISSUE_CATEGORIES[1]
    if value.get("recovery_status") == "validated_shared_interpretation":
        return DESCRIPTIVE_ISSUE_CATEGORIES[0]
    if value.get("essential"):
        return DESCRIPTIVE_ISSUE_CATEGORIES[4]
    if (("non-normative construction" in reason and re.fullmatch(
            r"If\s+.+?\s+is\s+\w+\s+and\s+.+?\s+is\s+\w+[.]?", text, re.I))
            or (reason == "no_supported_claim" and re.match(r"^Select\s+how\b", text, re.I))):
        return DESCRIPTIVE_ISSUE_CATEGORIES[0]
    if re.search(r"\b(?:not specified|not identified|ambiguous reference|unbound reference|unresolved reference|unsupported implicit context)\b", reason, re.I):
        return DESCRIPTIVE_ISSUE_CATEGORIES[2]
    return DESCRIPTIVE_ISSUE_CATEGORIES[5]


def build_descriptive_obligation_review(functional_inputs):
    from workflow_routing import descriptive_disposition_is_essential
    from validate_downstream_coherence import normalize_human_label

    review = {
        "true_descriptive_blockers": [], "misclassified_nonprose_blockers": [],
        "approved_authority_bearing_prose_support": [],
        "identifier_normalization_recoverable_cases": [],
        "minimum_shared_or_profile_adjustments": {
            "authority": False, "gate_override": False, "specifications_regenerated": False,
            "policy_version": DESCRIPTIVE_OBLIGATION_POLICY_VERSION,
            "implemented": [
                "Profile-bound non-prose dispositions in the existing centralized synthesis plan; exact normative content remains separate.",
                "Bounded exact-first then case/separator-normalized retrieval over already admitted same-owner sources; no fuzzy or prefix equivalence.",
                "Guard actor reconciliation and independent source checks share approved I/O support; ambiguous or conflicting definitions remain unresolved.",
                "Essential sources and their explicit dependency closure are declared in the executable IPOS document contract; independent unsupported detail is omitted and audited.",
                "Bounded same-record unique configurable-signal references preserve the antecedent range, output identifier and clock-duration relationship.",
                "Source/model fidelity failures are quarantined before publishable claim formation; retained prose and exact omission accounting remain independently checked.",
            ],
            "remaining": "Mixed behavior/table/procedure payloads need a separately supported span projection, not blanket table exemption. No broader semantic rewrite or authority expansion is applied.",
            "block_preflight": [],
            "limitation": "Only unresolved essential obligations block descriptive synthesis. Unsafe independent detail is omitted and reported. A parser failure is not proof of missing source information. Passing preflight is not publication certification.",
        },
    }
    for functional in functional_inputs:
        plan = build_ipos_claim_plan(functional)
        records = {record.record_id: record for record in plan.evidence.records}
        document = "Digital IPOS" if functional.domain == "digital" else "Analog IPOS"
        semantic_findings = _ipos_evidence_semantic_findings(plan.evidence)

        def item(identity, reason, spans, *, diagnostic=False):
            value = {"document_type": document, "block": functional.block, "identity": identity,
                    "reason": reason, "source_spans": [dict(record_id=span.record_id, start=span.start,
                    end=span.end, text=span.text) for span in spans],
                    "provenance": list(dict.fromkeys(source for span in spans
                                                     for source in records[span.record_id].provenance))}
            if diagnostic:
                value["diagnostic_notes"] = descriptive_blocker_notes(reason, spans, functional.block, records)
            return value

        routed_spans = set()
        for index, disposition in enumerate(plan.dispositions):
            if disposition.reason.startswith("nonprose_output_path:"):
                routed_spans.update(disposition.spans)
                value = item("disposition:" + str(index), disposition.reason, disposition.spans)
                value["output_path"] = disposition.reason.split(":", 1)[1]
                value["normative_preservation"] = "Exact approved requirement content remains in its existing output path; no copied register table or new prose obligation is introduced."
                review["misclassified_nonprose_blockers"].append(value)
            elif disposition.decision == "unresolved" or disposition.reason.startswith("omitted_nonessential:"):
                value = item("disposition:" + str(index), disposition.reason.removeprefix("omitted_nonessential:"), disposition.spans, diagnostic=True)
                value["essential"] = descriptive_disposition_is_essential(disposition, plan.evidence, profile=IPOS_DESCRIPTIVE_PROFILE)
                value["disposition"] = disposition.decision
                value["source_model_findings"] = [finding for finding in semantic_findings
                                                  if any(span.record_id in finding for span in disposition.spans)]
                review["true_descriptive_blockers"].append(value)
        for finding in semantic_findings:
            spans = tuple(dict.fromkeys(span for proposition in plan.evidence.propositions for span in proposition.spans
                                        if span.record_id in finding))
            value = item(finding, finding, spans, diagnostic=True)
            value["source_model_findings"] = [finding]
            value["essential"] = any(descriptive_disposition_is_essential(disposition, plan.evidence, profile=IPOS_DESCRIPTIVE_PROFILE)
                                     for disposition in plan.dispositions if set(spans).intersection(disposition.spans))
            review["true_descriptive_blockers"].append(value)
        for proposition in plan.evidence.propositions:
            if len(proposition.spans) == 2 and re.match(r"^This\s+signal\s+indicates\b", proposition.spans[-1].text, re.I):
                if any(proposition.proposition_id in claim.proposition_ids for claim in plan.claims):
                    value = item(proposition.proposition_id, "Same-record unique signal antecedent and clock-duration relationship", proposition.spans, diagnostic=True)
                    value["recovery_status"] = "validated_shared_interpretation"
                    review["identifier_normalization_recoverable_cases"].append(value)
        for record in plan.evidence.records:
            if any(record.record_id in finding for finding in semantic_findings):
                continue
            supported = tuple(value for value in plan.evidence.propositions
                              if any(span.record_id == record.record_id for span in value.spans))
            structured_support = any(span.record_id == record.record_id for span in routed_spans)
            structured_function = structured_support and bool(re.search(r"\bTo\s+(?:activate|choose)\b", record.text, re.I))
            if not supported and not structured_function:
                continue
            review["approved_authority_bearing_prose_support"].append({
                "document_type": document, "block": functional.block, "source_record_id": record.record_id,
                "authority_tier": record.authority_tier, "scope": record.ownership_scope,
                "source_text": record.text, "provenance": list(record.provenance),
                "supported_proposition_ids": [value.proposition_id for value in supported],
                "use": "Approved local meaning is eligible as support; final prose must preserve the admitted relationship and qualifiers. Projection and publication are not certified here."
                       if supported else "Structured configuration description may support local detail only; no capability or behavioral synthesis is certified by this row.",
                "contract_boundary": "Current IPOS same-owner refinement/I/O scope; inventory bounds macro-purpose. No new authority or source discovery.",
            })
        for proposition in plan.evidence.propositions:
            if len(proposition.spans) != 1 or proposition.spans[0].record_id.startswith("inventory:"):
                continue
            span = proposition.spans[0]
            text = _ipos_source_text(span.text)
            modals = _ipos_top_level_modals(text)
            prefix = text[:modals[0].start()].strip() if modals else ""
            if not re.match(r"^(?:When|If|Unless|After|Before|Once|During|At)\b", prefix, re.I) or "," in prefix:
                continue
            _condition, actor = _ipos_comma_less_guard_boundary(prefix, functional.block, plan.evidence.records)
            exact_owner = re.fullmatch(r"(.+\s+\S+)\s+((?:the\s+)?" + re.escape(functional.block) + r"(?:\s+block)?)", prefix, re.I)
            if actor and not exact_owner:
                identifier = re.sub(r"^(?:the\s+)|\s+(?:signal|block)$", "", actor, flags=re.I)
                support = retrieve_descriptive_identifier_support(identifier, plan.evidence.records, profile=IPOS_DESCRIPTIVE_PROFILE)
                normalized_owner = normalize_human_label(identifier) == normalize_human_label(functional.block)
                if normalized_owner or any(value["record_id"] in {"inventory:inputs", "inventory:outputs"} for value in support):
                    value = item(proposition.proposition_id, "Bounded approved actor reconciliation; source spelling preserved", proposition.spans)
                    value["retrieval_support"] = list(support)
                    value["recovery_status"] = "validated_shared_interpretation"
                    review["identifier_normalization_recoverable_cases"].append(value)
        findings = ipos_claim_preflight_findings(functional)
        for finding in findings:
            if finding.startswith("ipos_required_section_missing:"):
                value = item("preflight:" + finding, finding, (), diagnostic=True)
                value["essential"] = True
                review["true_descriptive_blockers"].append(value)
        review["minimum_shared_or_profile_adjustments"]["block_preflight"].append({
            "document_type": document, "block": functional.block,
            "remaining_textual_dispositions": sum(value.decision == "unresolved" for value in plan.dispositions),
            "routed_nonprose_dispositions": sum(value.reason.startswith("nonprose_output_path:") for value in plan.dispositions),
            "preflight_status": "BLOCKED" if findings else "PASS", "findings": findings,
            "omitted_nonessential_dispositions": sum(value.reason.startswith("omitted_nonessential:") for value in plan.dispositions),
        })
    issues = [value for key in ("true_descriptive_blockers", "misclassified_nonprose_blockers",
                               "identifier_normalization_recoverable_cases") for value in review[key]]
    for value in issues:
        value["problem_category"] = classify_descriptive_review_item(value)
        value["blocking"] = bool(value.get("essential")) and value.get("recovery_status") != "validated_shared_interpretation"
        value["blocking_reason"] = (
            "Unresolved approved meaning affects a required descriptive section or its explicit dependency; clean generation must stop."
            if value["blocking"] else
            "The shared recovery is supported; no unresolved obligation remains for this item. Final publication still requires the existing gate."
            if value.get("recovery_status") == "validated_shared_interpretation" else
            "Structured content remains in its existing non-prose path and does not require an invented descriptive paragraph."
            if value["problem_category"] == DESCRIPTIVE_ISSUE_CATEGORIES[1] else
            "Independent non-essential detail must be withheld until supported. It does not block required descriptive sections; retained content must still pass every existing check.")
        value.setdefault("diagnostic_notes", {"what_spec_already_states": "See the exact approved spans below.",
            "missing_from_spec": "No source-wide absence is established by this reporting item.",
            "user_action": "Review only the cited approved scope; do not infer missing detail.",
            "blocking_mechanism": value["blocking_reason"],
            "signal_register_information": "Identifier presence alone does not establish handling, timing or generation behavior.",
            "application_scope": "Approved same-owner scope: " + value["block"],
            "required_resolution": "Keep normative evidence unchanged and apply only verified shared rules."})
        value["unresolved_or_missing_information"] = "Unresolved interpretation: " + value["reason"] + ". " + value["diagnostic_notes"]["missing_from_spec"]
        value["clarification_need"] = value["diagnostic_notes"]["user_action"]
        value["review_only_proposal_type"] = (
            "shared interpretation rule with independent fidelity tests" if value["problem_category"] == DESCRIPTIVE_ISSUE_CATEGORIES[0]
            and value.get("recovery_status") != "validated_shared_interpretation" else
            "approved source/model relationship reconciliation" if value["problem_category"] == DESCRIPTIVE_ISSUE_CATEGORIES[3]
            else "source clarification within existing approved scope" if value["problem_category"] == DESCRIPTIVE_ISSUE_CATEGORIES[2]
            else None)
        value["recovery_status"] = value.get("recovery_status", "candidate_only_not_implemented" if value["problem_category"] == DESCRIPTIVE_ISSUE_CATEGORIES[0] else "not_recovered")
        if value["recovery_status"] == "validated_shared_interpretation":
            value["unresolved_or_missing_information"] = "None established for the recovered relationship; exact identifiers, quantities and dependency linkage are retained."
            value["clarification_need"] = "No source amendment is required for this recovered relationship."
            value["diagnostic_notes"]["blocking_mechanism"] = value["blocking_reason"]
            value["diagnostic_notes"]["missing_from_spec"] = value["unresolved_or_missing_information"]
            value["diagnostic_notes"]["user_action"] = value["clarification_need"]
            value["diagnostic_notes"]["required_resolution"] = "Retain the validated shared interpretation and run the unchanged final publication gate after authorized regeneration."
        value["problem_category"] = classify_descriptive_review_item(value)
    result = {"version": "descriptive-obligation-review-v2", "authority": False, "gate_override": False,
            "specifications_regenerated": False, "issues": issues,
            "categories": {category: sum(value["problem_category"] == category for value in issues)
                           for category in DESCRIPTIVE_ISSUE_CATEGORIES},
            "essential_issue_set": [dict(block=value["block"], identity=value["identity"], source_spans=value["source_spans"])
                                    for value in issues if value["blocking"]],
            "evidence_inventory": review["approved_authority_bearing_prose_support"],
            "minimum_shared_or_profile_adjustments": review["minimum_shared_or_profile_adjustments"]}
    result["note_schema"] = report_note_schema_definition()
    for value in result["issues"]:
        populate_report_issue_notes(value)
    return result


def ipos_decision_summary(review):
    result = []
    for block in review["minimum_shared_or_profile_adjustments"]["block_preflight"]:
        issues = [value for value in review["issues"] if value["block"] == block["block"]]
        artifact_issues = [value for value in review.get("artifact_alignment_issues", ()) if value["block"] == block["block"]]
        active = [value for value in issues if value["blocking_status"] == "blocking"]
        classes = sorted({value["issue_class"] for value in active + artifact_issues})
        nonblocking = sorted({value["issue_class"] for value in issues if value["blocking_status"] != "blocking"})
        passing = block.get("publication_status") == "PASS"
        descriptive_ready = block["preflight_status"] == "PASS" and not active
        observation = next((value for value in review.get("clean_generation_observations", {}).get("blocks", ())
                    if value["block"] == block["block"] and value["document_type"] == block["document_type"]), {})
        failed_materialization = observation.get("probe_status") == "BLOCKED" or observation.get("generation_status") == "BLOCKED"
        clarification = any(value["user_clarification_needed"] != "none" for value in issues if not value.get("historical_only"))
        result.append({"block": block["block"], "document_type": block["document_type"],
            "current_status": "PASS" if passing else "BLOCKED", "active_blocker_classes": classes,
            "nonblocking_classes": nonblocking, "clean_generation_possible_now": "yes" if passing else "no" if failed_materialization else "partial" if descriptive_ready else "no",
            "user_clarification_needed": "yes" if clarification else "no",
            "shortest_next_action": "Keep validated outputs" if passing else "Resolve recorded materialization failure" if failed_materialization else "Regenerate and run existing gate" if descriptive_ready else "Resolve active descriptive findings",
            "effective_descriptive_blocker_ids": [value["issue_id"] for value in active],
            "artifact_blocker_ids": [value["issue_id"] for value in artifact_issues]})
    return result


def remaining_ipos_blocker_details(repo_root, review):
    from workflow_routing import _ipos_claim_output_role, _ipos_document_contract

    decisions = review.get("decision_summary") or ipos_decision_summary(review)
    blocked = {(value["document_type"], value["block"]) for value in decisions if value["current_status"] == "BLOCKED"}
    context = json.loads((repo_root / "config/project_context.json").read_text(encoding="utf-8"))
    snapshot, _selection = ipos.resolve_complete_authoritative_input(
        repo_root, "6", project_id=str(context.get("project_name") or repo_root.name), snapshot_id=review["snapshot_id"])
    contract = ipos.resolve_downstream_contract(repo_root, snapshot.snapshot_id)
    sections = _ipos_document_contract()["sections"]
    result = {}
    for domain in ipos.CONFIG:
        document_type = "Digital IPOS" if domain == "digital" else "Analog IPOS"
        candidates = approved_snapshot_candidate_rows(snapshot, contract, domain=domain)
        for name in sorted(block for kind, block in blocked if kind == document_type):
            functional = build_ipos_functional_input(
                name, ipos._block_inventory_record(repo_root, name),
                [row for row in candidates if row["mapped_block"] == name], domain=domain,
                materialized=True, provenance=("approved snapshot", "artifacts/stage2_mirco_arc/block_inventory.csv"),
                candidate_requirement_rows=candidates)
            plan = build_ipos_claim_plan(functional)
            details = {"claims": {}, "sections": {}}
            for section in sections:
                claims = [claim for claim in plan.claims if _ipos_claim_output_role(claim.role) == section["role"]]
                meanings = list(dict.fromkeys(meaning for claim in claims for meaning in claim.meanings))
                support = [meaning.subject + ": " + ("not " if meaning.negative else "") + meaning.predicate
                           + " " + ", ".join(meaning.objects) for meaning in meanings[:2]]
                summary = "; ".join(support) or "No supported claim assigned to this section in the current shared plan."
                if len(meanings) > 2:
                    summary += "; remaining supported relations in appendix"
                details["sections"][section["title"].split()[0]] = {"title": section["title"], "meaning": summary}
                for claim in claims:
                    support = [meaning.subject + ": " + ("not " if meaning.negative else "") + meaning.predicate
                               + " " + ", ".join(meaning.objects) for meaning in claim.meanings[:2]]
                    summary = "; ".join(support)
                    if re.match(r"^(?:its?|their|this|that|these|those|they)\b", claim.meanings[0].subject, re.I):
                        excerpt = next((span.text for span in claim.spans if len(span.text.split()) <= 25
                                        and claim.meanings[0].subject.casefold() in span.text.casefold()), None)
                        summary = excerpt or summary
                    details["claims"][claim.claim_id] = {"section": section["title"], "meaning": summary,
                                                        "name": ", ".join(claim.responsibilities[:2])}
            result[name] = details
    return result


def remaining_ipos_blocker_markdown(review, details=None):
    details = details or {}
    evidence = review.get("current_evidence", {})
    if evidence.get("blocks") is not None:
        lines = ["# Remaining IPOS blockers", "", "Snapshot: " + markdown_literal(review["snapshot_id"]), "",
            "Current document status: " + evidence["status"] + ". Review-only; no gate override.", "",
            "Current artifact checks below are separate from stage execution and implementation readiness. Saved review findings remain historical.", "",
            "| IPOS block | Document status | Current evidence | Implementation readiness |",
            "| --- | --- | --- | --- |"]
        for block in evidence["blocks"]:
            lines.append("| " + " | ".join(markdown_literal(str(value)).replace("|", "\\|") for value in
                (block["block"], block["status"], block["reason"], "NOT_ASSESSED")) + " |")
        if evidence.get("run_context"):
            lines.extend(["", "Run exit: " + str(evidence["run_context"].get("exit_code")) +
                ". A successful process exit alone does not certify document publication or readiness."])
        lines.extend(["", "[Historical detailed evidence](descriptive_obligation_review_appendix.json)", ""])
        return "\n".join(lines)
    if evidence.get("status") == "UNVERIFIED":
        return "\n".join(["# Remaining IPOS blockers", "",
            "Current status: UNVERIFIED. " + markdown_literal(evidence["reason"]), "",
            "Saved review findings are historical evidence, not a current PASS or BLOCKED assessment.", "",
            "[Historical detailed evidence](descriptive_obligation_review_appendix.json)", ""])
    labels = {
        "ipos_final_claim_missing_or_changed": "Missing/changed supported claim",
        "ipos_final_unmodeled_content": "Unmodeled content",
        "ipos_final_required_section_missing": "Required section missing",
        "ipos_final_source_relationship_changed": "Source/model relationship changed",
    }
    lines = ["# Remaining IPOS blockers", "",
             "Historical saved review findings; not a current gate assessment. Support below is abbreviated; full conditions, IDs and offsets remain in the appendix.", "",
             "[Detailed evidence](descriptive_obligation_review_appendix.json)", ""]
    observations = review.get("clean_generation_observations", {}).get("blocks", [])
    decisions = review.get("decision_summary")
    if decisions is None:
        decisions = ipos_decision_summary(review)
    for decision in decisions:
        if decision["current_status"] != "BLOCKED":
            continue
        observation = next((value for value in observations if value["block"] == decision["block"]
                            and value["document_type"] == decision["document_type"]), {})
        active = [value for value in review.get("issues", []) if value.get("block") == decision["block"]
                  and value.get("blocking_status") == "blocking" and not value.get("historical_only")]
        probe_issues = [value for value in active if value.get("identity", "").startswith("current-probe:")]
        checks = observation.get("contract_report", {}).get("checks", {})
        findings = [str(finding) for check in checks.values() for finding in check.get("findings", [])]
        if findings:
            active = probe_issues
        else:
            findings = [value.get("reason", value.get("blocking_reason", "Recorded blocker")) for value in active]
        points = {}
        for finding in findings:
            for part in finding.split("; "):
                compact = re.sub(r":[^:;]*\.(?:md|docx)(?=:|$)", "", part.strip())
                code, separator, location = compact.partition(":")
                points.setdefault(location if separator else "Recorded finding", [])
                if labels.get(code, code) not in points[location if separator else "Recorded finding"]:
                    points[location if separator else "Recorded finding"].append(labels.get(code, code))
        lines.extend(["## " + markdown_literal(decision["block"]), "",
                      "| Section or claim | Failure type | Expected supported meaning | Observed problem | Likely failing layer |",
                      "| --- | --- | --- | --- | --- |"])
        block_details = details.get(decision["block"], {})
        ordinal = 0
        for location, failures in points.items():
            if location.startswith("audit:"):
                ordinal += 1
                claim = block_details.get("claims", {}).get(location[len("audit:"):])
                if claim is None:
                    raise ValueError("Cited blocker claim is not recoverable from the selected snapshot: " + location)
                title = claim["section"] + " / claim " + str(ordinal) + ": " + claim["name"]
                meaning = claim["meaning"]
                observed = "Candidate claim rejected by independent fidelity readback; the saved probe does not isolate the lost fact."
                layer = "realization/readback (not localized)"
            else:
                section = block_details.get("sections", {}).get(location, {})
                title = section.get("title", "Section " + location)
                meaning = section.get("meaning", "Exact supported relations are recorded in the appendix.")
                observed = "Assembled MD and DOCX section is not reconciled with the retained claim set."
                layer = "section mapping/readback (not localized)"
            fields = (title, "; ".join(failures), meaning, observed, layer)
            lines.append("| " + " | ".join(markdown_literal(field).replace("|", "\\|") for field in fields) + " |")
        lines.append("")
    if not any(line.startswith("## ") for line in lines):
        lines.extend(["No blocked IPOS blocks in the saved review.", ""])
    return "\n".join(lines)


def current_ipos_blocker_evidence(repo_root, snapshot_id, run_context=None):
    from ipos_blocker_review import apply_descriptive_omissions
    from spec_document_contract import ipos_document_contract_report, validate_materialization_chain
    from workflow_routing import build_ipos_normalized_records

    context = json.loads((repo_root / "config/project_context.json").read_text(encoding="utf-8"))
    snapshot, _selection = ipos.resolve_complete_authoritative_input(
        repo_root, "6", project_id=str(context.get("project_name") or repo_root.name), snapshot_id=snapshot_id)
    contract = ipos.resolve_downstream_contract(repo_root, snapshot.snapshot_id)
    results_path = repo_root / "artifacts/orchestrator/ipos_generation_results.json"
    results = json.loads(results_path.read_text(encoding="utf-8")) if results_path.is_file() else {}
    blocks = []
    for domain, config in ipos.CONFIG.items():
        document_type = "Digital IPOS" if domain == "digital" else "Analog IPOS"
        stage = "6" if domain == "digital" else "7"
        candidates = approved_snapshot_candidate_rows(snapshot, contract, domain=domain)
        names = sorted({row["mapped_block"] for row in candidates if contract.target(row["source_req_id"]) == document_type})
        for name in names:
            value = {"block": name, "document_type": document_type, "status": "UNVERIFIED",
                     "reason": "No matching current publication evidence", "findings": []}
            blocks.append(value)
            if run_context and (stage not in run_context["stages"] or
                    run_context.get("block") not in (None, "", name)):
                value["reason"] = "Outside the completed run scope; historical evidence only"
                continue
            folder = repo_root / config["output_dir"] / "blocks" / ipos._block_slug(name)
            markdown = folder / ipos._block_markdown_name(domain, name)
            docx = markdown.with_suffix(".docx")
            audit = folder / "descriptive_summary_audit.csv"
            materialization = folder / "materialization_audit.json"
            saved_report = folder / "document_contract_report.json"
            try:
                if domain == "digital":
                    if results.get("snapshot_id") != snapshot_id:
                        value["reason"] = "Generation observations missing or bound to another snapshot"
                        continue
                    observations = [row for row in results.get("blocks", ()) if row["block"] == name]
                    if len(observations) != 1 or results.get("scope") not in ("all", name):
                        value["reason"] = "No unique generation observation in the matching block scope"
                        continue
                    observation = observations[0]
                    if run_context and not (run_context["started_at"] <= results_path.stat().st_mtime <= run_context["finished_at"]):
                        value["reason"] = "Generation observations do not belong to the completed run"
                        continue
                    if observation.get("status") == "BLOCKED":
                        value.update(status="BLOCKED", reason=observation.get("waiting_reason") or
                            "; ".join(observation.get("findings", ())) or "Recorded current generation/publication failure",
                            findings=observation.get("findings", []))
                        continue
                    if observation.get("status") != "PASS":
                        continue
                paths = (markdown, docx, audit, materialization, saved_report)
                if not all(path.is_file() for path in paths):
                    value["reason"] = "Required current document or audit artifact is missing"
                    continue
                if run_context and not all(run_context["started_at"] <= path.stat().st_mtime <=
                        run_context["finished_at"] for path in paths):
                    value["reason"] = "Published artifacts do not belong to the completed run"
                    continue
                if re.findall(r"^- Snapshot: `([^`]+)`", markdown.read_text(encoding="utf-8"), re.M) != [snapshot_id]:
                    value["reason"] = "Published document does not match the selected snapshot"
                    continue
                functional = build_ipos_functional_input(name, ipos._block_inventory_record(repo_root, name),
                    [row for row in candidates if row["mapped_block"] == name and contract.target(row["source_req_id"]) == document_type],
                    domain=domain, materialized=True,
                    provenance=("approved snapshot", "artifacts/stage2_mirco_arc/block_inventory.csv"),
                    candidate_requirement_rows=candidates,
                    descriptive_source_records=contract.descriptive_context(repo_root, block=name, domain=domain))
                functional = apply_descriptive_omissions(repo_root, snapshot_id=snapshot_id, functional_input=functional)
                binding = validate_materialization_chain(materialization, "IPOS",
                    build_ipos_normalized_records(functional), markdown, docx)
                if binding:
                    value.update(reason="Stale or changed materialization; current status is unverified", findings=binding)
                    continue
                report = ipos_document_contract_report(repo_root, markdown, audit, functional)
                saved = json.loads(saved_report.read_text(encoding="utf-8"))
                if saved != report and report["status"] == "PASS":
                    value["reason"] = "Saved validation report no longer matches current artifact checks"
                    continue
                findings = [finding for check in report["checks"].values() for finding in check["findings"]]
                value.update(status="PASS" if report["status"] == "PASS" else "BLOCKED",
                    reason="Current snapshot-bound document checks PASS; residuals: " + str(len(report.get("residuals", ())))
                        if report["status"] == "PASS" else "; ".join(findings), findings=findings)
            except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
                value["reason"] = "Current evidence unavailable: " + str(error)
    status = "BLOCKED" if any(row["status"] == "BLOCKED" for row in blocks) else (
        "UNVERIFIED" if any(row["status"] == "UNVERIFIED" for row in blocks) else "PASS")
    return {"status": status, "blocks": blocks, "run_context": run_context,
            "authority": False, "gate_override": False}


def write_remaining_ipos_blocker_report(repo_root, snapshot_id, *, run_context=None):
    folder = repo_root / "artifacts/orchestrator"
    review = json.loads((folder / "descriptive_obligation_review.json").read_text(encoding="utf-8"))
    if review["snapshot_id"] != snapshot_id:
        raise ValueError("Blocker review does not match the run snapshot")
    output = folder / "remaining_ipos_blockers.md"
    try:
        review["current_evidence"] = current_ipos_blocker_evidence(repo_root, snapshot_id, run_context)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        review["current_evidence"] = {"status": "UNVERIFIED", "reason": "Current evidence unavailable: " + str(error)}
    output, _docx = export_review_document(output, remaining_ipos_blocker_markdown(review))
    return output


def descriptive_obligation_review_markdown(review):
    lines = ["| IPOS block | Current status | Active blocker classes | Non-blocking classes | Clean generation possible now | User clarification needed | Shortest next action |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for value in ipos_decision_summary(review):
        fields = (value["block"], value["current_status"], ", ".join(value["active_blocker_classes"]) or "none",
                  ", ".join(value["nonblocking_classes"]) or "none", value["clean_generation_possible_now"],
                  value["user_clarification_needed"], value["shortest_next_action"])
        lines.append("| " + " | ".join(markdown_literal(field) for field in fields) + " |")
    lines.extend(["", "# IPOS Decision Review", "", "Snapshot: " + markdown_literal(review.get("snapshot_id", "test scope")), "",
                  "Only unresolved essential descriptive obligations are active descriptive blockers. Non-prose routes, independent audited omissions and report-only history do not veto generation.", "",
                  "Partial means the current shared descriptive preflight passes, but the actual Markdown/DOCX gate has not certified clean regenerated outputs. It is not a publication PASS.", "",
                  "Clarification means a confirmed user question, including non-blocking interface-description gaps. Unestablished completeness alone does not request clarification; a yes is not automatically a generation blocker.", "",
                  "Full issue IDs, source excerpts, offsets, provenance, removed blockers and retained supported meaning: descriptive_obligation_review_appendix.md and its JSON/DOCX companions.", ""])
    return "\n".join(lines) + "\n"


def descriptive_obligation_review_appendix_markdown(review):
    lines = ["# Descriptive Obligation Review", "", "For user review only. No source, approval, mapping or gate is changed.", "",
             "Snapshot: " + markdown_literal(review.get("snapshot_id", "test scope")), "",
             "Essential unresolved items: " + str(len(review["essential_issue_set"])), "",
             "Preflight is not publication certification. Only current artifact gate PASS certifies the produced outputs; controlled generation observations, when available, are listed below.", ""]
    lines.extend(report_note_schema_markdown())
    for category in DESCRIPTIVE_ISSUE_CATEGORIES:
        values = [value for value in review["issues"] if value["problem_category"] == category]
        lines.extend(["## " + category, "", "Items: " + str(len(values)), ""])
        for value in values:
            lines.extend(["### " + markdown_literal(value.get("issue_id", value["block"] + " / " + value["identity"])), "",
                          "Block: " + markdown_literal(value["block"]), "",
                          "Category: " + category, "",
                          "Blocking: " + ("yes" if value["blocking"] else "no") + ". " + markdown_literal(value["blocking_reason"]), "",
                          "Unresolved or missing information: " + markdown_literal(value["missing_or_unresolved_information"]), "",
                          "Clarification need: " + markdown_literal(value["user_clarification_needed"]), "",
                          "Recovery status: " + markdown_literal(value["recovery_status"]), "",
                          "Review-only proposal type: " + markdown_literal(value.get("review_only_proposal_type") or "none"), ""])
            lines.extend(report_issue_note_markdown(value))
            if value.get("source_spans"):
                for span in value["source_spans"]:
                    fence = "`" * max(3, 1 + max((len(part) for part in re.findall(r"`+", span["text"])), default=0))
                    lines.extend(["Source: " + markdown_literal(span["record_id"]) + "; offsets " + str(span["start"]) + " to " + str(span["end"]),
                                  "", fence + "text", span["text"], fence, ""])
            elif value.get("source_text"):
                lines.extend(["```text", value["source_text"], "```", ""])
            lines.extend([markdown_literal(value.get("reason", value.get("use", ""))), "",
                          "Provenance: " + markdown_literal("; ".join(value["provenance"])), ""])
            if value.get("diagnostic_notes"):
                lines.extend(["**Diagnostic note**", ""])
                for field, label in (
                    ("what_spec_already_states", "What the specification already states"),
                    ("missing_from_spec", "What is missing or not identified"),
                    ("user_action", "What the user needs to do"),
                    ("blocking_mechanism", "Blocking mechanism"),
                    ("signal_register_information", "Signal/register information"),
                    ("application_scope", "Where the rule applies"),
                    ("required_resolution", "Required resolution"),
                ):
                    if field in value["diagnostic_notes"]:
                        lines.append("- **" + label + ":** " + markdown_literal(value["diagnostic_notes"][field]))
                lines.append("")
    lines.extend(["## Minimum Shared Or Profile Adjustments", ""])
    adjustments = review["minimum_shared_or_profile_adjustments"]
    lines.extend("- " + text for text in adjustments["implemented"])
    lines.extend(["", adjustments["remaining"], "", adjustments["limitation"], "",
                  "This report creates no authority path or gate override. Separately authorized regeneration is recorded below, not performed by report rendering.", "",
                  "| Block | Descriptive preflight | Existing artifact gate | Routed non-prose | Omitted detail | Essential unresolved |",
                  "| --- | --- | --- | ---: | ---: | ---: |"])
    for value in adjustments["block_preflight"]:
        lines.append("| " + markdown_literal(value["block"]) + " | " + value["preflight_status"] + " | "
                     + markdown_literal(value.get("publication_status", "NOT_CHECKED")) + " | "
                     + str(value["routed_nonprose_dispositions"]) + " | " + str(value["omitted_nonessential_dispositions"]) + " | "
                     + str(value["remaining_textual_dispositions"]) + " |")
    if review.get("previous_review"):
        lines.extend(["", "## Previous Review Reclassification", "",
                      "Previous exact issue identities, excerpts, offsets and notes are preserved in the companion JSON. Older blocker labels are historical, not current decisions.", "",
                      "| Block | Previous identity | Current category | Current disposition |",
                      "| --- | --- | --- | --- |"])
        for value in review.get("reclassified_issue_set", ()):
            lines.append("| " + " | ".join(markdown_literal(value[field]) for field in ("block", "previous_identity", "problem_category", "current_disposition")) + " |")
    if review.get("artifact_alignment_issues"):
        lines.extend(["", "## Current Artifact Alignment Issues", "",
                      "These are actual existing-artifact gate failures, not additional missing-source or essential-description claims.", ""])
        for value in review["artifact_alignment_issues"]:
            lines.extend(["### " + value["issue_id"], "", "Block: " + markdown_literal(value["block"]), "",
                          *report_issue_note_markdown(value), "```text", value["gate_output"], "```", ""])
    if review.get("removed_from_active_blocking_set"):
        lines.extend(["", "## Exact Issues Removed From Active Descriptive Blocking", "",
                      "Removal means the item is not an unresolved essential descriptive obligation; it is not proof that all source meaning has been recovered.", ""])
        for value in review["removed_from_active_blocking_set"]:
            lines.extend(["- " + markdown_literal(value["block"] + " / " + value["identity"] + ": " + value["removal_reason"] + "; current issue IDs: " + ", ".join(value["current_issue_ids"])), ""])
    if review.get("supported_prose_ledger"):
        lines.extend(["", "## Exact Supported Meaning Kept In Published Prose", "",
                      "Every paragraph below is source-linked retained content from a block that passes the actual publication gate. Newly source-linked materialization is not a claim of new source authority or complete unsupported-source recovery.", ""])
        for value in review["supported_prose_ledger"]:
            lines.extend(["### " + markdown_literal(value["block"] + " / " + value["claim_id"]), "",
                          "Disposition: " + value["comparison_to_previous_audit"], "",
                          "Section: " + markdown_literal(value["section"]), "",
                          "```text", value["rendered_prose"], "```", "",
                          "Exact contributor IDs: " + markdown_literal(", ".join(value["contributor_ids"])), "",
                          "Source references: " + markdown_literal("; ".join(value["source_record_ids"])), ""])
            for span in value["source_spans"]:
                lines.extend(["Source: " + markdown_literal(span["record_id"]) + "; offsets " + str(span["start"]) + " to " + str(span["end"]),
                              "", "```text", span["text"], "```", ""])
    if review.get("clean_generation_observations"):
        lines.extend(["", "## Controlled Generation Observations", "", "```json",
                      json.dumps(review["clean_generation_observations"], indent=2, ensure_ascii=True), "```", ""])
    if review.get("effective_descriptive_blocker_set"):
        lines.extend(["", "## Exact Remaining Current Descriptive Blockers", ""])
        for value in review["effective_descriptive_blocker_set"]:
            lines.extend(["- " + markdown_literal(value["block"] + " / " + value["issue_id"] + ": " + value["reason"]), ""])
    return "\n".join(lines) + "\n"


def write_ipos_generation_observations(root, snapshot_id, blocks, protection):
    report = {"snapshot_id": snapshot_id, "authority": False, "gate_override": False,
              "observed_at": datetime.now().astimezone().isoformat(), "blocks": blocks, "protection": protection}
    path = root / "artifacts/orchestrator/ipos_clean_generation_observations.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return path


def attach_ipos_decision_trace(root, review):
    path = root / "artifacts/orchestrator/ipos_clean_generation_observations.json"
    if path.is_file():
        observations = json.loads(path.read_text(encoding="utf-8"))
        if observations["snapshot_id"] != review["snapshot_id"]:
            raise ValueError("Generation observations do not match the selected snapshot")
        review["clean_generation_observations"] = observations
        review["specifications_regenerated"] = any(value.get("generation_status") == "PASS" for value in observations["blocks"])
        for value in observations["blocks"]:
            block = next((block for block in review["minimum_shared_or_profile_adjustments"]["block_preflight"]
                          if block["block"] == value["block"] and block["document_type"] == value["document_type"]), None)
            if block:
                block["specifications_regenerated"] = value.get("generation_status") == "PASS"
    removed = []
    for old in review.get("reclassified_issue_set", ()):
        matches = [value for value in review["issues"] if value["block"] == old["block"]
                   and old["previous_source_spans"] and all(span in value["source_spans"] for span in old["previous_source_spans"])]
        if not any(value["blocking_status"] == "blocking" for value in matches):
            removed.append({"block": old["block"], "identity": old["previous_identity"],
                            "source_spans": old["previous_source_spans"], "current_issue_ids": [value["issue_id"] for value in matches],
                            "removal_reason": old["problem_category"] + "; no unresolved essential-section dependency remains active"})
    for value in review["issues"]:
        if value["blocking_status"] != "blocking" and value.get("approved_port"):
            removed.append({"block": value["block"], "identity": value["identity"], "source_spans": value["source_spans"],
                            "current_issue_ids": [value["issue_id"]], "removal_reason": "report-only approved-port completeness question, not an essential descriptive dependency"})
    review["removed_from_active_blocking_set"] = removed
    ledger = []
    for block in review["minimum_shared_or_profile_adjustments"]["block_preflight"]:
        if block.get("publication_status") != "PASS":
            continue
        domain = "digital" if block["document_type"] == "Digital IPOS" else "analog"
        folder = root / ipos.CONFIG[domain]["output_dir"] / "blocks" / ipos._block_slug(block["block"])
        observation = next((value for value in review.get("clean_generation_observations", {}).get("blocks", ())
                            if value["block"] == block["block"] and value["document_type"] == block["document_type"]), {})
        previous = set(observation.get("previous_selected_claim_ids", ()))
        with (folder / "descriptive_summary_audit.csv").open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("decision") != "selected":
                    continue
                claim = json.loads(row["claim_json"])
                ledger.append({"block": block["block"], "claim_id": row["unit_id"], "section": row["target_section"],
                               "rendered_prose": row["rendered_summary"], "contributor_ids": claim["proposition_ids"],
                               "source_record_ids": list(dict.fromkeys(span["record_id"] for span in claim["spans"])),
                               "source_spans": claim["spans"], "supported_meanings": claim["meanings"],
                               "comparison_to_previous_audit": "previously selected claim retained" if row["unit_id"] in previous else "newly source-linked in current prose; not a claim of invented or newly approved meaning"})
    review["supported_prose_ledger"] = ledger
    review["effective_descriptive_blocker_set"] = [{key: value[key] for key in ("issue_id", "block", "reason", "source_spans", "blocking_reason")}
                                                 for value in review["issues"] if value["blocking_status"] == "blocking"]
    review["decision_summary"] = ipos_decision_summary(review)


def build_current_probe_failure_issues(review, functional_inputs):
    from workflow_routing import _ipos_claim_output_role, _ipos_document_contract

    path = {value.block: value for value in functional_inputs}
    sections = {value["title"].split()[0]: value["role"] for value in _ipos_document_contract()["sections"]}
    issues = []
    for observation in review.get("clean_generation_observations", {}).get("blocks", ()):
        if observation.get("probe_status") != "BLOCKED":
            continue
        functional = path[observation["block"]]
        plan = build_ipos_claim_plan(functional)
        checks = observation.get("contract_report", {}).get("checks", {})
        for layer, check in checks.items():
            if check["status"] == "PASS":
                continue
            findings = check["findings"]
            failed_sections = {sections[match[1]] for finding in findings if (match := re.search(r":(1\.[1-5])$", finding))}
            affected = [claim for claim in plan.claims if any(claim.claim_id in finding for finding in findings)
                        or _ipos_claim_output_role(claim.role) in failed_sections]
            records = {record.record_id: record for record in plan.evidence.records}
            source_spans = list(dict.fromkeys(span for claim in affected for span in claim.spans))
            value = {"document_type": observation["document_type"], "block": observation["block"],
                     "identity": "current-probe:" + layer, "reason": "; ".join(findings),
                     "current_failure_layer": layer, "problem_category": DESCRIPTIVE_ISSUE_CATEGORIES[0],
                     "source_spans": [asdict(span) for span in source_spans], "blocking": True,
                     "provenance": list(dict.fromkeys(source for span in source_spans for source in records[span.record_id].provenance)),
                     "affected_claim_ids": [claim.claim_id for claim in affected],
                     "recovery_status": "current_final_text_fidelity_failure_not_recovered", "review_only_proposal_type": "precise shared realization/readback reconciliation",
                     "diagnostic_notes": {"what_spec_already_states": "Exact approved claim-support spans are retained below.",
                        "missing_from_spec": "No missing source information is established; current candidate text fails independent verification.",
                        "user_action": "none", "blocking_mechanism": "The existing independent final-text fidelity check rejects the candidate section; this is not a stale-input-only finding.",
                        "signal_register_information": "Preserve the exact identifiers and context from the cited approved spans.",
                        "application_scope": functional.block, "required_resolution": "Resolve the recorded shared realization/readback mismatch, then repeat the probe without weakening the gate."}}
            populate_report_issue_notes(value)
            value["unresolved_or_missing_information"] = value["missing_or_unresolved_information"]
            value["clarification_need"] = value["user_clarification_needed"]
            value["issue_id"] = "IPOS-PROBE-" + hashlib.sha256((review["snapshot_id"] + ":" + functional.block + ":" + layer).encode("utf-8")).hexdigest()[:16]
            issues.append(value)
    return issues


def build_missing_information_report(functional_inputs, source_ports):
    from validate_downstream_coherence import human_label_key

    scoped = {human_label_key(value.block): value for value in functional_inputs if value.materialized}
    if len(scoped) != sum(value.materialized for value in functional_inputs):
        raise ValueError("Ambiguous approved block labels in signal review scope")
    plans = {key: build_ipos_claim_plan(value) for key, value in scoped.items()}
    issues, assessments = [], []
    for port in source_ports:
        functional = scoped.get(human_label_key(port.get("Owner", "")))
        if not functional or port.get("Ownership status", "").casefold().strip() != "approved":
            continue
        name = port.get("Port name", "").strip()
        if not name:
            raise ValueError("Approved source port without an exact name")
        plan = plans[human_label_key(functional.block)]
        try:
            support = retrieve_descriptive_identifier_support(name, plan.evidence.records, profile=IPOS_DESCRIPTIVE_PROFILE, max_candidates=128)
            retrieval_status = "bounded_search_complete"
        except ValueError as error:
            support, retrieval_status = (), "bounded_search_unresolved: " + str(error)
        record_ids = {value["record_id"] for value in support if value["record_id"].startswith("requirement:")}
        retained = {identity for claim in plan.claims for identity in claim.proposition_ids}
        propositions = [value for value in plan.evidence.propositions if value.proposition_id in retained
                        and any(span.record_id in record_ids for span in value.spans)]
        spellings = {value["identifier"] for value in support}
        spellings.add(name)
        pattern = r"(?<![\w-])(?:" + "|".join(re.escape(value) for value in sorted(spellings)) + r")(?![\w-])"
        named = [value for value in propositions if re.search(pattern, json.dumps(asdict(value.meaning)), re.I)]
        active = [value for value in named if re.search(pattern, value.meaning.subject + " " + " ".join(value.meaning.objects), re.I)
                  and value.meaning.predicate not in {"be", "have", "contain", "include", "comprise"}]
        passive = [value for value in named if re.search(pattern, value.meaning.subject, re.I)
                   and value.meaning.predicate == "be" and re.match(r"(?:set|reset|written|read|asserted|deasserted|activated|disabled|enabled|bypassed)\b", " ".join(value.meaning.objects), re.I)]
        qualified = [value for value in named if value.meaning.contexts]
        timed = [value for value in named if re.search(r"\b(?:cycles?|clocks?|ns|us|ms|seconds?|rising edge|falling edge|before|after|until|during)\b",
                                                     json.dumps(asdict(value.meaning)), re.I)]
        coverage = {"handling": bool(active or passive), "timing": bool(timed), "qualification": bool(qualified)}
        catalog_description = port.get("Type / details", "")
        coverage["timing"] = coverage["timing"] or bool(re.search(r"\b\d+(?:\.\d+)?\s*(?:[GMk]?Hz|ns|us|ms|seconds?|clock cycles?)\b", catalog_description, re.I))
        coverage["qualification"] = coverage["qualification"] or bool(re.search(r"\bactive[-\s]*(?:high|low)\b", catalog_description, re.I))
        if port.get("Direction", "").casefold().strip().startswith("out"):
            coverage["generation behavior"] = any(re.search(pattern, value.meaning.subject, re.I) or
                (value.meaning.predicate in {"produce", "generate", "write", "assert", "set", "send", "output", "deassert", "reset"}
                 and re.search(pattern, " ".join(value.meaning.objects), re.I)) for value in active + passive)
        missing = [field for field, established in coverage.items() if not established]
        assessment = {"block": functional.block, "port_name": name, "direction": port.get("Direction", ""),
                      "supported_relationship_coverage": coverage, "review_dimensions": missing,
                      "approved_requirement_mentions": sorted(record_ids), "retrieval_status": retrieval_status}
        assessments.append(assessment)
        if not missing:
            continue
        spans = [dict(record_id=record.record_id, start=0, end=len(record.text), text=record.text)
                 for record in plan.evidence.records if record.record_id in record_ids]
        mechanism = ("Approved requirement mentions exist, but the supported retained relationships do not establish every reviewed dimension. This can be a projection limitation; source-wide absence is not established."
                     if record_ids else "No named approved requirement support was found within the admitted same-owner scope. This is a bounded review result, not proof of absence in every source.")
        clarification = "Locate or clarify the approved " + ", ".join(missing) + " relationship for " + name + ". If already explicit, correct shared interpretation rather than amend the source."
        value = {"document_type": "Digital IPOS" if functional.domain == "digital" else "Analog IPOS",
                 "block": functional.block, "identity": "approved-port:" + name + ":" + port.get("Direction", ""),
                 "reason": "Signal/port descriptive completeness is not established for: " + ", ".join(missing),
                 "source_spans": spans, "approved_port": dict(port), "assessment": assessment,
                 "provenance": list(dict.fromkeys(["artifacts/stage2_mirco_arc/source_port_catalog.csv",
                     port.get("Source file", ""), *[source for record in plan.evidence.records if record.record_id in record_ids for source in record.provenance]])),
                 "problem_category": DESCRIPTIVE_ISSUE_CATEGORIES[2], "blocking": False,
                 "blocking_reason": "Reporting-only completeness question; no required descriptive-section dependency is established by identifier presence. Existing source-I/O coverage gates remain mandatory.",
                 "unresolved_or_missing_information": ", ".join(missing) + " is not established by supported named relationships. " + mechanism,
                 "clarification_need": clarification, "review_only_proposal_type": "signal/port behavior clarification within approved scope",
                 "recovery_status": "not_established_report_only"}
        value["diagnostic_notes"] = {"what_spec_already_states": "Approved catalog description: " + port.get("Type / details", "") + ". Exact same-owner requirement context is included below.",
            "missing_from_spec": value["unresolved_or_missing_information"], "user_action": clarification,
            "blocking_mechanism": value["blocking_reason"], "signal_register_information": name + "; direction: " + port.get("Direction", "unspecified"),
            "application_scope": "Approved same-owner scope: " + functional.block,
            "required_resolution": "Resolve only the reported dimensions from approved evidence. Do not invent bindings, timing values, polarity or generation rules."}
        if not port.get("Type / details", "").strip():
            value.update(confirmed_missing_information="The approved source-port catalog has no Type / details description for " + name,
                         confirmed_missing_scope="the cited approved catalog row for " + functional.block + " / " + name,
                         confirmed_user_clarification="State the purpose and handling of " + name + " in the approved interface description; do not infer it from the identifier.",
                         confirmed_clarification_type="clarify_output_generation" if port.get("Direction", "").casefold().startswith("out") else "make_actor_explicit")
        populate_report_issue_notes(value)
        issues.append(value)
    return {"version": "signal-port-missing-information-v1", "authority": False, "gate_override": False,
            "specifications_regenerated": False, "scope": "Approved source-port catalog rows in snapshot-materialized blocks; named same-owner admitted requirements only.",
            "limitation": "Conservative review screening, not a complete semantic proof. Parser-limited or unestablished dimensions are not certified missing facts. Timing is reported for review, not assumed applicable to every port.",
            "port_assessments": assessments, "issues": issues, "note_schema": report_note_schema_definition()}


def missing_information_markdown(report):
    lines = ["# Signal And Port Missing-Information Review", "", "For user review only. No source, approval, ownership or gate is changed.", "",
             "Snapshot: " + markdown_literal(report.get("snapshot_id", "test scope")), "", report["scope"], "", report["limitation"], "",
             "Approved ports assessed: " + str(len(report["port_assessments"])), "",
             "Reporting-only issues: " + str(len(report["issues"])), "",
             "| Block | Approved port | Direction | Dimensions needing review |", "| --- | --- | --- | --- |"]
    for value in report["port_assessments"]:
        lines.append("| " + " | ".join(markdown_literal(field) for field in (value["block"], value["port_name"], value["direction"], ", ".join(value["review_dimensions"]) or "none flagged")) + " |")
    review = {"issues": report["issues"], "essential_issue_set": [], "snapshot_id": report.get("snapshot_id", "test scope"),
              "minimum_shared_or_profile_adjustments": {"implemented": [], "remaining": report["limitation"],
                                                       "limitation": "All entries in this standalone report are non-blocking review questions.", "block_preflight": []}}
    lines.extend(["", *descriptive_obligation_review_appendix_markdown(review).splitlines()[2:]])
    return "\n".join(lines) + "\n"


def export_review_document(output, markdown, *, docx_suffix=""):
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise RuntimeError("Pandoc is required for the user-facing DOCX report")
    path = output.with_suffix(".md")
    docx = output.with_name(output.stem + docx_suffix + ".docx")
    path.write_text(markdown, encoding="utf-8")
    subprocess.run([pandoc, str(path), "--from=gfm", "--to=docx", "--standalone", "--toc", "--toc-depth=2",
                    "--metadata=lang:en-US", "--output", str(docx)], check=True)
    return path, docx


def finalize_descriptive_review(review, previous, functional_inputs):
    review["previous_review"] = previous.get("previous_review", previous) if previous else {}
    baseline = review["previous_review"]
    old_issues = [value for key in ("true_descriptive_blockers", "misclassified_nonprose_blockers",
                                  "identifier_normalization_recoverable_cases") for value in baseline.get(key, ())]
    plans = {value.block: build_ipos_claim_plan(value) for value in functional_inputs}
    reclassified = []
    for old in old_issues:
        spans = old.get("source_spans", ())
        matches = [value for value in review["issues"] if value["block"] == old["block"] and spans
                   and all(span in value["source_spans"] for span in spans)]
        plan = plans.get(old["block"])
        retained = {span for claim in plan.claims for span in claim.spans} if plan else set()
        recovered = bool(spans) and all(any(span.record_id == old_span["record_id"] and span.start <= old_span["start"]
                                          and span.end >= old_span["end"] for span in retained) for old_span in spans)
        if matches:
            current = matches[0]
        elif recovered:
            current = dict(old, problem_category=DESCRIPTIVE_ISSUE_CATEGORIES[0], blocking=False,
                           recovery_status="validated_shared_interpretation", blocking_reason="The exact previously unresolved source span now contributes to source-checked retained claims.",
                           unresolved_or_missing_information="No unresolved meaning remains for this admitted span under the current bounded interpretation.",
                           clarification_need="No source amendment required for this recovered relationship.", review_only_proposal_type=None)
            current["diagnostic_notes"] = dict(old.get("diagnostic_notes", {}), blocking_mechanism=current["blocking_reason"],
                                              missing_from_spec=current["unresolved_or_missing_information"], user_action=current["clarification_need"])
            review["issues"].append(current)
        else:
            current = dict(old, problem_category=DESCRIPTIVE_ISSUE_CATEGORIES[5], blocking=False,
                           recovery_status="previous_item_not_proven_recovered", blocking_reason="This historical item has not been proven recovered; withhold independent detail and keep the exact prior evidence for review.",
                           unresolved_or_missing_information="The previous relationship has no verified current retained-span match.",
                           clarification_need="Review the cited source and current shared plan; do not treat historical absence as source damage.", review_only_proposal_type="historical/current span reconciliation")
            review["issues"].append(current)
        reclassified.append({"block": old["block"], "previous_identity": old["identity"],
                            "problem_category": current["problem_category"],
                             "current_disposition": "blocking" if current["blocking"] else current["recovery_status"],
                             "previous_source_spans": spans})
    for value in review["issues"]:
        populate_report_issue_notes(value)
        identity = {key: value[key] for key in ("document_type", "block", "identity", "source_spans")}
        value["issue_id"] = "IPOS-DESC-" + hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    if len({value["issue_id"] for value in review["issues"]}) != len(review["issues"]):
        raise ValueError("Duplicate derived descriptive issue identity")
    review["reclassified_issue_set"] = reclassified
    for key in ("true_descriptive_blockers", "misclassified_nonprose_blockers", "identifier_normalization_recoverable_cases", "issues"):
        for value in review["previous_review"].get(key, ()):
            populate_report_issue_notes(value, historical=True)
    review["categories"] = {category: sum(value["problem_category"] == category for value in review["issues"])
                            for category in DESCRIPTIVE_ISSUE_CATEGORIES}
    review["essential_issue_set"] = [{key: value[key] for key in ("issue_id", "block", "identity", "source_spans")}
                                    for value in review["issues"] if value["blocking"]]


def apply_current_descriptive_review(report, review):
    report.setdefault("historical_document_summary", json.loads(json.dumps(report["documents"])))
    report["issues"] = [value for value in report["issues"] if value.get("origin") != "current_ipos_descriptive_assessment"]
    report["historical_issue_count"] = len(report["issues"])
    for value in report["issues"]:
        populate_report_issue_notes(value, historical=True)
    for value in (*review["issues"], *review.get("artifact_alignment_issues", ())):
        finding = issue(value["document_type"], value["block"] + ": " + value["identity"],
                        [span["record_id"] for span in value["source_spans"]] or [value["identity"]],
                        value.get("problem_category", value["issue_class"]), value["blocking_reason"], value["provenance"])
        finding.update(value, origin="current_ipos_descriptive_assessment")
        finding["conclusion"] = ("Artifact alignment required" if value["issue_class"] == "stale_alignment" else
                     "Need clarification" if value["user_clarification_needed"] != "none" else
                     "Report-only observation" if value["blocking_status"] == "report-only" else
                     "No source clarification needed")
        report["issues"].append(finding)
    report["issue_count"] = len(report["issues"])
    report["issue_counts_by_document"] = dict(Counter(value["document_type"] for value in report["issues"]))
    report["current_descriptive_assessment"] = review
    report["note_schema"] = report_note_schema_definition()
    report["allowed_conclusions"] = sorted(CONCLUSIONS)
    for block in report.get("ipos_closure_review", {}).get("blocks", ()):
        for value in block.get("points", ()):
            populate_report_issue_notes(value, historical=True)
    report["report_updated_at"] = datetime.now().astimezone().isoformat()
    for document in report["documents"]:
        blocks = [value for value in review["minimum_shared_or_profile_adjustments"]["block_preflight"]
                  if value["document_type"] == document["document_type"]]
        if blocks:
            document["blocks"] = blocks
            document["gate_status"] = "PASS" if all(value.get("publication_status") == "PASS" for value in blocks) else "BLOCKED"
            document["generation_status"] = "NOT_REGENERATED_BY_THIS_REVIEW"


def build_artifact_alignment_issues(blocks, snapshot_id):
    issues = []
    for block in blocks:
        if block.get("publication_status") != "FAIL_EXISTING_BLOCK_GATE":
            continue
        output = block["validation_output"]
        value = {"document_type": block["document_type"], "block": block["block"],
                 "identity": "existing-artifact-gate", "reason": output, "gate_output": output,
                 "blocking": True, "source_spans": [], "provenance": ["scripts/validate_ipos_gate.py"],
                 "user_review_only": True}
        value["issue_id"] = "IPOS-ALIGN-" + hashlib.sha256((snapshot_id + ":" + block["document_type"] + ":" + block["block"]).encode("utf-8")).hexdigest()[:16]
        populate_report_issue_notes(value)
        issues.append(value)
    return issues


def markdown_literal(value):
    return re.sub(r"([\\`*_{}\[\]()#+.!|<>:-])", r"\\\1", str(value)).replace("\n", " ")


IPOS_CLOSURE_CLASSES = frozenset({
    "safe to omit", "source clarification needed", "source-model relationship review needed",
    "structured-evidence recovery beyond this step", "not worth pursuing in this step",
})


def ipos_closure_classification(reason, decision="unresolved"):
    if decision in {"excluded", "equivalent_duplicate"}:
        return "safe to omit"
    if "structured/table/procedure" in reason:
        return "structured-evidence recovery beyond this step"
    if "unbalanced source delimiters" in reason or "unresolved subject reference" in reason:
        return "source clarification needed"
    if any(value in reason for value in (
            "relationship_changed", "ambiguous guard", "relative-clause subject", "incomplete predicate")):
        return "source-model relationship review needed"
    return "not worth pursuing in this step"


def apply_ipos_closure_review(report, functional_inputs):
    if report.get("authority") is not False or report.get("gate_override") is not False:
        raise ValueError("Closure review cannot create authority or override gates")
    blocks = []
    for functional in functional_inputs:
        document_type = "Digital IPOS" if functional.domain == "digital" else "Analog IPOS"
        plan = build_ipos_claim_plan(functional)
        findings = ipos_claim_preflight_findings(functional)
        records = {record.record_id: record for record in plan.evidence.records}
        points = []
        for context in plan.evidence.unresolved_contexts:
            points.append((context.context_id, context.reason, context.spans, "unresolved", "context"))
        covered = {(context.reason, context.spans) for context in plan.evidence.unresolved_contexts}
        for index, disposition in enumerate(plan.dispositions):
            if disposition.decision != "preserved" and (disposition.reason, disposition.spans) not in covered:
                points.append(("disposition:" + str(index), disposition.reason, disposition.spans,
                               disposition.decision, "disposition"))
        for finding in findings:
            spans = tuple(span for context in plan.evidence.unresolved_contexts
                          for span in context.spans if span.record_id in finding)
            points.append((finding, finding, spans, "unresolved", "preflight"))
        point_reviews = []
        for identity, reason, spans, decision, population in points:
            classification = ipos_closure_classification(reason, decision)
            if classification not in IPOS_CLOSURE_CLASSES:
                raise ValueError("Unsupported closure classification")
            matches = [value for value in report["issues"] if value["document_type"] == document_type
                       and (value["location"].startswith(functional.block + ":")
                            or value["location"] == functional.block)
                       and ((population == "context" and identity in value["requirement_or_context_references"])
                            or (population == "preflight" and value["blocker_class"] == reason)
                            or (population == "disposition" and value["blocker_class"] == reason
                                and value.get("disposition") == decision
                                and value.get("source_spans", []) == [
                                    {"record_id": span.record_id, "start": span.start,
                                     "end": span.end, "text": span.text} for span in spans]))]
            if not matches:
                sources = list(dict.fromkeys(source for span in spans
                               for source in records[span.record_id].provenance))
                value = issue(document_type, functional.block + ": closure " + population,
                              [identity], reason,
                              "Closure review preserves this exact current finding. No omission approval, "
                              "semantic repair or publication override is implied.",
                              sources or ["scripts/workflow_routing.py"])
                value["issue_id"] = "REVIEW-" + str(len(report["issues"]) + 1).zfill(4)
                value["source_spans"] = [{"record_id": span.record_id, "start": span.start,
                                        "end": span.end, "text": span.text} for span in spans]
                if population == "disposition":
                    value["disposition"] = decision
                report["issues"].append(value)
                matches = [value]
            for value in matches:
                value["closure_classification"] = classification
            point_reviews.append({"identity": identity, "population": population, "reason": reason,
                                  "classification": classification,
                                  "review_ids": [value["issue_id"] for value in matches]})
        blocks.append({"document_type": document_type, "block": functional.block,
                       "supported_claims": len(plan.claims),
                       "unresolved_contexts": len(plan.evidence.unresolved_contexts),
                       "preflight_findings": findings,
                       "partial_generation_decision": "NO-GO" if findings else "GO",
                       "supported_remainder_sufficient_under_current_contract": not bool(findings),
                       "decision_basis": "Existing shared claim preflight blocks writes despite retained claims. "
                                         "Review routing does not authorize omission of unresolved essential evidence."
                                         if findings else "Existing shared claim preflight passes; final block gate remains mandatory.",
                       "classification_counts": dict(Counter(point["classification"] for point in point_reviews)),
                       "points": point_reviews})
    certified = {(document["document_type"], block["block"])
                 for document in report["documents"] for block in document.get("blocks", [])
                 if block.get("publication_status") == "PASS" and block.get("publication_not_certified") is False}
    report["ipos_closure_review"] = {
        "version": 1, "reviewed_at": datetime.now().astimezone().isoformat(),
        "time_box": "At most two days; bounded diagnosis and review routing only in this step.",
        "authority": False, "gate_override": False, "specifications_regenerated": False,
        "classification_notice": "Review routing only. Parser limitations are not proof of damaged source. "
                                 "Source clarification requests concern admitted evidence and do not require blanket reapproval. "
                                 "Safe omission requires an existing excluded disposition; it never overrides an essential gap.",
        "blocks": blocks,
        "minimum_clean_ipos_set": [{"document_type": block["document_type"], "block": block["block"]}
                                   for block in blocks if block["partial_generation_decision"] == "GO"
                                   and (block["document_type"], block["block"]) in certified],
        "recommendation": "Retain the certified clean set. Next review the blocks with the fewest unresolved contexts "
                          "first, then their exact source/model findings. Make only separately authorized bounded shared fixes, "
                          "rerun unchanged preflight and generate one block at a time through the existing generator and gate. "
                          "Defer structured recovery and broad semantic work; do not force Stage 6 completion.",
    }
    report["issue_count"] = len(report["issues"])
    report["issue_counts_by_document"] = dict(Counter(value["document_type"] for value in report["issues"]))
    return report


def report_markdown(report):
    if report.get("authority") is not False or report.get("user_review_only") is not True:
        raise ValueError("Only a review-only, non-authoritative report may be exported")
    if len(report["issues"]) != report["issue_count"]:
        raise ValueError("Report issue count mismatch")
    lines = [
        "# Consolidated Descriptive Issue Report", "",
        "**For user review only. This report does not constitute approved content, authority or specification acceptance.**", "",
        "This report does not modify requirements, approvals, ownership, allocation, traceability or gates. "
        "Excerpts are diagnostic evidence, not approved text for inclusion in specifications. "
        "Any proposals are candidates for user review only.", "",
        "Entries include intentional exclusions, omissions, blockers and publication issues: "
        "the total is not a count of source defects. An out-of-scope exclusion does not demonstrate corruption.", "",
        "Snapshot: " + markdown_literal(report["snapshot_id"]), "",
        "Observed run start: " + markdown_literal(report["run_start"]), "",
        "Total entries: " + str(report["issue_count"]), "",
        "## Document Summary", "",
        "| Document | Gate or generation | Scope | Inline markers | Entries |",
        "| --- | --- | --- | --- | --- |",
    ]
    for document in report["documents"]:
        document_type = document["document_type"]
        values = (document_type, document.get("gate_status") or document.get("generation_status", ""),
                  document.get("scope", ""), document.get("requested_marker_free_publication", ""),
                  report["issue_counts_by_document"].get(document_type, 0))
        lines.append("| " + " | ".join(markdown_literal(value) for value in values) + " |")
    lines.extend(["", "PASS indicates only the recorded gate result. It does not certify the absence of markers "
                  "or the requested completeness. Block-level IPOS results report the existing gate on current files; "
                  "they do not certify the entire stage or other historical files.", "",
                  "## IPOS Block Preflight", "",
                  "| Document | Block | Requirements | Preflight | Unresolved contexts | Observed publication |",
                  "| --- | --- | --- | --- | --- | --- |"])
    for document in report["documents"]:
        for block in document.get("blocks", []):
            values = (document["document_type"], block["block"], block["requirements"],
                      block["preflight"], block["unresolved_contexts"], block.get("publication_status", "NOT_VERIFIED"))
            lines.append("| " + " | ".join(markdown_literal(value) for value in values) + " |")
    closure = report.get("ipos_closure_review")
    if closure:
        lines.extend(["", "## Historical Bounded IPOS Closure Review", "", closure["time_box"], "",
                      closure["classification_notice"], "",
                      "No specification was regenerated by this review. No gate or contract was changed.", "",
                      "| Document | Block | Supported claims | Unresolved contexts | Partial generation |",
                      "| --- | --- | --- | --- | --- |"])
        for block in closure["blocks"]:
            values = (block["document_type"], block["block"], block["supported_claims"],
                      block["unresolved_contexts"], block["partial_generation_decision"])
            lines.append("| " + " | ".join(markdown_literal(value) for value in values) + " |")
        clean = ", ".join(value["document_type"] + ": " + value["block"]
                          for value in closure["minimum_clean_ipos_set"]) or "None certified"
        lines.extend(["", "Historical minimum clean IPOS set (not current certification): " + markdown_literal(clean), "",
                      "### Shortest Next Step", "", closure["recommendation"], ""])
        for block in closure["blocks"]:
            if not block["points"]:
                continue
            lines.extend(["### " + markdown_literal(block["block"]), "", block["decision_basis"], "",
                          "| Exact blocking point | Classification | Review entries |",
                          "| --- | --- | --- |"])
            for point in block["points"]:
                values = (point["identity"] + ": " + point["reason"], point["classification"],
                          ", ".join(point["review_ids"]))
                lines.append("| " + " | ".join(markdown_literal(value) for value in values) + " |")
                if point.get("note_schema_version"):
                    lines.extend(["", *report_issue_note_markdown(point)])
    if report.get("current_descriptive_assessment"):
        lines.extend(["", "## Current IPOS Assessment", "",
                      "Updated: " + markdown_literal(report["report_updated_at"]), "",
                      "Historical entries retained: " + str(report["historical_issue_count"]) + ". Their earlier labels do not override the current assessment.", "",
                      *descriptive_obligation_review_appendix_markdown(report["current_descriptive_assessment"]).splitlines()[2:]])
    lines.extend(["", "## Historical Review Entries" if report.get("current_descriptive_assessment") else "## Allowed Conclusions", ""])
    lines.extend("- " + markdown_literal(value) for value in sorted(CONCLUSIONS))
    for document_type in dict.fromkeys(value["document_type"] for value in report["issues"]):
        lines.extend(["", "## " + markdown_literal(document_type), ""])
        for finding in report["issues"]:
            if finding["document_type"] != document_type or finding.get("origin") == "current_ipos_descriptive_assessment":
                continue
            if finding["conclusion"] not in CONCLUSIONS or finding.get("user_review_only") is not True:
                raise ValueError("Invalid issue review status or conclusion")
            lines.extend(["### " + finding["issue_id"], "",
                          "**Document:** " + markdown_literal(document_type), "",
                          "**Location:** " + markdown_literal(finding["location"]), "",
                          "**Blocker class:** " + markdown_literal(finding["blocker_class"]), "",
                          "**Explanation:** " + markdown_literal(finding["explanation"]), "",
                          ("**Historical conclusion:** " if finding.get("historical_only") else "**Conclusion:** ") + markdown_literal(finding["conclusion"]), "",
                          "**Requirement or context references:**", ""])
            lines.extend("- " + markdown_literal(value) for value in finding["requirement_or_context_references"])
            lines.extend(["", "**Source references:**", ""])
            lines.extend("- " + markdown_literal(value) for value in dict.fromkeys(finding["source_references"]))
            for field, label in (("audit_decision", "Audit decision"), ("disposition", "Disposition"),
                                 ("closure_classification", "Closure classification")):
                if finding.get(field):
                    lines.extend(["", "**" + label + ":** " + markdown_literal(finding[field])])
            if finding.get("note_schema_version"):
                lines.extend(["", *report_issue_note_markdown(finding)])
            excerpts = [("Source excerpt", finding.get("source_excerpt")),
                        ("Generated document excerpt", finding.get("rendered_excerpt")),
                        ("Retained supported content", finding.get("retained_excerpt"))]
            for span in finding.get("source_spans", []):
                label = f"Source fragment: {span['record_id']}; offset {span['start']}:{span['end']}"
                excerpts.append((label, span["text"]))
            for label, text in excerpts:
                if not text:
                    continue
                fence = "`" * max(3, 1 + max((len(value) for value in re.findall(r"`+", text)), default=0))
                lines.extend(["", "**" + markdown_literal(label) + ":**", "", fence + "text", text, fence, ""])
            if finding.get("proposed_clarification"):
                lines.extend(["", "**Candidate proposal for user review; NOT approved:**", "",
                              markdown_literal(finding["proposed_clarification"]), ""])
    return "\n".join(lines) + "\n"


def export_user_report(report, output, *, docx_suffix=""):
    return export_review_document(output, report_markdown(report), docx_suffix=docx_suffix)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--snapshot-id", required=True)
    parser.add_argument("--run-start", required=True, help="Observed workflow timestamp; diagnostic run-window selection only")
    parser.add_argument("--output", type=Path, default=Path("artifacts/orchestrator/cross_spec_issue_report.json"))
    parser.add_argument("--render-only", action="store_true", help="Export the existing JSON report without recollecting issues or rerunning specifications")
    parser.add_argument("--closure-review", action="store_true", help="Add bounded live IPOS triage to the saved report without generating specifications; requires --render-only")
    parser.add_argument("--descriptive-review", action="store_true", help="Refresh six-category consolidated and standalone signal/port reports without regenerating specifications; requires --render-only")
    args = parser.parse_args()
    if (args.closure_review or args.descriptive_review) and not args.render_only:
        parser.error("Review modes require --render-only")
    if args.closure_review and args.descriptive_review:
        parser.error("Select one review mode")
    root = args.repo_root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    if output.resolve() != (root / "artifacts/orchestrator/cross_spec_issue_report.json").resolve():
        raise ValueError("Report output must be the dedicated non-authoritative report path")
    if args.render_only:
        report = json.loads(output.read_text(encoding="utf-8"))
        if report["snapshot_id"] != args.snapshot_id or report["run_start"] != args.run_start:
            raise ValueError("Existing report does not match the requested snapshot and run")
        if args.closure_review or args.descriptive_review:
            context = json.loads((root / "config/project_context.json").read_text(encoding="utf-8"))
            snapshot, _selection = ipos.resolve_complete_authoritative_input(
                root, "6", project_id=str(context.get("project_name") or root.name), snapshot_id=args.snapshot_id)
            contract = ipos.resolve_downstream_contract(root, snapshot.snapshot_id)
            functional_inputs = []
            for domain in ipos.CONFIG:
                candidates = approved_snapshot_candidate_rows(snapshot, contract, domain=domain)
                for name in sorted({row["mapped_block"] for row in candidates}):
                    functional_inputs.append(build_ipos_functional_input(
                        name, ipos._block_inventory_record(root, name),
                        [row for row in candidates if row["mapped_block"] == name], domain=domain,
                        materialized=True, provenance=("approved snapshot", "artifacts/stage2_mirco_arc/block_inventory.csv"),
                        candidate_requirement_rows=candidates))
            if args.descriptive_review:
                protected = [root / "data/canonical/canonical_store.sqlite", *[path for path in (root / "artifacts").rglob("*")
                             if path.is_file() and "orchestrator" not in path.relative_to(root / "artifacts").parts
                             and not (path.name.startswith("~$") and path.suffix.casefold() in {".docx", ".xlsx"})]]
                before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
                review = build_descriptive_obligation_review(functional_inputs)
                review["minimum_shared_or_profile_adjustments"]["snapshot_id"] = snapshot.snapshot_id
                review["snapshot_id"] = snapshot.snapshot_id
                review["report_updated_at"] = datetime.now().astimezone().isoformat()
                review_path = output.with_name("descriptive_obligation_review.json")
                previous = json.loads(review_path.read_text(encoding="utf-8")) if review_path.exists() else {}
                source_port_path = root / "artifacts/stage2_mirco_arc/source_port_catalog.csv"
                with source_port_path.open(encoding="utf-8-sig", newline="") as handle:
                    missing = build_missing_information_report(functional_inputs, list(csv.DictReader(handle)))
                missing["snapshot_id"] = snapshot.snapshot_id
                review["issues"].extend(missing["issues"])
                finalize_descriptive_review(review, previous, functional_inputs)
                for block in review["minimum_shared_or_profile_adjustments"]["block_preflight"]:
                    domain = "digital" if block["document_type"] == "Digital IPOS" else "analog"
                    block.update(observe_ipos_block_publication(root, domain, block["block"], snapshot.snapshot_id, args.run_start, require_run_freshness=False))
                    functional = next(value for value in functional_inputs if value.block == block["block"] and value.domain == domain)
                    block.update(requirements=len(functional.local_requirement_ids), preflight=block["preflight_status"],
                                 unresolved_contexts=block["remaining_textual_dispositions"], specifications_regenerated=False)
                review["artifact_alignment_issues"] = build_artifact_alignment_issues(
                    review["minimum_shared_or_profile_adjustments"]["block_preflight"], snapshot.snapshot_id)
                attach_ipos_decision_trace(root, review)
                review["issues"].extend(build_current_probe_failure_issues(review, functional_inputs))
                review["categories"] = {category: sum(value["problem_category"] == category for value in review["issues"])
                                        for category in DESCRIPTIVE_ISSUE_CATEGORIES}
                review["effective_descriptive_blocker_set"] = [{key: value[key] for key in ("issue_id", "block", "reason", "source_spans", "blocking_reason")}
                                                              for value in review["issues"] if value["blocking_status"] == "blocking"]
                review["decision_summary"] = ipos_decision_summary(review)
                apply_current_descriptive_review(report, review)
                missing_path = output.with_name("signal_port_missing_information_report.json")
                review_path.write_text(json.dumps(review, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
                missing_path.write_text(json.dumps(missing, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
                output.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
                appendix_path = output.with_name("descriptive_obligation_review_appendix.json")
                appendix_path.write_text(json.dumps(review, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
                export_review_document(appendix_path, descriptive_obligation_review_appendix_markdown(review))
                export_review_document(review_path, descriptive_obligation_review_markdown(review), docx_suffix="_updated")
                export_review_document(missing_path, missing_information_markdown(missing))
                markdown, docx = export_user_report(report, output, docx_suffix="_updated")
                changed = [path.relative_to(root).as_posix() for path, digest in before.items()
                           if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest]
                if changed:
                    raise RuntimeError("Reporting modified protected authority/specification artifacts: " + "; ".join(changed))
                print(json.dumps({"report": str(output), "markdown": str(markdown), "docx": str(docx), "categories": review["categories"],
                                  "essential_issues": len(review["essential_issue_set"]), "historical_entries": report["historical_issue_count"],
                                  "approved_ports_assessed": len(missing["port_assessments"]), "port_review_issues": len(missing["issues"]),
                                  "protected_artifacts_unchanged": len(before), "authority": False, "specifications_regenerated": review["specifications_regenerated"],
                                  "blocks": [{key: value[key] for key in ("block", "preflight_status", "publication_status")} for value in review["minimum_shared_or_profile_adjustments"]["block_preflight"]]}, indent=2))
                return
            apply_ipos_closure_review(report, functional_inputs)
            output.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    else:
        report = generate_report(root, args.snapshot_id, args.run_start)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    markdown, docx = export_user_report(report, output)
    print(json.dumps({"report": str(output), "markdown": str(markdown), "docx": str(docx), "issues": report["issue_count"],
                      "counts": report["issue_counts_by_document"], "authority": False}, indent=2))


if __name__ == "__main__":
    main()