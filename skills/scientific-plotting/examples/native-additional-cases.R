# Native layouts for the remaining observation and supplied-result examples.
render_additional_case <- function(case, d, out, formats = 'png', save_object = FALSE, source_data = NULL) {
  dir.create(out, recursive = TRUE, showWarnings = FALSE)
  if (is.null(source_data)) {
    source_data <- file.path(out, 'input.csv')
    write.csv(d, source_data, row.names = FALSE, na = '')
  }
  groups <- if ('group' %in% names(d)) unique(as.character(d$group)) else 'Estimate'
  if ('group' %in% names(d)) d$group <- factor(d$group, levels = groups)
  pal <- biomedical_palette(groups, control = if ('Control' %in% groups) 'Control' else NULL)
  theme <- biomedical_theme(11.5) + theme(axis.title = element_text(size = 12), strip.text = element_text(size = 11.5), aspect.ratio = NULL)
  panel_width <- 45; panel_height <- 50

  if (case == 'paired') {
    stopifnot(!anyDuplicated(d[c('unit', 'condition')]), all(table(d$unit) == 2),
      length(unique(d$condition)) == 2, all(is.finite(d$value)))
    conditions <- unique(d$condition)
    d$condition <- factor(d$condition, levels = conditions)
    pal <- biomedical_palette(conditions)
    matched <- as.matrix(xtabs(value ~ unit + condition, d))
    test <- t.test(matched[, 2], matched[, 1], paired = TRUE)
    statistics <- data.frame(group1 = conditions[1], group2 = conditions[2], n = nrow(matched),
      estimate = unname(test$estimate), low = test$conf.int[1], high = test$conf.int[2],
      statistic = unname(test$statistic), df = unname(test$parameter), p = test$p.value,
      method = 'Two-sided paired t; group2 minus group1')
    statistics$label <- p_labels(statistics$p, nonsignificant = 'value')
    write.csv(statistics, file.path(out, 'statistics.csv'), row.names = FALSE)
    dodge <- position_dodge(width = .5)
    p <- ggplot(d, aes(condition, value, group = unit)) +
      geom_line(position = dodge, colour = 'grey70', linewidth = .35) +
      geom_point(aes(colour = condition), position = dodge, size = 1.2) +
      scale_colour_manual(values = pal, guide = 'none') +
      ggsignif::geom_signif(data = d, aes(condition, value, group = 1), inherit.aes = FALSE,
        comparisons = list(conditions), annotations = statistics$label, margin_top = .08,
        textsize = 11.5 / ggplot2::.pt, family = 'Arial', size = .35, vjust = -.15) +
      scale_y_continuous(expand = expansion(mult = c(.06, .12))) +
      labs(x = NULL, y = 'Response (a.u.)') + theme +
      theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1))
    panel_width <- 36
    caption <- paste(nrow(matched), 'matched units; native dodge preserves within-unit lines.',
      'Two-sided paired t test; one planned contrast; effect and nominal 95% CI are group2 minus group1.')
  } else if (case == 'repeated') {
    stopifnot(!anyDuplicated(d[c('unit', 'time')]))
    d <- d[order(d$unit, d$time), ]
    d$segment <- ave(is.na(d$value), d$unit, FUN = cumsum)
    visible <- d[!is.na(d$value), ]
    p <- ggplot(visible, aes(time, value, colour = group)) +
      geom_line(aes(group = interaction(unit, segment)), linewidth = .4, alpha = .6) +
      geom_point(size = 1.3) + facet_wrap(~group, nrow = 1, labeller = label_wrap_gen(18)) +
      scale_colour_manual(values = pal, guide = 'none') +
      labs(x = 'Day', y = 'Response (a.u.)') + theme
    panel_width <- 36
    write.csv(visible, file.path(out, 'connected_segments.csv'), row.names = FALSE)
    caption <- 'Descriptive repeated trajectories; actual time spacing, verified unit IDs and breaks at explicitly missing visits. Facets share scales.'
  } else if (case == 'independent-time') {
    stopifnot(!anyDuplicated(d$unit))
    s <- aggregate(value ~ group + time, d, function(x) c(mean = mean(x), sd = sd(x), n = length(x)))
    s <- data.frame(s[c('group', 'time')], s$value)
    p <- ggplot(s, aes(time, mean, colour = group)) +
      geom_linerange(aes(ymin = mean - sd, ymax = mean + sd), linewidth = .4) +
      geom_line(linewidth = .6) + geom_point(size = 1.6) + scale_colour_manual(values = pal) +
      labs(x = 'Day', y = 'Response (a.u.)') + theme
    write.csv(s, file.path(out, 'summary.csv'), row.names = FALSE)
    caption <- 'Descriptive means and SD of different independent units at each time. Native numeric ticks preserve actual time spacing; n is saved per group and time.'
  } else if (case == 'factorial') {
    stopifnot(!anyDuplicated(d$unit))
    d$genotype <- factor(d$genotype, levels = unique(d$genotype))
    d$treatment <- factor(d$treatment, levels = unique(d$treatment))
    pal <- biomedical_palette(levels(d$treatment))
    p <- ggplot(d, aes(genotype, value, colour = treatment, fill = treatment)) +
      stat_summary(fun = mean, geom = 'col', width = .65, alpha = .3,
        position = position_dodge(.75)) +
      stat_summary(fun.data = mean_sdl, fun.args = list(mult = 1), geom = 'errorbar',
        width = .16, position = position_dodge(.75)) +
      geom_point(position = position_jitterdodge(jitter.width = .12, dodge.width = .75, seed = 12), size = 1.2) +
      scale_colour_manual(values = pal) + scale_fill_manual(values = pal) + expand_limits(y = 0) +
      labs(x = NULL, y = 'Response (a.u.)') + theme +
      theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1))
    panel_width <- max(40, nlevels(d$genotype) * nlevels(d$treatment) * 10)
    panel_height <- max(50, panel_width)
    caption <- 'Descriptive factorial display of independent units; bars are means, error bars are SD, points are units. No interaction or pairwise inference is added.'
  } else if (case == 'dose-response') {
    source(file.path(native_skill, 'scripts/dose_response.R'))
    fit <- dose_response_candidates(d$dose, d$response)
    eligible <- subset(fit$comparison, converged & covariance_ok & midpoint_in_range & interval_in_range)
    stopifnot(nrow(eligible) > 0)
    selected <- eligible$model[which.min(eligible$aicc)]
    g <- subset(fit$predictions, model == selected)
    pal <- c(Assay = '#1F78B4')
    p <- ggplot(d, aes(dose, response)) +
      geom_ribbon(data = g, aes(y = NULL, ymin = low, ymax = high), fill = '#A6CEE3', alpha = .4) +
      geom_line(data = g, aes(y = fitted), colour = pal[1], linewidth = .65) +
      geom_point(size = 1.3, colour = pal[1]) +
      scale_x_log10(labels = scales::label_number(drop0trailing = TRUE, scale_cut = scales::cut_short_scale())) +
      labs(x = 'Dose (µM)', y = 'Response (%)') + theme
    for (field in c('comparison', 'parameters', 'predictions', 'residuals'))
      write.csv(fit[[field]], file.path(out, paste0(field, '.csv')), row.names = FALSE)
    if (save_object) saveRDS(fit, file.path(out, 'models.rds'))
    caption <- paste('Technical measurements from one synthetic assay;', selected,
      'selected by minimum AICc among eligible fits. 95% model confidence band; native log ticks follow the tested range.')
  } else if (case == 'distribution') {
    stopifnot(!anyDuplicated(d$unit))
    p <- ggplot(d, aes(group, value, colour = group)) +
      geom_boxplot(width = .5, outlier.shape = NA, linewidth = .45) +
      geom_point(aes(group = unit), position = position_dodge(.7), size = 1, alpha = .8) +
      scale_colour_manual(values = pal, guide = 'none') + labs(x = NULL, y = 'Response (a.u.)') + theme +
      theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1))
    panel_width <- max(36, length(groups) * 16); panel_height <- max(50, panel_width)
    caption <- 'Descriptive independent-unit distributions; boxes show median and quartiles, whiskers extend to 1.5 IQR, and all units are shown with native ID dodge.'
  } else if (case == 'survival') {
    stopifnot(!anyDuplicated(d$unit), all(d$event %in% c(0, 1)))
    f <- survival::survfit(survival::Surv(time, event) ~ group, d, conf.type = 'log-log')
    p <- survminer::ggsurvplot(f, data = d, conf.int = TRUE, conf.int.style = 'step',
      censor = TRUE, censor.shape = 3, palette = unname(pal[groups]), legend.labs = groups,
      ggtheme = theme, xlab = 'Time (months)', ylab = 'Survival probability')$plot +
      theme(legend.position = 'right', legend.title = element_blank())
    write.csv(survminer::surv_summary(f, data = d), file.path(out, 'survival_estimates.csv'), row.names = FALSE)
    if (save_object) saveRDS(f, file.path(out, 'model.rds'))
    caption <- 'One independent subject per row; native survminer Kaplan–Meier curves, 95% log-log confidence limits and censor marks. Risk counts and estimates are saved.'
  } else if (case == 'composition') {
    stopifnot(!anyDuplicated(d[c('sample', 'category')]), all(d$count >= 0),
      all(tapply(as.character(d$group), d$sample, function(x) length(unique(x))) == 1))
    d$denominator <- ave(d$count, d$sample, FUN = sum); stopifnot(all(d$denominator > 0))
    d$fraction <- d$count / d$denominator
    d$sample <- factor(d$sample, levels = unique(d$sample))
    pal <- biomedical_palette(unique(d$category))
    p <- ggplot(d, aes(sample, count, fill = category)) + geom_col(position = 'fill', width = .7) +
      facet_grid(. ~ group, scales = 'free_x', space = 'free_x', labeller = label_wrap_gen(12)) + scale_fill_manual(values = pal) +
      scale_y_continuous(labels = scales::label_percent(), expand = expansion(0)) +
      labs(x = 'Sample', y = 'Fraction') + theme +
      theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1))
    panel_width <- vapply(groups, function(g) 8 * length(unique(d$sample[d$group == g])), numeric(1))
    panel_height <- max(50, sum(panel_width))
    write.csv(d, file.path(out, 'fractions.csv'), row.names = FALSE)
    caption <- 'Descriptive per-sample composition. Native position_fill uses each sample total as denominator; group facets have space proportional to sample counts.'
  } else if (case == 'enrichment') {
    stopifnot(!anyDuplicated(d$term), all(d$padj > 0 & d$padj <= 1))
    d$neg_log10_padj <- -log10(d$padj)
    d$term <- factor(d$term, levels = rev(d$term))
    pal <- c(Enrichment = '#1F78B4')
    p <- ggplot(d, aes(neg_log10_padj, term)) + geom_col(width = .65, fill = pal[1]) +
      scale_y_discrete(labels = scales::label_wrap(28)) +
      labs(x = expression(-log[10](italic(P)[adj])), y = NULL) + theme +
      theme(axis.title.x = element_text(size = 16))
    panel_width <- 40; panel_height <- max(35, nrow(d) * 9)
    write.csv(d, file.path(out, 'display_values.csv'), row.names = FALSE)
    caption <- 'Supplied adjusted P values shown as minus log10; term order follows input. Counts and unrounded source values are retained; no new tests are computed.'
  } else stop('Unknown additional case')
  p <- p + ggh4x::force_panelsizes(cols = grid::unit(panel_width, 'mm'), rows = grid::unit(panel_height, 'mm'))
  export_tidyplots(p, file.path(out, 'figure'), formats = formats, save_object = save_object, source_data = source_data)
  write.csv(data.frame(group = names(pal), color = unname(pal)), file.path(out, 'palette.csv'), row.names = FALSE)
  writeLines(paste('Synthetic demonstration data.', caption, 'Input rows:', nrow(d)), file.path(out, 'caption.txt'))
  writeLines(capture.output(sessionInfo()), file.path(out, 'session-info.txt'))
}
