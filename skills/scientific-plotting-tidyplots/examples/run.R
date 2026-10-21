# Synthetic teaching data. Run: Rscript --vanilla examples/run.R OUTPUT
script <- sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)[1])
here <- dirname(normalizePath(script))
shared <- if (file.exists(file.path(here, "scripts", "compact.R"))) here else
  normalizePath(file.path(here, "..", "..", "scientific-plotting"))
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args)) args[1] else "tidyplots-examples"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
library(tidyplots)
library(ggplot2)
source(file.path(shared, "scripts", "compact.R"))
helper <- if (file.exists(file.path(here, "scripts", "tidyplots.R")))
  file.path(here, "scripts", "tidyplots.R") else file.path(here, "..", "scripts", "tidyplots.R")
source(helper)

# Independent biological units; two planned contrasts against Control.
d <- read.csv(file.path(shared, "examples", "groups.csv"), check.names = FALSE)
points <- stack(d)
names(points) <- c("response", "group")
points$group <- factor(points$group, levels = names(d))
points$unit_id <- paste(points$group, rep(seq_len(nrow(d)), ncol(d)), sep = "_")
pal <- biomedical_palette(names(d), control = "Control")
summary <- data.frame(group = factor(names(d), levels = names(d)), n = nrow(d),
                      mean = colMeans(d), sd = vapply(d, sd, numeric(1)))
summary$ymin <- summary$mean - summary$sd
summary$ymax <- summary$mean + summary$sd
tests <- lapply(d[-1], function(y) t.test(y, d$Control))
stats <- data.frame(comparison = paste(names(d)[-1], "minus Control"),
  n_treatment = nrow(d), n_control = nrow(d), difference = colMeans(d[-1]) - mean(d$Control),
  ci_low = vapply(tests, function(t) t$conf.int[1], numeric(1)),
  ci_high = vapply(tests, function(t) t$conf.int[2], numeric(1)),
  p = vapply(tests, function(t) t$p.value, numeric(1)))
stats$p_holm <- p.adjust(stats$p, "holm")
stats$x1 <- 1
stats$x2 <- 2:3
stats$y <- c(13, 16)
stats$label <- p_labels(stats$p_holm, adjusted = TRUE)
p <- points |>
  tidyplot(x = group, y = response, color = group, width = 50, height = 50, unit = "mm") |>
  add_sd_errorbar(width = 0.16, linewidth = 0.4) |>
  add_mean_dash(width = 0.3, linewidth = 0.7) |>
  add_data_points_beeswarm(size = 1.5, cex = 5) |>
  adjust_colors(pal) |>
  adjust_x_axis(title = NULL, labels = c("Control", "Drug\nA", "Drug\nB")) |>
  adjust_y_axis(limits = c(0, 19), padding = c(0, 0)) |>
  add(biomedical_theme(14)) |>
  adjust_font(fontsize = 14, family = "Arial") |>
  adjust_theme_details(axis.title = element_text(size = 16), legend.position = "none",
                       plot.margin = margin(8, 6, 4, 4)) |>
  add(labs(y = expression(italic("TP53") * plain(" RNA (a.u.)")))) |>
  adjust_size(width = 50, height = 50, unit = "mm")
p <- p + p_brackets(stats, p_col = "p_holm", adjusted = TRUE, size = 12,
                    tip = 0.15, text_gap = 0.3)
export_tidyplots(p, file.path(out, "groups"))
write.csv(points, file.path(out, "groups_source.csv"), row.names = FALSE)
write.csv(summary, file.path(out, "groups_summaries.csv"), row.names = FALSE)
write.csv(stats, file.path(out, "groups_statistics.csv"), row.names = FALSE)
write.csv(data.frame(condition = names(pal), color = unname(pal)),
          file.path(out, "groups_palette.csv"), row.names = FALSE)
writeLines("Synthetic teaching example of TP53 RNA abundance. Six independent biological units per group; points with mean and SD. Two-sided Welch tests compare each drug with Control; Holm correction across both planned comparisons. CIs are unadjusted 95% intervals for the mean difference. Only Holm-adjusted P < 0.05 is annotated; the full table retains all results. Plot area: 50 x 50 mm; the export includes labels at their original font sizes.",
           file.path(out, "groups_caption.txt"))

# Six donors; match IDs before testing or connecting observations.
d <- read.csv(file.path(shared, "examples", "paired.csv"))
points <- data.frame(donor = rep(d$donor, 2),
  visit = factor(rep(c("Before", "After"), each = nrow(d)), levels = c("Before", "After")),
  response = c(d$Before, d$After))
points$position <- as.numeric(points$visit) + rep(c(-0.08, 0.08, -0.04, 0, 0.04, 0), 2)
test <- t.test(d$After, d$Before, paired = TRUE)
stats <- data.frame(comparison = "After minus Before", n_pairs = nrow(d),
  difference = mean(d$After - d$Before), ci_low = test$conf.int[1],
  ci_high = test$conf.int[2], p = test$p.value, x1 = 1, x2 = 2, y = 10.8)
stats$label <- p_labels(stats$p)
pal <- biomedical_palette(c("Before", "After"), control = "Before")
p <- points |>
  tidyplot(x = position, y = response, color = visit, width = 50, height = 50, unit = "mm") |>
  add_line(group = donor, color = "grey70", linewidth = 0.4) |>
  add_data_points(size = 1.8) |>
  adjust_colors(pal) |>
  adjust_x_axis(title = NULL, breaks = 1:2,
                labels = c("Before\nstimulation", "After\nstimulation"), limits = c(0.6, 2.4)) |>
  adjust_y_axis(limits = c(5, 12), padding = c(0, 0)) |>
  add(biomedical_theme(14)) |>
  adjust_font(fontsize = 14, family = "Arial") |>
  adjust_theme_details(axis.title = element_text(size = 16), legend.position = "none",
                       plot.margin = margin(8, 6, 4, 4)) |>
  add(labs(y = expression(plain("Ca")^{plain("2+")} * plain(" signal (a.u.)")))) |>
  adjust_size(width = 50, height = 50, unit = "mm")
p <- p + p_brackets(stats, p_col = "p", size = 12, tip = 0.12, text_gap = 0.11)
export_tidyplots(p, file.path(out, "paired"))
write.csv(d, file.path(out, "paired_source.csv"), row.names = FALSE)
write.csv(points, file.path(out, "paired_plot_data.csv"), row.names = FALSE)
write.csv(stats, file.path(out, "paired_statistics.csv"), row.names = FALSE)
write.csv(data.frame(condition = names(pal), color = unname(pal)),
          file.path(out, "paired_palette.csv"), row.names = FALSE)
writeLines("Synthetic teaching example of calcium signal in arbitrary units. Six matched donors; each line joins the same donor before and after stimulation. Horizontal offsets separate points while retaining the pairing and measured y values. Two-sided paired t-test, one planned comparison, no multiplicity correction; unadjusted 95% CI of mean within-donor change. Only P < 0.05 is annotated; the full result is saved. Plot area: 50 x 50 mm; the export includes labels at their original font sizes.",
           file.path(out, "paired_caption.txt"))

# Repeated units with irregular time spacing; break at interior missing values.
d <- read.csv(file.path(shared, "examples", "trajectory.csv"))
points <- data.frame(time = rep(d$time, ncol(d) - 1),
  replicate = rep(names(d)[-1], each = nrow(d)), response = unlist(d[-1], use.names = FALSE))
points$condition <- factor(sub("_[0-9]+$", "", points$replicate), levels = c("Control", "Treated"))
points$segment <- ave(is.na(points$response), points$replicate, FUN = cumsum)
points$line_id <- interaction(points$replicate, points$segment)
points$included <- !is.na(points$response)
observed <- points[points$included, ]
pal <- biomedical_palette(levels(points$condition), control = "Control")
p <- observed |>
  tidyplot(x = time, y = response, color = condition, width = 50, height = 50, unit = "mm") |>
  add_line(group = line_id, linewidth = 0.4) |>
  add_data_points(size = 1.5) |>
  adjust_colors(pal) |>
  adjust_x_axis(title = "Time (min)", breaks = c(0, 20, 40, 60)) |>
  adjust_y_axis(title = "Response (a.u.)", limits = c(0.8, 2.5)) |>
  add(biomedical_theme(14)) |>
  adjust_font(fontsize = 14, family = "Arial") |>
  adjust_theme_details(axis.title = element_text(size = 16), legend.position = "none",
                       strip.text = element_text(size = 14, family = "Arial"),
                       plot.margin = margin(8, 6, 4, 4)) |>
  adjust_size(width = 50, height = 50, unit = "mm") |>
  split_plot(by = condition, ncol = 2, axes = "all", axis.titles = "margins", scales = "fixed")
export_tidyplots(p, file.path(out, "trajectory"))
write.csv(points, file.path(out, "trajectory_source.csv"), row.names = FALSE, na = "")
write.csv(observed, file.path(out, "trajectory_plot_data.csv"), row.names = FALSE)
write.csv(data.frame(condition = names(pal), color = unname(pal)),
          file.path(out, "trajectory_palette.csv"), row.names = FALSE)
writeLines("Synthetic teaching example. Three biological units per condition measured repeatedly at 0, 10, 20, 40 and 60 min. Dots and lines retain actual numeric time spacing. Each line connects a contiguous observed segment within one unit; two interior missing values remain blank in source data and break those lines. Facets use shared y scales. Descriptive display; no inferential test. Each facet plot area: 50 x 50 mm; the export includes labels at their original font sizes.",
           file.path(out, "trajectory_caption.txt"))

# Copy only the files needed to rerun this delivery outside the installed package.
dir.create(file.path(out, "scripts"), showWarnings = FALSE)
dir.create(file.path(out, "examples"), showWarnings = FALSE)
if (normalizePath(out) != here) file.copy(script, file.path(out, "run.R"), overwrite = TRUE)
if (normalizePath(out) != normalizePath(shared)) {
  file.copy(file.path(shared, "scripts", "compact.R"), file.path(out, "scripts"), overwrite = TRUE)
  file.copy(file.path(shared, "examples", c("groups.csv", "paired.csv", "trajectory.csv")),
            file.path(out, "examples"), overwrite = TRUE)
  file.copy(helper, file.path(out, "scripts", "tidyplots.R"), overwrite = TRUE)
}
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo.txt"))
cat("Examples saved to", normalizePath(out), "\n")
