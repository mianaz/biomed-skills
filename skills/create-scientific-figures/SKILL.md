---
name: create-scientific-figures
description: Turn biomedical research data into figures in R, Python or GraphPad Prism, including editable Prism PZFX tables. Choose charts and design-supported statistics, export editable sources, and inspect the rendered result. Use for biomedical comparisons, trajectories, dose responses, omics displays, figure sets and figure repair. Plotting in other research domains is outside this skill's scope.
---

# Create Scientific Figures

Version 3.17.1 — portable visual examples, four-panel composition and rendered color previews.

Given data, deliver the requested figure with editable sources. Choose the encoding,
analysis and layout within the user's scope, execute the code, and inspect the saved
image. A script or a successful export alone is not the deliverable.

For first use or a new environment, follow `references/quickstart.md`: check the
chosen R/Python runtime and Arial, then use the bundled examples if a starting
script is helpful. A working environment does not need repeated setup.

## Set the task scope

Use this skill for basic biological research (descriptive, functional or mechanistic),
experimental biomedicine, omics, medical imaging, clinical or epidemiological studies,
and translational research. Basic biology does not require a disease endpoint.
Include engineering or AI/ML evaluation when its question and data address a biomedical
problem. Standalone physics, materials, energy, environmental, economic and general
AI/ML plots are outside scope; a chart type or journal name does not establish eligibility.

Choose the task from the request; this is a working decision, not a mandatory question:

| Request | Scope of work |
|---|---|
| Repair an existing figure | Change the requested panels or properties. Preserve valid analysis, data, group identities and other established choices. Resolve a discovered error that affects the requested result and explain it. |
| Make a specified single panel | Answer the named question with its outcomes and contrasts. Other columns provide context; they do not require extra panels or analyses. Resolve crowding within the requested panel before proposing a wider redesign. |
| Design an open-ended figure or figure set | Plan coverage of the distinct outcomes relevant to the question before adding derived views. Record a scientific reason for omitting a relevant outcome. |

Honor the user's supplied analysis and reference scope. An analysis/chart-type template
does not also prescribe appearance or palette. Appearance-only repairs do not trigger
new statistical tests or model fitting.

## Choose the execution language

R and Python are first-class routes under the same scientific and delivery contract.
Honor an explicit language or an existing validated analysis. Otherwise use the
project's environment; with no preference, start with R for conventional experimental
tables and Python for an existing Python analysis. Read the shared controls and only
the selected route in `references/r-and-python.md`.
Use ggplot2/cowplot in R, Matplotlib (and Seaborn when useful) in Python, or native
GraphPad Prism when requested or appropriate. Retain specialized method-native plots
when reconstruction would change their results. Generate both languages only when
requested. A benchmark's assigned language conditions override personal defaults.

For editable Prism output, read `references/graphpad-prism.md`. Export compatible
Column, Grouped or XY data as `.pzfx` alongside the figure. Native graph styling
and Prism analyses require a Prism project/template and native verification;
label a data-only PZFX accurately. Preserve paired IDs and replicate subcolumns.

## Work from the data

1. Read the data and dictionary. Identify measured quantities, units, normalization,
   groups, biological versus technical replication, pairing, repeated measures and
   missingness. Distinguish supplied values from transformations still to be computed.
   Establish label meanings, including species and gene versus protein, before styling.
2. State the supported comparison in one sentence. Use supplied contrasts; otherwise
   select a small exploratory set from the design before inspecting P values. For an
   intervention, start with treatment versus reference within relevant strata unless
   another comparison was requested. Ask only when unresolved meaning or design would
   change the requested analysis; complete the supported work while resolving it.
3. For a supported experimental comparison, compute ordinary figure-level estimates
   and tests when absent, unless the request is explicitly descriptive or appearance-only.
   Read `references/statistics.md` when computing or displaying inference. It is the
   authority for analysis eligibility: the design and required quantities must identify
   the inference. Public sample IDs and raw rows are not universal prerequisites.
   Match paired/repeated observations by identifiable units; arbitrary row IDs do not
   establish independence. Preserve valid supplied analyses and their estimands.
   When inference cannot be identified, produce the supported descriptive figure and
   state what information is missing. Never fabricate raw points, pairing, n or P values.
4. Read `references/visual-design.md` and plan a compact encoding. Record the primary
   contrast and the roles of x, color and panel position briefly in the figure notes.
   Keep the primary comparison local. For open-ended layouts with a third factor or
   more than four competing curves, compare an overlay with aligned small multiples
   at the same intended placement; retain the candidates and reason for choosing.
5. Follow the relevant analysis reference:
   - For pharmacologic dose fitting/comparison, read `references/dose-response.md`:
     retain observations, diagnose supported models and report estimates with uncertainty.
   - For omics, enrichment, embeddings, networks or clinical-model outputs, read
     `references/analysis-to-chart.md`. Plot supplied valid results without rebuilding
     an upstream analysis solely to change its appearance.
   - For specialized single-cell/spatial data, read `references/single-cell-figures.md`.
   - For gene sets or signatures, follow the gene-set record in
     `references/figure-delivery.md`, including original and actually used genes.
   - For a worked decision pattern, use `references/visual-gallery.md`: inspect the
     matching preview and runnable source before adapting its geometry. It includes
     six analysis examples and a four-panel composition. Examples do not assign the
     user's data, test, palette or panel count; preserve the requested scope.
6. Compute, plot and export using `scripts/compact.R` or `scripts/compact.py` where
   applicable. Save full-precision results separately from formatted annotations.
   Preserve unique experimental observations in inference even when a display reuses
   a baseline or reference. See `statistics.md` for repeated units and comparison families.

## Keep the figure readable

- Show individual evidence when feasible: points with a defined summary for small
  groups, matched points for pairs, and true numeric positions for trajectories.
  Connect individuals only when the same unit was followed. Draw summaries behind
  observations and separate colliding points horizontally without changing their values.
- Use Arial, a cowplot-like compact appearance, and no decorative titles or grids.
  Put narrative and methods in the caption; retain necessary group and panel labels.
  Start near 14 pt, with axis titles slightly larger. All text, including scientific
  subscripts and superscripts, must exceed 10 pt at the intended viewing size.
- Choose the intended placement before plotting: use the known assembly width, or
  90 mm as a standalone-panel review assumption. Keep that target through revisions.
  Effective size equals exported points times placed/exported width. Compact labels,
  whitespace and layout before changing dimensions; enlarging the canvas alone does
  not repair readability. The physical-space guidance in `visual-design.md` supplies
  starting dimensions and treatment of long labels, compact axes and risk tables.
- Use the scientific typography rules in `visual-design.md` for complete gene-symbol
  italics (including digits), upright proteins, Greek letters, charges, indices and
  genotypes. Check these in axes, legends and panel labels of the final assembly.
- Resolve colors with `references/color-policy.md` before plotting. Use semantic
  condition names and retain the saved mapping through reordering, subsets and new
  panels. Explicit user colors take precedence over project context and the default.
  For new categorical mappings, use CARTO Bold, starting with purple/green; reserve
  gray for an identified control. Blue and orange remain available for larger sets.
  Use comparable scales and one useful key across related panels.
- Apply the annotation rule in `statistics.md`: choose visibility before reading
  the P values; default to hiding nonsignificant text and brackets. Use
  `nonsignificant="ns"` or `"value"` for a user request or a named scientific contrast
  whose display is needed, recording that reason. Retain all
  comparisons, estimates and intervals in the full table; disclose the display rule.
  Keep comparison keys, numeric P and positions in the same table. Use `p_brackets()`
  with `p_col` for categorical contrasts or assign the full `p_labels()` result for
  curves; remove empty rows only from drawing, before assigning lanes and headroom.
  Place model/global tests beside their named term or in the caption, not on a
  bracket implying a different contrast. Keep labels clear of the actual marks.

## Assemble a Nature two-column tool-comparison figure

When the user requests this format, start the full canvas at 183 mm wide and no
more than 170 mm high. Build each panel for its final placement; do not make an
oversized figure and shrink it. Put bold lowercase panel letters at the top-left
of their panels, use bold panel titles, and keep Arial or Helvetica throughout.

- Give each tool family one fixed color across every panel and later figure. Save
  the mapping in `palette.csv`. Use an Okabe–Ito or Paul Tol colorblind-safe
  palette and do not rely on red versus green alone to distinguish families.
- Give each shading or intensity scale one meaning throughout the figure. Do not
  reuse dark gray for different quantities such as "more" and "harder".
- Define every term in the figure or its manuscript legend; add a footnote when
  a short definition does not fit the legend.
- Make component plots in R or Python, export each as vector PDF, and assemble
  them in Illustrator, Inkscape or Affinity. Export the final figure as vector
  PDF or SVG with editable text and RGB colors; a PNG may serve only as a preview.
- Write the legend separately in the manuscript: one bold title sentence,
  followed by one sentence per panel in panel-letter order ("a, ... b, ...").
  Define all abbreviations and state `n` and its unit where relevant.

## Inspect and deliver

Retain the first rendered attempt, then open the saved PDF/PNG at the intended
placement. The export helpers measure PDF text and flag some geometry defects;
their checks differ and do not establish scientific correctness or detect every occlusion.

1. Verify the requested comparison is easy to see and the task stayed within scope.
2. Compare plotted n, values, summaries, interval endpoints, units, time distances,
   paired connections and each annotation with the saved source tables.
   Confirm that hidden comparisons have no bracket or reserved annotation space.
   Check directional caption claims against the signed quantity and stated time
   window; distinguish a value increasing toward zero from its magnitude decreasing.
3. Inspect every label and panel edge for clipping, overlap and font substitution.
   Check the whole annotation box against points, curves and error bars. Read ticks
   individually; a zero-overlap report can miss merged words or text covering data.
4. Check complete gene italics, upright protein/units, Greek glyphs and script size
   and position in actual axes, legends and panels, including the final assembly.
5. Check condition colors, group order, comparable scales and consistent summaries
   across panels. Investigate unmapped groups rendered gray and obscured observations.
   For color-encoded groups or values, generate grayscale and color-vision views
   with `scripts/color_preview.R` when its R dependencies are available, or an
   equivalent installed tool. Inspect them using `references/color-policy.md`.

Fix evidence errors first, layout second and local formatting third. Rerun and view
the affected export; usually one or two focused passes suffice. Retain revised
attempts and report remaining defects. Do not claim visual inspection when viewing
was unavailable.

Deliver according to `references/figure-delivery.md`: clean vector PDF and PNG,
editable plotting source/object, direct source tables, full statistics and a concise
caption covering n, unit, summary, test, correction and exclusions. For image evidence,
preserve originals and document crops, global adjustments and calibrated scale bars.
