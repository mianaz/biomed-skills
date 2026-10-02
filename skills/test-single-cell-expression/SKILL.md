---
name: test-single-cell-expression
description: Test condition-associated expression changes in single-cell RNA-seq at the biological-replicate level by aggregating raw counts per sample or sample-by-cell-type and fitting an explicit pseudobulk design. Use for replicate-aware differential expression between single-cell cohorts, cell-type-resolved contrasts, sample-level PCA or MDS, and requests involving pseudobulk, edgeR, DESeq2, limma-voom, or false positives from treating cells as replicates. Do not use for clinical outcome or survival modeling, within-object cluster markers, whole-tissue bulk RNA-seq, or changes in cell-type abundance.
---

# Test single-cell expression

Treat the biological sample—not the cell—as the unit of inference. Use raw counts to
create one pseudobulk profile per sample, optionally within each cell type or state.

## Workflow

1. Read the analysis contract and reconstruct the experimental unit, sample ID,
   condition, pairing, batch, covariates, and contrast direction. Stop if sample IDs
   are ambiguous or the design cannot distinguish condition from batch.
2. Confirm replication per condition and cell type. With very sparse replication,
   report descriptive effects and uncertainty rather than manufacturing an
   inferential p-value; do not use cell count to inflate `n`.
3. Aggregate **raw integer counts by sum** for each sample or sample-by-cell-type.
   Never average normalized or log-transformed expression.
4. Tabulate cells and library size per pseudobulk column. Define a context-appropriate
   minimum-cell rule before testing, keep excluded columns visible, and record the
   effect of filtering on group balance.
5. Build and check the design matrix and named contrast. Require full rank, correct
   reference levels, and enough residual degrees of freedom. Preserve pairing,
   repeated measures, and relevant covariates.
6. Filter weakly expressed genes on the pseudobulk matrix, normalize libraries, and
   fit a replicate-aware count model. Prefer edgeR quasi-likelihood or DESeq2 for
   ordinary count designs; use limma-voom when its modeling advantages fit the cohort.
   Verify the installed-version API before execution.
7. Check library distributions, sample PCA/MDS, dispersion/model diagnostics,
   influential samples, contrast direction, effect signs, p-value ranges, and the
   multiplicity family.
8. Save the count matrix, aligned sample metadata, design matrix, contrast, filtering
   decisions, diagnostics, complete result table, and claim-linked evidence. Record
   provenance with `ensure-biomedical-reproducibility`, create figures with
   `create-scientific-figures`, and run `verify-biomedical-analysis` before promoting
   a biological claim.
9. When pathway interpretation is requested, pass the complete signed statistic
   table, tested-gene universe, contrast direction, and filtering record to
   `analyze-pathway-enrichment`; do not enrich only a convenient subset unless a
   prespecified ORA question requires it.

Read `references/pseudobulk-workflow.md` for R-first implementation patterns.

## Boundaries

- For cluster markers within one dataset, use a marker method and label the result as
  descriptive unless biological replication is modeled.
- For replicate-aware shifts in population proportions, use
  `test-single-cell-abundance`.
- For perturbation screens, use `analyze-perturb-seq` and apply the same replicate
  principle within its perturbation-aware design.
- For ORA, ranked GSEA, or sample-level gene-set scoring, use
  `analyze-pathway-enrichment`; this skill owns the upstream expression model.
- Do not interpret a significant pseudobulk effect as a change in cell abundance or
  as a cell-level causal response.
