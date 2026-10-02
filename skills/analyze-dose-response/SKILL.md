---
name: analyze-dose-response
description: Design, validate, fit, compare, and interpret concentration- or dose-response experiments from plate, assay, animal, ex vivo, or other repeated biological measurements. Use for dilution series, potency or efficacy curves, IC50, EC50, ED50, Emax, Hill slope, benchmark dose, four- or five-parameter logistic models, partial curves, combination follow-up, or comparing curves across conditions. Preserve independent experiments, controls, plate/batch structure, assay range, units, censoring, uncertainty, and model diagnostics. Do not use for pooled CRISPR Perturb-seq, ordinary two-group testing, pharmacokinetic modeling, or treating technical wells as biological replicates.
---

# Analyze Dose Response

Estimate the response over a prespecified dose range and report what the observed
range supports. Do not force an IC50 or EC50 from a flat, partial, saturated, toxic,
or nonmonotonic curve.

## Validate design and assay readiness

1. Define the biological question, independent unit, technical repeats, treatment,
   concentration/dose units, vehicle, negative and positive controls, exposure time,
   response scale, direction, and target estimand.
2. Check dose spacing and range, randomization, plate layout, edge effects, batch/day/
   operator/instrument balance, dilution preparation, solubility, precipitation,
   interference, carryover, detection limits, saturation, and control performance.
3. Reconcile experiment → plate → specimen/unit → well/field/read hierarchy. Preserve
   raw and normalized responses and do not average away failed controls or between-
   experiment variation.
4. Define exclusions, normalization, blank subtraction, viability or nonspecific-
   toxicity criteria, and partial/failed curve rules before fitting.

Read `references/design-and-qc.md` before accepting a plate or dilution series.

## Fit a model supported by the curve

Plot every independent unit and experiment before fitting. Choose a constrained or
unconstrained four-parameter logistic, five-parameter asymmetric, Emax, log-linear,
nonlinear mixed, benchmark-dose, or nonmonotonic model from the assay and observed
shape. Read `references/models-and-comparisons.md` before choosing parameter bounds or
comparing conditions.

- Model concentration on the correct scale and define zero/vehicle separately from
  log dose.
- Estimate across independent experiments with hierarchical or replicate-aware
  uncertainty; do not fit pooled technical wells as independent evidence.
- Report potency only when the target response lies within an adequately supported
  portion of the curve. Otherwise report a bound, `not_estimable`, or descriptive range.
- Keep potency, maximal effect, slope, onset, toxicity, and assay failure as distinct
  quantities.

## Diagnose and compare

Inspect residuals by dose and experiment, parameter identifiability, covariance,
boundary estimates, leverage, monotonicity/asymmetry, control drift, and sensitivity
to exclusions, normalization, bounds, and model family. Compare full curves or named
parameters using a model that preserves shared controls, pairing, batches, and
independent experiments. Correct the declared family when testing many compounds,
endpoints, times, or parameters.

## Interpret boundedly

Use “estimated potency,” “maximal observed effect,” or “response over the tested
range.” Do not call an IC50 a binding affinity, therapeutic dose, mechanism, or in vivo
efficacy without the appropriate design. Separate cytotoxicity, assay interference,
and general signal loss from target-specific response.

## Deliver auditable outputs

Save the plate/sample map, raw and normalized data, control QC, inclusion flags,
model formula and bounds, per-experiment and joint estimates with intervals, fitted
values, residuals, diagnostics, comparison results, and sensitivity analyses. Use the
`dose-response` profile in `references/resource-profile.json`. Route structural data
checks to `validate-biomedical-data`, provenance to
`ensure-biomedical-reproducibility`, figures to `create-scientific-figures`, and the
complete bundle to `verify-biomedical-analysis`.
