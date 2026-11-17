# Heatmap meaning, order and normalization

Select a heatmap when joint matrix patterns answer the question; use the
[task-to-chart table](visual-design.md#match-the-reading-task) first. For rendering,
use [ComplexHeatmap](complexheatmap.md), square tiles and native guides. Save the
exact displayed matrix, transformation, color limits and final row/column order.

## Choose the order for the question

Preserve intrinsic time, dose, genomic or biological order. Cluster an axis when
similarity is the question; record the distance and linkage method. In a dendrogram,
branch rotations can change leaf order without changing the hierarchy. Interpret
similarity through the defined tree distances, rather than neighboring row positions
alone. Use the same ordering and color mapping across comparable conditions.

Standardize or cap values only when the analysis and intended comparison call for
it. Preserve uncapped values and state any display saturation. A row-wise z-score
shows a within-row pattern; it changes the quantity compared across rows. A few
profiles whose exact peaks or differences matter may be clearer on a position scale.
See [Heat maps](https://doi.org/10.1038/nmeth.1902) for the source examples.

## Marker blocks when type-specific expression is the question

For a type × marker matrix, a diagonal block order can expose which type each
marker favors. Keep types in the selected biological order, then sort genes by
peak type. This is one task-specific ordering, rather than a default for all matrices.
The published examples use particular standardizations/caps; retain those choices
for replication and select the transformation explicitly for new data.
Sources: [Popescu et al.](https://doi.org/10.1038/s41586-019-1652-y),
[Cao et al.](https://doi.org/10.1126/science.aba7721).

```r
# display_mat: types × genes, using the chosen analysis transformation.
# All entries are finite; exclude/resolve undefined profiles before ordering.
owner <- apply(display_mat, 2, which.max)
gene_order <- order(owner, -apply(display_mat, 2, max))
owner_block <- factor(rownames(display_mat)[owner[gene_order]],
                      levels = rownames(display_mat))
display_mat <- display_mat[, gene_order, drop = FALSE]
# Use column_split = owner_block, cluster_rows/columns = FALSE,
# cluster_column_slices = FALSE when preserving these blocks in Heatmap().
```

Save the order and reuse it if a requested companion plot represents the same
matrix. Use the same quantity and color mapping in both views.

## Significance overlays only when requested

Keep the default free of cell text. For an explicitly requested overlay, align the
supplied P-value matrix by row and column names and define the threshold/adjustment
rule in the caption. Use ComplexHeatmap's native `cell_fun` or `layer_fun` hook for
marks, with Arial and the shared effective-size and fill-luminance contrast rules.
Keep the complete statistics table. Source example:
[10.1126/science.adz2742](https://doi.org/10.1126/science.adz2742).

## Cross-validation confusion matrix

Specify which axis contains predictions, which contains actual classes, and which
conditional proportion is needed. For **rows = predicted, columns = actual**,
normalize each actual-class column to show recall/self-recovery on the diagonal.
Row normalization instead gives precision on that diagonal. Keep class counts and
held-out predictions, including the evaluation unit, with the normalized matrix.

```r
library(ComplexHeatmap)
library(circlize)
library(grid)

# counts: nonnegative held-out counts, rows = predicted, columns = actual.
# ord: class names in the same chosen biological order on both axes.
counts <- counts[ord, ord, drop = FALSE]
actual_n <- colSums(counts)
recall <- sweep(counts, 2, replace(actual_n, actual_n == 0, NA_real_), "/")
write.csv(counts, "cv_confusion_counts.csv")
write.csv(recall, "cv_confusion_recall.csv")

# Example sequential scale: white = 0, blue = 1; missing actual classes stay NA.
col_fun <- colorRamp2(c(0, 0.5, 1), c("#F7F7F7", "#92C5DE", "#2166AC"))
ht <- Heatmap(recall, name = "Fraction",
  col = col_fun, na_col = "#D9D9D9",
  cluster_rows = FALSE, cluster_columns = FALSE,
  width = unit(length(ord) * 8, "mm"),
  height = unit(length(ord) * 8, "mm"),
  row_title = "Predicted", column_title = "Actual",
  row_names_side = "left", column_names_rot = 45,
  row_title_gp = gpar(fontfamily = "Arial", fontsize = 12, fontface = "plain"),
  column_title_gp = gpar(fontfamily = "Arial", fontsize = 12, fontface = "plain"),
  row_names_gp = gpar(fontfamily = "Arial", fontsize = 12),
  column_names_gp = gpar(fontfamily = "Arial", fontsize = 12),
  heatmap_legend_param = list(at = c(0, 0.5, 1),
    title_gp = gpar(fontfamily = "Arial", fontsize = 12, fontface = "plain"),
    labels_gp = gpar(fontfamily = "Arial", fontsize = 12)))
draw(ht, heatmap_legend_side = "right")
```

Each nonempty actual-class column sums to one. The legend describes the fraction
of each actual class assigned to a predicted class; the diagonal is class recall.
A class with no actual observations has undefined recall and stays visibly missing.
Save this definition in the caption. Use the template's native export and sizing
workflow; the dimensions above set the matrix body, not the complete canvas.

A requested F1 comparison against a label-permutation null can accompany this view
when it addresses the evaluation question. Keep its valid upstream resampling and
prediction results. Classifier separation supports the evaluated distinction;
biological identities require their own evidence. Source example:
[Cao et al.](https://doi.org/10.1126/science.aba7721).
