"""Shared derived relation contract; callers supply snapshot-eligible evidence only."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass


RELATION_POLICY_VERSION = "governed-three-view-relations-v1"
RELATION_CLASSES = ("containment", "block_relation", "signal_connection")


def port_identifier(value: str) -> str:
    name = re.sub(r"[^A-Za-z0-9_]", "_", (value or "").strip())
    name = re.sub(r"_+", "_", name).strip("_") or "unnamedPort"
    return "port_" + name if name[0].isdigit() else name


def connection_statement(statement: str):
    match = re.fullmatch(r"(?:The\s+)?(.*?)\s+signal\s+shall be connected to the\s+(.*?)\s+signal(?:, with frequency (.+?)(?: and (with|without) clock gating(?:\s+(.+?))?)?)?\.?", statement.strip(), re.I)
    if not match:
        return None
    source, target, frequency, gating, control = match.groups()
    kind = ("clock" if frequency or re.search(r"(?:^|[._\s])(?:clk|clock)", source + " " + target, re.I)
            else "reset" if re.search(r"(?:^|[._\s])(?:reset|rst|hreset)", source + " " + target, re.I) else "signal")
    qualifiers = tuple((name, value) for name, value in (("frequency", frequency), ("gating", gating), ("control", control)) if value)
    return kind, source, target, qualifiers


def block_statement(statement: str):
    match = re.fullmatch(r"(?:The\s+)?(.+?)\s+(?:shall\s+)?(?:provide|provides|send|sends|transfer|transfers)\s+(?:the\s+)?(.+?)\s+to\s+(?:the\s+)?(.+?)\.?", statement.strip(), re.I)
    if match:
        source, payload, target = match.groups()
        kind = {"clock": "clock", "clocks": "clock", "clock signals": "clock", "reset": "reset",
                "resets": "reset", "reset signals": "reset", "data": "data", "control signals": "control",
                "status": "status"}.get(payload.casefold(), "interaction")
        return kind, source, target, (("payload", payload),)
    match = re.fullmatch(r"(?:The\s+)?(.+?)\s+(?:shall\s+)?(?:depend|depends)\s+on\s+(?:the\s+)?(.+?)\.?", statement.strip(), re.I)
    if match:
        return "dependency", match[1], match[2], ()
    match = re.fullmatch(r"(?:The\s+)?(.+?)\s+(?:shall\s+)?(?:communicate|communicates)\s+with\s+(?:the\s+)?(.+?)\.?", statement.strip(), re.I)
    return ("interaction", match[1], match[2], ()) if match else None


def io_connection_reference(details: str):
    details = details.strip()
    candidates = list(re.finditer(r"(?<![\w.])([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*\.)(?!\w)|(?<![\w.])([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+)(?![\w.])", details))
    if not candidates:
        return None
    if len(candidates) != 1 or candidates[0].end() != len(details) or re.search(r"\b(?:not|unconnected|open|except|unless|if|or)\b", details, re.I):
        return "", "Connection-table reference is conditional, ambiguous or requires unsupported projection grammar"
    peer = candidates[0][0]
    return (peer, "Connection-table peer port is incomplete; source text is preserved without repair") if peer.endswith(".") else (peer, "")


def io_block_reference(details: str):
    text = re.sub(r"^(?:wire|logic|reg)\s+", "", details.strip(), flags=re.I)
    if re.search(r"\b(?:not|unconnected|open|except|unless|if|or|and)\b", text, re.I):
        return None
    directed = re.fullmatch(r"(?:(?:test|\d+(?:\.\d+)?\s*(?:[kM](?:Hz)?|Hz))\s+)?(clock|clk|reset)(?:\s+(?:slow|fast|master|slave|\d+(?:\.\d+)?(?:[kM](?:Hz)?|Hz)?|MHz|kHz|Hz))*\s+(to|for|from)\s+(?:the\s+)?([A-Za-z][\w /-]*)", text, re.I)
    if directed:
        kind, role, label = directed.groups()
        return label.strip(), role.casefold(), "reset" if kind.casefold() == "reset" else "clock"
    exchange = re.fullmatch(r"(?:(?:AHB|APB|AXI|XBAR)\s+)?(bus|interconnect|interaction|communication|data|control|status)(?:\s+(?:connection|interface|link|transfer|signals?))?\s+(to|for|from|with)\s+(?:the\s+)?([A-Za-z][\w /-]*)", text, re.I)
    if exchange:
        payload, role, label = exchange.groups()
        kind = "bus" if payload.casefold() in {"bus", "interconnect"} else "interaction" if payload.casefold() in {"interaction", "communication"} else payload.casefold()
        return label.strip(), "peer" if role.casefold() == "with" else role.casefold(), kind
    associated = re.fullmatch(r"([A-Za-z][\w /-]*?)\s+(?:(?:master|slave)\s+)?(clock|clk|reset)(?:\s+elaboration)?", text, re.I)
    if associated:
        label, kind = associated.groups()
        return label.strip(), "associated", "reset" if kind.casefold() == "reset" else "clock"
    reset = re.fullmatch(r"reset\s+(?:\d+(?:\.\d+)?\s*(?:Hz|kHz|MHz)\s+domain\s+)?([A-Za-z][\w /-]*)", text, re.I)
    return (reset[1].strip(), "associated", "reset") if reset else None


@dataclass(frozen=True)
class RelationEndpoint:
    block: str
    node: str = ""
    port: str = ""
    direction: str = ""
    token: str = ""
    status: str = "resolved"

    @property
    def address(self) -> str:
        return self.node + ("." + self.port if self.port else "")


@dataclass(frozen=True)
class GovernedRelation:
    identity: str
    relation_class: str
    kind: str
    source: RelationEndpoint
    target: RelationEndpoint
    evidence: tuple[str, ...]
    snapshot_id: str
    qualifiers: tuple[tuple[str, str], ...] = ()
    status: str = "resolved"
    reason: str = ""


@dataclass(frozen=True)
class RelationInventory:
    snapshot_id: str
    relations: tuple[GovernedRelation, ...]
    gaps: tuple[dict, ...] = ()
    policy_version: str = RELATION_POLICY_VERSION
    blocks: tuple[str, ...] = ()
    signal_checks: tuple[dict, ...] = ()

    def view(self, relation_class: str) -> tuple[GovernedRelation, ...]:
        if relation_class not in RELATION_CLASSES:
            raise ValueError("Unknown relation class: " + relation_class)
        return tuple(row for row in self.relations if row.relation_class == relation_class)

    def payload(self) -> dict:
        return json.loads(json.dumps({"authority": False, **asdict(self)}))

    @property
    def fingerprint(self) -> str:
        return hashlib.sha256(json.dumps(self.payload(), sort_keys=True).encode("utf-8")).hexdigest()


def relation_record(relation_class, kind, source, target, evidence, snapshot_id, *, qualifiers=(), status="resolved", reason=""):
    if relation_class not in RELATION_CLASSES or not evidence or not snapshot_id:
        raise ValueError("Relations require a known class, evidence and snapshot")
    if relation_class == "signal_connection" and (not source.port or not target.port or not source.node or not target.node
            or source.status != "resolved" or target.status != "resolved" or source.direction not in {"out", "inout"}
            or target.direction not in {"in", "inout"}):
        raise ValueError("Signal relations require explicit resolved directed ports")
    payload = [relation_class, kind, asdict(source), asdict(target), list(qualifiers), snapshot_id]
    identity = "relation_" + hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:20]
    return GovernedRelation(identity, relation_class, kind, source, target, tuple(evidence), snapshot_id,
                            tuple(qualifiers), status, reason)


def endpoint_resolution_issue(source, target, qualifiers=()):
    peer = dict(qualifiers).get("peer_endpoint", "")
    if peer.endswith("."):
        return "incomplete_reference", "The documented peer path has no port suffix; its missing text cannot be inferred"
    for endpoint in (source, target):
        if endpoint.status == "conflicting":
            return "identity_conflict", "More than one admitted identity matches endpoint " + endpoint.token
        if endpoint.status == "outside_scope":
            return "outside_scope", "Endpoint is outside the materialized block scope: " + endpoint.token
        if not endpoint.node:
            return "unmapped_instance", "No exact admitted block/instance identity resolves endpoint " + endpoint.token
    if not source.port or not target.port:
        if dict(qualifiers).get("reference_level") == "block" or (not peer and all(endpoint.token in {endpoint.node, endpoint.block} for endpoint in (source, target))):
            return "block_only", "Documented block interaction has no pin-level contract; it is not a missing physical wire"
        missing = source if not source.port else target
        return "port_not_found", "Block identity is known, but no unique exact approved port resolves endpoint " + missing.token
    if not source.direction or not target.direction:
        return "direction_missing", "Both endpoints require an explicit approved direction"
    if source.direction not in {"out", "inout"} or target.direction not in {"in", "inout"}:
        return "direction_conflict", "Approved endpoint directions do not support the documented source-to-target connection"
    return "resolved", "Both exact scoped ports and compatible directions are established; serialization is checked separately"


def documented_link(kind, source, target, evidence, snapshot_id, *, qualifiers=()):
    """Retain block precision without promoting unsupported endpoints to wiring."""
    known_blocks = source.node and target.node and source.status == target.status == "resolved"
    block_source = RelationEndpoint(source.block, source.node, token=source.block, status=source.status)
    block_target = RelationEndpoint(target.block, target.node, token=target.block, status=target.status)
    status = "resolved" if known_blocks else "conflicting" if "conflicting" in {source.status, target.status} else "outside_scope" if "outside_scope" in {source.status, target.status} else "unresolved"
    block = relation_record("block_relation", kind, block_source, block_target, evidence, snapshot_id,
                            qualifiers=qualifiers, status=status,
                            reason="" if known_blocks else "Block identity is unresolved, conflicting or explicitly outside the selected scope")
    records, gaps = [block], []
    if (known_blocks and source.port and target.port
            and source.direction in {"out", "inout"} and target.direction in {"in", "inout"}):
        records.append(relation_record("signal_connection", kind, source, target, evidence, snapshot_id, qualifiers=qualifiers))
    else:
        resolution_status, resolution_reason = endpoint_resolution_issue(source, target, qualifiers)
        gaps.append({"relation_id": block.identity, "view": "signal_connection", "kind": kind,
                     "resolution_status": resolution_status,
                     "qualifiers": list(qualifiers),
                     "status": "conflicting" if source.direction == "in" or target.direction == "out" else "unresolved" if known_blocks else status,
                     "source": asdict(source), "target": asdict(target), "evidence": list(evidence),
                     "reason": resolution_reason})
    return records, gaps


def serialize_relations(inventory: RelationInventory) -> list[str]:
    lines = []
    for relation in inventory.relations:
        if relation.relation_class == "containment" or relation.status != "resolved":
            continue
        connection_type = "SignalConnection" if relation.relation_class == "signal_connection" else "BlockRelation"
        lines.append(f"        connection {relation.identity} : {connection_type} connect {relation.source.address} to {relation.target.address};")
        metadata = json.dumps(asdict(relation), sort_keys=True, ensure_ascii=True).replace("*/", "*\\u002f")
        lines.append(f"        doc {relation.identity} /* governedRelation={metadata} */;")
    return lines


def build_relation_inventory(scope, contract, port_rows, interaction_rows, *, endpoint_bindings=(), governed_interaction_rows=()) -> RelationInventory:
    from validate_downstream_coherence import connection_instance_block_keys, human_label_key

    records, gaps, signal_checks = [], [], []
    snapshot_id = scope.snapshot_id
    system = RelationEndpoint(scope.system_definition, scope.system_definition)
    parents = {"Digital IPOS": RelationEndpoint("Digital Subsystem", "topDigital"),
               "Analog IPOS": RelationEndpoint("Analog Subsystem", "topAnalog.analogSubsystem")}
    for target, parent in parents.items():
        if any(block.target == target for block in scope.blocks):
            records.append(relation_record("containment", "containment", system, parent, ("approved allocation",), snapshot_id))
    for block in scope.blocks:
        records.append(relation_record("containment", "containment", parents[block.target], RelationEndpoint(block.name, block.node),
                                       tuple(sorted(block.requirement_ids)), snapshot_id))
    approved_ports = [row for row in port_rows if row.get("Ownership status", "").casefold() == "approved"]
    ports = []
    for block in scope.blocks:
        counts = {}
        for row in approved_ports:
            if row.get("snapshot_id") and row["snapshot_id"] != snapshot_id:
                continue
            if human_label_key(row.get("Owner", "")) != block.key:
                continue
            name = row.get("Port name", "")
            base = port_identifier(name)
            counts[base] = counts.get(base, 0) + 1
            address = base if counts[base] == 1 else base + "_" + str(counts[base])
            direction = {"input": "in", "output": "out", "bidirectional": "inout", "inout": "inout"}.get(row.get("Direction", "").casefold(), "")
            ports.append((block, name, address, direction))

    def endpoint(token, explicit_block=""):
        logical_block, separator, logical_port = token.rpartition(".")
        bindings = [binding for binding in endpoint_bindings
                    if token == binding.get("endpoint") or token.startswith(str(binding.get("endpoint", "")) + ".")]
        if len(bindings) > 1:
            return RelationEndpoint(token, token=token, status="conflicting")
        if bindings:
            binding = bindings[0]
            owners = [block for block in scope.blocks if block.key == human_label_key(binding.get("block", ""))]
            if len(owners) != 1:
                return RelationEndpoint(binding.get("block", token), token=token, status="outside_scope")
            owner = owners[0]
            suffix = token[len(binding["endpoint"]):].removeprefix(".")
            port = binding.get("port", "") if not suffix else suffix
            matches = [(block, name, address, direction) for block, name, address, direction in ports
                       if block == owner and name == port]
            if len(matches) == 1:
                block, name, address, direction = matches[0]
                return RelationEndpoint(block.name, block.node, address, direction, token)
            return RelationEndpoint(owner.name, owner.node, token=token)
        matches = [(block, name, address, direction) for block, name, address, direction in ports
                   if (not explicit_block or human_label_key(explicit_block) == block.key)
                    and (token in {block.node + "." + name, block.name + "." + name, name if explicit_block else ""}
                        or (separator and human_label_key(logical_block) == block.key and logical_port == name))]
        if len(matches) == 1:
            block, name, address, direction = matches[0]
            return RelationEndpoint(block.name, block.node, address, direction, token)
        if len(matches) > 1:
            return RelationEndpoint(token, token=token, status="conflicting")
        if separator and not explicit_block:
            instance_keys = connection_instance_block_keys(logical_block, (block.name for block in scope.blocks))
            instance_owners = [block for block in scope.blocks if block.key in instance_keys]
            if len(instance_owners) > 1:
                return RelationEndpoint(token, token=token, status="conflicting")
            if len(instance_owners) == 1:
                owner = instance_owners[0]
                instance_ports = [(block, name, address, direction) for block, name, address, direction in ports
                                  if block == owner and name == logical_port]
                if len(instance_ports) == 1:
                    block, name, address, direction = instance_ports[0]
                    return RelationEndpoint(block.name, block.node, address, direction, token)
                if len(instance_ports) > 1:
                    return RelationEndpoint(owner.name, token=token, status="conflicting")
                return RelationEndpoint(owner.name, owner.node, token=token)
        block_matches = [block for block in scope.blocks if token in {block.node, block.name}
                 or token.startswith(block.node + ".") or token.startswith(block.name + ".")
                 or (separator and human_label_key(logical_block) == block.key)
                 or (explicit_block and block.key == human_label_key(explicit_block))]
        if len(block_matches) == 1:
            block = block_matches[0]
            return RelationEndpoint(block.name, block.node, token=token)
        return RelationEndpoint(explicit_block or token, token=token, status="conflicting" if len(matches) > 1 or len(block_matches) > 1 else "unresolved")

    def admit(kind, source, target, evidence, qualifiers=()):
        additions, residuals = documented_link(kind, source, target, evidence, snapshot_id, qualifiers=qualifiers)
        records.extend(additions)
        gaps.extend(residuals)

    rows = getattr(getattr(contract, "requirement_input", None), "rows", ())
    approved_statements = {row.get("source_req_id"): row.get("requirement_statement", row.get("statement", ""))
                           for row in rows if row.get("source_req_id") in contract.expected}
    admitted_interactions = {}
    admitted_requirement_ids = set()
    for index, row in enumerate(governed_interaction_rows):
        identities = tuple(item.strip() for item in row.get("Requirement IDs", "").split(";") if item.strip())
        if not identities:
            continue
        source_label, target_label = row.get("From block", "").strip(), row.get("To block", "").strip()
        exchange = row.get("Signal/control", "").strip()
        if not source_label or not target_label or not exchange or any(identity not in approved_statements for identity in identities):
            gaps.append({"view": "block_relation", "status": "unresolved", "resolution_status": "evidence_unbound", "evidence": list(identities),
                         "source": source_label, "target": target_label,
                         "reason": "Admitted interaction lacks complete endpoints, exchange or selected-snapshot requirement evidence", "candidate": dict(row)})
            continue
        source, target = endpoint(source_label, source_label), endpoint(target_label, target_label)
        from dataclasses import replace
        source = replace(source, status="outside_scope") if source.status == "unresolved" else source
        target = replace(target, status="outside_scope") if target.status == "unresolved" else target
        kind = row.get("Relation type", "").strip().casefold() or ("bus" if re.fullmatch(r"(?:bus|interconnect|crossbar|xbar)(?:\s+connection)?", exchange, re.I) else "interaction")
        qualifiers = tuple((name, value) for name, value in (("exchange", exchange), ("trigger", row.get("Trigger", "")),
                                                             ("protocol", row.get("Protocol", ""))) if value)
        admit(kind, source, target, (*identities, "snapshot_profile:interaction_rows:" + str(index + 1)), qualifiers)
        admitted_interactions[(human_label_key(source_label), human_label_key(target_label), frozenset(identities))] = kind
        admitted_requirement_ids.update(identities)
    for identity, statement in approved_statements.items():
        parsed = connection_statement(statement) or block_statement(statement)
        if parsed:
            kind, source, target, qualifiers = parsed
            admit(kind, endpoint(source), endpoint(target), (identity,), qualifiers)
        elif identity not in admitted_requirement_ids and re.search(r"\bconnect(?:ed|ion)?\b|\b(?:clock|reset)\s+(?:distribution|suppl|provid)|\b(?:send|sends|provide|provides|transfer|transfers|communicate|communicates|depend|depends)\b", statement, re.I):
            gaps.append({"view": "block_relation", "status": "non_materializable", "evidence": [identity],
                         "reason": "Approved relation candidate requires an unsupported projection grammar", "statement": statement})
    for index, row in enumerate(interaction_rows):
        identities = tuple(item.strip() for item in row.get("Requirement IDs", "").split(";") if item.strip())
        admitted_kind = admitted_interactions.get((human_label_key(row.get("From block", "")), human_label_key(row.get("To block", "")), frozenset(identities)))
        if admitted_kind:
            if row.get("Relation type", "").strip() and row["Relation type"].strip().casefold() != admitted_kind:
                gaps.append({"view": "block_relation", "status": "conflicting", "evidence": list(identities),
                             "source": row.get("From block", ""), "target": row.get("To block", ""),
                             "reason": "Derived matrix relation type conflicts with admitted profile evidence", "candidate": dict(row)})
            continue
        if not identities or any(identity not in approved_statements for identity in identities):
            gaps.append({"view": "block_relation", "status": "unresolved", "resolution_status": "evidence_unbound", "evidence": list(identities),
                         "reason": "Interaction lacks selected-snapshot requirement evidence", "candidate": dict(row), "row": index + 1})
            continue
        source, target = endpoint(row.get("From block", "")), endpoint(row.get("To block", ""))
        supported = [relation for relation in records if relation.relation_class == "block_relation"
                     and any(identity in relation.evidence for identity in identities)
                     and source.node and target.node and relation.source.node == source.node and relation.target.node == target.node]
        if not supported:
            gaps.append({"view": "block_relation", "status": "non_materializable", "evidence": list(identities),
                         "reason": "Matrix endpoints/type are not independently supported by the admitted statement grammar", "candidate": dict(row)})
            continue
        kind = row.get("Relation type", "").strip().casefold()
        if kind and any(relation.kind != kind for relation in supported):
            gaps.append({"view": "block_relation", "status": "conflicting", "evidence": list(identities),
                         "reason": "Matrix relation type conflicts with admitted evidence", "candidate": dict(row)})
    for row in approved_ports:
        owners = [block for block in scope.blocks if block.key == human_label_key(row.get("Owner", ""))]
        if len(owners) != 1:
            continue
        owner = owners[0]
        details = row.get("Type / details", "").strip()
        reference = io_connection_reference(details)
        peer, problem = reference or ("", "")
        names = "." + row.get("Port name", "") + "." + peer
        kind = ("clock" if re.search(r"(?:^|[._])(?:clk|clock|hclk)|\bclock\b", names + " " + details, re.I)
                else "reset" if re.search(r"(?:^|[._])(?:reset|rst|hreset)", names, re.I)
                else "bus" if re.search(r"\b(?:AHB|APB|AXI|bus)\b", details, re.I) else "signal")
        width = re.search(r"\[[^\]\n]+\]|\b\d+\s*bits?\b", details, re.I)
        evidence = ("source_port_catalog:" + row.get("Owner", "") + ":" + row.get("Port name", "") + ":" + row.get("Source page", ""),)
        check = {"block": owner.name, "node": owner.node, "port": row.get("Port name", ""), "kind": kind,
                 "direction": row.get("Direction", ""), "description": details,
                 "name_status": "present" if row.get("Port name", "").strip() else "missing",
                 "direction_status": "valid" if row.get("Direction", "").casefold() in {"input", "output", "inout", "bidirectional"} else "invalid_or_missing",
                 "description_status": "present" if re.sub(r"\[[^]]*\]|\b\d+\s*bits?\b|\b(?:wire|logic|reg|bits?)\b", "", details, flags=re.I).strip() else "not_established",
                 "width": width[0] if width else "unspecified", "peer_endpoint": peer,
                 "connection_status": "incomplete" if peer.endswith(".") else "unsupported" if problem else "candidate" if peer else "not_established",
                 "source_table": row.get("Table", ""), "source_page": row.get("Source page", ""),
                 "source_file": row.get("Source file", ""),
                 "evidence": list(evidence), "snapshot_id": snapshot_id,
                 "reason": problem or "Literal catalog details do not establish complete semantics or connectivity; an unestablished reference is not proof of source absence"}
        signal_checks.append(check)
        if row.get("snapshot_id") and row["snapshot_id"] != snapshot_id:
            check.update({"connection_status": "stale", "reason": "I/O candidate belongs to a different snapshot"})
            gaps.append({"view": "signal_connection", "status": "conflicting", "reason": "I/O candidate belongs to a different snapshot", "candidate": dict(row)})
            continue
        if not reference:
            block_reference = io_block_reference(details)
            if not block_reference:
                continue
            label, role, reference_kind = block_reference
            local = endpoint(row.get("Port name", ""), row.get("Owner", ""))
            remote = endpoint(label, label)
            if not remote.node:
                remote = RelationEndpoint(label, token=label, status="outside_scope")
            peer_role = "peer" if role == "peer" else "source" if role == "from" else "target" if role in {"to", "for"} or local.direction == "out" else "unspecified"
            check.update({"kind": reference_kind, "peer_block": remote.block, "peer_node": remote.node,
                          "peer_role": peer_role, "reference_level": "block", "peer_port_status": "not_established",
                          "connection_status": "block_only" if remote.node else "outside_scope",
                          "resolution_status": "block_only" if remote.node else "outside_scope",
                          "reason": "Description identifies a block-level peer only; its port and physical wiring are not established"})
            compatible = peer_role == "peer" or (peer_role == "source" and local.direction == "in") or (peer_role == "target" and local.direction == "out")
            if not compatible:
                check.update({"connection_status": "unresolved", "resolution_status": "direction_missing" if peer_role == "unspecified" else "direction_conflict",
                              "reason": "Documented block reference does not establish a compatible directed relationship for this local I/O"})
                continue
            local_block = RelationEndpoint(owner.name, owner.node, token=owner.name)
            source, target = (remote, local_block) if peer_role == "source" else (local_block, remote)
            admit(reference_kind, source, target, evidence,
                  (("local_port", local.address), ("reference_level", "block"), ("peer_label", label),
                   ("directionality", "unspecified" if peer_role == "peer" else "directed"),
                   ("source_details", details), ("source_table", row.get("Table", "")), ("source_page", row.get("Source page", ""))))
            continue
        local = endpoint(row.get("Port name", ""), row.get("Owner", ""))
        qualifiers = (("local_port", local.address), ("peer_endpoint", peer), ("source_details", details),
                      ("source_table", row.get("Table", "")), ("source_page", row.get("Source page", "")))
        if not peer:
            gaps.append({"view": "signal_connection", "kind": kind, "status": "unresolved", "target": asdict(local),
                         "resolution_status": "unsupported_reference",
                         "evidence": list(evidence), "qualifiers": list(qualifiers), "reason": problem, "candidate": dict(row)})
            continue
        remote = endpoint(peer)
        if not problem:
            check["connection_status"] = "resolved" if remote.port and remote.status == "resolved" else "unresolved"
        if local.direction == "in":
            source, target = remote, local
        elif local.direction == "out":
            source, target = local, remote
        else:
            check.update({"resolution_status": "direction_missing", "reason": "Local I/O reference has no unambiguous directed input/output relationship"})
            gaps.append({"view": "signal_connection", "kind": kind, "status": "unresolved", "target": asdict(local), "evidence": list(evidence),
                         "resolution_status": "direction_missing",
                         "reason": "I/O reference lacks an explicit directed peer relationship", "candidate": dict(row)})
            continue
        resolution_status, resolution_reason = endpoint_resolution_issue(source, target, qualifiers)
        check.update({"resolution_status": resolution_status, "reason": resolution_reason})
        admit(kind, source, target, evidence, qualifiers)
        if problem:
            gaps.append({"view": "signal_connection", "kind": kind, "status": "unresolved", "source": asdict(source), "target": asdict(target),
                         "resolution_status": "incomplete_reference" if peer.endswith(".") else "unsupported_reference",
                         "evidence": list(evidence), "qualifiers": list(qualifiers), "reason": problem})
    merged = {}
    for row in records:
        previous = merged.get(row.identity)
        if previous:
            from dataclasses import replace
            row = replace(row, evidence=tuple(dict.fromkeys((*previous.evidence, *row.evidence))))
        merged[row.identity] = row
        if row.status != "resolved":
            resolution_status, resolution_reason = endpoint_resolution_issue(row.source, row.target, row.qualifiers)
            gaps.append({"relation_id": row.identity, "view": row.relation_class, "kind": row.kind, "status": row.status,
                         "resolution_status": resolution_status,
                         "qualifiers": list(row.qualifiers),
                         "source": asdict(row.source), "target": asdict(row.target), "evidence": list(row.evidence), "reason": resolution_reason})
    for gap in gaps:
        gap["owners"] = sorted({contract.expected[identity].get("approved_block", "") for identity in gap.get("evidence", ())
                                if identity in contract.expected and contract.expected[identity].get("approved_block")})
    for row in tuple(merged.values()):
        if row.relation_class != "signal_connection":
            continue
        peers = [other for other in merged.values() if other.relation_class == "signal_connection"
                 and other.target.address == row.target.address and other.source.address != row.source.address
                 and other.qualifiers == row.qualifiers]
        if peers:
            from dataclasses import replace
            merged[row.identity] = replace(row, status="conflicting", reason="Multiple documented drivers without distinct conditions")
            gaps.append({"relation_id": row.identity, "view": "signal_connection", "status": "conflicting",
                         "reason": "Multiple documented drivers without distinct conditions", "evidence": list(row.evidence)})
    for check in signal_checks:
        if check["connection_status"] == "resolved" and not any(row.relation_class == "signal_connection" and row.status == "resolved"
                                                               and set(check["evidence"]) & set(row.evidence) for row in merged.values()):
            check["connection_status"] = "unresolved"
            if check.get("resolution_status") == "resolved":
                check.update({"resolution_status": "connection_conflict",
                              "reason": "Exact endpoints were found, but the candidate did not survive central connection validation"})
    return RelationInventory(snapshot_id, tuple(merged.values()), tuple(gaps), blocks=tuple(block.name for block in scope.blocks), signal_checks=tuple(signal_checks))


def serialized_connections(scope) -> list[dict]:
    """Read actual connectors and identity-bound metadata, never expected edges."""
    pattern = re.compile(r"\bconnection\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*([A-Za-z_][A-Za-z0-9_:]*)\s+connect\s+([A-Za-z_][A-Za-z0-9_.]*)\s+to\s+([A-Za-z_][A-Za-z0-9_.]*)\s*;")
    result = []
    for path in scope.structural_paths():
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        metadata = {}
        for match in re.finditer(r"\bdoc\s+(\w+)\s*/\*\s*governedRelation=(.*?)\s*\*/;", text, re.S):
            try:
                payload = json.loads(match[2])
                metadata[match[1]] = payload if isinstance(payload, dict) and match[1] not in metadata else {}
            except (ValueError, TypeError):
                metadata[match[1]] = {}
        legacy = {match[1]: match[2].strip() for match in re.finditer(r"\bdoc\s+(\w+)\s*/\*(.*?)\*/;", text, re.S)}
        clean = re.sub(r'"(?:\\.|[^"\\])*"|/\*.*?\*/|//[^\n]*', '""', text, flags=re.S)
        for match in pattern.finditer(clean):
            identity, connection_type, source, target = match.groups()
            owners = []
            for endpoint in (source, target):
                matches = [block for block in scope.blocks if endpoint == block.node or endpoint.startswith(block.node + ".")]
                owners.append(matches[0] if len(matches) == 1 else None)
            source_owner, target_owner = owners
            relation_class = "signal_connection" if source_owner and target_owner and source != source_owner.node and target != target_owner.node else "block_relation"
            result.append({"id": path.as_posix() + ":" + identity, "identity": identity, "path": path,
                           "source": source_owner.path if source_owner else None, "target": target_owner.path if target_owner else None,
                           "source_node": source, "target_node": target, "relation_class": relation_class,
                           "connection_type": connection_type, "metadata": metadata.get(identity, {}), "details": legacy.get(identity, "")})
    return result


def validate_serialized_relations(scope, inventory: RelationInventory) -> dict:
    actual = serialized_connections(scope)
    findings, coverage = [], {}
    expected = {row.identity: row for row in inventory.relations if row.relation_class != "containment" and row.status == "resolved"}
    for relation_class in ("block_relation", "signal_connection"):
        obligations = [row for row in expected.values() if row.relation_class == relation_class]
        matched = 0
        for row in obligations:
            copies = [item for item in actual if item["identity"] == row.identity]
            connection_type = "SignalConnection" if relation_class == "signal_connection" else "BlockRelation"
            if len(copies) != 1:
                findings.append("SYSML_RELATION_MISSING_OR_DUPLICATE:" + row.identity)
                continue
            text = copies[0]["path"].read_text(encoding="utf-8")
            if (f"// Snapshot ID: {scope.snapshot_id}" not in text
                    or f"// Downstream contract fingerprint: {scope.fingerprint}" not in text):
                findings.append("SYSML_RELATION_STALE_MODEL:" + row.identity)
                continue
            normalized = json.loads(json.dumps(asdict(row)))
            if (copies[0]["source_node"], copies[0]["target_node"], copies[0]["connection_type"], copies[0]["metadata"]) != (row.source.address, row.target.address, connection_type, normalized):
                findings.append("SYSML_RELATION_CHANGED:" + row.identity)
                continue
            missing_ports = False
            if relation_class == "signal_connection":
                for endpoint in (row.source, row.target):
                    block = scope.block_for_node(endpoint.node)
                    text = block.path.read_text(encoding="utf-8") if block and block.path.is_file() else ""
                    clean = re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
                    declarations = re.findall(r"\b(in|out|inout)\s+port\s+" + re.escape(endpoint.port) + r"\s*:\s*\w+\s*\{", clean)
                    if declarations != [endpoint.direction]:
                        findings.append("SYSML_RELATION_PORT_NOT_MATERIALIZED:" + row.identity + ":" + endpoint.address)
                        missing_ports = True
            if not missing_ports:
                matched += 1
        residual_count = sum(gap.get("view") == relation_class for gap in inventory.gaps)
        coverage[relation_class] = {"expected": len(obligations), "serialized": matched, "gaps": residual_count,
                       "status": "INCOMPLETE" if matched != len(obligations) else "PARTIAL" if residual_count else "REPRESENTED"}
    for row in actual:
        if row["identity"] not in expected:
            findings.append("SYSML_RELATION_UNSUPPORTED:" + row["identity"])
    from validate_downstream_coherence import sysml_materialization_findings
    hierarchy_findings = [item for item in sysml_materialization_findings(scope.repo_root, scope)
                          if "PART" in item or "IMPORT" in item or "STRUCTURAL_MODEL_MISSING" in item]
    actual_containment = set(containment_projection(scope))
    for relation in inventory.view("containment"):
        if (relation.source.node, relation.target.node) not in actual_containment:
            hierarchy_findings.append("SYSML_CONTAINMENT_MISSING:" + relation.source.node + "->" + relation.target.node)
    findings.extend(hierarchy_findings)
    coverage["containment"] = {"expected": len(inventory.view("containment")), "status": "FAIL" if hierarchy_findings else "PASS"}
    block_rows = []
    for block in inventory.blocks:
        local = [row for row in inventory.relations if block in {row.source.block, row.target.block}]
        local_signals = [row for row in inventory.signal_checks if row["block"] == block]
        local_gaps = [gap for gap in inventory.gaps if block in gap.get("owners", ())
                      or any(isinstance(gap.get(field), dict) and gap[field].get("block") == block for field in ("source", "target"))]
        block_rows.append({"block": block, **{relation_class: sum(row.relation_class == relation_class and row.status == "resolved" for row in local) for relation_class in RELATION_CLASSES},
                           "source_signals": len(local_signals),
                           "block_peer_references": sum(row.get("reference_level") == "block" for row in local_signals),
                           "descriptions_not_established": sum(row["description_status"] == "not_established" for row in local_signals),
                           "peer_references_resolved": sum(row["connection_status"] == "resolved" for row in local_signals),
                           "peer_references_not_established": sum(row["connection_status"] == "not_established" for row in local_signals),
                           "gaps": len(local_gaps), "relation_ids": [row.identity for row in local]})
    return {"authority": False, "snapshot_id": inventory.snapshot_id, "inventory_fingerprint": inventory.fingerprint,
            "views": coverage, "blocks": block_rows, "findings": findings, "gaps": list(inventory.gaps)}


def containment_projection(scope) -> tuple[tuple[str, str], ...]:
    parts = set()
    for path in (scope.system_path, scope.digital_path):
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        clean = re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"', "", text, flags=re.S)
        parents = []
        for token in re.finditer(r"\bpart\s+def\s+(\w+)\s*\{|\bpart\s+(?!def\b)(\w+)\s*:\s*(\w+)\s*;|[{}]", clean):
            if token[1]:
                parents.append(token[1])
            elif token[2]:
                parent = next((value for value in reversed(parents) if value), "")
                parts.add((path, parent, token[2], token[3]))
            elif token[0] == "{":
                parents.append(None)
            elif parents:
                parents.pop()
    result = []
    if (scope.system_path, scope.system_definition, "topDigital", "DigitalSubsystem") in parts:
        result.append((scope.system_definition, "topDigital"))
    if ((scope.system_path, scope.system_definition, "topAnalog", "TopAnalogArchitecture") in parts
            and (scope.system_path, "TopAnalogArchitecture", "analogSubsystem", "AnalogSubsystem") in parts):
        result.append((scope.system_definition, "topAnalog.analogSubsystem"))
    for block in scope.blocks:
        parent = "DigitalSubsystem" if block.target == "Digital IPOS" else "AnalogSubsystem"
        path = scope.digital_path if block.target == "Digital IPOS" else scope.system_path
        if (path, parent, block.node.rsplit(".", 1)[-1], block.definition) in parts:
            result.append((block.node.rsplit(".", 1)[0], block.node))
    return tuple(result)


def projection_filter_matches(row, selection):
    return (selection == "all" or row.get("kind") == selection or row.get("status") == selection
            or row.get("resolution_status") == selection or row.get("model_status") == selection
            or (selection == "unresolved" and row.get("gap")
                and row.get("status") not in {"block_only", "missing", "outside_scope"}))


def signal_description_projection(scope, *, selected_node="", kind="all") -> dict:
    inventory = scope.relation_inventory
    checks = inventory.signal_checks if inventory else ()
    model_by_identity = {}
    for row in relation_projection(scope, "signal_connection")["rows"]:
        model_by_identity.setdefault(row["identity"], []).append(row["model_status"])
    evidence_relations = {}
    for relation in inventory.view("signal_connection") if inventory else ():
        if relation.status == "resolved":
            for evidence in relation.evidence:
                evidence_relations.setdefault(evidence, []).append(relation)
    rows = [{**check, "identity": "signal_" + str(index), "source": check["node"] + "." + port_identifier(check["port"]),
         "target": check["peer_endpoint"] or check.get("peer_block", ""), "status": check.get("resolution_status", check["connection_status"]), "evidence": "; ".join(check["evidence"]),
         "gap": check["connection_status"] in {"unresolved", "unsupported", "incomplete", "stale", "outside_scope"}}
        for index, check in enumerate(checks)]
    for row, check in zip(rows, checks):
        relations = {relation.identity: relation for evidence in check["evidence"]
                     for relation in evidence_relations.get(evidence, ())
                     if row["source"] in {relation.source.address, relation.target.address}}
        statuses = {status for identity in relations for status in model_by_identity.get(identity, ())}
        row["resolution_status"] = row["status"]
        row["model_status"] = next((status for status in ("invalid", "historical/unverified", "unverified", "missing", "serialized")
                                    if status in statuses), "not_established")
        row["relation_ids"] = sorted(relations)
    visible = [row for row in rows if (not selected_node or row["node"] == selected_node or row["node"].startswith(selected_node + "."))
               and projection_filter_matches(row, kind)]
    return {"snapshot_id": scope.snapshot_id, "rows": visible, "total": len(rows), "hidden": len(rows) - len(visible),
        "serialized": 0, "gaps": sum(row["gap"] for row in visible)}


def relation_projection(scope, relation_class, *, selected_node="", kind="all") -> dict:
    if relation_class not in {"block_relation", "signal_connection"}:
        raise ValueError("Connector projection requires block or signal class")
    inventory = scope.relation_inventory
    report = validate_serialized_relations(scope, inventory) if inventory else {"findings": [], "gaps": []}
    rows = []
    for connection in serialized_connections(scope):
        if connection["relation_class"] != relation_class:
            continue
        metadata = connection["metadata"]
        findings = [item for item in report["findings"] if connection["identity"] in item]
        match = re.search(r"^// Snapshot ID:\s*(\S+)", connection["path"].read_text(encoding="utf-8"), re.M)
        actual_snapshot = match[1] if match else "unknown"
        rows.append({"identity": connection["identity"], "kind": metadata.get("kind", "unverified"),
                     "source": connection["source_node"], "target": connection["target_node"],
                     "evidence": "; ".join(metadata.get("evidence", ())), "snapshot_id": actual_snapshot,
                     "qualifiers": json.dumps(metadata.get("qualifiers", ())),
                     "status": "historical/unverified" if actual_snapshot != scope.snapshot_id else "invalid" if findings else "serialized" if metadata else "unverified",
                     "reason": "; ".join(findings) or connection["details"], "gap": False})
    expected = inventory.view(relation_class) if inventory else ()
    expected_by_identity = {relation.identity: relation for relation in expected}
    actual_ids = {row["identity"] for row in rows}
    for relation in expected:
        if relation.status == "resolved" and relation.identity not in actual_ids:
            rows.append({"identity": relation.identity, "kind": relation.kind, "source": relation.source.address,
                         "target": relation.target.address, "evidence": "; ".join(relation.evidence), "snapshot_id": scope.snapshot_id,
                         "qualifiers": json.dumps(relation.qualifiers), "status": "missing", "reason": "Documented but not serialized", "gap": True})
    for index, gap in enumerate(report["gaps"]):
        if gap.get("view") != relation_class:
            continue
        def address(value):
            if isinstance(value, dict):
                return value["node"] + ("." + value["port"] if value.get("port") else "") if value.get("node") else value.get("token") or value.get("block", "")
            return str(value or "")
        rows.append({"identity": gap.get("relation_id", "gap_" + str(index)), "kind": gap.get("kind", "unresolved"),
                     "source": address(gap.get("source")), "target": address(gap.get("target")),
                     "evidence": "; ".join(gap.get("evidence", ())), "snapshot_id": scope.snapshot_id,
                     "qualifiers": json.dumps(gap.get("qualifiers", ())),
                     "status": gap.get("resolution_status", gap.get("status", "unresolved")), "reason": gap.get("reason", ""), "gap": True})
    for row in rows:
        expected_relation = expected_by_identity.get(row["identity"])
        row["resolution_status"] = expected_relation.status if expected_relation else "not_established"
        row["model_status"] = row["status"] if row["status"] in {"serialized", "missing", "invalid", "unverified", "historical/unverified"} else "not_established"
        if row["gap"] and row["status"] != "missing":
            row["resolution_status"] = row["status"]
    visible = [row for row in rows if projection_filter_matches(row, kind)
               and (not selected_node or any(value == selected_node or value.startswith(selected_node + ".") for value in (row["source"], row["target"])))]
    return {"snapshot_id": scope.snapshot_id, "rows": visible, "total": len(rows), "hidden": len(rows) - len(visible),
            "serialized": sum(not row["gap"] for row in visible), "gaps": sum(row["gap"] for row in visible)}