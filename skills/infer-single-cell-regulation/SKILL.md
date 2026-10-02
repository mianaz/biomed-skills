---
name: infer-single-cell-regulation
description: Infer putative transcription-factor regulons, regulatory activity, and enhancer-linked programs from single-cell RNA or paired RNA-ATAC data. Use when choosing between curated-prior activity scoring, RNA-only pySCENIC-style de novo regulons, and SCENIC+-style multiomic regulation; when producing cell-level activity matrices; or when validating TF-target support across samples. Distinguish activity scoring, co-expression, motif support, chromatin accessibility, and perturbational evidence, and do not call an inferred regulator a causal driver without independent intervention evidence.
---

# Infer Single-Cell Regulation

Match the inferential claim to the evidence layer. A TF activity score, a co-expression
edge, a motif-supported regulon, an accessible enhancer link, and a perturbation effect
are different objects and must not be reported as interchangeable proof.

## Choose the task

1. Define whether the output should be curated-prior TF/pathway activity, a de novo
   RNA regulon, or an enhancer-linked multiomic regulon.
2. Confirm species, gene identifiers, samples/donors, cell states, count/normalized
   layers, and—when needed—paired chromatin data and peak calls.
3. Inspect whether the relevant state diversity and cell support occur across
   biological units. If a regulon is driven by one donor, batch, or rare low-quality
   population, report it as unstable.

## Select the evidence layer

- Use curated-prior scoring such as decoupleR with CollecTRI/DoRothEA or PROGENy when
  rapid TF/pathway activity from an existing expression object is the goal. This is
  activity inference from a prior network, not de novo GRN discovery.
- Use a pySCENIC-style pipeline for RNA-only de novo regulons: co-expression candidate
  edges, motif-based pruning, then per-cell regulon activity. Do not present Stage 1
  co-expression alone as a regulatory network.
- Use SCENIC+ or another enhancer-aware method only with compatible chromatin and RNA
  evidence. Enhancer accessibility strengthens regulatory plausibility but remains
  inferential.
- Use `analyze-perturb-seq` when direct perturbational effects of regulators are
  available; those effects can test, refine, or contradict inferred edges.

Read `references/regulatory-evidence.md` before selecting resources or interpreting
scores.

## Run and validate

1. Freeze the TF list, prior or motif/region resource, genome/annotation build, gene
   universe, and identifier mapping before inference.
2. Preserve sample identity and avoid allowing condition, donor, or cell-type mixture
   to masquerade as within-state regulation. Refit or summarize within relevant
   states when necessary.
3. For de novo RNA networks, retain co-expression weights, motif-pruning evidence,
   regulon membership, and activity scores as separate outputs.
4. For activity scoring, retain the prior source, sign/mode of regulation, target-set
   size, coverage, method, and score matrix. Treat scores as relative unless the
   method provides a validated cross-dataset calibration.
5. Test stability across donors, resampling, reasonable filters, resources, and
   thresholds. Report regulon size and target overlap; large overlapping regulons can
   create redundant activities.
6. For condition differences in regulon activity, model biological-replicate
   summaries or replicate-aware continuous scores with a method appropriate to the
   derived activity scale. Do not send activity scores to a raw-count pseudobulk
   model or test cells as biological replicates. Use `test-single-cell-expression`
   only for target-gene expression contrasts from raw counts.
7. Seek orthogonal support from accessible motifs/enhancers, ChIP/CUT&RUN, genetic
   perturbation, temporal ordering, or independent datasets. Keep conflicting evidence.

## Report bounded claims

Use “inferred activity,” “motif-supported regulon,” “putative TF-target edge,” or
“candidate regulatory program.” TF expression is neither necessary nor sufficient for
activity, and motif presence is not binding. Reserve “driver” or “regulates” for a
design with appropriate intervention and response evidence.

## Compose with the suite

- Use `annotate-single-cell-types` and `apply-single-cell-conventions` for stable state
  labels and aligned objects.
- Use `create-scientific-figures` for activity maps, regulon heatmaps, and network
  panels without duplicating plotting rules here.
- Use `ensure-biomedical-reproducibility` for priors, motif databases, reference build,
  parameters, code, and artifacts.
- Require `verify-biomedical-analysis` to audit resource compatibility, sample support,
  target-set coverage, motif pruning, threshold sensitivity, and causal wording.
