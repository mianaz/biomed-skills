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

## Empirical composition priors from the 500-panel CNS corpus

Across 500 independent quantitative panels curated from 49 *Cell* (156), *Nature*
(204) and *Science* (140) papers, complex multi-layer displays account for over
65% of quantitative panels (136 matrices/dot-plots, 53 distributions, 45 group
comparisons, 41 enrichment views, 39 compositions, 32 embeddings, 32 time-courses,
19 hierarchies, 17 genomic tracks, 16 networks). Use these recurring panel-pairing
and aspect-ratio priors when allocating space in `figure-plan`:

| Evidence unit | Typical CNS panel pairing | Starting panel aspect & allocation |
|---|---|---|
| **Single-cell / spatial atlas** | Hero embedding (`embedding`, 1:1 square with numbered badges) + per-donor stacked composition (`composition`, narrow/tall) + marker dot matrix (`matrix`, rectangular) | Give the hero embedding and dot matrix ~60–65% of row width; keep composition bars narrow (25–35 mm plot width). |
| **Mechanistic perturbation** | Experimental design / pathway schematic (`scientific-visual-explainer`, wide top banner or top-left anchor) + primary assay comparison (`group-comparison`, narrow/tall) + dose/time trajectory (`time-course` or `dose-response`) | Start 2–4 group comparisons narrower than tall (e.g., 30–42 mm wide × 50 mm tall) so 3–4 related readouts fit across one 180 mm row without shrinking text below 10 pt. |
| **Omics screen / pathway discovery** | Volcano or ranked overview (`enrichment`, ~50 × 50 mm) + GSEA running-score composite or leading-edge heatmap (`matrix` with sample covariate tracks) | Keep GSEA running score, hit ticks and rank metric vertically locked as one panel asset; scale heatmap height by feature count (`~3.5–4.5 mm` per labeled row). |
| **Clinical / translational cohort** | Cohort overview / OncoPrint (`genomic`, wide banner) + Kaplan–Meier with aligned risk table (`survival`, 50–65 mm wide × 65–75 mm tall including risk rows) + multivariable forest plot (`association`, horizontal) | Reserve at least `1.4 × text_pt × 25.4 / 72` mm per risk-table row below the survival axis; align forest plot labels on the left and effect intervals on the right. |

All 300 expansion adapters omit embedded publication panel letters (`a`, `b`, `c`)
at the code export stage while retaining internal condition, axis, legend and node
labels. Follow the same separation in `figure-plan`: export letter-free panel assets
from R/Python and place panel letters as independent PowerPoint text boxes.

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
Use the user's final-size typography requirements in
[visual standards](../../biomed-shared/visual-standards.md).

## Measure what the source supports

Use the definitions in [layout review](layout-review.md). Separate white-pixel
fraction from external whitespace. A micrograph and a scatterplot naturally have
different pixel occupancy. Native PDF font sizes require a stated statistic and
role; a median over all spans is not an axis-label median. Raster-only typography
is unmeasured unless its source settings are known. For color, record the
biological mapping and redundant labels, not just the number of distinct colors.
