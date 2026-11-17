# Explicit input names carry grouping and matrix-block identities.
native_file <- if (sys.nframe() > 0) sys.frame(1)$ofile else sub('^--file=', '', grep('^--file=', commandArgs(), value = TRUE)[1])
native_skill <- normalizePath(file.path(dirname(native_file), '..'))
library(ggplot2)
source(file.path(native_skill, 'scripts/compact.R'))
source(file.path(native_skill, 'scripts/tidyplots.R'))

render_representative_case <- function(case, input, out, tracks = NULL, columns = NULL,
                                       formats = 'png', save_object = FALSE, value_label = 'Feature value') {
  dir.create(out, recursive = TRUE, showWarnings = FALSE)
  theme <- biomedical_theme(11.5) + theme(axis.title = element_text(size = 12), strip.text = element_text(size = 11.5), aspect.ratio = NULL)
  if (case == 'lollipop') {
    d <- read.csv(input)
    stopifnot(!anyDuplicated(d[c('feature', 'group')]))
    d$feature <- factor(d$feature, levels = rev(unique(d$feature)))
    groups <- unique(d$group); pal <- biomedical_palette(groups)
    dodge <- position_dodge(width = .65, orientation = 'y')
    p <- ggplot(d, aes(value, feature, colour = group, group = group)) +
      geom_linerange(aes(xmin = 0, xmax = value), position = dodge, linewidth = .6) +
      geom_point(position = dodge, size = 1.8) + scale_colour_manual(values = pal) +
      scale_y_discrete(labels = scales::label_wrap(26)) +
      labs(x = 'Score', y = NULL) + theme +
      ggh4x::force_panelsizes(cols = grid::unit(40, 'mm'), rows = grid::unit(max(35, nlevels(d$feature) * length(groups) * 5), 'mm'))
    caption <- 'Supplied scores by named category and group. Native horizontal dodge aligns each stem with its point and supports any supplied group names.'
  } else if (case == 'cumulative-incidence') {
    d <- read.csv(input); stopifnot(!anyDuplicated(d$id), all(d$status >= 0))
    groups <- unique(d$group); pal <- biomedical_palette(groups)
    fit <- cmprsk::cuminc(d$time, d$status, factor(d$group, levels = groups), cencode = 0)
    keys <- expand.grid(group = groups, event = sort(unique(d$status[d$status != 0])), stringsAsFactors = FALSE)
    curves <- do.call(rbind, lapply(seq_len(nrow(keys)), function(i) {
      k <- keys[i, ]; z <- fit[[paste(k$group, k$event)]]
      if (is.null(z)) return(NULL)
      data.frame(time = z$time, incidence = z$est, variance = z$var, group = k$group, event = paste('Event', k$event))
    }))
    curves$group <- factor(curves$group, levels = groups)
    p <- ggplot(curves, aes(time, incidence, colour = group)) + geom_step(linewidth = .65) +
      facet_wrap(~event, nrow = 1) + scale_colour_manual(values = pal) +
      scale_x_continuous(n.breaks = 3, labels = scales::label_number(drop0trailing = TRUE, scale_cut = scales::cut_short_scale())) +
      scale_y_continuous(limits = c(0, 1)) + labs(x = 'Time', y = 'Cumulative incidence') + theme +
      ggh4x::force_panelsizes(cols = grid::unit(36, 'mm'), rows = grid::unit(45, 'mm'))
    write.csv(curves, file.path(out, 'estimates.csv'), row.names = FALSE)
    if (save_object) saveRDS(fit, file.path(out, 'model.rds'))
    caption <- 'Descriptive competing-risk cumulative incidence from cmprsk, with 0 denoting censoring. Exact group/event result keys preserve group names containing spaces. Estimates and variances are saved.'
  } else if (case == 'heatmap-composite') {
    m <- as.matrix(read.csv(input, row.names = 1, check.names = FALSE))
    tr <- read.csv(tracks, row.names = 1); spec <- read.csv(columns)
    stopifnot(setequal(rownames(m), rownames(tr)), setequal(colnames(m), spec$feature),
      !anyDuplicated(spec$feature), all(is.finite(m)), all(tr$count >= 0), all(tr$fraction >= 0 & tr$fraction <= 1))
    tr <- tr[rownames(m), , drop = FALSE]
    if (!'Arial' %in% names(grDevices::pdfFonts()))
      grDevices::pdfFonts(Arial = grDevices::pdfFonts('ArialMT')[[1]])
    txt <- grid::gpar(fontfamily = 'Arial', fontsize = 11.5, fontface = 'plain')
    col_fun <- circlize::colorRamp2(c(-2, 0, 2), c('#2166AC', 'white', '#B2182B'))
    blocks <- unique(spec$block)
    hts <- lapply(blocks, function(block) {
      features <- spec$feature[spec$block == block]
      ComplexHeatmap::Heatmap(m[, features, drop = FALSE], name = block, col = col_fun,
        cluster_rows = FALSE, cluster_columns = FALSE, row_names_side = 'left',
        row_names_gp = txt, column_names_gp = txt, column_names_rot = 90,
        column_title = block, column_title_gp = txt,
        width = grid::unit(length(features) * 8, 'mm'), height = grid::unit(nrow(m) * 8, 'mm'),
        show_heatmap_legend = identical(block, blocks[1]),
        heatmap_legend_param = list(title = value_label, title_gp = txt, labels_gp = txt))
    })
    count_ticks <- pretty(c(0, max(tr$count)), n = 2)
    count_ticks <- count_ticks[count_ticks >= 0 & count_ticks <= max(tr$count)]
    anno <- ComplexHeatmap::rowAnnotation(
      Count = ComplexHeatmap::anno_barplot(tr$count, width = grid::unit(18, 'mm'),
        gp = grid::gpar(fill = '#1F78B4'), axis_param = list(gp = txt, labels_rot = 0,
          at = count_ticks, labels = scales::label_number(drop0trailing = TRUE, scale_cut = scales::cut_short_scale())(count_ticks))),
      Fraction = ComplexHeatmap::anno_barplot(tr$fraction, width = grid::unit(18, 'mm'), ylim = c(0, 1),
        gp = grid::gpar(fill = '#A6CEE3'), axis_param = list(gp = txt, labels_rot = 0)),
      gap = grid::unit(5, 'mm'), annotation_name_gp = txt, annotation_name_rot = 45,
      annotation_name_offset = grid::unit(9, 'mm'))
    ht <- Reduce(`+`, hts) + anno
    draw_args <- list(heatmap_legend_side = 'right', padding = grid::unit(rep(3, 4), 'mm'))
    measure <- tempfile(fileext = '.pdf')
    grDevices::cairo_pdf(measure, width = 7, height = 5, family = 'Arial')
    drawn <- do.call(ComplexHeatmap::draw, c(list(object = ht), draw_args))
    width <- grid::convertWidth(ComplexHeatmap::width.HeatmapList(drawn), 'mm', valueOnly = TRUE) + 2
    height <- grid::convertHeight(ComplexHeatmap::height.HeatmapList(drawn), 'mm', valueOnly = TRUE) + 2
    grDevices::dev.off(); unlink(measure)
    export_biomedical(ht, file.path(out, 'figure'), width, height,
      formats = formats, save_object = save_object, draw_args = draw_args,
      source_data = list(matrix = normalizePath(input), tracks = normalizePath(tracks), columns = normalizePath(columns)))
    write.csv(data.frame(rows = nrow(m), columns = ncol(m), tile_mm = 8, width_mm = width, height_mm = height), file.path(out, 'layout.csv'), row.names = FALSE)
    pal <- c(Low = '#2166AC', Center = '#FFFFFF', High = '#B2182B')
    caption <- 'Supplied values with no scaling or added statistics. Named column-block metadata defines matrix panels; tracks join by row names. All matrix tiles are 8 mm squares. Native annotation axes follow count data; fractions retain the scientific 0–1 domain. RdBu is centered at 0 and saturates outside [-2, 2].'
  } else stop('Unknown representative case')
  if (case != 'heatmap-composite') export_tidyplots(p, file.path(out, 'figure'), formats = formats, save_object = save_object, source_data = normalizePath(input))
  write.csv(data.frame(group = names(pal), color = unname(pal)), file.path(out, 'palette.csv'), row.names = FALSE)
  writeLines(paste('Synthetic demonstration data.', caption), file.path(out, 'caption.txt'))
  writeLines(capture.output(sessionInfo()), file.path(out, 'session-info.txt'))
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  render_representative_case(args[1], args[2], args[3], if (length(args) > 3) args[4], if (length(args) > 4) args[5])
}
