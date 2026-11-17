library(ggplot2)
library(cowplot)
d <- read.csv("input.csv")
font_pt <- 11
theme_set(theme_cowplot(font_size = font_pt, font_family = "Arial") +
  theme(axis.text = element_text(size = font_pt), legend.text = element_text(size = font_pt),
        strip.text = element_text(size = font_pt), legend.position = "bottom"))
d$feature <- factor(d$feature, levels = rev(unique(d$feature)))
d$y <- as.numeric(d$feature) + ifelse(d$group == "A", -.14, .14)
p <- ggplot(d, aes(value, y, color = group)) +
  geom_segment(aes(x = 0, xend = value, yend = y), linewidth = .65) + geom_point(size = 2.4) +
  scale_color_manual(values = c(A = "#A6CEE3", B = "#1F78B4")) +
  scale_y_continuous(breaks = seq_along(levels(d$feature)), labels = levels(d$feature)) +
  scale_x_continuous(expand = expansion(mult = c(0, .08))) + labs(x = "Score", y = NULL, color = NULL)
width_mm <- 90; height_mm <- 80

saveRDS(p, "plot.rds")
ggsave("preview.pdf", p, width = width_mm, height = height_mm, units = "mm", device = cairo_pdf)
ggsave("preview.png", p, width = width_mm, height = height_mm, units = "mm", dpi = 300, device = ragg::agg_png, bg = "white")
