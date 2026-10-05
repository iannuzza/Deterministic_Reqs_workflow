"""Deterministic, same-block semantic facets for IPOS structural summaries."""

from __future__ import annotations

import re
import json
import textwrap
from typing import Dict, Iterable, List, Mapping, Sequence

_STOP_WORDS = frozenset({
    "a", "an", "and", "as", "at", "be", "by", "for", "from", "if", "in", "into",
    "is", "of", "on", "or", "the", "then", "to", "when", "with",
})
_ACTIONS = frozenset({
    "acquire", "average", "calculate", "control", "drive", "enable", "enter", "generate",
    "maintain", "process", "raise", "receive", "route", "sample", "select", "sequence",
    "set", "start", "stay", "store", "transfer", "transition", "wait", "write",
})
_ACTION_PURPOSES = {
    "acquire": "acquisition", "average": "data processing", "calculate": "data processing",
    "control": "control sequencing", "drive": "control signaling", "enable": "control signaling",
    "enter": "state progression", "generate": "control signaling", "maintain": "state control",
    "process": "data processing", "raise": "control signaling", "receive": "data acquisition",
    "route": "data routing", "sample": "data acquisition", "select": "configuration",
    "sequence": "control sequencing", "set": "control signaling", "start": "operation start",
    "store": "data storage", "transfer": "data routing", "transition": "state progression",
    "wait": "completion synchronization", "write": "data storage",
}


def _detail_clean(value: str) -> str:
    value = re.sub(r"\[[^]]*\]", "", value)
    value = re.sub(r"\([^()]*\)", "", value)
    value = re.sub(r"\([^()]*$", "", value)
    value = re.sub(r"\b[io]_", "", value)
    value = value.replace("_", " ")
    return re.sub(r"\s+", " ", value).strip(" ,;:.-")


def detail_evidence_facets(statement: str, candidate: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Project complete admitted clauses; preserve rejected fragments as presentation evidence."""
    facets: list[dict[str, str]] = []
    rejected: list[dict[str, str]] = []
    verbs = {
        "acquire": "Acquires", "accumulate": "Accumulates", "average": "Averages",
        "calculate": "Calculates", "configure": "Configures", "control": "Controls",
        "convert": "Converts", "copy": "Copies", "disable": "Disables", "divide": "Divides",
        "elaborate": "Elaborates", "enable": "Enables", "enter": "Enters", "exit": "Exits",
        "filter": "Filters", "generate": "Generates", "maintain": "Maintains",
        "perform": "Performs", "process": "Processes", "raise": "Raises", "receive": "Receives",
        "route": "Routes", "sample": "Samples", "select": "Selects", "sequence": "Sequences",
        "start": "Starts", "stop": "Stops", "store": "Stores", "subtract": "Subtracts",
        "transfer": "Transfers", "wait": "Waits", "write": "Writes",
    }
    clean = re.sub(r"\[(?:Covers:|TO:|Vpriority)[^]]*\]", "", statement, flags=re.I)
    modal = list(re.finditer(r"\bshall\s+(?:be\s+able\s+to\s+)?", clean, re.I))
    for index, match in enumerate(modal):
        end = modal[index + 1].start() if index + 1 < len(modal) else len(clean)
        raw = clean[match.end():end]
        raw = re.split(r"[.;](?:\s|$)", raw, maxsplit=1)[0]
        raw = re.sub(r"^(?:also|always)\s+", "", raw, flags=re.I)
        subject = re.split(r"[,;.]", clean[:match.start()])[-1].strip()
        context_match = re.search(r"\b(When|If|After|Before|While|During)\s+(.+?),", clean[:match.start()], re.I)
        context = _detail_clean(context_match.group(0)) if context_match else ""
        for clause in re.split(r"\s+(?:and\s+then|then|and)\s+(?=(?:" + "|".join(verbs) + r")\b)", raw, flags=re.I):
            clause = _detail_clean(clause)
            negative = clause.casefold().startswith("not ")
            predicate = clause[4:] if negative else clause
            action, _, detail = predicate.partition(" ")
            action = action.casefold()
            if action in {"stay", "remain"}:
                action = "maintain"
                detail = re.sub(r"^in this state\b", "the current state", detail, flags=re.I)
                if not detail:
                    detail = _detail_clean(subject)
            if action == "wait":
                detail = re.sub(r"^that (?:the )?(.+?) ends (?:the )?(.+? phase)\b", r"for \1 \2 completion", detail, flags=re.I)
            phrase = (f"Does not {action}" if negative else verbs.get(action, ""))
            invalid = (
                not phrase or not detail or len(detail.split()) < 2
                or re.search(r"\b(?:and|or|to|from|of|for|with|between|the|a|an|new|has|shall|checking)\s*$", detail, re.I)
                or re.search(r"\b(?:register|bitfield|0x[0-9a-f]+)\b", detail, re.I)
            )
            if invalid:
                rejected.append({"span": clause, "reason": "incomplete or implementation-only clause; not a standalone descriptive behavior"})
                continue
            text = f"{phrase} {detail}"
            if context and not re.search(r"\b(?:register|bitfield|0x[0-9a-f]+)\b", context, re.I):
                text += " " + context[:1].lower() + context[1:]
            facet = {"kind": "responsibility", "text": text.rstrip(" .") + ".", "source_span": clause}
            if not any(item["text"] == facet["text"] for item in facets):
                facets.append(facet)
    if not facets:
        phrase = _detail_clean(candidate)
        if re.match(r"(?:Accepts user (?:selection|configuration) of|Averages|Starts|Stores|Samples|Processes)\s+\S", phrase) and not re.search(r"\b(?:and|or|to|for|with|of|the)\s*$", phrase, re.I):
            facets.append({"kind": "responsibility", "text": phrase + ".", "source_span": candidate})
    return facets, rejected


def compose_detail_groups(rows: Sequence[dict[str, str]]) -> list[str]:
    """Group accepted evidence by literal entity or functional action, never by a name catalogue."""
    groups: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        if row.get("decision") != "accepted_candidate":
            continue
        statement = row["candidate_evidence_statement"]
        entity = extract_structural_function_name(statement)
        facets, rejected = detail_evidence_facets(statement, row["candidate_refinement"])
        row["detail_facets_json"] = json.dumps(facets, sort_keys=True)
        row["detail_omissions_json"] = json.dumps(rejected, sort_keys=True)
        row["description_policy"] = "functional_detail_v1"
        if not facets:
            row["presentation_status"] = "insufficient_evidence"
            continue
        title = entity or re.sub(r"\.$", "", row["candidate_refinement"])
        if not entity:
            subject = re.search(r"\b(?:the )?([A-Za-z][A-Za-z0-9_ ]*? block)\s+shall", statement, re.I)
            title = subject.group(1).strip() if subject else "Configuration and operation"
        groups.setdefault(title, []).append(row)
    rendered: list[str] = []
    for order, (title, members) in enumerate(groups.items(), start=1):
        texts = list(dict.fromkeys(facet["text"] for member in members for facet in json.loads(member["detail_facets_json"])))
        summary = "**" + _detail_clean(title) + ".** " + " ".join(texts)
        summary = "\n  ".join(textwrap.wrap(summary, width=110, break_long_words=False, break_on_hyphens=False))
        contributor_ids = "; ".join(member["candidate_evidence_requirement_id"] for member in members)
        for member in members:
            member.update({"summary_group_id": f"detail-{order:02d}", "rendered_summary": summary,
                           "summary_group_contributor_ids": contributor_ids, "output_order": str(order),
                           "presentation_status": "rendered"})
        rendered.append(summary)
    return rendered


def _tokens(value: object) -> set[str]:
    return {
        token for token in re.findall(r"[a-z0-9]+", str(value or "").casefold())
        if token not in _STOP_WORDS and len(token) > 1
    }


def _entity_key(value: object) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value or "").casefold())


def extract_structural_function_name(statement: str) -> str:
    """Return the literal FSM-like subject from a requirement statement."""
    modal = re.search(r"\b(?:shall|must|required\s+to)\b", statement, re.I)
    subject = statement[:modal.start()] if modal else statement
    matches: list[str] = []
    for match in re.finditer(
        r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)*_(?i:FSM|Phases)\b|"
        r"\b[A-Z][A-Z0-9]*(?:\s+[A-Z][A-Z0-9]*){0,2}\s+(?:FSM|Phases)\b",
        subject,
    ):
        matches.append(re.sub(r"\s+", " ", match.group(0).strip()))
    return matches[-1] if matches else ""


def _clean_phrase(value: str) -> str:
    value = re.sub(r"\[[^]]*\]|\([^)]*\)", "", value)
    value = re.split(r"\b(?:when|if|after|before|until|while|so\s+that)\b", value, maxsplit=1, flags=re.I)[0]
    value = re.sub(r"\b(?:the|a|an)\b", "", value, flags=re.I)
    value = re.sub(r"\s+", " ", value).strip(" ,:;.-")
    return value


def _supported_object(value: str) -> str:
    """Accept only a complete, non-parameter action-object field."""
    value = _clean_phrase(value)
    value = re.sub(r"\bthat\s+", "", value, flags=re.I)
    value = re.sub(r"\bchecking\s*$", "", value, flags=re.I)
    value = re.sub(
        r"\b([A-Za-z][A-Za-z0-9_ ]*?)\s+ends\s+(?:the\s+)?([A-Za-z][A-Za-z0-9_ ]*?\s+phase)\b",
        r"\1 \2 completion", value, flags=re.I,
    )
    timing_match = re.search(r"\b(?:a\s+)?configurable\s+time\s+([A-Za-z][A-Za-z0-9_ ]*?)(?:\s*\(|$)", value, re.I)
    if timing_match:
        value = f"{timing_match.group(1).strip()} timing"
    value = re.sub(r"\s+", " ", value).strip(" ,:;.-")
    if (
        not _tokens(value)
        or re.match(r"^(?:equal\s+to|in\s+this\s+state|for\b)", value, re.I)
        or re.search(r"\b(?:and|or|to|with|of)\s*$", value, re.I)
        or re.search(r"\b(?:shall|register|bitfield|address)\b", value, re.I)
    ):
        return ""
    return re.sub(r"[_-]+", " ", value)


def _action_object(statement: str) -> tuple[str, str]:
    state_match = re.search(
        r"(?:^|,)\s*(?:the\s+)?([^,.;]+?)\s+shall\s+(?:stay|remain|be)\s+(high|low|active|inactive|asserted|deasserted)\b",
        statement, re.I,
    )
    if state_match:
        return "maintain", _supported_object(f"{state_match.group(1)} {state_match.group(2).casefold()}")
    wait_signal = re.search(r"\bshall\s+wait(?:\s+(?:for|that))?\s+(?:the\s+)?(i_[A-Za-z0-9_]+)\b", statement, re.I)
    if wait_signal:
        signal = re.sub(r"^i_", "", wait_signal.group(1), flags=re.I).replace("_", " ")
        return "wait", _supported_object(signal)
    match = re.search(r"\bshall\s+(?:be\s+able\s+to\s+)?(?:be\s+)?([A-Za-z]+)\b([^.;]{0,180})", statement, re.I)
    if match:
        action = match.group(1).casefold()
        action = "maintain" if action == "stay" else action
        if action in _ACTIONS:
            object_text = _supported_object(match.group(2))
            if object_text:
                return action, object_text
    return "", ""


def _condition(statement: str) -> str:
    match = re.search(r"\b(?:when|if|after|before|until|while)\s+(.+?)(?=,|\bshall\b|\.|$)", statement, re.I)
    return _clean_phrase(match.group(1)) if match else ""


def _interaction(statement: str, entity: str) -> str:
    entity_key = _entity_key(entity)
    blocks = []
    for match in re.finditer(r"\b([A-Za-z][A-Za-z0-9_ ]{1,48}?)\s+block\b", statement, re.I):
        candidate = _clean_phrase(match.group(1))
        if candidate and _entity_key(candidate) != entity_key:
            blocks.append(candidate)
    signals = re.findall(r"\b(?:i|o)_[A-Za-z0-9_]+\b", statement)
    values = list(dict.fromkeys(blocks + signals[:2]))
    return ", ".join(values[:2])


def normalize_structural_facets(
    entity: str,
    evidence_rows: Iterable[Mapping[str, str]],
    function: str,
    inputs: str,
    outputs: str,
) -> list[dict[str, object]]:
    """Normalize accepted same-block evidence into lightweight auditable facets."""
    inventory_tokens = _tokens(function) | _tokens(inputs) | _tokens(outputs)
    facets: list[dict[str, object]] = []
    for row in evidence_rows:
        statement = str(row.get("candidate_evidence_statement") or "").strip()
        requirement_id = str(row.get("candidate_evidence_requirement_id") or "").strip()
        if not statement or not requirement_id:
            continue
        action, object_text = _action_object(statement)
        if not action or not object_text:
            continue
        condition = _condition(statement)
        interaction = _interaction(statement, entity)
        evidence_tokens = _tokens(object_text) | _tokens(condition) | _tokens(interaction)
        coverage_terms = sorted(inventory_tokens & evidence_tokens)
        facets.append({
            "entity": entity,
            "action": action,
            "object": object_text,
            "purpose": _ACTION_PURPOSES[action],
            "condition": condition,
            "interaction": interaction,
            "data_path": "",
            "evidence_ids": [requirement_id],
            "evidence_count": 1,
            "coverage_terms": coverage_terms,
            "accepted": True,
            "suppression_reason": "",
        })
    return facets


def render_structural_summary(entity: str, facets: Sequence[Mapping[str, object]]) -> tuple[str, str]:
    """Render a fixed-form, evidence-derived summary or an auditable suppression reason."""
    if not facets:
        return "", "no accepted same-block facet has a supported action-object pair"
    purposes = list(dict.fromkeys(str(facet["purpose"]) for facet in facets))
    objects = list(dict.fromkeys(str(facet["object"]) for facet in facets))
    interactions = list(dict.fromkeys(str(facet["interaction"]) for facet in facets if facet.get("interaction")))
    conditions = list(dict.fromkeys(str(facet["condition"]) for facet in facets if facet.get("condition")))
    purpose_text = " and ".join(purposes[:2])
    object_text = "; ".join(objects[:2])
    detail = interactions[0] if interactions else (conditions[0] if conditions else "the approved local control and data paths")
    return (
        f"**{entity}.** Provides {purpose_text} for {object_text}.\n"
        f"  It coordinates this local behavior through {detail}.",
        "",
    )
