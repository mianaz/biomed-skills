---
name: annotate-single-cell-types
description: Assign and verify hierarchical cell-type identities in scRNA-seq or snRNA-seq data using cluster markers, reference transfer, classifiers, curated marker panels, concordance checks, and explicit uncertainty. Use after preprocessing or integration to label coarse compartments and fine subtypes, reconcile several annotation methods, validate a marker panel, or review questionable labels. Automated predictions and model suggestions are candidates only; final labels require context-appropriate marker evidence.
---

# Annotate Single-Cell Types

No automated or reference-derived label is final until it agrees with documented,
species- and tissue-appropriate marker evidence. `unknown`, `mixed`, and a verified
parent label are valid outcomes.

## Annotation workflow

1. Confirm species, tissue, assay, disease context, feature symbols, canonical object,
   and sample/donor fields. Define the label hierarchy and vocabulary with
   `apply-single-cell-conventions`.
2. Identify coarse compartments first: immune, epithelial, endothelial, stromal, and
   other context-relevant lineages. Verify them before subclustering.
3. Generate one or more candidate labels using `references/candidate-methods.md`.
   Keep each method's label, score, reference, and granularity in separate fields.
4. Derive cluster markers, including positive and contradictory markers, and apply
   the mandatory gate in `references/marker-verification.md`.
5. Subcluster only within a verified parent compartment, then repeat candidate
   labeling and marker verification for fine subtypes.
6. Inspect each label across donors, samples, conditions, QC flags, doublet scores,
   and ambient-RNA estimates. A label confined to one failed sample needs review.
7. Use `references/concordance-and-specificity.md` when methods disagree, clusters
   may be over-split, or a small marker panel must be evaluated.
8. Use `references/module-and-panel-scores.md` for programs or states. Never promote
   a signature score to a cell identity without independent evidence.
9. Write verified and provisional labels to separate fields and update the identity
   ledger without erasing prior calls.

Human seed panels and liver-specific cautions are in
`references/markers-human.md`; mouse immune and stromal seeds are in
`references/markers-mouse.md`. Extend them with primary or authoritative references
for the actual tissue, species, age, and disease.

## Evidence and uncertainty

- Require several coherent positive markers and absence of strong contradictory
  lineage markers. One highly expressed gene is rarely sufficient.
- Interpret low or missing markers in light of nuclei versus cells, sequencing depth,
  dissociation sensitivity, and ambient RNA.
- Treat co-expression of incompatible lineages as a possible doublet, ambient
  contamination, transitional state, or technical artifact before inventing a type.
- Separate malignant from normal epithelium with independent evidence such as
  inferred copy-number structure; lineage markers alone are insufficient.
- Favor documented biological evidence over a tool's confidence score. Coarsen or
  mark unknown when evidence remains ambiguous.

## Deliverables

Return:

- cell-level candidate and final labels with confidence/status;
- a cluster-level evidence table containing supporting markers, contradictory
  markers, citations, method agreement, sample distribution, and rationale;
- the vocabulary mapping and hierarchy;
- unresolved or mixed populations; and
- any merges or splits triggered by specificity checks.

Register references, parameters, label versions, and object lineage with
`ensure-biomedical-reproducibility`. Route marker plots, confusion matrices, and
source data to `create-scientific-figures`. Route condition comparisons to
`test-single-cell-expression`, and use `verify-biomedical-analysis` before labels
support consequential claims.
