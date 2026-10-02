# Shared appearance/geometry helpers; statistics and canvas choice remain explicit.
biomedical_palette <- function(groups, existing = character(), control = NULL) {
  groups <- unique(as.character(groups))
  stopifnot(length(groups) > 0, !anyNA(groups), all(nzchar(groups)),
            is.character(existing))
  if (length(existing)) {
    stopifnot(!is.null(names(existing)), !anyNA(names(existing)),
              all(nzchar(names(existing))), !anyDuplicated(names(existing)),
              !anyNA(existing))
    grDevices::col2rgb(existing)
  }
  if (!is.null(control)) {
    control <- as.character(control)
    stopifnot(length(control) == 1, !is.na(control),
              control %in% c(groups, names(existing)))
  }
  pal <- existing
  if (!is.null(control) && !control %in% names(pal)) pal[control] <- "#666666"
  added <- sort(setdiff(groups, names(pal)), method = "radix")
  if (length(added)) {
    pool <- c("#7F3C8D", "#11A579", "#3969AC", "#F2B701", "#E73F74", "#80BA5A",
              "#E68310", "#008695", "#CF1C90", "#F97B72", "#A5AA99")
    codes <- apply(grDevices::col2rgb(pool), 2, paste, collapse = ",")
    used <- if (length(pal)) apply(grDevices::col2rgb(pal), 2, paste, collapse = ",") else character()
    pool <- pool[!duplicated(codes) & !codes %in% used]
    if (length(pool) < length(added))
      stop("Supply an explicit larger named palette and additional visual encoding.")
    pal[added] <- head(pool, length(added))
  }
  pal
}

biomedical_theme <- function(size = 14, x_angle = 0) {
  cowplot::theme_cowplot(font_size = size, font_family = "Arial") +
    ggplot2::theme(
      text = ggplot2::element_text(family = "Arial", size = size),
      axis.title = ggplot2::element_text(size = size + 1),
      axis.text = ggplot2::element_text(size = size, colour = "black"),
      axis.text.x = ggplot2::element_text(angle = x_angle,
                                        hjust = if (x_angle == 0) 0.5 else 1, vjust = 1),
      legend.text = ggplot2::element_text(size = size),
      legend.title = ggplot2::element_blank(),
      legend.key.size = grid::unit(3, "mm"),
      legend.margin = ggplot2::margin(0, 0, 0, 0),
      panel.grid = ggplot2::element_blank(),
      strip.background = ggplot2::element_blank(),
      plot.title = ggplot2::element_blank(),
      plot.subtitle = ggplot2::element_blank(),
      plot.margin = ggplot2::margin(3, 4, 3, 3))
}

p_labels <- function(p, adjusted = FALSE, missing_label = NULL,
                     nonsignificant = "hide", alpha = 0.05) {
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
  # Nested compositions and label grobs still need rendered inspection.
  for (i in grep("^panel", gt$layout$name)) {
    a <- gt$layout[i, ]
    grid::seekViewport(paste0(a$name, ".", a$t, "-", a$l, "-", a$b, "-", a$r))
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

# Export geometry once, then check the saved artifact. This does not replace viewing it.
export_biomedical <- function(p, stem, width_mm, height_mm, placed_width_mm = 90) {
  stopifnot(width_mm > 0, height_mm > 0, placed_width_mm > 0)
  p <- p + ggplot2::theme(plot.background = ggplot2::element_rect(fill = "white", colour = NA),
                          panel.background = ggplot2::element_rect(fill = "white", colour = NA))
  built <- ggplot2::ggplot_build(p)
  for (layer in built$data) {
    for (field in intersect(c("x", "y", "xend", "yend", "ymin", "ymax"), names(layer))) {
      if (anyNA(layer[[field]])) stop("Missing or scale-dropped geometry in ", field,
                                     "; resolve exclusions or limits before export.")
    }
  }
  dir.create(dirname(stem), recursive = TRUE, showWarnings = FALSE)
  saveRDS(p, paste0(stem, ".rds"))
  ggplot2::ggsave(paste0(stem, ".pdf"), p, width = width_mm, height = height_mm,
                  units = "mm", device = grDevices::cairo_pdf, bg = "white",
                  symbolfamily = grDevices::cairoSymbolFont("Arial", usePUA = FALSE))
  ggplot2::ggsave(paste0(stem, ".png"), p, width = width_mm, height = height_mm,
                  units = "mm", dpi = 300, device = ragg::agg_png, bg = "white")
  txt <- pdftools::pdf_data(paste0(stem, ".pdf"), font_info = TRUE)[[1]]
  page <- pdftools::pdf_pagesize(paste0(stem, ".pdf"))[1, ]
  effective <- txt$font_size * placed_width_mm / (page$width * 25.4 / 72)
  write.csv(transform(txt, placed_pt = effective), paste0(stem, "_pdf_text.csv"), row.names = FALSE)
  collisions <- text_overlaps(txt)
  write.csv(collisions, paste0(stem, "_text_overlaps.csv"), row.names = FALSE)
  if (nrow(collisions)) warning("Overlapping PDF text boxes; inspect and resolve: ",
                                paste(unique(collisions$text), collapse = "; "))
  outside <- txt$x < 0 | txt$y < 0 | txt$x + txt$width > page$width | txt$y + txt$height > page$height
  if (!nrow(txt)) stop("No text recovered from exported PDF; inspect the artifact.")
  if (any(!grepl("Arial", txt$font_name, ignore.case = TRUE)))
    stop("Saved PDF contains a substituted/non-Arial font; inspect *_pdf_text.csv.")
  if (any(txt$font_size <= 10)) stop("Exported text at or below 10 pt: ",
                                     paste(unique(txt$text[txt$font_size <= 10]), collapse = ", "),
                                     ". Check subscripts/plotmath as well as the theme.")
  if (any(effective <= 10)) stop("At the planned ", placed_width_mm, "-mm placement, minimum text is ",
                                 round(min(effective), 1), " pt. Increase text or compact the layout; do not enlarge the canvas alone.")
  if (any(outside)) stop("Text crosses the PDF page boundary: ",
                         paste(unique(txt$text[outside]), collapse = ", "))
  panel_text <- panel_text_bounds(p, width_mm, height_mm)
  write.csv(panel_text, paste0(stem, "_panel_text.csv"), row.names = FALSE)
  if (any(panel_text$clipped)) stop("Text is clipped inside a panel: ",
    paste(panel_text$label[panel_text$clipped], collapse = "; "),
    ". Reserve space for the whole label above its bracket; changing clip alone does not reserve space.")
  message("Size/boundary checks passed; ", nrow(collisions),
          " candidate text overlaps; ", nrow(panel_text), " direct panel-text groups checked. ",
          "View the saved PNG/PDF for text over data, nested/axis clipping and evidence fidelity.")
  invisible(p)
}
