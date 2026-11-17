# R and Python execution

Choose one native implementation. Both routes preserve the analysis unit, exact
source tables, statistics, semantic palette and intended placed width. R uses
tidyplots for ordinary tables or ggplot2/cowplot for custom geometry; Python uses Matplotlib. Specialized methods retain their validated
engine, transformations and coordinates. For Prism, preserve the native project.

## Shared annotation controls

For a requested cross-language implementation, use identical source data, experimental
units, contrast direction, test/model settings and multiple-testing family. Check n,
effect estimates, interval endpoints and P values within numerical tolerance; then
check semantic color and annotation mappings. A different statistical method is not
a rounding discrepancy. Reordering source rows or reordering displayed groups must
not change results or reassign identities. Visual layouts may differ by backend.

Format primary or requested contrasts with
`p_labels(..., nonsignificant = "value")`, including nonsignificant results.
The helper retains its legacy `"hide"` default for existing callers; choose the
visibility explicitly according to `statistics.md`. Retain the full result table.
Use native annotation layers for new figures. `p_brackets()` is retained for an
explicitly requested custom layout or exact replication, not the ordinary route.

## R

For multiple categorical x groups, pass `x_angle = 45` to `biomedical_theme()`;
use `x_angle = 0` for numeric ticks or a single group. Follow the
[legend placement rule](layout-legibility.md#legends): clear space inside the plot
first, then the right side when the key does not fit.

For ordinary tidy tables, use [tidyplots.md](tidyplots.md). For custom geometry,
use ggplot2/cowplot; ggprism and ggbeeswarm are useful when installed.

Apply the [native-control priority](template-first-layout.md#prefer-native-controls-and-data-driven-layout)
to ggplot2 and its extensions. Check installed help before unfamiliar APIs. For ordinary ggplot figures, source
`scripts/compact.R`: it supplies the cowplot theme, P formatting, explicit bracket
geometry and an export check based on a delivered or temporary PDF reference:

For a selected categorical comparison, pass the precomputed result to a native
annotation layer; let the layer place the bracket and label:

```r
# p is the selected chart with group on x and value on y.
statistics$label <- p_labels(statistics$p_holm, nonsignificant = "value")
p <- p + ggsignif::geom_signif(
  comparisons = asplit(as.matrix(statistics[c("group1", "group2")]), 1),
  annotations = statistics$label, margin_top = .08, step_increase = .12,
  textsize = 11.5 / ggplot2::.pt, family = "Arial")
```

The helpers do not decide tests, choose a canvas or guarantee that labels fit.
For a dense-label layout below their ordinary-text gate, use the
[role-specific export and check](figure-verification.md#2-measure-effective-font-size).
The export check rejects missing/scale-dropped coordinates, page-crossing text and
text at or below 10 pt (including plotmath subscripts), and effective text at the
planned placed width. Pass the actual assembly width; otherwise placement defaults
to the requested export width. The compact `*_export.json` records font and panel
measurements. Use `diagnostics=TRUE` to also write `*_text_overlaps.csv` with
candidate intersections between PDF word boxes. Inspect these named pairs in the image: rotated word boxes
can intersect without their letters touching. A zero-row report misses labels
hiding points/curves and crowded ticks merged into one extracted word. Use the reported defect to revise
the figure and always view the saved image. Read
them before using them and inspect the result. Use `missing_label="n.e."` only for
an unavailable test explained in the caption. The helpers cannot validate the
scientific test or a wrong join.
Use one shared adjustment key if repeated `P adj.` crowds the figure.
Each P value is formatted independently, so adding a smaller P does not pad every
other label with trailing zeros. Visible bracket labels have clearance proportional
to their text height; reserve room above those labels and the observations.
The native text check measures direct `geom_text` groups against their actual panel
viewport and rejects internally clipped text; `diagnostics=TRUE` retains the
`*_panel_text.csv` details. Nested compositions, label grobs,
axes/strips and text covering data still require visual inspection.

Create stable factors and a named palette before filtering panels. For categorical
colors use the shared helper; supply a recovered/user mapping through `existing`
when context exists (see `color-policy.md`):

```r
pal <- biomedical_palette(all_conditions, existing = known_colors, control = control_id)
# known_colors is character() without context; control_id is NULL if unspecified.
stopifnot(all(as.character(plot_data$condition) %in% names(pal)))
p <- p + scale_colour_manual(values = pal) + scale_fill_manual(values = pal)
```

Save the complete mapping, and reuse `pal` after reordering or subsetting. Change
display labels with scale `labels`, preserving the underlying keys. For dodged plots, make
numeric group positions explicit when needed so raw points, bars, intervals and
brackets align. Do not pass both `position=` and `width=` to geom_jitter. Use
`inherit.aes = FALSE` for annotation tables with different columns. Call functions
from their namespace when their package is not attached.

Keep calculations and plotting in a rerunnable script. Reuse shared direct inputs;
save objects only when useful/requested under [delivery](figure-delivery.md).
Export at a content-appropriate size:

```r
dir.create("output", showWarnings = FALSE)
# Save this unique input once; reuse this path for subsequent style revisions.
write.csv(plot_data, "output/source_data.csv", row.names = FALSE)
write.csv(statistics, "output/statistics.csv", row.names = FALSE)
# w_mm and h_mm were chosen for this content and its intended placement.
export_biomedical(p, "output/figure", width_mm = w_mm, height_mm = h_mm,
                   placed_width_mm = w_mm, source_data = "output/source_data.csv")
# Optional: formats = c("png", "pdf"), save_object = TRUE, diagnostics = TRUE.
```

Execute R and inspect the requested saved exports at final size. Preserve code,
shared data and approved milestones; a nonempty file can still be blank or clipped. For multiple figures reuse the saved palette, point sizes and summary conventions.
A second implementation is unnecessary unless the user needs another native format.

## Python

Use Matplotlib with pandas/NumPy and SciPy for supported figure-level calculations.
Read the installed function help for statistical defaults; in particular, request
Welch explicitly with `scipy.stats.ttest_ind(..., equal_var=False)`. Preserve pairing
with `ttest_rel` only after joining identifiable units. Save the method, version,
comparison family and full-precision results before formatting annotations.

For categorical P-value brackets, install the optional `statannotations` package
in this environment (`python -m pip install statannotations`). Keep precomputed
labels and their comparison order aligned. Import the bundled helper from the
assigned skill, not a personal installation:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("<skill-directory>/scripts").resolve()))
import matplotlib.pyplot as plt
from compact import biomedical_theme, biomedical_palette, export_biomedical
from statannotations.Annotator import Annotator

pal = biomedical_palette(all_conditions, existing=known_colors, control=control_id)
with biomedical_theme():
    fig, ax = plt.subplots()
    # Draw the chart selected from the scientific question on ax first.
    # This example assumes a categorical x axis with the stated order.
    annotator = Annotator(ax, pairs, data=plot_data, x="group", y="value", order=groups)
    annotator.configure(text_format="simple", loc="inside", fontsize=11.5)
    annotator.set_custom_annotations(statistics["label"].tolist())
    annotator.annotate()
    export_biomedical(fig, "output/figure", width_mm=w_mm, height_mm=h_mm,
                      placed_width_mm=w_mm, source_data="output/source_data.csv")
    # Optional: formats=("png", "pdf"), save_object=True, diagnostics=True.
plot_data.to_csv("output/source_data.csv", index=False)
statistics.to_csv("output/statistics.csv", index=False)
```

Store the keyed comparisons, full precision results, labels/units, group order,
canvas, placement and palette with the rerunnable source. CSV/JSON plus that script
are the portable editable source. Keep missingness and explicit exclusions.

The helper defaults to a 600 dpi PNG and one compact `*_export.json`. It measures
text using a temporary PDF, removes that temporary file, and raises on measurable
font/page-boundary failures. Requested PDFs remain as deliverables. Collision
reports identify candidates; they do not establish scientific correctness.
Matplotlib artist checks do not cover every custom collection, raster or nested
composition. Open every requested format and inspect marks, uncertainty, clipping
and labels at final size, including those not detectable by the helper.

Use `scripts/dose_response.py` for unweighted continuous dose series; see
`dose-response.md` for model and interval definitions. Install matplotlib, numpy,
pandas, scipy and pymupdf in the project's Python environment if absent. Run with a
noninteractive backend for automated export; a sandboxed benchmark additionally
starts Python with `-I -B` and task-local caches. Record actual package versions.
