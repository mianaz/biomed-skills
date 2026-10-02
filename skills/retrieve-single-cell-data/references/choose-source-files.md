# Choose source files

Select the least-transformed representation that is usable for the planned analysis,
not simply the largest or easiest file.

## File classes

| Class | Typical contents | Use |
|---|---|---|
| `raw_unfiltered_counts` | all droplets/barcodes | preferred when cell calling or ambient-RNA modeling is needed |
| `filtered_counts` | author- or pipeline-called cells | suitable for most downstream work if raw counts are retained |
| `count_table` | gene-by-cell or cell-by-gene matrix | suitable after orientation, identifier, and integer checks |
| `processed_object` | H5AD, RDS, h5Seurat, Loom, or atlas object | suitable only after locating an intact raw-count assay/layer and sample metadata |
| `reads_only` | FASTQ or aligned reads | re-quantify only when counts are unavailable or the reference/quantifier must change |
| `normalized_only` | log, scaled, or otherwise transformed expression | restricted exploratory reuse; unsuitable for methods that require counts |

## Selection order

1. Determine which steps require unfiltered droplets, raw counts, splice layers,
   feature-barcode modalities, or a particular reference build.
2. Prefer repository-provided matrices or objects that retain the required values.
3. Prefer raw droplets over filtered counts when ambient correction or cell calling
   is planned; otherwise filtered counts may avoid unnecessary reconstruction.
4. Use a processed object when it preserves counts and trustworthy metadata, but do
   not inherit its embeddings, integration, or labels as unquestioned truth.
5. Use reads as a last resort because re-quantification introduces chemistry,
   reference, software, and resource choices.
6. Treat normalized-only data as a limitation, not an equivalent substitute.

For multi-file archives, map each file to sample, library, modality, and matrix role
before merging. Verify supplied MD5/SHA checksums; otherwise calculate local hashes
through `ensure-biomedical-reproducibility` after acquisition.
