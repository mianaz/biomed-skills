# Choose the encoding and compact layout

Apply the task scope from `SKILL.md` before planning the layout. Repair the requested
properties of an existing figure; a specified single panel stays focused on its
question. Outcome coverage and alternative multi-panel layouts below apply to
open-ended figure design, not an automatic expansion of a focused task.
Use the fewest panels that make the required comparisons readable. Start a focused
question with one panel. Add a panel for distinct evidence or a necessary separation
of comparisons, not to repeat the same result in another chart or fill a grid.
Within a panel, keep one outcome, its raw evidence, summary and relevant P values
together when possible. Additional panels can separate strata of the same outcome.

For mixed-geometry assembly, adapt `examples/multipanel.R` and inspect its preview
in `visual-gallery.md`. It uses cowplot directly: align comparable plot regions,
share only a truly common condition key, and retain a separate heatmap scale. Keep
the fixed-aspect heatmap intentional rather than stretching it to match other axes.

For the source examples and their application limits, consult
[Points of View sources](../../biomed-shared/visualization-sources.md) when a design
choice needs justification.

## Set a per-panel complexity budget

List the outcomes, explanatory factors, levels and primary comparisons before
plotting. Usually encode at most two independently varying explanatory factors in
one coordinate system: time/dose plus a treatment contrast, or two grouped categorical
factors. The outcome is counted separately; complementary mixture labels describe
one factor. Replicate IDs are units, but displaying many individual traces still adds
visual load. In an open-ended layout, a third factor or more than four competing curves triggers comparison
with aligned small multiples: render both arrangements at the same intended placement
and record the choice in the figure notes. Reuse the same data, scales and summaries
so that this tests organization. Choose the view that exposes the primary contrast
locally with less line crossing and legend lookup; a cleaner-looking overview can
still conceal that contrast. These are design heuristics, not universal cutoffs:
level counts, crossings, label length and the reading task determine whether to split.

Choose scales for the comparison. Absolute magnitudes need comparable units,
transformations and ranges. Local shape or small variation can use clearly labelled
local scales; retain global context when it is needed to interpret their magnitude.
Use the fewest views that answer the question. Reusing one scale is useful only when
the required differences remain visible; bar lengths still need a meaningful zero.

Keep the primary contrast inside each panel; use a secondary stratifying factor for
panel position. Do not split the two treatment curves the reader must compare while
overlaying many background strata. Use stable panel order, comparable scales and one
shared key. Short condition labels and panel letters are useful; decorative strips
are not. Several simple panels can carry more usable information than one dense plot.
For a treatment-by-stratum time course, try treatment as color and stratum as panel,
with outcomes in aligned rows or paired blocks. An extra selected-time-point chart
should add a distinct reading task; do not use it just to rescue a crowded trajectory
or make room for P values that could be attached to the local comparison.

A composite can combine a small design/composition key with quantitative curves and
another outcome's chart. Choose each encoding for its reading task. A two-component
pie can identify a known starting mixture; it does not show measured replicate
variation. For a quantity encoded by circle area, use area proportional to value
(for example `scale_size_area()`), label the actual quantity and show a numeric size
key. A numeric y axis is unnecessary when y only positions named rows, but rows must
remain identifiable. Retain a quantitative axis when position carries magnitude;
prefer position over size when precise comparisons or spread are the main question.

When an open-ended figure request covers several nonredundant outcomes, cover them before
spending space on a selected time point or a second view of the same outcome. Avoid
making a simple trajectory figure taller by appending a redundant significance panel.

## Match the reading task

Use this table before template retrieval. The question determines what the reader
must compare; the shape of the input table alone does not select a chart.

| Reading task / data | Useful first choice | Preserve |
|---|---|---|
| Compare group means | Prism-style bars plus matching observations when a zero baseline is meaningful; otherwise center/interval with observations | Independent units and defined uncertainty; bars start at zero |
| Paired groups | Matched points with thin per-unit lines and a summary | Join by unit ID; never connect different samples |
| Time course | Same-unit trajectories, or group-summary lines with intervals and independent observations | True numeric spacing and missing segments; destructive samples at different times must never be joined as individual trajectories |
| Pharmacologic dose/concentration | Raw observations plus a supported fitted 4PL/5PL curve and uncertainty; read `dose-response.md` | Actual concentrations on a log axis, zero controls separately, tested range, parameter identifiability; lines joining means do not estimate potency |
| Compare distribution, tails or modes | Box with observations for spread; histogram, ECDF or supported density for shape | n and heterogeneity; choose a display that exposes the requested feature |
| Several same-unit endpoints | Grouped bars/points or aligned rows in one panel | Absolute magnitude and the same semantic colors |
| Effect estimates | Forest plot with explicit interval endpoints | Contrast labels and effect units; do not replace raw outcomes without a reason |
| Association | Scatter or density/hexbin when genuinely dense | Outliers, uncertainty and sampling structure |
| Browse matrix blocks and joint patterns | ComplexHeatmap or method-native view; read [heatmaps.md](heatmaps.md) | Explicit scale, semantic order, row selection, transformation and sample identities |
| Trace a network path / find connectivity blocks | Node–edge diagram for paths; adjacency matrix for blocks | Edge meaning/direction and node identities; layout distance has meaning only when defined |
| Compare sets and intersections | Overlap diagram for a few simple sets; combination matrix with native size bars for many combinations | Define exclusive combinations versus inclusive pairwise overlap and retain set totals |
| Composition | Per-sample stacked bars | Biological replication; pooled cells are not replicate samples |
| Survival | Kaplan–Meier with censoring marks | Follow-up scale, numbers at risk when useful, and censoring |
| Image evidence | Calibrated image with linked quantification | Field selection, comparable display transforms and scale bar |

Bars with matching sample points remain a familiar choice for a mean comparison.
Scatterplots answer relationships between measured numeric variables; raw dots
within categories support a group or distribution display. Keep a simple grouped comparison together; split a crowded factorial
display when that makes its contrasts readable. Avoid duplicate raw/effect panels
and rank-only displays that hide the measured values.

Choose chart types by the reading task, not a preference for dots. Raw sample points
can support bars, boxes, paired comparisons or curves. A dot/bubble matrix is useful
when its rows, columns and encoded quantities are needed together. For a single
quantity, prefer a suitable position-based chart over adding circle size and color.
Use bubble size only for a second quantity that matters to the question; use a
heatmap for a matrix when joint patterns are the task. For precise comparison or
ranking of a few values, use a common position scale (for example an interval plot
for supplied effects). Small input matrices do not automatically need heatmaps.
Retain square tiles without numeric overlays when a heatmap is selected.

For time data, distinguish calendar time, time after a named event and cyclic phase.
Record any alignment or phase transformation; preserve the original times. Choose
linear or cyclic placement from the question, with actual intervals and gaps visible.
For a measurement overlay on a pathway or anatomical view, keep the same relationship
scaffold across conditions and give the quantitative layer its own native scale/key.
Use the schematic workflow for editable biological context. State which geometry
is measured and which positions serve layout.

When the question is how two curves differ over time or dose, show the relevant
difference, ratio or model contrast on a quantitative axis with its valid interval.
Use the same x values, preserve the pairing/repeated-unit structure, and calculate
uncertainty for the contrast itself; subtracting separate interval endpoints is
not a contrast CI. If only the contrast is needed, it can be the single main panel.
Keep the original trajectories when their absolute values answer another requested
question. Distance between curves on the page is not a reliable difference readout.

For a selected bar-plus-point display, draw bars first, thin intervals second and
raw points last. With a point-and-interval display, use a small mean line or put the summary
beside the observations; an opaque diamond centered on them hides evidence.
Use beeswarm/quasirandom horizontal spacing when points collide, keeping y unchanged
and groups distinct. Verify visible observations, not only the number of point rows.
If the low-range groups become unreadable on a shared scale, consider aligned rows
or a clearly labelled scale treatment; do not cover their spread with larger symbols.

## Match data density to the final view

Inspect marks at the intended placed size before choosing binning, density, a
summary or a detail view. Use the data region's usable width, after axes and guides,
to judge how many bins can be distinguished. About 1 pt per bin is a useful print
trial for judging heights or colors, not a fixed limit on every chart. Increasing
DPI alone leaves the physical density unchanged.

Choose the aggregation statistic for the reading task. A bin mean can hide short
peaks or troughs: when those matter, retain a min–max envelope, selected original
extremes or a local view. Add only the information the question needs. A within-bin
range or SD describes variation within that bin; label it separately from a CI.
Save bin boundaries, counts, the summary definition and the displayed aggregate
alongside the original input. Define whether highlighted extremes use local or
global thresholds. Compare the aggregated view with the original values before
delivery. Binned height tracks suit magnitude comparisons; a compact heat strip
can serve sparse-event context. Choose each by its reading task.

## Plan physical space together with typography

Use cowplot/ggprism, Arial and a white background. Remove grids, strip backgrounds,
titles and subtitles. Put essential grouping labels in native axes or facets;
follow [native controls](template-first-layout.md#prefer-native-controls-and-data-driven-layout)
for legends, data labels and annotations.

Start near 14 pt for ticks, key labels and statistics, 14–15 pt for axis titles.
At 12 pt, a 180-mm panel shrunk to 90 mm has 6-pt text. Judge the exported figure at
its intended placed width; a theme declaration is not a readability measurement.
Apply the [shared type targets](../../biomed-shared/visual-standards.md#1-scientific-typography-and-effective-size).
If the intended placement is unspecified, use the
compact standalone export's actual width and record it. Pass `placed_width_mm`
explicitly; the helper's 90-mm default is not a target panel width. Keep
an agreed target through repairs; do not change `placed_width_mm` merely because
the export grew. The export canvas remains adjustable. `export_biomedical()` checks text after this
scaling; increasing the canvas alone cannot make that check pass. Shorten redundant
wording and use established quantity abbreviations with full definitions in the
caption before increasing width. Do not inflate canvas size to fit a plotting default.
Target approximately 11–12 pt effective ticks, legend and statistical text, with
axis titles only slightly larger. This is a starting hierarchy, not a ceiling.
When one text layer fails, adjust that layer first instead of scaling up every label.
For long categories compare short wrapped labels with rotation; rotated words should
not consume more vertical space than the evidence without a clear reading benefit.

Use the [shared full-canvas dimensions](../../biomed-shared/visual-standards.md#2-physical-space-and-panel-dimensions)
and [native panel sizing](template-first-layout.md#preserve-plot-height). Keep
comparable plots at similar scales and sizes. Honor supplied dimensions and
appearance-only repair scope. Inspect the data region as well as the outer canvas.

- Use roughly 4–6 useful major ticks. Eliminate repeated axis titles and empty space.
  Numeric sampling times need not all be tick labels: preserve their true positions
  while selecting readable ticks when adjacent time points are close. The points
  remain at every observed time even if only a subset receives a tick label. If
  every tick is essential, use 45 degrees and inspect at the placed size. In a
  vertical stack, keep x text/title only on the bottom panel.
  For numeric axes, use the existing R guide to omit overlapping tick labels at
  render time: `scale_x_continuous(breaks = times,
  guide = guide_axis(check.overlap = TRUE, angle = 45))`. This retains numeric
  spacing and all points; it changes labels only. Do not apply automatic label
  omission to categorical groups whose identities must remain visible.
- Start categorical x labels at 45 degrees whenever the axis has two or more groups, including short labels; use `hjust = 1, vjust = 1`.
  Wrap labels at natural boundaries; use concise scientific abbreviations
  consistently. Rotation alone
  does not guarantee separation: inspect the label ends and panel below.
- Wrap long y-axis titles, separating quantity from units where natural.
  For a short panel, also wrap a long quantity name. The rotated title's total
  length must fit that panel's height without entering the next panel. Use compact
  tick notation such as `1e4`, `1e5`, `1e6` when long integer labels consume space.
- A categorical y axis can double as the key. Do not repeat its categories in a legend.
  Keep a compact legend when color/shape describes another variable.
- Place a shared key close to the data in an unused area that does not cover marks.
  Minimize key size and margins; do not sacrifice label readability to fit it.
  Use native guides or facets for group identities. Allocate a separate
  margin for required panel letters so they cannot collide with rotated axis titles.
- Follow `color-policy.md` for fixed defaults, context inheritance and persistent
  category mappings. Match fill/color/shape guides so one variable does not acquire
  two legends. Keep labels or shapes when they convey needed information. Continuous magnitudes use a sequential scale; a diverging scale
  needs a meaningful center. Preserve the same limits for comparable quantities.

## Label biological quantities

Name the biological quantity in axes, native legends, facets and annotations.
For expression, prefer `Gene expression (z-score)` to `row z`, or `Normalized
expression (log₂ scale)` to `log2CPM` when those descriptions match the data.
Name a program score as a score, not expression. Keep units and useful scale cues
visible; record exact normalization, log base/pseudocount, scaling axis and reference
samples in the caption or linked source metadata. A label-only edit preserves values,
transformations and validated analyses.

## Scientific typography

Set typography from the biological entity and species, not a capitalization regex.
Human gene symbols such as *TP53* and mouse gene symbols such as *Trp53* are italic;
their protein symbols are upright (TP53 and TRP53). Keep the approved symbol's exact
case and spelling, including exceptions. Italicize digits within gene symbols too.
Full protein names, assay names, cell lines, group names and units remain upright.
A mixed marker axis needs individual labels: RNA gene symbols may be italic while
protein measurements and `All markers` remain upright. Keep the input identifier
unchanged; record species, entity and any display alias in the plotting label table.
Use [HGNC](https://www.genenames.org/about/guidelines/) and the
[mouse/rat nomenclature guide](https://www.informatics.jax.org/mgihome/nomen/gene.shtml)
for identity and style. Other organisms follow their own naming authority.

Preserve α/β/γ/δ/Δ and μ with the intended case. A protein label such as β-catenin
does not turn a gene symbol into a Greek-letter name. Use true layout for Ca²⁺,
H₂O, IC₅₀, log₂ and s⁻¹; chemical symbols, unit symbols and descriptive indices are
upright, while mathematical variables follow their defined notation. Retain the
meaning of genotype/allele superscripts, +/− signs and cell-surface positivity.
Use a real minus sign for negative exponents. Do not parse underscores or digits
in sample IDs, gene symbols or cell-line names as mathematical scripts. For mouse
allele names, consult the allele rules; a shorthand such as *Trp53*⁻/⁻ requires its
exact allele and biological meaning in the accompanying methods.

In R, use ordinary strings with `fontface = "italic"` in `geom_text()` or
`face = "italic"` in `element_text()` when the whole label is italic. Keep
`family = "Arial"`; the face selects Arial Italic. This retains text spacing.
For mixed labels or mathematical scripts, quote complete gene strings inside
plotmath: `italic("SLC7A11")`, not `italic(SLC7A11)`. Unquoted symbols use
mathematical spacing, which can spread the letters apart and leave digits upright
even when the embedded font is Arial Italic. Use `plain()` for upright spans and
quoted Unicode Greek letters to keep normal font selection in PDF and PNG. For a
mixed axis, supply an expression vector to `labels=`; for panel text use
`geom_text(parse = TRUE, family = "Arial", size = 16, size.unit = "pt")` with
explicit, trusted label expressions. Never parse arbitrary input identifiers.

```r
expression(italic("TP53"), plain("TP53"), italic("Trp53"),
           plain("β-catenin"), plain("Ca")^{plain("2+")}*plain(" (μM)"),
           plain("H")[2]*plain("O"), plain("IC")[50],
           plain("log")[2], plain("s")^{plain("−1")},
           italic("Trp53")^{plain("−/−")})
```

If Arial italics look unusually loose, compare the three routes with
`Rscript examples/arial-italics.R /path/to/font-preview` from this skill folder.
The 50 × 50 mm font specimen compares PNG/PDF/SVG rendering; these extra formats are specific to that typography diagnostic. Ordinary figures follow the shared delivery contract.
Inspect the text runs and actual font faces before changing fonts or margins.
For a true clipped edge, adjust the affected label's margin or justification while
preserving the existing plot dimensions.

In Python, `biomedical_theme()` sets Arial for both ordinary text and mathtext,
with explicit italic/bold faces and an upright default. Put gene spans in
`\mathit{}` and chemistry/units in `\mathrm{}`. Use literal Greek characters for
upright names and units; mathematical variables also need explicit `\mathit{}`.
Keep figure creation and export inside the theme context.

```python
labels = [r"$\mathit{TP53}$", "TP53", r"$\mathit{Trp53}$", "β-catenin",
          r"$\mathrm{Ca}^{2\!+}$ (μM)", r"$\mathrm{H}_{2}\mathrm{O}$",
          r"$\mathrm{IC}_{50}$", r"$\mathrm{log}_{2}$",
          r"$\mathrm{s}^{-1}$", r"$\mathit{Trp53}^{-\!/\!-}$"]
```

Both math engines shrink first-level scripts to about 70%: 14 pt can yield 9.8 pt.
Start the affected label at 16 pt for an unscaled panel, then measure the saved
glyphs and intended placement. Nested scripts shrink further. Do not substitute
precomposed Unicode subscript digits to evade this check: font coverage and their
visible size vary, and Arial can fall back to another font for those characters.
The export helpers save a PDF text/font table and reject non-Arial fonts or text
at/below 10 pt. Inspect the requested renders for complete gene italics, upright
protein spans, correct Greek glyphs, script baselines and clipping; a successful
text extraction alone cannot establish semantic correctness or visible glyph size.

For dense labels at 8–10 pt, use the documented
[role-specific verification route](figure-verification.md#2-measure-effective-font-size)
when the helper's all-text gate is stricter than the requested layout.

Check these labels in their actual roles: rotated axes, legend entries, facet/direct
group labels and the assembled figure. Record gene/protein/species meaning alongside
the display label when it is not obvious from the source dictionary. A free-standing
text specimen does not check space available in an axis or legend. Verify relevant
font spans and script baselines in the final PDF, then inspect the PNG for crowding
and font differences introduced by its renderer.

For an anonymized published comparator, preserve its original scientific lettering
and report inherited style defects separately. Removing panel letters or changing
category colors must not flatten existing italics, superscripts or subscripts.
Never silently improve only the published reference or only one benchmark arm.

## Statistical annotation geometry

Apply the visibility rule in `statistics.md` before allocating annotation space.
Draw short horizontal comparison lines/brackets whose endpoints map to the group
positions. Visible numeric P or `ns` labels go immediately above their corresponding lines. Use short plain-text P labels with one
short adjustment key instead of repeating a long method string over every group.
Avoid ornamental subscripts on adjustment-method labels: their effective font can
be much smaller than the stated annotation size. Preserve scientifically meaningful
scripts using the typography rules above. If labels still overlap, stagger annotation lanes or shorten the
repeated key before enlarging the figure.
Reserve local headroom based on the highest point or interval in each visible comparison,
then stagger only intersecting comparisons. Hidden annotations leave no bracket or
reserved lane. Retain a scientifically central negative comparison with an explicit
`ns` or `value` override and state the display choice in the caption.

For continuous curves, including survival curves, a bracket across the x axis
usually implies a time-point contrast. Use the model's native annotation function
or a keyed native guide label for a requested curve comparison; define the reference
and adjustment in the caption. Put a global/model-term result in the caption when
there is no suitable native annotation. Each displayed result must identify its
outcome and comparison. Check the complete text extent against all marks.
A white text background hides data rather than resolving a collision.

For survival plots, use `Survival (%)` or `Survival\nprobability` and a concise time
unit such as `Days` when the origin is defined in the caption. Keep one group key.
A risk table adds value when attrition/follow-up matters; it need not accompany
every small animal experiment. Save counts even if the compact figure omits it.
If included, place counts under matching numeric times; remove the main panel's
x text/title and let the table carry the shared time axis. Remove table axes,
ticks, grids and repeated legends; use colored row labels as the group key.
Reserve each row at least `1.4 * text_pt * 25.4 / 72` mm at export, plus separate
space for its time axis. For example, three 12-pt rows need about 18 mm for rows
alone, not including tick labels/title. Use this measured height in the assembly,
not a tiny arbitrary `rel_heights` fraction. Inspect row labels and first-column
counts separately. Optional content should earn its space before being added.

Use explicit numeric x positions when dodged bars and brackets must align. Apply the
same positions to raw points, summaries, caps and comparison endpoints. Horizontal
plots need the equivalent explicit coordinates. Text sizes in geom_text are in mm
unless `size.unit = "pt"` is set; do not assume they inherit the theme.

Set the visible range to include raw points, full interval endpoints, comparison
lines and their text. Scale limits can silently remove interval segments and text;
check the artifact for this, not just rows in the statistics table. `clip = "off"`
alone does not reserve space or prevent labels colliding with another panel.

Before adding space, shorten repeated labels, wrap the axis title, rotate categories,
remove duplicate guides and choose a more efficient arrangement. Then adjust canvas
and font together as needed. Never fix crowding by silently dropping observations,
intervals, statistical results or required dimensions of the data. A declared
nonsignificant-annotation rule changes the display, while the complete statistical
table and underlying observations remain available.
