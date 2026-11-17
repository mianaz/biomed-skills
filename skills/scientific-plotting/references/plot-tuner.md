# Plot Tuner

Use [Bioinfospace Plot Tuner](https://apps.bioinfospace.com/plot-tuner/) for
interactive ggplot2/tidyplots or matplotlib editing. The shared editor supports
axes, tick labels, text, individual points/lines/bars, layers, legends and panels.
It adds titles, subtitles, textboxes, shapes and statistical comparisons. Serve
`assets/plot-tuner/` locally when needed.

## Prepare and edit

Keep the native plot and its direct source data. Use
`scripts/plot-tuner/tuner.R` or `tuner.py`, or the app's **下载助手** archive.
The helper [README](../scripts/plot-tuner/README.md) gives dependencies, portable
examples and optional `stat_data` export. R panels start at 50 × 50 mm;
matplotlib keeps Figure dimensions. Pass independent ggplots in a named list
for panel layout. A faceted ggplot remains one panel.

1. Open the exported `project.json`. Select a small object from the object list
   or click the canvas. **单个元素** targets one mark or label; **整组** targets
   an axis, layer or legend. Drag or use arrow keys and exact inspector values.
2. Edit font, text, rotation, start/middle/end alignment, color, fill, opacity,
   stroke, point size and bar width. Theme presets affect the vector display. Palette choices include
   Paired, Set2, Dark2, RdBu and custom colors. Add an overlay legend only when the user explicitly requests a custom key; otherwise edit the native guide in the plotting source.
3. When the requested edit includes custom overlays, add textboxes with automatic wrapping and optional borders, titles,
   subtitles, rectangles, ellipses, lines and arrows. Set position, size,
   rotation and stacking order. Use Shift + click for panel alignment.
4. Save the complete project to resume editing. Download `tuner.json` under
   **参数与代码**, insert its replay block after native plot construction and run.

```r
source("tuner.R")
plot_tuner_export(p, "plot-tuner", width = 50, height = 50,
                  source_file = "plot.R", object_name = "p")
plot_tuner_render("plot-tuner", "plot-tuner/tuner.json")
```

```python
from tuner import plot_tuner_export, plot_tuner_render
plot_tuner_export(fig, "plot-tuner", source_file="plot.py", object_name="fig")
plot_tuner_render("plot-tuner", "plot-tuner/tuner.json")
```

When requested, write this concrete replay block into the user's plotting source.
Each run rebuilds the native SVG and replays saved display edits. Keep axis
scales and data transformations in the plotting source. The display presets
do not rewrite the native ggplot theme object.

## Statistics

Supply project observations through `stat_data`, import an observations CSV, or
import existing results. Raw rows use `group`, `value` and optional subject `id`.
Select the experimental unit and test from the study design. Available tests
are Welch, equal-variance Student, and paired t tests; paired tests match unique
IDs. Missing observations and incomplete pairs are counted in the result.

Each addition defines a comparison family with none, Holm or BH adjustment.
The display can show stars, raw P or adjusted P. Move the bracket and its text
separately. Imported results preserve their supplied method, adjustment and
available sample-size/effect/interval fields. Adjusted-only imports offer
adjusted P and stars. The CSV export records the family and source.

Native replay recalculates linked tests with R stats or Python scipy and writes
`tuned-statistics.csv`. Project observations refresh with `stat_data`; saved CSV
rows change when re-imported in the app. Preserve the test choice and family
with the analysis source. Browser calculations use bundled
[jStat](https://github.com/jstat/jstat); reference behavior follows
[R t.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html)
and [p.adjust](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html).

## Delivery and checks

Outputs are editable `tuned.svg`, vector `tuned.pdf` and 600-dpi `tuned.png`.
R also saves native gtables, settings and recalculated statistics in `tuned.rds`.
PDF conversion may outline text. Save the original plot object, direct data,
complete project and `tuner.json` alongside the exports.

Use stable panel names. IDs are scoped to native objects. After structural
plot changes, export again and review mapping. Re-export old projects with the
latest helper to gain semantic groups. Plotmath and raster content keep their
native appearance; text editing requires SVG text. The browser reads local
project files without uploading them.

Check final placed size, clipping, annotation overlap, palette assignments and
statistics after replay. The app reports effective text size and canvas bounds.

Interaction references: [mpltweak](https://github.com/shdbl/mpltweak) and
[Tavotto](https://www.tavotto.com/technology/). This implementation is independent.
