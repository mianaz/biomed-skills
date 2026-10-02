# Concordance and specificity

Use these diagnostics to adjudicate annotation granularity and method disagreement.
They diagnose labels or clusters; they do not create biological identities.

## Label concordance

1. Map every method or reference to one shared vocabulary and granularity.
2. Compare labels on the same cells and report the shared-cell count per pair.
3. Use a confusion matrix and a chance-corrected agreement measure such as Cohen's
   kappa. For two label vectors on the same cells, Cohen's kappa is symmetric.
4. Treat reference-to-query generalization as a separate directional evaluation;
   do not encode that direction by making a same-cell kappa matrix asymmetric.
5. Investigate outlier methods for domain mismatch, vocabulary differences, or
   poorly supported reference labels. Low agreement everywhere may require a coarser
   vocabulary or an `unknown` class.

Do not use fixed verbal kappa bands as biological truth; interpret agreement relative
to prevalence, class imbalance, shared-cell count, and the consequences of error.

## Whole-transcriptome cluster specificity

To test whether a cluster is reproducibly separable:

- balance or subsample cells per type;
- use donor- or sample-grouped cross-validation where replication permits;
- fit an interpretable linear classifier on a predefined expression feature space;
- report per-type precision, recall, and F1 plus the confusion matrix; and
- compare with a permuted-label null.

A cluster whose held-out performance approaches the null may be over-split. Compare
before and after a proposed merge. High separability still does not prove the chosen
biological name.

## Marker-panel discriminatory power

Evaluate a small panel with donor-grouped cross-validation after labels are verified.
Compare it with a broad-feature ceiling and a size-matched random or permuted floor.
Report per-class metrics and confusions, not only accuracy. For a prospective flow or
imaging panel, restrict to measurable surface or antibody-available targets and test
whether an achievable low-dimensional gating sequence separates the target types.
