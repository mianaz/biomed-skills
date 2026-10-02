# Six synthetic examples. Run: Rscript --vanilla examples/gallery.R OUTPUT_DIR
script <- sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)[1])
examples <- dirname(normalizePath(script))
skill <- if (file.exists(file.path(examples, "..", "scripts", "compact.R"))) dirname(examples) else examples
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop("Usage: Rscript --vanilla gallery.R OUTPUT_DIR")
out <- args[1]
library(ggplot2)
source(file.path(skill, "scripts", "compact.R"))
source(file.path(skill, "scripts", "dose_response.R"))
for (case in c("independent", "paired", "repeated", "dose_response", "survival", "heatmap"))
  dir.create(file.path(out, case), recursive = TRUE, showWarnings = FALSE)
pal <- biomedical_palette(c("Control", "A", "B"), control = "Control")

# Independent units: compute the complete two-comparison family before hiding NS.
d <- data.frame(id = sprintf("U%02d", 1:24),
  group = rep(c("Control", "A", "B"), each = 8),
  value = c(9.1, 10.2, 10.8, 9.6, 11.1, 10.0, 8.9, 10.5,
            13.1, 14.2, 12.8, 15.0, 13.8, 14.6, 12.5, 14.0,
            9.4, 10.8, 9.8, 11.3, 10.2, 9.7, 11.1, 10.5))
d$x <- match(d$group, c("Control", "A", "B"))
d$offset <- rep(c(-.13, -.09, -.05, -.02, .02, .05, .09, .13), 3)
fits <- setNames(lapply(c("A", "B"), function(g)
  t.test(d$value[d$group == g], d$value[d$group == "Control"])), c("A", "B"))
stats <- do.call(rbind, lapply(names(fits), function(g) {
  f <- fits[[g]]
  data.frame(comparison = paste(g, "minus Control"), n_group = 8, n_control = 8,
    difference = unname(f$estimate[1] - f$estimate[2]), low = f$conf.int[1], high = f$conf.int[2],
    t = unname(f$statistic), df = unname(f$parameter), p_raw = f$p.value,
    method = "Two-sided Welch t-test; unadjusted 95% CI for group minus Control")
}))
stats$p_holm <- p.adjust(stats$p_raw, "holm")
shuffled <- d[rev(seq_len(nrow(d))), ]
stopifnot(all.equal(unname(vapply(fits, function(f) f$p.value, numeric(1))),
  vapply(c("A", "B"), function(g) t.test(shuffled$value[shuffled$group == g],
    shuffled$value[shuffled$group == "Control"])$p.value, numeric(1)), check.attributes = FALSE))
s <- aggregate(value ~ group + x, d, function(x) c(mean = mean(x), sd = sd(x)))
s <- data.frame(s[1:2], s$value)
s$summary_x <- s$x + .29
rows <- data.frame(x1 = 1, x2 = 2:3, p = stats$p_holm)
rows$label <- p_labels(rows$p, adjusted = TRUE)
rows <- rows[nzchar(rows$label), ]
rows$y <- 16 + .9 * (seq_len(nrow(rows)) - 1)
p <- ggplot(d, aes(x + offset, value, colour = group)) +
  geom_errorbar(data = s, aes(summary_x, ymin = mean - sd, ymax = mean + sd),
                inherit.aes = FALSE, width = .13, linewidth = .45) +
  geom_segment(data = s, aes(x = summary_x - .065, xend = summary_x + .065, y = mean, yend = mean),
               inherit.aes = FALSE, linewidth = .6) +
  geom_point(size = 2.3) +
  scale_colour_manual(values = pal, guide = "none") +
  scale_x_continuous(breaks = 1:3, labels = c("Control", "A", "B"), limits = c(.6, 3.55)) +
  scale_y_continuous(limits = c(7.5, max(rows$y) + 1.5), breaks = c(8, 10, 12, 14, 16),
                     expand = expansion(0)) +
  labs(x = NULL, y = "Signal (a.u.)") + biomedical_theme(size = 12) +
  p_brackets(rows, p_col = "p", adjusted = TRUE, size = 12, tip = .15)
write.csv(d, file.path(out, "independent/source_data.csv"), row.names = FALSE)
write.csv(stats, file.path(out, "independent/statistics.csv"), row.names = FALSE)
write.csv(s, file.path(out, "independent/summary_statistics.csv"), row.names = FALSE)
saveRDS(fits, file.path(out, "independent/models.rds"))
export_biomedical(p, file.path(out, "independent/figure"), 90, 78, 90)

# Paired units: identify pairs by ID; never assume row order gives the pairing.
wide <- data.frame(id = sprintf("P%02d", 1:8),
  Before = c(8.5, 11.1, 9.8, 12.0, 8.9, 10.5, 11.8, 9.4),
  After = c(11.7, 13.3, 12.7, 14.6, 12.6, 12.4, 15.1, 11.9))
d <- reshape(wide, varying = list(c("Before", "After")), v.names = "value",
  timevar = "condition", times = c("Before", "After"), direction = "long", idvar = "id")
d$condition <- factor(d$condition, levels = c("Before", "After"))
d$x <- as.integer(d$condition)
d$plot_x <- d$x + c(-.10, -.07, -.04, -.01, .01, .04, .07, .10)[match(d$id, wide$id)]
paired <- merge(d[d$condition == "Before", c("id", "value")],
  d[rev(which(d$condition == "After")), c("id", "value")],
  by = "id", suffixes = c("_before", "_after"))
f <- t.test(paired$value_after - paired$value_before)
stopifnot(nrow(paired) == 8, !anyDuplicated(paired$id),
  all.equal(unname(f$estimate), mean(wide$After - wide$Before)))
stats <- data.frame(comparison = "After minus Before", n_pairs = nrow(paired),
  difference = unname(f$estimate), low = f$conf.int[1], high = f$conf.int[2],
  t = unname(f$statistic), df = unname(f$parameter), p_raw = f$p.value,
  method = "Two-sided one-sample t-test of paired differences; 95% t CI; one contrast")
rows <- data.frame(x1 = 1, x2 = 2, y = 16.1, p = f$p.value)
p <- ggplot(d, aes(plot_x, value, group = id)) +
  geom_line(colour = "#B5B5B5", linewidth = .55) +
  geom_point(aes(colour = condition), size = 2.5) +
  scale_colour_manual(values = c(Before = unname(pal["Control"]), After = unname(pal["A"])), guide = "none") +
  scale_x_continuous(breaks = 1:2, labels = c("Before", "After"), limits = c(.7, 2.3)) +
  scale_y_continuous(limits = c(7.5, 18), breaks = seq(8, 16, 2), expand = expansion(0)) +
  labs(x = NULL, y = "Signal (a.u.)") + biomedical_theme(size = 12) +
  p_brackets(rows, p_col = "p", size = 12, tip = .15)
write.csv(d, file.path(out, "paired/source_data.csv"), row.names = FALSE)
write.csv(stats, file.path(out, "paired/statistics.csv"), row.names = FALSE)
saveRDS(f, file.path(out, "paired/model.rds"))
export_biomedical(p, file.path(out, "paired/figure"), 90, 78, 90)

# Repeated observations: a random intercept retains within-unit dependence.
d <- expand.grid(day = c(0, 2, 4, 6), id = sprintf("R%02d", 1:12))
d$unit <- match(d$id, sprintf("R%02d", 1:12))
d$group <- factor(ifelse(d$unit <= 6, "Control", "A"), levels = c("Control", "A"))
intercepts <- c(-1.5, -.8, .3, 1.2, -.2, 1, -1.1, .9, -.4, 1.3, .2, -.7)
noise <- c(-.3, .4, -.1, .2, .2, -.4, .3, -.2, .1, -.2, .4, -.3,
  .3, -.1, -.4, .2, -.2, .3, .1, -.4, .4, -.3, .2, -.1,
  -.1, .3, -.3, .2, .2, -.2, .4, -.3, -.4, .2, -.1, .3,
  .3, -.4, .2, -.1, -.2, .1, -.3, .4, .1, .4, -.2, -.3)
d$value <- 10 + intercepts[d$unit] + .25 * d$day +
  ifelse(d$group == "A", .65 * d$day, 0) + noise
f <- nlme::lme(value ~ group * day, random = ~1 | id, data = d, method = "REML")
fr <- nlme::lme(value ~ group * day, random = ~1 | id, data = d[rev(seq_len(nrow(d))), ], method = "REML")
stopifnot(all.equal(nlme::fixef(f), nlme::fixef(fr), tolerance = 1e-8))
tab <- as.data.frame(summary(f)$tTable)
stats <- data.frame(term = rownames(tab), estimate = tab$Value, se = tab$Std.Error,
  df = tab$DF, low = tab$Value - qt(.975, tab$DF) * tab$Std.Error,
  high = tab$Value + qt(.975, tab$DF) * tab$Std.Error, p_raw = tab[["p-value"]],
  prespecified_contrast = rownames(tab) == "groupA:day")
g <- expand.grid(day = seq(0, 6, .1), group = levels(d$group))
g$group <- factor(g$group, levels = levels(d$group))
g$value <- as.numeric(predict(f, g, level = 0))
p <- ggplot(d, aes(day, value, colour = group)) +
  geom_line(aes(group = id), linewidth = .45, alpha = .4) +
  geom_line(data = g, linewidth = 1) +
  geom_point(size = 1.7, alpha = .8) +
  scale_colour_manual(values = pal[c("Control", "A")]) +
  scale_x_continuous(breaks = c(0, 2, 4, 6)) +
  scale_y_continuous(breaks = c(8, 10, 12, 14, 16, 18)) +
  labs(x = "Day", y = "Signal (a.u.)") + biomedical_theme(size = 12) +
  theme(legend.position = "top", legend.justification = "left")
write.csv(d, file.path(out, "repeated/source_data.csv"), row.names = FALSE)
write.csv(stats, file.path(out, "repeated/statistics.csv"), row.names = FALSE)
write.csv(g, file.path(out, "repeated/fitted_group_means.csv"), row.names = FALSE)
write.csv(data.frame(d, fitted = fitted(f), residual = residuals(f, type = "normalized")),
  file.path(out, "repeated/residuals.csv"), row.names = FALSE)
saveRDS(f, file.path(out, "repeated/model.rds"))
export_biomedical(p, file.path(out, "repeated/figure"), 90, 84, 90)

# One synthetic assay, three technical wells per concentration: conditional fit only.
d <- expand.grid(well = 1:3, dose = c(.01, .04, .16, .63, 2.5, 10, 40, 160))
d$assay_id <- "Synthetic_assay_1"
d$well_id <- sprintf("W%02d", seq_len(nrow(d)))
d$response <- 5 + 95 / (1 + (d$dose / 1.6)^1.15) +
  c(-1.4, .5, 1.1, .7, -1.2, .3, -1, 1.4, -.4, .8, -1.3, .6,
    -1.2, .4, 1.1, .9, -1.5, .3, -.8, 1.2, -.5, 1, -.6, -.2)
fit <- dose_response_candidates(d$dose, d$response)
eligible <- subset(fit$comparison, converged & covariance_ok & midpoint_in_range & interval_in_range)
stopifnot(nrow(eligible) > 0)
selected <- eligible$model[which.min(eligible$aicc)]
stopifnot(selected == fit$comparison$model[which.min(fit$comparison$aicc)])
fit$comparison$selected <- fit$comparison$model == selected
g <- subset(fit$predictions, model == selected)
stopifnot(all(is.finite(g$low)), all(is.finite(g$high)))
p <- ggplot(d, aes(dose, response)) +
  geom_ribbon(data = g, aes(y = NULL, ymin = low, ymax = high), fill = pal["A"], alpha = .18) +
  geom_line(data = g, aes(y = fitted), colour = pal["A"], linewidth = .8) +
  geom_point(size = 1.25, shape = 21, fill = "white", stroke = .35, colour = pal["A"]) +
  scale_x_log10(breaks = c(.01, .1, 1, 10, 100), labels = c("0.01", "0.1", "1", "10", "100")) +
  scale_y_continuous(breaks = seq(0, 100, 25)) +
  labs(x = "Concentration (µM)", y = "Response (%)") + biomedical_theme(size = 12)
write.csv(d, file.path(out, "dose_response/source_data.csv"), row.names = FALSE)
for (field in c("comparison", "parameters", "predictions", "residuals"))
  write.csv(fit[[field]], file.path(out, "dose_response", paste0(field, ".csv")), row.names = FALSE)
saveRDS(fit, file.path(out, "dose_response/models.rds"))
export_biomedical(p, file.path(out, "dose_response/figure"), 90, 78, 90)

# Right-censored survival: show censor marks and align risk counts with time.
d <- data.frame(id = sprintf("S%02d", 1:24),
  group = factor(rep(c("Control", "A"), each = 12), levels = c("Control", "A")),
  time = c(4, 5, 7, 8, 10, 11, 14, 17, 19, 21, 24, 24,
           7, 11, 13, 16, 18, 20, 22, 24, 24, 24, 24, 24),
  event = c(rep(1, 9), rep(0, 3), rep(1, 6), rep(0, 6)))
f <- survival::survfit(survival::Surv(time, event) ~ group, d, conf.type = "log-log")
test <- survival::survdiff(survival::Surv(time, event) ~ group, d)
ss <- summary(f, censored = TRUE)
curve <- data.frame(time = ss$time, n_risk = ss$n.risk, events = ss$n.event,
  censored = ss$n.censor, survival = ss$surv, low = ss$lower, high = ss$upper,
  group = sub("group=", "", as.character(ss$strata)))
steps <- do.call(rbind, lapply(c("Control", "A"), function(gr) {
  z <- subset(curve, group == gr)
  z <- rbind(data.frame(time = 0, n_risk = 12, events = 0, censored = 0,
    survival = 1, low = 1, high = 1, group = gr), z)
  r <- z[rep(seq_len(nrow(z)), each = 2), ]
  r$time <- c(0, rep(z$time[-1], each = 2), tail(z$time, 1))
  r
}))
risk <- expand.grid(time = c(0, 6, 12, 18, 24), group = c("Control", "A"))
risk$n <- mapply(function(t, gr) sum(d$group == gr & d$time >= t), risk$time, risk$group)
check_risk <- summary(f, times = c(0, 6, 12, 18, 24), extend = TRUE)
stopifnot(identical(as.integer(risk$n), as.integer(check_risk$n.risk)))
pvalue <- pchisq(test$chisq, df = length(test$n) - 1, lower.tail = FALSE)
main <- ggplot(steps, aes(time, survival, colour = group, fill = group)) +
  geom_ribbon(aes(ymin = low, ymax = high), alpha = .10, colour = NA) +
  geom_line(linewidth = .75) +
  geom_point(data = subset(curve, censored > 0), shape = 3, size = 2.4, stroke = .6) +
  scale_colour_manual(values = pal[c("Control", "A")], breaks = c("Control", "A")) +
  scale_fill_manual(values = pal[c("Control", "A")], breaks = c("Control", "A")) +
  scale_x_continuous(limits = c(0, 24), breaks = c(0, 6, 12, 18, 24), expand = expansion(c(.02, .03))) +
  scale_y_continuous(limits = c(0, 1), breaks = c(0, .5, 1), expand = expansion(c(0, .02))) +
  labs(x = "Day", y = "Survival probability") + biomedical_theme(size = 12) +
  theme(legend.position = "none",
        axis.title.y = element_text(margin = margin(r = 8)))
risk$group <- factor(risk$group, levels = c("A", "Control"))
riskplot <- ggplot(risk, aes(time, group, label = n, colour = group)) +
  geom_text(family = "Arial", size = 12, size.unit = "pt") +
  scale_colour_manual(values = pal, guide = "none") +
  scale_x_continuous(limits = c(0, 24), breaks = c(0, 6, 12, 18, 24), expand = expansion(c(.02, .03))) +
  labs(x = NULL, y = NULL) + biomedical_theme(size = 12) +
  theme(axis.line = element_blank(), axis.ticks = element_blank(), axis.text.x = element_blank(),
        axis.text.y = element_text(margin = margin(r = 10)),
        plot.margin = margin(0, 4, 3, 3))
previous_device <- cowplot::set_null_device("agg")
p <- cowplot::plot_grid(main, riskplot, ncol = 1, rel_heights = c(4.4, 1), align = "v", axis = "lr")
cowplot::set_null_device(previous_device)
write.csv(d, file.path(out, "survival/source_data.csv"), row.names = FALSE)
write.csv(curve, file.path(out, "survival/curve_statistics.csv"), row.names = FALSE)
write.csv(risk, file.path(out, "survival/risk_table.csv"), row.names = FALSE)
write.csv(data.frame(test = "Two-sided asymptotic log-rank test", chisq = test$chisq,
  df = 1, p_raw = pvalue, n_control = 12, n_a = 12, event_control = 9, event_a = 6),
  file.path(out, "survival/statistics.csv"), row.names = FALSE)
saveRDS(list(survfit = f, logrank = test), file.path(out, "survival/models.rds"))
export_biomedical(p, file.path(out, "survival/figure"), 90, 104, 90)

# Six individually measured analytes: row scaling is display-only, not a signature score.
m <- rbind(A = c(12, 14, 11, 24, 28, 25), B = c(35, 30, 33, 17, 20, 18),
  C = c(8, 11, 9, 10, 9, 12), D = c(20, 18, 22, 40, 43, 38),
  E = c(50, 54, 48, 34, 30, 32), F = c(15, 21, 18, 19, 17, 23))
colnames(m) <- c("C1", "C2", "C3", "A1", "A2", "A3")
d <- as.data.frame(as.table(m), responseName = "signal")
names(d)[1:2] <- c("analyte", "id")
d$group <- factor(ifelse(startsWith(as.character(d$id), "C"), "Control", "A"),
                   levels = c("Control", "A"))
d$log2_signal <- log2(d$signal)
d$row_mean <- ave(d$log2_signal, d$analyte, FUN = mean)
d$row_sd <- ave(d$log2_signal, d$analyte, FUN = sd)
d$z <- (d$log2_signal - d$row_mean) / d$row_sd
d$analyte <- factor(d$analyte, levels = rev(LETTERS[1:6]))
d$id <- factor(d$id, levels = colnames(m))
shuffled <- d[rev(seq_len(nrow(d))), ]
z_reordered <- (shuffled$log2_signal - ave(shuffled$log2_signal, shuffled$analyte, FUN = mean)) /
  ave(shuffled$log2_signal, shuffled$analyte, FUN = sd)
stopifnot(all.equal(unname(z_reordered), unname(shuffled$z)),
  max(abs(tapply(d$z, d$analyte, mean))) < 1e-12)
p <- ggplot(d, aes(id, analyte, fill = z)) + geom_tile() +
  facet_grid(. ~ group, scales = "free_x", space = "free_x") +
  scale_fill_gradient2(low = "#2166AC", mid = "white", high = "#B2182B", midpoint = 0,
    limits = c(-2, 2), breaks = c(-2, 0, 2), name = "Row z-score") +
  labs(x = "Sample", y = "Analyte") + biomedical_theme(size = 12) +
  theme(axis.line = element_blank(), axis.ticks = element_blank(), strip.text = element_text(size = 12),
    legend.position = "bottom", legend.title = element_text(size = 12),
    panel.spacing.x = grid::unit(2, "mm")) +
  guides(fill = guide_colourbar(title.position = "top", barwidth = grid::unit(28, "mm"),
                                 barheight = grid::unit(3, "mm")))
write.csv(d[c("analyte", "id", "group", "signal")], file.path(out, "heatmap/source_data.csv"), row.names = FALSE)
write.csv(d, file.path(out, "heatmap/display_values.csv"), row.names = FALSE)
export_biomedical(p, file.path(out, "heatmap/figure"), 90, 90, 90)
writeLines(capture.output(sessionInfo()), file.path(out, "session_info.txt"))

# Keep the rerunnable source and helpers beside the generated data and plot objects.
if (normalizePath(out) != examples) file.copy(script, file.path(out, "gallery.R"), overwrite = TRUE)
dir.create(file.path(out, "scripts"), showWarnings = FALSE)
if (normalizePath(file.path(out, "scripts")) != normalizePath(file.path(skill, "scripts")))
  file.copy(file.path(skill, "scripts", c("compact.R", "dose_response.R")), file.path(out, "scripts"), overwrite = TRUE)
write.csv(data.frame(variable = "condition", level = names(pal), color = unname(pal),
  source = "CARTO Bold; identified Control in gray"), file.path(out, "palette.csv"), row.names = FALSE)
cat("Synthetic gallery saved to", normalizePath(out), "\n")
