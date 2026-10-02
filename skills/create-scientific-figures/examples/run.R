# Synthetic teaching data; run all examples with Rscript --vanilla examples/run.R OUTPUT.
script <- sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)[1])
examples <- dirname(normalizePath(script))
skill <- if (file.exists(file.path(examples, "..", "scripts", "compact.R"))) dirname(examples) else examples
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args)) args[1] else "figure-examples"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
library(ggplot2)
source(file.path(skill, "scripts", "compact.R"))
source(file.path(skill, "scripts", "prism.R"))

# Independent groups: one observation per biological replicate.
d <- read.csv(file.path(examples, "groups.csv"), check.names = FALSE)
long <- stack(d)
names(long) <- c("response", "group")
long$group <- factor(long$group, levels = names(d))
pal <- biomedical_palette(names(d), control = "Control")
s <- data.frame(group = factor(names(d), levels = names(d)),
                mean = colMeans(d), sd = vapply(d, sd, numeric(1)))
tests <- lapply(d[-1], function(y) t.test(y, d$Control))
stats <- data.frame(comparison = paste(names(d)[-1], "vs Control"),
  n_treatment = nrow(d), n_control = nrow(d), difference = colMeans(d[-1]) - mean(d$Control),
  ci_low = vapply(tests, function(t) t$conf.int[1], numeric(1)),
  ci_high = vapply(tests, function(t) t$conf.int[2], numeric(1)),
  p = vapply(tests, function(t) t$p.value, numeric(1)))
stats$p_holm <- p.adjust(stats$p, "holm")
ann <- data.frame(x1 = 1, x2 = 2:3, y = c(12, 13.8), p_holm = stats$p_holm)
p <- ggplot(long, aes(group, response, colour = group)) +
  geom_errorbar(data = s, aes(y = mean, ymin = mean - sd, ymax = mean + sd), width = .16) +
  geom_point(position = position_jitter(width = .08, height = 0, seed = 1), size = 2) +
  geom_errorbar(data = s, aes(y = mean, ymin = mean, ymax = mean), width = .28, linewidth = .7) +
  p_brackets(ann, p_col = "p_holm", adjusted = TRUE, tip = .15, size = 11) +
  scale_colour_manual(values = pal) + scale_y_continuous(limits = c(0, 15.2)) +
  labs(x = NULL, y = "Response (a.u.)") + biomedical_theme(12) + theme(legend.position = "none")
export_biomedical(p, file.path(out, "groups"), 90, 80)
write.csv(long, file.path(out, "groups_source.csv"), row.names = FALSE)
write.csv(s, file.path(out, "groups_summaries.csv"), row.names = FALSE)
write.csv(stats, file.path(out, "groups_statistics.csv"), row.names = FALSE)
write_prism(d, file.path(out, "groups.pzfx"), title = "Independent groups (synthetic)", overwrite = TRUE)
writeLines("Synthetic demonstration. Six independent observations per group; dots, mean and SD. Two-sided Welch tests compare each drug with Control; Holm adjustment across the two tests. Intervals are unadjusted 95% confidence intervals of each mean difference. Prism file contains editable input data; tests and styling are produced by this R script.", file.path(out, "groups_caption.txt"))

# Paired observations: preserve each donor's row in R and Prism.
d <- read.csv(file.path(examples, "paired.csv"))
long <- data.frame(donor = rep(d$donor, 2), time = rep(c("Before", "After"), each = nrow(d)),
                   response = c(d$Before, d$After))
long$time <- factor(long$time, levels = c("Before", "After"))
long$position <- as.numeric(long$time) + rep(c(-.08, .08, -.04, 0, .04, 0), 2)
test <- t.test(d$After, d$Before, paired = TRUE)
stats <- data.frame(comparison = "After minus Before", n_pairs = nrow(d),
  difference = mean(d$After - d$Before), ci_low = test$conf.int[1], ci_high = test$conf.int[2], p = test$p.value)
pal <- biomedical_palette(c("Before", "After"), control = "Before")
p <- ggplot(long, aes(position, response)) + geom_line(aes(group = donor), colour = "#AAAAAA", linewidth = .4) +
  geom_point(aes(colour = time), size = 2) + scale_colour_manual(values = pal) +
  scale_x_continuous(breaks = 1:2, labels = c("Before", "After"), limits = c(.6, 2.4)) +
  p_brackets(data.frame(x1 = 1, x2 = 2, y = 10.8, p = test$p.value), p_col = "p", tip = .12, size = 11) +
  scale_y_continuous(limits = c(5, 12)) + labs(x = NULL, y = "Response (a.u.)") +
  biomedical_theme(12) + theme(legend.position = "none")
export_biomedical(p, file.path(out, "paired"), 90, 75)
write.csv(d, file.path(out, "paired_source.csv"), row.names = FALSE)
write.csv(stats, file.path(out, "paired_statistics.csv"), row.names = FALSE)
write_prism(d, file.path(out, "paired.pzfx"), id = "donor", title = "Paired donors (synthetic)", overwrite = TRUE)
write.csv(long, file.path(out, "paired_plot_data.csv"), row.names = FALSE)
writeLines("Synthetic demonstration. Six matched donors; each line joins the same donor before and after treatment. Small horizontal offsets separate nearby points. Two-sided paired t-test and 95% confidence interval of the within-donor mean change; one planned comparison, no multiplicity correction. Donor IDs remain aligned as Prism row titles; choose paired analysis in Prism if recalculating.", file.path(out, "paired_caption.txt"))

# Repeated trajectories: keep actual time spacing and break lines at missing values.
d <- read.csv(file.path(examples, "trajectory.csv"))
long <- data.frame(time = rep(d$time, ncol(d) - 1),
  replicate = rep(names(d)[-1], each = nrow(d)), response = unlist(d[-1], use.names = FALSE))
long$condition <- sub("_[0-9]+$", "", long$replicate)
long$segment <- ave(is.na(long$response), long$replicate, FUN = cumsum)
observed <- long[!is.na(long$response), ]
pal <- biomedical_palette(c("Control", "Treated"), control = "Control")
p <- ggplot(observed, aes(time, response, colour = condition)) +
  geom_line(aes(group = interaction(replicate, segment)), linewidth = .5, alpha = .6) +
  geom_point(size = 1.7) + scale_colour_manual(values = pal) +
  scale_x_continuous(breaks = c(0, 20, 40, 60)) +
  labs(x = "Time (min)", y = "Response (a.u.)") + biomedical_theme(12) +
  theme(legend.position = "top")
export_biomedical(p, file.path(out, "trajectory"), 90, 80)
write.csv(long, file.path(out, "trajectory_source.csv"), row.names = FALSE, na = "")
write.csv(aggregate(response ~ condition + time, observed, function(x) c(n = length(x), mean = mean(x), sd = sd(x))),
          file.path(out, "trajectory_summaries.csv"), row.names = FALSE)
write_prism(d, file.path(out, "trajectory.pzfx"), x = "time",
  groups = setNames(sub("_[0-9]+$", "", names(d)[-1]), names(d)[-1]),
  title = "Repeated trajectories (synthetic)", overwrite = TRUE)
writeLines("Synthetic demonstration. Three biological replicates per condition measured repeatedly at 0, 10, 20, 40 and 60 minutes. Lines connect adjacent available measurements within a replicate and break at the two missing observations. No inferential test is performed. CSV and Prism replicate subcolumns retain the missing values as blanks.", file.path(out, "trajectory_caption.txt"))
write.csv(data.frame(condition = names(pal), colour = unname(pal)), file.path(out, "trajectory_colors.csv"), row.names = FALSE)
if (normalizePath(out) != examples)
  file.copy(file.path(examples, c("run.R", "groups.csv", "paired.csv", "trajectory.csv")), out, overwrite = TRUE)
dir.create(file.path(out, "scripts"), showWarnings = FALSE)
if (normalizePath(file.path(out, "scripts")) != normalizePath(file.path(skill, "scripts")))
  file.copy(file.path(skill, "scripts", c("compact.R", "prism.R")), file.path(out, "scripts"), overwrite = TRUE)
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo.txt"))
cat("Examples saved to", normalizePath(out), "\n")
