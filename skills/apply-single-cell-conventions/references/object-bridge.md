# Object bridge

Use a bridge only when the receiving ecosystem provides a method that materially
improves the analysis. The canonical object remains the source of truth.

## Prepare the export

- Make cell IDs unique and feature IDs stable before conversion.
- Record which assay or layer contains raw counts and which contains normalized
  expression. Verify that a claimed count matrix is sparse and integer-like.
- Export only metadata required by the detour, but always include the join keys,
  sample, donor, batch, and current annotation status.
- Prefer an interoperable H5AD representation for R/Python exchange. Compatible
  routes include `anndataR`, `scConvert`, or `SeuratDisk`; choose the route supported
  by the installed object versions and inspect its mapping rather than assuming it.

## Map representations deliberately

| Concept | Seurat convention | AnnData convention |
|---|---|---|
| raw counts | named assay/layer | named layer; sometimes `.raw` |
| normalized expression | data layer | `.X` or named layer |
| cell metadata | object metadata | `.obs` |
| feature metadata | assay feature metadata | `.var` |
| embeddings | reductions | `.obsm` |

These are conventions, not guarantees. Inspect the actual object. Never assume
AnnData `.X` or a Seurat default assay contains raw counts.

## Return results

- Return embeddings with cell IDs and named dimensions. Create a new reduction key;
  do not replace an existing reduction.
- Return predictions, scores, latent variables, and QC metrics as keyed tables.
- Return feature-level values with stable feature IDs and preserve the symbol used
  for display as a separate field.
- If the detour filtered cells or features, return an explicit inclusion table and
  reason rather than silently shrinking the canonical object.

## Round-trip gate

Accept the transfer only after checking:

1. exact expected cell and feature sets, with duplicates absent;
2. unchanged count dimensions and representative count values;
3. expected sparse/dense representation and numeric type;
4. metadata equality after key-based reordering;
5. embedding row names, dimensions, and finite values; and
6. a small biological sanity check, such as preserved marker expression or matching
   per-cell library sizes.

If exact round-trip preservation is not possible, keep both representations, record
the loss explicitly, and restrict downstream use to the fields that passed.
