# Regression, influence and intervals

Use for association, a continuous response, influential observations or uncertainty
about fitted relationships. For performance on new data, also read
[prediction and learning](prediction-and-learning.md).

## Define the relationship and effect

Plot the observed relationship at the independent unit. Pearson correlation
describes a linear relationship; Spearman correlation describes monotone rank
association. Curvature, subgroup structure, restricted range and influential
observations can change their interpretation. Report the coefficient, interval,
independent n and the tested family when many associations were searched.

For regression, state outcome scale, predictor units, reference categories and
covariates. A coefficient describes change conditional on the other modeled
predictors. Explain the biological reason for adjustment; retain the distinction
between an adjusted association and a causal effect identified by the design.
Correlated predictors can change coefficient signs, magnitudes and uncertainty
when the fitted covariate set changes. Choose covariates from the question and
design, and document selection made after inspecting outcomes.

Distinguish uncertainty in a conditional mean from a prediction interval for a
new observation. Also state whether a confidence band is pointwise or simultaneous.
Report the supported predictor range and identify extrapolated predictions.

## Diagnose the model used for inference

| Check | Inspect | Consequence to assess |
|---|---|---|
| Functional form | Residuals versus fitted values and predictors | Curvature or an omitted interaction |
| Variance | Residual spread across predictions/groups | Validity of standard errors and intervals |
| Dependence | Design IDs; residuals over time, position or clusters | Need for a dependence-aware model or variance estimate |
| Error distribution | Residual Q–Q plot, tail behavior, sample size | Approximation for coefficient inference and prediction coverage |
| Influence | Leverage, residuals and Cook's distance together | Dependence of the fit and conclusion on a few units |
| Collinearity | Predictor relationships and coefficient uncertainty | Stability and identifiability of individual effects |

Use diagnostic values as prompts for investigation. Cutoffs illustrated in the
articles, such as a Cook's-distance or VIF threshold, are not automatic deletion
or pass/fail rules. A nonsignificant normality test does not establish model validity.
Stable fitted values alone do not validate their intervals or individual effects.

Investigate unusual values in the experimental records. Correct verified errors
with a traceable reason. Retain plausible biological extremes in the primary
analysis when eligible under the study rules; evaluate consequential influence
with a justified alternative and report the change in effect and uncertainty.
Distinguish prespecified exclusions from choices made after seeing outcomes.

## Choose a different regression target

| Need | Candidate | Decisive checks |
|---|---|---|
| Conditional mean with consequential outliers | Robust M/MM regression as a justified primary or sensitivity model | Data validity, biological subgroups, leverage, tuning and uncertainty method |
| Conditional median or another quantile | Quantile regression | Scientific quantile, functional form, tail support, intervals and quantile crossing |
| Relation to a predictor measured with error | Measurement-error model | Error mechanism and information from repeats, calibration or validation data |
| Symmetric relation between two noisy measurements | Deming or a justified symmetric fit | Prediction direction, units and evidence about error variances |

A robust method changes how observations influence the fit. Investigate masking,
swamping and valid biological extremes; choose the estimator for the question and
credible contamination model. A different answer from OLS is information to explain,
not an automatic instruction to remove observations.

Quantile regression estimates conditional quantiles. Heterogeneous residual variance
can motivate examining distributional changes, but it does not by itself invalidate
a correctly specified conditional-mean target. Tail estimates need sufficient data
and a suitable uncertainty method.

Classical independent, zero-mean predictor error attenuates a slope in the simple
single-predictor setting. Other error structures and multivariable models can behave
differently. Distinguish predicting from a noisy observed measurement from estimating
a relationship with the underlying quantity. Estimate error properties from relevant
information and carry their uncertainty into any correction.

Use directional regression for prediction of Y from X. For a reversible relation,
choose a symmetric model from the measurement process. Deming needs the measurement
error variance ratio in the software's stated orientation; observed total variances
are not a substitute. Orthogonal fits depend on the measurement units, and geometric
mean regression can have a slope magnitude that conceals weak association. Report
uncertainty and agreement/bias measures if comparing measurement methods.

## Choose the interval

| Target | Interval | State |
|---|---|---|
| Parameter or conditional mean | Confidence interval/band | Level, method and pointwise versus simultaneous coverage |
| New individual observation | Prediction interval | New observation's population, model and level |
| Specified fraction of a population | Tolerance interval | Coverage fraction and confidence level, plus distribution assumptions |

Individual variation remains in prediction and tolerance intervals even when a
mean is estimated precisely. Large-sample normality of a mean does not establish
normal individual tails. Verify the interval's model, dependence and software
convention, especially for reference ranges. State the supported predictor range
and identify extrapolation. Ordinary intervals after outcome-driven variable
selection need selection-aware justification; see [prediction](prediction-and-learning.md).

Deliver the fitted relationship, units/covariates, effect and appropriate interval,
diagnostic evidence and any consequential sensitivity comparison.

## Sources and scope

- *Association, correlation and causation*, pp. 899–900, Figs. 1–3:
  [DOI](https://doi.org/10.1038/nmeth.3587).
- *Simple linear regression*, pp. 999–1000, Figs. 1–3:
  [DOI](https://doi.org/10.1038/nmeth.3627).
- *Multiple linear regression*, pp. 1103–1104, Table 1 and Fig. 2:
  [DOI](https://doi.org/10.1038/nmeth.3665).
- *Analyzing outliers: influential or nuisance?*, pp. 281–282, Figs. 1–3;
  supplied PDF includes the April 2016 corrigendum correcting MSE and swapped means:
  [DOI](https://doi.org/10.1038/nmeth.3812).
- *Regression diagnostics*, pp. 385–386, Figs. 1–2:
  [DOI](https://doi.org/10.1038/nmeth.3854).
- *Model selection and overfitting*, pp. 703–704, Figs. 1–3:
  [DOI](https://doi.org/10.1038/nmeth.3968).
- *P values and the search for significance*, pp. 3–4, Figs. 1–3:
  [DOI](https://doi.org/10.1038/nmeth.4120).

Use established model implementations and verify their definitions. Do not
transcribe article equations or illustrative numerical cutoffs into analysis code
without checking them. Specialized implementations need their own primary method and software references.

- *Analyzing outliers: Robust methods to the rescue*, pp. 275–276: [s41592-019-0369-z](https://doi.org/10.1038/s41592-019-0369-z).
- *Quantile regression*, pp. 451–452: [s41592-019-0406-y](https://doi.org/10.1038/s41592-019-0406-y).
- *Predicting with confidence and tolerance*, pp. 843–845: [s41592-018-0196-7](https://doi.org/10.1038/s41592-018-0196-7).
- *Errors in predictor variables*, pp. 4–6: [s41592-023-02119-z](https://doi.org/10.1038/s41592-023-02119-z).
- *Symmetric alternatives to the ordinary least squares regression*, pp. 1610–1612: [s41592-025-02760-w](https://doi.org/10.1038/s41592-025-02760-w).
