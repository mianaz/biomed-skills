# ComplexHeatmap: square tiles and native legends

Use ComplexHeatmap for new heatmaps. Start from a reviewed compatible template
and preserve its matrix transformation, ordering and annotation definitions.
Apply [template and layout defaults](template-first-layout.md): square tiles,
no numeric/significance overlay by default, and a native right-side color key.
Cells must remain at least 8 × 8 mm after final placement. Set
`tile_mm >= 8 / placement_scale`; use `placement_scale = placed_width_mm / width_mm`.
For a large matrix, split/page the display instead of shrinking its cells.

For an unsplit matrix, set physical body dimensions from one tile size:

```r
library(ComplexHeatmap)
library(circlize)
library(grid)

tile_mm <- 8 # same-size placement; increase for a smaller placed width
# mat is an already validated gene-wise z-score matrix in this example.
ht <- Heatmap(mat, name = "Gene expression\n(z-score)",
  col = col_fun, # reuse the template's mapping and limits for this quantity
  width = unit(ncol(mat) * tile_mm, "mm"),
  height = unit(nrow(mat) * tile_mm, "mm"),
  row_names_gp = gpar(fontfamily = "Arial", fontsize = 12),
  column_names_gp = gpar(fontfamily = "Arial", fontsize = 12),
  heatmap_legend_param = list(direction = "vertical",
    title_gp = gpar(fontfamily = "Arial", fontsize = 12),
    labels_gp = gpar(fontfamily = "Arial", fontsize = 12)))
draw(ht, heatmap_legend_side = "right", annotation_legend_side = "right")
```

Supply `col_fun` from the project/user mapping or a scale suited to the
quantity under [color policy](color-policy.md). Preserve its clustering choices; make those explicit in the
adapted call. Do not standardize, cap or cluster the matrix solely to improve its
appearance. Save the exact displayed matrix and its row/column order.
For ordering decisions, marker displays, requested significance overlays or confusion
matrices, read [heatmaps.md](heatmaps.md).

For row/column splits, add total gap widths/heights to the matrix-body dimensions:
`width = ncol(mat) * tile_mm + total_column_gap_mm`, and equivalently for height.
Allocate additional canvas space for row/column names, dendrograms, annotations
and the right-side key. Do not set an arbitrary wide, short export size that
squeezes matrix rows. Use the shared exporter with the same `ht` and drawing
settings for requested formats. It measures native bodies, including splits,
and rejects nonsquare cells or cells below 8 mm at placement:

```r
source("scripts/compact.R")
export_biomedical(ht, "figures/expression", width_mm, height_mm,
  placed_width_mm = width_mm, source_data = "source_data/expression_z.csv")
# Default: 600 dpi PNG + compact audit record. Object and other formats are optional.
```

Use a biological color-key title that describes the actual matrix; put the exact
scaling axis, reference samples and any capping in the caption/source metadata.
The exporter does not change the matrix or choose its transformation.

`rowAnnotation()` and `HeatmapAnnotation()` add categorical or quantitative side
annotations. Use `row_split`/`column_split` when the scientific grouping requires
blocks. Add `cell_fun`/`layer_fun` text only for an explicitly requested overlay.
