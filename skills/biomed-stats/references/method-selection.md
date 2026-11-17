# Select the statistical route

Use this selector when the method is undecided. Read the row that matches the
scientific target, then the linked module. Keep the design checks in SKILL.md in
force for every row. If a justified method is already specified, go directly to
its diagnostics and reporting section.

## Resolve design before distribution

A continuous outcome can require a paired comparison, a block model, a hierarchical
model or an independent-group comparison. Identify allocation and dependence first.
A normality test cannot choose among those designs. Preserve a valid existing
analysis when only labels, wording or appearance change.

| Question or situation | Starting route | What decides the choice | Read next |
|---|---|---|---|
| What does the sample look like? | Descriptive summaries and observations | Scale, distribution, independent n; SD/IQR describe spread | [Uncertainty principles](../../biomed-shared/statistical-principles.md#distinguish-spread-precision-and-uncertainty-in-the-contrast) |
| How should the experiment be allocated, and how many units? | Design and prospective precision/power | Target effect, randomization levels, variance, costs, losses | [Design and power](design-and-power.md) |
| Do independent or matched groups differ in mean? | Welch/paired t or design-appropriate linear model | Mean estimand; pairing/blocks; variance and residual/difference behavior | [Routine contrasts](../../biomed-shared/statistical-analysis.md#choose-the-analysis-for-the-estimand) |
| Several factors, nested units, split plots or repeated times? | Factorial, hierarchical or repeated-measures model | Allocation level for each factor, crossing/nesting, covariance, target interaction | [Design and power](design-and-power.md#map-the-hierarchy-to-the-analysis) |
| Is the target a rank/location comparison, or an uncertainty estimate by resampling? | Rank test, bootstrap or randomization method | Estimand, symmetry/common shape when needed, ties, exchangeability | [Ranks and resampling](ranks-and-resampling.md) |
| How does a continuous response vary with covariates? | Regression/correlation | Mean vs quantile, functional form, covariates, influence, dependence | [Regression](regression-and-validation.md) |
| Are large residuals influential, or are both measurements noisy? | Robust fit or measurement-error/symmetric regression | Valid extremes vs error; direction of prediction; evidence about measurement noise | [Regression alternatives](regression-and-validation.md#choose-a-different-regression-target) |
| Are outcomes binary, categorical, counts or rates? | Count/denominator model, contingency test or suitable GLM | Sampling design, denominators/exposure, sparsity, category order | [Binary and diagnostic](binary-and-diagnostic.md) |
| How well does a test detect a condition? | Confusion matrix, ROC/PR, probability assessment | Target prevalence, threshold, errors that matter, reference standard | [Binary and diagnostic](binary-and-diagnostic.md#evaluate-a-diagnostic-test) |
| How well will a model predict new units? | Training/validation/test or nested validation | Intended deployment, independent unit, baseline, metric, leakage | [Prediction and learning](prediction-and-learning.md) |
| What can be learned from prior knowledge and these data? | Bayesian model | Likelihood, defensible prior, target posterior quantity, sensitivity | [Bayesian inference](bayesian-inference.md) |
| What is the effect of an exposure without randomization? | Outcome adjustment, matching, weighting or doubly robust estimation | Target population/estimand, temporal order, confounders, overlap | [Causal observational](causal-observational.md) |
| When does an event occur, with incomplete follow-up? | Censor-aware survival analysis | Time origin, event, censoring/competing events, probability/HR/time ratio | [Survival](survival-and-missing-data.md) |
| Some outcomes or covariates are missing? | Missingness assessment then justified handling | Target quantity, collection process, available information, sensitivity | [Missing data](survival-and-missing-data.md#assess-missingness-for-the-actual-estimand) |
| Are there multivariate patterns or groups? | PCA or clustering | Scaling, distance, features, stability and independent biological support | [Multivariate exploration](multivariate-exploration.md) |
| Are there state transitions or population transmission dynamics? | Markov/HMM or compartment model | Observed vs hidden states, time scale, observation model, process assumptions | [Dynamic models](dynamic-models.md) |

## Add only the needed cross-checks

- Many contrasts or selected features: define the scientific family and read
  [multiplicity and selection](../../biomed-shared/statistical-principles.md#define-the-comparison-family-and-error-criterion).
- Several datasets explored, with only some displayed: use the
  [dataset-family rules](../../biomed-shared/statistical-analysis.md#define-families-across-datasets).
  Scope follows the question and selection process; do not automatically pool all
  explored datasets into one correction family.
- A mean, a future observation and a population reference range need different
  intervals: read [interval choice](regression-and-validation.md#choose-the-interval).
- Prediction with a binary outcome uses both the prediction workflow and diagnostic
  metrics. Bayesian or causal methods still use the relevant outcome and design model.
- Count rates, ordinal/multinomial models, equivalence/noninferiority, advanced
  imputation, longitudinal causal effects and specialized endpoints need additional
  primary method sources. Identify that need when it arises; use the established
  general principles without claiming that the 65 articles teach every implementation.

Finish with a brief reason: “To estimate [quantity] in [population], use [method]
because [design and outcome]. Check [decisive assumption]; report [effect and
uncertainty].” Avoid choosing a method by the P value it produces.

For concrete demonstrations of this reasoning, read the relevant
[worked example](worked-examples.md): paired technical measurements, prospective
sample size or rare-positive classifier evaluation.
