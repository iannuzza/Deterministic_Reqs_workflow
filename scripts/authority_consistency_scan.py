"""Static consistency scan for reusable workflow authority boundaries."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

AUTHORITATIVE_HINTS = ("run_stage", "generate_", "workflow_cli", "validate_", "report", "sysml")
LEGACY_NAMES = ("load_approved_input", "freeze_legacy_export")
LOCAL_RESOURCE_MARKERS = ("STOPWORDS", "_STOPWORDS", "analog_terms", "digital_terms", "BLOCK_ALIASES", "USER_APPROVED_REQUIREMENT_IDS")
PROJECT_ID_RE = re.compile(r"(?:DDS_STBIO1|STBIOSystem|STBIO_[A-Za-z0-9_]+)")
MUTABLE_READ_RE = re.compile(r"(?:DictReader\(|read_text\(|json\.load[s]?\()")


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    line: int
    message: str


def _is_authoritative(path: Path) -> bool:
    return any(hint in path.name.lower() for hint in AUTHORITATIVE_HINTS)


def scan(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted((repo_root / "scripts").glob("*.py")):
        if path.name == "authority_consistency_scan.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
        except OSError:
            continue
        authoritative = _is_authoritative(path)
        explicit_legacy_boundary = "legacy=True" in text or "allow_legacy=True" in text
        for number, line in enumerate(lines, start=1):
            if any(name in line for name in LEGACY_NAMES) and authoritative and "def " not in line and "legacy" not in line.lower() and not explicit_legacy_boundary:
                findings.append(Finding("critical", "legacy_authority_bypass", path.relative_to(repo_root).as_posix(), number, "Legacy compatibility resolver referenced by an authoritative-looking module."))
            if authoritative and PROJECT_ID_RE.search(line):
                findings.append(Finding("important", "hardcoded_project_identifier", path.relative_to(repo_root).as_posix(), number, "Project-specific identifier appears in reusable/authoritative-looking code."))
            if any(marker in line for marker in LOCAL_RESOURCE_MARKERS) and ("=" in line or "{" in line) and path.name != "approved_vocabulary.py":
                findings.append(Finding("important", "embedded_lexical_resource", path.relative_to(repo_root).as_posix(), number, "Local vocabulary, alias, stopword, or project approval constant should be configuration-backed."))
            if authoritative and MUTABLE_READ_RE.search(line) and ("artifacts" in line or "summary" in line or "profile" in line):
                findings.append(Finding("important", "mutable_artifact_read", path.relative_to(repo_root).as_posix(), number, "Authoritative-looking module reads a mutable artifact directly; verify approved resolver boundary."))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan reusable workflow code for authority and project-specific assumptions.")
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", default="artifacts/validation/authority_consistency_scan.json")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    findings = scan(root)
    payload = {"repo_root": str(root), "finding_count": len(findings), "findings": [asdict(item) for item in findings]}
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for item in findings:
        print(f"{item.severity.upper()} {item.code} {item.path}:{item.line} {item.message}")
    return 1 if args.strict and any(item.severity == "critical" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
