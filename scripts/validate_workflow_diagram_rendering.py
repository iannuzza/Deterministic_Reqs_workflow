#!/usr/bin/env python3
"""Render the workflow graph in Tk and verify node, label, and scroll bounds."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from workflow_gui import (
    WORKFLOW_DIAGRAM_EDGES,
    WORKFLOW_DIAGRAM_NODES,
    SELECTABLE_WORKFLOW_NODE_IDS,
    WorkflowDiagramRenderer,
    WorkflowGUI,
)


SELECTABLE_NODE_IDS = SELECTABLE_WORKFLOW_NODE_IDS


def validate_rendering() -> list[str]:
    errors = []
    root = tk.Tk()
    root.withdraw()
    try:
        parent = ttk.Frame(root)
        parent.pack(fill=tk.BOTH, expand=True)
        renderer = WorkflowDiagramRenderer(
            parent,
            on_node_click=lambda _node_id: None,
            selectable_nodes=SELECTABLE_NODE_IDS,
        )
        root.update_idletasks()
        errors.extend(_check_canvas(renderer.canvas, "full"))
        _check_launch_bindings(renderer.canvas, "full", errors)
        renderer.set_active_stage("1")
        active_rect = renderer.node_items["s1"][0]
        if renderer.canvas.itemcget(active_rect, "fill") != WorkflowDiagramRenderer.COLORS["active"]["fill"]:
            errors.append("Full diagram does not highlight the selected run stage in green.")
        renderer.set_active_stage(None)
        if renderer.canvas.itemcget(active_rect, "fill") != WorkflowDiagramRenderer.COLORS["selectable"]["fill"]:
            errors.append("Full diagram does not restore selectable styling after the run stage clears.")

        compact = WorkflowGUI.__new__(WorkflowGUI)
        compact.diagram_canvas = tk.Canvas(root, background="#ffffff", highlightthickness=0)
        compact.diagram_canvas.pack(fill=tk.BOTH, expand=True)
        compact.compact_workflow_zoom = 1.0
        compact.stage_rects = {}
        compact.stage_labels = {}
        compact.active_stage = None
        compact.hover_stage = None
        compact.stage_failure_reasons = {}
        compact._on_stage_node_click = lambda _stage: None
        compact._on_stage_hover_enter = lambda _event, _stage: None
        compact._on_stage_hover_leave = lambda _stage, _widget: None
        compact._show_s5_context_menu = lambda _event: None
        compact._draw_compact_workflow_graph()
        root.update_idletasks()
        compact._set_active_stage_ui("1")
        compact_active_rect = compact.stage_rects["1"]
        if compact.diagram_canvas.itemcget(compact_active_rect, "fill") != WorkflowDiagramRenderer.COLORS["active"]["fill"]:
            errors.append("Compact diagram does not highlight the selected run stage in green.")
        compact._set_active_stage_ui(None)
        if compact.diagram_canvas.itemcget(compact_active_rect, "fill") != WorkflowDiagramRenderer.COLORS["selectable"]["fill"]:
            errors.append("Compact diagram does not restore selectable styling after the run stage clears.")
        compact.hover_stage = "0"
        compact._refresh_stage_styles()
        compact.hover_stage = None
        compact._refresh_stage_styles()
        errors.extend(_check_canvas(compact.diagram_canvas, "compact"))
        _check_launch_bindings(compact.diagram_canvas, "compact", errors)
    finally:
        root.destroy()
    return errors


def _check_canvas(canvas: tk.Canvas, label: str) -> list[str]:
    errors = []
    node_bounds = {}
    node_labels = {}
    for node in WORKFLOW_DIAGRAM_NODES:
        items = canvas.find_withtag(node["id"])
        rect_id = next((item for item in items if canvas.type(item) == "rectangle"), None)
        text_ids = [item for item in items if canvas.type(item) == "text"]
        label_id = text_ids[0] if text_ids else None
        if rect_id is None or label_id is None:
            errors.append(f"{label} diagram node {node['id']} is missing its rectangle or label.")
            continue
        rect = tuple(canvas.coords(rect_id))
        text = canvas.bbox(label_id)
        node_bounds[node["id"]] = rect
        node_labels[node["id"]] = text
        expected_fill = (
            WorkflowDiagramRenderer.COLORS["selectable"]["fill"]
            if node["id"] in SELECTABLE_NODE_IDS
            else WorkflowDiagramRenderer.COLORS[node["kind"]]["fill"]
        )
        if canvas.itemcget(rect_id, "fill") != expected_fill:
            errors.append(f"{label} diagram node {node['id']} has an incorrect selectable-state color.")
        if not text or (
            text[0] < rect[0] + 2
            or text[1] < rect[1] + 2
            or text[2] > rect[2] - 2
            or text[3] > rect[3] - 2
        ):
            errors.append(
                f"{label} diagram label for {node['id']} extends outside its block: "
                f"label={text}, block={rect}."
            )

    node_ids = list(node_bounds)
    for index, first_id in enumerate(node_ids):
        left1, top1, right1, bottom1 = node_bounds[first_id]
        for second_id in node_ids[index + 1:]:
            left2, top2, right2, bottom2 = node_bounds[second_id]
            if max(left1, left2) < min(right1, right2) and max(top1, top2) < min(bottom1, bottom2):
                errors.append(f"{label} diagram blocks {first_id} and {second_id} overlap.")
            text = node_labels[first_id]
            if text and max(text[0], left2) < min(text[2], right2) and max(text[1], top2) < min(text[3], bottom2):
                errors.append(f"{label} diagram label {first_id} overlaps block {second_id}.")
            text = node_labels[second_id]
            if text and max(text[0], left1) < min(text[2], right1) and max(text[1], top1) < min(text[3], bottom1):
                errors.append(f"{label} diagram label {second_id} overlaps block {first_id}.")

    if label == "full":
        rendered_items = canvas.find_all()
        if sum(canvas.type(item) == "line" for item in rendered_items) != len(WORKFLOW_DIAGRAM_EDGES):
            errors.append("Full diagram edge count does not match the workflow diagram definition.")

    bounds = canvas.bbox("all")
    scrollregion = tuple(float(value) for value in canvas.cget("scrollregion").split())
    if bounds and (
        scrollregion[0] > bounds[0]
        or scrollregion[1] > bounds[1]
        or scrollregion[2] < bounds[2]
        or scrollregion[3] < bounds[3]
    ):
        errors.append(f"{label.capitalize()} diagram scrollregion clips rendered content.")
    return errors


def _check_launch_bindings(canvas: tk.Canvas, label: str, errors: list[str]) -> None:
    for node in WORKFLOW_DIAGRAM_NODES:
        items = canvas.find_withtag(node["id"])
        click_bound = any(
            canvas.tag_bind(tag, "<Button-1>")
            for item in items
            for tag in canvas.gettags(item)
        )
        if node["id"] in SELECTABLE_NODE_IDS and not click_bound:
            errors.append(f"{label} selectable node {node['id']} has no click binding.")
        if node["kind"] == "main" and node["id"] not in SELECTABLE_NODE_IDS and click_bound:
            errors.append(f"{label} automatic node {node['id']} can be launched by click.")


def main() -> int:
    try:
        errors = validate_rendering()
    except tk.TclError as exc:
        print(f"Workflow diagram rendering crosscheck: FAIL ({exc})")
        return 1
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"Workflow diagram rendering crosscheck: FAIL ({len(errors)} issue(s))")
        return 1
    print(
        "Workflow diagram rendering crosscheck: PASS "
        f"({len(WORKFLOW_DIAGRAM_NODES)} nodes, {len(WORKFLOW_DIAGRAM_EDGES)} edges, "
        f"{len(SELECTABLE_NODE_IDS)} selectable nodes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())