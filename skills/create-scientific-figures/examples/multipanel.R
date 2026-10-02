# Synthetic split-donor experiment. Run: Rscript --vanilla multipanel.R OUTPUT
script <- sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)[1])
here <- dirname(normalizePath(script))
skill <- if (file.exists(file.path(here, "..", "scripts", "compact.R"))) dirname(here) else here
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args)) args[1] else "multipanel-example"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
library(ggplot2)
source(file.path(skill, "scripts", "compact.R"))
cowplot::set_null_device("agg")

# Four donors each supply one control and one treated aliquot; IDs link all panels.
conditions <- c("Control", "Treated")
d <- data.frame(sample = paste0(rep(c("C", "T"), each = 4), 1:4),
  donor = rep(paste0("D", 1:4), 2), condition = rep(conditions, each = 4),
  initial_cells = 1000 * c(86, 101, 109, 94, 88, 99, 111, 95),
  viability_pct = c(94, 91, 96, 92, 81, 75, 84, 78))
d$condition <- factor(d$condition, conditions)
d$x <- as.numeric(d$condition) + rep(c(-.09, -.03, .03, .09), 2)
pal <- biomedical_palette(conditions, control = "Control")
shapes <- c(Control = 1, Treated = 17)

trajectory <- expand.grid(minute = c(0, 10, 20, 40, 60), sample = d$sample,
                          stringsAsFactors = FALSE)
trajectory <- merge(trajectory, d[c("sample", "donor", "condition")], by = "sample", sort = FALSE)
trajectory <- trajectory[order(match(trajectory$sample, d$sample), trajectory$minute), ]
trajectory$signal <- c(1.02, 1.12, 1.21, 1.34, 1.39, .94, 1.03, 1.15, 1.22, 1.28,
  1.08, 1.18, 1.26, 1.42, 1.46, .98, 1.10, 1.18, 1.30, 1.35,
  1.01, 1.28, 1.56, 2.08, 2.24, .96, 1.19, 1.43, 1.87, 2.06,
  1.06, 1.32, NA, 2.16, 2.37, .99, 1.23, 1.51, 1.99, 2.17)
trajectory$segment <- ave(is.na(trajectory$signal), trajectory$sample, FUN = cumsum)
observed <- trajectory[!is.na(trajectory$signal), ]
observed$line <- interaction(observed$sample, observed$segment, drop = TRUE)

analytes <- data.frame(sample = rep(d$sample, 3), analyte = rep(c("A", "B", "C"), each = 8),
  abundance = c(8.2, 7.5, 9.0, 8.0, 13.1, 11.8, 14.0, 12.4,
                15.0, 13.8, 16.1, 14.4, 10.1, 9.4, 11.0, 9.8,
                5.2, 4.8, 5.7, 5.0, 5.5, 5.0, 6.1, 5.3))
analytes$z <- ave(analytes$abundance, analytes$analyte, FUN = function(x) as.numeric(scale(x)))
analytes$sample <- factor(analytes$sample, rev(d$sample))
stopifnot(all(table(d$donor, d$condition) == 1), !anyDuplicated(d$sample),
  nrow(observed) == 39, sum(is.na(trajectory$signal)) == 1,
  observed$line[observed$sample == "T3" & observed$minute == 10] !=
    observed$line[observed$sample == "T3" & observed$minute == 40],
  all(abs(tapply(analytes$z, analytes$analyte, mean)) < 1e-12),
  all(abs(tapply(analytes$z, analytes$analyte, sd) - 1) < 1e-12))

base <- biomedical_theme(11) + theme(axis.title = element_text(size = 11),
  legend.position = "none", plot.margin = margin(5, 5, 4, 6))
a <- ggplot(d, aes(x, initial_cells / 1000, colour = condition, shape = condition)) +
  geom_point(size = 2) + scale_colour_manual(values = pal) + scale_shape_manual(values = shapes) +
  scale_x_continuous(breaks = 1:2, labels = conditions, limits = c(.6, 2.4)) +
  scale_y_continuous(breaks = c(80, 100, 120), limits = c(75, 125)) +
  labs(x = NULL, y = "Initial cells (thousands)") + base
b <- ggplot(d, aes(x, viability_pct)) +
  geom_line(aes(group = donor), colour = "#B0B0B0", linewidth = .45) +
  geom_point(aes(colour = condition, shape = condition), size = 2) +
  scale_colour_manual(values = pal) + scale_shape_manual(values = shapes) +
  scale_x_continuous(breaks = 1:2, labels = conditions, limits = c(.6, 2.4)) +
  scale_y_continuous(breaks = c(70, 80, 90, 100), limits = c(70, 100)) +
  labs(x = NULL, y = "Viability at 60 min (%)") + base
c <- ggplot(observed, aes(minute, signal, colour = condition)) +
  geom_line(aes(group = line), linewidth = .4, alpha = .65) +
  geom_point(aes(shape = condition), size = 1.7) +
  scale_colour_manual(values = pal) + scale_shape_manual(values = shapes) +
  scale_x_continuous(breaks = c(0, 20, 40, 60)) +
  scale_y_continuous(breaks = c(1, 1.5, 2, 2.5), limits = c(.8, 2.5)) +
  labs(x = "Time (min)", y = "Fluorescence (a.u.)") + base
h <- ggplot(analytes, aes(analyte, sample, fill = z)) +
  geom_tile(colour = "white", linewidth = .4) + coord_fixed(ratio = .55) +
  scale_fill_gradient2(low = "#2166AC", mid = "white", high = "#B2182B", midpoint = 0,
    limits = c(-2, 2), breaks = c(-2, 0, 2), name = "Z score") +
  scale_x_discrete(expand = expansion(0)) + scale_y_discrete(expand = expansion(0)) +
  labs(x = "Endpoint analyte", y = NULL) + base +
  theme(axis.line = element_blank(), axis.ticks = element_blank(), legend.position = "right",
    legend.title = element_text(size = 11), legend.key.height = grid::unit(6, "mm"),
    legend.key.width = grid::unit(3, "mm"))
# Signed values retain direction in grayscale; choose ink from actual rendered tile fills.
rgb <- t(grDevices::col2rgb(ggplot_build(h)$data[[1]]$fill) / 255)
linear <- ifelse(rgb <= .04045, rgb / 12.92, ((rgb + .055) / 1.055)^2.4)
luminance <- drop(linear %*% c(.2126, .7152, .0722))
black_contrast <- (luminance + .05) / .05
white_contrast <- 1.05 / (luminance + .05)
labels <- transform(analytes, label = sprintf("%+.1f", round(z, 1)),
                    ink = ifelse(black_contrast >= white_contrast, "black", "white"))
h <- h + geom_text(data = labels, aes(label = label, colour = ink),
                   family = "Arial", size = 11, size.unit = "pt") + scale_colour_identity()
stopifnot(nrow(ggplot_build(h)$data[[2]]) == 24,
          all(pmax(black_contrast, white_contrast) >= 4.5))

# Check rendered pairing/points and the missing segment, not just input row counts.
paired_lines <- ggplot_build(b)$data[[1]]
expected <- d[order(d$donor, d$x), ]
time_layers <- ggplot_build(c)$data
t3_groups <- as.integer(unique(observed$line[observed$sample == "T3"]))
t3_lines <- split(time_layers[[1]]$x[time_layers[[1]]$group %in% t3_groups],
                 time_layers[[1]]$group[time_layers[[1]]$group %in% t3_groups])
stopifnot(identical(paired_lines$x, expected$x), identical(paired_lines$y, expected$viability_pct),
  identical(paired_lines$group, match(expected$donor, sort(unique(d$donor)))),
  identical(time_layers[[2]]$x, observed$minute), identical(time_layers[[2]]$y, observed$signal),
  length(t3_lines) == 2,
  all(vapply(t3_lines, function(x) all(x <= 10) || all(x >= 40), logical(1))),
  nrow(ggplot_build(h)$data[[1]]) == nrow(analytes))
aligned <- cowplot::align_plots(a, b, c, align = "v", axis = "lr")
ragg::agg_capture(width = 90, height = 65, units = "mm", res = 300)
left_mm <- vapply(aligned, function(g) grid::convertWidth(
  sum(g$widths[seq_len(g$layout$l[g$layout$name == "panel"] - 1)]), "mm", TRUE), numeric(1))
right_mm <- vapply(aligned, function(g) grid::convertWidth(
  sum(g$widths[(g$layout$r[g$layout$name == "panel"] + 1):length(g$widths)]), "mm", TRUE), numeric(1))
invisible(dev.off())
stopifnot(diff(range(left_mm)) < .01, diff(range(right_mm)) < .01)
legend <- cowplot::get_legend(a + theme(legend.position = "top", legend.justification = "center"))
body <- cowplot::plot_grid(plotlist = c(aligned, list(h)), ncol = 2,
  labels = letters[1:4], label_size = 12, label_fontfamily = "Arial", label_fontface = "bold",
  hjust = 0, label_x = 0, rel_heights = c(1, 1.15))
assembly <- cowplot::plot_grid(legend, body, ncol = 1, rel_heights = c(8, 137))
saveRDS(list(initial = a, paired = b, trajectory = c, heatmap = h), file.path(out, "panels.rds"))
saveRDS(pal, file.path(out, "condition_palette.rds"))
export_biomedical(assembly, file.path(out, "multipanel"), 180, 145, placed_width_mm = 180)
write.csv(d, file.path(out, "aliquots_source.csv"), row.names = FALSE)
write.csv(trajectory, file.path(out, "trajectory_source.csv"), row.names = FALSE, na = "")
write.csv(analytes, file.path(out, "analytes_source_and_display.csv"), row.names = FALSE)
write.csv(data.frame(condition = names(pal), colour = unname(pal), shape = shapes[names(pal)]),
          file.path(out, "condition_palette.csv"), row.names = FALSE)
writeLines(c(
  "Synthetic teaching example: one split-donor experiment, with four donors (D1-D4), each providing a Control (C1-C4) and Treated (T1-T4) aliquot. These are constructed values, not biological results.",
  "a, Initial cell counts in thousands, one observation per aliquot. b, Viability at 60 min; gray lines pair the same donor across conditions. Small horizontal offsets separate donor points without changing values.",
  "c, Fluorescence from the same aliquots at 0, 10, 20, 40 and 60 min. Points show all 39 available observations; individual lines preserve actual time spacing and break around the missing T3 value at 20 min. No interpolation or group averaging is applied.",
  "d, Endpoint abundance of three generic analytes A-C, measured in arbitrary units in the same eight aliquots. Each analyte is centered by its mean across all eight aliquots and divided by its sample SD using base R scale(); colors show these analyte-wise z scores, not raw abundance. Signed values rounded to one decimal preserve direction and magnitude in grayscale; black or white text is selected for contrast against the actual tile fill. All 24 raw and full-precision display values are saved. Sample order is fixed; no clustering or gene set is used.",
  "No inferential tests are performed. Conditions share a single gray/purple and circle/triangle key. The heatmap has its own diverging scale centered at zero; its cells use an intentional fixed y/x aspect ratio of 0.55.",
  "The quantitative panels have matching left/right margins. The fixed-aspect heatmap is positioned independently so its geometry is retained. Composition is 180 x 145 mm and reviewed at 180 mm width; all text is Arial and exceeds 10 pt. The assembled PDF, PNG, RDS, individual panel objects, source tables and export measurements accompany this script."),
  file.path(out, "caption.txt"))
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo.txt"))
if (normalizePath(out) != here) file.copy(script, file.path(out, "multipanel.R"), overwrite = TRUE)
dir.create(file.path(out, "scripts"), showWarnings = FALSE)
if (normalizePath(file.path(out, "scripts")) != normalizePath(file.path(skill, "scripts")))
  file.copy(file.path(skill, "scripts", "compact.R"), file.path(out, "scripts", "compact.R"), overwrite = TRUE)
cat("Four-panel example saved to", normalizePath(out), "\n")
