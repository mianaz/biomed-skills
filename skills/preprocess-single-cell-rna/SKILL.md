---
name: preprocess-single-cell-rna
description: Convert raw or author-processed scRNA-seq and snRNA-seq counts into an analysis-ready object through assay-aware cell calling, ambient-RNA handling, gene-identifier cleanup, doublet scoring, adaptive quality control, explicit exclusions, normalization, and feature selection. Use for droplet, plate-based, or nucleus RNA data before clustering, integration, annotation, or replicate-level testing. Do not use for ATAC-only, spatial-only, or already validated downstream result tables.
---

# Preprocess Single-Cell RNA

Process each biological sample independently until technical artifacts and cell-level
QC have been evaluated. Preserve the input counts and make every exclusion explicit.

## Workflow

1. Confirm sample, donor, condition, chemistry, specimen type, matrix class, feature
   reference, and whether the data are cells or nuclei. Apply
   `apply-single-cell-conventions` before combining inputs.
2. Read `references/assay-specific.md` and classify the input as droplet, plate-based,
   or nuclei. Do not apply droplet-specific empty-barcode methods to plate data.
3. Standardize feature identifiers with `references/gene-identifiers.md`, preserving
   original IDs and the mapping used.
4. If unfiltered droplets are available, perform or review cell calling. Choose an
   ambient-RNA strategy from `references/ambient-rna.md`; run it per sample.
5. Score doublets per sample with `references/doublets.md`. Retain scores, method
   calls, and evidence from multiplexing or genotype demultiplexing when available.
6. Calculate and review cell- and sample-level metrics using
   `references/quality-control.md`. Create QC flags first; derive the retained set in
   a separate, auditable selection step.
7. Normalize and select variable features with a method compatible with the count
   model and planned downstream analysis. Keep raw counts untouched and label every
   transformed layer precisely.
8. Apply `references/atlas-filtering.md` only for multi-study atlas feature
   harmonization or another stated need; do not remove stress, ribosomal,
   mitochondrial, immunoglobulin, or receptor genes by habit.
9. Save the analysis-ready object, cell-level QC table, sample summary, feature
   mapping, and explicit inclusion/exclusion table.

## Decision rules

- Thresholds are data- and assay-dependent selection rules, not universal constants.
  Inspect distributions within samples and biological contexts before exclusion.
- Flag before dropping. Preserve borderline cells unless the analysis contract
  defines an exclusion or the evidence supports one.
- Do not regress cell cycle, mitochondrial signal, library size, or other covariates
  merely because they correlate with an embedding. Regress only a justified
  technical nuisance that is not central to the biological question.
- Do not merge samples before ambient-RNA and doublet models that assume a
  sample-specific loading process.
- Do not treat a low-dimensional embedding as QC evidence without the underlying
  metrics and sample composition.

## Handoff and boundaries

Register parameters, software, source files, flags, exclusions, and object lineage
with `ensure-biomedical-reproducibility`. Route QC graphics and retained/excluded
source tables to `create-scientific-figures`. Hand the unintegrated analysis-ready
object to `integrate-single-cell-data` only if integration is justified; otherwise
continue to `annotate-single-cell-types`. Use `verify-biomedical-analysis` before
consequential downstream claims depend on the retained cell set.
