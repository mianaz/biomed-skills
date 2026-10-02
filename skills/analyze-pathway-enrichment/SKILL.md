---
name: analyze-pathway-enrichment
description: Analyze biological pathways and gene sets from thresholded hit lists, complete ranked differential-statistic tables, or sample-level expression profiles. Use for over-representation analysis, ranked GSEA, Hallmark, Reactome, Gene Ontology, pathway activity scoring, functional interpretation of RNA-seq/proteomics/screen results, or pathway comparisons across biological samples. Covers gene universes, identifier mapping, direction, multiplicity, redundancy, database releases, and replicate-aware validation. For single-cell condition comparisons, use pseudobulk statistics or biological-replicate summaries rather than treating cells as replicates; route TF/regulon activity to infer-single-cell-regulation.
---

# Analyze Pathway Enrichment

Match the method to the statistical object. Enrichment summarizes coordinated
evidence; it does not establish pathway activation, mechanism, or causality.

## Choose the analysis

- Use **over-representation analysis (ORA)** for a defensibly thresholded hit list.
  Define the eligible feature universe explicitly. ORA is directionless unless
  positive and negative hit lists are analyzed separately.
- Use **ranked gene-set enrichment** for a complete table of tested genes with a
  signed statistic. Retain weak and nonsignificant genes; do not threshold first.
- Use **per-sample pathway scoring** when the question concerns pathway variation
  across samples, covariates, or outcomes. Model the resulting scores with the
  biological sample as the unit of inference.

Read `references/method-selection.md` before choosing an input, rank, universe, or
gene-set collection. Read `references/interpretation-and-validation.md` before
promoting pathway-level claims.

## Workflow

1. Reconstruct the organism, assay, experimental unit, contrast direction, eligible
   features, and upstream filtering. For single-cell condition analyses, start from
   replicate-aware pseudobulk differential statistics produced by
   `test-single-cell-expression`, not cluster-marker p-values that treat cells as
   independent samples.
2. Freeze the input object before enrichment: the complete rank table, the hit rule
   and hit list, or the normalized sample-by-gene matrix. Preserve gene-level effect,
   uncertainty, test statistic, raw and adjusted p-values, and the upstream contrast
   identifier when available.
3. Harmonize organism and gene identifiers with the selected collections. Record
   dropped, ambiguous, one-to-many, and duplicate mappings; apply a declared,
   deterministic resolution rule before analysis. Report mapped coverage for both
   the input and each retained gene set.
4. Select a small, question-led set of collections. Use Hallmark for broad,
   comparatively low-redundancy programs; Reactome for curated hierarchical
   pathways; and GO for ontology-level biological processes, functions, or
   compartments. Do not search many releases and report only the favorable one.
5. Define the multiplicity family before testing. Record whether correction is
   within a collection, across collections, across contrasts/cell types, or another
   explicit family. Keep complete unfiltered results.
6. Run the selected method with documented gene-set size bounds and deterministic
   settings where supported. Confirm the current tool documentation and installed
   version before writing executable calls; do not infer an API from memory.
7. Inspect mapping coverage, set sizes, overlap or leading-edge genes, effect
   direction, influential genes, and sensitivity to reasonable hit thresholds,
   universe definitions, ranks, and gene-set releases. Collapse redundant terms by
   hierarchy or gene overlap while retaining the full table.
8. For sample-level activity, preserve pairing, batch, and covariates in a
   replicate-aware model. Check sample support, leverage, signature coherence, and
   leave-one-sample or leave-one-donor sensitivity. Scores computed from the same
   expression data are supporting views, not independent validation.
9. Save claim-ready results with the collection source and release/date, organism,
   identifier namespace, mapping resource, universe, rank or hit rule, set-size
   filters, correction family, complete statistics, leading-edge/overlap genes,
   redundancy groups, and validation status.

## Interpret boundedly

- State GSEA direction relative to the exact signed rank definition. Never infer
  direction from an unsigned ORA result.
- Say “enriched,” “depleted,” “higher score,” or “consistent with” as supported.
  Do not translate enrichment automatically into “activated,” “required,” or
  “drives.”
- Treat overlapping GO or Reactome terms as correlated summaries, not independent
  discoveries. Show representative terms without discarding contradictory results.
- Report no-result outcomes as not supported, inconclusive, or technical failure
  according to mapping, annotation, sample size, and sensitivity evidence.

## Compose with the suite

- Use `infer-single-cell-regulation` for TF-target regulons, TF activity, or claims
  about regulatory programs; conventional pathway gene sets and sample-level
  pathway scores remain here.
- Use `create-scientific-figures` for enrichment maps, running-score plots, and
  pathway heatmaps rather than duplicating figure policy.
- Register database releases, mapping resources, parameters, and result artifacts
  with `ensure-biomedical-reproducibility`.
- Require `verify-biomedical-analysis` to audit input completeness, universe and ID
  compatibility, multiplicity, sample support, sensitivity, and claim wording.
