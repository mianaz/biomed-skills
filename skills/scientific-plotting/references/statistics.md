# Figure-level statistical analysis

For a task requiring inference, use a supplied valid analysis or compute the analysis
warranted by the design. Appearance-only repairs preserve the existing valid analysis.
Put the choice and comparison family in the analysis script before calculating results.

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
specific limitation and plot what is known.

## Choose a defensible analysis

| Design / estimand | Starting analysis and display |
|---|---|
| Two independent groups; mean difference | Two-sided Welch t test with mean-difference CI when mean-based inference is justified; points plus mean and defined spread |
| Two matched conditions | Paired t test of within-unit differences when justified; matched points/lines. Consider a paired rank or design-based randomization test when its assumptions fit |
| More than two independent groups | Model/ANOVA appropriate to variances and design, with justified contrasts; use Welch methods for unequal variances when applicable |
| Identified experimental blocks/batches | Include a fixed block effect, an appropriate hierarchical model, or justified block-level contrasts; an unblocked Welch test does not account for an identified batch |
| Factorial experiment | Preserve all factors; test interactions explicitly if making an interaction claim. Planned within-stratum contrasts can answer a narrower question without claiming interaction |
| Repeated time course | Mixed/repeated-measures model for a trajectory hypothesis. Time-specific comparisons can use each unit once per time, with correction across times, but do not test a treatment-by-time interaction |
| Dose response across compounds | Fit and diagnose a suitable 4PL/5PL model; read `dose-response.md` for model selection, potency definitions, uncertainty and curve comparisons. Retain actual doses and experimental units; unequal mixtures of doses are not exchangeable compound replicates |
| Skewed, ordinal or bounded observations | Choose a scale/model or rank method suited to the estimand and support. Do not automatically log zeros or call a rank test a test of means |
| Proportions or contingency counts | Binomial/count-based methods at the independent unit; Fisher or chi-squared when appropriate. Do not reconstruct joint predictions from marginal tables |
| Association | Scatter with a justified correlation/regression and uncertainty; account for repeated/clustered observations and avoid causal language |
| Survival | Censor-aware Kaplan–Meier; log-rank or survival model for a defined comparison. Do not treat censor times as events |
| Many exploratory molecular features | Appropriate feature-wise analysis and an explicit FDR family; preserve effect magnitude and underlying expression evidence |

Inspect values, outliers, scale and residual/difference structure where relevant.
Small n cannot establish normality or make an asymptotic approximation reliable.
Wilcoxon signed-rank inference also has assumptions; do not use it as an automatic
safe fallback. Record assumptions and keep the small-sample uncertainty visible.
Default to two-sided comparisons unless a directional alternative was prespecified.

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
Do not generate every pairwise comparison just to fill the plot with brackets.

## Save and annotate

Save group names and contrast direction, independent n, effect estimate, interval and
confidence level, statistic/df when defined, test/sidedness, raw P, adjusted P,
correction method/family, exclusions and software version. Keep full precision in CSV.
A nominal effect CI is not a simultaneous CI merely because P values were adjusted.

Choose annotation visibility before reading P values. Both R and Python helpers
accept `nonsignificant="hide"` (default), `"ns"`, or `"value"`, and `alpha=0.05`.
Use unrounded P < alpha for significance; P equal to alpha is nonsignificant. When
correction applies, use the adjusted P column after correcting the complete family.
The `adjusted` flag changes the label prefix; it does not calculate a correction.

| Mode | Significant comparison | Nonsignificant comparison |
|---|---|---|
| `hide` | Numeric P and comparison line | No label or line |
| `ns` | Numeric P and comparison line | `ns` and comparison line, without numeric P |
| `value` | Numeric P and comparison line | Numeric P and comparison line |

Keep the complete statistical table, estimates and intervals in every mode. Missing
or untestable results require an explicit, explained `missing_label`; they are never
classified as `ns` or silently hidden. A key negative comparison may use `value` or
`ns` explicitly; name the contrast and why its result belongs on the figure, or cite
the user's request. Apply that exception to the named rows. An all-nonsignificant
family keeps the default; repeating every P value is not needed to preserve the
complete results, which remain in the table.
An absent annotation is not evidence of equivalence or absence of an effect.
State the visibility rule in the caption, for example: "Only comparisons with Holm-
adjusted P < 0.05 are annotated; all planned comparisons are in statistics.csv."

For visible categorical comparisons, use `P adj.` or a short shared adjustment label;
keep the full method in the caption. For `ns` mode, define `ns` and the threshold.
Round only labels. Both helpers start with two significant digits and increase to
six when rounding would change the value's relation to `alpha`, including rounding
onto the threshold. If six digits remain ambiguous, use a truthful `P < alpha` or
`P > alpha`; exact equality stays `P = alpha`. The small-value reporting bound is
`min(0.0001, alpha)`. Thus a custom threshold below 0.0001 remains interpretable.
Never display a nonzero value as zero; keep the full value in the statistical table.
Retain outcome, stratum, group pair, numeric P and rendered label in each comparison
row. Format the full P vector with `p_labels()`; hidden labels are empty strings and
retain their positions. Filter complete rows only for drawing, never the statistical
table or a separate label vector. Assign annotation lanes and y-axis headroom using
visible rows only; an all-nonsignificant panel in `hide` mode needs neither brackets
nor annotation headroom. Use the bundled helpers with numeric P columns rather than
reformatting P values in a separate plotting layer. Before export, compare the drawn
labels and brackets to the visible comparison rows; zero visible comparisons means
zero bracket geometry. Check every rendered label against its keyed numerical result,
especially after missing tests.
A model-level P belongs beside the named model term, not a bracket implying a pairwise
contrast. Define the summary/error bar and include n in the caption or unobtrusive key.

For processed feature statistics, keep raw P and adjusted P distinct. A line at
`-log10(0.05)` represents the P column used on the y axis. It is not an FDR threshold
when that axis uses raw P. Color may encode BH significance on a raw-P axis if the
legend says so; omit or correctly derive any threshold line.

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
