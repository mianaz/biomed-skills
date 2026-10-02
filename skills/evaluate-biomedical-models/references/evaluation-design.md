# Model evaluation design

## Name the evaluation claim

Distinguish:

- apparent performance on development data;
- internal validation within the development source;
- temporal, geographic, setting, or device external validation;
- model updating or recalibration;
- prospective impact or utility evaluation.

State the target population, prediction time, outcome horizon, intended action, and
acceptable error tradeoff. A technically external dataset can still be clinically
similar; explain which transportability dimension it tests.

## Choose split boundaries

Keep all records from an independent unit in one partition. Also group families,
sites, devices, acquisition batches, time episodes, and near-duplicate specimens when
they share information. For repeated cross-validation, keep the full preprocessing
and tuning pipeline inside each training fold.

Use temporal validation when deployment predicts future periods and site validation
when deployment spans institutions. Use nested resampling when hyperparameters,
features, thresholds, or ensembles are selected from the same source.

## Freeze and compare

Before final evaluation, freeze:

- model code and weights/version;
- feature definitions and availability time;
- missing-data and preprocessing rules;
- calibration and threshold;
- eligible population and unevaluable-case handling;
- primary metrics, subgroups, and comparators.

Compare with current practice and a simple credible baseline. When evaluating an
updated model, report both original and updated models on the same units and state
which data informed the update.

## Common leakage paths

- target-derived features or post-outcome measurements;
- participant, visit, image, specimen, site, or technical replicate in multiple sets;
- normalization, feature selection, augmentation, or imputation fitted before split;
- labels or adjudication informed by model output;
- threshold or subgroup chosen after inspecting test performance;
- duplicated public records crossing sources.
