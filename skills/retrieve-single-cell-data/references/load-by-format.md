# Load by format

Inspect content before choosing a reader. Preserve sparse matrices and original
identifiers whenever possible.

## 10x Matrix Market and HDF5

- Confirm that matrix, barcode, and feature files belong together and that feature
  types are retained for multi-modal data.
- In R, typical readers are `Seurat::Read10X()` and `Seurat::Read10X_h5()`; in Python,
  `scanpy.read_10x_mtx()` and `scanpy.read_10x_h5()` are common.
- Prefix sample IDs before combining matrices. Retain the original barcode and
  feature ID columns.
- Distinguish raw/unfiltered from filtered directories; the filename alone may not
  be sufficient.

## Delimited count tables

- Detect whether genes or cells are rows using identifier patterns and dimensions;
  never assume orientation.
- Separate annotation columns before numeric conversion. Reject negative values and
  investigate non-integer values before calling the table counts.
- Collapse duplicate features only with an explicit rule, usually summation for
  counts with identical stable IDs; preserve the original mapping.

## H5AD

- Inspect `.X`, `.layers`, `.raw`, `.obs`, `.var`, and `.obsm` before conversion.
  `.X` may contain normalized rather than raw expression.
- Identify the layer that contains integer-like counts and confirm cell/feature
  alignment across layers.
- Treat imported embeddings and labels as author-provided fields until independently
  evaluated.

## RDS and h5Seurat

- Inspect all assays and layers, the active assay, reductions, identities, and
  metadata. Confirm which layer is counts rather than normalized or corrected data.
- Do not depend on package-specific object internals without checking the installed
  object version.

## Loom and specialized objects

- Inspect row, column, and layer attributes. Spliced/unspliced layers may be
  necessary for trajectory methods; do not flatten them into one matrix.
- Convert with `apply-single-cell-conventions` and run a round-trip check before
  deleting the source representation.

## FASTQ

- Reconstruct the sample sheet, chemistry, read structure, reference genome,
  annotation release, and expected feature types before quantification.
- Keep runs and libraries distinguishable until technical replicates are justified
  for combination.
- Compare resulting cell/barcode counts and library summaries with the publication;
  large discrepancies require investigation, not silent acceptance.
