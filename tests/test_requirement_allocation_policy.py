from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from requirement_allocation_policy import (  # noqa: E402
    BLOCK_LOCAL_DIGITAL,
    SYSTEM_LEVEL,
    TOP_DIGITAL_ARCHITECTURE,
    accounting_status,
    allocation_row,
    direct_ipos_is_eligible,
    nearest_parent,
    rule_for,
    topic_policy,
    validate_allocation_rows,
)


def test_classes_define_valid_and_required_targets():
    assert rule_for(SYSTEM_LEVEL).required_downstream_targets == ("SRS",)
    assert rule_for(TOP_DIGITAL_ARCHITECTURE).owning_target == "DRS"
    assert rule_for(TOP_DIGITAL_ARCHITECTURE).required_downstream_targets == ("DRS",)
    assert rule_for(BLOCK_LOCAL_DIGITAL).direct_ipos_allowed is True
    assert rule_for(BLOCK_LOCAL_DIGITAL).forbidden_targets == ("SRS", "DRS")


def test_nearest_parent_prefers_architecture_parent_for_digital_ipos():
    assert nearest_parent(BLOCK_LOCAL_DIGITAL, ("Source", "SRS", "DRS")) == "DRS"
    assert nearest_parent(BLOCK_LOCAL_DIGITAL, ("Source", "SRS")) == "SRS"


def test_direct_block_local_source_to_ipos_is_not_under_covered():
    row = allocation_row(
        req_id="SRC-001",
        source_type="primary",
        spec_level="Digital IPOS",
        requirement_class=BLOCK_LOCAL_DIGITAL,
        actual_targets=("Digital IPOS",),
        rendered_in_specs=("Digital IPOS",),
        direct_source_to_ipos=True,
        owning_block="Controller",
        lineage_mode="direct_source_to_ipos",
    )
    assert row["coverage_status"] == "covered"
    assert row["direct_source_to_ipos"] == "true"
    assert row["lineage_mode"] == "direct_source_to_ipos"


def test_architecture_requirement_needs_both_system_and_digital_levels():
    assert accounting_status(TOP_DIGITAL_ARCHITECTURE, ("SRS",)) == "under_covered"
    assert accounting_status(TOP_DIGITAL_ARCHITECTURE, ("SRS", "DRS")) == "covered"


def test_direct_ipos_requires_all_explicit_gates():
    assert direct_ipos_is_eligible(
        BLOCK_LOCAL_DIGITAL,
        source_type="supplementary",
        approved=True,
        in_scope=True,
        owning_block="Controller",
        mixed_requirement=False,
        meaningful_intermediate=False,
        lineage_preserved=True,
    )
    assert not direct_ipos_is_eligible(
        BLOCK_LOCAL_DIGITAL,
        source_type="primary",
        approved=True,
        in_scope=True,
        owning_block="Controller",
        mixed_requirement=True,
        meaningful_intermediate=False,
        lineage_preserved=True,
    )


def test_topic_policy_forbids_local_detail_in_architecture_documents():
    assert topic_policy("local_register_access") == ("Digital IPOS",)
    assert topic_policy("shared_interconnect_resource") == ("DRS",)


def test_split_lineage_is_separate_from_coverage_status():
    row = allocation_row(
        req_id="SRC-002",
        source_type="primary",
        spec_level="DRS",
        requirement_class=TOP_DIGITAL_ARCHITECTURE,
        actual_targets=("DRS",),
        lineage_mode="split_lineage",
        split_parent_req_id="SRC-001",
    )
    assert row["coverage_status"] == "covered"
    assert row["lineage_mode"] == "split_lineage"


def test_validator_rejects_unchanged_block_local_upward_rendering():
    row = allocation_row(
        req_id="SRC-003",
        source_type="primary",
        spec_level="DRS",
        requirement_class=BLOCK_LOCAL_DIGITAL,
        owning_block="Controller",
        actual_targets=("DRS", "Digital IPOS"),
    )
    findings = validate_allocation_rows((row,))
    assert any("forbidden upward targets" in finding for finding in findings)
