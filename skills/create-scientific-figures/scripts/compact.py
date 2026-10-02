"""Matplotlib appearance and saved-PDF checks; statistics remain explicit."""
import csv
import json
from collections.abc import Mapping
from numbers import Real
from pathlib import Path
import warnings

import matplotlib as mpl
from matplotlib.colors import to_rgba
from matplotlib.text import Text
import numpy as np


def biomedical_palette(groups, existing=None, control=None):
    """Return a named mapping; initialize from all groups, then reuse it."""
    groups = list(dict.fromkeys(groups))
    if not groups or any(not isinstance(g, str) or not g for g in groups):
        raise ValueError("Group IDs must be nonempty strings.")
    if existing is not None and not isinstance(existing, Mapping):
        raise ValueError("existing must map group IDs to colors.")
    palette = dict(existing or {})
    if any(not isinstance(g, str) or not g for g in palette):
        raise ValueError("Existing group IDs must be nonempty strings.")
    used = {to_rgba(color) for color in palette.values()}
    if control is not None:
        if control not in groups and control not in palette:
            raise ValueError("control must be a known group ID.")
        palette.setdefault(control, "#666666")
        used.add(to_rgba(palette[control]))
    pool = ["#7F3C8D", "#11A579", "#3969AC", "#F2B701", "#E73F74", "#80BA5A",
            "#E68310", "#008695", "#CF1C90", "#F97B72", "#A5AA99"]
    pool = list(dict.fromkeys(color for color in pool if to_rgba(color) not in used))
    added = sorted(set(groups) - palette.keys())
    if len(added) > len(pool):
        raise ValueError("Supply an explicit larger named palette and additional visual encoding.")
    palette.update(zip(added, pool))
    return palette


def biomedical_theme(size=14):
    """Use as `with biomedical_theme():`; changes remain inside this context."""
    if not np.isfinite(size) or size <= 0:
        raise ValueError("size must be positive and finite.")
    return mpl.rc_context({
        "font.family": "Arial", "font.size": size, "axes.labelsize": size + 1,
        "xtick.labelsize": size, "ytick.labelsize": size, "legend.fontsize": size,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
        "axes.edgecolor": "black", "text.color": "black", "xtick.color": "black",
        "ytick.color": "black", "legend.frameon": False, "axes.facecolor": "white",
        "figure.facecolor": "white", "pdf.fonttype": 42, "ps.fonttype": 42,
        "svg.fonttype": "none",
        "mathtext.fontset": "custom", "mathtext.rm": "Arial",
        "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
        "mathtext.sf": "Arial", "mathtext.tt": "Arial", "mathtext.cal": "Arial",
        "mathtext.bfit": "Arial:italic:bold", "mathtext.default": "rm",
        "mathtext.fallback": None,
    })


def p_labels(p, adjusted=False, missing_label=None, nonsignificant="hide", alpha=0.05):
    """Preserve sequence positions or dictionary keys, including missing tests."""
    if not isinstance(nonsignificant, str) or nonsignificant not in ("hide", "ns", "value"):
        raise ValueError("nonsignificant must be hide, ns or value.")
    if not isinstance(alpha, Real) or isinstance(alpha, (bool, np.bool_)) or not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must be a finite number between 0 and 1.")
    if missing_label is not None and (not isinstance(missing_label, str) or not missing_label):
        raise ValueError("missing_label must be a nonempty string.")
    values = list(p.values()) if isinstance(p, Mapping) else list(p)
    alpha_text = next(text for digits in range(1, 18)
                      if float(text := f"{alpha:.{digits}g}") == alpha)
    bound = min(1e-4, alpha)
    labels = []
    for value in values:
        if value is not None and (not isinstance(value, Real) or isinstance(value, (bool, np.bool_))):
            raise ValueError("P values must be numeric, None or NaN.")
        if value is None or np.isnan(value):
            if missing_label is None:
                raise ValueError("Declare missing_label and explain the unavailable comparison; keep its row.")
            labels.append(missing_label)
        elif not np.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("Known P values must be finite and between 0 and 1.")
        elif value >= alpha and nonsignificant != "value":
            labels.append("" if nonsignificant == "hide" else "ns")
        else:
            if value < bound:
                label = "< " + ("0.0001" if bound == 1e-4 else alpha_text)
            elif value == alpha:
                label = "= " + alpha_text
            else:
                relation = np.sign(value-alpha)
                for digits in range(2, 7):
                    shown = f"{value:.{digits}g}"
                    if np.sign(float(shown)-alpha) == relation:
                        label = "= " + shown
                        break
                else:
                    label = ("< " if relation < 0 else "> " if relation > 0 else "= ") + alpha_text
            labels.append(("P adj. " if adjusted else "P ") + label)
    return dict(zip(p, labels)) if isinstance(p, Mapping) else labels


def p_brackets(ax, rows, tip=0, text_gap=0, size=14, p_col=None,
               adjusted=False, missing_label=None, nonsignificant="hide", alpha=0.05):
    """Add brackets from records (or a DataFrame), joining P and positions per row."""
    rows = rows.to_dict("records") if hasattr(rows, "to_dict") else list(rows)
    labels = p_labels([row[p_col] for row in rows] if p_col is not None else [],
                      adjusted, missing_label, nonsignificant, alpha)
    if p_col is not None:
        for row, computed in zip(rows, labels):
            if row.get("label") is not None and row["label"] != computed:
                raise ValueError("P label disagrees with its numeric comparison row.")
        rows = [dict(row, label=label) for row, label in zip(rows, labels)]
    rows = [row for row in rows if row.get("label") != ""]
    artists = []
    for row in rows:
        label = row.get("label")
        x1, x2, y = (row[key] for key in ("x1", "x2", "y"))
        if not isinstance(label, str) or not label or not np.isfinite([x1, x2, y, tip, text_gap, size]).all() or size <= 0:
            raise ValueError("Brackets need finite numeric geometry, a label and positive size.")
        artists.extend(ax.plot([x1, x1, x2, x2], [y-tip, y, y, y-tip], color="black", linewidth=0.8))
        artists.append(ax.annotate(label, ((x1+x2)/2, y+text_gap), xytext=(0, size*0.25),
                                   textcoords="offset points", ha="center", va="bottom",
                                   family="Arial", fontsize=size, clip_on=True,
                                   annotation_clip=False))
    return artists


def export_biomedical(fig, stem, width_mm, height_mm, placed_width_mm=90):
    """Save PDF/PNG, then audit text. Keep the calling script and direct data."""
    if not np.isfinite([width_mm, height_mm, placed_width_mm]).all() or min(width_mm, height_mm, placed_width_mm) <= 0:
        raise ValueError("Canvas and placement dimensions must be positive and finite.")
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.set_size_inches(width_mm/25.4, height_mm/25.4)
    with mpl.rc_context({"pdf.fonttype": 42, "savefig.bbox": None}):
        fig.savefig(str(stem)+".pdf", facecolor="white")
        fig.savefig(str(stem)+".png", dpi=300, facecolor="white")
    Path(str(stem)+"_figure.json").write_text(json.dumps(dict(
        backend="matplotlib", matplotlib_version=mpl.__version__, width_mm=width_mm,
        height_mm=height_mm, placed_width_mm=placed_width_mm,
        axes=[dict(xlabel=ax.get_xlabel(), ylabel=ax.get_ylabel(), xscale=ax.get_xscale(),
                   yscale=ax.get_yscale(), xlim=list(ax.get_xlim()), ylim=list(ax.get_ylim()))
              for ax in fig.axes]), indent=2)+"\n")
    # NaN line breaks are retained intentionally. Masked scatter points are dropped.
    geometry = []
    for ax in fig.axes:
        for line in ax.lines:
            xy = line.get_xydata()
            if line.get_visible() and (np.isinf(xy).any() or (len(xy) and not np.isfinite(xy).any())):
                geometry.append("nonfinite line coordinates")
        for collection in ax.collections:
            offsets = collection.get_offsets()
            if collection.get_visible() and (np.ma.getmaskarray(offsets).any() or not np.isfinite(offsets).all()):
                geometry.append("missing/dropped collection offsets")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    text_bounds = []
    undrawn = set()
    for ax in fig.axes:
        if not ax.get_visible():
            undrawn.update(id(text) for text in ax.findobj(match=Text))
        for axis in (ax.xaxis, ax.yaxis):
            low, high = sorted(axis.get_view_interval())
            for tick in axis.get_major_ticks()+axis.get_minor_ticks():
                if not axis.get_visible() or not low <= tick.get_loc() <= high:
                    undrawn.update((id(tick.label1), id(tick.label2)))
    for text in fig.findobj(match=Text):
        if id(text) in undrawn or not text.get_visible() or not text.get_text().strip():
            continue
        box = text.get_window_extent(renderer)
        outside = not fig.bbox.contains(box.x0, box.y0) or not fig.bbox.contains(box.x1, box.y1)
        clip = text.get_clip_box() if text.get_clip_on() else None
        clipped = clip is not None and (box.x0 < clip.x0-0.5 or box.x1 > clip.x1+0.5 or box.y0 < clip.y0-0.5 or box.y1 > clip.y1+0.5)
        text_bounds.append(dict(label=text.get_text(), outside_page=outside, clipped=clipped))
    with open(str(stem)+"_panel_text.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["label", "outside_page", "clipped"])
        writer.writeheader(); writer.writerows(text_bounds)
    import pymupdf as fitz
    with fitz.open(str(stem)+".pdf") as pdf:
        page = pdf[0]
        spans = [span for block in page.get_text("dict")["blocks"] if "lines" in block
                 for line in block["lines"] for span in line["spans"] if span["text"].strip()]
        words = page.get_text("words")
        overlaps = []
        # ponytail: quadratic scan suits compact panels; use a spatial index for thousands of words.
        for i, a in enumerate(words):
            for j in range(i+1, len(words)):
                b = words[j]
                if min(a[2], b[2])-max(a[0], b[0]) > 0.5 and min(a[3], b[3])-max(a[1], b[1]) > 1:
                    overlaps.append(dict(first=i, second=j, text=a[4]+" / "+b[4]))
        sizes = np.array([span["size"] for span in spans])
        effective = sizes * placed_width_mm / (page.rect.width*25.4/72)
        pdf_outside = any(not page.rect.contains(fitz.Rect(span["bbox"])) for span in spans)
    with open(str(stem)+"_pdf_text.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["text", "font", "italic", "baseline_y_pt", "native_pt", "placed_pt"])
        writer.writeheader()
        writer.writerows(dict(text=s["text"], font=s["font"], italic=bool(s["flags"] & 2),
                              baseline_y_pt=s["origin"][1], native_pt=float(n), placed_pt=float(p))
                         for s, n, p in zip(spans, sizes, effective))
    with open(str(stem)+"_text_overlaps.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["first", "second", "text"])
        writer.writeheader(); writer.writerows(overlaps)
    if overlaps:
        warnings.warn(f"{len(overlaps)} candidate PDF word overlaps; inspect the saved image.", stacklevel=2)
    if geometry:
        raise ValueError("; ".join(sorted(set(geometry))))
    if not len(sizes):
        raise ValueError("No text recovered from saved PDF; inspect the artifact.")
    if any("arial" not in span["font"].lower() for span in spans):
        raise ValueError("Saved PDF contains a substituted/non-Arial font; inspect *_pdf_text.csv.")
    if min(sizes) <= 10 or min(effective) <= 10:
        raise ValueError(f"Text must exceed 10 pt: saved minimum {min(sizes):.2f}, placed minimum {min(effective):.2f} pt.")
    if pdf_outside or any(row["outside_page"] or row["clipped"] for row in text_bounds):
        raise ValueError("Text crosses a page or rectangular clipping boundary; inspect *_panel_text.csv.")
    return dict(min_font_pt=float(min(sizes)), min_placed_font_pt=float(min(effective)),
                candidate_overlaps=len(overlaps), checked_texts=len(text_bounds),
                scope="PDF text plus Matplotlib text/rectangular clips and line/collection coordinates; inspect custom clip paths, text over data and evidence fidelity visually.")
