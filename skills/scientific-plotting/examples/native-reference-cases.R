# Native replacements for the first-party worked examples.
native_script <- sub('^--file=', '', grep('^--file=', commandArgs(), value = TRUE)[1])
native_file <- if (sys.nframe() > 0) sys.frame(1)$ofile else native_script
native_skill <- normalizePath(file.path(dirname(native_file), '..'))
library(ggplot2)
library(tidyplots)
source(file.path(native_skill, 'scripts/compact.R'))
source(file.path(native_skill, 'scripts/tidyplots.R'))
source(file.path(native_skill, 'examples/native-additional-cases.R'))

render_native_case <- function(case, d, out, comparisons = NULL, canvas_width = 50, canvas_height = 50,
                               formats = 'png', save_object = FALSE, source_data = NULL) {
  if (!case %in% c('independent', 'forest', 'heatmap')) return(render_additional_case(case, d, out, formats, save_object, source_data))
  dir.create(out, recursive = TRUE, showWarnings = FALSE)
  if (is.null(source_data)) {
    source_data <- file.path(out, 'input.csv')
    write.csv(d, source_data, row.names = FALSE)
  }
  groups <- if ('group' %in% names(d)) unique(as.character(d$group)) else 'Estimate'
  control <- if ('Control' %in% groups) 'Control' else NULL
  pal <- biomedical_palette(groups, control = control)
  theme <- biomedical_theme(11.5, x_angle = 45) +
    theme(axis.title = element_text(size = 12), legend.position = 'none')

  if (case == 'independent') {
    stopifnot(!anyDuplicated(d$unit), all(is.finite(d$value)))
    d$group <- factor(d$group, levels = groups)
    if (is.null(comparisons)) {
      stopifnot(length(groups) == 2)
      comparisons <- data.frame(group1 = groups[1], group2 = groups[2])
    }
    stopifnot(all(unlist(comparisons[c('group1','group2')]) %in% groups))
    statistics <- do.call(rbind, lapply(seq_len(nrow(comparisons)), function(i) {
      a <- d$value[d$group == comparisons$group1[i]]
      b <- d$value[d$group == comparisons$group2[i]]
      test <- t.test(b, a, alternative = 'two.sided', var.equal = FALSE)
      data.frame(group1 = comparisons$group1[i], group2 = comparisons$group2[i],
        n1 = length(a), n2 = length(b), estimate = unname(test$estimate[1] - test$estimate[2]),
        low = test$conf.int[1], high = test$conf.int[2], p = test$p.value,
        statistic = unname(test$statistic), df = unname(test$parameter),
        method = 'Two-sided Welch; group2 minus group1')
    }))
    statistics$p_holm <- p.adjust(statistics$p, 'holm')
    statistics$label <- p_labels(statistics$p_holm, nonsignificant = 'value')
    write.csv(statistics, file.path(out, 'statistics.csv'), row.names = FALSE)
    write.csv(comparisons, file.path(out, 'comparisons.csv'), row.names = FALSE)
    p <- d |> tidyplot(x = group, y = value, color = group, width = NA, height = NA, unit = 'mm') |>
      add_mean_bar(alpha = .35) |> add_sd_errorbar(width = .16, linewidth = .4) |>
      add(geom_point(aes(group = unit), position = position_dodge(width = .8), size = 1)) |>
      adjust_colors(pal) |>
      add(theme) |> adjust_font(fontsize = 11.5, family = 'Arial') |>
      add(labs(x = NULL, y = 'Response (a.u.)')) |>
      add(ggsignif::geom_signif(colour = 'black', show.legend = FALSE,
        comparisons = asplit(as.matrix(comparisons[c('group1','group2')]), 1),
        annotations = statistics$label, margin_top = .08, step_increase = .15,
        tip_length = .012, textsize = 11.5 / ggplot2::.pt, family = 'Arial',
        size = .35, vjust = -.15)) |>
      add(scale_y_continuous(n.breaks = 5, expand = expansion(mult = c(0, .1)))) |>
      add(expand_limits(y = 0)) |>
      adjust_size(width = NA, height = NA, unit = 'mm')
    export_biomedical(p, file.path(out, 'figure'), canvas_width, canvas_height,
      placed_width_mm = canvas_width, formats = formats, save_object = save_object, source_data = source_data)
    built <- ggplot_build(p)
    write.csv(built$data[[1]], file.path(out, 'bar_geometry.csv'), row.names = FALSE)
    write.csv(built$data[[2]], file.path(out, 'interval_geometry.csv'), row.names = FALSE)
    write.csv(built$data[[3]], file.path(out, 'point_geometry.csv'), row.names = FALSE)
    write.csv(built$data[[4]], file.path(out, 'annotation_geometry.csv'), row.names = FALSE)
    caption <- paste('Independent units; mean bars, SD and all sample points.',
      'n per group:', paste(names(table(d$group)), as.integer(table(d$group)), sep = ' = ', collapse = '; '),
      'Two-sided Welch tests; Holm correction across the supplied comparison plan.',
      'All primary adjusted P values are shown. Estimates and nominal 95% CIs are group2 minus group1.')
  } else if (case == 'forest') {
    stopifnot(all(d$lower > 0), all(d$lower <= d$estimate), all(d$estimate <= d$upper))
    d$contrast <- factor(d$contrast, levels = rev(unique(d$contrast)))
    pal <- c(Estimate = '#1F78B4')
    p <- ggplot(d, aes(estimate, contrast)) +
      geom_vline(xintercept = 1, colour = 'grey65', linetype = 2) +
      geom_errorbar(aes(xmin = lower, xmax = upper), orientation = 'y', width = .15, linewidth = .5) +
      geom_point(size = 1.8, colour = unname(pal['Estimate'])) +
      scale_x_log10(labels = scales::label_number(scale_cut = scales::cut_short_scale()),
        expand = expansion(mult = .08)) +
      scale_y_discrete(labels = scales::label_wrap(26)) +
      labs(x = 'Odds ratio (95% CI)', y = NULL) +
      biomedical_theme(11.5) + theme(axis.title.x = element_text(size = 12)) +
      ggh4x::force_panelsizes(cols = grid::unit(50, 'mm'), rows = grid::unit(35, 'mm'))
    export_tidyplots(p, file.path(out, 'figure'), formats = formats, save_object = save_object, source_data = source_data)
    write.csv(d, file.path(out, 'estimates.csv'), row.names = FALSE)
    caption <- 'Supplied odds ratios and 95% confidence interval endpoints; log scale with native ticks; reference value is 1.'
  } else if (case == 'heatmap') {
    stopifnot(!anyDuplicated(d[c('feature','sample')]), all(is.finite(d$value)),
      nrow(d) == length(unique(d$feature)) * length(unique(d$sample)))
    measure <- tempfile(fileext = '.pdf')
    grDevices::cairo_pdf(measure, width = 4, height = 4, family = 'Arial')
    mat <- as.matrix(xtabs(value ~ feature + sample, d))
    z <- t(scale(t(mat)))
    stopifnot(all(is.finite(z)))
    group <- d$group[match(colnames(z), d$sample)]
    # ComplexHeatmap also measures text on a PostScript device.
    if (!'Arial' %in% names(grDevices::pdfFonts()))
      grDevices::pdfFonts(Arial = grDevices::pdfFonts('ArialMT')[[1]])
    type <- grid::gpar(fontfamily = 'Arial', fontsize = 11.5, fontface = 'plain')
    tile_mm <- 8
    col_fun <- circlize::colorRamp2(c(-2, 0, 2), c('#2166AC', 'white', '#B2182B'))
    key <- ComplexHeatmap::packLegend(
      ComplexHeatmap::Legend(title = 'Group', labels = names(pal), legend_gp = grid::gpar(fill = unname(pal)),
        title_gp = type, labels_gp = type),
      ComplexHeatmap::Legend(title = 'Gene expression\n(z-score)', col_fun = col_fun, at = c(-2, 0, 2),
        legend_height = grid::unit(15, 'mm'), title_gp = type, labels_gp = type),
      direction = 'vertical', gap = grid::unit(3, 'mm'))
    ht <- ComplexHeatmap::Heatmap(z, name = 'Gene expression\n(z-score)',
      col = col_fun, show_heatmap_legend = FALSE,
      width = grid::unit(ncol(z) * tile_mm, 'mm'), height = grid::unit(nrow(z) * tile_mm, 'mm'),
      cluster_rows = FALSE, cluster_columns = FALSE, row_names_gp = type, column_names_gp = type,
      column_names_rot = 45, use_raster = FALSE,
      top_annotation = ComplexHeatmap::HeatmapAnnotation(Group = group, col = list(Group = pal),
        show_legend = FALSE, show_annotation_name = FALSE))
    draw_args <- list(heatmap_legend_side = 'right', heatmap_legend_list = list(key),
      padding = grid::unit(rep(3, 4), 'mm'))
    draw_heatmap <- function() do.call(ComplexHeatmap::draw, c(list(object = ht), draw_args))
    drawn <- draw_heatmap()
    legend_size <- ComplexHeatmap::heatmap_legend_size(drawn)
    width_mm <- grid::convertWidth(ComplexHeatmap::width.HeatmapList(drawn), 'mm', valueOnly = TRUE) + 2
    height_mm <- max(grid::convertHeight(ComplexHeatmap::height.HeatmapList(drawn), 'mm', valueOnly = TRUE),
      grid::convertHeight(legend_size[2], 'mm', valueOnly = TRUE)) + 2
    grDevices::dev.off(); unlink(measure)
    export_biomedical(ht, file.path(out, 'figure'), width_mm, height_mm,
      formats = formats, save_object = save_object, draw_args = draw_args,
      source_data = list(input = source_data, display = file.path(out, 'display_matrix.csv')))
    write.csv(z, file.path(out, 'display_matrix.csv'))
    write.csv(data.frame(feature = rownames(z)), file.path(out, 'row_order.csv'), row.names = FALSE)
    write.csv(data.frame(sample = colnames(z), group = group), file.path(out, 'column_order.csv'), row.names = FALSE)
    write.csv(data.frame(rows = nrow(z), columns = ncol(z), tile_mm = tile_mm,
      body_width_mm = ncol(z) * tile_mm, body_height_mm = nrow(z) * tile_mm,
      width_mm = width_mm, height_mm = height_mm), file.path(out, 'layout.csv'), row.names = FALSE)
    caption <- paste(nrow(z), 'features x', ncol(z), 'samples; values standardized within feature using the sample SD;',
      'alphabetical order, no clustering; 8 mm square tiles and native right-side legends.')
  } else stop('Choose independent, forest or heatmap.')
  write.csv(data.frame(group = names(pal), color = unname(pal)), file.path(out, 'palette.csv'), row.names = FALSE)
  writeLines(paste('Synthetic demonstration data.', caption, 'Input rows:', nrow(d)), file.path(out, 'caption.txt'))
  writeLines(capture.output(sessionInfo()), file.path(out, 'session-info.txt'))
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  comparisons <- if (length(args) == 4) read.csv(args[4]) else NULL
  render_native_case(args[1], read.csv(args[2], check.names = FALSE), args[3], comparisons, source_data = normalizePath(args[2]))
}
