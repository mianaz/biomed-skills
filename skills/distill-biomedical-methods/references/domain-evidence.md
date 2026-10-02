# Domain evidence prompts

Load the applicable section and preserve both strengths and limitations.

## Clinical and epidemiologic

- Are eligibility, time zero, exposure/intervention, comparator, outcome, follow-up,
  analysis sets, missingness, and adjustment strategy explicit?
- Are immortal time, selection, informative censoring, competing events, measurement
  error, and residual confounding addressed?
- Does the cohort represent the intended population and care setting?

## Diagnostic and predictive models

- Are the index/model and reference standard applied independently and blindly?
- Are development, tuning, calibration, threshold selection, and evaluation separated?
- Are splits at participant/site/time level, with external validation, calibration,
  missing predictions, subgroup performance, and decision utility?

## Imaging

- Are acquisition, geometry, reconstruction, preprocessing, registration, annotation,
  reader expertise, adjudication, and image-level exclusions recoverable?
- Could patient, series, slice, patch, site, scanner, or annotation leakage inflate results?
- Are segmentation/detection metrics aggregated at the intended clinical unit?

## Experimental and wet-lab

- Are independent biological units, technical repeats, controls, randomization,
  blinding, plate/batch allocation, reagents/lots, instruments, calibration, dose/time,
  exclusions, and assay range explicit?
- Are perturbation and rescue or orthogonal validation strong enough for the mechanism?

## Computational and omics

- Are representations, feature/reference releases, preprocessing, batch handling,
  model selection, benchmarks, ablations, seeds, and compute recoverable?
- Does inference preserve biological replication and avoid circular validation?

## Evidence synthesis

- Are protocol, search, screening, extraction, risk of bias, effect harmonization,
  heterogeneity, certainty, and deviations reproducible?
- Are companion reports linked so one study is not counted repeatedly?
