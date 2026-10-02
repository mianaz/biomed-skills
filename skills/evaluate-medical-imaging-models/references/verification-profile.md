# Medical-imaging model verification profile

## Imaging integrity

- Patient/specimen and image hierarchy, geometry, conversions, preprocessing, and
  exclusions reconcile to source manifests.
- Images, masks, regions, labels, and predictions align after all transforms.
- De-identification and data-use constraints are satisfied without destroying required grouping.

## Reference standard

- Label source, reader expertise, blinding, adjudication, uncertainty, timing, and
  indeterminate/missing handling are explicit.
- Spectrum, partial/differential verification, incorporation, and reader biases are assessed.

## Split and leakage

- Development, tuning, calibration, threshold selection, and final testing are separated.
- No participant/specimen, related image, site/device shortcut, near duplicate, future
  field, or preprocessing information crosses the declared boundary.

## Metrics and claims

- Task definitions, matching rules, aggregation, denominators, uncertainty, failures,
  and operating thresholds are recoverable.
- Metrics are recomputed on a sample at the independent unit; site/device/subgroup and
  external-cohort claims match the observed evidence.
- Technical, diagnostic, workflow, and patient-benefit claims remain distinct.
