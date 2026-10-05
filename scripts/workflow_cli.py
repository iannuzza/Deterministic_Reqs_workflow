#!/usr/bin/env python3
"""Local deterministic workflow CLI for Stage 0 to 7.

This CLI runs existing project scripts only. It does not invoke any LLM tools.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

from approved_snapshot_resolver import resolve_complete_snapshot_id


@dataclass(frozen=True)
class StageDef:
    key: str
    name: str
    runner: str
    validator: str
    runner_args: tuple[str, ...] = ()
    validator_args: tuple[str, ...] = ()


STAGE_ORDER: List[str] = ["0", "1", "2", "2a", "3", "4", "5", "6", "7"]
SNAPSHOT_BACKED_STAGES = {"3", "4", "5", "6", "7"}
STAGES: Dict[str, StageDef] = {
    "0": StageDef("0", "Stage 0", "scripts/run_stage0_gate0.py", "scripts/validate_stage0_gate.py"),
    "1": StageDef("1", "Stage 1", "scripts/run_stage1_requirements_gate1.py", "scripts/validate_stage1_gate.py"),
    "2": StageDef("2", "Stage 2", "scripts/run_stage1_specs_gate2.py", "scripts/validate_stage2_gate.py"),
    "2a": StageDef("2a", "Stage 2A", "scripts/run_stage2_micro_arc_gate.py", "scripts/validate_stage2_micro_arc_gate.py"),
    "3": StageDef("3", "Stage 3", "scripts/run_stage3_srs_gate.py", "scripts/validate_stage3_srs_gate.py"),
    "4": StageDef("4", "Stage 4", "scripts/run_stage4_ars_gate.py", "scripts/validate_stage4_ars_gate.py"),
    "5": StageDef("5", "Stage 5", "scripts/run_stage5_drs_gate.py", "scripts/validate_stage5_drs_gate.py"),
    "6": StageDef(
        "6", "Stage 6 Digital IPOS", "scripts/run_stage6_digital_ipos_gate.py", "scripts/validate_ipos_gate.py",
        validator_args=("--kind", "digital"),
    ),
    "7": StageDef(
        "7", "Stage 7 Analog IPOS", "scripts/run_stage7_analog_ipos_gate.py", "scripts/validate_ipos_gate.py",
        validator_args=("--kind", "analog"),
    ),
}

EXIT_OK = 0
EXIT_STAGE_FAIL = 3
EXIT_VALIDATE_FAIL = 4
EXIT_USAGE = 5

STAGE_HELP = "Allowed stage keys: 0, 1, 2, 2a, 3, 4, 5, 6, 7 (aliases like 'stage2', '2-a' are accepted)."
SINGLE_STAGE_HELP = "Allowed single-stage keys: 0, 1, 2, 2a, 3, 4, 5, 6, 7."
RETRIEVAL_TESTS = [
    "tests.test_embedding_text",
    "tests.test_semantic_index",
    "tests.test_fusion",
    "tests.test_benchmark",
    "tests.test_final_polish",
]

CLI_EXAMPLES = """Examples:
    # Top-level help
    python scripts/workflow_cli.py --help

    # Check status
    python scripts/workflow_cli.py status

    # Stage 1 taxonomy update
    python scripts/workflow_cli.py taxonomy-update
    python scripts/workflow_cli.py taxonomy-update --index-csv artifacts/stage1_requirements/ocr_extracts/index.csv

    # Optional architecture comparison
    python scripts/workflow_cli.py arch-compare --project-to-compare <project_name>
    python scripts/workflow_cli.py arch-compare --project-to-compare <project_name> --output-dir artifacts/comparison

    # Run the top-down pipeline through Stage 7
    python scripts/workflow_cli.py run --from-stage 0 --to-stage 7 --snapshot-id <id>

    # Validate the complete pipeline
    python scripts/workflow_cli.py validate --all

Direct script entrypoint for Stage 6:
    python scripts/run_stage6_architecture_comparison.py --project-to-compare <project_name>

Notes:
    - Stage ranges are inclusive and ordered by workflow: 0 -> 1 -> 2 -> 2a -> 3 -> 4 -> 5 -> 6 -> 7.
    - Stages 3-7 use one snapshot ID selected at workflow start.
    - A run may execute one stage or an ascending contiguous range; each stage runs once and stops on the first failure.
    - Stage 2A is mandatory before Stage 3 when the selected range includes Stage 3.
    - Use --dry-run to print commands without executing them.
"""


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _normalize_stage(value: str) -> str:
    raw = value.strip().lower()
    raw = raw.replace("stage", "").replace(" ", "")
    if raw in {"2a", "2-a", "2_a"}:
        return "2a"
    return raw


def _stage_range(start: str, end: str) -> List[str]:
    s = _normalize_stage(start)
    e = _normalize_stage(end)
    if s not in STAGES or e not in STAGES:
        raise ValueError(f"Unknown stage range: {start} -> {end}")
    i = STAGE_ORDER.index(s)
    j = STAGE_ORDER.index(e)
    if i > j:
        raise ValueError("Range must be ascending, for example: --from-stage 0 --to-stage 3")
    return STAGE_ORDER[i : j + 1]


def _log_manifest(repo_root: Path, payload: dict) -> None:
    out = repo_root / "artifacts" / "orchestrator" / "workflow_cli_runs.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def _run_python(repo_root: Path, script: str, dry_run: bool) -> int:
    cmd = [sys.executable, script]
    print(f"[{_now()}] RUN {' '.join(cmd)}")
    if dry_run:
        return 0
    return subprocess.run(cmd, cwd=repo_root).returncode


def _run_python_cmd(repo_root: Path, cmd: List[str], dry_run: bool) -> int:
    full_cmd = [sys.executable, *cmd]
    print(f"[{_now()}] RUN {' '.join(full_cmd)}")
    if dry_run:
        return 0
    return subprocess.run(full_cmd, cwd=repo_root).returncode


def _run_retrieval_tests(repo_root: Path, dry_run: bool) -> int:
    cmd = ["-m", "unittest", *RETRIEVAL_TESTS]
    print(f"\n[{_now()}] Retrieval test preflight")
    rc = _run_python_cmd(repo_root, cmd, dry_run)
    _log_manifest(
        repo_root,
        {
            "ts": _now(),
            "stage": "preflight",
            "kind": "retrieval_tests",
            "modules": RETRIEVAL_TESTS,
            "exit_code": rc,
        },
    )
    if rc != 0:
        print(f"[{_now()}] Retrieval test preflight: FAIL (exit={rc})")
    else:
        print(f"[{_now()}] Retrieval test preflight: PASS")
    return rc


def _run_retrieval_benchmark(repo_root: Path, dry_run: bool) -> int:
    context_path = repo_root / "config" / "project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}
    report_path = context.get("retrieval_benchmark_report_path", "artifacts/rag/retrieval_benchmark_report.json")
    selection_path = context.get("retrieval_selection_path", "config/retrieval_selection.json")
    cmd = [
        "scripts/run_retrieval_benchmark.py",
        "--project-context",
        "config/project_context.json",
        "--output",
        str(report_path),
        "--selection",
        str(selection_path),
    ]
    print(f"\n[{_now()}] Project retrieval benchmark")
    rc = _run_python_cmd(repo_root, cmd, dry_run)
    _log_manifest(
        repo_root,
        {
            "ts": _now(),
            "stage": "preflight",
            "kind": "retrieval_benchmark",
            "script": "scripts/run_retrieval_benchmark.py",
            "report": str(report_path),
            "selection": str(selection_path),
            "exit_code": rc,
        },
    )
    if rc != 0:
        print(f"[{_now()}] Project retrieval benchmark: FAIL (exit={rc})")
    else:
        print(f"[{_now()}] Project retrieval benchmark: PASS")
    return rc


def _acquire_lock(repo_root: Path) -> Path:
    lock_path = repo_root / "artifacts" / "orchestrator" / ".workflow_cli.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(f"pid={os.getpid()} started={_now()}\n")
    except FileExistsError as exc:
        raise RuntimeError(f"Another workflow_cli run appears active: {lock_path}") from exc
    return lock_path


def _release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass


def _validate_stage_keys(keys: Iterable[str]) -> List[str]:
    result: List[str] = []
    for key in keys:
        norm = _normalize_stage(key)
        if norm not in STAGES:
            raise ValueError(f"Unknown stage: {key}")
        result.append(norm)
    return result


def _project_id(repo_root: Path) -> str:
    context_path = repo_root / "config/project_context.json"
    if not context_path.exists():
        return repo_root.name
    context = json.loads(context_path.read_text(encoding="utf-8"))
    return str(context.get("project_name") or repo_root.name)


def _require_pre_freeze_gate(repo_root: Path) -> None:
    from pre_freeze_coherence_gate import evaluate
    result = evaluate(repo_root, repo_root / "artifacts/validation/source_to_stage2b_coherence.json")
    if not result["downstream_allowed"]:
        raise RuntimeError(f"Pre-freeze coherence gate blocked downstream workflow: {result['decision']}")


def _require_downstream_coherence(repo_root: Path, snapshot_id: str | None) -> None:
    if not snapshot_id:
        raise RuntimeError("Downstream coherence requires one explicit approved snapshot ID.")
    from validate_downstream_coherence import validate
    result = validate(repo_root, snapshot_id)
    if result["decision"] != "PASS":
        raise RuntimeError(
            f"Downstream snapshot coherence blocked workflow: {result['decision']} "
            f"({result['finding_count']} findings)"
        )


def _resolve_workflow_snapshot(repo_root: Path, snapshot_id: str | None, use_latest_approved: bool) -> str | None:
    if not use_latest_approved:
        return snapshot_id
    selected_id = resolve_complete_snapshot_id(repo_root, project_id=_project_id(repo_root))
    print(f"[{_now()}] Selected workflow snapshot: {selected_id}")
    return selected_id


def _run_stage_once(
    repo_root: Path,
    stage_key: str,
    validate_after_run: bool,
    dry_run: bool,
    snapshot_id: str | None = None,
) -> int:
    stage = STAGES[stage_key]
    print(f"\n[{_now()}] {stage.name} run 1/1")
    runner = stage.runner
    if stage_key in SNAPSHOT_BACKED_STAGES:
        if not snapshot_id:
            raise ValueError(f"Stage {stage_key} requires a resolved snapshot ID")
        rc_run = _run_python_cmd(
            repo_root,
            [runner, *stage.runner_args, "--snapshot-id", snapshot_id],
            dry_run,
        )
    else:
        rc_run = _run_python(repo_root, runner, dry_run)
    _log_manifest(
        repo_root,
        {
            "ts": _now(),
            "stage": stage.key,
            "kind": "runner",
            "script": stage.runner,
            "run": 1,
            "exit_code": rc_run,
        },
    )
    if rc_run != 0:
        return EXIT_STAGE_FAIL

    if not validate_after_run:
        return EXIT_OK

    if stage_key in SNAPSHOT_BACKED_STAGES:
        if not snapshot_id:
            raise ValueError(f"Stage {stage_key} requires a resolved snapshot ID")
        rc_val = _run_python_cmd(
            repo_root,
            [stage.validator, *stage.validator_args, "--snapshot-id", snapshot_id],
            dry_run,
        )
    else:
        rc_val = _run_python(repo_root, stage.validator, dry_run)
    _log_manifest(
        repo_root,
        {
            "ts": _now(),
            "stage": stage.key,
            "kind": "validator",
            "script": stage.validator,
            "run": 1,
            "exit_code": rc_val,
        },
    )
    return EXIT_OK if rc_val == 0 else EXIT_VALIDATE_FAIL


def cmd_run(args: argparse.Namespace, repo_root: Path) -> int:
    if args.stage and (args.from_stage or args.to_stage):
        raise ValueError("Use either --stage or --from-stage/--to-stage")
    if args.stage:
        single_stage = _normalize_stage(args.stage)
        stage_keys = _validate_stage_keys([single_stage])
    elif args.from_stage and args.to_stage:
        stage_keys = _stage_range(args.from_stage, args.to_stage)
    else:
        raise ValueError("Provide --stage or both --from-stage and --to-stage")

    if any(key in SNAPSHOT_BACKED_STAGES for key in stage_keys) and bool(args.snapshot_id) == bool(args.use_latest_approved):
        raise ValueError("Stages 3-7 require exactly one of --snapshot-id or --use-latest-approved")

    selected_snapshot_id = _resolve_workflow_snapshot(
        repo_root,
        args.snapshot_id,
        args.use_latest_approved,
    ) if any(key in SNAPSHOT_BACKED_STAGES for key in stage_keys) else args.snapshot_id

    if any(key in SNAPSHOT_BACKED_STAGES for key in stage_keys):
        if stage_keys[0] not in SNAPSHOT_BACKED_STAGES:
            _require_pre_freeze_gate(repo_root)
        _require_downstream_coherence(repo_root, selected_snapshot_id)

    print(f"Workflow run plan: {' -> '.join(stage_keys)}")
    rc_tests = _run_retrieval_tests(repo_root, args.dry_run)
    if rc_tests != 0:
        print(f"[{_now()}] STOP before workflow execution (regression tests exit={rc_tests})")
        return EXIT_VALIDATE_FAIL

    if "0" in stage_keys:
        rc_benchmark = _run_retrieval_benchmark(repo_root, args.dry_run)
        if rc_benchmark != 0:
            print(f"[{_now()}] STOP before Stage 0 execution (retrieval benchmark exit={rc_benchmark})")
            return EXIT_VALIDATE_FAIL
    else:
        print("Project retrieval benchmark preflight: SKIPPED (Stage 0 not selected)")

    for stage_key in stage_keys:
        rc = _run_stage_once(
            repo_root=repo_root,
            stage_key=stage_key,
            validate_after_run=True,
            dry_run=args.dry_run,
            snapshot_id=selected_snapshot_id,
        )
        if rc != 0:
            print(f"[{_now()}] STOP at stage {stage_key} (exit={rc})")
            return rc

    print(f"[{_now()}] Workflow run: PASS")
    return EXIT_OK


def cmd_validate(args: argparse.Namespace, repo_root: Path) -> int:
    if args.all:
        stage_keys = list(STAGE_ORDER)
    elif args.stage:
        stage_keys = _validate_stage_keys([args.stage])
    else:
        raise ValueError("Use --all or --stage")

    if any(key in SNAPSHOT_BACKED_STAGES for key in stage_keys) and bool(args.snapshot_id) == bool(args.use_latest_approved):
        raise ValueError("Validating stages 3-7 requires exactly one of --snapshot-id or --use-latest-approved")
    selected_snapshot_id = _resolve_workflow_snapshot(
        repo_root,
        args.snapshot_id,
        args.use_latest_approved,
    ) if any(key in SNAPSHOT_BACKED_STAGES for key in stage_keys) else args.snapshot_id

    if any(key in SNAPSHOT_BACKED_STAGES for key in stage_keys):
        _require_downstream_coherence(repo_root, selected_snapshot_id)

    print(f"Validate plan: {' -> '.join(stage_keys)}")
    for stage_key in stage_keys:
        stage = STAGES[stage_key]
        if stage_key in SNAPSHOT_BACKED_STAGES:
            rc = _run_python_cmd(
                repo_root,
                [stage.validator, *stage.validator_args, "--snapshot-id", selected_snapshot_id],
                args.dry_run,
            )
        else:
            rc = _run_python(repo_root, stage.validator, args.dry_run)
        _log_manifest(
            repo_root,
            {
                "ts": _now(),
                "stage": stage.key,
                "kind": "validator",
                "script": stage.validator,
                "attempt": 1,
                "exit_code": rc,
            },
        )
        if rc != 0:
            print(f"[{_now()}] Validation failed at stage {stage_key}")
            return EXIT_VALIDATE_FAIL
    if args.all:
        diagram_validator = "scripts/validate_workflow_diagram_rendering.py"
        rc = _run_python(repo_root, diagram_validator, args.dry_run)
        _log_manifest(
            repo_root,
            {
                "ts": _now(),
                "stage": "workflow-diagram",
                "kind": "validator",
                "script": diagram_validator,
                "attempt": 1,
                "exit_code": rc,
            },
        )
        if rc != 0:
            print(f"[{_now()}] Validation failed at workflow diagram rendering crosscheck")
            return EXIT_VALIDATE_FAIL
    print(f"[{_now()}] Validation: PASS")
    return EXIT_OK


def cmd_ipos(args: argparse.Namespace, repo_root: Path, stage_key: str) -> int:
    if bool(args.snapshot_id) == bool(args.use_latest_approved):
        raise ValueError("IPOS requires exactly one of --snapshot-id or --use-latest-approved")
    selected_snapshot_id = _resolve_workflow_snapshot(
        repo_root,
        args.snapshot_id,
        args.use_latest_approved,
    )
    _require_downstream_coherence(repo_root, selected_snapshot_id)
    return _run_stage_once(
        repo_root=repo_root,
        stage_key=stage_key,
        validate_after_run=True,
        dry_run=args.dry_run,
        snapshot_id=selected_snapshot_id,
    )


def cmd_validate_downstream(args: argparse.Namespace, repo_root: Path) -> int:
    cmd = ["scripts/evaluate_retrieval_mapping_flow.py"]
    if args.config:
        cmd.extend(["--config", args.config])
    if args.enable_semantic:
        cmd.append("--enable-semantic")
    rc = _run_python_cmd(repo_root, cmd, args.dry_run)
    _log_manifest(repo_root, {"ts": _now(), "stage": "post-pipeline", "kind": "downstream_validation", "script": cmd[0], "config": args.config, "semantic_evaluation": args.enable_semantic, "attempt": 1, "exit_code": rc})
    if rc != 0:
        print(f"[{_now()}] Downstream validation: FAIL (exit={rc})")
        return EXIT_VALIDATE_FAIL
    print(f"[{_now()}] Downstream validation: PASS (recommendations remain approval-gated)")
    return EXIT_OK


def cmd_taxonomy_update(args: argparse.Namespace, repo_root: Path) -> int:
    cmd = ["scripts/run_taxonomy_crosscheck_update.py", "--index-csv", args.index_csv]
    if args.initial_spec:
        cmd.extend(["--initial-spec", args.initial_spec])

    rc = _run_python_cmd(repo_root, cmd, args.dry_run)
    _log_manifest(
        repo_root,
        {
            "ts": _now(),
            "stage": "1",
            "kind": "taxonomy_update",
            "script": "scripts/run_taxonomy_crosscheck_update.py",
            "attempt": 1,
            "exit_code": rc,
        },
    )
    if rc != 0:
        print(f"[{_now()}] Taxonomy update: FAIL (exit={rc})")
        return EXIT_STAGE_FAIL
    print(f"[{_now()}] Taxonomy update: PASS")
    return EXIT_OK


def cmd_freeze_stage2b(args: argparse.Namespace, repo_root: Path) -> int:
    remediation = _run_python_cmd(
        repo_root,
        ["scripts/pre_freeze_warning_remediation.py"],
        args.dry_run,
    )
    if remediation != 0:
        print(f"[{_now()}] Pre-freeze warning remediation: FAIL (exit={remediation})")
        return EXIT_VALIDATE_FAIL
    for command in (
        ["scripts/validate_source_to_stage2b_coherence.py"],
        ["scripts/pre_freeze_coherence_gate.py"],
    ):
        if _run_python_cmd(repo_root, command, args.dry_run) != 0:
            print(f"[{_now()}] Pre-freeze readiness: FAIL")
            return EXIT_VALIDATE_FAIL
    rc = _run_python_cmd(
        repo_root,
        ["scripts/freeze_stage2b_snapshot.py", "--reviewer", args.reviewer],
        args.dry_run,
    )
    if rc != 0:
        print(f"[{_now()}] Stage 2B snapshot freeze: FAIL (exit={rc})")
        return EXIT_STAGE_FAIL
    print(f"[{_now()}] Stage 2B snapshot freeze: PASS")
    return EXIT_OK


def cmd_status(args: argparse.Namespace, repo_root: Path) -> int:
    lock = repo_root / "artifacts" / "orchestrator" / ".workflow_cli.lock"
    print("Workflow CLI status")
    print(f"- lock_file: {lock} ({'present' if lock.exists() else 'absent'})")
    print("- stages:")
    for key in STAGE_ORDER:
        stage = STAGES[key]
        runner_ok = (repo_root / stage.runner).exists()
        validator_ok = (repo_root / stage.validator).exists()
        print(
            f"  - {stage.key}: runner={'ok' if runner_ok else 'missing'} validator={'ok' if validator_ok else 'missing'}"
        )
    manifest = repo_root / "artifacts" / "orchestrator" / "workflow_cli_runs.jsonl"
    print(f"- run_manifest: {manifest} ({'present' if manifest.exists() else 'absent'})")
    return EXIT_OK


def cmd_arch_compare(args: argparse.Namespace, repo_root: Path) -> int:
    cmd = [
        "scripts/run_stage6_architecture_comparison.py",
        "--project-to-compare",
        args.project_to_compare,
    ]
    if args.workspace_root:
        cmd.extend(["--workspace-root", args.workspace_root])
    if args.output_dir:
        cmd.extend(["--output-dir", args.output_dir])
    if args.output_path:
        cmd.extend(["--output-path", args.output_path])

    rc = _run_python_cmd(repo_root, cmd, args.dry_run)
    _log_manifest(
        repo_root,
        {
            "ts": _now(),
            "stage": "arch-compare",
            "kind": "arch_compare",
            "script": "scripts/run_stage6_architecture_comparison.py",
            "attempt": 1,
            "exit_code": rc,
            "project_to_compare": args.project_to_compare,
        },
    )
    if rc != 0:
        print(f"[{_now()}] Architecture comparison: FAIL (exit={rc})")
        return EXIT_STAGE_FAIL
    print(f"[{_now()}] Architecture comparison: PASS")
    return EXIT_OK


def cmd_drs_after_stage2a(args: argparse.Namespace, repo_root: Path) -> int:
    _require_pre_freeze_gate(repo_root)
    cmd = ["scripts/run_stage5_drs_gate.py", "--requirements-only"]
    rc = _run_python_cmd(repo_root, cmd, args.dry_run)
    _log_manifest(
        repo_root,
        {
            "ts": _now(),
            "stage": "5",
            "kind": "drs_after_stage2a",
            "script": "scripts/run_stage5_drs_gate.py",
            "attempt": 1,
            "exit_code": rc,
            "requirements_only": True,
        },
    )
    if rc != 0:
        print(f"[{_now()}] Stage 5 requirements-only DRS path: FAIL (exit={rc})")
        return EXIT_STAGE_FAIL
    print(f"[{_now()}] Stage 5 requirements-only DRS path: PASS")
    return EXIT_OK


def cmd_final_sysml(args: argparse.Namespace, repo_root: Path) -> int:
    if bool(args.snapshot_id) == bool(args.use_latest_approved):
        raise ValueError("Final SysML requires exactly one of --snapshot-id or --use-latest-approved")
    selected_snapshot_id = _resolve_workflow_snapshot(
        repo_root,
        args.snapshot_id,
        args.use_latest_approved,
    )
    command = ["scripts/run_final_sysml_phase.py", "--snapshot-id", selected_snapshot_id]
    rc = _run_python_cmd(repo_root, command, args.dry_run)
    _log_manifest(
        repo_root,
        {
            "ts": _now(),
            "stage": "final-sysml",
            "kind": "final_sysml",
            "script": command[0],
            "snapshot_id": selected_snapshot_id,
            "attempt": 1,
            "exit_code": rc,
        },
    )
    if rc != 0:
        print(f"[{_now()}] Final SysML phase: FAIL (exit={rc})")
        return EXIT_STAGE_FAIL
    print(f"[{_now()}] Final SysML phase: PASS")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Deterministic local workflow CLI for Stage 0 to 7 (script-only, no LLM calls).",
        epilog=CLI_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repository root path. Default: auto-detect from scripts/workflow_cli.py location.",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser(
        "run",
        help="Run one stage or an ascending stage range",
        description=(
            "Run pipeline agents in canonical top-down order.\n"
            "Use --stage for one stage or --from-stage/--to-stage for an ascending range."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_run.add_argument("--stage", default=None, help=f"Single stage key. {SINGLE_STAGE_HELP}")
    p_run.add_argument("--from-stage", dest="from_stage", default=None, help=f"Ascending range start. {STAGE_HELP}")
    p_run.add_argument("--to-stage", dest="to_stage", default=None, help=f"Ascending range end. {STAGE_HELP}")
    p_run.add_argument("--snapshot-id", default=None, help="Explicit approved canonical snapshot ID for Stages 3-7")
    p_run.add_argument("--use-latest-approved", action="store_true", help="Select latest approved snapshot once, then use its ID for Stages 3-7")
    p_run.add_argument("--dry-run", action="store_true", help="Print the commands without executing them.")
    p_run.epilog = "Help: python scripts/workflow_cli.py run --help"

    p_val = sub.add_parser(
        "validate",
        help="Run gate validators",
        description="Validate one stage gate or all stage gates.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_val.add_argument("--all", action="store_true", help="Validate all stages in canonical order.")
    p_val.add_argument("--stage", default=None, help=f"Validate one stage key. {STAGE_HELP}")
    p_val.add_argument("--snapshot-id", default=None, help="Explicit approved canonical snapshot ID for Stages 3-7")
    p_val.add_argument("--use-latest-approved", action="store_true", help="Select latest approved snapshot once, then use its ID for Stages 3-7")
    p_val.add_argument("--dry-run", action="store_true", help="Print the commands without executing them.")
    p_val.epilog = "Help: python scripts/workflow_cli.py validate --help"

    p_downstream = sub.add_parser(
        "validate-downstream",
        help="Run project-agnostic downstream retrieval/mapping validation",
        description=(
            "Validate retrieval, evidence preservation, mapping, hierarchy, scope, and downstream rendering "
            "after the approved pipeline run. This command is local-only, deterministic, and advisory; it "
            "never applies recommendations."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_downstream.add_argument("--config", default=None, help="Project benchmark configuration JSON.")
    p_downstream.add_argument("--enable-semantic", action="store_true", help="Explicitly evaluate configured local semantic widening.")
    p_downstream.add_argument("--dry-run", action="store_true", help="Print the command without executing it.")
    p_downstream.epilog = "Help: python scripts/workflow_cli.py validate-downstream --help"

    p_tax = sub.add_parser(
        "taxonomy-update",
        help="Run deterministic Stage 1 taxonomy cross-check/update",
        description=(
            "Run the standalone deterministic taxonomy updater from OCR index.csv.\n"
            "This command executes scripts/run_taxonomy_crosscheck_update.py only (no LLM calls)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_tax.add_argument(
        "--index-csv",
        default="artifacts/stage1_requirements/ocr_extracts/index.csv",
        help="Path to OCR index CSV used as taxonomy update source.",
    )
    p_tax.add_argument(
        "--initial-spec",
        default=None,
        help="Optional explicit source spec path (.pdf/.html/.docx).",
    )
    p_tax.add_argument("--dry-run", action="store_true", help="Print the command without executing it.")
    p_tax.epilog = "Help: python scripts/workflow_cli.py taxonomy-update --help"

    p_snapshot = sub.add_parser(
        "freeze-stage2b",
        help="Freeze the approved Stage 2B architecture mapping snapshot",
    )
    p_snapshot.add_argument("--reviewer", required=True, help="Reviewer name or ID recorded in the snapshot")
    p_snapshot.add_argument("--dry-run", action="store_true", help="Print the command without executing it.")

    p_cmp = sub.add_parser(
        "arch-compare",
        help="Run Stage 6 architectural comparison against another workspace project",
        description=(
            "Run scripts/run_stage6_architecture_comparison.py with a sibling project name.\n"
            "Use --project-to-compare <project_name> to select the comparison target."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_cmp.add_argument(
        "--project-to-compare",
        required=True,
        help="Sibling project directory name in the same workspace root.",
    )
    p_cmp.add_argument(
        "--workspace-root",
        default=None,
        help="Optional workspace root path containing project directories.",
    )
    p_cmp.add_argument(
        "--output-dir",
        default=None,
        help="Optional output folder for comparison artifacts (default: artifacts/comparison).",
    )
    p_cmp.add_argument(
        "--output-path",
        default=None,
        help="Optional explicit final report markdown path.",
    )
    p_cmp.add_argument("--dry-run", action="store_true", help="Print the command without executing it.")
    p_cmp.epilog = "Help: python scripts/workflow_cli.py arch-compare --help"

    p_drs = sub.add_parser(
        "drs-after-stage2a",
        help="Run Stage 5 DRS directly after Stage 2A (skip Stage 3/4 generation)",
        description=(
            "Execute scripts/run_stage5_drs_gate.py in requirements-only mode.\n"
            "This path uses Stage 1 + Stage 2A artifacts and does not require running Stage 3/4."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_drs.add_argument("--dry-run", action="store_true", help="Print the command without executing it.")
    p_drs.epilog = "Help: python scripts/workflow_cli.py drs-after-stage2a --help"

    p_sysml = sub.add_parser(
        "final-sysml",
        help="Generate and centrally validate the complete final SysML set",
        description="Generate final SysML from one approved snapshot, run structural review, then invoke the central downstream validator.",
    )
    p_sysml.add_argument("--snapshot-id", default=None, help="Explicit approved canonical snapshot ID")
    p_sysml.add_argument("--use-latest-approved", action="store_true", help="Select latest approved snapshot once")
    p_sysml.add_argument("--dry-run", action="store_true", help="Print the command without executing it.")

    p_digital = sub.add_parser("digital-ipos", help="Generate and validate digital IPOS from the approved snapshot")
    p_digital.add_argument("--snapshot-id", default=None, help="Explicit approved canonical snapshot ID")
    p_digital.add_argument("--use-latest-approved", action="store_true", help="Select latest approved snapshot once")
    p_digital.add_argument("--dry-run", action="store_true", help="Print the command without executing it.")

    p_analog = sub.add_parser("analog-ipos", help="Generate and validate analog IPOS from the approved snapshot")
    p_analog.add_argument("--snapshot-id", default=None, help="Explicit approved canonical snapshot ID")
    p_analog.add_argument("--use-latest-approved", action="store_true", help="Select latest approved snapshot once")
    p_analog.add_argument("--dry-run", action="store_true", help="Print the command without executing it.")

    sub.add_parser("status", help="Show workflow CLI status")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
    else:
        repo_root = Path(__file__).resolve().parent.parent

    if args.command == "status":
        return cmd_status(args, repo_root)

    try:
        lock_path = _acquire_lock(repo_root)
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        print("Help: python scripts/workflow_cli.py --help")
        return EXIT_USAGE

    try:
        try:
            if args.command == "run":
                return cmd_run(args, repo_root)
            if args.command == "validate":
                return cmd_validate(args, repo_root)
            if args.command == "validate-downstream":
                return cmd_validate_downstream(args, repo_root)
            if args.command == "taxonomy-update":
                return cmd_taxonomy_update(args, repo_root)
            if args.command == "freeze-stage2b":
                return cmd_freeze_stage2b(args, repo_root)
            if args.command == "arch-compare":
                return cmd_arch_compare(args, repo_root)
            if args.command == "drs-after-stage2a":
                return cmd_drs_after_stage2a(args, repo_root)
            if args.command == "final-sysml":
                return cmd_final_sysml(args, repo_root)
            if args.command == "digital-ipos":
                return cmd_ipos(args, repo_root, "6")
            if args.command == "analog-ipos":
                return cmd_ipos(args, repo_root, "7")
            print(f"Unknown command: {args.command}")
            print("Help: python scripts/workflow_cli.py --help")
            return EXIT_USAGE
        except ValueError as exc:
            print(f"ERROR: {exc}")
            print("Help: python scripts/workflow_cli.py --help")
            if args.command:
                print(f"Command help: python scripts/workflow_cli.py {args.command} --help")
            return EXIT_USAGE
    finally:
        _release_lock(lock_path)


if __name__ == "__main__":
    raise SystemExit(main())
