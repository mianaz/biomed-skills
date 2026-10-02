# Time-to-event estimands and analysis data

## Define the time axis

Record eligibility, cohort entry, treatment/exposure assignment, time zero, delayed
entry, event ascertainment, competing events, censoring, and administrative end. These
may be different dates. Explain the time scale: time since entry, age, calendar time,
or another scientifically justified scale.

Avoid:

- assigning exposure using information accumulated after time zero;
- requiring future survival to enter an exposed group;
- excluding early events only from one group;
- resetting time zero differently by outcome or group;
- treating loss to follow-up as an event or a benign administrative censor without evidence.

## Name the estimand

Examples include survival probability at a fixed time, cumulative incidence of one
event type, restricted mean event-free time through a horizon, cause-specific hazard
ratio, subdistribution hazard ratio, recurrence rate, transition probability, or a
standardized risk contrast. State population, strategy/exposure, comparator, event,
competing-event strategy, horizon, and summary measure.

Hazard ratios are instantaneous relative rates conditional on the risk sets; they are
not risk ratios and do not alone provide absolute benefit. Choose a risk or restricted-
mean estimand when that better answers the decision.

## Build analysis sets

Preserve identifiers and dates for eligibility, entry, exposure, event types, last
known follow-up, and covariate measurement. Validate:

- no event or censoring precedes entry;
- delayed entry is represented when units become observable after the time scale begins;
- one status is assigned at each terminal time under declared precedence rules;
- recurrent events have ordered episodes and at-risk intervals;
- competing events remain visible;
- baseline covariates precede or coincide with time zero;
- exclusions and missingness reconcile to the source cohort.

Summarize event and censor counts by group, site, time period, and important analysis
set. Quantify follow-up with a method appropriate to censoring rather than only the raw
median observed time.

## Causal caution

For treatment or exposure effects, define the assignment strategy, confounding model,
time-varying treatment/confounders, switching, adherence, and censoring assumptions.
Ordinary covariate-adjusted Cox regression does not automatically emulate a target
trial or identify a causal effect.
