library(ComplexHeatmap)
library(circlize)
library(grid)
m <- as.matrix(read.csv("input.csv", row.names = 1))
tracks <- read.csv("tracks.csv", row.names = 1)
font_pt <- 11
txt <- gpar(fontfamily = "Arial", fontsize = font_pt)
colors <- colorRamp2(c(-2, 0, 2), c("#2166AC", "#F7F7F7", "#B2182B"))
legend <- list(title_gp = txt, labels_gp = txt)
a <- Heatmap(m[, 1:5], name = "Expression", col = colors, cluster_rows = FALSE,
  cluster_columns = FALSE, row_names_side = "left", row_names_gp = txt,
  column_names_gp = txt, column_names_rot = 45, column_title = "Markers",
  column_title_gp = txt, width = unit(50, "mm"), height = unit(50, "mm"),
  heatmap_legend_param = legend)
b <- Heatmap(m[, 6:8], name = "Score", col = colors, cluster_rows = FALSE,
  cluster_columns = FALSE, column_names_gp = txt, column_names_rot = 45,
  column_title = "Pathways", column_title_gp = txt, width = unit(30, "mm"),
  show_heatmap_legend = FALSE)
anno <- rowAnnotation(
  Count = anno_barplot(tracks$count, width = unit(15, "mm"), gp = gpar(fill = "#1F78B4"),
    axis_param = list(gp = txt, at = c(0, 200), labels_rot = 0)),
  Fraction = anno_barplot(tracks$fraction, width = unit(15, "mm"), gp = gpar(fill = "#A6CEE3"),
    axis_param = list(gp = txt, at = c(0, .5), labels_rot = 0)), gap = unit(6, "mm"),
  annotation_name_gp = txt, annotation_name_rot = 45, annotation_name_offset = unit(9, "mm"))
p <- a + b + anno
saveRDS(p, "plot.rds")
cairo_pdf("preview.pdf", width = 160/25.4, height = 105/25.4, family = "Arial")
draw(p, heatmap_legend_side = "bottom", padding = unit(c(7, 5, 5, 5), "mm")); dev.off()
ragg::agg_png("preview.png", width = 160, height = 105, units = "mm", res = 300)
draw(p, heatmap_legend_side = "bottom", padding = unit(c(7, 5, 5, 5), "mm")); dev.off()
