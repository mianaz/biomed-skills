---
name: biomed-stats
description: Plan, run or review biomedical statistics when the task needs a study design, sample-size rationale, model or contrast choice, effect estimate, uncertainty, causal adjustment or prediction evaluation. Start from the biological question and independent units, then load only the relevant method. Use for standalone statistical work or unresolved inference in another workflow; preserve valid results for wording or appearance-only edits. 生物医学统计、实验设计、样本量、统计分析与复核。
---

# Biomed Stats

Read [shared principles](../biomed-shared/core-principles.md).

Turn a biological question into an answerable design and an interpretable estimate.
Use progressive disclosure: establish the task and design here, choose a route in
[method selection](references/method-selection.md), then read only the relevant
method sections. Do not load every reference for a simple comparison.
For a concrete input-to-result walkthrough, open the optional
[worked examples](references/worked-examples.md): paired units, prospective power
and evaluation of a rare-positive classifier.

## Establish the task

| Product | Completion |
|---|---|
| Plan | Feasible allocation, estimand, comparisons and analysis; sample-size rationale or explicit planning scenarios |
| Analyze | Executed analysis, relevant diagnostics, effects and uncertainty, full results and biological interpretation |
| Review | Source-located statistical findings, their effect on conclusions and feasible repairs; identify what was recomputed |

Read the available protocol, data, metadata and analysis records first. Reuse valid
existing plans and results. Complete the requested products in the existing project
layout; a short analysis is sufficient for a simple question.

Before choosing a method, establish:

1. **Question and target:** description, group effect, association, causal effect,
   prediction or dynamic process; population, outcome, scale and time point.
2. **Independent information:** allocation and sampling units; pairing, blocks,
   nesting, repeated measurements and counts at each level.
3. **Observation and selection:** missingness/censoring, exclusions, measured
   covariates, planned comparisons and choices made after viewing outcomes.

Ask only for unrecoverable facts that change the analysis. If the target or
independence cannot be established, finish the supported description and name the
specific missing information. A different test cannot identify an unknown design.

## Select and execute

Apply [analysis consistency and reuse](../biomed-shared/analysis-consistency.md)
when constructing or reusing computed features.

Use the [method selector](references/method-selection.md) when a choice is needed.
For routine contrasts, consult the relevant section of shared
[analysis decisions](../biomed-shared/statistical-analysis.md); for explanations of
P values, uncertainty, replication or multiplicity, use the corresponding
[principle](../biomed-shared/statistical-principles.md). Method modules give their
own triggers, checks and sources.

Prefer R and established implementations. Check installed help and current primary
method documentation for specialized estimators, interval definitions and software
options. Run the justified model, inspect diagnostics and report all declared
contrasts. Match resampling and validation to the independent unit. Evaluate
consequential plausible alternatives when they could change the biological answer.
Preserve valid supplied Prism analyses and record actual exploratory selection.

## Deliver and hand off

Lead with the biological answer, effect and uncertainty, then the reason for the
method. Retain direct analysis data, unit definitions, exclusions, runnable R/Rmd,
fitted objects, relevant diagnostics and full-precision results. Record contrast
direction, independent n, interval method/level, model, raw/adjusted P and family
when applicable, and software versions. For prediction retain splits and held-out
predictions; for planning retain assumptions and the calculation.

For project work, update the
[root HTML dashboard](../biomed-shared/project-dashboard.md) with the delivered
result, direct data, analysis source and method record.

Reconcile n with the design, estimates with contrast direction, and adjustment with
the full family. Apply [writing principles](../biomed-shared/writing-principles.md)
when writing scientific interpretation. `scientific-plotting` owns rendering and
statistical display; `graphpad-prism` owns native projects;
`scientific-reproducibility` owns reusable handoff records;
`protocol-to-methods` writes the executed methods; `paper-review` owns the broader
manuscript argument. Use the same result record across these products.

For source rationale, read the optional
[source catalogue](../biomed-shared/statistical-sources.md). Read
[qualification notes](references/source-qualifications.md) when an article example
or equation is being implemented.
