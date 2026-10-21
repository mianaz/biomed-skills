# PowerPoint assembly and export

## Set dimensions and the style once

Use the [canvas sizing procedure](canvas-sizing.md) to choose each figure's
physical width and height. PowerPoint uses one slide size per deck. Keep the
required main and supplemental decks, with a common working page that fits
their figures. Record a per-slide export rectangle when figure sizes differ;
the working page is not the figure's required output size. Keep the background
white. A single-figure PPTX at the export size is an optional editable derivative.

Set a shared font, letter style, palette, line weights and gutter sizes in the
plan. Start with 3–5 mm outer margins and 2–4 mm gutters, then adjust for actual
labels and related panel groups. These are design starting points, not pass/fail
limits. A 50 × 50 mm plot area is a panel starting point; axes and legends add to
its full extent. Keep the supplied canvas for appearance-only changes.

Use physical dimensions throughout: `inches = mm / 25.4`; `points = mm * 72 / 25.4`.
If an authoring tool uses CSS pixels, convert at its documented scale. Confirm
the saved slide size rather than assuming that numeric units are interchangeable.

## Prepare independent assets

1. Save each plot, image or schematic separately under a stable panel ID, with
   no panel letter. Keep the source PDF/SVG, direct data and editable source.
2. Prefer vector artwork for plots when the installed PowerPoint version renders
   it reliably. A lossless PNG at sufficient placed resolution is a valid import
   alternative; retain the vector source. Check scientific glyphs and transparency.
3. Reuse an existing letter-free asset. If only a labeled composite exists, seek
   its independent originals. Separate/crop panels only when labels and neighboring
   content can be removed without losing evidence, axes, legends or scale bars.
   Otherwise use `needs-source`; do not erase labels by painting over image evidence.
4. Preserve aspect ratio. Trim excess export padding at the source when possible.
   Use calibrated scale bars for images and preserve the original field and
   processing record. Reuse a shared legend as its own object when useful.

An asset may contain facets that form one panel. A multi-panel figure with
several display letters is not an independent panel asset.

## Build the slide objects

Use the installed PowerPoint authoring workflow or a PPTX writer that emits
separate pictures, shapes and text boxes. Give objects useful names such as
`panel:response`, `letter:response`, `placeholder:rescue` and `legend:groups`.
Reference those IDs in the inventory. Grouping for movement is optional and must
remain reversible. Keep each letter as a text box, even when grouped with its panel.

Place data objects first, then placeholders, then letters. Use a consistent
letter anchor near the top-left of each panel and a small dedicated label space.
Use bold lowercase letters unless the supplied convention requires another form.
Keep size and offset constant across both decks. Letter order follows the visual
reading order and the figure legend, while stable panel IDs stay unchanged.

Use native rectangles with no fill or a very light neutral fill for placeholders.
Keep the state, planned readout/comparison and chart type visible. Record the
figure's claim, asset paths and unresolved work in slide notes, not a decorative
title bar. Export slides, not notes pages or handouts.

Save and reopen the PPTX. In the Selection Pane, move a panel and its letter
independently, then undo. Inspect PPTX objects when automating: pictures/charts
must map to individual panels, and letter text must live in distinct text shapes.
A single whole-slide picture fails this check even if the source is high resolution.

## Verify effective size before export

For an imported panel with a known source width:

`effective_font_pt = source_font_pt × placed_panel_width / source_panel_width`

For the final figure placed in a manuscript, multiply again by
`manuscript_figure_width / exported_figure_width`. Native PPT text needs only this second
factor. A 12 pt label in an 80 mm panel placed at 50 mm becomes 7.5 pt. Repair
the source typography or layout; a larger raster export does not repair it.

Measure actual glyphs when the vector PDF permits it. For raster text, use known
source settings plus the scaling calculation and visual inspection. Mark unknown
source font size as unmeasured rather than estimating it from DPI metadata.

For raster assets, `effective_ppi = available_pixels / placed_inches`, using both
axes and the retained pixels after a crop. Record the minimum per panel. Disabling
compression preserves available detail but cannot restore missing source pixels.

## Export the assembled figure

1. Save the final deck and turn off picture compression where the installed
   PowerPoint version supports it. Use its highest-quality PDF export and retain
   the original slide dimensions. Check the exported page size and slide count.
   If per-figure export rectangles are used, crop the rendered page to its recorded
   rectangle without scaling. Retain the full-page PDF and record the crop in mm.
   Include every panel, letter, shared legend and scale bar within that rectangle.
2. Prefer a PDF exported by PowerPoint. If unavailable, render the PPTX through
   an installed compatible office renderer, record that renderer, and compare
   the output for font, SVG, transparency and crop changes. Report native
   PowerPoint verification as pending if it was not performed.
3. Render the actual exported PDF pages to PNG and lossless TIFF. Use 600 dpi by
   default; apply a higher journal requirement for line art or another specified
   value. Use RGB unless a verified production requirement specifies otherwise.
   Color-profile conversion requires a separate managed workflow.
4. Verify pixel dimensions, physical dimensions, resolution metadata, color mode
   and TIFF compression by opening the saved files. Check the smallest raster
   panel as well as the whole figure. High output DPI does not upgrade its detail.

The bundled helper requires Python with PyMuPDF and Pillow. From this skill folder:

```bash
python3 scripts/export_figures.py path/to/main-figures.pdf output/main \
  --prefix Figure_ --dpi 600
python3 scripts/export_figures.py path/to/supplemental-figures.pdf output/supplemental \
  --prefix Figure_S --dpi 600
```

It writes one PDF/PNG/TIFF set per page, `exports.tsv` and `preview.html`.
The default status is `draft`, with `_DRAFT` in filenames. Use `--status ready`
only for inspected figures without unresolved placeholders or delivery defects.
For a mixed deck, retain all-page draft exports and export ready pages separately
with `--pages 1 3`; their original page numbers remain in the filenames. Use
`--start` when the first deck slide represents a figure number other than one.
Keep the plan's page-to-figure mapping authoritative, including Extended Data names.

The helper accepts optional per-page rectangles with `--regions regions.json`.
Use page numbers as keys and `[left, top, width, height]` in millimetres, for
example `{"1": [0, 0, 180, 125], "2": [0, 0, 180, 172]}`. These values come from
the saved figure plan. Cropping retains object scale; later manuscript resizing
requires another effective-font check.

The helper preserves PDF geometry and rasterizes only. It does not validate
scientific claims, detect placeholders, certify source resolution or create a PPTX.
Use a separate output directory for each deck/status to keep its preview coherent.

## Official implementation references

Checked 2026-10-14. Consult these for the relevant installed version:

- [Microsoft: turn off picture compression](https://support.microsoft.com/en-us/office/graphics-visuals/turn-off-picture-compression).
- [Microsoft: high-resolution slide export](https://learn.microsoft.com/en-us/previous-versions/troubleshoot/microsoft-365/microsoft-365-apps/powerpoint/change-export-slide-resolution).
  Its registry route applies to Windows; do not apply it on macOS. The PDF route
  above avoids depending on the default “Save as picture” resolution.
- [PyMuPDF: render pages at a specified DPI](https://pymupdf.readthedocs.io/en/latest/recipes-images.html#how-to-increase-image-resolution).
