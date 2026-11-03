# Skill scope and writing review — 2026-11-03

Release: 0.5.1. Scope: all 14 released skill entries, writing/shared references,
section guidance, the reproducibility contract and installed writing routes.
The workspace also contains a separate uncommitted visual redesign with 13
entries. This release preserves that work and does not publish its assets.

## Trigger and ownership map

| Skill | Trigger | Owned output | Boundary |
|---|---|---|---|
| paper-framing | Choose the contribution, scientific story or conceptual model | Framing recommendation and overall figure sequence | No mandatory framing stage before a simple writing request |
| paper-writing | Draft from evidence or substantially rebuild an argument | Requested manuscript prose, including legends and cover letters | Owns substantive synthesis; uses records-based Methods workflow when needed |
| paper-polishing | Polish, translate or compress developed prose | Revised text preserving meaning, numbers and claims | Fragmentary notes and new mechanisms route to writing |
| paper-distill | Explain a paper or answer a focused reading question | Sourced digest or focused answer | Full gene-list extraction only when relevant to reuse or the claim |
| paper-evidence-map | Request an editable claim–experiment–result graph | Canvas, source graph, evidence table and preview | Mapping does not itself authorize manuscript revision |
| paper-to-protocol | Turn reported Methods into executable steps | Sourced procedure and supported printable/import outputs | Planned procedures retain their status |
| protocol-to-methods | Write Methods from protocol and execution records | Requested paragraph, subsection or complete Methods package | No automatic file package for a paragraph-only request |
| submission-check | Find current journal rules or prepare submission files | Verified rules at requested scope or submission package | A dimension lookup does not launch package preparation |
| scientific-plotting | Create, repair or evaluate biomedical data figures | Rendered figures, editable sources and direct data | Owns visual and statistical-display rules |
| scientific-plotting-tidyplots | User requests this tidyplots-specific entry by name | Delegate to scientific-plotting and its tidyplots route | Compatibility entry; no second output contract |
| graphpad-prism | Requested deliverable is a native Prism project or figure | Verified native project/export or accurately labelled fallback | Reuses plotting rules; native format work stays here |
| figure-plan | Plan panels or assemble manuscript figures | Panel inventory or editable whole-figure decks and exports | Planning-only requests end at the plan; panel drawing uses its owner |
| scientific-visual-explainer | Explain mechanisms or workflows visually | Static schematic, HTML lesson or requested animation | Data charts route to plotting; whole-figure assembly to figure-plan |
| scientific-reproducibility | Conduct/document analyses or prepare reusable handoffs | Inputs, code, objects, parameters and analysis records | No new analysis for prose or appearance-only edits |

## Findings and repairs

| Issue | Before | Repair |
|---|---|---|
| Methods contamination | Analysis log called a manuscript Methods section despite containing results and interpretation. | Separate the analysis record from the procedures selected for Methods. |
| Formatting scope | Shared manuscript pagination and Times New Roman applied to all consumers. | Limit document defaults to full manuscript exports; preserve figure workflow typography. |
| Reviewer recursion and scope | Complete sections always triggered review; reviewer could inherit the same delegation instruction. | Primary writer launches one reviewer for substantive drafting/structural work; reviewer does not delegate. |
| Section duplication | Detailed section rules repeated in the shared table and section references. | Keep placement/consistency in shared guidance; each section reference owns its detailed rules. |
| Polishing versus writing | Developed prose translation and drafting from notes could overlap. | Translate prose in polishing; construct or substantially rebuild arguments in writing. |
| Overproduction | Focused paper reading, a Methods paragraph or a journal-size query could require full artifact packages. | Scale deliverables to the requested task; retain complete workflows for full requests. |
| Reproducibility versus plotting | A second visual contract imposed tests, figure variants, typography and legends. | Keep records and reusable inputs here; delegate figure rules to scientific-plotting. |
| Scientific labels | All sample/category labels were restricted to filename-safe characters. | Apply safe-character rules to internal IDs only and preserve source/display labels. |
| Runtime assumptions | Heavy work always required a scheduler. | Use scheduling on shared clusters and available compute controls on local/managed runtimes. |
| Compatibility duplication | The tidyplots entry repeated the main plotting workflow. | Retain a short delegate and existing resources for old callers. |
| Invalid metadata | Visual-explainer description failed YAML parsing. | Use a valid quoted, task-focused description. |
| Stale documentation | The architecture still described an unreleased 0.4.0 proposal and verbatim frozen guidance. | Describe the maintained guidance and current distribution. |

## Validation

- All released skill metadata are checked with the skill-creator validator.
- Writing package integration and all 22 tests in the clean release pass.
- An independent reviewer inspected the entry points and writing/reproducibility
  references. A bounded fictional Methods trial retained n, normalization and
  test, and excluded outcome, proposed mechanism and resolved import error.
- The earlier fictional Results/Discussion trial clarified comparisons and
  produced a specific literature comparison. Neither trial establishes quality
  across a full manuscript or all 14 workflows.
- New reusable evaluation cases cover section translation, analysis-log-to-Methods,
  independent logic review and requirements-only queries. The fixture remains
  labelled not_run_on_agent because the complete fixture suite was not executed.

## Release boundary

Build on current remote main and include only reviewed writing/scope changes.
Leave local pending visual work and unpublished plotting commits untouched.
Update the curated plugin source through the normal plugin installer and align
standalone writing skills that are also visible to Codex. Verify installed files
against this release before reporting synchronization complete.
