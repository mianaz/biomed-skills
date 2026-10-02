---
name: prioritize-single-cell-targets
description: Prioritize disease-relevant cell states and therapeutic target candidates by integrating single-cell expression with human genetics, variant-to-gene evidence, regulatory context, perturbation results, tractability, and safety. Use for scDRS or cell-type enrichment, fine-mapping/colocalization-informed gene nomination, Open Targets or DepMap evidence review, and transparent multi-criteria ranking. Treat database scores and computational associations as evidence components rather than validation, avoid double-counting correlated sources, and do not call a ranked candidate a causal disease gene or validated target.
---

# Prioritize Single-Cell Targets

Produce a transparent evidence matrix and ranked candidate set, not a single opaque
score. Keep cell-state relevance, variant-to-gene mapping, functional support,
tractability, and safety separate until their assumptions and conflicts are visible.

## Define the decision

1. State the disease/phenotype, population and ancestry, tissue/context, intended
   intervention direction, target modality, and whether the task is cell-state
   prioritization, gene nomination, or therapeutic ranking.
2. Require an annotated single-cell object with biological-unit metadata and a
   compatible genetics input when making genetics-based claims.
3. Check GWAS/QTL genome build, alleles, ancestry/LD reference, sample overlap, locus
   definition, and gene identifiers before scoring.
4. Define ranking criteria, hard exclusions, and evidence tiers before inspecting
   candidate names. Missing evidence is unknown, not zero.

## Build the evidence ladder

1. **Cell-state relevance:** use GWAS-informed gene scores or heritability-enrichment
   methods appropriate to the input. scDRS yields disease-association scores relative
   to matched control gene sets; it does not identify causal cells.
2. **Variant-to-gene support:** combine fine-mapping with context-matched eQTL/sQTL
   colocalization and, when appropriate, chromatin links. Do not default to the nearest
   gene or interpret a colocalization posterior as experimental proof.
3. **Single-cell context:** evaluate expression, state specificity, condition effects,
   and regulatory programs with replicate-aware evidence. Route regulatory questions
   to `infer-single-cell-regulation`.
4. **Functional perturbation:** use `analyze-perturb-seq` or orthogonal experiments to
   test direction and consequences in relevant cells. Preserve off-target and efficacy
   uncertainty.
5. **Translation:** review tractability, known drugs, tissue distribution, essentiality,
   adverse biology, and genetic direction of effect. Open Targets and similar resources
   aggregate evidence but do not make components independent.

Read `references/evidence-ranking.md` before combining scores or querying mutable
resources.

## Rank without hiding assumptions

1. Create one row per candidate and one column per evidence component, with source,
   direction, context, confidence, missingness, and conflict flags.
2. Normalize only comparable quantities. Do not add raw scores from different tools or
   databases simply because each ranges from zero to one.
3. Avoid double-counting the same GWAS, publication, or database-derived evidence
   through multiple aggregators.
4. Use prespecified hard gates for incompatible direction, absent targetability, or
   unacceptable safety only when justified. Otherwise retain separate component ranks
   and a Pareto/criteria view.
5. If weights are used, expose them and repeat the ranking across defensible choices.
   Highlight candidates whose rank is unstable.
6. Validate top candidates in independent cohorts/atlases where possible and retain
   negative or conflicting evidence.

## Interpret conservatively

- Cell-state enrichment means disease-associated genes are overrepresented under the
  method; it does not show that the cell state causes disease.
- Colocalization supports a shared local genetic signal under model assumptions; it
  does not prove the nominated gene or direction without additional evidence.
- Database association scores are prioritization aids, not calibrated probabilities of
  efficacy.
- DepMap dependency is context-specific and can signal either an oncology opportunity
  or a safety liability; cell-line effects do not establish normal-tissue safety.
- A final rank is conditional on available evidence and criteria. Call outputs
  “prioritized candidates” or “genetically supported hypotheses,” not validated targets.

## Compose with the suite

- Use `annotate-single-cell-types`, `test-single-cell-expression`, and
  `test-single-cell-abundance` for cell-state evidence.
- Use `create-scientific-figures` for evidence matrices, rank stability, locus, and
  cell-state panels.
- Use `ensure-biomedical-reproducibility` for mutable database snapshots, query
  results, genetics resources, criteria, and artifacts.
- Require `verify-biomedical-analysis` to audit allele/build alignment, LD/ancestry,
  colocalization assumptions, source overlap, ranking weights, conflicts, and claim scope.
