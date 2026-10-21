# Learn structure from reference figures

Read this when studying a paper corpus or choosing a figure pattern. Start from
local full text and rendered figures, not the journal name. Record paper, figure,
page, reading scope and the source of each observation. Keep copyrighted figure
crops and private library paths in the project outputs, outside a public skill.

## Extract the argument before the geometry

For each main figure, write its question, answer and evidence groups. Link each
supporting figure to the inference it tests or extends. Distinguish an author's
claim from your interpretation. Read the corresponding Results and captions;
inspect Methods when an assay's meaning or design changes the inference.

Count independently lettered panels. Also record nested image fields, axes or
facets when density matters. A single letter can cover several views that must
move together. An unlettered display has no observed letter count; do not infer
labels from its caption. Missing supplements are unavailable, not zero.

Useful patterns have a scientific reason:

| Pattern | Use when | Preserve |
|---|---|---|
| Column chains | Each column develops a distinct line of evidence | Within-column order and clear transition to the next column |
| Matched rows/columns | Conditions share assays or calibration steps | Aligned scales, equal type size and condition identity |
| Image + quantification | A representative field needs a population readout | Their adjacency, sampling context and scale bars |
| Wide overview + focused tests | A workflow, trajectory or genomic region anchors local evidence | Overview readability and links to the focused comparisons |
| Complementary intervention blocks | Different perturbations test the same explanation | Both directions of evidence, including informative null results |

Chart variety is a consequence of complementary evidence. Repeated assays may
need repeated chart types. Never add a diagram, change a valid chart or move a
critical control to supplement just to create visual variety.

## Main versus supporting evidence

Apply the removal test in the main skill. Supporting figures often hold essential
validation; their location does not make them scientifically minor. Main should
still show enough of the decisive comparison for the reader to follow the claim.
Prefer a concise main comparison with an explicit supporting link to either
hiding the evidence or duplicating the entire experiment.

Examples from a local four-paper development study (53 figures, 2026-10-14):

- [Stankey et al., Nature 2024](https://doi.org/10.1038/s41586-024-07501-1),
  Figs 1–5: disease locus → necessity → sufficiency → regulatory mechanism →
  human context and candidate intervention. Fig. 1 uses column chains. The
  unsuccessful metabolic rescue in Fig. 4 constrains the explanation and belongs
  in the main argument. The ex vivo results do not establish clinical efficacy.
- [Zhang et al., Nature 2020](https://doi.org/10.1038/s41586-020-2071-9),
  Figs 1–4: functional protein → immune dependence → killer-cell-triggered death
  → direct proteolysis. Extended Data Fig. 11 contains mutant/rescue evidence;
  review its causal role before treating it as optional detail.
- [Grob et al., Nature Communications 2024](https://doi.org/10.1038/s41467-023-44396-4),
  Figs 1–4: assay construction/calibration → changed conditions → drug response
  → combined reporter application. Keep the core calibration in main. Supplementary
  Figs 7 and 10 test medium and optical confounding, rather than adding decoration.
- [Hayward et al., Cancer Cell 2026](https://doi.org/10.1016/j.ccell.2026.03.022),
  Figs 1–5: tissue tension → macrophage/STAT3 involvement → lipid products →
  complementary perturbations → early-lesion/human context. Image fields and
  quantification often share one letter. The cited supplement was unavailable
  in this study and was not counted or reviewed.

These examples describe the papers; they do not prescribe a universal sequence
or figure count. The 18 main figures had 4–14 letters (median 7), too broad and
too selected a sample to justify a quota. Published small fonts are not targets.
Use the user's final-size typography requirements.

## Measure what the source supports

Use the definitions in [layout review](layout-review.md). Separate white-pixel
fraction from external whitespace. A micrograph and a scatterplot naturally have
different pixel occupancy. Native PDF font sizes require a stated statistic and
role; a median over all spans is not an axis-label median. Raster-only typography
is unmeasured unless its source settings are known. For color, record the
biological mapping and redundant labels, not just the number of distinct colors.
