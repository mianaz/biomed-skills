# Method selection

Start with a no-correction baseline. Choose the least complex method that addresses
the identified nuisance variation while preserving the required biology.

## Common choices

### Harmony

- Operates on a low-dimensional representation, commonly scaled PCA, and returns a
  corrected embedding while leaving counts unchanged.
- Useful for fast, R-led integration with a clear batch covariate and substantial
  overlap in cell states.
- Inspect convergence and sensitivity to diversity penalties or cluster parameters;
  do not assume defaults fit severe imbalance.

### scVI

- Fits a count-based probabilistic model and returns a latent representation.
- Useful for large datasets, several technical covariates, or a Python-native model
  workflow.
- Supply the intact count layer, an explicit batch key, and only defensible
  covariates. A GPU can improve speed but is not a scientific requirement.

### scANVI

- Extends an scVI model with partial labels and can support reference mapping or
  semi-supervised latent structure.
- Reserve an explicit unlabeled category and avoid training on uncertain fine labels.
- Treat predicted labels as candidates; evaluate calibration, domain shift, and
  canonical markers independently.

### Anchor-based mapping

- Seurat-style anchors are useful for R-led reference mapping or joint integration
  when comparable cell states and features exist.
- Tune features and dimensions from overlap and scale. Inspect mapping scores and
  unmatched populations rather than forcing every query cell into a reference type.

### Mutual-nearest-neighbor methods

- MNN-family methods can be effective when batches share populations but differ
  locally. Their assumptions weaken when composition or biology differs strongly.

## Selection questions

- Is the output a corrected embedding, normalized expression model, or transferred
  reference label?
- Are all samples expected to share cell states?
- Are batch and biology separable in the design?
- Does the method support the scale, sparsity, covariates, and installed ecosystem?
- Can unmatched query populations remain unmatched?
- Can the unintegrated values and cell IDs be carried through unchanged?

Compare a small set of scientifically plausible methods only when the choice is
material. Select from predeclared biological-preservation and batch-removal checks,
not from the prettiest embedding.
