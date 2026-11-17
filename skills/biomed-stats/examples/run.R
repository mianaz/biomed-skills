# Three constructed teaching examples; no research or patient data.
example_file <- sub('^--file=', '', grep('^--file=', commandArgs(), value = TRUE)[1])
example_dir <- dirname(normalizePath(example_file))
out <- file.path(example_dir, 'results')
dir.create(out, showWarnings = FALSE)

# 1. Equal-weight donor means, with treatment minus control as the target.
donor <- sprintf('D%02d', 1:6)
control <- c(80, 70, 90, 75, 85, 65)
change <- c(-6, -10, -4, -12, -8, -2)
wells <- expand.grid(well = 1:3, condition = c('control', 'treatment'),
                     donor = donor, stringsAsFactors = FALSE)
id <- match(wells$donor, donor)
wells$viability_percent <- control[id] +
  ifelse(wells$condition == 'treatment', change[id], 0) +
  ifelse(wells$condition == 'control', c(-2, 0, 2)[wells$well],
         c(-1, 0, 1)[wells$well])
means <- aggregate(viability_percent ~ donor + condition, wells, mean)
paired <- reshape(means, idvar = 'donor', timevar = 'condition', direction = 'wide')
paired <- paired[order(paired$donor), ]
paired$change_pp <- paired$viability_percent.treatment - paired$viability_percent.control
paired_test <- t.test(paired$change_pp, mu = 0, alternative = 'two.sided')
paired_result <- data.frame(contrast = 'treatment minus control', unit = 'percentage points',
  independent_pairs = nrow(paired), mean_change = mean(paired$change_pp),
  ci_lower = paired_test$conf.int[1], ci_upper = paired_test$conf.int[2],
  confidence_level = 0.95, statistic = unname(paired_test$statistic),
  df = unname(paired_test$parameter), p_value = paired_test$p.value,
  method = 'paired t test via donor differences', family_size = 1)
leave_one_out <- data.frame(omitted_donor = paired$donor,
  mean_change = vapply(seq_len(nrow(paired)), function(i)
    mean(paired$change_pp[-i]), numeric(1)))
write.csv(wells, file.path(out, 'paired-wells.csv'), row.names = FALSE)
write.csv(paired, file.path(out, 'paired-donor-means.csv'), row.names = FALSE)
write.csv(paired_result, file.path(out, 'paired-result.csv'), row.names = FALSE)
write.csv(leave_one_out, file.path(out, 'paired-influence.csv'), row.names = FALSE)

# 2. Prospective assumptions, chosen independently of the first example's result.
planning <- expand.grid(effect_pp = c(3, 5, 8), sd_difference_pp = c(6, 8, 10))
planning$alpha <- 0.05
planning$target_power <- 0.8
planning$analyzable_pairs <- ceiling(mapply(function(effect, sd_difference)
  power.t.test(delta = effect, sd = sd_difference, sig.level = 0.05,
    power = 0.8, type = 'paired', alternative = 'two.sided', strict = TRUE)$n,
  planning$effect_pp, planning$sd_difference_pp))
planning$attained_power <- mapply(function(n, effect, sd_difference)
  power.t.test(n = n, delta = effect, sd = sd_difference, sig.level = 0.05,
    type = 'paired', alternative = 'two.sided', strict = TRUE)$power,
  planning$analyzable_pairs, planning$effect_pp, planning$sd_difference_pp)
planning$assumed_pair_loss <- 0.1
planning$donors_to_recruit <- ceiling(planning$analyzable_pairs / 0.9)
write.csv(planning, file.path(out, 'prospective-power.csv'), row.names = FALSE)

# 3. Fixed predictions on a constructed, independent held-out cohort.
diagnostic <- data.frame(unit_id = sprintf('U%04d', 1:1000),
  truth = c(rep(1L, 10), rep(0L, 990)),
  classifier = c(rep(1L, 9), 0L, rep(1L, 20), rep(0L, 970)),
  all_negative_baseline = 0L)
counts <- data.frame(model = c('classifier', 'all_negative_baseline'),
  TP = c(sum(diagnostic$classifier == 1 & diagnostic$truth == 1), 0),
  FN = c(sum(diagnostic$classifier == 0 & diagnostic$truth == 1), 10),
  FP = c(sum(diagnostic$classifier == 1 & diagnostic$truth == 0), 0),
  TN = c(sum(diagnostic$classifier == 0 & diagnostic$truth == 0), 990))
metrics <- data.frame(model = rep(counts$model, each = 4),
  metric = rep(c('accuracy', 'sensitivity', 'specificity', 'PPV'), 2))
metrics$numerator <- as.vector(t(cbind(counts$TP + counts$TN,
  counts$TP, counts$TN, counts$TP)))
metrics$denominator <- as.vector(t(cbind(rowSums(counts[, c('TP', 'FN', 'FP', 'TN')]),
  counts$TP + counts$FN, counts$TN + counts$FP, counts$TP + counts$FP)))
metrics$estimate <- metrics$numerator / metrics$denominator
metrics$estimate[metrics$denominator == 0] <- NA_real_
metrics$ci_lower <- NA_real_
metrics$ci_upper <- NA_real_
fixed_rate <- metrics$model == 'all_negative_baseline' &
  metrics$metric %in% c('sensitivity', 'specificity')
for (i in which(metrics$denominator > 0 & !fixed_rate)) {
  interval <- binom.test(metrics$numerator[i], metrics$denominator[i])$conf.int
  metrics$ci_lower[i] <- interval[1]
  metrics$ci_upper[i] <- interval[2]
}
metrics$interval <- '95% Clopper-Pearson, marginal for each metric'
metrics$interval[fixed_rate] <- 'Fixed by the all-negative prediction rule'
metrics$interval[metrics$denominator == 0] <- 'Undefined: no predicted positives'
write.csv(diagnostic, file.path(out, 'diagnostic-predictions.csv'), row.names = FALSE)
write.csv(counts, file.path(out, 'diagnostic-counts.csv'), row.names = FALSE)
write.csv(metrics, file.path(out, 'diagnostic-metrics.csv'), row.names = FALSE, na = '')
saveRDS(list(paired_test = paired_test, paired = paired, planning = planning,
             diagnostic_counts = counts, diagnostic_metrics = metrics),
        file.path(out, 'analysis.rds'))
writeLines(trimws(capture.output(sessionInfo()), which = 'right'),
           file.path(out, 'session-info.txt'))

# Fill the human-readable walkthrough from these executed results.
report <- paste(readLines(file.path(example_dir, 'report-template.html')), collapse = '\n')
main_plan <- planning[planning$effect_pp == 5 & planning$sd_difference_pp == 8, ]
report <- gsub('{{PAIR_RESULT}}', sprintf(
  '平均变化 %.1f 个百分点，95%% CI %.2f 至 %.2f；双侧 P = %.4f（6 位供者，df = 5）。',
  paired_result$mean_change, paired_result$ci_lower, paired_result$ci_upper,
  paired_result$p_value), report, fixed = TRUE)
pair_rows <- vapply(seq_len(nrow(paired)), function(i) sprintf(
  '<tr><td>%s</td><td>%.1f</td><td>%.1f</td><td>%+.1f</td></tr>',
  paired$donor[i], paired$viability_percent.control[i],
  paired$viability_percent.treatment[i], paired$change_pp[i]), character(1))
report <- gsub('{{PAIR_ROWS}}', paste(pair_rows, collapse = ''), report, fixed = TRUE)
report <- gsub('{{PLAN_RESULT}}', sprintf(
  '需要 %d 位具有完整配对数据的供者；取整后功效 %.1f%%。若预期 10%% 的供者配对数据不可用，计划招募 %d 位供者。',
  main_plan$analyzable_pairs, 100 * main_plan$attained_power,
  main_plan$donors_to_recruit), report, fixed = TRUE)
plan_rows <- apply(planning, 1, function(x) sprintf(
  '<tr><td>%g</td><td>%g</td><td>%d</td><td>%.1f%%</td><td>%d</td></tr>',
  x[['effect_pp']], x[['sd_difference_pp']], x[['analyzable_pairs']],
  100 * x[['attained_power']], x[['donors_to_recruit']]))
report <- gsub('{{PLAN_ROWS}}', paste(plan_rows, collapse = ''), report, fixed = TRUE)
metric_rows <- vapply(seq_len(nrow(metrics)), function(i) {
  x <- metrics[i, ]
  value <- if (x$denominator == 0) '未定义：无预测阳性' else sprintf(
    '%.1f%%（%.1f%%–%.1f%%）', 100*x$estimate, 100*x$ci_lower, 100*x$ci_upper)
  if (fixed_rate[i]) value <- sprintf('%.1f%%（由预测规则确定）', 100*x$estimate)
  sprintf('<tr><td>%s</td><td>%s</td><td>%d / %d</td><td>%s</td></tr>',
    x$model, x$metric, x$numerator, x$denominator, value)
}, character(1))
report <- gsub('{{METRIC_ROWS}}', paste(metric_rows, collapse = ''), report, fixed = TRUE)
writeLines(report, file.path(example_dir, 'index.html'))
cat('Three teaching examples executed. Open', file.path(example_dir, 'index.html'), '\n')
