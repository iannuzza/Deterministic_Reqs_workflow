#!/usr/bin/env python3
"""Stage supplementary PDF requirement sources without changing the primary corpus."""

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
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from pypdf import PdfReader

from merge_engine import merge_staging_batch, register_staged_ingestion


NORMATIVE_RE = re.compile(r"\b(?:shall|must|required to|is required to)\b", re.IGNORECASE)
TAG_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:[_-][A-Z0-9]+)+\b")
TAGGED_REQUIREMENT_HEADER_RE = re.compile(
    r"\[\s*(?P<id>[A-Z][A-Z0-9]*(?:[_-][A-Z0-9]+)*_?\s*\d+)\s*\]\s*REQUIREMENT\s*: ?",
    re.IGNORECASE,
)
TRAILING_INCOMPLETE_WORDS = {
    "and", "or", "to", "of", "for", "in", "on", "at", "with", "from",
    "that", "the", "a", "an", "be", "shall", "must",
}
REVIEW_FIELDS = [
    "staged_id", "source_req_id", "requirement_statement", "source_spec", "source_revision",
    "source_page", "source_chunk_id", "req_class", "classification", "matched_canonical_id", "match_reason",
    "recommended_action", "review_decision", "reviewer_notes",
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "source"


def _normalized(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value.lower()).split())


def _similarity(left: str, right: str) -> float:
    left_terms, right_terms = set(_normalized(left).split()), set(_normalized(right).split())
    return len(left_terms & right_terms) / len(left_terms | right_terms) if left_terms and right_terms else 0.0


def _normalize_tagged_lines(lines: List[str]) -> List[str]:
    """Join OCR line breaks that split a tagged header or its numeric suffix."""
    normalized: List[str] = []
    index = 0
    while index < len(lines):
        current = " ".join(lines[index].split())
        if index + 1 < len(lines) and "[" in current and "]" not in current:
            current = f"{current} {lines[index + 1].strip()}"
            index += 1
        normalized.append(current)
        index += 1
    return normalized


def _is_complete_statement(statement: str) -> bool:
    words = re.findall(r"[A-Za-z0-9]+", statement)
    return len(words) >= 7 and words[-1].lower() not in TRAILING_INCOMPLETE_WORDS and not statement.rstrip().endswith((":", ",", "-", "("))


def _validate_staged_bodies(staged: List[Dict[str, str]], page_texts: List[str]) -> None:
    """Fail ingestion when a tagged body is not source-terminated and complete."""
    failures = []
    for row in staged:
        page_text = "\n".join(_normalize_tagged_lines(page_texts[int(row["source_page"]) - 1].splitlines()))
        header = next((match for match in TAGGED_REQUIREMENT_HEADER_RE.finditer(page_text)
                       if re.sub(r"\s+", "", match.group("id")).upper() == row["source_req_id"].upper()), None)
        end = page_text.upper().find("[END]", header.end()) if header else -1
        if header is None or end < 0 or not _is_complete_statement(row["requirement_statement"]):
            failures.append(f"{row['source_req_id']}@p{row['source_page']}")
    if failures:
        raise ValueError("Supplementary body preservation validation failed: " + ", ".join(failures))


def _write_csv(path: Path, fields: Iterable[str], rows: Iterable[Dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def discover_tag_pattern(page_texts: List[str]) -> str:
    """Discover the tagged-header convention directly from source text."""
    tags = [match.group("id") for text in page_texts for match in TAGGED_REQUIREMENT_HEADER_RE.finditer(text)]
    if not tags:
        raise ValueError("No bracketed tagged REQUIREMENT headers found in source specification.")
    normalized_tags = [re.sub(r"\s+", "", tag) for tag in tags]
    prefix = Counter(tag.rsplit("_", 1)[0] for tag in normalized_tags).most_common(1)[0][0]
    return re.escape(prefix) + r"_\d+"


def _write_workbook(csv_path: Path) -> None:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Source Ingestion Review"
    for row in rows:
        worksheet.append(row)
    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for row in worksheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    headers = [str(cell.value or "").strip() for cell in worksheet[1]]
    if worksheet.max_row >= 2:
        if "classification" in headers:
            classification_column = get_column_letter(headers.index("classification") + 1)
            classification_validation = DataValidation(
                type="list",
                formula1='"System,Digital,Analog,Block"',
                allow_blank=False,
            )
            classification_validation.errorTitle = "Invalid classification"
            classification_validation.error = "Select System, Digital, Analog, or Block from the dropdown."
            classification_validation.promptTitle = "Classification"
            classification_validation.prompt = "Select the reviewed source classification; Block routes to block-level review."
            classification_validation.showErrorMessage = True
            classification_validation.showInputMessage = True
            worksheet.add_data_validation(classification_validation)
            classification_validation.add(f"{classification_column}2:{classification_column}{worksheet.max_row}")
        if "review_decision" in headers:
            decision_column = get_column_letter(headers.index("review_decision") + 1)
            decision_validation = DataValidation(
                type="list",
                formula1='"pending,approved,rejected,needs_clarification"',
                allow_blank=False,
            )
            decision_validation.errorTitle = "Invalid review decision"
            decision_validation.error = "Select pending, approved, rejected, or needs_clarification from the dropdown."
            decision_validation.promptTitle = "Review decision"
            decision_validation.prompt = "Select approved only after reviewing the classification and source text."
            decision_validation.showErrorMessage = True
            decision_validation.showInputMessage = True
            worksheet.add_data_validation(decision_validation)
            decision_validation.add(f"{decision_column}2:{decision_column}{worksheet.max_row}")
    if "review_decision" in headers:
        decision_column = headers.index("review_decision") + 1
        pending_fill = PatternFill("solid", fgColor="FCE4D6")
        approved_fill = PatternFill("solid", fgColor="E2F0D9")
        for row_index in range(2, worksheet.max_row + 1):
            decision = str(worksheet.cell(row=row_index, column=decision_column).value or "").strip().lower()
            worksheet.cell(row=row_index, column=decision_column).fill = (
                approved_fill if decision == "approved" else pending_fill
            )
    for column in worksheet.columns:
        worksheet.column_dimensions[get_column_letter(column[0].column)].width = min(max(len(str(cell.value or "")) for cell in column) + 2, 60)
    workbook.save(csv_path.with_suffix(".xlsx"))


def _default_review_classification(row: Dict[str, str]) -> str:
    """Provide a review default without conflating source comparison with domain classification."""
    evidence = " ".join((row.get("source_req_id") or "", row.get("source_spec") or "")).lower()
    return "Digital" if "main_controller" in evidence or "main_ctrl" in evidence else "System"


def migrate_review_schema(ingestion_dir: Path) -> Path:
    """Upgrade a legacy supplementary review CSV/XLSX while preserving user decisions."""
    review_path = ingestion_dir / "comparison_results.csv"
    rows = _read_csv(review_path)
    if not rows:
        raise ValueError(f"No review rows found: {review_path}")
    workbook_path = review_path.with_suffix(".xlsx")
    if "req_class" in rows[0] and workbook_path.exists():
        return _sync_saved_review_workbook(ingestion_dir)
    if "req_class" not in rows[0]:
        for row in rows:
            row["req_class"] = row.get("classification") or "new"
            row["classification"] = _default_review_classification(row)
    else:
        for row in rows:
            row["req_class"] = row.get("req_class") or "new"
            row["classification"] = row.get("classification") or _default_review_classification(row)
    _write_csv(review_path, REVIEW_FIELDS, rows)
    _write_workbook(review_path)
    return review_path


def _sync_saved_review_workbook(ingestion_dir: Path) -> Path:
    """Use the user-saved review workbook as the authoritative input for a merge."""
    review_path = ingestion_dir / "comparison_results.csv"
    workbook_path = review_path.with_suffix(".xlsx")
    if not workbook_path.exists():
        return review_path
    with review_path.open("r", encoding="utf-8-sig", newline="") as handle:
        fieldnames = csv.DictReader(handle).fieldnames or []
    workbook = load_workbook(workbook_path, data_only=False)
    try:
        worksheet = workbook["Source Ingestion Review"]
        values = list(worksheet.iter_rows(values_only=True))
        headers = [str(value or "").strip() for value in values[0]] if values else []
        if headers != fieldnames:
            raise ValueError("Saved comparison_results.xlsx columns do not match comparison_results.csv.")
        rows = [
            dict(zip(fieldnames, ["" if value is None else str(value).strip() for value in row]))
            for row in values[1:]
            if any(value is not None and str(value).strip() for value in row)
        ]
        if "review_decision" in headers:
            decision_column = headers.index("review_decision") + 1
            approved_fill = PatternFill("solid", fgColor="E2F0D9")
            pending_fill = PatternFill("solid", fgColor="FCE4D6")
            for row_index, row in enumerate(rows, start=2):
                worksheet.cell(row=row_index, column=decision_column).fill = (
                    approved_fill if row["review_decision"].casefold() == "approved" else pending_fill
                )
        with review_path.open("r", encoding="utf-8-sig", newline="") as handle:
            current_rows = [
                {key: (value or "").strip() for key, value in row.items()}
                for row in csv.DictReader(handle)
            ]
        if current_rows != rows:
            _write_csv(review_path, fieldnames, rows)
        workbook.save(workbook_path)
        return review_path
    finally:
        workbook.close()


def stage_source(repo_root: Path, source: Path, revision: str, revision_date: str = "") -> Path:
    existing_batches = []
    for metadata_path in (repo_root / "artifacts" / "source_ingestion").glob("*/source_metadata.json"):
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if (
            metadata.get("source_spec") == source.name
            and str(metadata.get("source_revision", "")).strip() == revision.strip()
            and metadata_path.parent.joinpath("comparison_results.xlsx").exists()
        ):
            existing_batches.append(metadata_path.parent)
    if existing_batches:
        return max(existing_batches, key=lambda path: path.stat().st_mtime)
    previous_batches = []
    for metadata_path in (repo_root / "artifacts" / "source_ingestion").glob("*/source_metadata.json"):
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if metadata.get("source_spec") == source.name and str(metadata.get("source_revision", "")).strip() != revision.strip():
            previous_batches.append(metadata_path.parent)
    previous_batch = max(previous_batches, key=lambda path: path.stat().st_mtime) if previous_batches else None
    previous_reviews = {}
    if previous_batch:
        previous_reviews = {row.get("source_req_id", ""): row for row in _read_csv(previous_batch / "comparison_results.csv")}
    texts = [(page.extract_text() or "").strip() for page in PdfReader(str(source)).pages]
    tag_pattern = discover_tag_pattern(texts)
    ingestion_id = f"{_slug(source.stem)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output = repo_root / "artifacts" / "source_ingestion" / ingestion_id
    output.mkdir(parents=True)
    extracts_dir = output / "ocr_extracts"
    extracts_dir.mkdir()
    source_name = source.name
    staged = []
    raw_rows = []
    for page_no, text in enumerate(texts, start=1):
        raw_rows.append({"source_spec": source_name, "page": page_no, "text": text})
        page_path = extracts_dir / f"{source.stem}_p{page_no:03d}.txt"
        page_path.write_text(text + "\n", encoding="utf-8")
        lines = _normalize_tagged_lines([line for line in text.splitlines() if line.strip()])
        for line_no, line in enumerate(lines, start=1):
            tag = TAGGED_REQUIREMENT_HEADER_RE.search(line)
            if tag:
                body = [line[tag.end():].strip()]
                terminated = False
                for following in lines[line_no:]:
                    if "[END]" in following.upper():
                        before_end = following[:following.upper().find("[END]")].strip()
                        if before_end:
                            body.append(before_end)
                        terminated = True
                        break
                    body.append(following)
                statement = " ".join(part for part in body if part).strip()
                if not terminated or not NORMATIVE_RE.search(statement):
                    continue
                source_req_id = re.sub(r"\s+", "", tag.group("id"))
                candidate = {
                    "staged_id": f"{ingestion_id}:{source_req_id}",
                    "source_req_id": source_req_id, "requirement_statement": statement,
                    "source_spec": source_name, "source_revision": revision,
                    "source_page": str(page_no), "source_chunk_id": f"p{page_no:03d}:l{line_no}",
                    "ingested_at": _now(), "ingestion_id": ingestion_id,
                }
                existing = next((item for item in staged if item["source_req_id"] == source_req_id), None)
                if existing is None or len(_normalized(candidate["requirement_statement"])) > len(_normalized(existing["requirement_statement"])):
                    if existing is not None:
                        staged.remove(existing)
                    staged.append(candidate)
    _validate_staged_bodies(staged, texts)
    canonical_path = repo_root / "artifacts" / "stage1_requirements" / "requirements_summary.csv"
    with canonical_path.open("r", encoding="utf-8-sig", newline="") as handle:
        canonical = list(csv.DictReader(handle))
    review = []
    for candidate in staged:
        exact = next((row for row in canonical if _normalized(row.get("requirement_statement", "")) == _normalized(candidate["requirement_statement"])), None)
        best = max(canonical, key=lambda row: _similarity(candidate["requirement_statement"], row.get("requirement_statement", "")), default={})
        score = _similarity(candidate["requirement_statement"], best.get("requirement_statement", "")) if best else 0.0
        if exact or score >= 0.82:
            req_class, matched, reason = "duplication", (exact or best).get("id", ""), "exact or normalized near duplicate"
        elif score >= 0.45:
            req_class, matched, reason = "refines", best.get("id", ""), f"normalized lexical overlap={score:.2f}"
        else:
            req_class, matched, reason = "new", "", "no deterministic overlap"
        previous = previous_reviews.get(candidate["source_req_id"], {})
        unchanged = bool(previous and _normalized(previous.get("requirement_statement", "")) == _normalized(candidate["requirement_statement"]))
        review_decision = previous.get("review_decision", "") if unchanged else ("pending" if req_class == "new" else "approved")
        review.append({
            **candidate,
            "req_class": req_class,
            "classification": previous.get("classification", "System") if unchanged else "System",
            "matched_canonical_id": matched,
            "match_reason": reason,
            "recommended_action": "manual_review",
            "review_decision": review_decision or "pending",
            "reviewer_notes": previous.get("reviewer_notes", "") if unchanged else "",
        })
    _write_csv(output / "raw_ocr_pages.csv", ["source_spec", "page", "text"], raw_rows)
    _write_csv(
        output / "ocr_index.csv",
        ["source_file", "page", "text_file", "status"],
        [{"source_file": str(source), "page": row["page"], "text_file": str(extracts_dir / f"{source.stem}_p{int(row['page']):03d}.txt"), "status": "text-extracted"} for row in raw_rows],
    )
    _write_csv(output / "normalized_requirements.csv", list(staged[0]) if staged else ["staged_id", "source_req_id", "requirement_statement"], staged)
    review_path = output / "comparison_results.csv"
    _write_csv(review_path, REVIEW_FIELDS, review)
    _write_workbook(review_path)
    comparison_rows = []
    current_by_id = {row["source_req_id"]: row for row in staged}
    for source_req_id in sorted(set(previous_reviews) | set(current_by_id)):
        previous = previous_reviews.get(source_req_id, {})
        current = current_by_id.get(source_req_id, {})
        previous_text = previous.get("requirement_statement", "")
        current_text = current.get("requirement_statement", "")
        status = "unchanged" if previous_text and current_text and _normalized(previous_text) == _normalized(current_text) else ("added" if current_text and not previous_text else ("removed" if previous_text and not current_text else "changed"))
        comparison_rows.append({"source_req_id": source_req_id, "previous_revision": previous.get("source_revision", ""), "previous_statement": previous_text, "current_revision": revision, "current_statement": current_text, "change_status": status})
    _write_csv(output / "revision_comparison.csv", ["source_req_id", "previous_revision", "previous_statement", "current_revision", "current_statement", "change_status"], comparison_rows)
    metadata = {"ingestion_id": ingestion_id, "source_spec": source_name, "source_revision": revision, "source_revision_date": revision_date, "tag_pattern": tag_pattern, "staged_at": _now(), "counts": {kind: sum(row["req_class"] == kind for row in review) for kind in ("new", "duplication", "refines", "conflict", "removed")}}
    (output / "source_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    register_staged_ingestion(repo_root, output)
    print(json.dumps({"ingestion_dir": str(output), **metadata["counts"]}, indent=2))
    return output


def merge_source(repo_root: Path, ingestion_dir: Path, conflict_winner_ids: tuple[str, ...] = ()) -> None:
    """Merge only explicitly approved review rows and rebuild the shared local index."""
    _sync_saved_review_workbook(ingestion_dir)
    staging_batch_id = register_staged_ingestion(repo_root, ingestion_dir)
    metadata_path = ingestion_dir / "source_metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    context_path = repo_root / "config" / "project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}
    project_id = str(metadata.get("project_id") or context.get("project_name") or repo_root.name)
    canonical_result = merge_staging_batch(
        repo_root,
        project_id=project_id,
        staging_batch_id=staging_batch_id,
        approved_by=str(metadata.get("approved_by") or "legacy-review"),
        conflict_winner_ids=conflict_winner_ids,
    )
    review_rows = _read_csv(ingestion_dir / "comparison_results.csv")
    approved_rows = [
        row for row in review_rows
        if row.get("review_decision", "").strip().lower() == "approved"
    ]
    if not approved_rows:
        raise ValueError("No approved rows in comparison_results.csv; edit the review workbook/CSV before merge.")
    staged_by_id = {row["staged_id"]: row for row in _read_csv(ingestion_dir / "normalized_requirements.csv")}
    corpus = repo_root / "artifacts" / "stage1_requirements" / "integrated_requirements.csv"
    primary = repo_root / "artifacts" / "stage1_requirements" / "requirements_summary.csv"
    existing = _read_csv(corpus) if corpus.exists() else _read_csv(primary)
    fields = list(dict.fromkeys([key for row in existing for key in row] + [key for row in staged_by_id.values() for key in row] + ["req_class", "classification"]))
    existing_ids = {
        (row.get("source_req_id") or row.get("id") or row.get("canonical_id") or "").strip()
        for row in existing
    }
    # Repeated approvals must be idempotent: one source requirement ID gets one corpus row.
    deduplicated_existing = []
    for row in existing:
        row_id = (row.get("source_req_id") or row.get("id") or row.get("canonical_id") or "").strip()
        if row_id and row_id in {(
            item.get("source_req_id") or item.get("id") or item.get("canonical_id") or ""
        ).strip() for item in deduplicated_existing}:
            continue
        deduplicated_existing.append(row)
    additions = []
    addition_ids = set(existing_ids)
    for row in approved_rows:
        candidate = staged_by_id.get(row["staged_id"])
        if candidate is None:
            continue
        candidate_id = (candidate.get("source_req_id") or candidate.get("id") or candidate.get("staged_id") or "").strip()
        if candidate_id in addition_ids:
            continue
        candidate["classification"] = row.get("classification", "").strip()
        candidate["req_class"] = row.get("req_class") or row.get("classification", "")
        candidate["id"] = candidate.get("id") or candidate["staged_id"]
        additions.append(candidate)
        addition_ids.add(candidate_id)
    for row in additions:
        row["id"] = row.get("id") or row["staged_id"]
    _write_csv(corpus, fields, [*deduplicated_existing, *additions])
    combined_index = repo_root / "artifacts" / "stage1_requirements" / "integrated_ocr_index.csv"
    primary_index = repo_root / "artifacts" / "stage1_requirements" / "ocr_extracts" / "index.csv"
    _write_csv(combined_index, ["source_file", "page", "text_file", "status"], [*_read_csv(primary_index), *_read_csv(ingestion_dir / "ocr_index.csv")])
    command = [sys.executable, str(repo_root / "scripts" / "build_rag_index.py"), "--source-index", str(combined_index), "--db-path", str(repo_root / context["rag_db_path"]), "--manifest", str(repo_root / context["rag_manifest_path"])]
    subprocess.run(command, cwd=repo_root, check=True)
    manifest = {"merged_at": _now(), "ingestion_dir": str(ingestion_dir), "approved_count": len(additions), "corpus": str(corpus), "combined_index": str(combined_index), "canonical_merge": canonical_result}
    (ingestion_dir / "merge_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage a supplementary tagged PDF source specification.")
    parser.add_argument("command", choices=("stage", "merge"))
    parser.add_argument("--source", help="Supplementary PDF source specification")
    parser.add_argument("--revision", help="Source revision identifier")
    parser.add_argument("--revision-date", default="", help="Source revision date; separate from ingestion timestamp")
    parser.add_argument("--ingestion-dir", help="Staged ingestion directory to merge")
    parser.add_argument(
        "--conflict-winner-id",
        action="append",
        default=[],
        help="Explicitly approve a staged ID as the winner of a same-ID text conflict; repeat for multiple conflicts",
    )
    parser.add_argument("--migrate-review-schema", action="store_true", help="Upgrade comparison_results.csv/.xlsx to separate req_class and classification columns")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    if args.migrate_review_schema:
        ingestion_dir = Path(args.ingestion_dir or "").resolve()
        if not ingestion_dir.exists():
            parser.error("--migrate-review-schema requires --ingestion-dir <existing directory>")
        print(migrate_review_schema(ingestion_dir))
    elif args.command == "stage":
        source = Path(args.source or "").resolve()
        if not source.exists() or source.suffix.lower() != ".pdf" or not args.revision:
            parser.error("stage requires --source <PDF> and --revision <revision>")
        stage_source(repo_root, source, args.revision, args.revision_date)
    else:
        ingestion_dir = Path(args.ingestion_dir or "").resolve()
        if not ingestion_dir.exists():
            parser.error("merge requires --ingestion-dir <existing directory>")
        merge_source(repo_root, ingestion_dir, tuple(args.conflict_winner_id))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())