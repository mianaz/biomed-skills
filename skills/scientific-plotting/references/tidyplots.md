# tidyplots R route

Use this route for ordinary biomedical plots from tidy tables. The
`scientific-plotting-tidyplots` variation selects it by default. Keep the shared
scientific, color, typography and delivery rules in `SKILL.md` authoritative.

## Environment and API

Use the core R environment in [quickstart.md](quickstart.md), plus `tidyplots`.
The runnable examples were checked with tidyplots 0.4.0. Check the installed
version and function arguments before adapting a recipe. The official site also
shows a development version; a documented function may be absent from a release.

Read the official [function index](https://jbengler.github.io/tidyplots/reference/index.html)
when a function is unfamiliar. These are the useful starting points:

| Need | Functions |
|---|---|
| Observations | `add_data_points()`, `add_data_points_beeswarm()` |
| Distribution | `add_boxplot()`, `add_violin()` |
| Center and spread | `add_mean_dash()`, `add_median_dash()`, `add_sd_errorbar()`, `add_ci95_errorbar()` |
| Trajectory | `add_line(group = unit_id)`, `add_mean_line(group = condition)` |
| Small tidy heatmap | `add_heatmap(scale = "none")` |
| Labels | `add_data_labels()`, `add_data_labels_repel()`, `add_annotation_text()` |
| Style and size | `adjust_font()`, `adjust_theme_details()`, `adjust_colors()`, `adjust_size()` |
| Facets | `split_plot()` |
| Export | `save_plot()` or the shared `export_biomedical()` |

## Type size and full canvas size

Tidyplots [font defaults](https://jbengler.github.io/tidyplots/reference/adjust_font.html)
start at 7 pt. Apply cowplot styling, then explicitly set Arial and the type sizes.
A complete theme applied later can reset prior settings.

- Use `adjust_font(fontsize = 14, family = "Arial")` for theme text. Set axis
  titles separately, usually 16 pt. Check facets and legends too.
- Theme text settings do not resize geometric text. Set `fontsize = 14` in
  `add_annotation_text()`. In ggplot2 text layers use `size = 14, size.unit = "pt"`.
  Default P-value labels to 12 pt. In `add_test_pvalue()` the `label.size`
  argument is in mm: use `label.size = 12 / ggplot2::.pt`. Check other
  label-layer arguments with help.
- Gene symbols require complete italics, including digits; proteins and units
  remain upright. Use the shared [scientific typography](visual-design.md#scientific-typography)
  rules. Start labels with scripts at 16 pt: a first-level script near 0.7 times
  that size can exceed 10 pt. Measure the saved glyphs, including the final assembly.
- In 0.4.0, axis-title helpers can turn a plotmath expression into literal code.
  Keep `title = ggplot2::waiver()` in the axis adjustment so its scale does not
  override the label. Set scientific titles with ggplot2 `labs()` through `add()`
  after the tidyplots axis adjustments, for example:
  `add(ggplot2::labs(y = expression(plain("Ca")^{plain("2+")})))`.
  Verify the displayed glyphs; readable literal code is still a wrong label.
- Set the intended complete figure size before rendering. Tidyplots
  [width and height](https://jbengler.github.io/tidyplots/reference/adjust_size.html)
  refer to the plot area, excluding axes, labels and legends. Default each panel
  to 50 × 50 mm, with `unit = "mm"`, and retain the font sizes above. Apply
  `adjust_size(width = 50, height = 50, unit = "mm")` after the cowplot theme.
  The variation's `scripts/tidyplots.R` measures the outer canvas using Cairo
  font metrics and adds 1 mm around it before running the shared export checks.
  Use the resulting complete width as the intended placement. For an explicitly
  fixed outer canvas, use `width = NA, height = NA` in `tidyplot()` and the final
  `adjust_size()`, then supply the full dimensions to `export_biomedical()`.
- `save_plot()` can infer a larger device size and add padding. Use explicit
  width/height and `view_plot = FALSE` for scripted exports. For a multipage
  result, export each page with an explicit Cairo device and check every page;
  the release's default list-to-PDF path uses the base PDF device.
- Measure effective text size as exported points times placed/exported width.
  Every text element must exceed 10 pt. Keep the agreed canvas and placement
  through repairs; reduce crowding by wrapping labels, local spacing or aligned
  panels. A larger canvas followed by shrinking does not repair type size.

## Observations and a defined summary

`shared` below is the installed `scientific-plotting` folder; `tidyplots_skill` is
the companion variation folder. Resolve them from the package location. The
shared theme supplies Arial and cowplot styling; this route retains those sizes
in a fixed 50 × 50 mm plot area.

```r
library(tidyplots)
source(file.path(shared, "scripts", "compact.R"))
source(file.path(tidyplots_skill, "scripts", "tidyplots.R"))

# df has one row per independent biological unit, with condition and value.
df$condition <- factor(df$condition, levels = c("Control", "Treatment"))
pal <- biomedical_palette(levels(df$condition), control = "Control")
p <- df |>
  tidyplot(x = condition, y = value, color = condition,
           width = 50, height = 50, unit = "mm") |>
  add_sd_errorbar(width = 0.16, linewidth = 0.4) |>
  add_mean_dash(width = 0.3, linewidth = 0.7) |>
  add_data_points_beeswarm(size = 1.8) |>
  adjust_colors(pal) |>
  adjust_x_axis(title = NULL) |>
  adjust_y_axis(title = "Signal (a.u.)") |>
  add(biomedical_theme(14)) |>
  adjust_font(fontsize = 14, family = "Arial") |>
  adjust_theme_details(axis.title = ggplot2::element_text(size = 16),
                       legend.position = "none") |>
  adjust_size(width = 50, height = 50, unit = "mm")

# Export the 50 mm plot area plus labels, with unchanged font sizes.
export_tidyplots(p, "figures/fig1_clean")
write.csv(df, "source_data/fig1_points.csv", row.names = FALSE)
write.csv(data.frame(condition = names(pal), color = unname(pal)),
          "source_data/palette.csv", row.names = FALSE)
```

Adapt the summary to the question. SD describes spread; SEM describes precision
of the mean; a CI has a stated level and method. Save the exact summary and interval
endpoints. For precomputed summaries, use explicit columns with ggplot2 geometry
through `add()`; avoid summarizing the summary again. Show observations for small n.
Use a box/violin only when its distribution summary is useful for the sample size.

## Statistics from the study design

Compute inference before drawing. Keep the full result table and use the shared
[statistics rules](statistics.md). Choose the test, estimand, comparison family and
correction from the design, including pairing and repeated units. A tidyplots
helper's default t-test and unadjusted P values do not identify that analysis.

For categorical comparisons, attach precomputed, keyed results:

```r
# comparisons retains all planned results, including nonsignificant results.
# x1/x2 are category positions; y is the planned annotation height.
comparisons$label <- p_labels(comparisons$p_adj, adjusted = TRUE)
visible <- comparisons[comparisons$label != "", , drop = FALSE]
# y_span is the upper plotted y limit minus the lower plotted y limit.
p <- p + p_brackets(visible, p_col = "p_adj", adjusted = TRUE, size = 12,
                    text_gap = 0.016 * y_span)
```

`text_gap` is in y-axis units. On a linear 50 mm plot area, 0.016 of the full
plotted y span adds 0.8 mm above the bracket.

Assign annotation lanes and extra headroom from visible rows only. Keep numeric P,
contrast keys and positions in the same rows. The shared default hides nonsignificant
labels and brackets; a requested or scientifically necessary negative contrast can
use `ns` or `value` mode with its reason in the caption. Retain all results and
intervals in the full table. An empty label does not imply equivalence.

Use native `add_test_pvalue()` only when it reproduces the intended analysis exactly.
Set the method, planned comparisons, pairing, correction family, visibility and
`label.size` explicitly. Confirm the reported values against the saved analysis.
Use `paired_by` only with true matched unit IDs. Prefer precomputed drawing when
facet-wise package tests would change the intended correction family or model.

## Paired, longitudinal and split plots

For pairs, use `add_line(group = unit_id)` and raw points, with the same unit ID
across conditions. Keep lines behind points. Technical replicates do not create
additional biological pairs.

For trajectories, keep time/dose numeric. A categorical axis gives unequal intervals
equal spacing. Preserve missing rows in source data; partition each unit's line
into contiguous observed segments before drawing. `add_line()` or `add_mean_line()`
can otherwise bridge an omitted interior measurement. Use a repeated-measure model
when inference requires one; separate time-point tests do not test an interaction.

For facets, finish layers, labels, fonts, palette and panel-size settings before
`split_plot()`. Keep scales comparable when the question requires comparison. In
0.4.0 a split can return one plot or a list of pages: inspect the actual result
before exporting. A list is not a single ggplot. Preserve final-size type in every
panel and every page. Use a shared legend or direct facet labels where possible.

Small tidy heatmaps can use `add_heatmap(scale = "none")`; save the exact displayed
matrix, order and any prior scaling. Use a method-native heatmap tool for annotation
blocks or complex matrices. Choose continuous/diverging scales from the scientific
quantity, and keep the color policy across the full figure set.

## Inspection and delivery

Use [figure-delivery.md](figure-delivery.md). `export_tidyplots()` measures the
complete canvas around the fixed panels, then calls the shared `export_biomedical()`
to save PDF/PNG and `.rds` and check rendered fonts, sizes and some boundaries. Open the
saved images at intended placement to check overlap, clipping, scientific glyphs,
paired lines, summary endpoints and every P label. Inspect color-vision and grayscale
views when color encodes groups or values. Check the final assembly too.

Save plotting code, direct geometry tables, full statistics, summaries, palette,
versions and the caption. The variation's `examples/run.R` is a runnable starting
point with synthetic data; its generated delivery includes a portable script and
helpers. Its worked plots demonstrate the route, not scientific validation of a
new dataset.
