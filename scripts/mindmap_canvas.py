#!/usr/bin/env python3
"""Turn a mind map outline (JSON) into an Obsidian .canvas file.

Usage: python3 mindmap_canvas.py outline.json "path/to/Map.canvas"

Outline format:
{
  "center": "The problem",
  "left_title": "Causes",          (optional label above the left side)
  "right_title": "Solutions",      (optional label above the right side)
  "left":  [{"text": "Branch", "color": "1", "children": [{"text": "Sub"}]}],
  "right": [...]
}

Branches grow outward from the center; children inherit their branch's
color. Colors are Obsidian's "1"-"6" (red, orange, yellow, green, cyan, purple).
"""
import json
import math
import sys
import uuid

NODE_W = 260
CENTER_W = 340
COL_GAP = 120
ROW_GAP = 30
TITLE_GAP = 60
CHARS_PER_LINE = 30
LINE_H = 26
PAD_H = 34


def text_height(text, width):
    chars = max(1, int(CHARS_PER_LINE * width / NODE_W))
    lines = sum(max(1, math.ceil(len(line) / chars)) for line in text.split("\n"))
    return PAD_H + lines * LINE_H


def new_id():
    return uuid.uuid4().hex[:16]


def subtree_height(node):
    own = text_height(node["text"], NODE_W)
    kids = node.get("children", [])
    if not kids:
        return own
    return max(own, stack_height(kids))


def stack_height(nodes):
    return sum(subtree_height(n) for n in nodes) + ROW_GAP * (len(nodes) - 1)


def column_x(depth, side):
    offset = CENTER_W / 2 + COL_GAP + (depth - 1) * (NODE_W + COL_GAP)
    return offset if side == "right" else -offset - NODE_W


def place_stack(kids, parent_id, depth, center_y, side, color, canvas):
    y = center_y - stack_height(kids) / 2
    for kid in kids:
        h = subtree_height(kid)
        place(kid, parent_id, depth, y + h / 2, side, color, canvas)
        y += h + ROW_GAP


def place(node, parent_id, depth, center_y, side, color, canvas):
    color = node.get("color", color)
    h = text_height(node["text"], NODE_W)
    node_id = new_id()
    card = {
        "id": node_id,
        "type": "text",
        "text": node["text"],
        "x": round(column_x(depth, side)),
        "y": round(center_y - h / 2),
        "width": NODE_W,
        "height": h,
    }
    edge = {
        "id": new_id(),
        "fromNode": parent_id,
        "fromSide": side,
        "toNode": node_id,
        "toSide": "left" if side == "right" else "right",
    }
    if color:
        card["color"] = color
        edge["color"] = color
    canvas["nodes"].append(card)
    canvas["edges"].append(edge)
    place_stack(node.get("children", []), node_id, depth + 1, center_y, side, color, canvas)


def build(outline):
    canvas = {"nodes": [], "edges": []}
    center_h = text_height(outline["center"], CENTER_W) + 20
    center_id = new_id()
    canvas["nodes"].append({
        "id": center_id,
        "type": "text",
        "text": "# " + outline["center"],
        "x": round(-CENTER_W / 2),
        "y": round(-center_h / 2),
        "width": CENTER_W,
        "height": center_h,
        "color": "6",
    })
    for side in ("left", "right"):
        branches = outline.get(side, [])
        if branches:
            place_stack(branches, center_id, 1, 0, side, None, canvas)
        title = outline.get(side + "_title")
        if title:
            top = -max(stack_height(branches) if branches else 0, center_h) / 2
            canvas["nodes"].append({
                "id": new_id(),
                "type": "text",
                "text": "## " + title,
                "x": round(column_x(1, side)),
                "y": round(top - TITLE_GAP - 50),
                "width": NODE_W,
                "height": 60,
            })
    return canvas


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        outline = json.load(f)
    if not outline.get("center"):
        sys.exit("Outline needs a \"center\" with the problem text.")
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(build(outline), f, indent="\t", ensure_ascii=False)
    print("Wrote " + sys.argv[2])


if __name__ == "__main__":
    main()
