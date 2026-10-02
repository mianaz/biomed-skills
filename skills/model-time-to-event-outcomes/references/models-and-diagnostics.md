# Survival models and diagnostics

## Choose from the question

| Question or structure | Candidate approach | Main caution |
|---|---|---|
| Event-free survival by group | Kaplan-Meier, log-rank as descriptive comparison | Competing events change interpretation |
| Absolute event probability with competing events | Aalen-Johansen/cumulative incidence | Do not use 1-KM for cause-specific risk |
| Covariate association with hazard | Cox or flexible parametric model | Check proportionality and functional form |
| Difference in average event-free time through horizon | Restricted mean survival time | Horizon must be supported and prespecified |
| Acceleration/deceleration of survival time | Accelerated failure-time model | Distributional assumptions matter |
| Etiologic association for one cause | Cause-specific hazard model | Does not directly estimate cumulative incidence |
| Effect on observed cumulative incidence | Subdistribution or direct risk model | Risk-set interpretation differs from cause-specific hazard |
| Recurrent events or transitions | Gap/total-time recurrent, frailty, multistate model | Define risk intervals, terminal events, and dependence |

Do not select a model solely because one global test is significant.

## Diagnostics

- verify design rank, event counts, overlap/positivity, sparse categories, and separation;
- inspect proportional hazards globally and for consequential covariates using plots
  and time interaction, not only one p-value;
- assess nonlinear continuous effects with prespecified transforms or flexible terms;
- inspect residuals, influence, leverage, and site/cluster contribution;
- check baseline/cumulative hazard and absolute-risk calibration when predictions are reported;
- evaluate whether censoring depends on measured risk, group, site, or calendar time;
- show risk-set support at every reported horizon.

If proportional hazards fails, use time-varying effects, stratification, a flexible
model, or a non-hazard estimand rather than averaging a misleading hazard ratio.

## Multiplicity and sensitivity

Declare the family across outcomes, event types, time horizons, subgroups, exposures,
and models. Prespecify the primary estimand. Label data-driven cut points and subgroup
searches exploratory.

Test the assumptions most capable of changing the conclusion: time origin or grace
period, exposure definition, delayed entry, competing-event strategy, missing-data
method, censoring weights, functional form, influential units/sites, and unmeasured
confounding where a causal interpretation is considered.
