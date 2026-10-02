---
name: infer-single-cell-trajectories
description: Infer and validate single-cell state progressions using graph topology, pseudotime, RNA velocity, and fate probabilities. Use when cells plausibly sample a continuous biological process such as differentiation, activation, or recovery; when choosing among PAGA, diffusion pseudotime, Slingshot, Monocle3, scVelo, or CellRank; or when auditing roots, branches, terminal states, and directionality. Do not use to force an ordering across unrelated cell types, treat an embedding as time, or claim lineage ancestry without independent temporal, tracing, or perturbational evidence.
---

# Infer Single-Cell Trajectories

Treat a trajectory as a model of sampled state continuity, not a reconstructed movie.
Require a biologically coherent subset and evidence that the inferred structure is not
driven by batch, doublets, cell cycle, stress, or one donor.

## Establish the question and prerequisites

1. State whether the task needs topology, relative ordering, direction, terminal-state
   probabilities, or gene changes along an already accepted path.
2. Start from a quality-controlled, annotated object. Use
   `preprocess-single-cell-rna` and `annotate-single-cell-types` when those gates have
   not been passed.
3. Restrict to cell states that could plausibly share a process. Do not connect broad
   immune, stromal, and epithelial compartments simply because an embedding places
   them nearby.
4. Inspect support by sample, donor, condition, and observed time point. If the path
   exists only in one sample or there are no biological replicates, label it
   descriptive and do not generalize.
5. For velocity, confirm that spliced/unspliced layers came from a compatible assay
   and quantification workflow and retain adequate signal after QC.

## Choose the method by the evidence needed

- Use PAGA or another graph abstraction to test coarse connectivity and candidate
  branches before fitting a fine ordering.
- Use diffusion pseudotime for a connected continuum with an externally justified
  root; use Slingshot or Monocle3 when multiple lineages or graph branches are needed.
- Use RNA velocity only when kinetic layers and diagnostics support directionality.
- Use CellRank when transition kernels and terminal states are credible enough to
  estimate fate probabilities; fate quality cannot exceed kernel quality.
- Use observed sampling time, lineage barcodes, or perturbations as external evidence
  whenever available rather than asking pseudotime to replace them.

Read `references/method-selection.md` before selecting or combining methods.

## Run and validate

1. Define the lineage subset, feature space, graph, root, and candidate terminal
   states before interpreting results.
2. Fit the smallest method that answers the question. Preserve method-native outputs
   when translating them would alter graph or kinetic semantics.
3. Check topology and ordering across donors, resampling, reasonable graph settings,
   and alternative defensible roots. Report unstable branches rather than selecting
   only the preferred result.
4. For velocity, inspect gene-level phase portraits or fit diagnostics, velocity
   confidence/coherence, boundary behavior, and agreement across samples. Reject
   arrows dominated by low counts or a few genes.
5. For fate models, test sensitivity to terminal-state definitions and kernel weights;
   confirm probabilities are calibrated as relative model outputs, not observed fate.
6. Test smooth or branch-specific trends with a trajectory-aware model (for example,
   a GAM/tradeSeq-style model) while preserving donor/sample through supported design
   terms, per-unit fits, or stability summaries. Use `test-single-cell-expression`
   only for raw-count contrasts between predefined states or conditions, not for
   pseudotime response curves, and never treat cells as biological replicates.
7. Preserve a structured result containing lineage membership, root and terminal
   definitions, pseudotime or transition values, branch assignments, uncertainty or
   stability summaries, and per-sample support.

## Interpret conservatively

- Pseudotime is relative order, not elapsed time; its scale and distance are usually
  not physically meaningful.
- A branch is a model-supported state split, not proof that one cell became another.
- Velocity reflects model assumptions about RNA kinetics and sampling; it is not
  direct observation of future state.
- Fate probabilities are conditional on the fitted state space, transition kernel,
  and terminal states.
- Root choice can reverse the story. Justify it from external markers, observed time,
  lineage tracing, or perturbation—not visual preference.

## Compose with the suite

- Apply object and identity rules from `apply-single-cell-conventions`.
- Send trajectory, embedding, and trend panels to `create-scientific-figures`.
- Record inputs, layers, graph settings, roots, seeds, software, and artifacts with
  `ensure-biomedical-reproducibility`.
- Require `verify-biomedical-analysis` to audit sample support, roots, topology
  stability, kinetic diagnostics, branch claims, and figure/source-data agreement.
