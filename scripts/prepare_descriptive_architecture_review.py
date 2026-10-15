"""Prepare indexed descriptive content in the existing architecture review package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sqlite3
import tempfile
from pathlib import Path

from mapping_review_sync import write_descriptive_review_sheet, reviewed_descriptive_context
from stage1_descriptive_evidence import extract_indexed_descriptive_candidates
from validate_stage2_profile import _draft_review_sha256


def prepare(root: Path, ingestion: Path, page: int, section: str, owner: str,
            domain: str, revision_id: str, snapshot_id: str, backup: Path) -> dict:
    metadata = json.loads((ingestion / "source_metadata.json").read_text(encoding="utf-8"))
    index_path = ingestion / "ocr_index.csv"
    with index_path.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if int(row["page"]) == page
                and Path(row["source_file"]).name == metadata["source_spec"]]
    if len(rows) != 1:
        raise ValueError("The indexed source page is not unique.")
    artifact = Path(rows[0]["text_file"])
    if not artifact.is_absolute():
        artifact = (index_path.parent / artifact).resolve(strict=True)
    db = root / "data/canonical/canonical_store.sqlite"
    db_hash = hashlib.sha256(db.read_bytes()).hexdigest()
    with sqlite3.connect(db.as_uri() + "?mode=ro", uri=True) as connection:
        connection.row_factory = sqlite3.Row
        snapshot = connection.execute("SELECT * FROM snapshots WHERE snapshot_id=?", (snapshot_id,)).fetchone()
        if snapshot is None or snapshot["status"] != "approved":
            raise ValueError("An existing approved snapshot is required as the unchanged review baseline.")
        revision = connection.execute(
            "SELECT r.*,s.source_name,s.project_id FROM source_revisions r JOIN source_specs s "
            "ON s.source_spec_id=r.source_spec_id WHERE r.source_revision_id=?", (revision_id,)
        ).fetchone()
        if revision is None or revision["project_id"] != snapshot["project_id"]:
            raise ValueError("Registered source revision does not belong to the selected project.")
        revision_metadata = json.loads(revision["metadata_json"])
        if (revision["source_name"] != metadata["source_spec"]
                or revision["revision_number"] != metadata["source_revision"]
                or revision["revision_date"] != metadata["source_revision_date"]
                or revision_metadata.get("ingestion_id") != metadata["ingestion_id"]):
            raise ValueError("Registered revision differs from ingestion metadata.")
    with tempfile.TemporaryDirectory() as directory:
        selected_index = Path(directory) / "index.csv"
        with selected_index.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=["source_file", "page", "text_file"])
            writer.writeheader()
            writer.writerow({"source_file": rows[0]["source_file"], "page": rows[0]["page"], "text_file": str(artifact)})
        candidates = extract_indexed_descriptive_candidates(selected_index, source_context={rows[0]["source_file"]: {
            "source_revision": metadata["source_revision"], "source_revision_id": revision_id,
            "ingestion_id": metadata["ingestion_id"],
        }})
    candidates = [record for record in candidates if record["section"] == section]
    if len(candidates) != 1:
        raise ValueError("The requested descriptive section must yield exactly one candidate.")
    record = dict(candidates[0], source_spec_id=revision["source_spec_id"],
                  source_revision_date=revision["revision_date"],
                  source_revision_fingerprint=revision["content_fingerprint"],
                  proposed_mapped_block=owner, proposed_domain=domain,
                  required_for_review=True,
                  review_decision="pending", mapped_block="", domain="", review_rationale="")
    lines = artifact.read_text(encoding="utf-8-sig").splitlines()
    if lines and lines[0].strip().isdigit():
        record["printed_page"] = lines[0].strip()
    folder = root / "artifacts/stage1_specs"
    draft_path = folder / "architecture_profile_draft.json"
    workbook_path = folder / "architecture_mapping_preview.xlsx"
    request_path = folder / "architecture_profile_approval_request.md"
    profile_path = root / "config/stage2_mirco_arc_profile.json"
    profile_hash = hashlib.sha256(profile_path.read_bytes()).hexdigest()
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    if owner not in profile.get("block_defs", {}):
        raise ValueError("Proposed owner is not in the existing architecture profile.")
    if draft.get("governed_source_context", {}).get("records"):
        raise ValueError("Existing descriptive candidates must be preserved and reviewed separately.")
    if workbook_path.with_name("~$" + workbook_path.name).exists():
        raise ValueError("Save and close the architecture workbook before preparing review.")
    backup.mkdir(parents=True, exist_ok=False)
    for path in (draft_path, workbook_path, request_path):
        shutil.copy2(path, backup / path.name)
    draft["governed_source_context"] = {"version": 1, "records": [record]}
    draft["review_package"]["draft_profile_sha256"] = _draft_review_sha256(draft)
    try:
        write_descriptive_review_sheet(workbook_path, draft)
        reviewed_descriptive_context(workbook_path, draft, profile)
        draft_path.write_text(json.dumps(draft, indent=2) + "\n", encoding="utf-8")
        request_path.write_text(request_path.read_text(encoding="utf-8") +
            "\n## Pending Supplementary Descriptive Content\n\n"
            "Review Descriptive Content Review in the existing architecture workbook. This is not a new approval lane. "
            "Do not approve through the IPOS blocker workbook or user clarified.\n\n"
            f"Baseline snapshot (unchanged): `{snapshot_id}`. Candidate decision: pending. "
            f"Proposed owner/domain: {owner} / {domain}.\n\n"
            f"Exact extracted passage:\n\n> {record['statement']}\n\n"
            f"Provenance:\n\n```json\n{json.dumps(record, indent=2)}\n```\n\n"
            "Explicitly set review_decision, mapped_block, domain and review_rationale; save and close Excel. "
            "Only explicit architecture-profile approval and successful validation permit a subsequent new snapshot.\n",
            encoding="utf-8")
    except Exception:
        for path in (draft_path, workbook_path, request_path):
            shutil.copy2(backup / path.name, path)
        raise
    if db_hash != hashlib.sha256(db.read_bytes()).hexdigest() or profile_hash != hashlib.sha256(profile_path.read_bytes()).hexdigest():
        raise RuntimeError("Authority changed while preparing review; inspect concurrent activity.")
    return {"record": record, "canonical_db_unchanged": True, "approved_profile_unchanged": True,
            "review_workbook": str(workbook_path), "backup": str(backup)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("root", "ingestion", "backup"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--page", type=int, required=True)
    for name in ("section", "owner", "source-revision-id", "snapshot-id"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--domain", choices=("digital", "analog", "mixed_signal", "system"), required=True)
    args = parser.parse_args()
    result = prepare(args.root.resolve(), args.ingestion.resolve(), args.page, args.section,
                     args.owner, args.domain, args.source_revision_id, args.snapshot_id, args.backup.resolve())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()