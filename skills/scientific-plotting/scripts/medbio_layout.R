# Appearance-only editions of the registered MedBioinform source scripts.
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(grid))
medbio_half_jitter <- ggproto(NULL, position_jitter(),
  compute_layer = function(self, data, params) self$compute_panel(data, params, NULL))

edit_medbio_call <- function(x) {
  if (!is.call(x)) return(x)
  name <- paste(deparse(x[[1]]), collapse = "")
  for (i in seq_along(x)[-1]) if (!identical(x[[i]], quote(expr = ))) x[i] <- list(edit_medbio_call(x[[i]]))
  if (name %in% c("rm", "pdf", "png", "tiff", "dev.off", "ggsave", "save", "write.csv"))
    return(quote(invisible(NULL)))
  if (name %in% c("element_text", "ggplot2::element_text")) {
    x$size <- quote(font_pt); x$family <- "Arial"
  }
  if (name %in% c("gpar", "grid::gpar")) {
    x$fontfamily <- "Arial"
    if ("fontsize" %in% names(x)) x$fontsize <- quote(font_pt)
  }
  if (name %in% c("geom_text", "geom_text_repel", "geom_label", "geom_label_repel", "stat_compare_means")) {
    x$size <- quote(font_pt / ggplot2::.pt); x$family <- "Arial"
  }
  if (name %in% c("Heatmap", "ComplexHeatmap::Heatmap")) {
    x$row_names_gp <- quote(gpar(fontfamily = "Arial", fontsize = font_pt))
    x$column_names_gp <- quote(gpar(fontfamily = "Arial", fontsize = font_pt))
    x$width <- quote(unit(plot_width_mm, "mm"))
    x$height <- quote(unit(plot_height_mm, "mm"))
  }
  if (name %in% c("pheatmap", "pheatmap::pheatmap")) {
    x$fontsize <- quote(font_pt); x$fontfamily <- "Arial"
    x$fontsize_row <- quote(font_pt); x$fontsize_col <- quote(font_pt)
    x$filename <- NA_character_
  }
  if (name == "corrplot") { x$tl.cex <- quote(font_pt / 12); x$cl.cex <- quote(font_pt / 12) }
  x
}

medbio_theme <- function(p) {
  if (inherits(p, "patchwork")) return(p & theme(text = element_text(family = "Arial", size = font_pt),
    plot.title = element_text(family = "Arial", size = font_pt)))
  complete <- theme_get() + p$theme
  for (role in c("text", "axis.text.x", "axis.text.y", "axis.title.x", "axis.title.y",
                 "legend.text", "legend.title", "strip.text.x", "strip.text.y", "plot.title")) {
    element <- calc_element(role, complete)
    if (inherits(element, "element_text")) {
      element$family <- "Arial"; element$size <- font_pt
      p$theme[[role]] <- element
    }
  }
  p <- p + theme(plot.margin = unit(get0("plot_margin_mm", ifnotfound = c(4, 5, 4, 5)), "mm"),
    legend.spacing.x = unit(3, "mm"))
  for (layer in p$layers) if (inherits(layer$geom, c("GeomText", "GeomLabel", "GeomTextRepel", "GeomLabelRepel"))) {
    layer$aes_params$size <- font_pt / ggplot2::.pt
    layer$aes_params$family <- "Arial"
  }
  if (any(vapply(p$scales$scales, function(s) is.language(s$name) || is.expression(s$name), logical(1))))
    p$theme$legend.title <- element_text(family = "Arial", size = 16)
  for (axis in c("x", "y")) if (is.language(p$labels[[axis]]) || is.expression(p$labels[[axis]]))
    p$theme[[paste0("axis.title.", axis)]] <- element_text(family = "Arial", size = 16)
  p
}

medbio_text <- function(g) {
  if (inherits(g, "text")) {
    g$gp$fontfamily <- "Arial"
    censor <- is.character(g$label) && all(grepl("^[ |]+$", g$label))
    if (!censor) g$gp$fontsize <- max(font_pt, g$gp$fontsize, if (is.expression(g$label)) 12 else 0)
  }
  if (length(g$grobs)) g$grobs <- lapply(g$grobs, medbio_text)
  if (length(g$children)) for (i in seq_along(g$children)) g$children[[i]] <- medbio_text(g$children[[i]])
  g
}

render_medbio <- function(source_file = "source-edited.R") {
  source("layout.R", local = .GlobalEnv)
  theme_set(theme_gray(base_size = font_pt, base_family = "Arial") +
    theme(axis.text = element_text(size = font_pt), legend.text = element_text(size = font_pt),
          strip.text = element_text(size = font_pt), plot.title = element_text(size = font_pt)))
  set.seed(1)
  dir.create("figures", showWarnings = FALSE)
  dir.create("source_data", showWarnings = FALSE)
  env <- new.env(parent = .GlobalEnv)
  grDevices::cairo_pdf("figures/source-session.pdf", width = canvas_width_mm / 25.4,
                      height = canvas_height_mm / 25.4, family = "Arial", onefile = TRUE)
  dev.control(displaylist = "enable")
  par(family = "Arial")
  expressions <- parse(source_file)
  native <- NULL
  for (expr in expressions) {
    if (is.call(expr) && as.character(expr[[1]])[1] == "pheatmap") {
      heatmap_input <- eval(expr[[2]], env)
      write.csv(heatmap_input, "source_data/heatmap-input.csv")
    }
    value <- withVisible(eval(expr, env))
    if ((value$visible || inherits(value$value, c("pheatmap", "Heatmap", "HeatmapList"))) && inherits(value$value, c("ggplot", "ggsurvplot", "grob", "pheatmap", "Heatmap", "HeatmapList"))) {
      native <- value$value
      if (inherits(native, "ggplot")) native <- medbio_theme(native)
      if (inherits(native, "pheatmap")) grid.draw(native$gtable) else print(native)
    }
  }
  recorded <- recordPlot()
  dev.off()
  if ("showtext" %in% loadedNamespaces()) showtext::showtext_auto(FALSE)
  grDevices::cairo_pdf("figures/measurement.pdf", width = 8, height = 8, family = "Arial")
  if (is.null(native)) native <- recorded
  if (inherits(native, "ggsurvplot")) {
    write.csv(native$data.survplot, "source_data/survival-curves.csv", row.names = FALSE)
    write.csv(native$data.survtable, "source_data/risk-table.csv", row.names = FALSE)
    native$plot <- medbio_theme(native$plot)
    native$table <- medbio_theme(native$table) + theme(legend.position = "none",
      axis.text.x = element_blank(), axis.ticks.x = element_blank())
    native <- cowplot::plot_grid(native$plot, native$table + labs(x = NULL), ncol = 1,
      align = "v", axis = "lr", rel_heights = c(3, 1.2))
  }
  if (exists("df_cor",env,inherits=FALSE)) write.csv(env$df_cor,"source_data/correlation-matrix.csv")
  if (inherits(native,"Heatmap")) write.csv(native@matrix,"source_data/heatmap-matrix.csv")
  if (inherits(native, "ggplot")) {
    built <- ggplot_build(native)
    saveRDS(list(data = native$data, layers = built$data), "source_data/plot-data.rds")
    for (i in seq_along(built$data)) {
      d <- built$data[[i]]
      d <- d[, !vapply(d, is.list, logical(1)), drop = FALSE]
      write.csv(d, sprintf("source_data/layer-%02d.csv", i), row.names = FALSE)
    }
    titled <- native
    native <- native + labs(title = NULL, subtitle = NULL)
    composite <- inherits(native, "patchwork") || any(vapply(native$layers,
      function(x) inherits(x$geom, c("GeomDrawGrob", "GeomCustomAnn")), logical(1)))
    g <- if (inherits(native, "patchwork")) patchwork::patchworkGrob(native) else ggplotGrob(native)
    panels <- g$layout[grepl("^panel(?:-|$)", g$layout$name), ]
    cols <- unique(panels$l); rr <- unique(panels$t)
    # Allocate enough physical space for category labels and facets before measuring the canvas.
    nx <- max(vapply(built$layout$panel_params, function(a) if (isTRUE(a$x$scale_is_discrete)) length(a$x$get_labels()) else 0L, integer(1)))
    ny <- max(vapply(built$layout$panel_params, function(a) if (isTRUE(a$y$scale_is_discrete)) length(a$y$get_labels()) else 0L, integer(1)))
    pw <- max(plot_width_mm, length(cols) * 20, nx * 4.3)
    ph <- max(plot_height_mm, length(rr) * 12, ny * 4.5)
    if (!composite) {
      for (i in grep("^guide-box", g$layout$name)) {
        guide <- g$grobs[[i]]
        if (!inherits(guide, "gtable")) next
        gw <- convertWidth(sum(guide$widths), "mm", TRUE)
        gh <- convertHeight(sum(guide$heights), "mm", TRUE)
        side <- g$layout$name[i]
        if (side %in% c("guide-box-left", "guide-box-right")) ph <- max(ph, gh)
        if (side %in% c("guide-box-top", "guide-box-bottom")) pw <- max(pw, gw)
      }
      if (length(cols)) g$widths[cols] <- unit(pw / length(cols), "mm")
      if (length(rr)) g$heights[rr] <- unit(ph / length(rr), "mm")
      canvas_width_mm <- ceiling(convertWidth(sum(g$widths), "mm", TRUE))
      canvas_height_mm <- ceiling(convertHeight(sum(g$heights), "mm", TRUE))
    }
    native <- g
    plot_width_mm <- pw; plot_height_mm <- ph
  } else if (inherits(native, "pheatmap")) {
    native <- native$gtable
    cell <- native$layout[native$layout$name == "matrix", ]
    rn <- if ("row_names" %in% native$layout$name) native$grobs[[which(native$layout$name == "row_names")]]$label else character()
    cn <- if ("col_names" %in% native$layout$name) native$grobs[[which(native$layout$name == "col_names")]]$label else character()
    native$widths[cell$l] <- unit(max(plot_width_mm, length(cn) * 4.5), "mm")
    native$heights[cell$t] <- unit(max(plot_height_mm, length(rn) * 4.5), "mm")
    canvas_width_mm <- ceiling(convertWidth(sum(native$widths), "mm", TRUE)) + 4
    canvas_height_mm <- ceiling(convertHeight(sum(native$heights), "mm", TRUE)) + 4
  }
  if (inherits(native, c("gtable", "grob"))) {
    # Nested source composites retain their panel layout; use the explicit canvas setting.
    measured_w <- convertWidth(sum(native$widths), "mm", TRUE)
    measured_h <- convertHeight(sum(native$heights), "mm", TRUE)
    canvas_width_mm <- max(canvas_width_mm, ceiling(measured_w))
    canvas_height_mm <- max(canvas_height_mm, ceiling(measured_h))
  }
  if (inherits(native, c("grob", "gtable"))) native <- medbio_text(native)
  draw <- function() {
    if (inherits(native, "recordedplot")) replayPlot(native)
    else if (inherits(native, c("Heatmap", "HeatmapList"))) ComplexHeatmap::draw(native,heatmap_legend_side="right", annotation_legend_side="right")
    else { grid.newpage(); grid.draw(native) }
  }
  dev.off()
  grDevices::cairo_pdf("figures/compact.pdf", width = canvas_width_mm / 25.4,
                      height = canvas_height_mm / 25.4, family = "Arial")
  draw(); dev.off()
  ragg::agg_png("figures/compact.png", width = canvas_width_mm, height = canvas_height_mm,
                units = "mm", res = 600, background = "white")
  draw(); dev.off()
  saveRDS(native, "plot-layout.rds")
  saveRDS(native, "plot-native.rds")
  write.csv(data.frame(font_pt, plot_width_mm, plot_height_mm, canvas_width_mm, canvas_height_mm),
            "layout-measured.csv", row.names = FALSE)
  writeLines(c(if (source_file == "source-synthetic.R")
                 "Synthetic-data demonstration of the linked MedBioinform plot. See synthetic.json for input generation and plotting adaptations."
               else "Appearance edition of the linked MedBioinform source.",
               "Installed package versions are listed below.",
               capture.output(sessionInfo())), "methods.md")
  invisible(native)
}
