---
name: evaluate-biomedical-models
description: Evaluate a biomedical predictive, prognostic, diagnostic, classification, regression, or risk model against its intended use using leakage-safe validation, appropriate comparators, discrimination, calibration, error, uncertainty, subgroup performance, domain shift, and decision usefulness. Use for held-out or external validation, cross-validation design, model comparison, threshold selection, clinical utility, reproducibility review, or auditing performance claims. Do not use to infer causal effects, accept training-set metrics, optimize a model on its final test set, or analyze imaging-specific acquisition and reference-standard issues without evaluate-medical-imaging-models.
---

# Evaluate Biomedical Models

Judge whether a model performs for a defined population, outcome, setting, and
decision—not whether it can produce an impressive metric on a convenient split.

## Reconstruct the intended use

1. Define the prediction target, time of prediction, horizon, eligible population,
   deployment setting, user, action, and cost of false positive and false negative
   decisions.
2. Identify the independent unit and every grouping that can leak information:
   participant, family, site, batch, time period, image, specimen, repeated visit, or
   technical replicate.
3. Freeze the candidate model, preprocessing, feature selection, calibration,
   threshold, and evaluation set before final testing. Record any post hoc change as
   model development rather than validation.

Read `references/evaluation-design.md` before selecting resampling, temporal, site,
or external validation.

## Validate without leakage

- Fit imputation, scaling, feature selection, harmonization, augmentation, and
  hyperparameter tuning only within the training portion of each resample.
- Split at the independent unit and preserve natural clusters. Use nested resampling
  when the same dataset selects hyperparameters and estimates performance.
- Prefer a geographically, temporally, or operationally external cohort when the
  claim concerns transportability. Do not call a random internal split external.
- Compare against the relevant baseline: standard practice, a simple model, existing
  score, or no-action policy—not only weaker custom variants.
- Account for missing predictions and unevaluable cases; report whether failures are
  associated with site, group, acquisition, or outcome.

## Measure the properties that matter

Select metrics from the intended decision and outcome. Report uncertainty at the
independent-unit level and avoid treating resampling folds as independent studies.
Read `references/metrics-and-uncertainty.md` before choosing metrics.

At minimum, evaluate:

- discrimination or ranking where relevant;
- calibration across the useful risk range;
- task-appropriate error or agreement;
- performance at prespecified operating thresholds;
- net benefit, workload, or other decision consequence when actionability is claimed;
- subgroup, site, time, acquisition, and prevalence sensitivity;
- robustness to missingness and plausible distribution shift.

Do not select a threshold from the test set and then report its performance as
unbiased. Do not let a single aggregate metric hide calibration, class imbalance,
unevaluable cases, or a failing clinically important subgroup.

## Report bounded claims

Follow `references/reporting-and-claims.md`. Save predictions with unit IDs or safe
hashed linkage, outcomes, split membership, model/version, all prespecified metrics,
confidence intervals, calibration data, threshold tables, subgroup results, failure
counts, and comparison results. Distinguish development, internal validation,
external validation, and prospective impact evaluation.

Use `validate-biomedical-data` before modeling, `ensure-biomedical-reproducibility`
for model/data lineage, `create-scientific-figures` for supplied metrics, and
`verify-biomedical-analysis` for an independent leakage and performance audit. Use
`evaluate-medical-imaging-models` for imaging acquisition, geometry, annotation, and
reader-reference concerns; use `model-time-to-event-outcomes` for event-time estimands
and censoring-aware model construction.
