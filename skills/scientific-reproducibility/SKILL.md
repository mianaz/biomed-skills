---
name: scientific-reproducibility
description: Preserve data, analysis choices, parameters and reusable outputs when performing or documenting scientific analyses. Use for source-data exports, saved analysis objects, analysis records and reproducible handoffs. Figure design and rendering belong to scientific-plotting; manuscript Methods drafting belongs to protocol-to-methods.
---

# Scientific Reproducibility

Read [shared principles](../biomed-shared/core-principles.md).

Keep reported or reused analysis outputs rebuildable from their inputs, code and
parameters. Apply this workflow while conducting analyses or when a reproducible
handoff is requested. Reading a paper, polishing prose and appearance-only figure
edits do not trigger a fresh analysis or a new project structure.

## Preserve the analysis record

Reuse the project's output layout. For a new analysis, `figures/`, `source_data/` and
`methods.md` provide a simple starting structure; add `objects/` only when needed.

Keep the project's top-level HTML entry current under the
[dashboard contract](../biomed-shared/project-dashboard.md). Link each delivered
result and figure to its direct data, code/object and method or run record;
retain the project's current-version decisions and access to older outputs.

- Save unique direct inputs once, including independent units, group definitions,
  transformations, exclusions and original identifiers. Reuse them across panels
  and appearance revisions; link large upstream data by its existing version/path.
- Retain runnable source and parameters. Save objects when needed for expensive
  computation, complex state or native tuning, and preserve native manual edits.
  Use CSV/TSV for shareable tables and native formats for state tables cannot carry.
- Record methods, software versions, source references, parameters and reasons for
  consequential choices in the [analysis log](references/methods-log.md). Preserve
  results and unresolved issues with their actual status.
- Preserve valid upstream statistics. Run a new test only when requested or needed
  for the scientific inference; appearance-only edits and descriptive figures do
  not require new tests. Save full-precision estimates, intervals and P values.

For reused features and method choices, apply
[analysis consistency](../biomed-shared/analysis-consistency.md). Keep the primary
definition, computation and linked outputs in the existing analysis record, with
named adaptations and reasons for changes.

When recording statistical inference, apply the shared
[result fields](../biomed-shared/statistical-analysis.md#retain-the-statistical-result)
and retain the target effect, comparison family and analysis-selection history.
Read the relevant [statistical principle](../biomed-shared/statistical-principles.md)
when interpreting those choices or results.

For figure exports, use the [figure handoff](references/figure-output-contract.md).
`scientific-plotting` owns design, typography, statistical display and visual
verification. Follow existing project delivery requirements when retaining versions.

## Run and name outputs

For parameter sweeps, include informative parameters in run names and keep a
per-run table linking inputs, parameters, outputs and completion status. Use
file-safe internal IDs where required by tools; preserve scientific display labels
and source sample IDs, with a mapping if internal IDs differ.

On a shared cluster, submit compute-heavy work through its scheduler or use an
allocated interactive compute session. Follow the project's confirmed account,
resources and environment; record job IDs and inspect completion logs. For local
workstations or managed runtimes without a scheduler, use their available compute
controls. A scheduler is not a prerequisite for all computational work.

When revising code, preserve scientific meaning, source data, statistical results
and the records needed to rebuild the affected outputs.
