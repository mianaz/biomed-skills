# Verify the saved scientific figure

Use this review before delivering a new figure, after a repair, and when auditing
an existing figure. Work on the requested saved exports, then on the assembled
figure when assembly is in scope. Use the current user, project and journal
requirements; otherwise apply [shared visual standards](../../biomed-shared/visual-standards.md).
Read the current official journal guide for a submission-specific check.

## 1. Check the scientific comparison and necessary statistics

Read [statistics.md](statistics.md) when inference is present or needed. Check the
plot, caption and complete analysis table together.

| Figure purpose | Required check |
|---|---|
| Descriptive pattern, distribution or trajectory | State the biological unit, independent n, displayed summary and spread/interval definition. Show observations when a summary would hide the small sample. |
| Inferential group or paired comparison | Verify the test/model against the independent unit, matching, hierarchy and contrast. Report the effect and uncertainty where estimable, the test/sidedness and the relevant P value. |
| Several contrasts or molecular features | Name the complete comparison family and correction, where needed. Match labels to raw or adjusted P values and retain all results, including unshown comparisons. |
| Factorial or repeated experiment | Match the claim to the model term: interaction, trajectory or a named within-stratum contrast. Preserve unit IDs and actual time spacing. |
| Supplied effects, survival, prediction or fitted curves | Check estimate/interval endpoints, model and evaluation context, censoring or tested range as applicable. Use the valid upstream result. |

For every relevant panel:

- Reconcile n with the independent observations and exclusions. Distinguish
  biological replicates from repeated technical measurements.
- Define SD, SEM, CI or another interval, including its level and calculation.
  Check the actual endpoints and match the summary to the legend.
- Match each visible statistical label/bracket to its keyed result and comparison
  direction. Use full precision for thresholds; check P versus adjusted P, the
  correction family and annotation visibility rule.
- Make the main comparison easy to read. Facet or overlay factors according to
  that comparison; inspect the within-facet contrasts and cross-facet scales.
- When a statistical result is needed but absent, compute it only from suitable
  inputs within the task's analysis scope. Preserve valid results during appearance
  repairs and identify the specific missing analysis or metadata in an audit.

A descriptive figure needs clear summary and sample information. Add inferential
statistics when the scientific question calls for them. Keep missing results
explicit; they cannot supply an error bar, `ns` label or inferential claim.

## 2. Measure effective font size

Measure text in a delivered or temporary reference PDF with a reader that resolves
composed text and page transformations. For PNG-only exports, retain the native
measurement summary in `*_export.json` and remove the temporary PDF. This checks
native font metrics; inspect the actual PNG for glyphs and final raster layout. `verify_figure.py` uses PyMuPDF. An exported PDF text span or
`pdftools::pdf_data(font_info=TRUE)$font_size` provides a size; a word-box height or
the raw PDF `Tf` operand alone does not.

For proportional placement:

`effective_pt = measured_export_pt × placed_width_mm / exported_width_mm`

For a panel placed in a figure and then scaled in a manuscript, include both scale
factors. Measuring the final assembled PDF already includes the panel-placement
factor; apply only the remaining manuscript scale. Preserve the aspect ratio.

Check Arial family and embedding, rotation, italic gene symbols, statistical
labels, legends, subscripts and superscripts. Target **>10 pt at final placement**.
Record dense labels below the ordinary target by role/panel, with **8 pt**
as the absolute floor. Increasing DPI changes pixel sampling, not physical text
size. Resolve small text through font and layout edits, then inspect again.

The bundled export helpers and default checker enforce an all-text >10 pt gate.
For a permitted dense-label layout at 8–10 pt, export through the native device
and resolve the size flags by checking those roles separately; ordinary text keeps
its >10 pt target. Record the actual minimum and role in the same report. Keep
the real placement width fixed when measuring either route.

Raster, outlined and Type 3 glyphs require visual/native-source review because PDF text
extraction cannot measure them. A PDF with no extractable text stays unchecked.
The checker also flags embedded rasters so their labels receive separate review.

Use bold only for panel letters by default. Letter-free manuscript panels use
`--bold none`; inspect any surviving letter at every composition level. Follow an
explicit project emphasis rule when it differs.

## 3. Verify formats, dimensions and effective resolution

Deliver the formats and editable source in
[figure-delivery.md](figure-delivery.md): a 600 dpi PNG by default, with PDF, TIFF
or SVG only when requested/required. Check the rerunnable source and shared inputs,
or the native project when one is retained, against the delivered figure.
A native project or data-only PZFX does not substitute for a verified figure export.

For each saved format check its decoded type, page/frame count, dimensions, crop,
colors, transparency and content. Inspect fonts in vector files and preserve vector
axes/text when dense data layers need rasterization. Vector geometry has no DPI;
embedded images retain their own pixel-resolution requirements.

Compute resolution from pixels and final placed dimensions:

`effective_dpi_x = pixel_width × 25.4 / placed_width_mm`

`effective_dpi_y = pixel_height × 25.4 / placed_height_mm`

Use the smaller value. For PDF raster layers, use the layer's placed box, including
figure scaling. The saved DPI tag is useful metadata; pixels and placement determine
effective resolution. Keep aspect ratio and pixel dimensions across conversions.

The package default for raster plots with labels/lines is **600 dpi**. Pure
continuous-tone images can use **300 dpi**; use the current venue's higher or
format-specific requirement when applicable. Re-export from the vector/native
source to increase sampling. Retain source pixel limits for measured image data;
upsampling does not recover detail. Inspect TIFF compression and avoid JPEG
recompression of quantitative figures.

## 4. Inspect every final render

Open each requested saved export at intended viewing size. Inspect the longest
label at every edge, rotated axis titles, legend keys next to long entries,
statistical brackets above data, and panel letters beside axis titles. Inspect
the `panels` field of `*_export.json` for actual data-panel dimensions
(`diagnostics=TRUE` also writes `*_panel_layout.csv`); review a height/width ratio
below 0.8 against the reading task and preserve height when making a compact panel.
Rows marked `assembly_layout` describe the enclosing composition; inspect its
individual data panels separately rather than treating that ratio as their shape.
Confirm that keys and annotations come from native plotting functions unless a
custom layout was explicitly requested. Check gaps,
missing values, group colors, scales, units, scale bars and interval endpoints.
For aggregated dense data, compare the saved bins and summary with the original
values and check that task-relevant extremes remain visible at this size. For
matrices, check semantic order, displayed transformation, biological key title and
normalization denominator. Check the measured `heatmap_cells` against the shared
8 mm final-placement minimum, including any later assembly scale.

Apply [reader read-back](../../biomed-shared/reader-feedback.md) to the saved
figure and caption during this review, then reconcile the visible message with
the intended scientific comparison and source results.

Inspect individual panels and their actual assembled placement. A PDF containing
selectable Arial text can still have clipped labels or overlapping content. Fix
specific defects, rerender the affected files and repeat the affected checks.

## Run the artifact checker

Use a Python environment with PyMuPDF and Pillow (listed in `scripts/requirements.txt`).
From the skill folder, check one figure and its companion formats per call:

```sh
python3 scripts/verify_figure.py panel.png \
  --placed-width-mm 76 --bold none --min-dpi 600 \
  --output panel-verification.json
```

The checker uses a matching `panel_export.json` for PNG-only native text metrics;
pass `--text-report` for a differently named record. Without native metrics,
raster font measurement remains review-needed. It still requires visual inspection.
Add `--placed-height-mm` when an actual placement box is known; the checker flags
stretching. Use `--require pdf tiff` for a PDF/TIFF delivery. Set `--image-min-dpi 600`
when PDF raster layers contain plot lines or labels. Other formats receive a native
inspection flag. Exact source-to-export equality and scientific statistics need
the review above.

The JSON records effective text sizes, fonts, decoded formats, pixel dimensions,
effective DPI (with 1-dpi tolerance for pixel rounding), unresolved measurements
and separate pending manual checks. Exit
0 means the measured checks passed, 1 means a failure, and 2 means measurement
coverage needs review. All three retain the scientific and visual review steps.
Record the final result in the figure notes: files and placed dimensions, analysis
checked or descriptive scope, font minimum, export formats/resolution, renders
inspected and any remaining issue. Call the figure complete only when required
checks and any stated exceptions are resolved.
