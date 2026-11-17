# tidyplots R route

Use this R route within `scientific-plotting` for ordinary biomedical plots from
tidy tables. Keep the shared
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
| Heatmaps | Use the [ComplexHeatmap route](complexheatmap.md) |
| Required data labels | `add_data_labels()`, `add_data_labels_repel()` |
| Style and size | `adjust_font()`, `adjust_theme_details()`, `adjust_colors()`, `adjust_size()` |
| Facets | `split_plot()` |
| Export | `save_plot()` or the shared `export_biomedical()` |

## Type size and full canvas size

Tidyplots [font defaults](https://jbengler.github.io/tidyplots/reference/adjust_font.html)
start at 7 pt. Apply cowplot styling, then explicitly set Arial and the type sizes.
A complete theme applied later can reset prior settings.

- Use `adjust_font(fontsize = 11.5, family = "Arial")` for theme text. Set axis
  titles separately, usually 16 pt. Check facets and legends too.
- Theme text settings do not resize data-label layers. Set their font size
  explicitly. In ggplot2 text layers use `size = 14, size.unit = "pt"`.
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
- Start within a 50 × 50 mm **complete canvas**, including axes and legends.
  Tidyplots `width` and `height` specify the data area. For an ordinary fixed-canvas
  figure, use `width = NA, height = NA` in `tidyplot()` and the final
  `adjust_size()`, retain `theme(aspect.ratio = 1)` (or a taller panel), and give
  complete dimensions to `export_biomedical()`. Wrap labels before a small,
  justified increase. Inspect the saved panel and full page.
  Use `export_tidyplots()` only for intentionally fixed panel dimensions: it
  measures the full canvas plus 1 mm padding per side. Do not call the measured
  export a 50 mm figure just because `adjust_size(width = 50)` was used.
- `save_plot()` can infer a larger device size and add padding. Use explicit
  width/height and `view_plot = FALSE` for scripted exports. For a multipage
  result, export each page with an explicit Cairo device and check every page;
  the release's default list-to-PDF path uses the base PDF device.
- Measure effective text size as exported points times placed/exported width.
  Every text element must exceed 10 pt. Keep the agreed canvas and placement
  through repairs; reduce crowding by wrapping labels, local spacing or aligned
  panels. A larger canvas followed by shrinking does not repair type size.

## Observations and a defined summary

`shared` below is the installed `scientific-plotting` folder. Resolve it from
the package location. The
shared theme supplies Arial and cowplot styling. This example answers a group-mean
question with a meaningful zero; use the selected chart from `visual-design.md` for
other tasks. Start at 50 × 50 mm total, then narrow when the data and labels fit.

```r
library(tidyplots)
source(file.path(shared, "scripts", "compact.R"))
source(file.path(shared, "scripts", "tidyplots.R"))

# df has one row per independent biological unit, with condition and value.
df$condition <- factor(df$condition, levels = c("Control", "Treatment"))
pal <- biomedical_palette(levels(df$condition), control = "Control")
p <- df |>
  tidyplot(x = condition, y = value, color = condition,
           width = NA, height = NA, unit = "mm") |>
  add_mean_bar(alpha = 0.35) |>
  add_sd_errorbar(width = 0.16, linewidth = 0.4) |>
  add_data_points_beeswarm(size = 1.8) |>
  adjust_colors(pal) |>
  adjust_x_axis(title = NULL) |>
  adjust_y_axis(title = "Signal (a.u.)") |>
  add(biomedical_theme(11.5, x_angle = 45)) |>
  adjust_font(fontsize = 11.5, family = "Arial") |>
  adjust_theme_details(axis.title = ggplot2::element_text(size = 12),
                       legend.position = "none") |>
  adjust_size(width = NA, height = NA, unit = "mm")

# Full canvas dimensions; inspect effective text and panel shape after export.
export_biomedical(p, "figures/fig1_clean", 50, 50, placed_width_mm = 50)
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

For categorical comparisons, attach precomputed, keyed results. Prefer native
positioning such as `rstatix::get_y_position()` with
`ggpubr::stat_pvalue_manual()` through `add()`; let group names map endpoints and
use the extension's spacing controls. Keep the supplied statistics unchanged.
Follow the [native-control priority](template-first-layout.md#prefer-native-controls-and-data-driven-layout).
For an ordinary categorical comparison, `ggsignif::geom_signif()` can place a
supplied label from `comparisons` and `annotations` using native headroom controls;
`ggpubr::stat_pvalue_manual()` accepts a keyed result table and calculated positions.
Use `p_labels(..., nonsignificant = "value")` for primary or requested contrasts.
Let the annotation layer draw both bracket and text. Keep all results in the saved
statistics table; secondary label visibility follows `statistics.md`.

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

Use ComplexHeatmap for heatmaps. Save the exact displayed matrix, order and any
prior scaling, and apply the same color policy across the figure set.

## Inspection and delivery

Use [figure-delivery.md](figure-delivery.md). `export_tidyplots()` measures the
complete canvas around the fixed panels, then calls the shared `export_biomedical()`
to save a 600 dpi PNG and compact audit record and check rendered fonts, sizes and
some boundaries. It accepts `formats`, `save_object`, `source_data` and `diagnostics`
under the [shared export contract](figure-delivery.md). Open the
saved images at intended placement to check overlap, clipping, scientific glyphs,
paired lines, summary endpoints and every P label. Check the final assembly too.

Save plotting code, direct geometry tables, full statistics, summaries, palette,
versions and the caption. The bundled `examples/tidyplots.R` is a runnable starting
point with synthetic data; its generated delivery includes a portable script and
helpers. Its worked plots demonstrate the route, not scientific validation of a
new dataset.
