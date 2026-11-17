# Source qualifications and corrections

Read when implementing an equation, numerical example or categorical recommendation
from a column. The 65 main articles and captions were read; selected figures were
also inspected. The source catalogue records the scope. A conceptual synthesis can
use an article while qualifying an example or interpretation.

## Publisher corrections checked

| Article | Correction and local status |
|---|---|
| [Power and sample size](https://doi.org/10.1038/nmeth.2738) | Supplied PDF includes the 26 November 2013 and 3 August 2015 errata |
| [Nonparametric tests](https://doi.org/10.1038/nmeth.2937) | Supplied PDF includes the 23 May 2014 correction to the X sample-size subscript |
| [Bayesian statistics](https://doi.org/10.1038/nmeth.3368) | Supplied PDF includes the 24 September 2015 likelihood-curve correction |
| [Analyzing outliers: influential or nuisance?](https://doi.org/10.1038/nmeth.3812) | Supplied PDF includes the 14 April 2016 corrections to MSE and swapped means |
| [Classification evaluation](https://doi.org/10.1038/nmeth.3945) | Supplied PDF includes the 16 September 2016 F-beta correction |
| [Classification and regression trees](https://doi.org/10.1038/nmeth.4370) | Supplied PDF includes the 28 July 2017 correction to Fig. 1 subset-purity labels |
| [Tabular data](https://doi.org/10.1038/nmeth.4239) | Supplied PDF includes the correction for aa: z = −2.167, P = 0.03 |
| [Two-level factorial experiments](https://doi.org/10.1038/s41592-019-0335-9) | The local corrected Table 1 has −0.09. The [2019 correction](https://doi.org/10.1038/s41592-019-0405-z) was read through the publisher search index |
| [Nested designs](https://doi.org/10.1038/nmeth.3137) | Original PDF retains errors. [2020 correction](https://doi.org/10.1038/s41592-020-0969-7) read through the publisher PDF search index: 5 technical replicates becomes 3; cost is b*C_B + b*c*C_C + b*c*n*C_N; reference is Fig. 3b |

This records corrections encountered and checked. It is not an exhaustive search
for every amendment or supplement. Separate correction PDFs for the last two rows
are not required to establish main-article completeness and were not archived locally.

## Interpretation and implementation decisions

These are suite qualifications, not publisher-issued corrections unless listed above.

| Source/example | Decision used in the suite |
|---|---|
| *Designing comparative experiments*: observed-effect power | Use prospective scenarios for planning and effect/intervals for completed studies. The decision also uses Hoenig & Heisey (2001), sections 2.1 and 3: [DOI](https://doi.org/10.1198/000313001300339897) |
| *Visualizing samples with box plots*: categorical plot and sample-size advice | Match display to the data and question; preserve the user's justified bar + error + sample-point display. Define quartiles, whiskers and n for box plots |
| *Simple linear regression*, p. 999 | The printed r*sX/sY is inverted for OLS of Y on X; the slope is r*sY/sX. Use established implementations |
| *Bayesian statistics*, pp. 377–378 | Specify credible-interval type; Bayes factor is posterior odds divided by prior odds. A continuous interval containing zero is not a model comparison with a point null |
| *Logistic regression*, pp. 541–542 | p/(1−p) is odds; exp(beta) is the conditional odds ratio for the stated predictor change |
| *Propensity score weighting*, p. 639 | The PS-to-ATE shorthand describes a conversion of weights, not multiplication of treatment effects |
| *Double robustness*, Fig. 3, p. 870 | Visually checked: untreated residual is printed over PS. With PS = Pr(treated), its denominator must be 1−PS. Use the ATE expression in the causal module and a verified implementation |
| *Symmetric alternatives…*, Fig. 2 | Inverse slope follows 1/d; do not reuse the inconsistent sign in the caption. Deming's ratio refers to measurement-error variances |
| *Clustering*, pp. 545–546 | Standard k-means uses squared Euclidean distance. RMS and 1−r are not interchangeable without an explicit normalization and transformation |
| *Classification and regression trees*, p. 757 | Use parent impurity minus weighted child impurity. Do not reuse the sign error in the worked information-gain expression |
| *Neural networks primer* | A quadratic interaction can express XOR; compare appropriate simple baselines. Use a signed log-ratio label when the data are signed, rather than negative fold change |
| *Convolutional neural networks* | A fixed dense network generally changes output when inputs are permuted. Input length requirements depend on architecture |
| *Hidden Markov models* | Forward likelihood, marginal posterior states and the most probable joint path are different outputs. The last uses Viterbi decoding |
| Survival columns | Use a rate interpretation for hazard and retain censoring. Curve tests are not general tests of the median; HR and time ratio need their own model-specific interpretation |
| *Consequences of missing data* | Introductory consequences are covered; detailed imputation requires additional sources |

Use examples of sample size, split proportions, class-imbalance ratios, diagnostic
cutoffs and tuning parameters as illustrations. Set them for the actual estimand,
design and loss/precision target. Robust, Bayesian, causal and resampling methods
each retain assumptions that must match the intended use.

Implementation cross-checks read include the official R `wilcox.test`,
`survival::survdiff`, `survival::cox.zph` and competing-risks documentation; the
[AIPW documentation](https://yqzhong7.github.io/AIPW/); and the
[hmmlearn API](https://hmmlearn.readthedocs.io/en/stable/api.html). Exact access scopes
are retained in the local review record. Check current primary documentation when
executing a specialized method; no article workbook was executed in this review.
