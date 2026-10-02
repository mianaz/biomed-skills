---
name: model-time-to-event-outcomes
description: Analyze survival, failure-time, event-time, or time-to-event outcomes with explicit eligibility, time zero, event and censoring definitions, delayed entry, competing events, recurrent events, covariates, estimands, diagnostics, and sensitivity analyses. Use for Kaplan-Meier or cumulative-incidence summaries, Cox or flexible survival models, restricted mean survival time, hazard or risk contrasts, clinical follow-up cohorts, or censored experimental outcomes. Do not use for single-cell pseudotime, ordinary binary outcomes without follow-up time, or evaluating a frozen prediction model's performance—that belongs to evaluate-biomedical-models.
---

# Model Time-to-Event Outcomes

Make eligibility, time zero, event definition, and follow-up observable before choosing
a survival model. A sophisticated model cannot repair an incoherent risk set.

## Define the event process

1. State the target population, eligibility time, time origin, time scale, event,
   competing events, censoring events, follow-up end, analysis sets, and target estimand.
2. Draw the unit and episode structure. Distinguish one first event, recurrent events,
   multiple event types, transitions, repeated eligibility, and clustered participants.
3. Verify that covariates are available at prediction or risk-set entry. Classify
   baseline, time-varying, post-exposure, and outcome-derived variables.
4. Reconstruct eligible → entered → event/competing event/censored → analyzed counts
   and follow-up by group. Stop for an undefined time zero, impossible chronology,
   outcome-dependent eligibility, or exposure definition that creates immortal time.

Read `references/estimands-and-data.md` before building the analysis dataset.

## Describe before modeling

- Report participants or independent units, events by type, follow-up distribution,
  delayed entry, missing covariates, and number at risk over time.
- Use Kaplan-Meier only for the event-free survival quantity it estimates. Use
  cumulative incidence when competing events alter the probability of the event of
  interest. Do not censor a competing event and call the resulting curve observed risk.
- Show uncertainty and risk tables. Do not report a median when the curve never reaches
  it; use prespecified survival probabilities or restricted mean time when appropriate.

## Choose the model from the estimand

Select Cox, stratified or time-varying Cox, accelerated failure time, flexible
parametric, restricted mean, cause-specific, subdistribution, recurrent-event, frailty,
or multistate methods from the question and event process. Read
`references/models-and-diagnostics.md` before fitting or interpreting hazards.

Preserve clustering, pairing, site, and repeated episodes. Limit model complexity to
the event information; use shrinkage or a simpler prespecified model rather than
unstable variable selection. Define how missing data and informative censoring are
addressed, and keep causal language out of an associational design.

## Diagnose and test sensitivity

Check design rank, positivity/support, proportional or distributional assumptions,
functional form, influential units, residual patterns, sparse risk sets, separation,
competing-event handling, and calibration when absolute risk is reported. Evaluate
reasonable alternative time origins, grace periods, exposure definitions, censoring
assumptions, missing-data methods, and influential sites or units when they threaten
the conclusion.

## Deliver auditable results

Save the cohort-construction flow, event table, analysis dataset or safe linkage,
model formula and contrast, risk/cumulative-incidence data, estimates with denominators
and intervals, diagnostics, sensitivity results, and claim-evidence links. Use the
`clinical-time-to-event` resource profile described in
`references/resource-profile.json` for contract and verification fields.

Route data integrity to `validate-biomedical-data`, provenance to
`ensure-biomedical-reproducibility`, frozen risk-model performance to
`evaluate-biomedical-models`, supplied results to `create-scientific-figures`, and the
complete bundle to `verify-biomedical-analysis`.
