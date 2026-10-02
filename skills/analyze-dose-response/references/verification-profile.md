# Dose-response verification profile

## Assay and controls

- Dose units, preparation, range, spacing, vehicle, controls, exposure time, assay
  direction, dynamic range, interference, toxicity, and plate/batch QC are explicit.
- Independent experiments/biological units are distinct from technical wells, fields,
  and reads; exclusions reconcile to all attempted curves.

## Curve and model

- Raw and normalized data, zero-dose handling, model family, parameterization, bounds,
  starting values, convergence, and fitted/residual values are recoverable.
- Plateaus, transition, and requested potency/benchmark are supported by the observed
  range; partial, flat, failed, or nonmonotonic curves are labeled rather than forced.
- Parameter uncertainty preserves experiment/unit and batch dependence.

## Comparisons and multiplicity

- The compared quantity is prespecified and a joint dependence-aware model is used.
- Shared controls, pairing, batch/day, many compounds, times, endpoints, and parameters
  are handled in the declared testing family.

## Claims

- Potency, efficacy, slope, toxicity, interference, binding, mechanism, exposure, and
  therapeutic effect are not conflated.
- Tables, figures, control QC, curve classifications, parameters, intervals, and
  narrative agree for every promoted result.
