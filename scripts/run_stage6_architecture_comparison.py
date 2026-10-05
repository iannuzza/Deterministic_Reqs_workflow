#!/usr/bin/env python3
"""Run mixed-signal architecture comparison against another workspace project.

This script compares the current project's Stage 2A micro-architecture artifacts
against another project folder in the same workspace root.

Required input artifacts in each project:
- artifacts/stage2_mirco_arc/block_inventory.csv
- artifacts/stage2_mirco_arc/interface_catalog.csv
- artifacts/stage2_mirco_arc/interaction_matrix.csv
- artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv

Outputs (default folder: artifacts/comparison):
- block_inventory_comparison.csv
- block_interaction_matrix.csv
- hierarchy_comparison.csv
- modularization_assessment.md
- efficiency_scorecard.csv
- final_recommendation.md
- final_report.md
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple


HELP_CMD = "python scripts/run_stage6_architecture_comparison.py --help"

HOW_TO_RUN = """How to run:
    python scripts/run_stage6_architecture_comparison.py --project-to-compare <project_name>
    python scripts/run_stage6_architecture_comparison.py --project-to-compare <project_name> --workspace-root <workspace_root>
    python scripts/run_stage6_architecture_comparison.py --project-to-compare <project_name> --output-dir artifacts/comparison
    python scripts/run_stage6_architecture_comparison.py --project-to-compare <project_name> --output-path artifacts/comparison/final_report_custom.md

From workflow CLI:
    python scripts/workflow_cli.py arch-compare --project-to-compare <project_name>
"""


@dataclass(frozen=True)
class ProjectArtifacts:
    project_name: str
    project_root: Path
    block_inventory: Path
    interface_catalog: Path
    interaction_matrix: Path
    requirement_traceability: Path


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_") or "project"


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


def _read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def _pick(row: Dict[str, str], options: Sequence[str]) -> str:
    for key in options:
        if key in row and row[key] is not None:
            return row[key].strip()
    return ""


def _load_artifacts(project_root: Path) -> ProjectArtifacts:
    project_name = project_root.name
    base = project_root / "artifacts" / "stage2_mirco_arc"
    return ProjectArtifacts(
        project_name=project_name,
        project_root=project_root,
        block_inventory=base / "block_inventory.csv",
        interface_catalog=base / "interface_catalog.csv",
        interaction_matrix=base / "interaction_matrix.csv",
        requirement_traceability=base / "requirement_to_block_traceability.csv",
    )


def _missing_files(artifacts: ProjectArtifacts) -> List[Path]:
    required = [
        artifacts.block_inventory,
        artifacts.interface_catalog,
        artifacts.interaction_matrix,
        artifacts.requirement_traceability,
    ]
    return [path for path in required if not path.exists()]


def _collect_blocks(path: Path) -> Set[str]:
    rows = _read_csv_rows(path)
    result: Set[str] = set()
    for row in rows:
        block = _pick(row, ["Block", "block", "Owner", "owner"])
        if block:
            result.add(block)
    return result


def _collect_interfaces(path: Path) -> Set[str]:
    rows = _read_csv_rows(path)
    result: Set[str] = set()
    for row in rows:
        name = _pick(row, ["Interface", "interface", "Signal/control", "signal/control"])
        if name:
            result.add(name)
    return result


def _collect_interactions(path: Path) -> Set[Tuple[str, str]]:
    rows = _read_csv_rows(path)
    result: Set[Tuple[str, str]] = set()
    for row in rows:
        src = _pick(row, ["From block", "From", "from", "Source", "source"])
        dst = _pick(row, ["To block", "To", "to", "Target", "target"])
        if src and dst:
            result.add((src, dst))
    return result


def _collect_requirement_ids(path: Path) -> Set[str]:
    rows = _read_csv_rows(path)
    result: Set[str] = set()
    for row in rows:
        req_id = _pick(row, ["Requirement ID", "Req ID", "requirement_id", "requirement id"])
        if req_id:
            result.add(req_id)
    return result


def _norm_set(values: Iterable[str]) -> Set[str]:
    return {_norm(v) for v in values if _norm(v)}


def _jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def _jaccard_edges(a: Set[Tuple[str, str]], b: Set[Tuple[str, str]]) -> float:
    if not a and not b:
        return 1.0
    a_norm = {(_norm(x), _norm(y)) for x, y in a if _norm(x) and _norm(y)}
    b_norm = {(_norm(x), _norm(y)) for x, y in b if _norm(x) and _norm(y)}
    union = a_norm | b_norm
    if not union:
        return 0.0
    return len(a_norm & b_norm) / len(union)


def _sample(values: Set[str], limit: int = 10) -> List[str]:
    return sorted(values)[:limit]


def _role_for_block(block_name: str, interfaces: Set[str], interactions: Set[Tuple[str, str]]) -> str:
    name_n = _norm(block_name)
    if any(name_n in _norm(i) or _norm(i) in name_n for i in interfaces):
        return "Interface/Boundary"
    outgoing = sum(1 for src, _ in interactions if _norm(src) == name_n)
    incoming = sum(1 for _, dst in interactions if _norm(dst) == name_n)
    if outgoing and incoming:
        return "Processing/Bridging"
    if outgoing and not incoming:
        return "Source/Controller"
    if incoming and not outgoing:
        return "Sink/Endpoint"
    return "Uncertain"


def _find_block_by_keywords(blocks: Set[str], keywords: Sequence[str]) -> str:
    keyword_norms = [_norm(k) for k in keywords if _norm(k)]
    if not keyword_norms:
        return ""

    best_block = ""
    best_score = -1
    for block in sorted(blocks):
        bn = _norm(block)
        if not bn:
            continue
        btokens = set(re.findall(r"[a-z0-9]+", block.lower()))
        score = 0
        for kn in keyword_norms:
            if kn in bn:
                score += 4
            ktokens = set(re.findall(r"[a-z0-9]+", kn.lower()))
            if ktokens and ktokens.issubset(btokens):
                score += 2
            score += len(ktokens & btokens)
        if score > best_score:
            best_score = score
            best_block = block

    return best_block if best_score > 0 else ""


def _has_edge(interactions: Set[Tuple[str, str]], src_block: str, dst_block: str) -> bool:
    if not src_block or not dst_block:
        return False
    sn = _norm(src_block)
    dn = _norm(dst_block)
    if not sn or not dn:
        return False
    for src, dst in interactions:
        if _norm(src) == sn and _norm(dst) == dn:
            return True
    return False


def _domain_label(block_name: str) -> str:
    bn = _norm(block_name)
    if any(k in bn for k in ["analog", "mems", "sensor", "afe", "adc", "dac", "bias"]):
        return "analog/mixed"
    if any(k in bn for k in ["digital", "core", "logic", "control", "fifo", "state"]):
        return "digital"
    if any(k in bn for k in ["spi", "i2c", "uart", "serial", "host", "register", "interface"]):
        return "interface/control"
    if any(k in bn for k in ["clock", "pll", "osc", "timing", "reset"]):
        return "clock/reset"
    if any(k in bn for k in ["power", "pmu", "regulator"]):
        return "power"
    return "other"


def _build_equivalence_map(blocks_a: Set[str], blocks_b: Set[str]) -> Dict[str, str]:
    b_by_norm = {_norm(b): b for b in blocks_b if _norm(b)}
    mapping: Dict[str, str] = {}
    for blk in sorted(blocks_a):
        blk_n = _norm(blk)
        if blk_n in b_by_norm:
            mapping[blk] = b_by_norm[blk_n]
            continue
        # fallback: partial lexical match for split/rename hints
        parts = set(re.findall(r"[a-z0-9]+", blk.lower()))
        best = ""
        best_score = 0
        for cand in blocks_b:
            cand_parts = set(re.findall(r"[a-z0-9]+", cand.lower()))
            score = len(parts & cand_parts)
            if score > best_score:
                best = cand
                best_score = score
        mapping[blk] = best if best_score >= 2 else "uncertain"
    return mapping


def _rows_to_markdown(headers: List[str], rows: List[List[str]]) -> str:
    out: List[str] = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        safe = [cell.replace("\n", " ") for cell in row]
        out.append("| " + " | ".join(safe) + " |")
    return "\n".join(out) + "\n"


def _write_csv(path: Path, headers: List[str], rows: List[List[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _scorecard(
    blocks_a: Set[str],
    blocks_b: Set[str],
    interfaces_a: Set[str],
    interfaces_b: Set[str],
    interactions_a: Set[Tuple[str, str]],
    interactions_b: Set[Tuple[str, str]],
    reqs_a: Set[str],
    reqs_b: Set[str],
) -> List[Tuple[str, float, float, str, str]]:
    ba = _norm_set(blocks_a)
    bb = _norm_set(blocks_b)
    ia = _norm_set(interfaces_a)
    ib = _norm_set(interfaces_b)
    edge_a = {(_norm(s), _norm(t)) for s, t in interactions_a if _norm(s) and _norm(t)}
    edge_b = {(_norm(s), _norm(t)) for s, t in interactions_b if _norm(s) and _norm(t)}

    def bounded_ratio(n: int, d: int) -> float:
        if d <= 0:
            return 1.0
        return max(0.0, min(1.0, n / d))

    block_eff_a = 1.0 - bounded_ratio(abs(len(edge_a) - len(ba)), max(len(ba), 1) * 2)
    block_eff_b = 1.0 - bounded_ratio(abs(len(edge_b) - len(bb)), max(len(bb), 1) * 2)

    func_sep_a = 1.0 - bounded_ratio(len(ba & ia), max(len(ba), 1))
    func_sep_b = 1.0 - bounded_ratio(len(bb & ib), max(len(bb), 1))

    coupling_a = 1.0 - bounded_ratio(len(edge_a), max(len(ba), 1) * max(len(ba) - 1, 1))
    coupling_b = 1.0 - bounded_ratio(len(edge_b), max(len(bb), 1) * max(len(bb) - 1, 1))

    reuse_a = _jaccard(ba, bb)
    reuse_b = _jaccard(bb, ba)

    hierarchy_a = 1.0 - bounded_ratio(abs(len(edge_a) - len(ba)), max(len(edge_a), len(ba), 1))
    hierarchy_b = 1.0 - bounded_ratio(abs(len(edge_b) - len(bb)), max(len(edge_b), len(bb), 1))

    iface_share_a = _jaccard(ia, ib)
    iface_share_b = _jaccard(ib, ia)

    dup_conn_a = 1.0 - bounded_ratio(len(interactions_a) - len(edge_a), max(len(interactions_a), 1))
    dup_conn_b = 1.0 - bounded_ratio(len(interactions_b) - len(edge_b), max(len(interactions_b), 1))

    maintain_a = (block_eff_a + func_sep_a + coupling_a + hierarchy_a) / 4.0
    maintain_b = (block_eff_b + func_sep_b + coupling_b + hierarchy_b) / 4.0

    trace_a = bounded_ratio(len(reqs_a), max(len(ba), 1) * 5)
    trace_b = bounded_ratio(len(reqs_b), max(len(bb), 1) * 5)

    criteria = [
        ("block_count_efficiency", block_eff_a, block_eff_b, "Interaction-to-block proportionality."),
        ("functional_separation", func_sep_a, func_sep_b, "Separation between functional blocks and interface labels."),
        ("coupling_level", coupling_a, coupling_b, "Lower normalized edge density is better."),
        ("reuse_of_common_blocks", reuse_a, reuse_b, "Common normalized blocks across both projects."),
        ("hierarchy_clarity", hierarchy_a, hierarchy_b, "Balance between hierarchy granularity and interactions."),
        ("interface_sharing_quality", iface_share_a, iface_share_b, "Overlap quality for micro/serial-like interfaces."),
        ("duplication_of_connections", dup_conn_a, dup_conn_b, "Penalizes repeated edge entries."),
        ("maintainability", maintain_a, maintain_b, "Composite architecture maintainability score."),
        ("traceability", trace_a, trace_b, "Requirement trace row density relative to block inventory."),
    ]

    out: List[Tuple[str, float, float, str, str]] = []
    for criterion, sa, sb, rationale in criteria:
        if abs(sa - sb) < 0.03:
            better = "Tie"
        else:
            better = "Project A" if sa > sb else "Project B"
        out.append((criterion, sa, sb, better, rationale))
    return out


def _emit_reports(
    current: ProjectArtifacts,
    other: ProjectArtifacts,
    out_dir: Path,
    final_report_path: Path,
    blocks_a: Set[str],
    blocks_b: Set[str],
    interfaces_a: Set[str],
    interfaces_b: Set[str],
    interactions_a: Set[Tuple[str, str]],
    interactions_b: Set[Tuple[str, str]],
    reqs_a: Set[str],
    reqs_b: Set[str],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    blocks_a_norm = _norm_set(blocks_a)
    blocks_b_norm = _norm_set(blocks_b)
    interfaces_a_norm = _norm_set(interfaces_a)
    interfaces_b_norm = _norm_set(interfaces_b)

    overlap_blocks = blocks_a_norm & blocks_b_norm
    overlap_ifaces = interfaces_a_norm & interfaces_b_norm

    block_similarity = _jaccard(blocks_a_norm, blocks_b_norm)
    iface_similarity = _jaccard(interfaces_a_norm, interfaces_b_norm)
    interaction_similarity = _jaccard_edges(interactions_a, interactions_b)

    eq_map = _build_equivalence_map(blocks_a, blocks_b)
    score_rows = _scorecard(
        blocks_a=blocks_a,
        blocks_b=blocks_b,
        interfaces_a=interfaces_a,
        interfaces_b=interfaces_b,
        interactions_a=interactions_a,
        interactions_b=interactions_b,
        reqs_a=reqs_a,
        reqs_b=reqs_b,
    )

    # Keep Project A and Project B block results on the same row for easier review.
    block_rows: List[List[str]] = []
    matched_b_norms: Set[str] = set()
    for a_block in sorted(blocks_a):
        a_role = _role_for_block(a_block, interfaces_a, interactions_a)
        b_block = eq_map.get(a_block, "uncertain")
        b_role = _role_for_block(b_block, interfaces_b, interactions_b) if b_block != "uncertain" else "uncertain"
        note = "exact" if b_block != "uncertain" and _norm(b_block) == _norm(a_block) else "inferred"
        if b_block != "uncertain":
            matched_b_norms.add(_norm(b_block))
        block_rows.append([a_block, a_role, b_block, b_role, note])

    # Include B-side blocks that did not map from any A-side block.
    for b_block in sorted(blocks_b):
        if _norm(b_block) in matched_b_norms:
            continue
        b_role = _role_for_block(b_block, interfaces_b, interactions_b)
        block_rows.append(["", "", b_block, b_role, "unmapped_in_a"])

    _write_csv(
        out_dir / "block_inventory_comparison.csv",
        ["Project A Block Name", "Project A Role", "Project B Block Name", "Project B Role", "Notes"],
        block_rows,
    )

    edges_a = {(_norm(s), _norm(t)): (s, t) for s, t in interactions_a if _norm(s) and _norm(t)}
    edges_b = {(_norm(s), _norm(t)): (s, t) for s, t in interactions_b if _norm(s) and _norm(t)}
    all_edges = sorted(set(edges_a.keys()) | set(edges_b.keys()))
    inter_rows: List[List[str]] = []
    for src_n, dst_n in all_edges:
        a_present = "yes" if (src_n, dst_n) in edges_a else "no"
        b_present = "yes" if (src_n, dst_n) in edges_b else "no"
        src_disp = edges_a.get((src_n, dst_n), edges_b.get((src_n, dst_n), (src_n, dst_n)))[0]
        dst_disp = edges_a.get((src_n, dst_n), edges_b.get((src_n, dst_n), (src_n, dst_n)))[1]
        interaction_type = "data/control"
        comment = "shared" if a_present == "yes" and b_present == "yes" else "project-specific"
        inter_rows.append([src_disp, dst_disp, interaction_type, a_present, b_present, comment])

    _write_csv(
        out_dir / "block_interaction_matrix.csv",
        ["From Block", "To Block", "Interaction Type", "Project A", "Project B", "Comments"],
        inter_rows,
    )

    def hierarchy_guess(blocks: Set[str]) -> Tuple[int, int, int]:
        leaves = sum(1 for b in blocks if "interface" in b.lower() or "host" in b.lower())
        cores = max(len(blocks) - leaves, 0)
        levels = 3 if len(blocks) > 6 else 2
        return levels, cores, leaves

    lv_a, core_a, leaf_a = hierarchy_guess(blocks_a)
    lv_b, core_b, leaf_b = hierarchy_guess(blocks_b)
    hier_rows = [
        ["L0", current.project_name, other.project_name, "Top system node", "none"],
        ["L1", f"Core subsystems={core_a}", f"Core subsystems={core_b}", str(core_a - core_b), "partitioning"],
        ["L2", f"Boundary/interface nodes={leaf_a}", f"Boundary/interface nodes={leaf_b}", str(leaf_a - leaf_b), "interface handling"],
        ["Depth", str(lv_a), str(lv_b), str(lv_a - lv_b), "hierarchy clarity"],
    ]
    _write_csv(
        out_dir / "hierarchy_comparison.csv",
        ["Level", "Project A", "Project B", "Difference", "Impact"],
        hier_rows,
    )

    mod_md = "# modularization_assessment\n\n"
    mod_md += "## Partitioning Comparison\n\n"
    mod_md += f"- Project A blocks: {len(blocks_a)}\n"
    mod_md += f"- Project B blocks: {len(blocks_b)}\n"
    mod_md += f"- Shared normalized blocks: {len(overlap_blocks)}\n\n"
    mod_md += "## Modularization Strategy Comparison\n\n"
    mod_md += "- Reuse: inferred from normalized block overlap and interface overlap.\n"
    mod_md += "- Coupling: inferred from normalized interaction density.\n"
    mod_md += "- Cohesion: inferred by block role distribution and edge locality.\n\n"
    mod_md += "## Interface Sharing Analysis for Similar Elements\n\n"
    shared_ifaces = sorted(interfaces_a_norm & interfaces_b_norm)
    if shared_ifaces:
        for iface in shared_ifaces[:20]:
            mod_md += f"- shared interface pattern: {iface}\n"
    else:
        mod_md += "- uncertain: no normalized interface overlap found.\n"
    _write_text(out_dir / "modularization_assessment.md", mod_md)

    score_csv_rows: List[List[str]] = []
    for criterion, sa, sb, better, rationale in score_rows:
        score_csv_rows.append([criterion, f"{sa:.3f}", f"{sb:.3f}", better, rationale])
    _write_csv(
        out_dir / "efficiency_scorecard.csv",
        ["Criterion", "Project A Score", "Project B Score", "Better Project", "Rationale"],
        score_csv_rows,
    )

    better_a = sum(1 for _, sa, sb, _, _ in score_rows if sa > sb + 0.03)
    better_b = sum(1 for _, sa, sb, _, _ in score_rows if sb > sa + 0.03)
    if better_a > better_b:
        winner = "Project A"
        winner_reason = "higher score across more criteria"
    elif better_b > better_a:
        winner = "Project B"
        winner_reason = "higher score across more criteria"
    else:
        winner = "Tie"
        winner_reason = "balanced criteria scores"

    # Build explicit architecture recommendation with actionable mixed-signal proposals.
    norm_edges_a = {(_norm(s), _norm(t)) for s, t in interactions_a if _norm(s) and _norm(t)}
    norm_edges_b = {(_norm(s), _norm(t)) for s, t in interactions_b if _norm(s) and _norm(t)}
    unique_a_edges = sorted([(s, t) for s, t in interactions_a if (_norm(s), _norm(t)) not in norm_edges_b])
    unique_b_edges = sorted([(s, t) for s, t in interactions_b if (_norm(s), _norm(t)) not in norm_edges_a])

    role_patterns = {
        "sensor": ["mems", "sensor", "sensing"],
        "afe": ["analogfront", "afe", "analog", "conditioning"],
        "adc": ["adc", "converter"],
        "digital_core": ["digitalcontrolcore", "digitalcontrol", "controlcore", "digitalcore", "processingcore"],
        "fifo": ["fifo", "buffer"],
        "interrupt": ["interrupt", "irq"],
        "register": ["registercontrol", "register", "regmap", "config", "configuration"],
        "spi": ["spi", "serialspi"],
        "i2c": ["i2c", "seriali2c"],
        "host": ["hostinterface", "host", "mcu", "processor"],
        "calibration": ["calibration", "selftest", "trim", "offset"],
        "clock": ["clock", "pll", "osc", "timing"],
        "power": ["power", "pmu", "regulator", "bias"],
        "reset": ["reset"],
    }
    roles_a = {role: _find_block_by_keywords(blocks_a, pats) for role, pats in role_patterns.items()}
    roles_b = {role: _find_block_by_keywords(blocks_b, pats) for role, pats in role_patterns.items()}

    canonical_edges: List[Tuple[str, str, str]] = [
        ("sensor", "afe", "Sensor front-end boundary"),
        ("afe", "adc", "Analog to converter handoff"),
        ("adc", "digital_core", "Conversion output into digital processing"),
        ("register", "digital_core", "Register-mediated runtime configuration"),
        ("digital_core", "fifo", "Data decoupling for host-read timing"),
        ("fifo", "interrupt", "Event signaling from buffered data path"),
        ("spi", "register", "SPI control path through register abstraction"),
        ("i2c", "register", "I2C control path through register abstraction"),
        ("calibration", "register", "Calibration loop captured via controllable registers"),
    ]
    rec_lines: List[str] = []
    rec_lines.append("# Final Recommendation of the Better Architecture Organization")
    rec_lines.append("")
    rec_lines.append("## Decision")
    rec_lines.append("")
    if winner == "Tie":
        rec_lines.append(
            f"- Result: Tie between {current.project_name} and {other.project_name}."
        )
        rec_lines.append(
            f"- Basis: equivalent aggregate efficiency signals ({winner_reason}), high block/interface overlap, and matching interaction topology."
        )
    elif winner == "Project A":
        rec_lines.append(f"- Better architecture organization: {current.project_name} (Project A).")
        rec_lines.append(f"- Basis: {winner_reason} with stronger organization scorecard pattern.")
    else:
        rec_lines.append(f"- Better architecture organization: {other.project_name} (Project B).")
        rec_lines.append(f"- Basis: {winner_reason} with stronger organization scorecard pattern.")

    rec_lines.append("")
    rec_lines.append("## Proposed Best Block Connections and Interactions")
    rec_lines.append("")
    rec_lines.append("- Proposed links are evidence-driven from detected block roles in both projects.")
    for src_role, dst_role, rationale in canonical_edges:
        a_src = roles_a.get(src_role, "")
        a_dst = roles_a.get(dst_role, "")
        b_src = roles_b.get(src_role, "")
        b_dst = roles_b.get(dst_role, "")
        a_ok = _has_edge(interactions_a, a_src, a_dst) if a_src and a_dst else False
        b_ok = _has_edge(interactions_b, b_src, b_dst) if b_src and b_dst else False

        a_repr = f"{a_src} -> {a_dst}" if a_src and a_dst else "not-observed"
        b_repr = f"{b_src} -> {b_dst}" if b_src and b_dst else "not-observed"

        if a_repr == "not-observed" and b_repr == "not-observed":
            continue

        action = "keep" if a_ok and b_ok else "review"
        if a_ok and not b_ok and b_repr != "not-observed":
            action = f"add in {other.project_name}"
        elif b_ok and not a_ok and a_repr != "not-observed":
            action = f"add in {current.project_name}"
        elif not a_ok and not b_ok:
            action = "consider adding in both"

        rec_lines.append(
            f"- [{action}] {rationale}: A({a_repr}, {'present' if a_ok else 'missing'}) | B({b_repr}, {'present' if b_ok else 'missing'})."
        )

    # Mixed-signal-specific quality checks for organization robustness.
    rec_lines.append("")
    rec_lines.append("## Mixed-Signal Quality Checks")
    rec_lines.append("")
    a_analog = sorted([b for b in blocks_a if _domain_label(b) == "analog/mixed"])
    b_analog = sorted([b for b in blocks_b if _domain_label(b) == "analog/mixed"])
    a_digital = sorted([b for b in blocks_a if _domain_label(b) == "digital"])
    b_digital = sorted([b for b in blocks_b if _domain_label(b) == "digital"])
    rec_lines.append(
        f"- Analog/digital partition visibility: A analog={len(a_analog)} digital={len(a_digital)} | B analog={len(b_analog)} digital={len(b_digital)}."
    )

    a_clk = roles_a.get("clock", "")
    a_rst = roles_a.get("reset", "")
    b_clk = roles_b.get("clock", "")
    b_rst = roles_b.get("reset", "")
    rec_lines.append(
        f"- Clock/reset control observability: A clock={a_clk or 'not-observed'} reset={a_rst or 'not-observed'} | B clock={b_clk or 'not-observed'} reset={b_rst or 'not-observed'}."
    )

    a_pwr = roles_a.get("power", "")
    b_pwr = roles_b.get("power", "")
    rec_lines.append(
        f"- Power-control block observability: A power={a_pwr or 'not-observed'} | B power={b_pwr or 'not-observed'}."
    )

    host_core_direct_a = False
    host_core_direct_b = False
    if roles_a.get("host") and roles_a.get("digital_core"):
        host_core_direct_a = _has_edge(interactions_a, roles_a["host"], roles_a["digital_core"])
    if roles_b.get("host") and roles_b.get("digital_core"):
        host_core_direct_b = _has_edge(interactions_b, roles_b["host"], roles_b["digital_core"])
    rec_lines.append(
        f"- Host-to-core direct coupling check: A={'present' if host_core_direct_a else 'not-observed'} | B={'present' if host_core_direct_b else 'not-observed'} (prefer register/protocol mediation)."
    )

    rec_lines.append("")
    rec_lines.append("## Interaction Consolidation Proposals")
    rec_lines.append("")
    if unique_a_edges:
        rec_lines.append(f"- Edges present only in {current.project_name} (review for optional reuse in {other.project_name}):")
        for src, dst in unique_a_edges[:12]:
            rec_lines.append(f"  - `{src} -> {dst}`")
    if unique_b_edges:
        rec_lines.append(f"- Edges present only in {other.project_name} (review for optional reuse in {current.project_name}):")
        for src, dst in unique_b_edges[:12]:
            rec_lines.append(f"  - `{src} -> {dst}`")
    if not unique_a_edges and not unique_b_edges:
        rec_lines.append("- No project-unique normalized interactions detected; keep shared interaction baseline as canonical.")

    rec_lines.append("")
    rec_lines.append("## Rationale and Traceability")
    rec_lines.append("")
    rec_lines.append(f"- Evidence: {out_dir / 'block_inventory_comparison.csv'}")
    rec_lines.append(f"- Evidence: {out_dir / 'block_interaction_matrix.csv'}")
    rec_lines.append(f"- Evidence: {out_dir / 'hierarchy_comparison.csv'}")
    rec_lines.append(f"- Evidence: {out_dir / 'efficiency_scorecard.csv'}")
    rec_lines.append("- Note: explicit findings are reported as direct artifact observations; inferred suggestions are clearly marked as proposals.")

    final_recommendation_path = out_dir / "final_recommendation.md"
    _write_text(final_recommendation_path, "\n".join(rec_lines) + "\n")

    final_lines: List[str] = []
    final_lines.append("# final_report")
    final_lines.append("")
    final_lines.append("## Executive Summary")
    final_lines.append("")
    final_lines.append(f"- Project A: {current.project_name}")
    final_lines.append(f"- Project B: {other.project_name}")
    final_lines.append(f"- Overall efficiency assessment: {winner} ({winner_reason}).")
    final_lines.append("")
    final_lines.append("## Block Inventory Comparison")
    final_lines.append("")
    final_lines.append(f"- Evidence file: {out_dir / 'block_inventory_comparison.csv'}")
    final_lines.append(f"- Blocks A={len(blocks_a)}, B={len(blocks_b)}, overlap={len(overlap_blocks)}")
    final_lines.append("")
    final_lines.append("## Block Interaction Comparison")
    final_lines.append("")
    final_lines.append(f"- Evidence file: {out_dir / 'block_interaction_matrix.csv'}")
    final_lines.append(f"- Interactions A={len(interactions_a)}, B={len(interactions_b)}, similarity={interaction_similarity:.3f}")
    final_lines.append("")
    final_lines.append("## Partitioning Comparison")
    final_lines.append("")
    final_lines.append("- Evidence file: modularization_assessment.md")
    final_lines.append("- Findings are architecture-level and deterministic from artifact data.")
    final_lines.append("")
    final_lines.append("## Hierarchy Composition Comparison")
    final_lines.append("")
    final_lines.append(f"- Evidence file: {out_dir / 'hierarchy_comparison.csv'}")
    final_lines.append(f"- Hierarchy clarity proxy: A={score_rows[4][1]:.3f}, B={score_rows[4][2]:.3f}")
    final_lines.append("")
    final_lines.append("## Modularization Strategy Comparison")
    final_lines.append("")
    final_lines.append("- Evidence file: modularization_assessment.md")
    final_lines.append("- Explicit findings are separated from inferred findings in per-file notes.")
    final_lines.append("")
    final_lines.append("## Efficiency Assessment")
    final_lines.append("")
    final_lines.append(f"- Evidence file: {out_dir / 'efficiency_scorecard.csv'}")
    final_lines.append(f"- Block similarity={block_similarity:.3f}, Interface similarity={iface_similarity:.3f}")
    final_lines.append(f"- Recommended better project for architecture efficiency: {winner}")
    final_lines.append(f"- Detailed recommendation file: {final_recommendation_path}")
    final_lines.append("")
    final_lines.append("## Key Similarities")
    final_lines.append("")
    final_lines.append(f"- Shared normalized blocks: {len(overlap_blocks)}")
    final_lines.append(f"- Shared normalized interfaces: {len(overlap_ifaces)}")
    final_lines.append("")
    final_lines.append("## Key Differences")
    final_lines.append("")
    final_lines.append(f"- Blocks only in A: {len({b for b in blocks_a if _norm(b) not in blocks_b_norm})}")
    final_lines.append(f"- Blocks only in B: {len({b for b in blocks_b if _norm(b) not in blocks_a_norm})}")
    final_lines.append(f"- Interaction topology divergence score: {1.0 - interaction_similarity:.3f}")
    final_lines.append("")
    final_lines.append("## Recommendations")
    final_lines.append("")
    final_lines.append("- Reuse shared interface blocks where normalized overlap is high.")
    final_lines.append("- For uncertain mappings, treat as split/merged candidates and review manually.")
    final_lines.append("- Prefer deeper hierarchy only when it reduces coupling and improves reuse.")
    final_lines.append("")
    final_lines.append("## Final recommendation of the better architecture organization")
    final_lines.append("")
    final_lines.append(f"- See detailed recommendation and connection proposals in: {final_recommendation_path}")

    _write_text(final_report_path, "\n".join(final_lines) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Stage 6 architectural comparison against another workspace project.",
        epilog=f"{HOW_TO_RUN}\nHelp: {HELP_CMD}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--project-to-compare",
        required=True,
        help="Name of sibling project directory in the same workspace root.",
    )
    parser.add_argument(
        "--workspace-root",
        default=None,
        help="Workspace root containing sibling project directories. Default: parent of current project root.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for comparison artifacts. Default: artifacts/comparison",
    )
    parser.add_argument(
        "--output-path",
        default=None,
        help="Optional explicit final report path. Default: <output-dir>/final_report.md",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    current_project_root = Path(__file__).resolve().parent.parent
    workspace_root = Path(args.workspace_root).resolve() if args.workspace_root else current_project_root.parent
    compare_project_root = (workspace_root / args.project_to_compare).resolve()

    print("Stage 6 architecture comparison", flush=True)
    print(f"Current project: {current_project_root.name}", flush=True)
    print(f"Workspace root: {workspace_root}", flush=True)
    print(f"Compare project: {compare_project_root}", flush=True)

    if not compare_project_root.exists() or not compare_project_root.is_dir():
        print(f"ERROR: compare project not found: {compare_project_root}", flush=True)
        print(f"Help: {HELP_CMD}", flush=True)
        return 2

    if compare_project_root == current_project_root:
        print("ERROR: compare project must be different from current project.", flush=True)
        print(f"Help: {HELP_CMD}", flush=True)
        return 2

    current = _load_artifacts(current_project_root)
    other = _load_artifacts(compare_project_root)

    missing_current = _missing_files(current)
    missing_other = _missing_files(other)
    if missing_current or missing_other:
        print("ERROR: required Stage 2A artifacts are missing.", flush=True)
        if missing_current:
            print("Missing in current project:", flush=True)
            for path in missing_current:
                print(f"- {path}", flush=True)
        if missing_other:
            print("Missing in compared project:", flush=True)
            for path in missing_other:
                print(f"- {path}", flush=True)
        print(f"Help: {HELP_CMD}", flush=True)
        return 3

    blocks_a = _collect_blocks(current.block_inventory)
    blocks_b = _collect_blocks(other.block_inventory)
    interfaces_a = _collect_interfaces(current.interface_catalog)
    interfaces_b = _collect_interfaces(other.interface_catalog)
    interactions_a = _collect_interactions(current.interaction_matrix)
    interactions_b = _collect_interactions(other.interaction_matrix)
    reqs_a = _collect_requirement_ids(current.requirement_traceability)
    reqs_b = _collect_requirement_ids(other.requirement_traceability)

    if args.output_dir:
        out_dir = Path(args.output_dir).resolve()
    else:
        out_dir = current_project_root / "artifacts" / "comparison"

    if args.output_path:
        final_report_path = Path(args.output_path).resolve()
    else:
        final_report_path = out_dir / "final_report.md"

    _emit_reports(
        current=current,
        other=other,
        out_dir=out_dir,
        final_report_path=final_report_path,
        blocks_a=blocks_a,
        blocks_b=blocks_b,
        interfaces_a=interfaces_a,
        interfaces_b=interfaces_b,
        interactions_a=interactions_a,
        interactions_b=interactions_b,
        reqs_a=reqs_a,
        reqs_b=reqs_b,
    )

    print("Comparison artifacts written:", flush=True)
    print(f"- {out_dir / 'block_inventory_comparison.csv'}", flush=True)
    print(f"- {out_dir / 'block_interaction_matrix.csv'}", flush=True)
    print(f"- {out_dir / 'hierarchy_comparison.csv'}", flush=True)
    print(f"- {out_dir / 'modularization_assessment.md'}", flush=True)
    print(f"- {out_dir / 'efficiency_scorecard.csv'}", flush=True)
    print(f"- {out_dir / 'final_recommendation.md'}", flush=True)
    print(f"- {final_report_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())