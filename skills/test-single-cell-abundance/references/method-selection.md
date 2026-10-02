# Differential-abundance method selection

## Contents

1. Shared prerequisites
2. Milo neighborhoods
3. sccomp compositions
4. Propeller transformed proportions
5. Reporting and verification

## 1. Shared prerequisites

Create two canonical tables before choosing a method:

- one row per cell with stable cell, sample, condition, batch, inclusion, and optional
  cell-type identifiers;
- one row per biological sample with design variables and total retained cell count.

Confirm that sample capture and filtering do not make “relative abundance” incomparable
across conditions. No statistical model repairs perfect condition/batch confounding.

## 2. Milo neighborhoods

Use overlapping neighborhoods on a biologically justified reduced-space graph when
changes are continuous, local, or poorly represented by hard cluster boundaries.
Milo fits neighborhood counts with a negative-binomial model and applies a
neighborhood-aware multiple-testing correction.

Record and justify:

- reduced representation and whether it was computed without condition leakage;
- number of dimensions, graph `k`, neighborhood sampling proportion, and refinement;
- neighborhood sizes and sample coverage;
- design formula, contrast direction, offsets, and spatial FDR threshold;
- mapping from significant neighborhoods back to cells and supported labels.

Inspect neighborhood-size and sample-coverage distributions before interpreting
results. A visually coherent patch on an embedding is not sufficient evidence.

## 3. sccomp compositions

Use a population-level compositional model when named cell types or states are the
scientific units of interest and effect intervals are important. Model both
composition and, where relevant, variability; include justified covariates and inspect
outlier handling.

Retain the input count table, formula, priors/default version, convergence diagnostics,
posterior effect or credible interval, and multiplicity-aware result. Verify the
installed-version package API and diagnostics before execution.

## 4. Propeller transformed proportions

Use propeller for a fast frequentist population-level analysis when transformed
proportions and limma-style moderation fit the design. Record whether logit or
arcsine-square-root transformation was used, how zeros were handled, the design and
contrast, and the correction family.

For covariate-adjusted work, construct the sample-by-population transformed matrix and
fit the explicit design rather than relying on a simplified group-only call.

## 5. Reporting and verification

For every tested population or neighborhood report:

- effect scale and direction;
- uncertainty interval when available;
- biological samples per group and total cells per sample;
- raw and adjusted significance measure plus correction method;
- zero/rare-population and exclusion handling;
- design formula and contrast;
- annotation or neighborhood mapping uncertainty.

Interpret results jointly. A rise in one component can mechanically coincide with
declines in others, and all methods remain conditional on the observed cell capture
and preprocessing pipeline. A sensitivity analysis with a second method is useful only
when it probes a material modeling uncertainty; do not require it by default.
