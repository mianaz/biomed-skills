# Figure delivery contract

Apply this contract to every reported, shared, or submission figure. Private
diagnostics may use a single preview, but must be upgraded before they support a claim.

## Package the figure

Default to one lossless **600 dpi PNG** at the intended physical size. Add PDF,
SVG or TIFF only when requested or required by the delivery task. Do not create
extra formats, separate legend exports or duplicate titled/clean versions by default.
The font check can use a temporary PDF; remove that temporary file after measurement. For project work, update the
[root HTML dashboard](../../biomed-shared/project-dashboard.md) with previews and
links to the requested exports and existing source records. A standalone figure task
can use a requested gallery without creating a new project structure.

Use a short factual title only when it adds dataset, gene/gene-set or measurement
information absent from the axes. Omit a title that repeats the x/y labels. Do not
add a subtitle or subheading by default. Put sample sizes (n and experimental unit),
summary/interval definitions, test and correction method in the caption, not in
plot titles, axis labels or group headers. Show n on the plot only when requested.

Statistical annotations show numbers only by default: `0.013` or `<0.0001`, with
no `P`, `padj`, `P adj.` or equals-sign prefix. The caption identifies whether these
are raw or adjusted P values and names the correction and comparison family.
Keep each number visibly linked to its comparison.

Keep rerunnable plotting source, parameters, direct inputs and full-precision
statistics in the existing analysis structure. Preserve valid native sources and
manual edits. Share code/data packages or native Prism projects when requested.

## Reuse inputs and save objects selectively

Save each unique direct plotting dataset once, then link all panels and style
revisions to it. Reuse existing source tables when they contain the exact displayed
values and identifiers. Reference large upstream data by its existing path/accession
and version; retain the small derived table or matrix actually needed to redraw.
New transformations or selections need their own direct values or a reproducible
recipe and stable input reference. Avoid copying a full analysis object per panel.

Code plus inputs and parameters are the default reconstruction route. Save an RDS,
pickle or other plot object only when requested or useful for native tuning,
expensive computation, complex state or edits that the script cannot reproduce.
Create `objects/` only when used. Preserve existing native files containing manual
edits. A compact schematic SVG/scene can be its editable source without requiring
additional PPTX/PDF copies.

The shared exporters default to `formats="png"`, `save_object=FALSE` (Python:
`formats=("png",)`, `save_object=False`). `source_data` records an existing source
path or reference; it does not copy or save that input. They retain one compact
`*_export.json` for placement, font measurements, source references and geometry.
Use `diagnostics=TRUE`/`True` only when detailed measurement tables are useful.
Keep current outputs and approved milestones in the existing version scheme;
remove only newly created temporary files automatically. Existing results are not
automatically deleted or pruned by an export.

## Save exact figure source data

- Preserve the values actually sent to each geometry, including transformed/scaled
  values, category order, grouping keys and uncertainty endpoints, in the shared
  source record above. Style-only revisions reuse it.
- Retain excluded observations with `included = false` and an `exclusion_reason`.
  Never make an excluded group look like a measured zero.
- For a summary panel, include the displayed summary and enough identifiers to link to
  the underlying observations when available. Do not publish unrelated sensitive
  columns merely because they were present in memory.
- For heatmaps, save the exact plotted matrix after scaling/capping and the displayed
  row/column order. If raw values are also useful, save them separately and label them.
- For embeddings, save displayed coordinates, label/group fields, inclusion status,
  and any displayed feature value. Do not rerun an embedding only to recreate a plot.
- For images, reference the original and processed image in the image-integrity block;
  do not duplicate large raw files solely for this package.
- Spot-check row counts, groups, extrema, factor levels, and annotated values against
  the rendered panel.

## Record each quantitative panel

Record supplied validated analyses or the analyses computed from the data by this
workflow. Identify which route was used and explain the test and comparison family.
Save full-precision statistics, not just the rounded figure labels.

```text
panel_id:
analysis_unit:
groups and contrast direction:
n per group:
biological replicates:
technical replicates:
displayed value or effect:
center statistic:
spread or interval:
test and sidedness:
pairing, blocking, or repeated-measure structure:
multiple-comparison method and correction family:
displayed p-value:              # exact raw or adjusted value; identify which
annotation rule:                # hide / ns / value, threshold and any explicit exceptions
source-data file:
visible exclusions:
panel role and reason:          # primary / supporting / diagnostic
delivery placement:             # main/supplement, body/appendix, slide, dashboard, etc.
```

For model-evaluation panels, also record the supplied split, seed/fold count, metric
definition, interval/variability definition, and baseline. If any required field is
unknown, determine whether it can be established from the inputs. If not, state the
specific inferential limitation; do not invent it from plotting-library defaults.

For annotations selected by the visibility rule in `statistics.md`, prefer numeric
P values (`0.013` or `<0.0001` at that reporting precision) over stars;
`ns` mode uses `ns` for nonsignificant comparisons. Hidden comparisons retain their
full-precision results in the statistical table. If a venue or user requires stars, provide the
threshold legend and retain exact values in the panel report/source table. Make the
uncertainty definition explicit; an unlabeled error bar is incomplete. Link each
P annotation to its actual contrast with a short comparison line or bracket, or an
unambiguous contrast row. Avoid detached P values that make the reader guess the comparison.

Write directional caption statements from the displayed quantity and saved results.
Check the named groups, contrast order, transformation and time window. For example,
a signed value changing from -0.8 to -0.2 increases by 0.6 while its absolute magnitude
decreases by 0.6. Use the quantity actually plotted. Inspect the full claimed interval:
an endpoint difference establishes a net change, not a monotonic trajectory. A claim
about a fitted trend must agree with the corresponding model term and uncertainty.

## Record gene sets and signatures

For gene sets or signatures displayed in a figure, use the shared
[gene-set record](../../biomed-shared/gene-set-records.md). Link that existing
membership and computation table from the figure notes and Methods when present.

## Record image integrity

For microscopy, spatial images, radiology, gels, blots, or other image evidence:

```text
panel_id:
original image:
processed display image:
field selection rule:
crop and rotation:
global brightness / contrast / gamma:
channel mapping or pseudocolor:
scale-bar calibration and units:
stitching, tiling, or projection:
splicing or lane rearrangement:
reuse in another figure:
linked quantification panel or table:
```

Apply display adjustments to the full relevant image or comparison set. Do not make
undisclosed local selective adjustments, erase background, duplicate structures, or
splice lanes without visible boundaries and disclosure. Preserve informative
background. Use a calibrated scale bar rather than magnification alone, and apply
comparable display ranges when panels are visually compared.

### Connect image analysis to quantitative results

When measurements are derived from images, link the analysis inputs, critical
settings, software/model version and object-level measurements to the independent
sample summaries. Keep representative input/output examples together: the input
image, segmentation/detection or ROI overlay, and the corresponding measurement.
Retain manual ROIs or corrections used in analysis. Use the existing analysis record
and source tables for this information.

For an established workflow, record its reference, version and consequential
settings. For a new combination of steps, also retain their order and runnable
workflow. For a trained image model, identify the model/training version and keep
independent validation inputs and outputs suited to the intended measurement.
Show the diagnostic example in the analysis preview when a preview is requested;
select manuscript image examples according to the figure's scientific purpose.

## Export at final physical size

- Export PNG at 600 dpi by default. For requested PDF/SVG, keep vector text and
  simple geometry editable/selectable and embed fonts where supported. Use TIFF
  when requested or required for submission. Avoid JPEG recompression of line art
  or quantitative images.
- Specify width and height in mm or inches before DPI. A high DPI number does not fix
  an undersized or upsampled source image.
- Use at least 300 dpi for continuous-tone image composites and commonly 600 dpi for
  line-art raster output, unless the current venue guide specifies otherwise. Never
  upsample to imply detail absent from the source.
- Rasterize only dense point/image layers when vector output becomes unwieldy; retain
  vector axes, labels, annotations, and simple lines.
- Verify the current venue's official author instructions immediately before
  submission; journal dimensions, color modes, fonts, and accepted formats change.

Choose dimensions from content and intended placement; no fixed width applies to
every plot. Direct R devices are sufficient. For example:

```r
w_mm <- 89; h_mm <- 70
# Save source_data/fig1_a.csv once when this direct input is first created.
export_biomedical(p_clean, "figures/fig1_a", w_mm, h_mm,
                  source_data = "source_data/fig1_a.csv")
# When requested, add formats = c("png", "pdf") or save_object = TRUE.
```

Use `svglite` when editable SVG is needed and `ragg::agg_tiff` for lossless TIFF.

## Verify and record delivery

Apply [figure-verification.md](figure-verification.md) to the saved exports and
final placement. It covers necessary statistics, measured typography, formats,
effective DPI and visual inspection. Keep the compact export record and a short review
note; save a separate checker report when that checker is used. For image evidence, also reconcile the field, crop,
channels, display range and scale bar with the image-integrity record above.
For image-derived measurements, inspect the linked input/overlay example and
reconcile object counts or values with the sample-level analysis table.
