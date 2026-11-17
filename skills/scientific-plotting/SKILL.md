---
name: scientific-plotting
description: Choose and draw biomedical data figures, or repair existing figures, with editable sources and final-size visual checks. Match the scientific question and study design to a plot type and a published, R or Prism template. Prefer R with tidyplots or ggplot2/cowplot, ComplexHeatmap for heatmaps, and native Prism when requested. Use for scientific plotting, chart selection, publication figures, figure audits, interactive figure tuning, statistical annotations, effective font size and export/DPI checks, 科研绘图、图型选择和图表检查。
---

# Scientific Plotting

Read [shared principles](../biomed-shared/core-principles.md).
Deliver a figure that makes the biological comparison clear, with reusable source
and checks at its intended viewing size.

## 1. Set the scope

| Task | Action |
|---|---|
| Plotting plan only | Specify the chart, required inputs and intended checks; finish with the plan. |
| New figure or requested redesign | Identify the reading task, comparison and study design; choose the chart before its template. |
| Appearance repair | Preserve valid analysis, identities, plot type and dimensions; change the requested properties. |
| Audit | Inspect saved figures and source records; report or repair defects at the requested scope. |
| Source replication | Start from the original panel and code/native project; preserve its scientific content and requested visual features. |

Inspect the actual table or object: quantities, units, transformations, independent
units, groups, pairing/nesting and supplied results. Set the intended placement.
For computed features, use [analysis consistency](../biomed-shared/analysis-consistency.md).
For requested interactive tuning, use [Plot Tuner](references/plot-tuner.md).

## 2. Choose the chart and reuse a suitable implementation

For new figures or redesigns, read the [task-to-chart table](references/visual-design.md#match-the-reading-task)
and [template/layout defaults](references/template-first-layout.md). Select an
encoding from the question and data; sample points support that encoding.

When choosing a template, use [reference libraries](references/reference-libraries.md).
Inspect the chosen source, input contract and review status. A compatible reviewed
recipe can be reused directly. Show a short HTML shortlist when a comparison helps
selection; use the [template database](references/template-database.md) for catalog
browsing. Keep the chosen source and material adaptations in the figure notes.
Reuse the layers and calculations needed for this task; a template's example
tests and annotations apply only when the current analysis calls for them.

## 3. Analyze when needed and draw

For a new inferential comparison or statistical annotation, use
[statistical display](references/statistics.md). Reuse valid upstream results;
compute a new analysis only when the scientific question and task require it.
Descriptive plots retain clear quantities and summaries. Heatmap inference is
optional and follows the explicit trigger in that reference.

Apply [visual standards](../biomed-shared/visual-standards.md). Read only the
implementation needed for the chosen chart:

| Need | Reference |
|---|---|
| Ordinary tidy R tables | [tidyplots](references/tidyplots.md) |
| Custom R geometry or existing Python implementation | [R and Python](references/r-and-python.md) |
| Heatmap | [ComplexHeatmap](references/complexheatmap.md) |
| Native Prism project or table export | [graphpad-prism](../graphpad-prism/SKILL.md) |
| Label, spacing or typography repair | [Visual design](references/visual-design.md), [layout and legibility](references/layout-legibility.md) |
| Color mapping | [Color policy](references/color-policy.md) |
| Dose-response fitting | [Dose response](references/dose-response.md) |
| Omics, enrichment, survival or performance outputs | [Analysis to chart](references/analysis-to-chart.md) |
| Statistical brackets collide | [Bracket layout](references/stat-bracket-layout.md) |
| Publication-template geometry | [Panel patterns](references/cns-panel-patterns.md) |
| Runtime setup | [Quickstart](references/quickstart.md) |
| A worked example is needed | [Visual gallery](references/visual-gallery.md), [input-specific recipes](examples/reference-cases.R) |

Prefer the selected engine's native controls and established extensions. Keep
analysis results separate from display transformations and annotation geometry.

## 4. Verify and deliver

Apply [figure verification](references/figure-verification.md) to saved artifacts:
scientific values and necessary statistics, effective typography, file formats and
resolution, and visual inspection. Repair defects and recheck the affected output.
Use the artifact checker where it supports the output; resolve its manual-review
items in the same figure record.

Follow [figure delivery](references/figure-delivery.md) for formats, source tables,
caption, shared inputs, retained code and optional objects. Keep export defaults in
that reference. Export independent, letter-free panels for manuscript assembly.

Use [figure-plan](../figure-plan/SKILL.md) for whole manuscript figure assembly and
[scientific-visual-explainer](../scientific-visual-explainer/SKILL.md) for mechanism
schematics. A specific format or native-project request follows that deliverable's
workflow without running unrelated routes.
