---
name: analyze-perturb-seq
description: Analyze pooled CRISPR perturbation experiments with single-cell readouts, including Perturb-seq, CROP-seq, CRISP-seq, CRISPRi/a, knockout, and combinatorial designs. Use for guide assignment QC, perturbation-efficacy assessment, replicate-aware differential expression or abundance, guide/target concordance, response-program discovery, and perturbation similarity. Preserve randomized assignment and control structure where present, distinguish guides from target-level effects, and limit causal claims to the assayed intervention and context. Do not use for ordinary small-molecule dose-response, plate assays, pharmacology curves, or perturbations without single-cell guide-linked readouts.
---

# Analyze Perturb-seq

Treat guide assignment and experimental design as the first analysis result. A clean
transcriptome cannot rescue ambiguous guides, inadequate controls, batch-confounded
perturbations, or absent biological replication.

## Reconstruct the design

1. Identify perturbation modality, guide capture method, library, target-to-guide map,
   multiplicity/MOI strategy, donors or replicate cultures, batches, time points,
   cell states, and intended contrasts.
2. Identify non-targeting, safe-targeting, positive, and vehicle/mock controls and
   confirm they occur across batches and biological units.
3. Define whether multiple guides per cell are errors, expected combinatorial
   perturbations, or both under different assignment confidence levels.
4. Preserve guide-level identities even when the final question is target-level;
   independent guides are essential evidence for efficacy and off-target robustness.

## Gate on assignment and efficacy

1. Evaluate guide UMI/count distributions, assignment confidence, unassigned cells,
   multi-guide cells, barcode swapping/contamination, and rates by sample and batch.
   Use experiment-specific mixture/negative-control evidence rather than universal
   percentages.
2. Apply transcriptome QC with `preprocess-single-cell-rna` while preserving guide and
   sample metadata. Check whether QC preferentially removes particular perturbations.
3. Assess on-target efficacy using the expected mechanism and phenotype. Target RNA
   reduction may support CRISPRi but is not a universal efficacy readout for knockout
   or CRISPRa; use protein or downstream signatures when appropriate.
4. Use Mixscape-like classification only when its negative-control and response-
   mixture assumptions fit the perturbation mode and cell support. An assigned guide
   or inferred responder class is not direct proof of editing.

Read `references/design-and-inference.md` before selecting an effect model or
aggregating guides.

## Estimate perturbation effects

1. Define contrasts against appropriate controls within batch/sample and cell state.
   Do not regress away guide identity or discard guide-correlated components by default;
   genuine perturbation biology may be the signal of interest.
2. With biological replicates, use sample-by-perturbation(-by-cell-state) aggregation
   or another design-aware method and route expression testing to
   `test-single-cell-expression`.
3. Without biological replicates, do not treat cells as independent experimental
   replicates. Report cell-level screens as exploratory and use guide concordance,
   negative controls, and resampling to characterize uncertainty.
4. Model high-MOI combinations explicitly or exclude them according to the declared
   design. Do not attribute a combination response to one guide.
5. Compare guides targeting the same gene before aggregation. Report heterogeneous or
   opposite guide effects; do not average away suspected off-targets or failed guides.
6. Evaluate perturbation effects on cell-state abundance with
   `test-single-cell-abundance`; account for differential viability and capture.
7. Cluster or embed perturbations from validated effect profiles, not raw cell
   embeddings alone, and preserve uncertainty in similarity claims.

## Interpret intervention evidence carefully

Randomized, well-controlled perturbations can support a causal effect of the assigned
intervention on measured outcomes in the assayed cells and time window. Off-target
activity, incomplete editing, selection, guide multiplicity, and cell-state-dependent
efficacy limit attribution to the intended gene. Do not extend an in-vitro
transcriptional effect to therapeutic benefit, organismal phenotype, or clinical
safety without further evidence.

## Compose with the suite

- Use `infer-single-cell-regulation` to compare response programs with inferred
  regulons without treating agreement as independent proof.
- Use `prioritize-single-cell-targets` only after guide/target effects and uncertainty
  are explicit.
- Use `create-scientific-figures` for assignment QC, effect, concordance, and program
  panels.
- Use `ensure-biomedical-reproducibility` for guide maps, controls, assignment settings,
  contrasts, software, and artifacts.
- Require `verify-biomedical-analysis` to audit assignment, controls, replication,
  guide aggregation, multiplicity, effect signs, and causal scope.
