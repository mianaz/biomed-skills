---
name: evaluate-medical-imaging-models
description: Evaluate medical-imaging or digital-pathology models with patient-, examination-, lesion-, reader-, site-, and device-aware validation. Use for classification, detection, segmentation, registration, reconstruction, triage, or quantitative-imaging model claims involving DICOM, NIfTI, whole-slide images, microscopy, masks, bounding boxes, reader annotations, or external imaging cohorts. Audit acquisition, geometry, de-identification, reference standards, patient/slice/patch leakage, task-specific metrics, calibration, operating points, subgroup and domain shift, reader comparison, and clinical unit-level uncertainty. Do not use merely to display image panels or to train and tune a model on its final test set.
---

# Evaluate Medical Imaging Models

Evaluate the model at the unit and operating setting where it would be used. Image,
slice, patch, or lesion counts do not replace independent patients, specimens, readers,
sites, or acquisition sessions.

## Reconstruct data and intended use

1. Define modality, anatomy, population, setting, intended user/action, task, prediction
   time, clinical unit, output, and failure cost.
2. Inventory acquisition site/device/protocol, reconstruction, image geometry,
   preprocessing, registration, quality exclusions, de-identification, labels,
   annotations, readers, adjudication, and reference standard.
3. Reconcile patient → study → series → instance/slide → region/lesion/patch hierarchy.
   Verify image-label and mask geometry before evaluating predictions.
4. Define development, tuning, internal test, external test, and reader-comparison
   cohorts. Detect overlap or near-duplicates at every hierarchy level.

Read `references/acquisition-and-reference-standard.md` before accepting a label or
external cohort as ground truth.

## Prevent leakage and choose the evaluation unit

- Partition at patient or independent specimen level and preserve site, time, scanner,
  family, repeated study, and bilateral structure as required by deployment.
- Fit preprocessing, harmonization, augmentation, feature selection, calibration, and
  threshold selection inside training/tuning data only.
- Aggregate patch, slice, frame, lesion, or field predictions to the declared clinical
  unit before making participant- or specimen-level claims.
- Keep unreadable, out-of-distribution, abstained, and failed cases in the accounting.
  Do not silently exclude the cases most likely to fail in practice.

## Evaluate the imaging task

Compose with `evaluate-biomedical-models` for generic validation, calibration,
uncertainty, subgroup, and decision-utility rules. Read
`references/task-metrics-and-leakage.md` for imaging-specific classification,
detection, segmentation, registration, reconstruction, and reader-study metrics.

Use locked operating points for final evaluation. Report patient/specimen-level
uncertainty, paired comparisons on shared cases, multiplicity for many structures or
subgroups, and performance across site, scanner/vendor, protocol, demographic,
pathology, disease-severity, and image-quality strata when relevant. External
validation must differ on a meaningful deployment axis, not merely use a random holdout.

## Bound the claim

Distinguish technical accuracy, reader-level agreement, diagnostic accuracy,
workflow impact, and patient benefit. A high Dice score does not prove diagnostic
utility; a high AUROC does not establish calibration, an operating threshold, or
clinical benefit. Name spectrum, verification, reader, annotation, and referral biases.

## Deliver the verification packet

Save cohort accounting, acquisition and preprocessing manifest, unit/split map,
reference-standard provenance, frozen model and threshold, prediction outputs, failure
cases, task metrics with independent-unit denominators and intervals, calibration,
subgroup/site/device results, reader comparisons, and representative error review.
Use the `medical-imaging-model-evaluation` profile in
`references/resource-profile.json` and require an independent
`verify-biomedical-analysis` pass before promoting a performance claim.
