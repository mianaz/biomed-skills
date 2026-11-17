# Binary, categorical and diagnostic outcomes

Use for counts, proportions, categorical responses or diagnostic performance.
For training a new classifier, also read [prediction and learning](prediction-and-learning.md).

## Match the denominator and model

| Data and target | Candidate | Check before use |
|---|---|---|
| One categorical sample against specified probabilities | Goodness-of-fit test | Expected counts, parameters estimated from data, category definitions |
| Association in independent contingency counts | Pearson chi-squared or appropriate exact/Monte Carlo test | Expected cell counts and approximation; sampling and conditioning assumptions |
| Binary response with covariates | Binomial/logistic model | Independent or clustered trials, link shape, separation, sparse events |
| Ordered or multiple unordered categories | Ordinal or multinomial model | Whether order is meaningful; verify the selected model's assumptions |
| Number of events per time/exposure | Count/rate model | Exposure denominator, overdispersion, clustering and possible structural zeros |

Use actual counts and denominators. Percentages alone do not supply sample size.
Paired binary outcomes need a paired analysis; a simple independence table discards
that structure. Multiple observations within a subject need a corresponding model.
Choose an exact or simulation method from the sampling scheme and question, without
a universal cell-count cutoff.

In logistic regression, logit(p) is log[p/(1-p)]. The quantity p/(1-p) is **odds**;
exp(beta) is the conditional odds ratio for the stated predictor change. Give
reference levels, units and confidence intervals. For absolute-risk questions,
report estimated probabilities or standardized risk contrasts with uncertainty.
An odds ratio is not a risk ratio. Inspect separation, convergence and coefficient
instability; obtain primary documentation for penalized or exact alternatives
when needed. A binary endpoint at a common observed time differs from a censored
time-to-event endpoint.

## Evaluate a diagnostic test

Define the intended population, reference standard, positive class, sampling scheme
and threshold. Record TP, FP, FN and TN at that threshold, plus sensitivity,
specificity, PPV/NPV and intervals relevant to the intended use. Assess calibration
when reporting individual probabilities, alongside discrimination.

For prevalence pi, sensitivity Se and specificity Sp,
PPV = Se*pi / [Se*pi + (1-Sp)*(1-pi)]. Case-control or enriched test samples require
care when transporting PPV/NPV to a different population. ROC and PR curves compare
thresholds; PR has a no-skill baseline tied to prevalence. If curves cross, examine
the operating region and costs that matter. State the PR/AUC integration convention
and give uncertainty, especially when there are few true positives.

Select a threshold using training/validation data and the intended consequences,
then evaluate it on held-out data. Comparing only AUC can hide poor calibration or
unacceptable errors at the required threshold. Compare a meaningful baseline and
report the same metrics for it; a high majority-class accuracy can coexist with
zero sensitivity.

For sequential/compound tests, product rules require conditional independence given
truth. Shared assays or inputs can violate it. Evaluate the whole testing pathway,
including missed cases at the first screen. For pooled assays, validate dilution
and detection effects. Estimating population prevalence additionally requires a
representative sampling design and propagation of test-accuracy uncertainty.

Deliver the model/effect or diagnostic performance table, denominators, uncertainty,
threshold rationale and applicable population. Refer to primary method and software
documentation for ordinal, rate, sparse-data or complex sampling implementations.

## Sources

- *Tabular data*, pp. 329–330 and its correction: [nmeth.4239](https://doi.org/10.1038/nmeth.4239).
- *Logistic regression*, pp. 541–542: [nmeth.3904](https://doi.org/10.1038/nmeth.3904).
- *Classification evaluation*, pp. 603–604 and corrected F-beta formula: [nmeth.3945](https://doi.org/10.1038/nmeth.3945).
- *Testing for rare conditions*, pp. 224–225: [s41592-021-01089-4](https://doi.org/10.1038/s41592-021-01089-4).
- *Graphical assessment of tests and classifiers*, pp. 840–842: [s41592-021-01232-1](https://doi.org/10.1038/s41592-021-01232-1).
- *Comparing classifier performance with baselines*, pp. 546–548: [s41592-024-02234-5](https://doi.org/10.1038/s41592-024-02234-5).

Paired/clustered analysis, calibration and leakage checks above are suite
implementation requirements; the columns provide the main conceptual framework.
