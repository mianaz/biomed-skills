# Shared appearance/geometry helpers; statistics and canvas choice remain explicit.
.biomedical_palettes <- jsonlite::fromJSON(file.path(dirname(sys.frame(1)$ofile),
  "..", "assets", "palettes.json"))
biomedical_palette <- function(groups, existing = character(), control = NULL, palette = "npg") {
  groups <- unique(as.character(groups))
  stopifnot(length(groups) > 0, !anyNA(groups), all(nzchar(groups)))
  pal <- existing
  if (is.character(palette) && !is.null(names(palette))) {
    pal[names(palette)] <- palette
    pool <- .biomedical_palettes$npg
  } else if (is.function(palette)) {
    pool <- palette(length(union(groups, names(existing))))
  } else if (length(palette) == 1 && tolower(palette) %in% names(.biomedical_palettes)) {
    pool <- .biomedical_palettes[[tolower(palette)]]
  } else pool <- palette
  stopifnot(is.character(pal), is.character(pool), !anyNA(pool))
  if (length(pal)) {
    stopifnot(!is.null(names(pal)), !anyNA(names(pal)), all(nzchar(names(pal))),
              !anyDuplicated(names(pal)), !anyNA(pal))
    grDevices::col2rgb(pal)
  }
  if (!is.null(control)) {
    stopifnot(length(control) == 1, control %in% union(groups, names(pal)))
    if (!control %in% names(pal)) pal[control] <- "#666666"
  }
  added <- sort(setdiff(groups, names(pal)), method = "radix")
  if (length(added)) {
    codes <- apply(grDevices::col2rgb(pool, alpha = TRUE), 2, paste, collapse = ",")
    used <- if (length(pal)) apply(grDevices::col2rgb(pal, alpha = TRUE), 2, paste, collapse = ",") else character()
    pool <- pool[!duplicated(codes) & !codes %in% used]
    if (length(pool) < length(added)) stop("Choose a palette with enough distinct colors for the complete group set.")
    pal[added] <- head(pool, length(added))
  }
  pal
}

biomedical_theme <- function(size = 14, x_angle = 0, aspect_ratio = 1) {
  cowplot::theme_cowplot(font_size = size, font_family = "Arial") +
    ggplot2::theme(
      text = ggplot2::element_text(family = "Arial", size = size),
      axis.title = ggplot2::element_text(size = size + 1),
      axis.text = ggplot2::element_text(size = size, colour = "black"),
      axis.text.x = ggplot2::element_text(angle = x_angle,
                                        hjust = if (x_angle == 0) 0.5 else 1, vjust = 1),
      legend.text = ggplot2::element_text(size = size),
      legend.title = ggplot2::element_blank(),
      legend.position = "right", legend.direction = "vertical",
      aspect.ratio = aspect_ratio,
      legend.key.size = grid::unit(3, "mm"),
      legend.margin = ggplot2::margin(0, 0, 0, 0),
      panel.grid = ggplot2::element_blank(),
      strip.background = ggplot2::element_blank(),
      plot.title = ggplot2::element_text(size = size, face = "plain"),
      plot.subtitle = ggplot2::element_blank(),
      plot.margin = ggplot2::margin(3, 4, 3, 3))
}

p_labels <- function(p, adjusted = FALSE, missing_label = NULL,
                     nonsignificant = "hide", alpha = 0.05, show_prefix = FALSE) {
  stopifnot(is.character(nonsignificant), length(nonsignificant) == 1,
            nonsignificant %in% c("hide", "ns", "value"),
            is.numeric(alpha), length(alpha) == 1, is.finite(alpha), alpha > 0, alpha < 1)
  stopifnot(is.numeric(p), all(is.na(p) | (is.finite(p) & p >= 0 & p <= 1)))
  if (!is.null(missing_label))
    stopifnot(is.character(missing_label), length(missing_label) == 1,
              !is.na(missing_label), nzchar(missing_label))
  if (anyNA(p) && is.null(missing_label))
    stop("Declare missing_label and explain why the comparison has no P value; do not remove rows to format labels.")
  labels <- rep(if (is.null(missing_label)) NA_character_ else missing_label, length(p))
  known <- !is.na(p)
  alpha_text <- vapply(1:17, function(digits) sprintf("%.*g", digits, alpha), character(1))
  exact <- which(as.numeric(alpha_text) == alpha)
  alpha_text <- alpha_text[if (length(exact)) exact[1] else 17]
  bound <- min(1e-4, alpha)
  if (any(known)) labels[known] <- paste0(if (adjusted) "P adj. " else "P ",
    vapply(p[known], function(value) {
      if (value < bound) return(paste0("< ", if (bound == 1e-4) "0.0001" else alpha_text))
      if (value == alpha) return(paste0("= ", alpha_text))
      relation <- sign(value - alpha)
      for (digits in 2:6) {
        shown <- sprintf("%.*g", digits, value)
        if (sign(as.numeric(shown) - alpha) == relation) return(paste0("= ", shown))
      }
      paste0(if (relation < 0) "< " else if (relation > 0) "> " else "= ", alpha_text)
    }, character(1)))
  if (!show_prefix) labels[known] <- sub("^P (adj[.] )?(= )?", "", labels[known])
  if (nonsignificant != "value") labels[known & p >= alpha] <- if (nonsignificant == "hide") "" else "ns"
  names(labels) <- names(p)
  labels
}

# Bind numeric P and geometry in the same row; label-only rows remain supported.
p_brackets <- function(rows, tip = 0, text_gap = 0, size = 14,
                       p_col = NULL, adjusted = FALSE, missing_label = NULL,
                       nonsignificant = "hide", alpha = 0.05) {
  p_labels(numeric(), missing_label = missing_label, nonsignificant = nonsignificant, alpha = alpha)
  if (!is.null(p_col)) {
    stopifnot(is.character(p_col), length(p_col) == 1, p_col %in% names(rows))
    labels <- p_labels(rows[[p_col]], adjusted = adjusted, missing_label = missing_label,
                       nonsignificant = nonsignificant, alpha = alpha)
    if ("label" %in% names(rows) && !identical(as.character(rows$label), unname(labels)))
      stop("P labels disagree with their numeric comparison rows; regenerate labels from ", p_col, ".")
    rows$label <- labels
  }
  stopifnot(all(c("x1", "x2", "y", "label") %in% names(rows)), !anyNA(rows$label))
  rows <- rows[rows$label != "", , drop = FALSE]
  if (!nrow(rows)) return(list())
  list(
    ggplot2::geom_segment(data = rows, ggplot2::aes(x = x1, xend = x2, y = y, yend = y),
                          inherit.aes = FALSE, linewidth = 0.4),
    ggplot2::geom_segment(data = rows, ggplot2::aes(x = x1, xend = x1, y = y, yend = y - tip),
                          inherit.aes = FALSE, linewidth = 0.4),
    ggplot2::geom_segment(data = rows, ggplot2::aes(x = x2, xend = x2, y = y, yend = y - tip),
                          inherit.aes = FALSE, linewidth = 0.4),
    ggplot2::geom_text(data = rows,
                       ggplot2::aes(x = (x1 + x2)/2, y = y + text_gap, label = label),
                       inherit.aes = FALSE, family = "Arial", size = size,
                       size.unit = "pt", vjust = -0.25))
}

# Measure direct panel text on the actual device; page bounds miss internal clips.
panel_text_bounds <- function(p, width_mm, height_mm) {
  tmp <- tempfile(fileext = ".pdf")
  grDevices::cairo_pdf(tmp, width = width_mm / 25.4, height = height_mm / 25.4,
    symbolfamily = grDevices::cairoSymbolFont("Arial", usePUA = FALSE))
  on.exit({ grDevices::dev.off(); unlink(tmp) })
  gt <- ggplot2::ggplotGrob(p)
  grid::grid.newpage(); grid::grid.draw(gt); grid::grid.force()
  rows <- data.frame(panel = character(), label = character(), left = double(),
    right = double(), bottom = double(), top = double(), clipped = logical())
  nested <- inherits(p, "patchwork") || any(vapply(p$layers,
    function(layer) inherits(layer$geom, "GeomDrawGrob"), logical(1)))
  panels <- data.frame(panel = character(), scope = character(), width_mm = double(), height_mm = double())
  # Nested compositions and label grobs still need rendered inspection.
  for (i in grep("^panel", gt$layout$name)) {
    a <- gt$layout[i, ]
    grid::seekViewport(paste0(a$name, ".", a$t, "-", a$l, "-", a$b, "-", a$r))
    panels <- rbind(panels, data.frame(panel = a$name,
      scope = if (nested) "assembly_layout" else "data_panel",
      width_mm = grid::convertWidth(grid::unit(1, "npc"), "mm", valueOnly = TRUE),
      height_mm = grid::convertHeight(grid::unit(1, "npc"), "mm", valueOnly = TRUE)))
    for (g in gt$grobs[[i]]$children) if (inherits(g, "text")) {
      bounds <- c(
        grid::convertX(grid::grobX(g, 180), "npc", valueOnly = TRUE),
        grid::convertX(grid::grobX(g, 0), "npc", valueOnly = TRUE),
        grid::convertY(grid::grobY(g, 270), "npc", valueOnly = TRUE),
        grid::convertY(grid::grobY(g, 90), "npc", valueOnly = TRUE))
      outside <- any(bounds[c(1, 3)] < -0.001 | bounds[c(2, 4)] > 1.001)
      rows <- rbind(rows, data.frame(panel = a$name, label = paste(g$label, collapse = " | "),
        left = bounds[1], right = bounds[2], bottom = bounds[3], top = bounds[4],
        clipped = outside && identical(p$coordinates$clip, "on")))
    }
    grid::upViewport(0)
  }
  panels$height_width_ratio <- panels$height_mm / panels$width_mm
  attr(rows, "panels") <- panels
  rows
}

# PDF word-box intersections identify candidate text collisions, not text over data.
text_overlaps <- function(txt) {
  pairs <- data.frame(first = integer(), second = integer(), text = character())
  # ponytail: pair scan suits compact figures; use a spatial index for thousands of labels.
  for (i in seq_len(nrow(txt))) {
    j <- which(seq_len(nrow(txt)) > i &
      pmin(txt$x[i] + txt$width[i], txt$x + txt$width) - pmax(txt$x[i], txt$x) > 0.5 &
      pmin(txt$y[i] + txt$height[i], txt$y + txt$height) - pmax(txt$y[i], txt$y) > 1)
    if (length(j)) pairs <- rbind(pairs, data.frame(first = i, second = j,
      text = paste(txt$text[i], txt$text[j], sep = " / ")))
  }
  pairs
}

# Measure native heatmap bodies, including splits, on the active export device.
heatmap_cell_sizes <- function(drawn) {
  cells <- data.frame(heatmap = character(), row_slice = integer(), column_slice = integer(),
    width_mm = double(), height_mm = double())
  for (h in drawn@ht_list) if (inherits(h, "Heatmap")) {
    rows <- ComplexHeatmap::row_order(drawn, name = h@name)
    cols <- ComplexHeatmap::column_order(drawn, name = h@name)
    if (!is.list(rows)) rows <- list(rows)
    if (!is.list(cols)) cols <- list(cols)
    for (i in seq_along(rows)) for (j in seq_along(cols)) {
      size <- NULL
      ComplexHeatmap::decorate_heatmap_body(h@name, {
        size <- c(grid::convertWidth(grid::unit(1, "npc"), "mm", valueOnly = TRUE),
                  grid::convertHeight(grid::unit(1, "npc"), "mm", valueOnly = TRUE))
      }, row_slice = i, column_slice = j, envir = environment())
      cells <- rbind(cells, data.frame(heatmap = h@name, row_slice = i, column_slice = j,
        width_mm = size[1] / length(cols[[j]]), height_mm = size[2] / length(rows[[i]])))
    }
  }
  cells
}

# Requested exports plus one compact measurement record; source inputs stay shared.
export_biomedical <- function(p, stem, width_mm, height_mm, placed_width_mm = width_mm,
                             dpi = 600, formats = "png", save_object = FALSE,
                             source_data = NULL, diagnostics = FALSE, draw_args = list()) {
  stopifnot(width_mm > 0, height_mm > 0, placed_width_mm > 0, dpi > 0,
            is.logical(save_object), length(save_object) == 1)
  formats <- unique(tolower(formats))
  stopifnot(length(formats) > 0, all(formats %in% c("png", "pdf", "svg", "tiff")))
  is_heatmap <- inherits(p, c("Heatmap", "HeatmapList"))
  if (!is_heatmap) {
    p <- p + ggplot2::theme(plot.background = ggplot2::element_rect(fill = "white", colour = NA),
                            panel.background = ggplot2::element_rect(fill = "white", colour = NA))
    built <- ggplot2::ggplot_build(p)
    for (i in seq_along(built$data)) {
      layer <- built$data[[i]]
      fields <- intersect(c("x", "y", "xend", "yend", "ymin", "ymax", "xmin", "xmax"), names(layer))
      # Error bars draw endpoints; their unused center coordinate may be NA.
      if (inherits(p$layers[[i]]$geom, "GeomErrorbar"))
        fields <- setdiff(fields, if (isTRUE(layer$flipped_aes[1])) "x" else "y")
      for (field in fields) {
        if (anyNA(layer[[field]])) stop("Missing or scale-dropped geometry in ", field,
                                       "; resolve exclusions or limits before export.")
      }
    }
  }
  dir.create(dirname(stem), recursive = TRUE, showWarnings = FALSE)
  audit_pdf <- if ("pdf" %in% formats) paste0(stem, ".pdf") else tempfile(fileext = ".pdf")
  if (!"pdf" %in% formats) on.exit(unlink(audit_pdf), add = TRUE)
  cells <- NULL
  render <- function(file, format) {
    if (!is_heatmap) {
      device <- switch(format, pdf = grDevices::cairo_pdf, png = ragg::agg_png,
                       svg = svglite::svglite, tiff = ragg::agg_tiff)
      args <- list(filename = file, plot = p, width = width_mm, height = height_mm,
                   units = "mm", dpi = dpi, device = device, bg = "white")
      if (format == "pdf") args$symbolfamily <- grDevices::cairoSymbolFont("Arial", usePUA = FALSE)
      if (format == "tiff") args$compression <- "lzw"
      do.call(ggplot2::ggsave, args)
    } else {
      switch(format,
        pdf = grDevices::cairo_pdf(file, width = width_mm / 25.4, height = height_mm / 25.4, family = "Arial"),
        png = ragg::agg_png(file, width = width_mm, height = height_mm, units = "mm", res = dpi),
        svg = svglite::svglite(file, width = width_mm / 25.4, height = height_mm / 25.4),
        tiff = ragg::agg_tiff(file, width = width_mm, height = height_mm, units = "mm", res = dpi, compression = "lzw"))
      on.exit(grDevices::dev.off())
      drawn <- do.call(ComplexHeatmap::draw, c(list(object = p),
        utils::modifyList(list(heatmap_legend_side = "right", annotation_legend_side = "right"), draw_args)))
      if (format == "pdf") cells <<- heatmap_cell_sizes(drawn)
    }
  }
  render(audit_pdf, "pdf")
  txt <- pdftools::pdf_data(audit_pdf, font_info = TRUE)[[1]]
  page <- pdftools::pdf_pagesize(audit_pdf)[1, ]
  ratio <- placed_width_mm / (page$width * 25.4 / 72)
  effective <- txt$font_size * ratio
  collisions <- text_overlaps(txt)
  outside <- txt$x < 0 | txt$y < 0 | txt$x + txt$width > page$width | txt$y + txt$height > page$height
  if (!nrow(txt)) stop("No text recovered from the reference render; inspect the artifact.")
  if (any(!grepl("Arial", txt$font_name, ignore.case = TRUE))) stop("Reference render contains a substituted/non-Arial font.")
  if (any(txt$font_size <= 10) || any(effective <= 10)) stop("Text must exceed 10 pt at the planned placement.")
  if (any(outside)) stop("Text crosses the reference page boundary: ", paste(unique(txt$text[outside]), collapse = ", "))
  panels <- panel_text <- NULL
  if (!is_heatmap) {
    panel_text <- panel_text_bounds(p, width_mm, height_mm)
    panels <- attr(panel_text, "panels")
    if (any(panel_text$clipped)) stop("Text is clipped inside a panel: ", paste(panel_text$label[panel_text$clipped], collapse = "; "))
    if (any(panels$scope == "data_panel" & panels$height_width_ratio < .8)) warning("Review short data panels against the reading task.")
  } else {
    cells$placed_width_mm <- cells$width_mm * placed_width_mm / width_mm
    cells$placed_height_mm <- cells$height_mm * placed_width_mm / width_mm
    if (any(cells$placed_width_mm < 8 - .01 | cells$placed_height_mm < 8 - .01))
      stop("Heatmap cells must be at least 8 mm at final placement; increase body dimensions or split the view.")
    if (any(abs(cells$width_mm / cells$height_mm - 1) > .01)) stop("Heatmap cells must be square.")
  }
  for (format in setdiff(formats, "pdf")) render(paste0(stem, ".", format), format)
  if (save_object) saveRDS(if (is_heatmap) list(heatmap = p, draw_args = draw_args) else p, paste0(stem, ".rds"))
  if (diagnostics) {
    write.csv(transform(txt, placed_pt = effective), paste0(stem, "_pdf_text.csv"), row.names = FALSE)
    write.csv(collisions, paste0(stem, "_text_overlaps.csv"), row.names = FALSE)
    if (!is_heatmap) {
      write.csv(panels, paste0(stem, "_panel_layout.csv"), row.names = FALSE)
      write.csv(panel_text, paste0(stem, "_panel_text.csv"), row.names = FALSE)
    }
  }
  files <- paste0(stem, ".", formats)
  report <- list(schema = "biomed-export-1", files = I(basename(files)),
    export_mm = c(width_mm, height_mm), placed_width_mm = placed_width_mm, dpi = dpi,
    source_data = source_data, object_saved = save_object,
    font_check = list(source = if ("pdf" %in% formats) "delivered PDF" else "temporary PDF",
      fonts = I(unique(txt$font_name)), min_native_pt = min(txt$font_size),
      min_effective_pt = min(effective), text_runs = nrow(txt), page_bounds_pass = TRUE),
    panels = panels, heatmap_cells = cells, candidate_text_overlaps = nrow(collisions),
    manual_review = "Inspect final exports for text over data, glyphs and scientific meaning.")
  jsonlite::write_json(report, paste0(stem, "_export.json"), auto_unbox = TRUE, pretty = TRUE, digits = 8)
  if (nrow(collisions)) warning("Candidate text overlaps; inspect the saved figure or request diagnostics = TRUE.")
  message("Export checks passed; inspect the requested ", paste(formats, collapse = "/"), " at final size.")
  invisible(p)
}
