# Doublets

Run doublet detection within sample or capture batch before integration. Expected
rates depend on loading, chemistry, and recovered-cell count.

## Evidence sources

- `scDblFinder` is a common R-native classifier; Scrublet is a common Python-native
  classifier.
- Cell hashing, genotype demultiplexing, or multi-species mixtures provide stronger
  direct evidence for some heterotypic doublets.
- Very high counts/features, incompatible lineage markers, and isolated embedding
  position are supporting diagnostics, not standalone calls.

## Workflow

1. Use raw counts from one sample or capture batch.
2. Supply or evaluate an expected rate based on the platform and loading record.
3. Store every method's score and call under a distinct field.
4. Return results to the canonical object by exact cell ID; never by row position.
5. Review disagreements and cells near thresholds. A consensus rule may improve
   specificity, but preserve the component calls.
6. Flag first. Exclude only through an explicit selection rule and retain the reason.

Homotypic doublets are intrinsically harder to detect and may look like large normal
cells. Heterotypic calls can also reflect ambient RNA or transitional states. Report
these limitations and inspect whether a purported rare population is enriched for
doublet evidence.
