# Communication method and evidence guide

## Method families

| Question | Useful family | Main limitation |
|---|---|---|
| Which cell populations express compatible ligands/receptors? | CellChat, CellPhoneDB, LIANA methods | Co-expression and curated prior only |
| Are candidates robust across algorithms/resources? | LIANA-style consensus/rank aggregation | Shared databases and assumptions create correlated evidence |
| Which ligand may explain a receiver gene program? | NicheNet-like ligand-target modeling | Prior network and response-gene definition dominate ranking |
| Is signaling spatially plausible? | Spatially constrained ligand-receptor analysis | Proximity is not contact, secretion, or direction |
| Does signaling differ by condition? | Replicate-aware differential framework or per-unit summaries | Pooled-cell comparisons create pseudoreplication |

Check current official documentation for supported species, resources, complex rules,
normalization expectations, and score interpretation. Do not transfer thresholds or
probability scales from one framework to another.

## Define the population and expression universe

- Use biologically interpretable labels at a resolution supported across samples.
  Over-splitting creates rare populations and unstable edges; over-merging obscures
  state-specific signals.
- Preserve zero/missing distinctions and the genes actually measurable after QC.
- Handle multisubunit receptor/ligand complexes according to the selected resource;
  a highly expressed single subunit may not imply a functional complex.
- Ortholog conversion can lose paralog, complex, and species-specific signaling
  information. Mark mapped and unmapped interactions.

## Compare conditions without pseudoreplication

- Keep donor/sample as the experimental unit. Estimate or summarize interactions by
  unit when possible, then compare units or report recurrence.
- Separate abundance effects from per-cell-state expression effects.
- Match population definitions and interaction resources across conditions.
- Do not interpret different numbers of detected edges after unequal cell sampling as
  network rewiring without cell-number sensitivity checks.
- If one condition lacks a cell population, report absence/estimability explicitly;
  do not fabricate a zero score on an incomparable population set.

## Build an evidence ladder

Treat each layer as additional support, not automatic validation:

1. Ligand and receptor/complex expression in the proposed populations.
2. Replicate recurrence and a stable condition effect.
3. Compatible receiver pathway or target-gene activity.
4. Spatial adjacency or tissue-compartment plausibility.
5. Protein-level localization or secreted-ligand measurement.
6. Perturbation/blocking with a receiver response and appropriate controls.

Only the later experimental layers can support strong mechanistic language.

## Common failure modes

- Ambient RNA makes abundant secreted ligands appear broadly expressed.
- Doublets create artificial sender-receiver co-expression.
- Cell-type abundance or annotation granularity changes edge counts.
- Rare populations yield unstable ranks.
- Database overlap makes cross-method consensus less independent than it appears.
- Network/chord visuals exaggerate dense edge counts and hide uncertainty.

Use `create-scientific-figures` to show replicate support, expression evidence, and
uncertainty rather than only an aesthetically dense global network.
