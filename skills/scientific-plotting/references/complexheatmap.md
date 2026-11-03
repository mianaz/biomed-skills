# ComplexHeatmap: square tiles and native legends

Use ComplexHeatmap for new heatmaps. Start from a reviewed compatible template
and preserve its matrix transformation, ordering and annotation definitions.
Apply [template and layout defaults](template-first-layout.md): square tiles,
no numeric/significance overlay by default, and a native right-side color key.

For an unsplit matrix, set physical body dimensions from one tile size:

```r
library(ComplexHeatmap)
library(circlize)
library(grid)

tile_mm <- 5
ht <- Heatmap(mat, name = "Value",
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

Supply `col_fun` from the chosen template or a RdBu scale appropriate to the
measured quantity. Preserve its clustering choices; make those explicit in the
adapted call. Do not standardize, cap or cluster the matrix solely to improve its
appearance. Save the exact displayed matrix and its row/column order.

For row/column splits, add total gap widths/heights to the matrix-body dimensions:
`width = ncol(mat) * tile_mm + total_column_gap_mm`, and equivalently for height.
Allocate additional canvas space for row/column names, dendrograms, annotations
and the right-side key. Do not set an arbitrary wide, short export size that
squeezes matrix rows. Use the same `ht` and drawing settings for PDF and PNG.

`rowAnnotation()` and `HeatmapAnnotation()` add categorical or quantitative side
annotations. Use `row_split`/`column_split` when the scientific grouping requires
blocks. Add `cell_fun`/`layer_fun` text only for an explicitly requested overlay.
