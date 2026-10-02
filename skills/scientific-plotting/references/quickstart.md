# First figure

Use this page once when setting up a project. Run commands with the interpreter
that will draw the figures. Paths below are relative to the installed skill folder
or `skills/scientific-plotting` in this repository.

## R

Use R with Cairo support and an installed, licensed Arial font. Check the runtime:

```bash
Rscript --vanilla scripts/check_environment.R
```

The core packages are ggplot2, cowplot, ragg, pdftools and systemfonts. Install
missing packages into your usual R library:

```r
install.packages(c("ggplot2", "cowplot", "ragg", "pdftools", "systemfonts"))
```

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
Matplotlib, NumPy, pandas, SciPy and PyMuPDF. Arial must be installed separately;
fonts are not redistributed with the skill. A successful setup check confirms
availability; the export helper still measures the font and size in each saved PDF.

## Three complete examples

From the skill folder:

```bash
Rscript --vanilla examples/run.R figure-examples
```

| Example | Data and analysis | Preview |
|---|---|---|
| Independent groups | Six observations per group; mean/SD, Welch tests and Holm adjustment | [View](../examples/groups.png) |
| Paired observations | Six donor pairs; matched lines and a paired t-test | [View](../examples/paired.png) |
| Repeated trajectories | Three replicates per condition; uneven time spacing and two missing values; descriptive | [View](../examples/trajectory.png) |

All three datasets are synthetic teaching examples. The output folder contains
PDF/PNG, R plot objects, source tables, captions, statistics or descriptive summaries,
editable `.pzfx` tables, runtime versions and a copy of the script and its helpers.
Run `Rscript --vanilla figure-examples/run.R another-output` to reproduce the
delivery without the installed skill folder.

Open a `.pzfx` in GraphPad Prism to edit its input table. These fresh files contain
data, without preconfigured graphs or analyses. For native graph projects and
existing templates, see [GraphPad Prism output](graphpad-prism.md).

## Visual decisions and composition

The [visual gallery](visual-gallery.md) includes six complete analysis examples and
a four-panel composition, with previews and portable source. From the skill folder:

```bash
Rscript --vanilla examples/gallery.R gallery-output
Rscript --vanilla examples/multipanel.R multipanel-output
```

The gallery uses `nlme`, `survival` and `drc` for its corresponding analyses. The
four-panel example uses the core plotting packages. Each script saves its synthetic
data and editable plot objects; adapt the matching example rather than generating
every panel for a new task.

For rendered color previews, use `scripts/color_preview.R` on an R- or Python-made
PNG. It additionally uses `png` and `colorspace`; see [color previews](color-policy.md#preview-the-rendered-colors)
for the command and viewing scale.

## Your own data

Start a new agent task after installing the skill, attach a CSV plus the meanings
of its columns, and ask:

> Use $scientific-plotting. Compare these groups, show the individual
> biological replicates, and save a compact PDF/PNG plus editable source and
> GraphPad Prism data. The subject IDs identify paired observations.

Specify pairing only when it exists. Include units, biological/technical replication
and any supplied analysis. The agent can then choose a supported figure and test.
For appearance-only edits, identify the changes and provide the existing plot/source.
