---
name: integrate-single-cell-data
description: Decide whether single-cell batch correction or reference integration is scientifically justified, select and run an embedding- or model-based method, and evaluate technical mixing against preservation of cell identity, rare populations, condition effects, and trajectories. Use when combining scRNA-seq or snRNA-seq samples, donors, chemistries, studies, tissues, species, or partially labeled references. Do not use merely because multiple samples exist or when batch is inseparable from the biology of interest.
---

# Integrate Single-Cell Data

Integration is a hypothesis about removable technical variation, not a mandatory
pipeline stage. Preserve an unintegrated baseline and raw counts throughout.

## Decide whether to integrate

1. Define the nuisance variable to remove and the biological variables to preserve.
   Inspect the sample-by-condition-by-batch design before looking at an embedding.
2. If batch is perfectly or nearly perfectly confounded with condition, tissue,
   genotype, or stage, do not claim that correction recovers the missing comparison.
   Narrow the question, add data, or analyze strata separately.
3. Compare unintegrated structure, per-sample QC, shared cell types, and marker
   expression. Do not correct a difference that is plausibly biological.
4. Decide between joint integration, reference mapping, and no correction. Reference
   mapping is often safer when a stable atlas exists and the query should not reshape
   it.

## Run the integration

1. Confirm unique cell IDs, immutable counts, consistent gene IDs, and complete
   sample/donor/batch fields using `apply-single-cell-conventions`.
2. Choose a method from `references/method-selection.md` based on data scale,
   ecosystem, covariates, reference labels, and the desired output. Do not select by
   popularity alone.
3. Fit at the sample or donor-aware level. Keep the unintegrated representation and
   store every corrected latent space or reduction under a new key.
4. For cross-species work read `references/cross-species.md`; for highly imbalanced
   multi-tissue work read `references/cross-tissue.md`.
5. Return embeddings, latent variables, predictions, and model diagnostics by exact
   cell ID. Never use positional alignment.
6. Evaluate with `references/integration-qc.md`. Accept a result only when technical
   mixing improves without erasing expected biological structure.

## Guardrails

- Never overwrite raw counts with integrated, corrected, denoised, or imputed values.
- Do not use an integrated expression matrix as the default input for
  biological-replicate-level differential expression.
- Do not force rare, tissue-specific, developmental, malignant, or activated states
  to mix with a reference population merely to improve a batch metric.
- A visually smooth UMAP is not evidence of valid integration.
- Semi-supervised predictions remain candidate annotations and must pass
  `annotate-single-cell-types`.

## Handoff

Register the design, model inputs, parameters, seeds, reference mappings, and outputs
with `ensure-biomedical-reproducibility`. Route diagnostic plots to
`create-scientific-figures`. Hand both corrected and unintegrated representations,
the integration-QC table, and unresolved confounding to
`annotate-single-cell-types`. Use `verify-biomedical-analysis` before consequential
claims depend on the corrected space.
