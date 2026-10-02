# Metrics and uncertainty

Match metrics to the outcome, prevalence, intended decision, and error costs.

## Binary outcomes

Report discrimination and precision-recall behavior when imbalance matters, but also
calibration-in-the-large, calibration slope/curve, and task-relevant threshold
sensitivity, specificity, predictive values, likelihood ratios, or workload.

Accuracy alone is inadequate under imbalance. AUROC does not define a threshold or
calibration. Predictive values depend on prevalence; report transport assumptions.

## Continuous and ordinal outcomes

Report error in original units, bias, spread, calibration or agreement, and clinically
meaningful tolerance rates. Correlation is not agreement. Inspect error across the
measurement range and relevant subgroups.

## Time-to-event predictions

Use censoring-aware discrimination, calibration at prespecified horizons, prediction
error, and decision metrics. Define time zero, horizon, competing events, and censoring
assumptions. Route model construction and event-time estimands to
`model-time-to-event-outcomes`.

## Uncertainty

Compute intervals at the independent-unit level and preserve clustering. Use paired
comparisons when models are evaluated on the same units. Bootstrap the entire
evaluation procedure when appropriate, including recalibration or threshold fitting
that is legitimately part of evaluation.

Do not treat folds, patches, lesions, images, repeated visits, or technical replicates
as independent participants. Report denominators and missing predictions for every
metric. For small subgroups, emphasize interval width and avoid unstable rankings.

## Decision usefulness

When actionability is claimed, specify the action, threshold range, harms, resource
cost, baseline policy, and population. Decision curves or cost analyses supplement,
not replace, discrimination and calibration.
