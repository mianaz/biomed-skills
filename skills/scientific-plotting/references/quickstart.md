# First figure

Use this page once when setting up a project. Run commands with the interpreter
that will draw the figures. Paths below are relative to the installed skill folder
or `skills/scientific-plotting` in this repository.

## R

Use R with Cairo support and an installed, licensed Arial font. Check the runtime:

```bash
Rscript --vanilla scripts/check_environment.R
```

The core packages are ggplot2, cowplot, ragg, pdftools, systemfonts and jsonlite; the examples
below also use tidyplots, ggbeeswarm and ggsignif. Install
missing packages into your usual R library:

```r
install.packages(c("ggplot2", "cowplot", "ragg", "pdftools", "systemfonts", "jsonlite",
                   "tidyplots", "ggbeeswarm", "ggsignif"))
```

For package-supplied palettes, install `ggsci` when using its callbacks; the bundled
named palettes do not require that package. Optional SVG export uses `svglite`.
The dose-response helper also uses `drc`; install it when fitting dose-response
models. The Prism table writer uses base R and requires no additional R package.
On Linux, installation of Cairo/ragg/pdftools may require the corresponding system
development libraries; use your operating system's R package instructions.

## Python

Use the project's existing environment, or create a local virtual environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/check_environment.py
```

On Windows, use `.venv\Scripts\python.exe` instead. The required packages are
Matplotlib, NumPy, pandas, SciPy, PyMuPDF and Pillow. Arial must be installed separately;
fonts are not redistributed with the skill. A successful setup check confirms
availability; the export helper measures fonts in a delivered or temporary PDF reference.

## Three complete examples

From the skill folder:

```bash
Rscript --vanilla examples/tidyplots.R figure-examples
```

| Example | Data and analysis | Preview |
|---|---|---|
| Independent groups | Six observations per group; mean/SD, Welch tests and Holm adjustment | [View](../examples/groups.png) |
| Paired observations | Six donor pairs; matched lines and a paired t-test | [View](../examples/paired.png) |
| Repeated trajectories | Three replicates per condition; uneven time spacing and two missing values; descriptive | [View](../examples/trajectory.png) |

All three datasets are synthetic teaching examples. The output folder contains
600 dpi PNGs, shared source tables, captions, statistics or descriptive summaries,
runtime versions and a copy of the script and its helpers.
Run `Rscript --vanilla figure-examples/run.R another-output` to reproduce the
delivery without the installed skill folder.

For Prism input tables and native graph projects, see
[GraphPad Prism output](graphpad-prism.md).

## Visual decisions and composition

The [visual gallery](visual-gallery.md) includes six complete analysis examples and
a four-panel composition, with previews and portable source. From the skill folder:

```bash
Rscript --vanilla examples/gallery.R gallery-output
Rscript --vanilla examples/multipanel.R multipanel-output
```

The gallery uses `nlme`, `survival` and `drc` for its corresponding analyses. The
four-panel example uses the core plotting packages. Each script saves its synthetic
data and reusable source; retain objects when useful. Adapt the matching example instead of generating
every panel for a new task.

Only when color diagnostics are requested, for rendered color previews, use `scripts/color_preview.R` on an R- or Python-made
PNG. It additionally uses `png` and `colorspace`; see [color policy](color-policy.md)
for the command and viewing scale.

## Your own data

Start a new agent task after installing the skill, attach a CSV plus the meanings
of its columns, and ask:

> Use $scientific-plotting. Compare these groups, show the individual
> biological replicates, and save a compact 600 dpi PNG plus reusable source and
> GraphPad Prism data. The subject IDs identify paired observations.

Specify pairing only when it exists. Include units, biological/technical replication
and any supplied analysis. The agent can then choose a supported figure and test.
For appearance-only edits, identify the changes and provide the existing plot/source.

## Check an existing figure

Use [figure-verification.md](figure-verification.md) for a saved R, Python or Prism
export. Its PDF/PNG/TIFF checker uses PyMuPDF and Pillow, including when R produced
the figure. It measures final-placement font size and effective pixel resolution;
complete the accompanying scientific and visual review before delivery.
