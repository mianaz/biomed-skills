---
name: design-biomedical-study
description: Design a biomedical study before data collection or before an existing study is analyzed by defining the decision, target population, unit hierarchy, intervention or exposure, controls, endpoints, allocation, blinding, replication, precision, bias controls, governance, and analysis handoff. Use for experimental protocols, observational cohorts, diagnostic-accuracy studies, validation studies, pilot studies, sample-size planning, or requests to improve a proposed study design. Do not use to execute the resulting analysis, write a laboratory SOP, or substitute technical replicates for independent biological or participant-level units.
---

# Design a Biomedical Study

Create a design that can answer a specific decision-relevant question within the
available ethical, material, financial, and operational constraints. Separate what
the study can identify from what later analysis can only describe.

## Establish the design target

1. State the decision, primary question, target population or system, intended use,
   and claim that would be supported by a positive, negative, or inconclusive result.
2. Choose the design family: randomized experiment, controlled laboratory study,
   prospective or retrospective cohort, case-control study, diagnostic-accuracy
   study, prediction-model development or validation, method comparison, or pilot.
3. Define the estimand or target quantity before selecting tests. Name the population,
   intervention or exposure, comparator, outcome, time horizon, and summary measure
   when applicable.

Read `references/design-patterns.md` when selecting among design families or handling
diagnostic, observational, or repeated-measure structures.

## Define units, allocation, and measurements

1. Draw the unit hierarchy from the independent unit through repeated or technical
   measurements—for example participant to visit to lesion, animal to tissue to field,
   or experiment to plate to well. Assign sampling, intervention, and analysis roles.
2. Specify inclusion, exclusion, recruitment or sampling frame, analysis sets, and
   how missing or unevaluable units will be accounted for.
3. Define comparators and controls, including negative, positive, vehicle, sham,
   reference-standard, or baseline controls as the design requires.
4. Specify randomization, allocation concealment, blocking, stratification, blinding,
   order balancing, and batch or site allocation at the level where each can prevent
   bias. Do not claim blinding or randomization that operations cannot implement.
5. Define primary and secondary endpoints with units, timing, acquisition method,
   measurement validity, adjudication, and direction of benefit or harm.

Read `references/units-endpoints-and-precision.md` before counting replicates,
selecting endpoints, or justifying sample size.

## Size the study honestly

- Base sample size on the independent unit, target effect or precision, variability,
  event rate, prevalence, clustering, attrition, multiplicity, and planned model.
- Prefer a precision or feasibility target when an effect-size assumption would be
  speculative. Label a pilot as a pilot; do not retrofit confirmatory power claims.
- Run sensitivity across plausible assumptions and identify which assumption drives
  feasibility. Do not use technical measurements to inflate effective sample size.

## Control bias, governance, and feasibility

Identify confounding, selection, measurement, information, spectrum, verification,
observer, batch, attrition, and leakage risks relevant to the design. Record human-
subjects, animal, biosafety, hazardous-material, privacy, consent, data-use, and
disclosure requirements before irreversible work. Read
`references/governance-and-handoff.md` for the compact risk screen and completion gate.

## Hand off an executable design

Produce a concise design record containing the question, estimand, unit hierarchy,
sampling and allocation, controls, endpoints, analysis sets, precision rationale,
bias controls, governance status, feasibility limits, and unresolved decisions. Route
it to `plan-biomedical-analysis` to create or update the analysis contract. Route data
readiness to `validate-biomedical-data`, implementation to the narrowest domain skill,
and independent review to `verify-biomedical-analysis`.

Finish when every primary endpoint and comparison has a valid independent unit,
measurement plan, analysis set, and feasible path to evidence. Do not hide a design
failure behind a more elaborate downstream model.
