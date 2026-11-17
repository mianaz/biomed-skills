# Source-result adapters: analysis inputs and named label choices stay explicit.
native_file <- if (sys.nframe() > 0) sys.frame(1)$ofile else sub('^--file=', '', grep('^--file=', commandArgs(), value = TRUE)[1])
native_skill <- normalizePath(file.path(dirname(native_file), '..'))
library(ggplot2)
source(file.path(native_skill, 'scripts/compact.R'))
source(file.path(native_skill, 'scripts/tidyplots.R'))

render_enrichment_case <- function(case, d, out) {
  dir.create(out, recursive = TRUE, showWarnings = FALSE)
  write.csv(d, file.path(out, 'input.csv'), row.names = FALSE)
  d$ID <- as.character(d$ID)
  theme <- biomedical_theme(11.5) + theme(axis.title = element_text(size = 12),
    strip.text = element_text(size = 11.5), aspect.ratio = NULL)
  if (case == 'go-ontology') {
    stopifnot(!anyDuplicated(d$ID), all(d$padj > 0 & d$padj <= 1))
    d$score <- -log10(d$padj)
    d$type <- factor(d$type, levels = unique(d$type))
    d$ID <- factor(d$ID, levels = rev(d$ID))
    labels <- setNames(d$Description, d$ID)
    pal <- biomedical_palette(levels(d$type))
    p <- ggplot(d, aes(score, ID, fill = type)) + geom_col(width = .65) +
      facet_wrap(~type, ncol = 1, scales = 'free_y', labeller = label_wrap_gen(18)) +
      scale_y_discrete(labels = function(x) stringr::str_wrap(labels[x], 32)) +
      scale_fill_manual(values = pal, guide = 'none') + labs(x = '−log10(adjusted P)', y = NULL) + theme +
      ggh4x::force_panelsizes(cols = grid::unit(40, 'mm'), rows = grid::unit(as.numeric(table(d$type)) * 11, 'mm'))
    caption <- 'Supplied GO results, retaining all supplied terms and ontology identities. Values use minus log10 of adjusted P. The legacy source used natural logarithms with a log10 label; the adapter corrects that display mismatch.'
  } else if (case == 'enrichment-lollipop') {
    stopifnot(!anyDuplicated(d$ID), all(d$pvalue > 0 & d$pvalue <= 1), all(d$Count >= 0))
    d$score <- -log10(d$pvalue)
    d$ID <- factor(d$ID, levels = rev(d$ID)); labels <- setNames(d$Description, d$ID)
    pal <- setNames(RColorBrewer::brewer.pal(11, 'RdBu')[6:1],
      seq(0, max(d$score), length.out = 6))
    p <- ggplot(d, aes(Count, ID)) +
      geom_linerange(aes(xmin = 0, xmax = Count), linewidth = .5, colour = 'grey65') +
      geom_point(aes(colour = score), size = 2) +
      scale_y_discrete(labels = function(x) stringr::str_wrap(labels[x], 30)) +
      scale_colour_gradientn(colours = unname(pal), limits = c(0, max(d$score)),
        name = expression(-log[10](italic(P))),
        guide = guide_colourbar(barheight = grid::unit(30, 'mm'), display = 'rectangles')) +
      scale_x_continuous(n.breaks = 3, labels = scales::label_number(drop0trailing = TRUE, scale_cut = scales::cut_short_scale())) +
      labs(x = 'Gene count', y = NULL) + theme +
      theme(legend.title = element_text(size = 16, face = 'plain')) +
      ggh4x::force_panelsizes(cols = grid::unit(40, 'mm'), rows = grid::unit(max(40, nrow(d) * 12), 'mm'))
    caption <- 'Supplied KEGG results; stems and equal-sized points show gene counts. Color shows minus log10 of the supplied raw P values, from zero to the displayed maximum using the neutral-to-red arm of RdBu. Native ticks follow the current counts; the redundant Count size mapping is removed.'
  } else if (case == 'ranked-gsea') {
    stopifnot(!anyDuplicated(d$ID), all(d$pvalue > 0 & d$pvalue <= 1), all(d$gene_set_size > 0))
    d <- d[order(d$NES, decreasing = TRUE), ]; d$rank <- seq_len(nrow(d))
    d$score <- -log10(d$pvalue)
    d$label_group <- ifelse(d$highlight, d$ID, 'Other gene sets')
    pal <- biomedical_palette(unique(d$label_group), control = 'Other gene sets')
    highlighted <- d[d$highlight, ]
    label_key <- setNames(paste(highlighted$rank, highlighted$ID, sep = ' · '), highlighted$ID)
    p <- ggplot(d, aes(rank, NES)) + geom_hline(yintercept = 0, colour = 'grey80', linewidth = .35) +
      geom_point(aes(size = gene_set_size, alpha = score, fill = label_group), shape = 21, colour = 'black', stroke = .3) +
      ggrepel::geom_text_repel(aes(label = ifelse(highlight, as.character(rank), '')),
        size = 11.5 / ggplot2::.pt, family = 'Arial', seed = 11, max.overlaps = Inf,
        point.padding = .4, box.padding = .5, min.segment.length = 0, max.time = 5, max.iter = 50000) +
      scale_fill_manual(values = pal, breaks = highlighted$ID,
        labels = function(x) stringr::str_wrap(label_key[x], 30), name = 'Gene set (rank)',
        guide = guide_legend(override.aes = list(alpha = 1, size = 2), order = 1)) +
      scale_size_area(max_size = 3, name = 'Genes per set', guide = guide_legend(order = 2, nrow = 1, title.position = 'top')) +
      scale_alpha_continuous(range = c(.25, 1), name = 'Significance', guide = guide_legend(order = 3, nrow = 1, title.position = 'top')) +
      scale_x_continuous(n.breaks = 4) + scale_y_continuous(n.breaks = 4, expand = expansion(mult = .15)) +
      labs(x = 'Gene set rank', y = 'Normalized enrichment score') + theme +
      theme(legend.title = element_text(size = 11.5, face = 'plain')) +
      ggh4x::force_panelsizes(cols = grid::unit(60, 'mm'), rows = grid::unit(95, 'mm'))
    caption <- 'Supplied GSEA results ranked by NES. Point area shows actual genes per set; alpha shows minus log10 of raw P. Named highlight flags select pathways before drawing. Native rank labels link to a native pathway key; grey points are other gene sets. The legacy setSize/10 column is restored to gene count and the misleading proportion label is removed.'
  } else stop('Unknown enrichment case')
  export_tidyplots(p, file.path(out, 'figure'))
  write.csv(d, file.path(out, 'display_values.csv'), row.names = FALSE)
  write.csv(data.frame(group = names(pal), color = unname(pal)), file.path(out, 'palette.csv'), row.names = FALSE)
  writeLines(caption, file.path(out, 'caption.txt'))
  writeLines(capture.output(sessionInfo()), file.path(out, 'session-info.txt'))
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  render_enrichment_case(args[1], read.csv(args[2], check.names = FALSE), args[3])
}
