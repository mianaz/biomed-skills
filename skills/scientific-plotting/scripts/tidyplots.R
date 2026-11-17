# Source the shared compact.R first. Each panel must have fixed dimensions.
export_tidyplots <- function(p, stem, dpi = 600, placed_width_mm = NULL,
                              formats = "png", save_object = FALSE, source_data = NULL, diagnostics = FALSE) {
  sizing <- tempfile(fileext = ".pdf")
  grDevices::cairo_pdf(sizing, width = 7, height = 7,
    symbolfamily = grDevices::cairoSymbolFont("Arial", usePUA = FALSE))
  layout <- ggplot2::ggplotGrob(p)
  flexible <- any(grid::unitType(layout$widths) == "null") ||
              any(grid::unitType(layout$heights) == "null")
  width_mm <- grid::convertWidth(sum(layout$widths), "mm", valueOnly = TRUE) + 2
  height_mm <- grid::convertHeight(sum(layout$heights), "mm", valueOnly = TRUE) + 2
  grDevices::dev.off()
  unlink(sizing)
  if (flexible) stop("export_tidyplots requires fixed panel sizes; set adjust_size() or use export_biomedical() with explicit canvas dimensions.")
  if (is.null(placed_width_mm)) placed_width_mm <- width_mm
  export_biomedical(p, stem, width_mm, height_mm,
                    placed_width_mm = placed_width_mm, dpi = dpi, formats = formats,
                    save_object = save_object, source_data = source_data, diagnostics = diagnostics)
}
