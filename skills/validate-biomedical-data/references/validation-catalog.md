# Biomedical data validation catalog

Load only the relevant sections. Passing file-level checks does not establish assay,
label, endpoint, or reference-standard validity.

## Universal checks

- Inventory and hash or stably locate every received object.
- Detect unreadable, truncated, encrypted, empty, duplicated, and unexpectedly changed
  files or collection members.
- Reconcile row/column dimensions and identifiers across data, metadata, dictionaries,
  labels, and manifests.
- Check type, category vocabulary, unit, precision, range, missingness, timestamp order,
  uniqueness, and foreign-key relationships.
- Build eligible → received → excluded/missing → analyzable accounting at the independent
  unit and each important nested level.
- Identify transformations already applied and distinguish raw, derived, normalized,
  imputed, manually edited, and model-generated fields.
- Check sensitivity, license, consent/data-use, retention, and disclosure constraints.

## Clinical and epidemiologic tables

- Confirm one person can be linked across encounters without exposing identifiers.
- Validate index date, eligibility window, exposure timing, outcome timing, follow-up,
  censoring, death, and competing-event definitions.
- Detect impossible chronology, duplicated encounters, code-system/version drift,
  units changing across sites, and future information in baseline features.
- Compare cohort counts across extraction logic, tables, sites, periods, and outcomes.

## Imaging collections

- Reconcile study, series, instance, participant, visit, modality, body part, laterality,
  acquisition, scanner/site, and label identifiers.
- Check geometry, orientation, spacing, dimensions, missing slices/frames, duplicate
  pixels, corrupted series, and image-label or mask alignment.
- Verify de-identification without destroying grouping, time, or acquisition fields
  required by the approved analysis.
- Detect participant, series, slice, patch, reader, and site overlap across intended
  train/validation/test sets.

## Experimental and assay data

- Reconcile experiment, plate, well, specimen, donor/animal, treatment, dose, time,
  batch, operator, instrument, and control maps.
- Check unit conversion, dilution series, plate orientation, blank/vehicle/positive
  controls, detection limits, saturation, and standard-curve validity.
- Separate independent experiments and biological units from aliquots, wells, fields,
  reads, and repeated instrument measurements.

## Omics matrices

- Reconcile matrix axes with feature and sample/cell metadata.
- Identify raw count, normalized, transformed, corrected, and imputed layers.
- Validate feature namespace/species/build, sample ownership, sparse/dense shape, and
  integer requirements for count models.
- Route modality-specific QC to the corresponding omics skill after this structural
  audit.
