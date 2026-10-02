# Atlas feature filtering

Use a cross-study feature policy only when building an atlas or another analysis that
requires a shared feature universe. Preserve the full per-study objects.

## Construct the shared universe

1. Harmonize stable IDs and symbols first.
2. Define a reproducible presence rule across studies, such as detectable or present
   in at least half of eligible studies. Treat one-half as an example, not a default;
   choose the fraction from study count, sparsity, and the planned model.
3. Prefer comparable protein-coding features for general embeddings while retaining
   immunoglobulin and T-cell receptor genes when immune biology or annotation needs
   them.
4. Remove mitochondrial, ribosomal, stress, sex-linked, or dissociation-response
   genes only when they would obscure the stated objective. Keep a list and retain
   them in the source object.
5. Handle tiny or shallow studies explicitly; do not let one low-coverage dataset
   erase informative features from every cohort.

Report the rule, denominator, study eligibility, feature counts at each step, and a
comparison showing that major lineages and rare populations remain recoverable.
