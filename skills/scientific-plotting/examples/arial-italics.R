# Compare mathematical symbols with text italics at the same Arial size.
library(ggplot2)
out <- commandArgs(trailingOnly = TRUE)
out <- if (length(out)) out[1] else "arial-italics"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
d <- data.frame(
  method = c("Math symbols", "Quoted text", "Text face"),
  expression = c('italic(SLC7A11)', 'italic("SLC7A11")', "SLC7A11"),
  y = c(4.7, 2.7, 0.7)
)
p <- ggplot(d, aes(x = 0.5, y = y)) +
  geom_text(aes(y = y + 0.8, label = method), family = "Arial", size = 11, size.unit = "pt") +
  geom_text(data = d[1:2, ], aes(label = expression), parse = TRUE,
    family = "Arial", size = 18, size.unit = "pt") +
  geom_text(data = d[3, ], aes(label = expression), fontface = "italic",
    family = "Arial", size = 18, size.unit = "pt") +
  scale_x_continuous(limits = c(0, 1), expand = expansion(mult = 0)) +
  scale_y_continuous(limits = c(0, 6), expand = expansion(mult = 0)) +
  theme_void(base_family = "Arial") +
  theme(plot.margin = margin(2, 2, 2, 2, unit = "pt"))
write.csv(d, file.path(out, "source-labels.csv"), row.names = FALSE)
ggsave(file.path(out, "comparison.png"), p, width = 50, height = 50, units = "mm",
  device = ragg::agg_png, dpi = 600, bg = "white")
ggsave(file.path(out, "comparison.pdf"), p, width = 50, height = 50, units = "mm",
  device = cairo_pdf, family = "Arial", bg = "white",
  symbolfamily = cairoSymbolFont("Arial", usePUA = FALSE))
ggsave(file.path(out, "comparison.svg"), p, width = 50, height = 50, units = "mm",
  device = svglite::svglite, bg = "white")
t <- pdftools::pdf_data(file.path(out, "comparison.pdf"), font_info = TRUE)[[1]]
write.csv(t, file.path(out, "rendered-text.csv"), row.names = FALSE)
stopifnot(all(grepl("Arial", t$font_name)), min(t$font_size) > 10)
