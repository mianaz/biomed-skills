# Assay-specific preprocessing

## Droplet cells

- Distinguish raw droplets from filtered cells.
- Run cell calling, ambient correction, and doublet modeling per capture batch.
- Preserve feature-barcode modalities and chemistry metadata when present.

## Plate-based cells

- Skip empty-droplet and soup methods whose assumptions require a common droplet
  background.
- Retain plate, well, sorting, and library metadata; inspect plate and well-position
  effects.
- Choose normalization from the observed library-size distribution. Full-length
  protocols may require gene-length-aware reasoning for comparisons that depend on
  transcript abundance.
- Doublet evidence may come from sorting, well occupancy, or expression classifiers
  rather than droplet loading rates.

## Single nuclei

- Quantify intronic as well as exonic signal when the pipeline and scientific goal
  support it; exon-only counting can markedly reduce sensitivity.
- Record whether a `GeneFull`-like or include-introns mode was used and the exact
  reference annotation.
- Expect different complexity, mitochondrial fraction, and ambient profiles from
  whole cells. Do not reuse whole-cell QC thresholds.
- Interpret missing cytoplasmic markers cautiously during annotation.

For every assay, store PCA, integrated embeddings, UMAP, and other reductions under
distinct keys. Never overwrite one reduction with another.
