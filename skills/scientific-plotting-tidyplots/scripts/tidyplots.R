# Source the shared compact.R first. Each panel must have fixed dimensions.
export_tidyplots <- function(p, stem, dpi = 600) {
  sizing <- tempfile(fileext = ".pdf")
  grDevices::cairo_pdf(sizing, width = 7, height = 7,
    symbolfamily = grDevices::cairoSymbolFont("Arial", usePUA = FALSE))
  layout <- ggplot2::ggplotGrob(p)
  width_mm <- grid::convertWidth(sum(layout$widths), "mm", valueOnly = TRUE) + 2
  height_mm <- grid::convertHeight(sum(layout$heights), "mm", valueOnly = TRUE) + 2
  grDevices::dev.off()
  unlink(sizing)
  export_biomedical(p, stem, width_mm, height_mm,
                    placed_width_mm = width_mm, dpi = dpi)
}
