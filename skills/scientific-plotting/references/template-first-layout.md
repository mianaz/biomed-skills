# Reviewed templates and plotting defaults

Apply these defaults to new figures and requested redesigns. Explicit user choices
and exact source replication take precedence. Appearance-only edits retain their
requested scope. These rules govern new adaptations even when an older example
uses another legend location or geometry.

## Start from a reviewed template

Before drawing a new figure, select a compatible template we have reviewed, using
the supplied template or the suite's curated template/source catalog. Inspect its
actual rendered figure and editable source. Match the scientific comparison,
independent unit, pairing and required inputs before choosing by appearance.
Check the reading task in [visual-design.md](visual-design.md#match-the-reading-task)
before selecting the retrieval category. In the selection reason, state which
visible position, interval or pattern answers the question directly.

Start with that template's code and settings: engine, panel dimensions, bar widths,
spacing, axes, native guides and typography. Replace data and labels, then change
only what the new data or current preferences require. Do not rebuild a familiar
chart from generic defaults when a compatible reviewed template is available.
Record the template ID/path and the few material changes in the figure notes.
A selected original, recovered source and reviewed adaptation are distinct states;
retain the catalog's actual review status. If no compatible reviewed source is
available, state that specific gap briefly and use the closest suitable source or
a minimal new plot. Do not block completion or relabel an unreviewed plot as approved.

## Prefer native controls and data-driven layout

Use the plotting engine's parameters and established extension functions first:
ggplot2/tidyplots stats, scales, positions, guides and facets; ggh4x for extended
axes/facets, ggrepel for data labels, and gridExtra/cowplot for layout when needed.
Let these functions derive positions from the current data and group identities.
Use named mappings and native controls for tick selection, label placement,
intervals, statistical annotation lanes and panel sizing. Pass precomputed results
to an annotation function when inference has already been calculated.

Keep scientific choices and style parameters explicit, including contrasts, units,
reference values, palette and physical sizes. Derive data-dependent coordinates,
ranges and label positions from the current inputs; avoid fixed numeric positions,
row-number group assignments and dataset-specific patches. Keep legends in native
guides, group headings in axes/facets and precomputed comparisons in annotation
layers such as `ggsignif::geom_signif()` or `ggpubr::stat_pvalue_manual()`.
Use data-linked label functions only for labels the reading task needs.
Unless explicitly requested, do not add floating `text`/`annotate`/`draw_label`
elements above or below the completed plot, fake a key with swatches and text, or
use the custom `p_brackets()` helper. Move explanatory prose to the separate
caption; if a native layout cannot fit, simplify the labels or revise that layout.
Keep custom annotation geometry only for an explicit user request or exact source
replication, and record that scope.
When adaptability is part of the task, change the value range or category order
and rerun the same plotting code to check those mappings and positions.

For source replication, keep the published title text, coloured title strips,
mathematical notation, statistical labels, palette and shared-axis arrangement.
Prefer `ggh4x::strip_themed()` for coloured facets, ggpubr's statistical annotation
layers for correlations/comparisons, patchwork's axis/guide collection for shared
layouts, and ComplexHeatmap annotations for matrix tracks. Retain the author's
native implementation when suitable. Store source wording and colour mappings as
named input metadata; compute statistics and annotation positions from the data.
Record any required manual layout exception. A successful render alone does not
approve source fidelity; compare these features against the published panel.

## Native legends: inside, then right

Use ggplot2's native scales, `guides()` and `theme()` for ggplot/tidyplots legends.
Place the key in unused space inside the panel when it fits without covering data,
intervals or annotations. Otherwise use a vertical key on the right. Do not default
to a bottom horizontal key or draw a replacement legend with a separate plot,
manual swatches or text. Keep a shared native legend only when assembly needs it.
Remove a redundant key when the axis already identifies the same groups.

## Preserve plot height

Apply the [shared canvas and aspect rules](../../biomed-shared/visual-standards.md#2-physical-space-and-panel-dimensions).
Start an ordinary ggplot data panel with `theme(aspect.ratio = 1)`; a narrow group
comparison can use a larger height/width ratio. Keep the reviewed mark widths and
group spacing. For tidyplots on a fixed full canvas, use
`adjust_size(width = NA, height = NA)` after styling, retain the chosen panel
aspect, and pass full dimensions to `export_biomedical()`.
Use explicit panel sizes only when the layout needs them, then measure the whole
export with `export_tidyplots()`. Its measured result is not a 50 mm canvas promise.
Inspect panel dimensions in `*_panel_layout.csv` and the saved view. A height/width
ratio below 0.8 flags a potentially flat panel for review, not an automatic failure
for a horizontal forest or other justified geometry. Reflow facets or move the
native guide before compressing height. Never distort data coordinates to force a square.

## Square heatmap tiles, no numeric overlay

Use ComplexHeatmap for new heatmaps. Choose one physical tile size and set the
matrix body to `ncol(mat) * tile_mm` by `nrow(mat) * tile_mm`, with cells at least
8 mm at final placement; add the total split
gaps to the corresponding dimensions. The full heatmap can therefore be rectangular
while its individual tiles stay square. Put names, annotations and a right-side
color key outside this matrix body. Do not compress rows to fit a wide short canvas.
For a large matrix, split coherent blocks or use a larger/overview view as needed.

Do not print values or significance symbols in tiles by default. Use overlays
only when explicitly requested or when they are the specified quantitative readout.
Retain the exact matrix as source data. Ordinary heatmaps use color and their
native key to show values.

## Keep color work proportionate

Use [color policy](color-policy.md) to resolve user choices, project mappings
and suitable new categorical or continuous scales. Keep category identities and meaningful scale limits
consistent. Do not run a separate palette audit, grayscale/CVD simulation, color
comparison sheet or color-approval step unless the user explicitly requests it.
Normal inspection of the saved figure remains part of delivery.

## Statistical content and exports

Heatmaps omit statistical and extra effect-size annotations unless requested.
For inferential comparison plots, apply [statistics](statistics.md) to the primary
comparison, including a nonsignificant result when that is the outcome. Descriptive
comparisons use the descriptive branch of that reference. Follow [delivery](figure-delivery.md)
for the default 600 dpi PNG, optional additional formats, numeric-only P labels, caption-based n and
nonredundant titles without subtitles.
