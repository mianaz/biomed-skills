# Regulatory evidence and method guide

## Distinguish the outputs

| Output | What supports it | What it does not prove |
|---|---|---|
| TF/pathway activity score | Expression of signed prior targets | Direct TF binding or de novo edges |
| Co-expression edge | Predictive/correlated expression across cells | Direct or causal regulation |
| Motif-supported regulon | Co-expression plus motif enrichment in candidate targets | TF occupancy in the assayed cells |
| Enhancer-linked regulon | RNA, accessibility, motif, and enhancer-gene linkage | Functional enhancer action without intervention |
| Perturbational response | Controlled TF/gene intervention and downstream change | Generality beyond the assayed context or absence of off-target effects |

## Curated-prior activity

Use decoupleR-style scoring when the question is which known TF or pathway programs
are active. Select an organism-compatible, signed network and require adequate target
coverage. CollecTRI/DoRothEA are TF-target priors; PROGENy is a pathway-responsive gene
prior. Network release, target-set size, and method affect scores.

With decoupleR, ULM scores each regulator against its signed targets independently
and is a common choice for CollecTRI-style TF priors. MLM estimates overlapping
signatures jointly and is commonly paired with PROGENy when coverage and collinearity
support that fit. Treat ULM versus MLM as a modeling decision, not a fixed property of
the resource, and verify the current implementation.

- Use one score definition consistently across compared groups.
- Avoid comparing absolute scores across separately processed datasets without
  explicit calibration.
- Summarize and test condition differences at the biological-replicate level.
- Retain long-form activity output before embedding it in an object.

## RNA-only regulons

A pySCENIC-style workflow has three logically separate stages:

1. Infer candidate TF-target co-expression edges, commonly with GRNBoost2/GENIE3.
2. Prune modules with species/build-compatible cis-regulatory motif rankings.
3. Score the surviving regulons per cell, commonly with AUCell.

Skipping motif pruning changes the claim to co-expression only. Binarizing AUCell can
help summarize active fractions, but threshold choice is model/data dependent; retain
continuous scores and show threshold sensitivity. Do not use a universal minimum cell
count as a quality guarantee—assess state diversity, target detection, replicate
support, and stability directly.

## Enhancer-aware regulation

Use SCENIC+-style analysis only when RNA and chromatin modalities, peak coordinates,
motif resources, and genome builds are compatible. Check barcode pairing/alignment,
peak quality, TSS enrichment, motif enrichment, enhancer-gene distance/linkage, and
support across donors. RNA plus ATAC narrows hypotheses but does not by itself show
that an enhancer or TF causes expression.

## Stability and orthogonal validation

- Repeat with reasonable cell/feature subsamples and report recurrent edges/regulons.
- Check whether edges disappear when donor, condition, or cell state is controlled.
- Quantify regulon overlap and correlated activity; collapse or label redundant
  programs rather than presenting them as independent discoveries.
- Compare with independent datasets and orthogonal binding/accessibility evidence.
- Use regulator perturbation plus rescue or targeted assays for stronger mechanistic
  validation.

## Output contract

Keep separate tables for candidate edges, motif/enhancer support, final regulon
membership, cell-level activity, group-level summaries, stability, and external
validation. This separation lets `verify-biomedical-analysis` trace exactly which
evidence supports each regulatory claim.
