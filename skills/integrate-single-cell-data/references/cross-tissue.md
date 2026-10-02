# Cross-tissue integration

Large tissues and abundant cell types can dominate an atlas latent space. Preserve
tissue-specific biology while learning comparable structure.

## Balance representation

- Inspect counts by tissue, donor, sample, and coarse cell type.
- Downsample or weight within cell-type-by-tissue strata for model fitting when
  imbalance would otherwise dominate. Keep all cells for projection and downstream
  summaries.
- Treat fixed caps such as a set number of cells per stratum as examples. Choose a
  rule from memory, runtime, and the smallest informative strata.
- Keep donor diversity within each stratum; do not select many cells from one donor
  in place of biological replication.

## Choose features and validate

- Shared variable genes can work when comparable states dominate.
- A curated marker- or program-gene representation can reduce tissue-specific noise
  for coarse alignment, but it must not be used to prove the identities encoded in
  the same marker list.
- Hold out tissues or donors to test whether the representation generalizes.
- Inspect tissue-specific markers, rare resident populations, and malignant cells
  before accepting mixing.

Use separate within-tissue analyses when the biological differences are the target
or when comparable states are too sparse for defensible joint correction.
