# Dose-response design and quality control

## Plan the range and controls

- Choose dose spacing and range from prior information, solubility, assay window,
  expected potency, maximal feasible exposure, and toxicity or interference limits.
- Use enough distinct doses to identify the intended curve parameters; extra technical
  wells cannot compensate for a range that misses both plateaus or the transition.
- Include blank, vehicle/negative, positive/reference, and assay-specific interference
  controls. Match vehicle concentration across doses when feasible.
- Randomize or balance compounds/conditions, doses, controls, and samples across plate
  position, day, operator, instrument, and processing order.
- Replicate independent biological units or experiments across meaningful batches;
  identify technical wells, fields, and reads separately.

For animal or in vivo dose studies, include route, schedule, body-size basis,
formulation, exposure confirmation, tolerability, humane endpoints, and approved
maximum dose. Do not equate nominal administered dose with tissue exposure.

## Validate the assay

Check control separation and variability, plate maps, edge/row/column effects,
evaporation, drift, signal stability, standard curves, detection and quantification
limits, saturation, dynamic range, carryover, compound precipitation, autofluorescence,
quenching, cytotoxicity, and nonspecific response.

Record control-QC criteria before curve fitting. A failed plate or experiment remains
in accounting even if excluded under a prespecified rule.

## Normalize transparently

Preserve raw values. Record blank subtraction, reference scaling, baseline correction,
log transform, plate normalization, and direction so fitted parameters can be mapped
back to observed units. Avoid normalizing every curve to its own observed extrema when
the maximal effect is a quantity of interest.

## Curve readiness

Classify each experiment before joint inference:

- full monotone curve with supported lower and upper regions;
- partial transition with one plateau unsupported;
- flat/no response over tested range;
- saturated or out-of-range response;
- nonmonotonic/biphasic response;
- failed control or technical failure;
- confounded by toxicity or interference.
