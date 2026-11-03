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

Start with that template's code and settings: engine, panel dimensions, bar widths,
spacing, axes, native guides and typography. Replace data and labels, then change
only what the new data or current preferences require. Do not rebuild a familiar
chart from generic defaults when a compatible reviewed template is available.
Record the template ID/path and the few material changes in the figure notes.
A selected original, recovered source and reviewed adaptation are distinct states;
retain the catalog's actual review status. If no compatible reviewed source is
available, state that specific gap briefly and use the closest suitable source or
a minimal new plot. Do not block completion or relabel an unreviewed plot as approved.

## Native legends: inside, then right

Use ggplot2's native scales, `guides()` and `theme()` for ggplot/tidyplots legends.
Place the key in unused space inside the panel when it fits without covering data,
intervals or annotations. Otherwise use a vertical key on the right. Do not default
to a bottom horizontal key or draw a replacement legend with a separate plot,
manual swatches or text. Keep a shared native legend only when assembly needs it.
Remove a redundant key when the axis already identifies the same groups.

## Preserve plot height

Judge the data panel, excluding axes, labels and legends. For ordinary vertical
bars and small-group comparisons, require width <= height by default: start near
50 x 50 mm and narrow to roughly 30–40 x 45–55 mm when the groups fit. Preserve
vertical room for observations, error bars and statistics. Start from the reviewed
bar width and group spacing; reducing height is not a way to make the panel compact.
Use `theme(aspect.ratio = height / width)` for an ordinary ggplot panel or explicit
`adjust_size(width = ..., height = ..., unit = "mm")` with tidyplots. Allow a
scientifically required shape for long time series, horizontal forests or images;
record that reason briefly. Never distort data coordinates to force a square.

## Square heatmap tiles, no numeric overlay

Use ComplexHeatmap for new heatmaps. Choose one physical tile size and set the
matrix body to `ncol(mat) * tile_mm` by `nrow(mat) * tile_mm`; add the total split
gaps to the corresponding dimensions. The full heatmap can therefore be rectangular
while its individual tiles stay square. Put names, annotations and a right-side
color key outside this matrix body. Do not compress rows to fit a wide short canvas.
For a large matrix, split coherent blocks or use a larger/overview view as needed.

Do not print values or significance symbols in tiles by default. Use overlays
only when explicitly requested or when they are the specified quantitative readout.
Retain the exact matrix as source data. Ordinary heatmaps use color and their
native key to show values.

## Keep color work proportionate

Reuse the selected template/project mapping; otherwise use Paired for categories
and RdBu for continuous data. Keep category identities and meaningful scale limits
consistent. Do not run a separate palette audit, grayscale/CVD simulation, color
comparison sheet or color-approval step unless the user explicitly requests it.
Normal inspection of the saved figure remains part of delivery.
