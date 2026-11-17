# Statistical principles

Use when designing an experiment or interpreting statistical evidence. These
principles synthesize 65 Points of Significance main texts and captions. Source
numbers refer to the optional [catalogue](statistical-sources.md). Read the sections
relevant to the question.
When executing or checking an analysis, read the relevant section of
[statistical analysis](statistical-analysis.md).

## Start with the biological question and target effect

Name the population, outcome, comparison and effect to estimate, including its
scale and time point. Define a biologically meaningful difference before planning
sample size. Interpret magnitude and uncertainty in that biological context. [1, 5, 6]

## Count replication at the level of inference

Identify treatment allocation, biological sampling and repeated measurement
separately. Record the hierarchy and the number of units at each level. Biological
and technical replicate labels depend on the question; they do not establish
statistical independence. Additional readings of the same material improve
measurement precision, while independent biological sampling supports population
inference. Allocate effort using the relevant variance components and costs. Model
which levels are nested and which are crossed; use the error structure and degrees
of freedom appropriate to the effect being tested. [7, 9, 12]

## Design for precision and generalization

Control technical variation; sample the biological variation needed for the target
population. Use random allocation to reduce systematic treatment differences, and
blocks or matching to account for known nuisance variation. Carry that structure
into the analysis. Compare the variance reduction from blocking with its cost and
degrees of freedom; its power benefit depends on the design. State the population
represented by the sampled conditions. Treatment-by-background variation can justify
deliberate heterogeneity in the design. [6, 9, 11, 31]

## Plan power for the intended analysis

Power is the probability of detecting a specified alternative under the assumed
design and model. Specify the meaningful effect, variability, significance level,
sidedness, target power and independent sample size. Include the comparison family
and dependence structure when they affect the calculation. Show how plausible
effect and variance assumptions change the required resources. [5, 6, 7]

## Preserve matching and compare effects directly

For paired observations, estimate within-unit differences and their uncertainty.
For independent groups, account for uncertainty in both groups. A claim that
treatments differ requires their direct contrast. For a factorial question,
estimate the interaction: how one factor's effect changes with the other factor.
Report the scale and simple effects needed to explain that interaction. An omnibus
ANOVA tests whether all relevant means are equal; specify contrasts to identify
the differences that answer the biological question. [2, 6, 8, 11]

## Distinguish spread, precision and uncertainty in the contrast

SD describes observed spread; SEM describes precision of a mean. Label error bars
and state the confidence level and method for intervals. A confidence procedure's
coverage concerns repeated samples under its assumptions. Estimate the contrast's
own uncertainty; error-bar overlap between group summaries is not a general test.
For paired data, retain individual changes or the paired effect and its interval.
Choose a confidence interval for a parameter, a prediction interval for a new
observation, or a tolerance interval for a population fraction at a stated confidence.
Individual variation remains even with a precisely estimated mean. [1, 2, 6, 10, 34]

## Explain effect size and statistical evidence together

Report direction, magnitude and uncertainty, followed by biological meaning. A
P value describes how unusual the observed or more extreme test statistic would
be under the specified null model and its assumptions. It does not give the
probability that the hypothesis is true. Assess a nonsignificant result through
the effect sizes compatible with its interval and the study's sensitivity. [4, 5, 6]

## Define the comparison family and error criterion

State the family and its scientific purpose. Family-wise error control addresses
the probability of any false rejection in that family; FDR control addresses the
expected fraction of false rejections among discoveries, with zero when there are
no discoveries. Apply the chosen method to the complete intended family under its
assumptions. Keep raw and adjusted P values and name the adjustment method. [3]

Define that scope from the scientific claim and selection process. Exploring several
datasets in one project does not automatically make all their tests one family.
Separately specified dataset analyses can retain dataset-specific families. A family
can span figures, and one figure can contain several distinct families. Preserve
outcome-driven selection when deciding how to interpret the displayed results. [3, 21]

## Preserve how the analysis was selected

Record planned comparisons and decisions made after seeing data. Retain exploratory
findings with their biological rationale and actual selection history. Account for
selection in formal inference: selecting the most compelling interval produces
the same selection problem as choosing the smallest P value. Evaluate scientific
contribution using the design, effect, uncertainty and biological evidence. [4, 21]

## Match the estimator and resampling to the question

Mean, median and rank-based comparisons answer different questions. Interpreting
a rank-sum test as a location or median comparison requires suitable distribution
assumptions. Small samples can permit only a coarse set of exact P values. Bootstrap
uncertainty depends on the observed sample and any assumed generating model;
resampling many times does not enlarge the original independent sample. [13, 14]

## Diagnose models before interpreting their coefficients

Inspect the relationship visually and assess residual trends, variance, dependence
and influential observations. Interpret a coefficient with its covariates, units
and scale stated. Correlated predictors can make individual coefficients unstable
even when predictions appear stable. Investigate unusual observations using their
experimental records and biological context; report consequential sensitivity. [15–19]

## Evaluate prediction using data outside model selection

Separate model fitting, selection and performance evaluation. Use an untouched
test set or an appropriate nested validation design. Small samples make performance
estimates variable; report that uncertainty. Keep prediction accuracy and the
interpretation of individual biological effects as distinct targets. [17, 20, 21]

## Define event time and account for censoring

Specify the event, time origin, follow-up and censoring. Retain the partial
follow-up information from censored subjects. Choose survival probabilities,
time ratios or hazard ratios to match the question, and state the model assumptions
needed for their interpretation. Estimate uncertainty on that chosen scale. [22, 23]

## Assess missingness for each target quantity

Record what is missing, what remains observed and the plausible reason. Missing
data reduce information and can change which population is represented. Bias
depends on the estimand and model: a correctly specified conditional regression
can remain unbiased under covariate-dependent selection while a marginal mean
changes. Response-dependent selection can bias that regression too. Imputation
requires assumptions and propagation of its uncertainty. [24]

## Respect denominators and decision thresholds

Retain counts, denominators and the sampling scheme. For diagnostic decisions,
define the reference standard, positive class and error costs. Sensitivity,
specificity, predictive values, calibration and discrimination describe different
properties; prevalence changes the interpretation of a positive result. Evaluate
the selected operating threshold and compare a meaningful baseline. [27, 43, 44, 45, 48]

## Make prior information explicit

State the likelihood, prior and posterior quantity. Check predictive behavior and
sensitivity to consequential prior choices. Define the credible-interval type and
condition any probability statement on the model used. Multiple pieces of evidence
need a joint likelihood that represents their dependence. [37, 38, 39]

## Identify the causal target before adjustment

Specify the intervention/exposure, population, time and target effect. Choose
adjustment from temporal and scientific relationships. Matching, weighting and
outcome models require sufficient confounder information and support for the
comparison. Inspect balance and overlap, retain the resulting target population,
and propagate estimation uncertainty. [40, 41, 42]

## Connect multivariate patterns to independent evidence

PCA and clustering depend on transformations, features, distances and algorithm
choices. Inspect loadings and stability, relate patterns to the study design, and
use additional biological evidence for interpretation. When evaluating prediction,
learn transformations only from the training portion. [50, 51, 57]

## Define states and the observation process

For dynamic models, define states, time scale, transitions and how observations
arise. Separate sequence likelihood, state probabilities and decoded paths. For
population models, state rate assumptions and whether outputs are chosen scenarios
or fitted forecasts. Assess uncertainty for the intended decision and horizon. [60, 61, 62, 63, 64, 65]

The columns give conceptual foundations. Examples do not set universal thresholds,
split sizes or sample sizes. Use prospective assumptions for planning, preserve
selection history, and check primary implementation documentation for the method
being executed. The source catalogue records coverage and further sources.
