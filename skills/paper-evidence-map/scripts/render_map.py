#!/usr/bin/env python3
"""Render an evidence graph as Obsidian Canvas, local HTML and linked tables."""

import argparse
import csv
import html
import json
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory


COLUMNS = {"premise": 0, "experiment": 0, "result": 1, "subclaim": 2, "inference": 2, "main_claim": 3, "question": 0}
COLORS = {"question": "#f1f5f9", "premise": "#f1f5f9", "experiment": "#dbeafe", "result": "#dcfce7", "subclaim": "#ede9fe", "inference": "#fef3c7", "main_claim": "#ddd6fe"}
RELATIONS = {"tests", "produces", "supports", "contradicts", "qualifies", "depends_on", "part_of", "addresses"}
SYMBOLS = {"tests": "T", "produces": "P", "supports": "S", "contradicts": "C", "qualifies": "Q", "depends_on": "D", "part_of": "O", "addresses": "A"}
EVIDENCE = {"supports", "contradicts", "qualifies"}
CLAIMS = {"main_claim", "subclaim", "inference"}
FIELDS = ["claim_id", "claim", "experiment_id", "experiment_and_controls", "result_id", "observed_result", "relation", "source", "reason"]


def render(graph, output):
    nodes, edges = graph["nodes"], graph["edges"]
    if not nodes:
        raise ValueError("The graph needs at least one node.")
    index = {n["id"]: n for n in nodes}
    if len(index) != len(nodes) or any(not isinstance(n["id"], str) or not n["id"].strip() for n in nodes):
        raise ValueError("Node IDs must be nonblank unique strings.")
    for node in nodes:
        if node["type"] not in COLUMNS or not node["text"].strip() or not node["source"].strip():
            raise ValueError(f"Invalid type or missing text/source: {node['id']}")
        if any(k in node and (not isinstance(node[k], int) or isinstance(node[k], bool)) for k in ("x", "y")):
            raise ValueError(f"Canvas coordinates must be integers: {node['id']}")
    for edge in edges:
        if edge["from"] not in index or edge["to"] not in index or edge["from"] == edge["to"]:
            raise ValueError(f"Invalid edge endpoints: {edge}")
        if edge["relation"] not in RELATIONS or not edge["reason"].strip():
            raise ValueError(f"Invalid relation or missing reason: {edge}")
        if edge["relation"] == "produces" and (index[edge["from"]]["type"], index[edge["to"]]["type"]) != ("experiment", "result"):
            raise ValueError("A produces edge must point from experiment to result.")
    output = Path(output)
    filenames = ("evidence-map.canvas", "evidence-map.html", "evidence-table.md", "evidence-table.tsv")
    if any((output / name).exists() for name in filenames):
        raise FileExistsError("Existing deliverables preserved. Reconcile edits and use a new render directory.")
    output.mkdir(parents=True, exist_ok=True)
    counts, canvas_nodes = Counter(), []
    top = sum(n["type"] == "question" for n in nodes) * 160 + 30
    for node in nodes:
        column = COLUMNS[node["type"]]
        question = node["type"] == "question"
        row = counts["question" if question else column]
        counts["question" if question else column] += 1
        x = node.get("x", 30 + column * 400)
        y = node.get("y", row * 160 if question else top + row * 310)
        text = f"## {node['id']} · {node['type'].replace('_', ' ')}\n\n{node['text']}\n\n{node.get('details', '')}\n\nSource: {node['source']}"
        canvas_nodes.append({"id": node["id"], "type": "text", "x": x, "y": y, "width": 1500 if question else 300, "height": 130 if question else 220, "color": COLORS[node["type"]], "text": text})
    positions = {n["id"]: n for n in canvas_nodes}
    canvas_edges, paths, labels = [], [], []
    for i, edge in enumerate(edges):
        a, b = positions[edge["from"]], positions[edge["to"]]
        color = "#b91c1c" if edge["relation"] == "contradicts" else "#a16207" if edge["relation"] == "qualifies" else "#475569"
        adjacent = abs(b["x"] - a["x"]) == 400
        if edge["relation"] == "addresses" and b["id"] in index and index[b["id"]]["type"] == "question":
            sx, sy, tx, ty = a["x"] + a["width"] / 2, a["y"], b["x"] + b["width"] / 2, b["y"] + b["height"]
            lane = ty + 25
            path = f"M {sx} {sy} L {sx} {lane} L {tx} {lane} L {tx} {ty}"
            label_x, label_y = (sx + tx) / 2, lane - 6
            from_side, to_side = "top", "bottom"
        elif a["x"] == b["x"]:
            sx, sy, tx, ty = a["x"] + a["width"], a["y"] + a["height"] / 2, b["x"] + b["width"], b["y"] + b["height"] / 2
            lane = sx + 35
            path = f"M {sx} {sy} L {lane} {sy} L {lane} {ty} L {tx} {ty}"
            label_x, label_y = lane + 16, (sy + ty) / 2
            from_side = to_side = "right"
        elif adjacent:
            forward = b["x"] > a["x"]
            sx, sy = a["x"] + (a["width"] if forward else 0), a["y"] + a["height"] / 2
            tx, ty = b["x"] + (0 if forward else b["width"]), b["y"] + b["height"] / 2
            lane = (sx + tx) / 2
            path = f"M {sx} {sy} L {lane} {sy} L {lane} {ty} L {tx} {ty}"
            label_x, label_y = lane, sy - 16 if sy == ty else (sy + ty) / 2
            from_side, to_side = ("right", "left") if forward else ("left", "right")
        elif a["y"] == b["y"]:
            sx, sy, tx, ty = a["x"] + a["width"] / 2, a["y"] + a["height"], b["x"] + b["width"] / 2, b["y"] + b["height"]
            lane = max(sy, ty) + 30 + (i % 3) * 22
            path = f"M {sx} {sy} L {sx} {lane} L {tx} {lane} L {tx} {ty}"
            label_x, label_y = (sx + tx) / 2, lane - 6
            from_side = to_side = "bottom"
        else:
            # ponytail: fixed-column gutters; use Canvas layout for dense cross-links.
            forward = b["x"] > a["x"]
            sx, sy = a["x"] + (a["width"] if forward else 0), a["y"] + a["height"] / 2
            tx, ty = b["x"] + (0 if forward else b["width"]), b["y"] + b["height"] / 2
            gx, hx = sx + (35 if forward else -35), tx + (-35 if forward else 35)
            lane = max(n["y"] + n["height"] for n in canvas_nodes) + 30 + (i % 3) * 22
            path = f"M {sx} {sy} L {gx} {sy} L {gx} {lane} L {hx} {lane} L {hx} {ty} L {tx} {ty}"
            label_x, label_y = (gx + hx) / 2, lane - 6
            from_side, to_side = ("right", "left") if forward else ("left", "right")
        canvas_edges.append({"id": f"edge-{i + 1}", "fromNode": edge["from"], "toNode": edge["to"], "fromSide": from_side, "toSide": to_side, "toEnd": "arrow", "color": color, "label": edge["relation"]})
        paths.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2" marker-end="url(#arrow)"><title>{html.escape(edge["reason"])}</title></path>')
        rotation = f' transform="rotate(90 {label_x} {label_y})"' if a["x"] == b["x"] or adjacent and sy != ty else ""
        labels.append(f'<text x="{label_x}" y="{label_y}"{rotation} text-anchor="middle" fill="{color}"><title>{html.escape(edge["relation"] + ": " + edge["reason"])}</title>{SYMBOLS[edge["relation"]]}</text>')
    (output / filenames[0]).write_text(json.dumps({"nodes": canvas_nodes, "edges": canvas_edges}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = []
    for edge in edges:
        result, claim = index[edge["from"]], index[edge["to"]]
        if result["type"] != "result" or claim["type"] not in CLAIMS or edge["relation"] not in EVIDENCE:
            continue
        experiments = [index[e["from"]] for e in edges if e["relation"] == "produces" and e["to"] == result["id"]] or [None]
        for experiment in experiments:
            references = dict.fromkeys(n["source"] for n in (experiment, result, claim) if n)
            if edge.get("source"):
                references[edge["source"]] = None
            rows.append([claim["id"], claim["text"], experiment["id"] if experiment else "Not available", (experiment["text"] + ": " + experiment.get("details", "")) if experiment else "Producing experiment not available", result["id"], result["text"] + ": " + result.get("details", ""), edge["relation"], "; ".join(references), edge["reason"]])
    with (output / filenames[3]).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t")
        writer.writerow(FIELDS)
        writer.writerows(rows)
    def cell(value):
        return html.escape(str(value)).replace("|", "\\|").replace("\n", "<br>")
    paper = graph["paper"]
    md = [f"# {graph['title']}", paper["citation"], f"Source: {paper['source']}", f"Read scope: {paper['read_scope']}", "## Evidence table", "| " + " | ".join(FIELDS) + " |", "| " + " | ".join(["---"] * len(FIELDS)) + " |"]
    md.extend("| " + " | ".join(f"[{cell(v)}](#{row[0].lower()})" if i == 0 else f"[{cell(v)}](#{row[2].lower()})" if i == 2 and row[2] in index else f"[{cell(v)}](#{row[4].lower()})" if i == 4 else cell(v) for i, v in enumerate(row)) + " |" for row in rows)
    md.append("\n## Nodes\n")
    for node in nodes:
        md.extend([f"### {node['id']}\n", f"**{node['type'].replace('_', ' ')}:** {node['text']}\n", node.get("details", "") + "\n", f"Source: {node['source']}\n"])
    md.extend(["\n## Relations\n", "| From | Relation | To | Reason | Source |", "|---|---|---|---|---|"])
    md.extend(f"| [{cell(e['from'])}](#{e['from'].lower()}) | {cell(e['relation'])} | [{cell(e['to'])}](#{e['to'].lower()}) | {cell(e['reason'])} | {cell(e.get('source', 'Endpoint references'))} |" for e in edges)
    (output / filenames[2]).write_text("\n\n".join(md[:5]) + "\n\n" + "\n".join(md[5:]) + "\n", encoding="utf-8")
    min_x, min_y = min(n["x"] for n in canvas_nodes) - 20, min(n["y"] for n in canvas_nodes) - 20
    width = max(n["x"] + n["width"] for n in canvas_nodes) - min_x + 20
    height = max(n["y"] + n["height"] for n in canvas_nodes) - min_y + 115
    cards = []
    for node in nodes:
        p = positions[node["id"]]
        tooltip = html.escape(node.get("details", "") + "\nSource: " + node["source"], quote=True)
        cards.append(f'<div class="card" title="{tooltip}" style="left:{p["x"]}px;top:{p["y"]}px;width:{p["width"]}px;height:{p["height"]}px;background:{p["color"]}"><b>{html.escape(node["id"])} · {html.escape(node["type"].replace("_", " "))}</b><p>{html.escape(node["text"])}</p></div>')
    preview = f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>{html.escape(graph["title"])}</title>
<style>body{{font:24px Arial,sans-serif;color:#172033;margin:24px}}h1{{font-size:30px}}.board{{position:relative;width:{width}px;height:{height}px}}.content{{position:absolute;left:{-min_x}px;top:{-min_y}px}}.card{{position:absolute;box-sizing:border-box;border:1px solid #94a3b8;border-radius:12px;padding:16px;overflow:auto}}.card b{{font-size:24px}}.card p{{margin:12px 0 0;line-height:1.25}}svg text{{font:24px Arial,sans-serif;paint-order:stroke;stroke:white;stroke-width:5px;stroke-linejoin:round}}</style>
<h1>{html.escape(graph["title"])}</h1><p>{html.escape(paper["citation"])}</p><p><a href="evidence-table.md">Evidence table</a> · <a href="evidence-map.canvas">Editable Canvas</a> · Hover for details and sources.</p>
<p>T tests · P produces · S supports · C contradicts · Q qualifies · D depends on · O part of · A addresses</p>
<div class="board"><div class="content"><svg width="{width + min_x}" height="{height + min_y}" style="position:absolute;overflow:visible"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/></marker></defs>{"".join(paths)}{"".join(labels)}</svg>{"".join(cards)}</div></div></html>'''
    (output / filenames[1]).write_text(preview, encoding="utf-8")
    return rows


def self_test():
    graph = json.loads((Path(__file__).resolve().parents[1] / "assets/example.json").read_text(encoding="utf-8"))
    with TemporaryDirectory() as temporary:
        output = Path(temporary)
        rows = render(graph, output)
        assert {(r[0], r[2], r[4]) for r in rows} == {("C1", "E1", "R1"), ("C1", "E2", "R2"), ("C2", "E2", "R2"), ("I1", "E3", "R3")}
        canvas = json.loads((output / "evidence-map.canvas").read_text(encoding="utf-8"))
        assert len(canvas["nodes"]) == len(graph["nodes"]) and len(canvas["edges"]) == len(graph["edges"])
        assert next(n for n in canvas["nodes"] if n["id"] == "C0")["y"] == 500
        try:
            render(graph, output)
        except FileExistsError:
            pass
        else:
            raise AssertionError("Existing edits must be preserved.")
        broken = json.loads(json.dumps(graph))
        broken["edges"][0]["to"] = "missing"
        try:
            render(broken, output / "broken")
        except ValueError:
            pass
        else:
            raise AssertionError("Dangling edges must be rejected.")
    print("PASS: shared evidence, Canvas links, positions, invalid endpoints and overwrite protection")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", nargs="?", type=Path)
    parser.add_argument("output", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        if args.graph is None or args.output is None:
            parser.error("Provide graph.json and an output directory, or --self-test.")
        render(json.loads(args.graph.read_text(encoding="utf-8")), args.output)
        print(f"Created evidence map and table in {args.output}")
