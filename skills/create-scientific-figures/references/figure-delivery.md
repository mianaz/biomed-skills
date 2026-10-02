# Figure delivery contract

Apply this contract to every reported, shared, or submission figure. Private
diagnostics may use a single preview, but must be upgraded before they support a claim.

## Package the figure

Use one stable basename across artifacts. Adapt directories to project conventions;
the default layout is:

```text
figures/
  <figure>_clean.pdf
  <figure>_clean.png
  <figure>_titled.pdf          # optional review preview, only when requested
  <figure>_titled.png          # optional review preview, only when requested
  <figure>_legend.pdf          # when assembly needs a separate legend
source_data/
  <figure>_<panel>.csv         # one clear table per quantitative panel
  <figure>_<panel>_matrix.tsv  # exact plotted matrix when applicable
  palette.csv                  # shared semantic color map, including single plots
figure-notes/
  <figure>.md                  # human-readable panel and display report
```

The clean version omits review titles and explanatory subtitles but keeps necessary
axis, legend, panel, and statistical labels. Put explanatory text in the external
caption. An optional titled review preview states the intended reading when requested.
Keep the plotting script and editable source: `.rds` for R, the native Prism project,
or a rerunnable `.py` script plus JSON figure settings for Python. A Python pickle
may supplement these files but does not replace portable tables and source code.
When Prism output is requested, also provide a `.pzfx` data table via
`scripts/prism.R`, or a native Prism project with its verified graph/analysis sheets.
State which was delivered: a fresh PZFX stores editable data without reproducing
the R/Python graph's styling or transferring its statistical analyses. See
`graphpad-prism.md` for pairing, replicate subcolumns and native-project delivery.
Retain the first rendered attempt before optimization. Record the execution language
and package versions; both routes deliver the same scientific content.
For categorical color encodings, save the map and its provenance as described in
`color-policy.md`. Reuse the full map across the figure set, including absent levels.

## Save exact figure source data

- Save the values actually sent to each geometry, including transformed/scaled
  values, category order, grouping keys, and uncertainty endpoints.
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
P values (`P = 0.013` or `P adj. < 0.0001` at that reporting precision) over stars;
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

For every gene set or signature used in analysis or displayed in a figure, deliver a
complete membership table and link it from the caption/figure notes and Methods when
present. Reuse an equivalent existing analysis table. Record:

- Set ID/name, species, original definition and complete original membership, and
  the complete genes actually used after mapping/filtering. Include mapped IDs,
  missing genes, additions/removals and their reasons. A name or gene count is insufficient.
- Original publication with author/year and DOI, PMID or source link when available.
  For database sets include database, collection, identifier and release/version.
  Identify custom/modified definitions and construction; label unknown provenance
  or unavailable original membership explicitly rather than inventing it.
- Actual scoring/enrichment method, software/function/version, input layer and
  normalization, analysis unit and key parameters. For z-scores identify the scaling
  axis, reference population and aggregation; for GSEA identify the ranking statistic,
  contrast, gene universe and enrichment parameters. Keep scoring separate from
  subsequent display scaling or group averaging.

When plotting supplied scores, preserve their provided computation record and identify
missing fields. The plotting task does not authorize inventing membership or rerunning
the underlying analysis to fill a documentation gap.

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

## Export at final physical size

- Use vector PDF or SVG for plots and line art. Keep text selectable or embed fonts as
  required by the target workflow.
- Also create a lossless raster preview. Use PNG for ordinary review; use TIFF when the
  venue or image workflow requires it. Do not introduce JPEG recompression into line
  art or quantitative images.
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
ggplot2::ggsave("figures/fig1_clean.pdf", p_clean,
                width = w_mm, height = h_mm, units = "mm", device = grDevices::cairo_pdf)
ggplot2::ggsave("figures/fig1_clean.png", p_clean,
                width = w_mm, height = h_mm, units = "mm", dpi = 600,
                device = ragg::agg_png)
readr::write_csv(panel_source, "source_data/fig1_a.csv")
```

Use `svglite` when editable SVG is needed and `ragg::agg_tiff` for lossless TIFF.

## Render and inspect

Open or render the exported files at their final physical size. Inspect the artifact,
not only the plotting device.

1. Confirm every required file exists, is nonempty, opens, and has the expected page
   count and dimensions.
2. Check font substitution, selectable text, line weights, raster sharpness, panel
   alignment, and any transparency or clipping changes introduced during export.
3. Check labels, units, ticks, legends, annotations, panel tags, and scale bars for
   overlap or truncation.
   Inspect the longest tick label, every statistical annotation and every panel
   edge. Check readability at 100% of the intended physical size, not only a zoomed
   preview; report any remaining obstruction as a failed delivery item.
4. Compare scales, coordinates, colors, and category order across related panels.
5. For color-encoded groups or values, generate PNG views with `scripts/color_preview.R`
   or an equivalent installed tool as described in `color-policy.md`. Inspect
   grayscale and color-vision-deficiency views at the same
   intended size; check actual lines, points and legends, and add a targeted cue
   when group identity becomes ambiguous.
6. Confirm plotted counts, extrema, summaries, intervals, p-values, and exclusions
   against the source files.
7. For images, confirm the field, crop, channel mapping, display range, and scale bar
   match the image-integrity block.
8. View the assembled figure at its intended placed width. Compute effective text size
   as exported size times placed/exported width. If text or evidence is unreadable,
   revise layout and dimensions together and inspect again; do not only zoom in.

Do not call the figure complete until the exported artifact passes this loop.
