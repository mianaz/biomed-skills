# Statistical analysis decisions

Read the section needed for the current analysis, review or figure task. Consult
the relevant [statistical principle](statistical-principles.md) when its rationale
or interpretation is needed. This file maintains shared execution rules. The model menu
and software checks consolidate existing suite guidance; topics beyond the cited
full texts are not presented as summaries of Points of Significance.

Reuse a valid supplied analysis. Select the model and comparison family from the
question and design before calculating results. Record choices made after seeing
data as exploratory and preserve their rationale.

When choosing methods or reusing molecular features, apply
[analysis consistency and reuse](analysis-consistency.md). Use the same
feature definitions across comparable analyses and select established methods
suited to the question and design.

## Identify the information available

Record independent unit, outcome scale, groups, pairing/blocking, repeated measures,
technical measurements per unit, missing values and any prespecified contrasts.
Aggregate technical readings within the biological unit when that matches the
estimand, or use an appropriate hierarchical model. Never count cells, wells or time
points as independent animals/donors. Join paired observations by ID, not row order.

Before choosing a test, establish that the design identifies independent units.
Eligibility depends on the design and quantities needed for the requested inference,
not on a universal requirement for public sample IDs or raw observation rows.
An explicit independent-sample design can support inference without public sample
names; arbitrary row IDs, duplicate records or missing batch labels cannot supply
that evidence. When independence or the relevant matching cannot be determined,
finish the descriptive analysis and record the unavailable inference. A rank test
or a nominal multiple-testing correction does not repair an unidentified hierarchy.

Summary means and error bars alone are not raw samples. Some summary-statistic tests
are identifiable when n and SD and the required assumptions are known; pairing,
covariance and distributions cannot be recovered from a chart summary. State the
specific limitation and summarize what is known.

## Choose the analysis for the estimand

| Design / estimand | Starting analysis |
|---|---|
| One mean against a fixed reference | One-sample t test/interval when mean-based inference is justified; if the reference is estimated from another sample, include its uncertainty in the comparison |
| Two independent groups; mean difference | Two-sided Welch t test with mean-difference CI when mean-based inference is justified |
| Two matched conditions | Paired t test of within-unit differences when justified. Consider a paired rank or design-based randomization test when its assumptions fit |
| More than two independent groups | Model/ANOVA appropriate to variances and design, with justified contrasts; use Welch methods for unequal variances when applicable |
| Identified experimental blocks/batches | Include a fixed block effect, an appropriate hierarchical model, or justified block-level contrasts; an unblocked Welch test does not account for an identified batch |
| Nested or crossed sampling/allocation | Map units to their parent levels and treatment assignments; use justified unit-level summaries or a model with the corresponding dependence, error terms and degrees of freedom |
| Factorial experiment | Preserve all factors; test interactions explicitly if making an interaction claim. Planned within-stratum contrasts can answer a narrower question without claiming interaction |
| Repeated time course | Mixed/repeated-measures model for a trajectory hypothesis. Time-specific comparisons can use each unit once per time, with correction across times, but do not test a treatment-by-time interaction |
| Dose response across compounds | Fit and diagnose a suitable dose-response model; define potency, uncertainty and curve comparisons. Retain actual doses and experimental units; unequal mixtures of doses are not exchangeable compound replicates |
| Skewed, ordinal or bounded observations | Choose a scale/model or rank method suited to the estimand and support. Do not automatically log zeros or call a rank test a test of means |
| Proportions or contingency counts | Binomial/count-based methods at the independent unit; Fisher or chi-squared when appropriate. Do not reconstruct joint predictions from marginal tables |
| Association | Justified correlation/regression and uncertainty; account for repeated/clustered observations and distinguish association from a causal effect supported by the design |
| Survival | Censor-aware Kaplan–Meier; log-rank or survival model for a defined comparison. Do not treat censor times as events |
| Many exploratory molecular features | Appropriate feature-wise analysis and an explicit FDR family; preserve effect magnitude and underlying expression evidence |

Inspect values, outliers, scale and residual/difference structure where relevant.
Small n cannot establish normality or make an asymptotic approximation reliable.
Wilcoxon signed-rank inference also has assumptions; do not use it as an automatic
safe fallback. Record assumptions and keep the small-sample uncertainty visible.
Distinguish a mean, median, location-shift or distributional target. Rank-sum
inference needs suitable common-shape assumptions for a median-shift interpretation;
ties and small n affect exact P-value resolution. Bootstrap the independent units
with their pairing or clustering preserved, and name the interval method.
Default to two-sided comparisons unless a directional alternative was prespecified.
An omnibus ANOVA result does not identify which contrasts differ. Report the
contrasts that address the question with their estimates, intervals and family.

A dose/time-pooled contrast requires an explicit marginal estimand, comparable or
standardized dose/time support, and a justified sampling model. Calling a pooled
test exploratory does not establish those conditions. When biological inference is
unidentified, dose-response modeling can still quantify the observed assay response
under stated conditional error assumptions. Report fit parameters, uncertainty and
diagnostics without presenting assay records as independent donors or inventing P values.

With only an exploratory data table, an agent-selected time point or subgroup is
not a prespecified comparison. Describe that selection as exploratory. Distinguish
destructive sampling at successive times from repeated measurement of the same
unit, and account for an identified experimental batch in inference.
Build the inferential table from unique experimental observations, independently
of the display table. A shared baseline duplicated for two trajectory panels must
not be fitted twice as if independently observed under both treatments. Analyze
post-treatment observations when future-arm assignment of baseline is undefined,
or use a model that explicitly represents the single shared baseline.

Choose contrasts from the design before examining P values. For a small family of
related exploratory comparisons, Holm is a useful family-wise correction; for a
large discovery screen, BH controls FDR under its dependence conditions. Define the
family, include nonsignificant comparisons, and never correct only selected hits.
Choose comparisons for their scientific purpose.

## Define families across datasets

Do not automatically correct across every dataset explored in a project or run.
For a dataset-specific question, estimate the effect, interval and raw P from its
defined analysis cohort and model. Use other datasets in a combined, hierarchical
or meta-analysis only when that is the intended analysis. Define any multiplicity
family by the scientific claims and how results were selected.

| Situation | Scope to use |
|---|---|
| Separately specified cohort analyses with cohort-specific claims | Retain each cohort's justified comparison family; sharing a project or figure does not itself require a joint correction |
| Dataset chosen by recorded eligibility or technical suitability, independently of the target result | Analyze the selected target cohort and its relevant comparisons; record the selection basis |
| Cohorts or contrasts chosen because their P values or effect sizes were most favorable | Account for that search in inference, or evaluate the selected hypothesis in independent validation data; retain the selection history |
| Several related contrasts support one family-level claim across panels | Use the full scientific family, including relevant comparisons shown elsewhere or not displayed |
| Selected features displayed from a larger molecular screen | Retain the screen's feature-level adjustment over its defined tested universe |

Exploratory results may retain nominal P values with the scope and selection stated;
identify them as unadjusted, and reserve adjusted-significance claims for the error
control actually performed. A blanket correction over unrelated analyses does not
solve an unspecified selection process.

When the intended analysis population changes under justified inclusion criteria,
recompute the corresponding estimate and inference. Moving a panel, omitting a
dataset from a figure, or displaying fewer points alone does not redefine the
analysis population or comparison family. Record dataset, analysis-cohort definition,
family membership, selection basis and adjustment method with the result.

The separation of dataset-specific families is a suite implementation decision.
The selection principle is supported by *P values and the search for significance*,
pp. 3–4, especially Figs. 1–2: [DOI](https://doi.org/10.1038/nmeth.4120).

## Missingness, exclusions and diagnostics

Reconcile missing observations and exclusions by group, unit and time. Preserve
reasons and the analysis denominator. Choose handling from the likely mechanism
and model, with sensitivity analysis when that choice changes the conclusion.
Do not silently replace missing outcomes with zero or delete observations to
improve significance. Consult primary method documentation for imputation or
specialized missing-data methods.

Inspect relevant residuals, influential observations, variance and dependence
assumptions. Keep data corrections distinct from analytic exclusions. For
resampling, preserve the independent unit and the design's valid exchangeability.
A model should have enough independent information to estimate the requested
parameters and uncertainty; fitting more rows does not create missing replication.
Interpret regression coefficients conditional on the included predictors. Check
collinearity and distinguish an interval for a mean from prediction uncertainty.
For prediction, separate training, selection and evaluation; fit preprocessing and
feature selection within training splits and keep records of one unit together.

For survival, record the event, time origin, censoring and competing events. State
the assumptions supporting the chosen estimator; evaluate proportional hazards
when reporting a constant Cox hazard ratio. Curve tests address distributions,
and hazard ratios require their own interpretation. For missing data, assess bias
for the actual estimand: a marginal mean and conditional regression can respond
differently to the same selection process.

## Retain the statistical result

Save group names and contrast direction, independent n, effect estimate, interval and
confidence level, statistic/df when defined, test/sidedness, raw P, adjusted P,
correction method/family, exclusions and software version. Keep full precision in CSV.
A nominal effect CI is not a simultaneous CI merely because P values were adjusted.

## Implementation checks

`t.test(x, y, var.equal = FALSE)` uses Welch's method; `paired = TRUE` uses matched
vectors. Check IDs and missing-pair removal explicitly. Use `p.adjust(p, "holm")` or
`p.adjust(p, "BH")` on the complete declared family. These are examples, not universal
test assignments. Check package help for models unfamiliar to you.

In Python, `scipy.stats.ttest_ind(x, y, equal_var=False)` is the Welch route;
`ttest_rel(x, y)` requires explicitly matched units. Use a named, documented
multiple-testing implementation (for example `statsmodels.stats.multitest.multipletests`
with `method="holm"` or `"fdr_bh"`) on the complete family. Preserve NA rows and
comparison keys when reconnecting results to the figure. Backend defaults do not
choose the scientific test.

Primary references: [R t.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html),
[R p.adjust](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html),
[R wilcox.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/wilcox.test.html).
