# Imaging task metrics and leakage

## Classification and triage

Evaluate at the intended patient/exam/specimen unit. Report discrimination,
calibration, locked-threshold performance, predictive values at relevant prevalence,
failure/abstention, workload, and decision consequence. When multiple images feed one
decision, specify aggregation before testing.

## Detection and localization

Define lesion matching, overlap/distance rule, duplicate detections, ignored regions,
minimum size, and handling of multiple lesions. Report sensitivity versus false
positives per image/exam and participant-level consequences where applicable. Lesions
within one patient are dependent.

## Segmentation

Report overlap together with boundary or distance error and clinically relevant
volume/measurement error. Handle empty masks explicitly. Aggregate per patient or
specimen with uncertainty; a pixel-pooled score can hide poor cases and size effects.

## Registration, reconstruction, and quantitative imaging

Use task-relevant geometric/landmark or measurement error plus image-fidelity metrics.
Perceptual similarity alone does not establish preservation of pathology. For
quantitative biomarkers, assess repeatability, reproducibility, bias, agreement,
calibration, and sensitivity to acquisition/reconstruction.

## Reader studies

Preserve reader and case as crossed sources of variation. Define reading order,
washout, assistance condition, carryover control, adjudication, and endpoint. Compare
model, readers, and assisted readers on shared cases with multi-reader multi-case or
another justified dependence-aware method.

## Leakage audit

Check patient, family, visit, bilateral organ, study, series, slice, frame, patch,
specimen, block, slide, stain, site, scanner, protocol, and near-duplicate overlap.
Also check label leakage, post-outcome metadata, burned-in text, institution markers,
annotation artifacts, acquisition shortcuts, and preprocessing fitted across splits.
