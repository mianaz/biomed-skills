# Synthetic visual gallery

Six runnable examples show how the study design changes the plot and analysis.
All data are synthetic. Choose a relevant example; these are not required panels
or biological results. The six single-case previews target 90 mm placement with Arial text.

| Case | When and why | Preview | Source |
|---|---|---|---|
| Independent groups | Small independent samples: show every unit, with mean ± SD beside the points. Compare A and B separately with Control using Welch tests and Holm correction; retain both results while annotating only adjusted P < 0.05. | [PNG](../examples/gallery/independent.png) | [R](../examples/gallery.R) |
| Paired observations | Before/after measurements: join the same ID and test within-unit differences. Small horizontal offsets separate nearby observations; matching remains correct after rows are reordered. | [PNG](../examples/gallery/paired.png) | [R](../examples/gallery.R) |
| Repeated measurements | Follow the same units over time: thin lines show units, thick lines show group means from a random-intercept model. The named comparison is the group-by-day slope difference. | [PNG](../examples/gallery/repeated.png) | [R](../examples/gallery.R) |
| Dose response | One assay, three technical wells per dose: show wells, a supported 4PL/5PL candidate fit and its pointwise conditional 95% mean-response interval. Save all candidate fits and relative ED50 intervals. | [PNG](../examples/gallery/dose_response.png) | [R](../examples/gallery.R) |
| Censored survival | Time-to-event data: retain censor marks and 95% log-log intervals; align numbers at risk to the same time axis. Save the log-rank result separately. | [PNG](../examples/gallery/survival.png) | [R](../examples/gallery.R) |
| Heatmap | Compare sample patterns across measured analytes: log2-transform signals and scale each row across all six samples. Preserve raw values and exact display values; this is display scaling, not a gene-set score. | [PNG](../examples/gallery/heatmap.png) | [R](../examples/gallery.R) |

From this skill's directory, run:

```sh
Rscript --vanilla examples/gallery.R gallery-output
```

The script resolves its helpers from its own location, so an absolute script path
also works from another directory. It uses the usual R setup plus `nlme`, `survival`
and `drc`, and makes no downloads. Each case saves PDF, PNG, the editable ggplot RDS,
direct source data and complete numerical results; fitted cases also save native
models. The output includes package versions, the script and its helpers for reuse.

Assertions check keyed pairing, row-order invariance, risk counts and heatmap scaling.
The export helper measures Arial and effective text size in each PDF. Inspect the
saved image when adapting an example, especially the assembled survival panel.

## Four panels from one experiment

Use [multipanel.R](../examples/multipanel.R) for a mixed-geometry figure; inspect the
[assembled preview](../examples/multipanel.png) before adapting it.

```sh
Rscript --vanilla examples/multipanel.R multipanel-output
```

Four synthetic donors each supply a Control and Treated aliquot. Initial cell counts,
paired endpoint viability, individual fluorescence trajectories and an endpoint
analyte heatmap share sample identities. The trajectory preserves an internal missing
observation; the heatmap scales each analyte across the eight aliquots. These are
descriptive panels with no inferential tests or gene sets.

At 180 × 145 mm, the three quantitative panels share aligned margins and one
condition key; the fixed-aspect heatmap retains its own diverging scale. Signed
cell values preserve the heatmap's direction in grayscale, with contrasting text.
The code
uses cowplot directly and saves the assembled figure, individual panel objects,
source/display tables and caption. Adapt the panel roles and dimensions to the
question; this example does not require four panels for simpler data.
