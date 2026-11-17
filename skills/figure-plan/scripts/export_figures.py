#!/usr/bin/env python3
"""Rasterize a PDF exported from a figure deck; never compose panels."""

import argparse
import csv
import html
import json
from pathlib import Path

import fitz
from PIL import Image

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("pdf", type=Path)
parser.add_argument("output", type=Path)
parser.add_argument("--prefix", default="Figure_")
parser.add_argument("--dpi", type=int, default=600)
parser.add_argument("--start", type=int, default=1)
parser.add_argument("--pages", type=int, nargs="+", help="One-based PDF pages")
parser.add_argument("--status", choices=["draft", "ready"], default="draft")
parser.add_argument("--regions", type=Path,
                    help="JSON page -> [left, top, width, height] in mm; crop without scaling")
args = parser.parse_args()
if args.dpi <= 0:
    parser.error("--dpi must be positive")

doc = fitz.open(args.pdf)
if not doc.is_pdf or not len(doc):
    parser.error("Input must be a nonempty PDF exported from the figure deck")
pages = args.pages if args.pages is not None else list(range(1, len(doc) + 1))
if len(set(pages)) != len(pages) or any(p < 1 or p > len(doc) for p in pages):
    parser.error("--pages must contain distinct page numbers within the PDF")
args.output.mkdir(parents=True, exist_ok=True)
regions = json.loads(args.regions.read_text()) if args.regions else {}
rows, cards = [], []

for number in pages:
    page = doc[number - 1]
    label = f"{args.prefix}{args.start + number - 1}"
    stem = label + ("_DRAFT" if args.status == "draft" else "")
    with fitz.open() as single_page:
        single_page.insert_pdf(doc, from_page=number - 1, to_page=number - 1)
        if str(number) in regions:
            left, top, width, height = regions[str(number)]
            crop = fitz.Rect(left, top, left + width, top + height) * (72 / 25.4)
            tolerance = 0.01 * 72 / 25.4
            allowed = page.rect + (-tolerance, -tolerance, tolerance, tolerance)
            if page.rotation or width <= 0 or height <= 0 or not allowed.contains(crop):
                parser.error(f"Page {number}: crop requires an unrotated page and a positive rectangle inside it")
            crop = crop & page.rect
            crop += (page.cropbox.x0, page.cropbox.y0, page.cropbox.x0, page.cropbox.y0)
            single_page[0].set_cropbox(crop)
        single_page.save(args.output / f"{stem}.pdf")
    with fitz.open(args.output / f"{stem}.pdf") as exported:
        rendered_page = exported[0]
        pix = rendered_page.get_pixmap(dpi=args.dpi, colorspace=fitz.csRGB, alpha=False)
        width_mm = rendered_page.rect.width * 25.4 / 72
        height_mm = rendered_page.rect.height * 25.4 / 72
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    img.save(args.output / f"{stem}.png", dpi=(args.dpi, args.dpi))
    img.save(args.output / f"{stem}.tiff", compression="tiff_lzw",
             dpi=(args.dpi, args.dpi))
    rows.append({
        "figure": label, "pdf_page": number, "status": args.status,
        "width_mm": round(width_mm, 3), "height_mm": round(height_mm, 3),
        "width_px": pix.width, "height_px": pix.height, "dpi": args.dpi,
        "color_mode": "RGB", "tiff_compression": "LZW",
        "crop_left_mm": regions.get(str(number), [0, 0])[0],
        "crop_top_mm": regions.get(str(number), [0, 0])[1],
        "pdf": f"{stem}.pdf", "png": f"{stem}.png", "tiff": f"{stem}.tiff",
    })
    safe = html.escape(stem, quote=True)
    cards.append(f'''<section>
<h2>{html.escape(label)} <small>{args.status}</small></h2>
<p>{width_mm:.1f} × {height_mm:.1f} mm · {pix.width} × {pix.height} px · {args.dpi} dpi</p>
<a href="{safe}.png"><img src="{safe}.png" alt="{safe}" loading="lazy"></a>
<p><a href="{safe}.pdf">PDF</a> · <a href="{safe}.png">PNG</a> · <a href="{safe}.tiff">TIFF</a></p>
</section>''')

with (args.output / "exports.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

preview = '''<!doctype html>
<html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Figure export review</title>
<style>
body {font: 16px Arial, sans-serif; margin: 24px auto; padding: 0 20px; max-width: 1100px; color: #222; background: #f5f5f5}
h1 {font-size: 26px} h2 {font-size: 20px} small {font-size: 14px; font-weight: normal}
section {background: white; margin: 24px 0; padding: 20px}
img {display: block; width: 100%; height: auto} p {line-height: 1.5} a {color: #295b8e}
</style><body><h1>Figure export review</h1>
<p>Actual PDF page renders. Fit-to-window previews do not establish physical viewing size.
Use the recorded dimensions for manuscript placement. Status is supplied by the figure plan;
this exporter does not assess evidence, placeholders or source-image quality.</p>
'''
preview += f"<p>Source: {html.escape(args.pdf.name)}</p>" + "\n".join(cards) + "</body></html>"
(args.output / "preview.html").write_text(preview, encoding="utf-8")
doc.close()
print(f"Exported {len(rows)} figure(s): {args.output / 'preview.html'}")
