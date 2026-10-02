---
name: infer-cell-cell-communication
description: Infer candidate ligand-receptor signaling between annotated cell populations from single-cell or spatial expression data. Use for within-condition interaction screening, replicate-aware condition comparisons, pathway-level communication summaries, receiver-response prioritization, or integrating expression with spatial proximity. Supports method selection among CellChat, LIANA, CellPhoneDB, NicheNet, and related tools while enforcing species/database compatibility, sample replication, composition-aware interpretation, and non-causal claims. Do not use as physical proof that two cell types communicate.
---

# Infer Cell-Cell Communication

Produce a ranked, auditable set of signaling hypotheses. Expression compatibility,
database membership, and spatial proximity can increase plausibility; none alone proves
ligand secretion, receptor engagement, downstream response, or causal communication.

## Establish prerequisites

1. Start from defensible cell-type/state labels. Use `annotate-single-cell-types` when
   annotation is incomplete or uncertain.
2. Retain sample/donor and condition identities. Cells are observations within
   biological units, not independent condition replicates.
3. Check sender and receiver abundance, detection, ambient RNA, doublets, annotation
   uncertainty, and representation across samples. Avoid universal minimum-cell
   cutoffs; quantify the support available for each population and method.
4. Select a ligand-receptor resource compatible with species, tissue, identifiers,
   complexes, cofactors, and the biological question. Record its release through
   `ensure-biomedical-reproducibility`.

## Match the method to the question

- Use CellChat, CellPhoneDB, LIANA, or similar frameworks for candidate sender-
  receiver ligand-receptor interactions within a condition.
- Prefer a consensus framework such as LIANA when method disagreement itself is
  informative; consensus is computational robustness, not experimental validation.
- For condition differences, analyze biological units or otherwise use a
  replicate-aware design. Do not compare two pooled cell clouds as if cells were
  replicate samples.
- Use NicheNet-like ligand-to-target approaches when a defined receiver response gene
  program is part of the question.
- Add spatial adjacency/proximity only when coordinates are available and the null
  model respects tissue geometry. Coordinate this with
  `analyze-spatial-transcriptomics`.

Read `references/evidence-and-methods.md` for method and null-model decisions.

## Run and validate

1. Define sender/receiver populations, condition contrasts, expression universe,
   interaction resource, complex handling, and filtering before ranking results.
2. Run the method separately by biological unit when supported, or preserve unit
   identity in the model. Summarize recurrence and effect direction across units.
3. Distinguish changes in communication score from changes in population abundance.
   Use `test-single-cell-abundance` when composition shifts are part of the claim.
4. Confirm ligand expression in senders, receptor/complex expression in receivers,
   and plausible receiver target/pathway activity. Check whether ambient RNA or rare
   populations drive the result.
5. Apply the method's calibrated permutation/multiple-testing procedure when it
   provides one. Do not compare raw scores across tools as if they share a scale.
6. Perform sensitivity checks for database choice, expression threshold, cell-number
   imbalance/downsampling, annotation resolution, and exclusion of weakly supported
   samples.
7. Return a tidy interaction table containing sender, receiver, ligand, receptor or
   complex, pathway, database, method-specific score, calibrated significance when
   available, replicate support, condition effect, expression support, spatial or
   receiver-response support, and limitations.

## State claims precisely

Use “candidate interaction,” “expression pattern consistent with signaling,” or
“prioritized ligand-receptor hypothesis.” Do not say a sender activated a receiver or
that signaling caused a phenotype without perturbation/blocking and downstream
response evidence. A chord count is a summary of database-supported candidates, not
communication magnitude.

## Compose with the suite

- Use `test-single-cell-expression` for replicate-aware sender/receiver expression or
  response-gene comparisons.
- Use `create-scientific-figures` for dot, heatmap, network, chord, and spatial panels.
- Use `ensure-biomedical-reproducibility` for database release, parameters, software,
  and result artifacts.
- Require `verify-biomedical-analysis` to audit biological units, score comparability,
  multiplicity, composition confounding, replicate recurrence, and claim language.
