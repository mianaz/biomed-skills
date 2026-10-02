# Single-cell and spatial figure recipes

Use these recipes for visualization only. The applicable single-cell or spatial skill
must supply the processed object, analysis choices, statistics, and biological
interpretation.

## Implementation map

| Figure | R-first implementation | Method-native carve-out |
|---|---|---|
| UMAP/t-SNE/PCA groups | Seurat or `scop`; custom layers with `ggplot2` | Scanpy embedding plot |
| Feature/module score map | Seurat/`scop` with fixed limits | Scanpy or model-native feature plot |
| Marker dot/violin plot | Seurat/`scop`, or `ggplot2` from a tidy summary | Python object-native plot if values are exported |
| Group/matrix heatmap | `ComplexHeatmap`, `pheatmap`, or tidy tiles | Native matrix plot when transformation is exposed |
| Velocity/fate/trajectory | Plot supplied coordinates/curves; `ggplot2` for restyle | scVelo, CellRank, or method-native plot is canonical |
| Spatial expression/composition | Seurat/`scop` or `ggplot2` over supplied coordinates | Platform-native spatial plotting |
| Integration/benchmark diagnostics | R result-table plot | scIB or integration-tool native summary |

Always inspect the installed help for package-specific arguments. Do not copy API
spelling from a similarly named package or fork.

## Embeddings

- Recolor the same stored coordinates for comparisons across condition, tissue,
  species, or annotation. Do not recompute one embedding per subset and present the
  panels as geometrically comparable.
- Use identical axis limits and aspect ratio across related panels. State when panels
  use different embeddings.
- Bind cell-type colors by name and retain one canonical cell-type order across the
  embedding, dotplot, heatmap, legend, and source tables.
- Reduce point size with cell count. For very large objects, rasterize points only;
  keep axes, labels, trajectories, and legends vector.
- Draw contextual cells first in light gray and focal cells last when highlighting a
  subset. Record the highlight rule and do not hide excluded populations.
- Label only groups that remain readable. For many populations, use coarse labels,
  direct numbered labels plus a separate key, or small multiples rather than a dense
  cloud of overlapping names.
- Export `cell_id`, displayed coordinates, displayed group, feature/score when used,
  inclusion flag, and any facet/highlight field.

## Feature maps and density

- Use shared color limits when comparing the same feature across groups. If limits
  differ, make that visually explicit and do not imply direct color comparison.
- Distinguish zero, missing, and below-display-threshold values. Do not map all three
  silently to the same color.
- Control draw order so high values are not systematically hidden, while avoiding a
  sort order that visually exaggerates rare signal. Density, hexbin, or contours are
  often clearer than opaque overplotting.
- For a marker panel, group genes by biological compartment and keep a shared feature
  order rather than making one giant unordered grid.

## Dotplots, violins, and heatmaps

- State what dot size and color encode. Export the group-by-feature table containing
  both displayed quantities, group cell counts, and the final order.
- Use violins/boxes for distribution shape only when cell-level distributions answer
  the display question; do not make cells look like independent biological replicates.
- Save the exact heatmap matrix after any visualization-only scaling or capping, plus
  the row/column order and annotations.
- Cluster only axes whose order is genuinely exploratory. Preserve fixed biological,
  lineage, temporal, or confusion-matrix order.
- Use a sequential scale for magnitude and a centered diverging scale only for signed
  deviation. Label the transformation and center.

## Composition and abundance displays

- Keep sample identity visible when the scientific unit is the sample. Per-sample
  bars or points reveal variation that a pooled-cell stack hides.
- A stacked bar communicates composition, not evidence of a condition effect. Add
  only the replicate-aware result supplied by the abundance-analysis workflow.
- For many cell types, use grouped small multiples, selected lineages, or an alluvial
  display with a readable key rather than a pinstripe stack.
- Export sample, group, cell type, count, denominator, displayed fraction, inclusion
  status, and the validated statistical annotation table when present.

## Trajectory, velocity, and fate

- Preserve the method-native geometry when arrows, streamlines, transition
  probabilities, or fate curves depend on fitted model state.
- Distinguish computed vectors/curves from hand-drawn explanatory arrows in the panel
  note and caption. Never present a decorative arrow as a model output.
- Keep the underlying embedding, trajectory coordinates, pseudotime/fate values, and
  displayed feature trends in source data.
- Use the same branch and cell-state colors across trajectory, trend, and heatmap
  panels.

## Spatial and image-linked panels

- Preserve tissue orientation and aspect ratio. Include a calibrated scale bar where
  spatial distance is meaningful.
- Use comparable color limits for panels intended for direct comparison. State any
  per-section normalization or rescaling supplied by the analysis.
- Keep histology/fluorescence display adjustments global and record them in the image
  integrity block. Do not selectively clean individual spots or regions.
- Export displayed coordinates, section/region identity, values or proportions, and
  inclusion status; link them to the displayed image field.

## Main versus supplement

Main panels usually show the cell states, spatial pattern, condition effect, or
biological trajectory that answers the primary question. Put preprocessing QC,
doublet/ambient-RNA diagnostics, integration scorecards, parameter sweeps, annotation
concordance, dense full marker atlases, and method benchmarks in the supplement unless
technical validity or method performance is itself the central claim.

This placement rule is not permission to hide uncertainty: retain the supporting
panel and link it clearly from the main claim.
