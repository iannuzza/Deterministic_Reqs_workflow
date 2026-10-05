#!/usr/bin/env python3
"""Generic OCR extraction entry point.

Bootstraps stage-1 OCR inputs from an initial specification source in specs/.
Supported source types: PDF and HTML.
"""

import argparse
import csv
from datetime import datetime
import html as html_lib
import json
from pathlib import Path
import re
import zipfile
from typing import Optional

from pypdf import PdfReader


STAGE2_PROFILE = Path("config/stage2_mirco_arc_profile.json")
TAXONOMY_REPORT = Path("artifacts/stage1_requirements/taxonomy_crosscheck.md")

_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "into",
    "using",
    "through",
    "that",
    "this",
    "shall",
    "must",
    "mode",
    "data",
    "input",
    "output",
    "signal",
    "status",
    "control",
    "behavior",
    "interface",
    "manager",
}

_SHORT_ALLOWED = {"spi", "i2c", "i3c", "adc", "dac", "pwm", "pll", "i2s", "can", "lin", "usb", "sda", "scl"}


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _validate_initial_spec(candidate: Path) -> None:
    if not candidate.exists() or candidate.suffix.lower() not in {".pdf", ".html", ".htm", ".docx"}:
        raise FileNotFoundError(f"Initial specification not found or unsupported type: {candidate}")


def _load_project_context(repo_root: Path) -> dict:
    config_path = repo_root / "config/project_context.json"
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _find_initial_spec(
    spec_dir: Path,
    explicit_spec: Optional[str],
    explicit_pdf: Optional[str],
    repo_root: Path,
) -> Path:
    # Keep backward compatibility with --initial-pdf while preferring --initial-spec.
    selected = explicit_spec or explicit_pdf
    if selected:
        candidate = Path(selected)
        if not candidate.is_absolute():
            candidate = repo_root / candidate
        _validate_initial_spec(candidate)
        return candidate

    project_context = _load_project_context(repo_root)
    configured_spec = (project_context.get("source_spec_path") or "").strip()
    if configured_spec:
        candidate = Path(configured_spec)
        if not candidate.is_absolute():
            candidate = repo_root / candidate
        _validate_initial_spec(candidate)
        return candidate

    candidates = sorted(
        [
            *spec_dir.glob("*.html"),
            *spec_dir.glob("*.htm"),
            *spec_dir.glob("*.pdf"),
            *spec_dir.glob("*.docx"),
        ]
    )
    if not candidates:
        raise FileNotFoundError(f"No supported specification files found in spec folder: {spec_dir}")
    return candidates[0]


def _extract_full_pdf_text(initial_pdf: Path, out_dir: Path) -> tuple[list[list[str]], int, int]:
    reader = PdfReader(str(initial_pdf))
    rows: list[list[str]] = []
    non_empty_pages = 0

    for page_num, page in enumerate(reader.pages, start=1):
        extracted = page.extract_text() or ""
        extracted = extracted.strip()

        text_file = out_dir / f"{initial_pdf.stem}_p{page_num:03d}.txt"
        if extracted:
            non_empty_pages += 1
            status = "text-extracted"
            content = extracted + "\n"
        else:
            status = "empty-page"
            content = (
                "# No extractable text found on this page\n"
                f"source_pdf={initial_pdf.as_posix()}\n"
                f"page={page_num}\n"
                "note=page may require image OCR engine (tesseract)\n"
            )

        text_file.write_text(content, encoding="utf-8")
        rows.append([initial_pdf.as_posix(), str(page_num), text_file.as_posix(), status])

    return rows, len(reader.pages), non_empty_pages


def _extract_text_from_html_fragment(fragment: str) -> str:
    no_script = re.sub(r"<script\\b[^>]*>.*?</script>", " ", fragment, flags=re.IGNORECASE | re.DOTALL)
    no_style = re.sub(r"<style\\b[^>]*>.*?</style>", " ", no_script, flags=re.IGNORECASE | re.DOTALL)
    with_breaks = re.sub(r"</(p|div|section|br|li|tr|h[1-6])>", "\\n", no_style, flags=re.IGNORECASE)
    no_tags = re.sub(r"<[^>]+>", " ", with_breaks)
    unescaped = html_lib.unescape(no_tags)
    compact = re.sub(r"[\\t\\r ]+", " ", unescaped)
    compact = re.sub(r"\\n\\s*\\n+", "\\n", compact)
    return compact.strip()


def _extract_full_html_text(initial_html: Path, out_dir: Path) -> tuple[list[list[str]], int, int]:
    html_text = initial_html.read_text(encoding="utf-8", errors="ignore")
    # Most converted specs use one <section class="page"> per page.
    pages = re.split(r"(?i)<section[^>]*class=[\"']page[\"'][^>]*>", html_text)
    page_fragments = pages[1:] if len(pages) > 1 else [html_text]

    rows: list[list[str]] = []
    non_empty_pages = 0

    for page_num, fragment in enumerate(page_fragments, start=1):
        extracted = _extract_text_from_html_fragment(fragment)

        text_file = out_dir / f"{initial_html.stem}_p{page_num:03d}.txt"
        if extracted:
            non_empty_pages += 1
            status = "text-extracted"
            content = extracted + "\n"
        else:
            status = "empty-page"
            content = (
                "# No extractable text found on this page\n"
                f"source_html={initial_html.as_posix()}\n"
                f"page={page_num}\n"
                "note=page may require source conversion cleanup\n"
            )

        text_file.write_text(content, encoding="utf-8")
        rows.append([initial_html.as_posix(), str(page_num), text_file.as_posix(), status])

    return rows, len(page_fragments), non_empty_pages


def _extract_full_docx_text(initial_docx: Path, out_dir: Path) -> tuple[list[list[str]], int, int]:
    try:
        with zipfile.ZipFile(initial_docx) as archive:
            xml_bytes = archive.read("word/document.xml")
    except Exception as exc:
        raise RuntimeError(f"Unable to read DOCX content: {exc}") from exc

    xml_text = xml_bytes.decode("utf-8", errors="ignore")
    # Preserve paragraph boundaries before stripping tags.
    with_breaks = re.sub(r"</w:p>", "\n", xml_text, flags=re.IGNORECASE)
    no_tags = re.sub(r"<[^>]+>", " ", with_breaks)
    unescaped = html_lib.unescape(no_tags)
    compact = re.sub(r"[\t\r ]+", " ", unescaped)
    compact = re.sub(r"\n\s*\n+", "\n", compact).strip()

    text_file = out_dir / f"{initial_docx.stem}_p001.txt"
    if compact:
        status = "text-extracted"
        content = compact + "\n"
        non_empty_pages = 1
    else:
        status = "empty-page"
        content = (
            "# No extractable text found in DOCX\n"
            f"source_docx={initial_docx.as_posix()}\n"
            "page=1\n"
            "note=docx may contain non-text objects only\n"
        )
        non_empty_pages = 0

    text_file.write_text(content, encoding="utf-8")
    rows = [[initial_docx.as_posix(), "1", text_file.as_posix(), status]]
    return rows, 1, non_empty_pages


def _write_taxonomy_report(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _camel_tokens(name: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)
    return [t.lower() for t in re.split(r"[^a-zA-Z0-9]+", spaced) if t]


def _normalize_term(term: str) -> str:
    cleaned = re.sub(r"[^a-z0-9_\- ]+", " ", term.lower()).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def _term_allowed(term: str) -> bool:
    if not term:
        return False
    if term in _SHORT_ALLOWED:
        return True
    if term in _STOPWORDS:
        return False
    return len(term) >= 4


def _derive_terms_for_block(block_name: str, meta: dict) -> list[str]:
    terms: list[str] = []

    for token in _camel_tokens(block_name):
        if _term_allowed(token):
            terms.append(token)

    text_fields = [
        str(meta.get("function", "")),
        str(meta.get("inputs", "")),
        str(meta.get("outputs", "")),
    ]
    joined = " ".join(text_fields)
    # Keep single words and compact short phrases (1-3 words) that can be searched in source text.
    words = [_normalize_term(w) for w in re.findall(r"[A-Za-z0-9_\-]+", joined)]
    for w in words:
        if _term_allowed(w):
            terms.append(w)

    phrases = re.findall(r"\b([a-zA-Z0-9_\-]+(?:\s+[a-zA-Z0-9_\-]+){1,2})\b", joined)
    for ph in phrases:
        ph_norm = _normalize_term(ph)
        if ph_norm and all(_term_allowed(p) for p in ph_norm.split()):
            terms.append(ph_norm)

    unique: list[str] = []
    seen = set()
    for t in terms:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique


def _update_taxonomy_rules_from_spec(repo_root: Path, initial_spec: Path, rows: list[list[str]]) -> None:
    profile_path = repo_root / STAGE2_PROFILE
    report_path = repo_root / TAXONOMY_REPORT

    if not profile_path.exists():
        raise FileNotFoundError(f"Missing Stage 2 profile: {profile_path}")

    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    block_defs = profile.get("block_defs", {})
    mapping_rules = profile.get("mapping_rules", {})
    if not isinstance(block_defs, dict) or not isinstance(mapping_rules, dict):
        raise ValueError("Invalid Stage 2 profile: block_defs/mapping_rules must be objects")

    spec_parts: list[str] = []
    for row in rows:
        if len(row) < 3:
            continue
        text_path = Path(row[2])
        if text_path.exists():
            spec_parts.append(text_path.read_text(encoding="utf-8", errors="ignore"))
    spec_text = "\n".join(spec_parts).lower()

    removed_legacy_keys: list[str] = []
    for key in list(mapping_rules.keys()):
        if key != "Unassigned" and key not in block_defs:
            removed_legacy_keys.append(key)
            del mapping_rules[key]

    detected_signals: list[str] = []
    updates: list[str] = []
    for block_name, meta in block_defs.items():
        if block_name == "Unassigned":
            continue

        derived_terms = _derive_terms_for_block(block_name, meta if isinstance(meta, dict) else {})
        hits = [term for term in derived_terms if term in spec_text]
        if not hits:
            continue

        detected_signals.append(f"{block_name}: {', '.join(hits)}")

        existing_terms = mapping_rules.get(block_name, [])
        if not isinstance(existing_terms, list):
            existing_terms = []

        normalized_existing = {str(t).strip().lower() for t in existing_terms if str(t).strip()}
        added = [term for term in hits if term not in normalized_existing]
        if added:
            mapping_rules[block_name] = existing_terms + added
            updates.append(f"{block_name}: +{', '.join(added)}")

    profile["mapping_rules"] = mapping_rules
    profile_path.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")

    report_lines = [
        "# Stage 1 Taxonomy Crosscheck",
        "",
        f"- Source spec: {initial_spec.as_posix()}",
        f"- Stage 2 profile: {STAGE2_PROFILE.as_posix()}",
    ]
    if removed_legacy_keys:
        report_lines.append(f"- Removed legacy mapping keys: {', '.join(sorted(set(removed_legacy_keys)))}")
    else:
        report_lines.append("- Removed legacy mapping keys: none")

    if detected_signals:
        report_lines.append("- Detected domain signals from source spec:")
        for item in detected_signals:
            report_lines.append(f"  - {item}")
    else:
        report_lines.append("- Detected domain signals from source spec: none")

    if updates:
        report_lines.append("- Applied mapping_rules updates:")
        for item in updates:
            report_lines.append(f"  - {item}")
    else:
        report_lines.append("- Applied mapping_rules updates: none")

    _write_taxonomy_report(report_path, report_lines)
    print(f"Taxonomy crosscheck report: {report_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare OCR extraction index from spec source (PDF/HTML/DOCX)")
    parser.add_argument("--spec-folder", default="specs", help="Folder containing specification sources")
    parser.add_argument("--initial-spec", default=None, help="Specific initial spec path to use (.pdf/.html/.docx)")
    parser.add_argument("--initial-pdf", default=None, help="Deprecated alias for --initial-spec")
    args = parser.parse_args()

    scripts_dir = Path(__file__).resolve().parent
    repo_root = scripts_dir.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    spec_dir = Path(args.spec_folder)
    if not spec_dir.is_absolute():
        spec_dir = repo_root / spec_dir
    spec_dir = spec_dir.resolve()

    if spec_dir == scripts_dir or scripts_dir in spec_dir.parents:
        print(f"Invalid spec folder location: {spec_dir}")
        print(f"Spec folder must not be under scripts folder: {scripts_dir}")
        _append_log(repo_root, script_name, f"FAIL invalid spec folder location: {spec_dir}")
        return 1

    if not spec_dir.exists():
        print(f"Spec folder not found: {spec_dir}")
        _append_log(repo_root, script_name, f"FAIL spec folder not found: {spec_dir}")
        return 1

    try:
        initial_spec = _find_initial_spec(spec_dir, args.initial_spec, args.initial_pdf, repo_root)
    except FileNotFoundError as exc:
        print(str(exc))
        _append_log(repo_root, script_name, f"FAIL {exc}")
        return 1

    out_dir = repo_root / "artifacts/stage1_requirements/ocr_extracts"
    out_dir.mkdir(parents=True, exist_ok=True)

    if initial_spec.suffix.lower() == ".pdf":
        rows, total_pages, non_empty_pages = _extract_full_pdf_text(initial_spec, out_dir)
    elif initial_spec.suffix.lower() == ".docx":
        try:
            rows, total_pages, non_empty_pages = _extract_full_docx_text(initial_spec, out_dir)
        except RuntimeError as exc:
            print(str(exc))
            _append_log(repo_root, script_name, f"FAIL {exc}")
            return 1
    else:
        rows, total_pages, non_empty_pages = _extract_full_html_text(initial_spec, out_dir)

    index = out_dir / "index.csv"
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source_file", "page", "text_file", "status"])
        writer.writerows(rows)

    print(f"Prepared OCR output folder: {out_dir}")
    print(f"Initial specification: {initial_spec}")
    print(f"Total pages: {total_pages}")
    print(f"Pages with extractable text: {non_empty_pages}")
    print(f"Generated OCR index: {index}")

    _append_log(
        repo_root,
        script_name,
        (
            "PASS "
            f"initial_spec={initial_spec.as_posix()} "
            f"pages={total_pages} non_empty_pages={non_empty_pages} "
            f"index={index.as_posix()}"
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
