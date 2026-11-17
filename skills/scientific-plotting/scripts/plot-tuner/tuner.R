library(grid)

# Keep this helper beside the plotting script, or source it from the skill.
tuner_walk <- function(g, visit, path = "root") {
  if (inherits(g, "text")) g <- visit(g, path)
  for (slot in c("grobs", "children")) {
    for (i in seq_along(g[[slot]])) {
      g[[slot]][[i]] <- tuner_walk(g[[slot]][[i]], visit,
                                  paste0(path, ".", substr(slot, 1, 1), i))
    }
  }
  g
}

tuner_number <- function(x, fallback = 0) {
  value <- suppressWarnings(as.numeric(sub("[^0-9.eE+-].*$", "", x)))
  if (!length(value) || is.na(value)) fallback else value
}

tuner_style <- function(node, patch = list()) {
  fields <- strsplit(xml2::xml_attr(node, "style") %||% "", ";", fixed = TRUE)[[1]]
  fields <- fields[grepl(":", fields, fixed = TRUE)]
  style <- as.list(setNames(trimws(sub("^[^:]+:", "", fields)), trimws(sub(":.*$", "", fields))))
  style <- modifyList(style, patch)
  xml2::xml_set_attr(node, "style", paste(paste0(names(style), ":", unlist(style)), collapse = ";"))
  invisible(style)
}
`%||%` <- function(x, y) if (is.null(x) || (length(x) == 1 && is.na(x))) y else x

tuner_model <- function(doc, prefix, owners = list()) {
  nodes <- xml2::xml_find_all(doc, ".//*[not(ancestor::*[local-name()='defs' or local-name()='clipPath' or local-name()='mask' or local-name()='marker' or local-name()='pattern']) and (local-name()='text' or local-name()='path' or local-name()='polyline' or local-name()='polygon' or local-name()='line' or local-name()='rect' or local-name()='circle' or local-name()='ellipse' or local-name()='use' or local-name()='image')]")
  counters <- new.env(hash = TRUE, parent = emptyenv())
  elements <- vector("list", length(nodes)); memberships <- vector("list", length(nodes))
  for (i in seq_along(nodes)) {
    node <- nodes[i]; tag <- xml2::xml_name(node)
    attr <- function(key) xml2::xml_attr(node, key)
    num <- function(key) tuner_number(attr(key))
    cx <- num("x"); cy <- num("y")
    if (tag %in% c("circle", "ellipse")) { cx <- num("cx"); cy <- num("cy") }
    if (tag == "rect") { cx <- cx + num("width") / 2; cy <- cy + num("height") / 2 }
    if (tag == "line") { cx <- (num("x1") + num("x2")) / 2; cy <- (num("y1") + num("y2")) / 2 }
    if (tag %in% c("polyline", "polygon")) {
      v <- as.numeric(unlist(strsplit(trimws(attr("points")), "[, ]+")))
      if (length(v)) { cx <- mean(range(v[seq(1, length(v), 2)])); cy <- mean(range(v[seq(2, length(v), 2)])) }
    }
    transform <- attr("transform") %||% ""
    shift <- regmatches(transform, regexec("translate\\(\\s*([-+0-9.eE]+)[, ]+([-+0-9.eE]+)", transform))[[1]]
    if (length(shift) == 3) { cx <- cx + as.numeric(shift[2]); cy <- cy + as.numeric(shift[3]) }
    angle <- regmatches(transform, regexec("rotate\\(\\s*([-+0-9.eE]+)", transform))[[1]]
    angle <- if (length(angle) > 1) as.numeric(angle[2]) else 0
    owner <- attr("data-tuner-owner"); group <- attr("data-tuner-group")
    key <- owner %||% prefix; part <- if (exists(key, counters, inherits = FALSE)) counters[[key]] else 0
    counters[[key]] <- part + 1
    id <- paste0(key, ":node", part)
    groups <- unique(c(owner, group)); groups <- groups[!is.na(groups) & nzchar(groups)]
    style <- tuner_style(node)
    role <- attr("data-tuner-role") %||% if (tag == "text") "text" else if (tag == "rect" && grepl("%", attr("width"))) "background" else "graphic"
    font <- tuner_number(style[["font-size"]] %||% "11px", 11)
    size <- if (tag == "circle") num("r") * 2 * 25.4 / 72 else 2
    xml2::xml_set_attr(node, "data-tuner-id", id)
    xml2::xml_set_attr(node, "data-tuner-leaf", "1")
    xml2::xml_set_attr(node, "data-tuner-cx", cx); xml2::xml_set_attr(node, "data-tuner-cy", cy)
    xml2::xml_set_attr(node, "data-tuner-size", size)
    label <- if (tag == "text") xml2::xml_text(node) else paste(role, i)
    elements[[i]] <- list(id = id, kind = if (tag == "text") "text" else "shape", tag = tag,
      role = role, label = label, groups = unname(as.list(groups)), anchor = list(cx, cy), angle_deg = angle, text_anchor = style[["text-anchor"]] %||% attr("text-anchor") %||% "start",
      font_pt = font, font_family = "Arial", stroke_mm = tuner_number(style[["stroke-width"]] %||% ".7", .7) * 25.4 / 72, size_mm = size, fill = style$fill %||% if (tag == "text") "#000000" else "none",
      stroke = style$stroke %||% "none", parent_transform = "")
    for (key in groups) {
      if (is.null(owners[[key]])) owners[[key]] <- list(id = key, kind = "group", role = attr("data-tuner-group-role") %||% "group", label = attr("data-tuner-group-label") %||% key)
      memberships[[i]] <- setNames(rep(id, length(groups)), groups)
    }
  }
  flat <- unlist(memberships)
  for (key in unique(names(flat))) owners[[key]]$members <- unname(as.list(flat[names(flat) == key]))
  list(svg = as.character(doc), elements = unname(c(owners, elements)))
}

tuner_svg <- function(g, width, height, prefix, edits = list()) {
  paints <- new.env(hash = TRUE, parent = emptyenv()); owners <- list(); index <- 0L
  top_names <- if (inherits(g, "gtable")) g$layout$name else character()
  tag <- function(item, path = "root", role = "graphic", semantic = NULL) {
    name <- item$name %||% ""
    top <- suppressWarnings(as.integer(sub("^root\\.g([0-9]+).*$", "\\1", path)))
    cell <- if (!is.na(top) && top <= length(top_names)) top_names[top] else ""
    if (grepl("axis-[bt]|xlab-[bt]", cell)) semantic <- list(id = paste0(prefix, ":axis-bottom"), label = "X 坐标轴", role = "axis")
    if (grepl("axis-[lr]|ylab-[lr]", cell)) semantic <- list(id = paste0(prefix, ":axis-left"), label = "Y 坐标轴", role = "axis")
    if (grepl("axis-|[xy]lab-", cell)) role <- if (inherits(item, "text")) "text-tick" else "axis-line"
    if (grepl("panel.grid", name, fixed = TRUE)) role <- "grid"
    if (grepl("background", name, fixed = TRUE)) role <- "background"
    if (grepl("^geom_", name)) {
      role <- if (grepl("point", name)) "data-point" else if (grepl("rect|bar|col", name)) "data-bar" else "data-line"
      semantic <- list(id = paste0(prefix, ":series-", path), label = paste0(if (role == "data-point") "点系列" else if (role == "data-bar") "条形系列" else "曲线系列", " ", length(owners) + 1), role = "series")
    }
    if (grepl("^panel", cell) && role != "grid" && inherits(item, c("polyline", "lines", "segments", "xspline"))) {
      role <- "data-line"
      if (is.null(semantic)) semantic <- list(id = paste0(prefix, ":series-", path), label = "线 / 误差线系列", role = "series")
    }
    if (inherits(item, "text") && !grepl("axis-|[xy]lab-", cell)) role <- if (cell %in% c("title", "subtitle", "caption")) paste0("text-", cell) else "text"
    key <- paste0(prefix, ":", path)
    drawable <- inherits(item, c("text", "points", "polyline", "lines", "segments", "rect", "circle", "polygon", "pathgrob", "xspline"))
    if (drawable) {
      owners[[key]] <<- list(id = key, label = if (inherits(item, "text")) paste(as.character(item$label), collapse = " · ") else role,
        kind = "group", role = "group", font_pt = item$gp$fontsize %||% 11)
      for (paint in c("col", "fill")) {
        values <- item$gp[[paint]]
        if (is.null(values) && paint == "col" && inherits(item, "text")) values <- "black"
        if (is.null(values)) next
        originals <- values; values <- unique(values)
        for (j in seq_along(values)) {
          if (is.na(values[j])) next
          rgba <- grDevices::col2rgb(values[j], alpha = TRUE)
          if (!rgba[4]) next
          index <<- index + 1L; marker <- sprintf("#%06X", 1048576L + index)
          rgb <- grDevices::col2rgb(marker)
          values[j] <- grDevices::rgb(rgb[1], rgb[2], rgb[3], alpha = rgba[4], maxColorValue = 255)
          paints[[marker]] <- list(owner = key, group = semantic, role = role,
            color = grDevices::rgb(rgba[1], rgba[2], rgba[3], maxColorValue = 255))
        }
        item$gp[[paint]] <- values[match(originals, unique(originals))]
      }
    }
    for (slot in c("grobs", "children")) for (i in seq_along(item[[slot]])) item[[slot]][[i]] <- tag(item[[slot]][[i]], paste0(path, ".", substr(slot, 1, 1), i), role, semantic)
    item
  }
  tagged <- tag(g)
  svg <- svglite::stringSVG({ grid.newpage(); grid.draw(tagged) }, width = width / 25.4, height = height / 25.4)
  doc <- xml2::read_xml(as.character(svg)); nodes <- xml2::xml_find_all(doc, ".//*[@style]")
  for (node in nodes) {
    text_style <- xml2::xml_attr(node, "style")
    markers <- unique(regmatches(text_style, gregexpr("#[0-9A-Fa-f]{6}", text_style))[[1]])
    for (marker in markers) {
      if (!exists(marker, envir = paints, inherits = FALSE)) next
      paint <- paints[[marker]]
      text_style <- gsub(marker, paint$color, text_style, fixed = TRUE)
      xml2::xml_set_attr(node, "data-tuner-owner", paint$owner)
      xml2::xml_set_attr(node, "data-tuner-role", paint$role)
      if (!is.null(paint$group)) {
        xml2::xml_set_attr(node, "data-tuner-group", paint$group$id)
        xml2::xml_set_attr(node, "data-tuner-group-label", paint$group$label)
        xml2::xml_set_attr(node, "data-tuner-group-role", paint$group$role)
      }
    }
    xml2::xml_set_attr(node, "style", text_style)
  }
  text <- as.character(doc)
  for (old in xml2::xml_attr(xml2::xml_find_all(doc, ".//*[@id]"), "id")) {
    new <- paste0(gsub("[^a-zA-Z0-9]", "_", prefix), "_", old)
    text <- gsub(paste0('id="', old, '"'), paste0('id="', new, '"'), text, fixed = TRUE)
    text <- gsub(paste0("url(#", old, ")"), paste0("url(#", new, ")"), text, fixed = TRUE)
  }
  tuner_model(xml2::read_xml(text), prefix, owners)
}

tuner_layers <- function(plot, width, height) {
  device <- tempfile(fileext = ".svg")
  svglite::svglite(device, width = width / 25.4, height = height / 25.4)
  g <- ggplot2::ggplotGrob(plot)
  grid.newpage(); grid.draw(g); grid.force()
  layers <- list()
  panel_cell <- which(g$layout$name == "panel")[1]
  region <- NULL
  if (!is.na(panel_cell)) {
    cell <- g$layout[panel_cell, ]
    seekViewport(paste0(cell$name, ".", cell$t, "-", cell$l, "-", cell$b, "-", cell$r))
    top <- deviceLoc(unit(0, "npc"), unit(1, "npc"), valueOnly = TRUE)
    region <- list(x = top$x * 25.4, y = height - top$y * 25.4,
      width = convertWidth(unit(1, "npc"), "mm", valueOnly = TRUE), height = convertHeight(unit(1, "npc"), "mm", valueOnly = TRUE))
    params <- ggplot2::ggplot_build(plot)$layout$panel_params[[1]]$x
    region$x_labels <- unname(as.list(as.character(params$get_labels())))
    region$x_positions <- unname(as.list(region$x + as.numeric(params$break_positions()) * region$width))
    upViewport(0)
  }
  guides <- which(grepl("^guide-box", g$layout$name))
  for (i in guides) {
    legend <- g$grobs[[i]]
    if (!inherits(legend, "gtable")) next
    cell <- g$layout[i, ]
    seekViewport(paste0(cell$name, ".", cell$t, "-", cell$l, "-", cell$b, "-", cell$r))
    if (!is.null(legend$vp)) downViewport(legend$vp$name)
    top <- deviceLoc(unit(0, "npc"), unit(1, "npc"), valueOnly = TRUE)
    w <- convertWidth(unit(1, "npc"), "mm", valueOnly = TRUE)
    h <- convertHeight(unit(1, "npc"), "mm", valueOnly = TRUE)
    legend$vp <- NULL
    layers[[paste0("legend", length(layers) + 1)]] <- list(
      grob = legend, role = "legend", x = top$x * 25.4,
      y = height - top$y * 25.4, width = w, height = h)
    g$grobs[[i]] <- nullGrob()
    upViewport(0)
  }
  grDevices::dev.off()
  unlink(device)
  result <- c(list(plot = list(grob = g, role = "plot", x = 0, y = 0, width = width, height = height)), layers)
  attr(result, "region") <- region
  result
}

# Pass a ggplot or a named list of ggplots. width/height describe each panel in mm.
plot_tuner_export <- function(plots, directory = "plot-tuner", width = 50, height = 50,
                              settings = NULL, source_file = "plot.R", object_name = "p", stat_data = NULL, stat_object = NULL) {
  if (inherits(plots, "ggplot")) plots <- list(panel1 = plots)
  if (is.null(names(plots))) names(plots) <- paste0("panel", seq_along(plots))
  dir.create(directory, recursive = TRUE, showWarnings = FALSE)
  saveRDS(plots, file.path(directory, "plots.rds"))
  panels <- list()
  for (i in seq_along(plots)) {
    layers <- tuner_layers(plots[[i]], width, height)
    panels[[i]] <- list(id = names(plots)[i], name = names(plots)[i],
                        x = 5 + (i - 1) * (width + 5), y = 5,
                        width = width, height = height, region = attr(layers, "region"), layers = layers)
  }
  native <- list(panels = panels, width = 5 + length(plots) * (width + 5), height = height + 10)
  saveRDS(native, file.path(directory, "native.rds"))
  project <- list(schema = "bioinfospace.plot-tuner/2", engine = "ggplot2", name = basename(source_file),
                  source_file = source_file, object_name = object_name, editor_version = 3,
                  canvas = list(width = native$width, height = native$height), stat_data = stat_data, stat_object = stat_object, panels = list())
  for (panel in panels) {
    built <- ggplot2::ggplot_build(plots[[panel$id]])
    panel$legend_items <- list()
    for (scale in built$plot$scales$scales) {
      if (!any(scale$aesthetics %in% c("colour", "fill")) || !scale$is_discrete()) next
      breaks <- scale$get_breaks(); labels <- scale$get_labels(breaks); colors <- scale$map(breaks)
      for (k in seq_along(breaks)) if (!is.na(colors[k]) && !as.character(labels[k]) %in% vapply(panel$legend_items, function(x) x$label, "")) panel$legend_items[[length(panel$legend_items) + 1]] <- list(label = as.character(labels[k]), color = colors[k])
    }
    for (j in seq_along(panel$layers)) {
      layer <- panel$layers[[j]]
      id <- paste0(panel$id, "/", names(panel$layers)[j])
      image <- tuner_svg(layer$grob, layer$width, layer$height, id)
      layer$grob <- NULL
      panel$layers[[j]] <- c(list(id = id), layer, image)
    }
    panel$layers <- unname(panel$layers)
    project$panels[[length(project$panels) + 1]] <- panel
  }
  jsonlite::write_json(project, file.path(directory, "project.json"), auto_unbox = TRUE, pretty = TRUE, dataframe = "rows", null = "null")
  if (!is.null(settings)) plot_tuner_render(directory, settings)
  invisible(project)
}

tuner_extend_operations <- function(layer, operations, panel, settings) {
  ids <- vapply(operations, function(o) o$id, "")
  style <- settings$styles[[panel$id]] %||% list()
  colors <- unlist(style$colors); source_colors <- tolower(unlist(style$source_colors))
  metadata <- setNames(layer$elements, vapply(layer$elements, function(e) e$id, ""))
  for (e in layer$elements) {
    if (e$kind == "group" || e$id %in% ids) next
    op <- list(id = e$id); dx <- 0; dy <- 0
    if (!is.null(style$theme) && style$theme != "original") {
      if (e$role == "grid" || (e$role == "axis-line" && style$theme == "minimal")) op$hidden <- TRUE
      if (e$role == "background") op$fill <- "#ffffff"
      if (e$role == "axis-line" && style$theme == "prism") op$stroke_mm <- .35
      if (e$kind == "text") op$font_family <- "Arial"
    }
    if (length(colors)) {
      primary <- if (e$role == "data-line") e$stroke else if (!e$fill %in% c("none", "#ffffff", "#FFFFFF")) e$fill else e$stroke
      index <- match(tolower(substr(primary, 1, 7)), source_colors)
      if (!is.na(index)) op$color <- colors[(index - 1) %% length(colors) + 1] else for (paint in c("fill", "stroke")) {
        index <- match(tolower(substr(e[[paint]], 1, 7)), source_colors)
        if (!is.na(index)) op[[paint]] <- colors[(index - 1) %% length(colors) + 1]
      }
    }
    for (id in c(unlist(e$groups), e$id)) {
      edit <- settings$elements[[id]]
      if (is.null(edit)) next
      dx <- dx + (edit$dx_mm %||% 0); dy <- dy + (edit$dy_mm %||% 0)
      op <- modifyList(op, edit)
      if (!is.null(edit$font_pt) && e$kind == "text" && id != e$id) {
        members <- metadata[[id]]$members
        font <- max(vapply(metadata[unlist(members)], function(m) if (m$kind == "text") m$font_pt else 0, numeric(1)), 0)
        op$font_pt <- edit$font_pt * e$font_pt / if (font > 0) font else e$font_pt
      }
    }
    if (dx != 0) op$dx_mm <- dx
    if (dy != 0) op$dy_mm <- dy
    if (e$kind != "text") { op$font_pt <- NULL; op$text_anchor <- NULL }
    if (e$role == "axis-line" && is.null(settings$elements[[e$id]]$angle_deg)) op$angle_deg <- NULL
    if (length(op) > 1) operations[[length(operations) + 1]] <- op
  }
  operations
}

tuner_apply_operations <- function(svg, layer, operations) {
  elements <- list2env(setNames(layer$elements, vapply(layer$elements, function(e) e$id, "")), hash = TRUE, parent = emptyenv())
  nodes <- xml2::xml_find_all(svg, ".//*[@data-tuner-id]")
  lookup <- list2env(setNames(as.list(nodes), xml2::xml_attr(nodes, "data-tuner-id")), hash = TRUE, parent = emptyenv())
  for (op in operations) {
    if (!exists(op$id, lookup, inherits = FALSE)) next
    node <- lookup[[op$id]]; e <- elements[[op$id]]; patch <- list()
    if (isTRUE(op$hidden)) patch$display <- "none"
    if (!is.null(op$color)) {
      if (e$kind == "text") patch$fill <- op$color else for (paint in c("fill", "stroke")) if (e[[paint]] != "none") patch[[paint]] <- op$color
    }
    for (key in c("fill", "stroke", "opacity")) if (!is.null(op[[key]])) patch[[key]] <- op[[key]]
    if (!is.null(op$stroke_mm) && e$kind != "text") patch[["stroke-width"]] <- op$stroke_mm * 72 / 25.4
    if (e$kind == "text") {
      if (!is.null(op$text_anchor) && nzchar(op$text_anchor)) { patch[["text-anchor"]] <- op$text_anchor; xml2::xml_set_attr(node, "text-anchor", op$text_anchor) }
      for (key in c("font_family", "font_weight", "font_style")) if (!is.null(op[[key]])) patch[[gsub("_", "-", key)]] <- op[[key]]
      if (!is.null(op$font_pt)) patch[["font-size"]] <- paste0(op$font_pt, "px")
      if (!is.null(op[["text"]])) xml2::xml_text(node) <- op[["text"]]
      if (any(c("font_pt", "font_family", "font_weight", "font_style", "text") %in% names(op))) { xml2::xml_set_attr(node, "textLength", NULL); xml2::xml_set_attr(node, "lengthAdjust", NULL) }
    }
    if (!is.null(op$size_mm) && e$role == "data-point") {
      original_stroke <- e$stroke_mm %||% (tuner_number(tuner_style(node)[["stroke-width"]] %||% ".7", .7) * 25.4 / 72)
      patch[["stroke-width"]] <- (op$stroke_mm %||% original_stroke) * 72 / 25.4 / (op$size_mm / e$size_mm)
    }
    tuner_style(node, patch)
    anchor <- unlist(e$anchor); cx <- anchor[1]; cy <- anchor[2]
    dx <- (op$dx_mm %||% 0) * 72 / 25.4; dy <- (op$dy_mm %||% 0) * 72 / 25.4
    angle <- (op$angle_deg %||% e$angle_deg) - e$angle_deg
    size <- if (e$role == "data-point") (op$size_mm %||% e$size_mm) / e$size_mm else 1
    sx <- if (e$role == "data-bar") (op$bar_width_pct %||% 100) / 100 else 1
    sx <- sx * size
    transform <- paste0("translate(", dx, " ", dy, ") rotate(", angle, " ", cx, " ", cy,
      ") translate(", cx, " ", cy, ") scale(", sx, " ", size, ") translate(", -cx, " ", -cy, ") ")
    if (!is.null(op$before_svg)) xml2::xml_add_sibling(node, xml2::xml_root(xml2::read_xml(op$before_svg)), .where = "before")
    if (dx != 0 || dy != 0) {
      transform <- paste0(transform, e$parent_transform %||% "", " ")
      detached <- xml2::xml_find_all(svg, ".//*[@data-tuner-detached]")
      if (!length(detached)) detached <- xml2::xml_add_child(svg, xml2::xml_root(xml2::read_xml('<g xmlns="http://www.w3.org/2000/svg" class="svglite" data-tuner-detached=""/>'))) else detached <- detached[[1]]
      original <- node; node <- xml2::xml_add_child(detached, node); xml2::xml_remove(original)
    }
    xml2::xml_set_attr(node, "transform", paste0(transform, xml2::xml_attr(node, "transform") %||% ""))
  }
  svg
}

tuner_recompute_statistics <- function(project, settings) {
  annotations <- settings$annotations
  indices <- which(vapply(annotations, function(a) a$type == "stat", logical(1)))
  for (i in indices) {
    a <- annotations[[i]]
    if (a$method %in% c("welch", "student", "paired")) {
      rows <- if (a$data_source == "project") project$stat_data[[a$panel]] else settings$stat_sources[[a$source_key]]$rows
      if (!length(rows)) stop("The new export has no linked statistics data")
      data <- do.call(rbind, lapply(rows, function(r) data.frame(group = as.character(r$group), value = r$value %||% NA_real_, id = as.character(r$id %||% NA_character_))))
      left <- data[data$group == a$group1, ]; right <- data[data$group == a$group2, ]
      if (a$method == "paired") {
        if (anyNA(left$id) || anyNA(right$id) || anyDuplicated(left$id) || anyDuplicated(right$id)) stop("Paired data require unique IDs within each group")
        pairs <- merge(left, right, by = "id", suffixes = c(".left", ".right"))
        pairs <- pairs[complete.cases(pairs[, c("value.left", "value.right")]), ]
        x <- pairs$value.left; y <- pairs$value.right
      } else { x <- left$value[is.finite(left$value)]; y <- right$value[is.finite(right$value)] }
      test <- stats::t.test(x, y, paired = a$method == "paired", var.equal = a$method == "student")
      a$p_value <- unname(test$p.value); a$statistic <- unname(test$statistic); a$df <- unname(test$parameter)
      a$n1 <- length(x); a$n2 <- length(y); a$omitted <- nrow(left) + nrow(right) - length(x) - length(y); a$effect <- mean(x) - mean(y)
      a$ci_low <- test$conf.int[1]; a$ci_high <- test$conf.int[2]
      annotations[[i]] <- a
    }
  }
  families <- unique(vapply(annotations[indices], function(a) a$family, ""))
  for (family in families) {
    members <- indices[vapply(annotations[indices], function(a) a$family == family, logical(1))]
    method <- annotations[[members[1]]]$adjustment
    if (method == "provided") next
    p <- vapply(annotations[members], function(a) a$p_value, numeric(1))
    adjusted <- stats::p.adjust(p, method = method)
    for (j in seq_along(members)) annotations[[members[j]]]$p_adjusted <- adjusted[j]
  }
  annotations[indices]
}

tuner_stat_label <- function(a) {
  p <- if (isTRUE(a$use_adjusted)) a$p_adjusted else a$p_value
  if (a$display == "stars") return(if (p < .0001) "****" else if (p < .001) "***" else if (p < .01) "**" else if (p < .05) "*" else "ns")
  paste0(if (isTRUE(a$use_adjusted)) "adjusted P" else "P", if (p < .0001) " < 0.0001" else paste0(" = ", format(signif(p, 3), scientific = FALSE, trim = TRUE)))
}

plot_tuner_render <- function(directory = "plot-tuner", settings = file.path(directory, "tuner.json")) {
  project <- jsonlite::read_json(file.path(directory, "project.json"))
  if (is.character(settings)) settings <- jsonlite::read_json(settings)
  statistics <- tuner_recompute_statistics(project, settings)
  canvas <- settings$canvas
  doc <- xml2::read_xml(sprintf('<svg xmlns="http://www.w3.org/2000/svg" width="%smm" height="%smm" viewBox="0 0 %s %s"><rect width="100%%" height="100%%" fill="white"/></svg>', canvas$width, canvas$height, canvas$width, canvas$height))
  for (panel in project$panels) {
    box <- settings$panels[[panel$id]]
    if (is.null(box)) box <- panel[c("x", "y", "width", "height")]
    for (layer in panel$layers) {
      change <- settings$layers[[layer$id]]
      if (!is.null(change$x)) layer$x <- change$x
      if (!is.null(change$y)) layer$y <- change$y
      svg <- xml2::read_xml(layer$svg)
      if (!is.null(settings$operations)) {
        svg <- tuner_apply_operations(svg, layer, tuner_extend_operations(layer, settings$operations[[layer$id]], panel, settings))
      } else {
      nodes <- xml2::xml_find_all(svg, ".//*[@data-tuner-id]")
      for (node in nodes) {
        edit <- settings$elements[[xml2::xml_attr(node, "data-tuner-id")]]
        if (is.null(edit)) next
        if (!is.null(edit$font_pt)) {
          style <- xml2::xml_attr(node, "style")
          style <- gsub("font-size:[^;]+;?", "", style)
          xml2::xml_set_attr(node, "style", paste0(style, ";font-size:", edit$font_pt, "px"))
          xml2::xml_set_attr(node, "textLength", NULL)
          xml2::xml_set_attr(node, "lengthAdjust", NULL)
        }
        dx <- if (is.null(edit$dx_mm)) 0 else edit$dx_mm * 72 / 25.4
        dy <- if (is.null(edit$dy_mm)) 0 else edit$dy_mm * 72 / 25.4
        transform <- xml2::xml_attr(node, "transform")
        if (is.na(transform)) transform <- ""
        xml2::xml_set_attr(node, "transform", paste0("translate(", dx, " ", dy, ") ", transform))
      }
      }
      sx <- box$width / panel$width
      sy <- box$height / panel$height
      attrs <- c(x = box$x + layer$x * sx, y = box$y + layer$y * sy,
                 width = layer$width * sx, height = layer$height * sy, overflow = "visible")
      for (key in names(attrs)) xml2::xml_set_attr(xml2::xml_root(svg), key, attrs[[key]])
      xml2::xml_add_child(doc, xml2::xml_root(svg))
    }
    for (overlay in settings$overlays) {
      if (overlay$panel_id != panel$id) next
      svg <- xml2::read_xml(overlay$svg)
      for (key in c("x", "y", "width", "height")) xml2::xml_set_attr(svg, key, box[[key]])
      xml2::xml_add_child(doc, xml2::xml_root(svg))
    }
  }
  for (a in statistics) {
    labels <- xml2::xml_find_all(doc, ".//*[@data-stat-id]")
    hit <- which(xml2::xml_attr(labels, "data-stat-id") == a$id)
    if (length(hit)) xml2::xml_text(labels[hit]) <- tuner_stat_label(a)
  }
  if (length(statistics)) {
    columns <- c("id", "panel", "group1", "group2", "method", "provided_method", "n1", "n2", "statistic", "df", "effect", "ci_low", "ci_high", "p_value", "p_adjusted", "adjustment", "family", "data_source", "source_name", "alternative", "omitted")
    table <- do.call(rbind, lapply(statistics, function(a) as.data.frame(setNames(lapply(columns, function(k) a[[k]] %||% NA), columns))))
    write.csv(table, file.path(directory, "tuned-statistics.csv"), row.names = FALSE)
  }
  stem <- file.path(directory, "tuned")
  xml2::write_xml(doc, paste0(stem, ".svg"))
  rsvg::rsvg_pdf(paste0(stem, ".svg"), paste0(stem, ".pdf"),
                   width = round(canvas$width / 25.4 * 72), height = round(canvas$height / 25.4 * 72))
  rsvg::rsvg_png(paste0(stem, ".svg"), paste0(stem, ".png"),
                  width = round(canvas$width / 25.4 * 600), height = round(canvas$height / 25.4 * 600))
  saveRDS(list(native = readRDS(file.path(directory, "native.rds")), settings = settings, statistics = statistics), paste0(stem, ".rds"))
  invisible(stem)
}
