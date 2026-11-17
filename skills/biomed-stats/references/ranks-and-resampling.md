# Ranks and resampling

Use when choosing a rank test or estimating uncertainty by resampling. Apply the
shared [analysis decisions](../../biomed-shared/statistical-analysis.md).

## Choose the quantity before the test

Specify whether the question concerns a mean difference, location shift, median,
ordered response or another statistic. Explain a change in that target when
replacing a mean-based analysis with a rank method.

The Wilcoxon rank-sum test compares independent samples through their pooled
ranks. A median/location-shift interpretation requires suitable common-shape
assumptions; otherwise distributional differences can affect the result. Paired
signed-rank analysis uses within-unit differences and requires a suitable symmetry
assumption. The sign test uses only the direction of those differences. Keep
the pairing and record ties, zero differences and the exact/asymptotic method.

Inspect small-sample resolution. For example, with independent, continuous data
and group sizes 4 and 3, the smallest two-sided exact rank-sum P is 2/35. Use the
actual method and tie handling to assess resolution in the current design. Apply
the selected multiplicity procedure to the full family; the article's simple
N-times-P examples do not describe every FDR-adjusted result.

## Bootstrap the estimation process

State the statistic, sampling unit and resampling scheme. A parametric bootstrap
simulates from a fitted generating model; a nonparametric bootstrap samples the
observed units with replacement. The former depends on that model's adequacy;
the latter has limited information about unobserved tails, especially at small n.
Assess whether the original sample can support the target uncertainty estimate.

Implementation rules extending the source's independent-sample illustration:

- Resample independent units. Carry paired observations together and use an
  appropriate cluster, block or model-based scheme for dependent data.
- Repeat data-dependent estimation steps inside the resample when the target is
  uncertainty in the full procedure. State when a result is conditional on a fixed
  model, transformation or selection.
- Record the seed, repetitions, failures and interval construction. Check whether
  Monte Carlo variability matters at the reported precision.
- Distinguish the bootstrap SE from a confidence interval. More resamples improve
  simulation precision; independent n remains the original number of units.

For permutation/randomization inference, specify the null and permissible
reassignments from the design. Bootstrap sampling and label permutation have
different purposes and require different justifications.

## Sources and scope

- Krzywinski & Altman, *Nonparametric tests*, pp. 467–468, Figs. 1–3;
  the supplied PDF includes the corrected sample subscript and May 2014 corrigendum.
  [DOI](https://doi.org/10.1038/nmeth.2937).
- Kulesa et al., *Sampling distributions and the bootstrap*, pp. 477–478, Fig. 3.
  [DOI](https://doi.org/10.1038/nmeth.3414).
- [R wilcox.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/wilcox.test.html)
  supplies the implementation definitions, including symmetry and location
  interpretation. Check the installed version for ties and exact inference.

The cluster, pipeline and permutation checks above are suite implementation
rules. Use primary method documentation for the particular dependent-data scheme.
