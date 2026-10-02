# Dose-response models and comparisons

## Model families

- **Four-parameter logistic:** lower and upper asymptotes, midpoint, and slope for a
  monotone symmetric transition.
- **Five-parameter logistic:** add asymmetry only when data support the extra parameter.
- **Emax/Hill:** use when pharmacologic efficacy and concentration-response form fit
  the scientific interpretation.
- **Constrained curves:** fix a plateau only with assay or control justification; show
  sensitivity to the constraint.
- **Nonlinear mixed effects:** combine independent experiments or units while modeling
  between-unit parameter variation and within-unit technical error.
- **Benchmark-dose models:** estimate dose at a prespecified response change with model
  uncertainty and model-choice sensitivity.
- **Nonmonotonic models:** use only with adequate range/density and a plausible,
  reproducible shape; do not force a logistic summary.

Specify whether concentration is molar, mass/volume, administered dose, or another
quantity. Handle vehicle/zero as a separate control because `log(0)` is undefined.

## Identifiability and bounds

Inspect profile likelihood, covariance, parameter correlation, convergence from
several starts, and boundary solutions. Parameter bounds encode scientific assumptions
and must be reported. If the response target is outside the supported fitted range,
report `not_estimable` or a one-sided bound rather than extrapolating a precise midpoint.

Do not overinterpret Hill slope when plateaus or transition are weakly identified.

## Comparisons

Prespecify whether the comparison concerns potency, maximal effect, slope, benchmark
dose, area over a supported range, or the full curve. Fit a joint model that respects
pairing, shared controls, independent experiments, batches, and repeated responses.
Avoid comparing two separately estimated IC50 values only by whether their confidence
intervals overlap.

For many compounds, times, endpoints, or parameters, define the multiplicity family.
Use hierarchical screening or confirmatory prioritization when appropriate, and retain
all curves including failed/not-estimable cases.

## Diagnostics and sensitivity

Check residuals versus dose/fitted value/plate/experiment, heteroscedasticity,
influential doses or units, control drift, model family, normalization, exclusions,
bounds, and loss function. Show per-experiment estimates or curves so one large or
high-signal run does not hide heterogeneity.
