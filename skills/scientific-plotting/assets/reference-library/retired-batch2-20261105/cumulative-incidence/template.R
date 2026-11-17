library(ggplot2)
library(cowplot)
d <- read.csv("input.csv")
font_pt <- 11
theme_set(theme_cowplot(font_size = font_pt, font_family = "Arial") +
  theme(axis.text = element_text(size = font_pt), legend.text = element_text(size = font_pt),
        strip.text = element_text(size = font_pt), legend.position = "bottom"))
fit <- cmprsk::cuminc(d$time, d$status, d$group, cencode = 0)
curves <- do.call(rbind, lapply(setdiff(names(fit), "Tests"), function(k) {
  parts <- strsplit(k, " ")[[1]]
  data.frame(time = fit[[k]]$time, incidence = fit[[k]]$est, group = parts[1],
             event = paste("Event", parts[2]))
}))
write.csv(curves, "estimates.csv", row.names = FALSE)
p <- ggplot(curves, aes(time, incidence, color = group)) + geom_step(linewidth = .7) +
  facet_wrap(~event) + scale_color_manual(values = c(A = "#A6CEE3", B = "#1F78B4")) +
  scale_y_continuous(limits = c(0, 1), breaks = c(0, .5, 1)) +
  labs(x = "Time", y = "Cumulative incidence", color = NULL)
width_mm <- 125; height_mm <- 85

saveRDS(p, "plot.rds")
ggsave("preview.pdf", p, width = width_mm, height = height_mm, units = "mm", device = cairo_pdf)
ggsave("preview.png", p, width = width_mm, height = height_mm, units = "mm", dpi = 300, device = ragg::agg_png, bg = "white")
