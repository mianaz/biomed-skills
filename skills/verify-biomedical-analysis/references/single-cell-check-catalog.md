# Single-cell verification catalog

Use this catalog only when the `single-cell-analysis` profile is active. Record each
result in manifest `quality.checks` using the exact check ID.

## Cell and sample quality

- `single-cell:qc-retention`: Reconstruct cells per biological sample before and
  after each filter. Match thresholds, exclusions, and retained samples to source
  metadata; fail if a sample disappears without an explicit record.
- `single-cell:doublet-ambient`: Confirm doublet and ambient-RNA assessments are
  recorded, or verify a study-specific reason they do not apply. Flag conclusions
  that depend on untreated contamination.
- `single-cell:integration-balance`: Review both technical mixing and biological
  conservation by sample and condition. A visually mixed embedding alone does not
  demonstrate valid integration.

## Annotation and inference

- `single-cell:annotation-evidence`: Require discriminatory positive and negative
  marker evidence that is not circular with the reference transfer used to assign
  labels.
- `single-cell:replicate-aware-inference`: Reconstruct the inferential unit.
  Condition-level expression and abundance tests must not treat cells as independent
  biological replicates.
- `single-cell:identifiability`: Bound trajectory, communication, regulatory, and
  spatial results to associations or model-implied states unless the design supplies
  perturbational or temporal evidence for stronger claims.
