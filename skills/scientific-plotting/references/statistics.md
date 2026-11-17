# Statistical display for figures

Read the relevant shared [statistical principles](../../biomed-shared/statistical-principles.md)
and [analysis decisions](../../biomed-shared/statistical-analysis.md) when inference
is needed. They own units, model/contrast choice, diagnostics and result records.
This reference owns statistical display. For study planning, sample-size work or
a standalone analysis/review, use `biomed-stats`.

For a task requiring inference, use a supplied valid analysis or compute the analysis
warranted by the design. Appearance-only repairs preserve the existing valid analysis.
Put the choice and comparison family in the analysis script before calculating results.

## Match statistical content to the question

For a descriptive comparison, report the units, observations and summary/interval
definitions needed to read it. For a new inferential comparison, use the valid supplied analysis or perform the
appropriate analysis from the available independent observations. State the
experimental unit and n, show observations where useful, define the mean/median
and SD/SEM/CI, and identify the primary contrast. Report its effect and uncertainty
in the caption or linked results, and its numerical raw/adjusted P value on the
figure when the design supports a test. Show a primary nonsignificant result too.
Statistics belong to the requested scientific comparison, not to a decorative
annotation pass after drawing. Do not return unlabeled summary bars or a matrix
with no explanation of its comparison, scale or analysis.

Heatmaps default to descriptive displays. Do not add statistical tests, P/q values,
significance marks or extra effect-size annotations unless the user requests them.
State the matrix unit, transformation and scale in the caption. This display
default applies even when an upstream analysis contains inferential results.
When heatmap inference is requested, analyze independent samples before display
scaling; place requested statistics outside the tiles. Add effect sizes only when
requested. Do not invent tests from summaries lacking the necessary information.

## Connect the analysis to the figure

Use the shared analysis decisions to identify units, preserve matching, choose
contrasts and define multiplicity. Build the statistical table independently of
plotting rows. Display duplication must not create extra observations in the fit.
For multiple datasets, use the shared
[family-scope rules](../../biomed-shared/statistical-analysis.md#define-families-across-datasets).
Keep dataset-specific results keyed to their analysis cohort and comparison family;
panel placement or omission alone does not change that family. State the applicable
scope and any result-driven selection in the caption or linked analysis record.
For dose-response figures, also read [dose response](dose-response.md) for potency,
curve diagnostics and the uncertainty shown on the figure.

## Save and annotate

Save the complete result fields specified in the shared analysis decisions,
including estimates, interval method/level, independent n and raw/adjusted P.
Use those keyed results for annotation. A nominal effect CI is not a simultaneous
CI merely because P values were adjusted.

Choose annotation visibility before reading P values. Use `nonsignificant="value"`
for primary or explicitly requested comparisons, so both positive and negative
results remain visible. The helper default below applies to secondary annotations.
Both R and Python helpers
accept `nonsignificant="hide"` (default), `"ns"`, or `"value"`, and `alpha=0.05`.
Use unrounded P < alpha for significance; P equal to alpha is nonsignificant. When
correction applies, use the adjusted P column after correcting the complete family.
Labels omit the P/adjusted prefix and equals sign by default; identify the test and
correction in the caption. `show_prefix=TRUE` (R) or `show_prefix=True` (Python)
restores a prefix when requested. `adjusted` selects that optional prefix; it never
calculates a correction.

| Mode | Significant comparison | Nonsignificant comparison |
|---|---|---|
| `hide` | Numeric P and comparison line | No label or line |
| `ns` | Numeric P and comparison line | `ns` and comparison line, without numeric P |
| `value` | Numeric P and comparison line | Numeric P and comparison line |

Keep the complete statistical table, estimates and intervals in every mode. Missing
or untestable results require an explicit, explained `missing_label`; they are never
classified as `ns` or silently hidden. Primary and requested contrasts use `value`
regardless of significance; use `ns` only when explicitly requested. Secondary
comparisons may remain in the complete results table.
An absent annotation is not evidence of equivalence or absence of an effect.
State the visibility rule in the caption, for example: "Numbers show Holm-adjusted
P values for the primary contrasts; all comparisons are in statistics.csv."

For visible categorical comparisons, show numeric-only labels;
keep the correction method in the caption. For `ns` mode, define `ns` and the threshold.
Round only labels. Both helpers start with two significant digits and increase to
six when rounding would change the value's relation to `alpha`, including rounding
onto the threshold. If six digits remain ambiguous, use a truthful `< alpha` or
`> alpha`; exact equality shows the numeric alpha value. The small-value reporting bound is
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

For box plots, define the quartiles, whisker rule and plotted points, and report n.
Treat a point outside a whisker as a display feature to investigate in context.
For small samples, show the observations so the summary can be assessed.

For processed feature statistics, keep raw P and adjusted P distinct. A line at
`-log10(0.05)` represents the P column used on the y axis. It is not an FDR threshold
when that axis uses raw P. Color may encode BH significance on a raw-P axis if the
legend says so; omit or correctly derive any threshold line.
