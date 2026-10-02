# R and Python execution

Choose one native implementation. Both routes preserve the analysis unit, exact
source tables, statistics, semantic palette and intended placed width. R uses
ggplot2/cowplot; Python uses Matplotlib. Specialized methods retain their validated
engine, transformations and coordinates. For Prism, preserve the native project.

## Shared annotation controls

For a requested cross-language implementation, use identical source data, experimental
units, contrast direction, test/model settings and multiple-testing family. Check n,
effect estimates, interval endpoints and P values within numerical tolerance; then
check semantic color and annotation mappings. A different statistical method is not
a rounding discrepancy. Reordering source rows or reordering displayed groups must
not change results or reassign identities. Visual layouts may differ by backend.

`p_labels()` and `p_brackets()` use the same arguments in both languages:
`nonsignificant="hide"` (default), `"ns"`, or `"value"`, with `alpha=0.05`.
See `statistics.md` for the display policy and complete-family correction rules.
`p_labels()` preserves sequence length/order and R names or Python dictionary keys;
hidden labels are `""`. Missing tests still require an explicit `missing_label`.

```r
statistics$label <- p_labels(statistics$p_holm, adjusted = TRUE,
                             nonsignificant = "hide", alpha = 0.05)
```

```python
statistics["label"] = p_labels(statistics["p_holm"], adjusted=True,
                                nonsignificant="hide", alpha=0.05)
```

Use the same mode and threshold when passing a prelabelled table to `p_brackets()`;
it rejects labels that disagree with the numeric P in their row. Bind plotting
positions by outcome, stratum and comparison keys. Keep every statistics row when
exporting; filter empty labels only from the annotation copy before assigning lanes
or custom axis limits. `p_brackets()` draws neither text nor lines for hidden rows.
Supply `p_col` for threshold-based selection; label-only rows are already explicit
display choices and cannot be classified from numeric P by the helper.
For a named primary comparison that must remain visible, pass that keyed subset to
`p_brackets(..., nonsignificant="value")` and the remaining comparisons with the
default; generate each subset's labels with its matching mode and disclose the choice.

## R

Use ggplot2/cowplot; ggprism and ggbeeswarm are useful when installed.

Check installed help before unfamiliar APIs. For ordinary ggplot figures, source
`scripts/compact.R`: it supplies the cowplot theme, P formatting, explicit bracket
geometry and an export check based on actual PDF text, not theme declarations:

```r
library(ggplot2)
source("<skill-directory>/scripts/compact.R")
# Choose the experimental-unit analysis and calculate statistics first.
# Each annotation row retains comparison keys, numeric p_holm and x1/x2/y positions.
p <- ggplot(plot_data, aes(x, value)) +
  geom_point() +
  biomedical_theme(x_angle = 45) +
  p_brackets(annotation_rows, p_col = "p_holm", adjusted = TRUE,
             tip = 0.02 * diff(range(plot_data$value)),
             text_gap = 0.01 * diff(range(plot_data$value)))
```

The helpers do not decide tests, choose a canvas or guarantee that labels fit.
The export check rejects missing/scale-dropped coordinates, page-crossing text and
text at or below 10 pt (including plotmath subscripts), and effective text at the
planned placed width (90 mm by default for a standalone panel), while preserving the export
for inspection. It also writes `*_text_overlaps.csv` with candidate intersections
between PDF word boxes. Inspect these named pairs in the image: rotated word boxes
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
`*_panel_text.csv` measures direct `geom_text` groups against their actual panel
viewport and rejects internally clipped text. Nested compositions, label grobs,
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

Keep calculations and plotting in a rerunnable script. Save direct data and the
plot object, then export at a content-appropriate size:

```r
dir.create("output", showWarnings = FALSE)
write.csv(plot_data, "output/source_data.csv", row.names = FALSE)
write.csv(statistics, "output/statistics.csv", row.names = FALSE)
saveRDS(p, "output/plot.rds")
# w_mm and h_mm were chosen for this content and its intended placement.
export_biomedical(p, "output/figure", width_mm = w_mm, height_mm = h_mm,
                   placed_width_mm = 90)
```

Execute R, open the saved PDF/PNG and inspect. A nonempty PDF can still be blank or
clipped. Retain the first export before revisions; preserve the code, data and final
RDS. For multiple figures reuse the saved palette, point sizes and summary conventions.
A second implementation is unnecessary unless the user needs another native format.

## Python

Use Matplotlib with pandas/NumPy and SciPy for supported figure-level calculations.
Read the installed function help for statistical defaults; in particular, request
Welch explicitly with `scipy.stats.ttest_ind(..., equal_var=False)`. Preserve pairing
with `ttest_rel` only after joining identifiable units. Save the method, version,
comparison family and full-precision results before formatting annotations.

Import the bundled helper from the assigned skill, not a personal installation:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("<skill-directory>/scripts").resolve()))
import matplotlib.pyplot as plt
from compact import biomedical_theme, biomedical_palette, p_brackets, export_biomedical

pal = biomedical_palette(all_conditions, existing=known_colors, control=control_id)
with biomedical_theme():
    fig, ax = plt.subplots()
    ax.scatter(plot_data["x"], plot_data["value"],
               c=plot_data["condition"].map(pal))
    ax.set(xlabel="Group", ylabel="Response")
    p_brackets(ax, annotation_rows, p_col="p_holm", adjusted=True,
               tip=0.02, text_gap=0.03)
    export_biomedical(fig, "output/figure", width_mm=w_mm, height_mm=h_mm,
                      placed_width_mm=90)
plot_data.to_csv("output/source_data.csv", index=False)
statistics.to_csv("output/statistics.csv", index=False)
```

The annotation table retains `x1`, `x2`, `y` and numeric P values in the same row;
`tip` and `text_gap` are data-axis distances. Store labels/units, group order, canvas,
placement and palette with the rerunnable `.py` source. CSV/JSON plus that script are
the portable editable source; a Matplotlib pickle is optional and version-dependent.
Keep every relevant input row, including missingness and explicit exclusions.

The helper exports PDF/PNG, a figure specification and actual PDF text measurements,
and raises on measurable typography/page-boundary failures while leaving files for
inspection. Collision reports identify candidates, not scientific correctness.
Matplotlib artist checks do not cover every custom collection, raster or nested
composition. Open both delivered formats and inspect marks, uncertainty, clipping
and labels at final size, including those not detectable by the helper.

Use `scripts/dose_response.py` for unweighted continuous dose series; see
`dose-response.md` for model and interval definitions. Install matplotlib, numpy,
pandas, scipy and pymupdf in the project's Python environment if absent. Run with a
noninteractive backend for automated export; a sandboxed benchmark additionally
starts Python with `-I -B` and task-local caches. Record actual package versions.
