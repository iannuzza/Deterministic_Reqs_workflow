#!/usr/bin/env python3
"""Convert Stage 3 SRS Markdown files into a single LaTeX document.

Default behavior:
- reads all *.md in artifacts/stage3_srs
- also includes the micro-architecture diagram from artifacts/stage2_mirco_arc when available
- writes artifacts/stage3_srs/stage2_srs_combined.tex
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import List

from workflow_routing import document_author_name


DEFAULT_INPUT_DIR = Path("artifacts/stage3_srs")
DEFAULT_OUTPUT_TEX = Path("artifacts/stage3_srs/stage2_srs_combined.tex")
DEFAULT_DIAGRAM_MD = Path("artifacts/stage2_mirco_arc/micro_architecture_block_diagram.md")


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = text
    for src, dst in replacements.items():
        out = out.replace(src, dst)
    return out


def _md_heading_to_latex(line: str) -> str | None:
    m = re.match(r"^(#{1,6})\s+(.*)$", line)
    if not m:
        return None

    level = len(m.group(1))
    title = _escape_latex(m.group(2).strip())
    mapping = {
        1: "section",
        2: "subsection",
        3: "subsubsection",
        4: "paragraph",
        5: "subparagraph",
        6: "textbf",
    }

    cmd = mapping[level]
    if cmd == "textbf":
        return "\\textbf{" + title + "}"
    return "\\" + cmd + "{" + title + "}"


def _convert_markdown_lines(lines: List[str]) -> List[str]:
    out: List[str] = []
    in_code = False
    in_itemize = False

    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\n")
        line = line.lstrip("\ufeff")

        if line.strip().startswith("```"):
            if not in_code:
                if in_itemize:
                    out.append("\\end{itemize}")
                    out.append("")
                    in_itemize = False
                out.append("\\begin{verbatim}")
                in_code = True
            else:
                out.append("\\end{verbatim}")
                out.append("")
                in_code = False
            i += 1
            continue

        if in_code:
            out.append(line)
            i += 1
            continue

        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*[-: ]+\|", lines[i + 1].strip()):
            if in_itemize:
                out.append("\\end{itemize}")
                out.append("")
                in_itemize = False

            header = [c.strip() for c in line.strip().strip("|").split("|")]
            cols = len(header)
            aligns = "|" + "|".join(["p{0.22\\textwidth}" for _ in range(cols)]) + "|"
            out.append("\\begin{longtable}{" + aligns + "}")
            out.append("\\hline")
            out.append(" & ".join(_escape_latex(c) for c in header) + r" \\")
            out.append("\\hline")
            out.append("\\endfirsthead")
            out.append("\\hline")
            out.append(" & ".join(_escape_latex(c) for c in header) + r" \\")
            out.append("\\hline")
            out.append("\\endhead")
            i += 2
            while i < len(lines):
                row_line = lines[i].rstrip("\n")
                if not row_line.startswith("|"):
                    break
                row = [c.strip() for c in row_line.strip().strip("|").split("|")]
                if len(row) < cols:
                    row.extend([""] * (cols - len(row)))
                if len(row) > cols:
                    row = row[:cols]
                out.append(" & ".join(_escape_latex(c) for c in row) + r" \\")
                out.append("\\hline")
                i += 1
            out.append("\\end{longtable}")
            out.append("")
            continue

        heading = _md_heading_to_latex(line)
        if heading is not None:
            if in_itemize:
                out.append("\\end{itemize}")
                out.append("")
                in_itemize = False
            out.append(heading)
            out.append("")
            i += 1
            continue

        if re.match(r"^\s*[-*]\s+", line):
            item_text = re.sub(r"^\s*[-*]\s+", "", line)
            if not in_itemize:
                out.append("\\begin{itemize}")
                in_itemize = True
            out.append("\\item " + _escape_latex(item_text))
            i += 1
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            num_text = re.sub(r"^\s*\d+\.\s+", "", line)
            if not in_itemize:
                out.append("\\begin{itemize}")
                in_itemize = True
            out.append("\\item " + _escape_latex(num_text))
            i += 1
            continue

        if in_itemize and line.strip() == "":
            out.append("\\end{itemize}")
            out.append("")
            in_itemize = False
            i += 1
            continue

        if line.strip() == "":
            out.append("")
        else:
            out.append(_escape_latex(line))
        i += 1

    if in_itemize:
        out.append("\\end{itemize}")
        out.append("")

    return out


def _collect_markdown_files(input_dir: Path, external_diagram_md: Path | None = None) -> List[Path]:
    files = sorted(input_dir.glob("*.md"))
    if not files and not (external_diagram_md and external_diagram_md.exists()):
        return []

    preferred = [
        input_dir / "system_requirements_specification.md",
    ]
    if external_diagram_md and external_diagram_md.exists():
        preferred.append(external_diagram_md)
    preferred.append(input_dir / "micro_architecture_block_diagram.md")

    ordered: List[Path] = []
    seen = set()
    for p in preferred:
        if p.exists() and p not in seen:
            ordered.append(p)
            seen.add(p)
    for p in files:
        if p not in seen:
            ordered.append(p)
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Stage 3 SRS markdown files to a single LaTeX file")
    parser.add_argument("--input-dir", default=str(DEFAULT_INPUT_DIR), help="Directory containing stage3_srs markdown files")
    parser.add_argument("--output-tex", default=str(DEFAULT_OUTPUT_TEX), help="Output LaTeX file path")
    parser.add_argument(
        "--diagram-md",
        default=str(DEFAULT_DIAGRAM_MD),
        help="Path to micro-architecture diagram markdown to include after SRS main document",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    input_dir = (repo_root / args.input_dir).resolve()
    output_tex = (repo_root / args.output_tex).resolve()
    diagram_md = (repo_root / args.diagram_md).resolve()

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"SRS md->latex: FAIL (missing input dir: {input_dir})")
        _append_log(repo_root, script_name, f"FAIL missing_input_dir={input_dir}")
        return 1

    md_files = _collect_markdown_files(input_dir, diagram_md)
    if not md_files:
        print(f"SRS md->latex: FAIL (no markdown files in {input_dir})")
        _append_log(repo_root, script_name, f"FAIL no_markdown_files={input_dir}")
        return 1

    latex_lines: List[str] = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage{geometry}",
        r"\usepackage{longtable}",
        r"\usepackage{array}",
        r"\usepackage{hyperref}",
        r"\geometry{margin=1in}",
        r"\setlength{\parskip}{0.5em}",
        r"\setlength{\parindent}{0pt}",
        "",
        r"\title{Stage 2 SRS Combined Document}",
        r"\author{" + _escape_latex(document_author_name()) + r"}",
        r"\date{" + datetime.now().strftime("%Y-%m-%d") + r"}",
        "",
        r"\begin{document}",
        r"\thispagestyle{empty}",
        r"\null",
        r"\newpage",
        r"\tableofcontents",
        r"\newpage",
        "",
    ]

    for md_file in md_files:
        rel = md_file.relative_to(repo_root).as_posix()
        latex_lines.append(r"\section*{Source: " + _escape_latex(rel) + "}")
        latex_lines.append(r"\addcontentsline{toc}{section}{Source: " + _escape_latex(rel) + "}")
        latex_lines.append("")

        lines = md_file.read_text(encoding="utf-8-sig").splitlines(True)
        latex_lines.extend(_convert_markdown_lines(lines))
        latex_lines.append("")

    latex_lines.append(r"\end{document}")

    output_tex.parent.mkdir(parents=True, exist_ok=True)
    output_tex.write_text("\n".join(latex_lines) + "\n", encoding="utf-8")

    print("SRS md->latex: PASS")
    print(f"- Input dir: {input_dir}")
    print(f"- Markdown files: {len(md_files)}")
    print(f"- Output tex: {output_tex}")

    _append_log(
        repo_root,
        script_name,
        f"PASS md_files={len(md_files)} output={output_tex.as_posix()}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

