---
name: test-single-cell-abundance
description: Test whether annotated cell populations or local neighborhoods change in relative abundance across biological conditions using replicate-aware compositional methods. Use for cell-type proportion changes, differential abundance, compositional analysis, Milo or miloR, sccomp, propeller or speckle, neighborhood abundance, and questions such as whether a population is enriched or depleted in disease. Do not use for expression changes within a population, untested composition plots, or cell-level tests that treat cells as replicates.
---

# Test single-cell abundance

Use biological samples as replicates and model the dependence created because cell
population proportions share a common total.

## Workflow

1. Reconstruct sample, condition, batch, donor, pairing, cell-type, and inclusion
   fields from the contract and object metadata. Confirm the contrast direction and
   whether the sampling fraction has a comparable biological meaning across samples.
2. Count cells per sample and population; report total cells, zero counts, excluded
   samples, and group balance. With inadequate biological replication, provide
   descriptive proportions without inferential p-values.
3. Decide whether the question is about named populations or local changes along a
   continuous manifold:
   - use a neighborhood method such as Milo for cluster-free localization;
   - use a compositional count model such as sccomp for population-level effects and
     uncertainty;
   - use propeller for a fast transformed-proportion analysis when its assumptions
     and design support the question.
4. Build the replicate-level design with relevant covariates and pairing. Check rank
   and group/batch confounding before fitting.
5. Report effect direction and magnitude with interval or uncertainty, the biological
   replicate count, multiplicity method/family, and method-specific diagnostics. Do
   not interpret one population in isolation from the rest of the composition.
6. Save the sample-by-population count table, complete sample metadata, model design,
   tested neighborhoods or populations, complete results, and mapping back to cells.
7. Trace key claims in the evidence index, create figures through
   `create-scientific-figures`, and verify sample/contrast consistency with
   `verify-biomedical-analysis`.

Read `references/method-selection.md` for method patterns and required diagnostics.

## Boundaries

- Use `annotate-single-cell-types` before population-level testing when labels are not
  already independently supported; neighborhood testing can precede fine labels but
  still depends on the chosen graph.
- Use `test-single-cell-expression` for condition-associated expression changes.
- A stacked composition chart is descriptive until a replicate-aware test is supplied.
- Association of abundance with condition is not evidence that one population caused
  another change.
