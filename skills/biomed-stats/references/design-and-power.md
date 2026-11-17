# Experimental design and power

Use when planning allocation, replication, factorial questions or sample size.
Consult the relevant [shared principle](../../biomed-shared/statistical-principles.md)
for interpretation; the optional [source catalogue](../../biomed-shared/statistical-sources.md)
contains the full design bibliography. This workflow is the suite's practical synthesis.

## Make the design answerable

Write a compact design record with the information needed for this task:

| Decision | Record |
|---|---|
| Biological target | Population, outcome, scale, time point and meaningful effect |
| Replication | Allocation unit, sampling hierarchy and counts at each level |
| Comparison | Control, contrasts, factors, interactions and comparison family |
| Variation | Biological variation to sample; technical or nuisance variation to control |
| Allocation | Randomization and blocking scheme; masking where feasible |
| Analysis | Model, covariance structure, effect/interval definition and error criterion |
| Resources | Available units, measurement costs, losses and practical constraints |

Use paired designs when the same unit or a justified match can supply both
conditions. Keep the matching in the analysis. Record whether time points use
repeated measurements or destructive sampling. Arrange batches so treatments can
be compared within batches; a treatment perfectly confounded with batch cannot
be separated from that batch effect by including both in a model.

For a complete block, allocate each treatment within every block. When a block
cannot accommodate all treatments, choose an incomplete-block design that supports
the required contrasts and model the actual allocation. Assess the variance removed
by blocking against its degrees-of-freedom and resource costs; blocking does not
guarantee higher power.

For a treatment-by-genotype question, use the relevant combinations and estimate
the interaction and informative simple effects. In a 2 × 2 design, the additive
interaction is $(\mu_{11} - \mu_{01}) - (\mu_{10} - \mu_{00})$, where the indices
identify the levels of A and B. State the response scale. A difference
in the significance labels of two contrasts does not estimate this quantity.

## Rehearse the proposed data and analysis

For a new experiment, build a small mock data table at the planned observation
level. Include unit and parent IDs, treatment, blocks/batches, time and measurement
columns needed for the actual design. Apply the proposed allocation, including
destructive sampling or repeated measurements as appropriate.

Run the intended model and contrasts on clearly labeled simulated outcomes.
Check that the target effect is estimable, that matching and nesting are preserved,
and that treatment can be separated from batch or other design factors. If a design
choice prevents the comparison, revise the allocation and rerun the affected step.
Consider plausible outcome patterns and what each would mean biologically.

Retain the mock table and runnable analysis with the design record. Use this run
to test the data structure and analysis route; justify sample size with the effect,
variance and error assumptions in the power calculation below. For a simple design,
a short table and analysis are sufficient. This rehearsal adapts Box 1 of
[How thoughtful experimental design can empower biologists in the omics era](https://www.nature.com/articles/s41467-025-62616-x).

## Map the hierarchy to the analysis

| Allocation or sampling structure | Analysis implication |
|---|---|
| Each animal receives one treatment; subsamples belong to that animal | Animals are nested within treatment; retain subsample dependence and use animal-level information for the treatment comparison |
| Each donor supplies material to all treatments | Donor and treatment are crossed; preserve the within-donor comparison and donor block |
| One factor is allocated to an animal and another to its tissue aliquots | Record both allocation levels and use the corresponding error structure for each effect |

Choose fixed effects for the specific comparisons of interest and random components
when modeling population variation is justified. A block's name alone does not
determine that choice. An omnibus F test addresses equality of the relevant means;
report the scientific contrasts and their intervals as well.

In the balanced nested example in *Nested designs*, the treatment F test uses the
between-mouse mean square and its degrees of freedom, rather than the residual
from technical readings. Check the actual model's error terms, covariance and
degrees of freedom before computing inference; do not apply that example's
next-layer denominator to every hierarchical design.

In a split-plot design, map each factor to its allocation level: whole plots,
subplots and their interaction can require different error terms and precision.
Keep cages, animals and aliquots distinct when they play different allocation roles.
Destructive samples at different times have a different dependence structure from
repeated measurements on the same unit.

## Choose factorial coverage and design optimality

Use a full factorial design when all combinations and interactions matter and are
feasible. For a fractional factorial design, report the alias structure and which
interactions must be assumed negligible. An unreplicated saturated model has no
residual degrees of freedom for an ordinary error estimate. Record factor coding:
with two-level ±1 coding, a main effect averaged over the other factor is twice
its coefficient. The 2 × 2 difference-in-differences defined above is four times
the product-term coefficient. State the contrast and factorial-effect convention.

For constrained designs, state the candidate region, assumed response model,
resource constraints and objective. D-optimal design targets joint coefficient
precision; I-optimal design targets average prediction variance over a specified
region. Include interior settings when curvature or lack of fit must be assessed.
An optimal allocation is conditional on these choices; compare practical alternatives.

Control nuisance variation while sampling the backgrounds needed for the target
population. If treatment effects vary by background, deliberate heterogeneity or
crossed blocks can improve the relevance of the estimate. Choose this scope from
the biological question and resources; preserve measurement consistency.

## Allocate replication to the question

Estimate important variance components from relevant pilot data or sources and
identify their uncertainty. For a balanced mouse → cell → reading hierarchy with
independent additive variance components, the variance of the grand mean is

$$
\operatorname{Var}(\bar X) =
\frac{\sigma^2_{\mathrm{mouse}}}{n_{\mathrm{mouse}}} +
\frac{\sigma^2_{\mathrm{cell}}}{n_{\mathrm{mouse}}n_{\mathrm{cell}}} +
\frac{\sigma^2_{\mathrm{reading}}}{n_{\mathrm{mouse}}n_{\mathrm{cell}}n_{\mathrm{reading}}}.
$$

Use this illustration to explain why extra readings reduce only some uncertainty.
For the actual design, compute power or precision with its model, cluster sizes
and contrasts. A question about between-animal means and a question about
within-animal heterogeneity can favor different allocations. Compare gains with
costs; retain technical replication when assay precision or quality control is a
study objective. A model cannot recover unsampled population variation.

The 2020 correction to *Nested designs* changes the example's technical-replicate
count from 5 to 3, corrects the cell and reading cost subscripts, and points to
Fig. 3b. The original PDF retains those errors. Use the corrected assumptions when
reconstructing that example; retain per-level costs explicitly in a new design.

## Calculate sample size or attainable precision

Specify the effect in biological units, expected SD or other distribution
parameters, sidedness, alpha/error control, target power, allocation ratio and the
unit to which n refers. For pairs, use variability of the differences or a stated
within-pair correlation. For clusters and repeated measures, preserve dependence
in the calculation. Match the planned multiplicity adjustment and contrast.

Use an established analytic calculation for a matching simple design; use a
documented model-based simulation when the design requires it. Check function
definitions: n may mean units per arm, total units or pairs. Round to a feasible
allocation and recheck power or precision. Record assumed losses separately from
the number required for analysis. Treat any unknown inputs as labeled scenarios.

Show a small range over plausible effect and variance assumptions rather than a
single unsupported number. If resources are fixed, report the effects detectable
at the chosen power or the expected interval precision. Set alpha and power to
fit the scientific costs of errors; 0.05 and 80% are conventions, not universal
requirements. More sampling improves precision but does not remove bias.

For completed studies, interpret the estimate and interval. Use a new planning
calculation to address a future study, with independently justified alternatives
or clearly labeled assumptions. An observed-effect power calculation adds no
independent evidence to the result being assessed; see Hoenig & Heisey (2001),
sections 2.1 and 3, [DOI](https://doi.org/10.1198/000313001300339897), read as a
supplementary source outside Points of Significance.

Deliver the selected design, assumptions, calculation source and result, feasible
alternatives and the few missing inputs that materially change the recommendation.


## Additional design sources

- *Split plot design*, pp. 165–166: [nmeth.3293](https://doi.org/10.1038/nmeth.3293).
- *Two-level factorial experiments*, pp. 211–212, corrected Table 1: [s41592-019-0335-9](https://doi.org/10.1038/s41592-019-0335-9).
- *Optimal experimental design*, pp. 559–560: [s41592-018-0083-2](https://doi.org/10.1038/s41592-018-0083-2).
- *The standardization fallacy*, pp. 5–7: [s41592-020-01036-9](https://doi.org/10.1038/s41592-020-01036-9).
