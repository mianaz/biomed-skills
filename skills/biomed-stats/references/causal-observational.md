# Causal analysis of observational data

Use when the question asks for an exposure or treatment effect without randomized
allocation. Start with the treatment strategies, population, time zero, outcome
and follow-up. Define the target effect, such as ATE in the eligible population or
ATT among the treated, before selecting an adjustment method.

## Establish identification before fitting

Map temporal order and the scientific relationships among exposure, outcome and
covariates. Identify pre-exposure confounders and distinguish them from mediators,
colliders and consequences of treatment. State the assumptions needed for the
target effect: consistency, exchangeability given measured covariates, positivity
and the relevant interference assumptions. Inspect how measurement and selection
could compromise these assumptions. Covariate balance can assess measured inputs;
the scientific case for sufficient confounder measurement remains essential.

| Approach | When useful | Decisions and checks |
|---|---|---|
| Outcome regression/standardization | A credible outcome model can estimate the desired marginal contrast | Functional form, interactions, target population and extrapolation |
| Matching | Comparable exposed and unexposed units can be retained | Distance/PS model, caliper scale, replacement, ratio, balance and retained target |
| Propensity-score weighting | The target population can be represented with supported weights | Estimand-specific weights, overlap, balance, extreme weights and precision |
| Doubly robust estimation | Combine exposure and outcome models for the same target | Both models, overlap, valid inference and sample splitting when appropriate |

Select confounders from the scientific structure and available information. A
propensity score is a treatment probability, not a prediction contest: assess
balance of the covariates themselves and their important nonlinear/interaction
terms. A good treatment-classification score does not establish confounding control.

## Match or weight to the target

For binary treatment A, let e(X) = Pr(A=1 | X). Unstabilized ATE weights are 1/e(X)
for treated units and 1/[1-e(X)] for controls. ATT weights are 1 for treated units
and e(X)/[1-e(X)] for controls. State normalization/stabilization and the exact
estimator. The article's shorthand about multiplying by PS concerns weights.

Inspect overlap, covariate balance, the weight distribution and effective sample
size by group. Predefine feasible responses to poor support in relation to the
estimand. Capping weights, dropping unsupported units and changing the target
population have different consequences; record the resulting target and sensitivity.
Stabilization alone does not restore missing support. For matching, report retained
and unmatched units and use inference appropriate to the matched/weighted design.

## Combine models with the correct augmentation

For the standard ATE AIPW estimator, with m_a(X) estimating E(Y | A=a, X), average
the following over the target sample:

$$
m_1(X_i)-m_0(X_i)
+\frac{A_i\{Y_i-m_1(X_i)\}}{e(X_i)}
-\frac{(1-A_i)\{Y_i-m_0(X_i)\}}{1-e(X_i)}.
$$

Use an established implementation with appropriate uncertainty. If flexible
learning estimates the nuisance models, verify the cross-fitting and regularity
requirements for the selected estimator. Doubly robust consistency requires the
identification conditions and at least one correctly specified nuisance model,
with the applicable estimation conditions. It does not remove sensitivity to
unmeasured confounding or extreme propensity scores.

The untreated residual in the 2026 column's Fig. 3 is printed with PS in the
denominator. With PS defined there as treatment probability, use **1-PS** for that
residual. This is an implementation qualification from equation and figure review,
not a publisher-issued correction. See [source qualifications](source-qualifications.md).

Deliver the causal question, target population, assumptions, covariates, overlap
and balance checks, exclusions/weights, effect and interval, and a sensitivity
analysis suited to the main threats. Time-varying exposure, competing events,
instrumental variables and other specialized designs need their own primary methods.

## Sources

- *Propensity score matching*, pp. 1770–1772: [s41592-024-02405-4](https://doi.org/10.1038/s41592-024-02405-4).
- *Propensity score weighting*, pp. 638–640: [s41592-025-02629-y](https://doi.org/10.1038/s41592-025-02629-y).
- *Double robustness*, pp. 868–870: [s41592-026-03099-6](https://doi.org/10.1038/s41592-026-03099-6).
- Additional implementation cross-check: [AIPW package documentation](https://yqzhong7.github.io/AIPW/),
  estimator scope, causal assumptions and cross-fitting. Check the chosen version's
  estimator and defaults; do not inherit its propensity truncation bound silently.
- Additional conceptual check: Funk et al. (2011),
  [Doubly Robust Estimation of Causal Effects](https://pmc.ncbi.nlm.nih.gov/articles/PMC3070495/),
  abstract and assumptions section accessed through the search index; not a full-paper read.
