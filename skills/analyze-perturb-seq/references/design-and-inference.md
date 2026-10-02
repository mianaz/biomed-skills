# Perturb-seq design and inference guide

## Assignment is a calibrated classification problem

Use guide-count distributions, empty/negative droplets or control barcodes, and the
declared MOI/combinatorial design to set assignment confidence. Summarize assignment by
sample, batch, guide, target, and cell state. Report ambiguous, unassigned, and multi-
guide cells separately; do not force every barcode into a guide class.

Check for:

- guides or targets missing from specific batches/replicates;
- uneven guide capture or guide abundance;
- barcode swapping, ambient guide signal, or index contamination;
- guide assignment correlated with low quality or doublet metrics;
- control imbalance across samples and cell states; and
- survival/capture depletion that removes strong perturbations before measurement.

There is no universal acceptable unassigned fraction or cells-per-guide threshold.
Power depends on replicate structure, effect size, guide efficiency, expression,
dispersion, cell state, and the intended contrast.

## Define the effect unit

Keep three levels distinct:

1. **Cell-guide observation:** useful for assignment and heterogeneity.
2. **Guide effect:** preserves independent guide behavior and off-target evidence.
3. **Target effect:** combines concordant guides under an explicit rule.

With independent biological units, aggregate or model at sample × guide/target × cell
state. A large number of cells from one culture does not replace replicate cultures or
donors. When guide is the only replication layer, describe the limitation and avoid
population-level generalization.

## Choose controls and contrasts

- Use non-targeting/safe-targeting controls distributed across batches.
- Use positive controls to confirm the assay can detect an expected response.
- Compare within compatible batch, time, cell state, and donor strata or model those
  factors explicitly.
- For CRISPRa/i/KO, define direction and efficacy evidence appropriate to the modality.
- For combinatorial screens, include main effects and interaction terms only when the
  design supports their separation.

## Separate efficacy, response, and abundance

- **Efficacy:** evidence that the intended molecular intervention occurred.
- **Expression response:** within-state transcriptomic effect.
- **Abundance/viability response:** altered recovery or state frequency.

These can disagree. A depleted perturbation may have few surviving cells for expression
analysis; an expression-null result may reflect failed editing; a state shift can alter
composition without a within-state expression change.

## Guide aggregation and robustness

- Estimate each guide separately first.
- Check effect direction, magnitude, target knockdown/activation where measurable, and
  response-program overlap.
- Exclude or downweight a guide only by a prespecified, documented criterion; retain the
  discordance in results.
- Use negative controls to calibrate false discoveries and empirical effect magnitude.
- Correct across the declared gene/perturbation/contrast family.

## Output contract

Preserve cell-guide assignments and confidence, guide/sample QC, control summaries,
efficacy evidence, guide-level effects, target aggregation, abundance/viability effects,
response programs, guide concordance, and limitations. This lets
`verify-biomedical-analysis` distinguish failed perturbation from absent biological
response.
