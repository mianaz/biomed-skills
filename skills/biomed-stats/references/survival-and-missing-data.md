# Survival and missing data

Use when outcomes are partly observed through censoring or missingness. Apply the
shared [analysis decisions](../../biomed-shared/statistical-analysis.md).

## Define the event and observation process

Record the event definition, time origin, time unit, entry time, last follow-up,
event/censor indicator and reason. Distinguish right, left and interval censoring
and delayed entry; choose software that represents the actual observation scheme.
Check whether censoring can reasonably be treated as independent of event time
under the analysis assumptions, including relevant conditioning variables.

Retain censored subjects' known follow-up. Counting a censoring time as an event
or discarding censored subjects loses that information and can bias estimates.
Distinguish loss to follow-up from an event that prevents the outcome of interest,
such as death before recurrence. For cumulative incidence with competing events,
use a method for that target; 1 minus a KM curve that censors competing events
does not estimate the observed probability of the specific event.

## Choose an interpretable survival target

| Target | Analysis and reporting |
|---|---|
| Survival probability at a specified time | Censor-aware survival curve, estimate and CI, with numbers at risk |
| Median survival | Report the estimate and CI only when estimable within supported follow-up; otherwise report that it was not reached |
| Difference between survival curves | Justified log-rank/weighted test or model; state the comparison and weighting |
| Covariate-adjusted hazard ratio | Cox model with covariate units, reference values, CI and proportional-hazards assessment |
| Multiplicative effect on survival time | AFT model with time ratio, CI and stated distribution/estimation assumptions |

Curve-comparison tests address survival distributions. Do not relabel their
P values as tests specifically of median survival. A Cox hazard ratio compares
instantaneous event rates among those still at risk. It is not a risk ratio or
the reciprocal of a time ratio; translating to survival time or absolute risk
requires the fitted survival model and a stated time/covariate setting.

Assess the proportional-hazards assumption with relevant plots and diagnostics,
including scaled Schoenfeld residuals when appropriate. If the effect varies over
time, use a justified time-varying or alternative model and report the effect on
the chosen scale. Fit AFT models with a censor-aware procedure; ordinary regression
of observed log follow-up treating censoring as failure is unsuitable.

Retain event counts, censor counts, numbers at risk, the fitted object and the
analysis denominator. Preserve continuous predictors unless a justified threshold
was specified; record any outcome-driven threshold search and its validation.

## Assess missingness for the actual estimand

Tabulate missing data by variable, group and time. Identify wholly absent units
and partial records, reasons for loss, and information still available about
those units. State the observed-data assumptions used by the analysis.

The missing-data article illustrates three different consequences:

1. Random loss reduces precision, with greater uncertainty where observations
   were already sparse.
2. Selection based only on a modeled covariate can preserve a correctly specified
   conditional regression while biasing marginal population means.
3. Selection related to the response, even after conditioning on covariates, can
   bias that regression as well.

These are conditional examples, not proof of a mechanism in a new dataset. Use
the collection process and available variables to justify handling. Assess plausible
departures when they could alter the scientific conclusion.

The source introduces possible imputation benefits and false precision; it does
not provide a complete imputation protocol. Before implementing one, consult the
method's primary documentation for the target estimand, observed-data assumptions,
model compatibility and uncertainty combination. Save the assumptions and outputs.
Avoid deterministic filling that treats estimated values as fully observed data.

## Sources and implementation qualifications

- Dey et al. (2022), *Survival analysis—time-to-event data and censoring*,
  pp. 906–908, Figs. 2–3: [DOI](https://doi.org/10.1038/s41592-022-01563-7).
- Dey et al. (2022), *Regression modeling of time-to-event data with censoring*,
  pp. 1513–1515, Figs. 1–2: [DOI](https://doi.org/10.1038/s41592-022-01689-8).
- Dey et al. (2026), *Consequences of missing data*, pp. 1661–1663, Fig. 2:
  [DOI](https://doi.org/10.1038/s41592-026-03203-w).

Additional implementation sources, outside the series:
[survival: competing risks](https://stat.ethz.ch/R-manual/R-devel/library/survival/doc/compete.pdf),
[survdiff](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/survdiff.html),
[cox.zph](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/cox.zph.html).
These support the competing-event distinction, curve-test target and PH checks.
Use the conditional assumptions above when applying the articles' simplified
censoring examples and descriptions of hazard. Obtain further primary sources
for advanced censoring, causal effects, imputation or specialized endpoints.
