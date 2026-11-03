---
name: scientific-reproducibility
description: Preserve data, analysis choices, parameters and reusable outputs when performing or documenting scientific analyses. Use for source-data exports, saved analysis objects, analysis records and reproducible handoffs. Figure design and rendering belong to scientific-plotting; manuscript Methods drafting belongs to protocol-to-methods.
---

# Scientific Reproducibility

Keep reported or reused analysis outputs rebuildable from their inputs, code and
parameters. Apply this workflow while conducting analyses or when a reproducible
handoff is requested. Reading a paper, polishing prose and appearance-only figure
edits do not trigger a fresh analysis or a new project structure.

## Preserve the analysis record

Reuse the project's output layout. For a new analysis, `figures/`, `source_data/`,
`objects/` and `methods.md` provide a simple starting structure.

- Save the direct inputs behind reported results, including independent units,
  group definitions, transformations and exclusions. Keep original identifiers.
- Retain runnable analysis/plotting source and the object or native project needed
  for later tuning. Use CSV/TSV for shareable tables and the native format where
  it preserves information the table cannot carry.
- Record methods, software versions, source references, parameters and reasons for
  consequential choices in the [analysis log](references/methods-log.md). Preserve
  results and unresolved issues with their actual status.
- Preserve valid upstream statistics. Run a new test only when requested or needed
  for the scientific inference; appearance-only edits and descriptive figures do
  not require new tests. Save full-precision estimates, intervals and P values.

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
