# Plot Tuner helpers · editor 03

Open https://apps.bioinfospace.com/plot-tuner/ . Keep `tuner.R` or `tuner.py`
beside your plotting script. The examples contain synthetic data.

R packages: ggplot2, svglite, xml2, jsonlite, rsvg. Python packages: matplotlib,
cairosvg; Cairo must be available. Add scipy for statistics calculated from raw
observations during Python replay. Install Arial for matching text.

At the end of your R script:

```r
source("tuner.R")
plots <- list(Response = p)
stats_data <- list(Response = data.frame(group = d$condition, value = d$response))
plot_tuner_export(plots, "plot-tuner", width = 50, height = 50,
                  source_file = "plot.R", object_name = "plots",
                  stat_data = stats_data, stat_object = "stats_data")
```

For several panels, add independent ggplots to that list. A faceted ggplot stays
one panel. `stat_data` is optional; the app can also read an observations CSV.
Use `group`, `value` and, for paired comparisons, a unique subject `id`.

Python:

```python
from tuner import plot_tuner_export, plot_tuner_render
plot_tuner_export(fig, "plot-tuner", source_file="plot.py", object_name="fig")
```

Several figures: `figures = {"Response": fig1, "Trajectory": fig2}`. Export
`figures` with `object_name="figures"`. Optional `stat_data` uses panel names
mapped to records with `group`, `value`, `id`; `stat_object` names that variable.

Open `plot-tuner/project.json`. Use **单个元素** to move one tick label, point,
line or bar. Use **整组** for a complete axis, data layer or legend. The object
list helps select small items. Drag, use arrow keys, or enter exact positions.
The inspector edits text, font, rotation, color, opacity, point size, bar width
and line thickness. Text alignment uses start, middle or end along the writing
direction; native labels rotate around that fixed alignment point. Add titles,
subtitles, legends, textboxes and shapes from
the top toolbar. Textboxes wrap to their width and can have a border.

Theme presets change the vector display. Palette edits follow the native
categorical colors. Keep axis scales and data transformations in the native
plotting source. New legends can use native labels/colors or supplied entries.

**添加统计** accepts project observations, an observations CSV, or existing
results. Calculated tests: Welch, equal-variance Student, and paired t test.
Choose the experimental unit and pairing from the study design. Each addition
forms one comparison family with none, Holm or BH adjustment. Display stars,
P or adjusted P; drag the label and bracket separately. Download the statistics
table to preserve methods, sample sizes, effect, interval, P and provenance.
Existing results retain their supplied method and adjustment information.

Save the complete project to resume editing. Download `tuner.json` into the
`plot-tuner/` directory, keep the export call, then add:

```r
plot_tuner_render("plot-tuner", "plot-tuner/tuner.json")
```

The same call works in Python. **参数与代码** supplies a complete source block.
Each run rebuilds native SVG, applies saved edits and recomputes linked tests
from the exported observations or saved CSV. Updated CSV observations require
re-import in the app; project observations refresh through `stat_data`.

Outputs: editable `tuned.svg`, vector `tuned.pdf`, 600-dpi `tuned.png`, and
`tuned-statistics.csv` when comparisons exist. R also saves native gtables,
settings and recalculated statistics in `tuned.rds`. PDF conversion can outline
text. Keep original plot objects, direct data, the project and settings.

Use stable panel names. After changing plot/layer structure, export a fresh
project and check element mapping. Older projects open, but re-export with
these helpers to obtain semantic axis and data groups. Inspect final exports
at their placed size. Project files stay in your browser.
