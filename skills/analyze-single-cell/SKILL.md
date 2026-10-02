---
name: analyze-single-cell
description: Coordinate an end-to-end single-cell transcriptomics analysis by identifying the assay and study design, choosing a canonical object, and routing public-data discovery, retrieval, preprocessing, integration, annotation, testing, trajectories, communication, and verification to the appropriate specialist skills. Use for broad scRNA-seq or snRNA-seq requests, mixed-stage projects, unfamiliar single-cell datasets, or when deciding which single-cell workflow should run next. Do not use for spatial-only or bulk-only analyses.
---

# Analyze Single-Cell Data

Route a single-cell project without turning this skill into a second copy of every
specialist workflow.

## Establish the analysis

1. Read the research question, sample metadata, assay chemistry, organism, tissue,
   and available files. Distinguish cells from biological replicates; the donor or
   specimen is usually the unit for condition-level inference.
2. Use `plan-biomedical-analysis` when a validated analysis contract is absent or
   the question, contrasts, exclusions, or deliverables are still ambiguous.
3. Choose one canonical object and ecosystem for the project. Follow the user's
   existing stack when practical; cross language boundaries only for a method with
   clear scientific value, then return results by stable cell and feature IDs.
4. Apply `apply-single-cell-conventions` before creating competing object versions,
   label vocabularies, or cross-language exports.
5. Preserve immutable raw counts and sample-level metadata. Never replace counts
   with corrected expression or treat cells as independent biological replicates.

## Route the work

- Use `curate-single-cell-datasets` to discover and compare public datasets. For a
  known accession or file collection, use `retrieve-single-cell-data`.
- Use `preprocess-single-cell-rna` for cell calling, ambient RNA, doublets, QC,
  identifier cleanup, normalization, and feature selection.
- Use `integrate-single-cell-data` only after deciding that a removable technical
  effect exists and is not inseparable from the biology of interest.
- Use `annotate-single-cell-types` for candidate labels, marker verification,
  hierarchical annotation, and annotation uncertainty.
- Route condition-level expression to `test-single-cell-expression` and abundance
  changes to `test-single-cell-abundance`; both require biological-replicate-aware
  designs.
- Route gene-list ORA, ranked enrichment from pseudobulk statistics, and
  replicate-aware pathway scores to `analyze-pathway-enrichment`; use complete
  signed rank tables rather than cell-level marker p-values for condition claims.
- Route developmental ordering to `infer-single-cell-trajectories`, signaling to
  `infer-cell-cell-communication`, regulatory programs to
  `infer-single-cell-regulation`, perturbation screens to `analyze-perturb-seq`, and
  spatial assays to `analyze-spatial-transcriptomics`.
- Route target ranking to `prioritize-single-cell-targets` only after the upstream
  evidence has passed its domain checks.

If a named downstream skill is not installed yet, state the intended handoff and
complete only the stages whose scientific contract is available.

## Coordinate the run

- Use `orchestrate-biomedical-work` when stages can be delegated or run in parallel.
- Maintain lineage with `ensure-biomedical-reproducibility`; do not create a
  single-cell-specific provenance system here.
- Send finalized numerical results to `create-scientific-figures` and narrative
  synthesis to `communicate-biomedical-results`.
- Use `verify-biomedical-analysis` before promoting manuscript-critical or otherwise
  consequential conclusions.

## Completion gate

Finish only when the canonical object, sample identities, retained/excluded cells,
analysis stage, unresolved uncertainties, and next specialist handoff are explicit.
Do not imply that an embedding, cluster, transferred label, or module score is a
biological conclusion by itself.
