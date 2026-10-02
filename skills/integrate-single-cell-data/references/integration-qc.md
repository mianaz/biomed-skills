# Integration quality control

Evaluate two competing objectives: removal of unwanted technical structure and
preservation of expected biology. Passing only one objective is failure.

## Technical mixing

Measure within shared populations and with sample-size awareness. Useful diagnostics
include:

- neighborhood composition by batch, sample, and donor;
- batch silhouette or inverse silhouette;
- iLISI/cLISI with the intended interpretation stated;
- kBET acceptance;
- graph connectivity; and
- per-population sample coverage.

No single metric is decisive. Perfect mixing can indicate overcorrection when real
biology differs among batches.

## Biological preservation

Check:

- canonical lineage and state-marker expression before versus after integration;
- separation or silhouette for independently supported coarse identities;
- retention of rare and sample-restricted populations;
- expected condition, tissue, stage, sex, and genotype signals;
- local continuity for trajectories when relevant; and
- concordance of replicate-level summaries in the original count space.

## Comparison design

1. Include the unintegrated baseline.
2. Evaluate per cell type and per sample, not only globally.
3. Balance or weight cells so the largest population does not dominate.
4. Use donor- or sample-held-out evaluation where prediction or mapping is involved.
5. Inspect confusion and failure cases, including cells with low mapping confidence.
6. Record the method-selection rule before reading the final UMAP.

Reject or qualify an integration that improves batch mixing while collapsing known
lineages, removing a plausible biological gradient, or leaving entire samples
unrepresented in shared populations.
