---
name: retrieve-single-cell-data
description: Validate a known public single-cell accession or file collection, identify the correct samples and assay, choose the least-transformed usable count representation, acquire it safely, load it without losing raw counts or metadata, and document the authors' upstream processing. Use for GEO, SRA, ENA, ArrayExpress, BioStudies, CELLxGENE, atlas, or publication-linked scRNA-seq and snRNA-seq data. Use curate-single-cell-datasets first when the dataset itself still needs to be discovered.
---

# Retrieve Single-Cell Data

Turn a verified accession into a faithful local count object. Do not begin a large
download until the sample-level scope and available representations are understood.

## Retrieve and load

1. Validate the accession, publication linkage, organism, assay, tissue, conditions,
   and sample scope with `references/validate-accession.md`.
2. Inventory every relevant supplementary file, processed object, archive, and read
   run. Classify rather than guessing from filenames.
3. Select the best representation for the planned analysis using
   `references/choose-source-files.md`. Prefer usable counts; use FASTQ only when
   counts are unavailable or re-quantification is scientifically required.
4. Respect authentication, licenses, embargoes, and controlled-access procedures.
   Never bypass a manual or governed access step.
5. Acquire files with stable original names, verify supplied checksums when
   available, and check archive contents before extraction.
6. Load according to `references/load-by-format.md`. Preserve raw counts, original
   cell barcodes, feature IDs, sample annotations, and source-file relationships.
7. Make cell IDs globally unique and reconcile metadata by exact sample and cell
   keys using `apply-single-cell-conventions`.
8. Run structural sanity checks: dimensions, sparsity, integer-like counts,
   nonnegative values, library-size range, detected-feature range, duplicate IDs,
   empty samples, and agreement with reported cell counts.
9. Extract the authors' documented upstream processing using
   `references/authors-processing.md`. Record uncertainty rather than inferring
   undocumented steps.

## Guardrails

- A series-level title does not prove that every sample has the stated disease,
  tissue, assay, or treatment. Validate the promoted sample subset.
- Do not confuse actual spatial transcriptomics with dissociated single-cell data
  that was analyzed using spatial concepts.
- Do not call normalized expression “raw data.” If normalized-only values are all
  that exist, mark downstream count-based methods as unavailable or conditional.
- Do not silently combine donors, samples, runs, or modalities while loading.
- Do not discard raw droplet matrices before deciding whether ambient-RNA correction
  or cell calling is needed.

## Handoff

Register sources, checksums, retrieval times, and file lineage with
`ensure-biomedical-reproducibility`. Hand the loaded object, sample table, file-class
assessment, authors-processing summary, and unresolved conflicts to
`preprocess-single-cell-rna`. Use `verify-biomedical-analysis` before a retrieved
cohort defines a consequential comparison or benchmark.
