"""Authoritative requirement corpus and approved-stage input resolution.

Business logic must use this module instead of selecting requirement CSV exports.
CSV files remain storage/export artifacts only.
"""

from __future__ import annotations

import csv
import hashlib
import json
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional

from canonical_store import canonical_db_path, connect, resolve_snapshot
from requirement_allocation_policy import requires_hierarchy_parent


PRIMARY_CORPUS = Path("artifacts/stage1_requirements/requirements_summary.csv")
INTEGRATED_CORPUS = Path("artifacts/stage1_requirements/integrated_requirements.csv")
SNAPSHOT_PATH = Path("artifacts/stage1_specs/approved_mapping_snapshot.json")
SNAPSHOT_ROWS_PATH = Path("artifacts/stage1_specs/approved_mapping_snapshot.csv")


class CorpusResolutionError(RuntimeError):
    """Raised when a stage cannot obtain an authoritative input view."""


def authoritative_store_path(repo_root: Path) -> Path:
    """Return the authoritative SQLite path; retrieval indexes are separate."""
    return canonical_db_path(repo_root)


@dataclass(frozen=True)
class RequirementInput:
    """Resolver-issued immutable input view for a downstream stage."""

    stage: str
    snapshot_id: str
    corpus_hash: str
    snapshot_hash: str
    source_path: Path
    rows: tuple[Dict[str, str], ...]
    source_links: Mapping[str, tuple[str, ...]]
    mapping: Mapping[str, str]
    allocation: Mapping[str, Mapping[str, str]] = field(default_factory=dict)

    @property
    def requirement_ids(self) -> tuple[str, ...]:
        return tuple(row.get("source_req_id") or row.get("id") or "" for row in self.rows)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise CorpusResolutionError(f"Resolver input is missing: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _repo_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def authoritative_corpus_path(repo_root: Path) -> Path:
    """Return the authoritative corpus path; only this function may choose it."""
    integrated = repo_root / INTEGRATED_CORPUS
    primary = repo_root / PRIMARY_CORPUS
    if integrated.exists():
        return integrated
    if primary.exists():
        return primary
    raise CorpusResolutionError("No tracked requirement corpus is available.")


def _row_id(row: Mapping[str, str]) -> str:
    return (row.get("canonical_id") or row.get("source_req_id") or row.get("id") or "").strip()


def _links(row: Mapping[str, str]) -> tuple[str, ...]:
    values = [row.get("source_req_id", "")]
    if not values[0].strip() and not row.get("canonical_id", "").strip():
        values.append(row.get("id", ""))
    values.extend((row.get("source_req_ids") or "").replace(",", ";").split(";"))
    return tuple(dict.fromkeys(value.strip() for value in values if value.strip()))


def _legacy_input(repo_root: Path, stage: str) -> RequirementInput:
    corpus = authoritative_corpus_path(repo_root)
    rows = _read_csv(corpus)
    source_links = {_row_id(row): _links(row) for row in rows if _row_id(row)}
    mapping = {key: (row.get("mapped_block") or row.get("approved_block") or "").strip() for key, row in ((_row_id(row), row) for row in rows) if key}
    return RequirementInput(
        stage=stage,
        snapshot_id="legacy-unfrozen",
        corpus_hash=_sha256(corpus),
        snapshot_hash="legacy",
        source_path=corpus,
        rows=tuple(rows),
        source_links=source_links,
        mapping=mapping,
    )


def load_approved_input(repo_root: Path, stage: str, *, allow_legacy: bool = False) -> RequirementInput:
    """Load a resolver-issued input view for a downstream generator or validator.

    Downstream stages should set ``allow_legacy=False``. The compatibility option is
    only for migration and primary-only historical runs.
    """
    snapshot = repo_root / SNAPSHOT_PATH
    rows_path = repo_root / SNAPSHOT_ROWS_PATH
    if not snapshot.exists() or not rows_path.exists():
        if allow_legacy:
            warnings.warn(
                "load_approved_input(..., allow_legacy=True) uses compatibility artifacts and is non-authoritative.",
                DeprecationWarning,
                stacklevel=2,
            )
            return _legacy_input(repo_root, stage)
        raise CorpusResolutionError(
            f"Stage {stage} requires an approved Stage 2B mapping snapshot: {SNAPSHOT_PATH}"
        )

    try:
        metadata = json.loads(snapshot.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CorpusResolutionError(f"Invalid approved mapping snapshot: {snapshot}") from exc
    if metadata.get("status") != "approved":
        raise CorpusResolutionError("Approved mapping snapshot status is not approved.")
    snapshot_hash = _sha256(snapshot)
    expected_rows_hash = str(metadata.get("snapshot_rows_sha256") or "")
    if expected_rows_hash and expected_rows_hash != _sha256(rows_path):
        raise CorpusResolutionError("Approved mapping snapshot rows have changed.")
    corpus = authoritative_corpus_path(repo_root)
    expected_corpus_hash = str(metadata.get("corpus_sha256") or "")
    if expected_corpus_hash and expected_corpus_hash != _sha256(corpus):
        raise CorpusResolutionError("Authoritative corpus changed since Stage 2B approval.")

    rows = _read_csv(rows_path)
    source_links = {_row_id(row): _links(row) for row in rows if _row_id(row)}
    mapping = {key: (row.get("mapped_block") or row.get("approved_block") or "").strip() for key, row in ((_row_id(row), row) for row in rows) if key}
    return RequirementInput(
        stage=stage,
        snapshot_id=str(metadata.get("snapshot_id") or ""),
        corpus_hash=_sha256(corpus),
        snapshot_hash=snapshot_hash,
        source_path=rows_path,
        rows=tuple(rows),
        source_links=source_links,
        mapping=mapping,
    )


def load_sqlite_snapshot_input(
    repo_root: Path,
    stage: str,
    *,
    snapshot_id: str | None = None,
    use_latest_approved: bool = False,
) -> RequirementInput:
    """Load a snapshot from canonical SQLite using an explicit selector.

    This is the migration boundary for downstream generators. It intentionally
    does not infer a latest snapshot when neither selector is supplied.
    """
    try:
        connection = connect(repo_root)
        snapshot = resolve_snapshot(
            connection,
            snapshot_id=snapshot_id,
            use_latest_approved=use_latest_approved,
        )
        revision_ids = json.loads(snapshot["canonical_revision_set_json"] or "[]")
        if not isinstance(revision_ids, list) or not revision_ids:
            raise CorpusResolutionError("Approved snapshot has no canonical revision set.")
        placeholders = ",".join("?" for _ in revision_ids)
        rows = connection.execute(
            f"""SELECT crr.revision_id, cr.canonical_requirement_id AS canonical_id,
                       cr.source_req_id, crr.requirement_text AS requirement_statement,
                       crr.approved_classification, crr.lifecycle_state
                FROM canonical_requirement_revisions crr
                JOIN canonical_requirements cr
                  ON cr.canonical_requirement_id = crr.canonical_requirement_id
               WHERE crr.revision_id IN ({placeholders})
               ORDER BY cr.canonical_requirement_id""",
            revision_ids,
        ).fetchall()
        if len(rows) != len(revision_ids):
            raise CorpusResolutionError("Approved snapshot references missing canonical revisions.")
        materialized = [dict(row) for row in rows]
        source_links = {
            row["canonical_id"]: tuple(
                item[0] for item in connection.execute(
                    "SELECT source_req_id FROM requirement_provenance WHERE revision_id = ? ORDER BY provenance_id",
                    (row["revision_id"],),
                ).fetchall() if item[0]
            ) for row in materialized
        }
        mapping = {
            row["canonical_id"]: (mapping_row[0] or "")
            for row in materialized
            for mapping_row in connection.execute(
                "SELECT approved_block FROM architecture_mappings WHERE canonical_requirement_id = ? AND lifecycle_state = 'approved' ORDER BY mapping_id LIMIT 1",
                (row["canonical_id"],),
            ).fetchall()
        }
        mapping_ids = json.loads(snapshot["mapping_revision_set_json"] or "[]")
        if not isinstance(mapping_ids, list) or not mapping_ids:
            raise CorpusResolutionError("Approved snapshot has no allocation mapping set.")
        mapping_placeholders = ",".join("?" for _ in mapping_ids)
        allocation_rows = connection.execute(
            f"""SELECT am.mapping_id, am.canonical_requirement_id, am.allocation_class,
                       am.owning_target, am.allocation_rationale, am.lineage_mode,
                       am.source_origin_req_ids, am.hierarchy_parent_req_ids,
                       am.lineage_candidate_parent_req_ids, am.owning_domain,
                       am.approved_block
                  FROM architecture_mappings am
                 WHERE am.mapping_id IN ({mapping_placeholders})
                   AND am.lifecycle_state = 'approved'""",
            mapping_ids,
        ).fetchall()
        if len(allocation_rows) != len(mapping_ids):
            raise CorpusResolutionError("Approved snapshot references missing approved allocation mappings.")
        required_allocation_fields = (
            "allocation_class", "owning_target", "lineage_mode", "source_origin_req_ids"
        )
        incomplete = [
            str(row["canonical_requirement_id"])
            for row in allocation_rows
            if any(not str(row[field] or "").strip() for field in required_allocation_fields)
            or (
                requires_hierarchy_parent(
                    str(row["allocation_class"] or "").strip(),
                    str(row["lineage_mode"] or "").strip(),
                )
                and not str(row["hierarchy_parent_req_ids"] or "").strip()
            )
        ]
        if incomplete:
            raise CorpusResolutionError(
                "Approved snapshot contains incomplete allocation metadata for canonical requirements: "
                + ", ".join(incomplete[:10])
            )
        allocation = {
            str(row["canonical_requirement_id"]): {
                key: str(row[key] or "").strip()
                for key in row.keys()
                if key not in {"mapping_id", "canonical_requirement_id"}
            }
            for row in allocation_rows
        }
        db_path = authoritative_store_path(repo_root)
        snapshot_material_hash = str(snapshot["content_fingerprint"] or "")
        return RequirementInput(
            stage=stage,
            snapshot_id=str(snapshot["snapshot_id"]),
            corpus_hash=snapshot_material_hash,
            snapshot_hash=snapshot_material_hash,
            source_path=db_path,
            rows=tuple(materialized),
            source_links=source_links,
            mapping=mapping,
            allocation=allocation,
        )
    except (OSError, ValueError, LookupError, PermissionError, json.JSONDecodeError, KeyError) as exc:
        raise CorpusResolutionError(f"Cannot resolve canonical SQLite snapshot for stage {stage}: {exc}") from exc
    finally:
        try:
            connection.close()
        except UnboundLocalError:
            pass


def write_approved_snapshot(
    repo_root: Path,
    rows: Iterable[Mapping[str, str]],
    *,
    snapshot_id: str,
    approved_by: str,
    mapping_preview_hash: str,
) -> Path:
    """Write an immutable Stage 2B snapshot from already approved mapping rows."""
    materialized = [{key: str(value or "").strip() for key, value in row.items()} for row in rows]
    if not materialized:
        raise CorpusResolutionError("Cannot freeze an empty architecture mapping.")
    rows_path = repo_root / SNAPSHOT_ROWS_PATH
    rows_path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(key for row in materialized for key in row))
    with rows_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(materialized)
    corpus = authoritative_corpus_path(repo_root)
    metadata = {
        "schema_version": 1,
        "status": "approved",
        "snapshot_id": snapshot_id,
        "approved_by": approved_by,
        "mapping_preview_sha256": mapping_preview_hash,
        "corpus_sha256": _sha256(corpus),
        "snapshot_rows_sha256": _sha256(rows_path),
        "row_count": len(materialized),
    }
    snapshot = repo_root / SNAPSHOT_PATH
    snapshot.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return snapshot
