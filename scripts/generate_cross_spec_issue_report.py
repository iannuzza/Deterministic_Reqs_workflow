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
from datetime import datetime
from pathlib import Path

import generate_ipos_specs as ipos
from spec_document_contract import PUBLICATION_REVIEW_MARKERS, drs_document_events
from workflow_routing import (
    approved_snapshot_candidate_rows, build_ipos_claim_plan,
    build_ipos_functional_input, ipos_claim_preflight_findings,
)


CONCLUSIONS = frozenset({
    "Need clarification", "Functionality not clear from approved source",
    "Source-model relationship needs review", "Structured evidence not sufficiently recoverable",
    "Candidate clarification proposal for user review",
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


def observe_ipos_block_publication(repo_root, domain, block, snapshot_id, run_start):
    folder = repo_root / ipos.CONFIG[domain]["output_dir"] / "blocks" / ipos._block_slug(block)
    markdown = folder / ipos._block_markdown_name(domain, block)
    artifacts = (markdown, markdown.with_suffix(".docx"))
    if any(not path.is_file() or path.stat().st_mtime < datetime.fromisoformat(run_start).timestamp()
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


def markdown_literal(value):
    return re.sub(r"([\\`*_{}\[\]()#+.!|<>:-])", r"\\\1", str(value)).replace("\n", " ")


def report_markdown(report):
    if report.get("authority") is not False or report.get("user_review_only") is not True:
        raise ValueError("Only a review-only, non-authoritative report may be exported")
    if len(report["issues"]) != report["issue_count"]:
        raise ValueError("Report issue count mismatch")
    lines = [
        "# Report centralizzato delle issue descrittive", "",
        "**Solo per revisione utente. Non costituisce contenuto approvato, autorita o accettazione delle specifiche.**", "",
        "Questo report non modifica requisiti, approvazioni, ownership, allocation, traceability o gate. "
        "Gli estratti sono evidenza diagnostica, non testo approvato da inserire nelle specifiche. "
        "Eventuali proposte sono esclusivamente candidate per la revisione utente.", "",
        "Le voci includono esclusioni intenzionali, omissioni, blocchi e problemi di pubblicazione: "
        "il totale non equivale al numero di difetti sorgente. Un'esclusione per scope non dimostra corruzione.", "",
        "Snapshot: " + markdown_literal(report["snapshot_id"]), "",
        "Inizio del run osservato: " + markdown_literal(report["run_start"]), "",
        "Voci totali: " + str(report["issue_count"]), "",
        "## Sintesi per documento", "",
        "| Documento | Gate o generazione | Scope | Marker inline | Voci |",
        "| --- | --- | --- | --- | --- |",
    ]
    for document in report["documents"]:
        document_type = document["document_type"]
        values = (document_type, document.get("gate_status") or document.get("generation_status", ""),
                  document.get("scope", ""), document.get("requested_marker_free_publication", ""),
                  report["issue_counts_by_document"].get(document_type, 0))
        lines.append("| " + " | ".join(markdown_literal(value) for value in values) + " |")
    lines.extend(["", "PASS indica soltanto l'esito del gate registrato. Non certifica l'assenza di marker "
                  "o la completezza richiesta. I risultati IPOS per blocco riportano il gate esistente sui file correnti; "
                  "non certificano l'intero stage o gli altri file storici.", "",
                  "## Preflight dei blocchi IPOS", "",
                  "| Documento | Blocco | Requisiti | Preflight | Contesti irrisolti | Pubblicazione osservata |",
                  "| --- | --- | --- | --- | --- | --- |"])
    for document in report["documents"]:
        for block in document.get("blocks", []):
            values = (document["document_type"], block["block"], block["requirements"],
                      block["preflight"], block["unresolved_contexts"], block.get("publication_status", "NOT_VERIFIED"))
            lines.append("| " + " | ".join(markdown_literal(value) for value in values) + " |")
    lines.extend(["", "## Conclusioni ammesse", ""])
    lines.extend("- " + markdown_literal(value) for value in sorted(CONCLUSIONS))
    for document_type in dict.fromkeys(value["document_type"] for value in report["issues"]):
        lines.extend(["", "## " + markdown_literal(document_type), ""])
        for finding in report["issues"]:
            if finding["document_type"] != document_type:
                continue
            if finding["conclusion"] not in CONCLUSIONS or finding.get("user_review_only") is not True:
                raise ValueError("Invalid issue review status or conclusion")
            lines.extend(["### " + finding["issue_id"], "",
                          "**Documento:** " + markdown_literal(document_type), "",
                          "**Posizione:** " + markdown_literal(finding["location"]), "",
                          "**Classe del blocco:** " + markdown_literal(finding["blocker_class"]), "",
                          "**Spiegazione:** " + markdown_literal(finding["explanation"]), "",
                          "**Conclusione:** " + markdown_literal(finding["conclusion"]), "",
                          "**Riferimenti a requisiti o contesti:**", ""])
            lines.extend("- " + markdown_literal(value) for value in finding["requirement_or_context_references"])
            lines.extend(["", "**Riferimenti sorgente:**", ""])
            lines.extend("- " + markdown_literal(value) for value in dict.fromkeys(finding["source_references"]))
            for field in ("audit_decision", "disposition"):
                if finding.get(field):
                    lines.extend(["", "**" + field + ":** " + markdown_literal(finding[field])])
            excerpts = [("Estratto sorgente", finding.get("source_excerpt")),
                        ("Estratto del documento generato", finding.get("rendered_excerpt")),
                        ("Contenuto supportato mantenuto", finding.get("retained_excerpt"))]
            for span in finding.get("source_spans", []):
                label = f"Frammento sorgente: {span['record_id']}; offset {span['start']}:{span['end']}"
                excerpts.append((label, span["text"]))
            for label, text in excerpts:
                if not text:
                    continue
                fence = "`" * max(3, 1 + max((len(value) for value in re.findall(r"`+", text)), default=0))
                lines.extend(["", "**" + markdown_literal(label) + ":**", "", fence + "text", text, fence, ""])
            if finding.get("proposed_clarification"):
                lines.extend(["", "**Proposta candidata per revisione utente; NON approvata:**", "",
                              markdown_literal(finding["proposed_clarification"]), ""])
    return "\n".join(lines) + "\n"


def export_user_report(report, output):
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        raise RuntimeError("Pandoc is required for the user-facing DOCX report")
    markdown = output.with_suffix(".md")
    docx = output.with_suffix(".docx")
    markdown.write_text(report_markdown(report), encoding="utf-8")
    subprocess.run([pandoc, str(markdown), "--from=gfm", "--to=docx", "--standalone",
                    "--toc", "--toc-depth=2", "--metadata=lang:it-IT", "--output", str(docx)], check=True)
    return markdown, docx


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--snapshot-id", required=True)
    parser.add_argument("--run-start", required=True, help="Observed workflow timestamp; diagnostic run-window selection only")
    parser.add_argument("--output", type=Path, default=Path("artifacts/orchestrator/cross_spec_issue_report.json"))
    parser.add_argument("--render-only", action="store_true", help="Export the existing JSON report without recollecting issues or rerunning specifications")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    if output.resolve() != (root / "artifacts/orchestrator/cross_spec_issue_report.json").resolve():
        raise ValueError("Report output must be the dedicated non-authoritative report path")
    if args.render_only:
        report = json.loads(output.read_text(encoding="utf-8"))
        if report["snapshot_id"] != args.snapshot_id or report["run_start"] != args.run_start:
            raise ValueError("Existing report does not match the requested snapshot and run")
    else:
        report = generate_report(root, args.snapshot_id, args.run_start)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    markdown, docx = export_user_report(report, output)
    print(json.dumps({"report": str(output), "markdown": str(markdown), "docx": str(docx), "issues": report["issue_count"],
                      "counts": report["issue_counts_by_document"], "authority": False}, indent=2))


if __name__ == "__main__":
    main()