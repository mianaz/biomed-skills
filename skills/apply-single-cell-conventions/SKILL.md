---
name: apply-single-cell-conventions
description: Keep single-cell objects, count layers, cell and feature identifiers, metadata fields, embeddings, label vocabularies, factor orders, and R/Python round trips consistent across a project. Use when initializing a scRNA-seq or snRNA-seq project, converting Seurat and AnnData objects, returning Python-derived embeddings or labels to an R-led analysis, renaming cell types, combining datasets, or diagnosing misaligned metadata. Do not use to choose biological methods or plotting aesthetics.
---

# Apply Single-Cell Conventions

Establish one source of truth and make every transfer key-based and reversible.

## Set the contract

1. Select the canonical object for the project. In an R-led project this is usually
   a Seurat object; in a Python-led project it is usually AnnData. Treat detours to
   the other ecosystem as method-specific computations, not independent forks.
2. Preserve immutable raw counts in an explicitly named assay or layer. Keep
   normalized, scaled, corrected, and imputed values separate and never call them
   counts.
3. Make cell IDs globally unique before merging, preferably by prefixing the source
   sample. Keep original barcodes in a metadata field.
4. Preserve stable feature IDs alongside display symbols. Do not collapse duplicate
   symbols without recording the aggregation rule.
5. Define canonical metadata names and types for sample, donor, condition, batch,
   assay, tissue, cluster, cell type, annotation status, and exclusion status.

Read `references/object-bridge.md` for conversion and round-trip checks. Read
`references/identity-ledger.md` before relabeling cells, harmonizing datasets, or
creating shared categorical orders.

## Enforce identity-safe transfers

- Join labels, scores, and covariates by exact cell ID; join feature-level results by
  stable feature ID. Never rely on row or column position.
- Store each embedding under a distinct, descriptive key. Do not overwrite PCA with
  UMAP or replace an unintegrated reduction with a corrected one.
- Before accepting a round trip, compare cell and feature sets, count representation,
  metadata values, categorical levels, and embedding dimensions.
- Stop on duplicated IDs, missing join keys, silent cell loss, unexpected gene loss,
  or reordered data that cannot be reconciled from identifiers.

## Keep labels coherent

- Distinguish identity (`cell_type`) from state, program score, cluster, and predicted
  label. A state score is not a cell type.
- Keep provisional and verified annotations in separate fields. Do not overwrite the
  evidence trail when a label changes.
- Apply one canonical spelling, hierarchy, and factor order across objects, tables,
  tests, and figures. Run a relabel sweep after any vocabulary change.
- Bind semantic colors by category name only after the vocabulary is stable; route
  palette and export decisions to `create-scientific-figures`.

## Keep boundaries

- Leave method choice to the relevant single-cell specialist.
- Register files, parameters, and object checkpoints with
  `ensure-biomedical-reproducibility` rather than duplicating general provenance.
- Use `verify-biomedical-analysis` for independent audit of consequential transfers
  or label changes.
