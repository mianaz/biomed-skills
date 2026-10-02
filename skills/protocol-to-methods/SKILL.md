---
name: protocol-to-methods
description: Convert a laboratory or computational protocol and experiment records into a publication-ready Methods draft, preserving actual parameters, deviations, citations and reproducibility details. Supports Labmate notebook exports and journal-specific Methods structures.
---
# Protocol to Methods

Read the protocol, relevant paper/source citations and actual experiment records.
For Labmate notebook exports, inspect `procedure.protocolSteps`: `stepText`,
`completed`, `deviation`, and `actualParams`. Use actual execution records over
planned defaults. A protocol alone supports a Methods template; label it as such
and do not imply that its procedures were performed. Completion marks alone do
not establish sample sizes, approvals or successful results.

1. Establish the study system, design, independent unit, groups and procedure
   order. Reconcile discrepancies between the protocol and execution notes.
2. Write topical Methods subsections in logical order. Convert commands to concise
   narrative prose; combine routine steps while retaining details needed to
   reproduce the work. Preserve actual quantities, times, temperatures, reagents
   and identifiers, instruments, software/version and parameters.
3. Include controls, biological/technical replication, exclusions, randomization,
   blinding, ethics, sample-size rationale and statistical methods when supplied
   and applicable. Put missing information in `methods-questions.md`, with a clear
   draft placeholder only where necessary. Never fabricate approvals, catalog
   numbers, sample sizes or an analysis choice.
4. Keep published method citations and describe the actual modifications. For a
   Cell Press target, use the current STAR Methods template and Key Resources
   Table; for Nature or Science use the requested journal's current structure.
   `submission-check` resolves journal/stage requirements.
5. Deliver `methods.md`, a source-to-subsection mapping and the short questions
   list. Produce Word or another requested manuscript format when the available
   document tools support it.

For gene sets, link a complete original/used gene table with species, omissions,
additions and literature/database version. Report the actual scoring/enrichment
method, software/function/version, input layer/normalization, analysis unit and
parameters; distinguish display scaling and group averaging. Specify z-score
axis/reference and aggregation, or GSEA ranking statistic and contrast.

Apply `nature-writing`, then `nature-polishing`, then `humanizer` when available.
If unavailable, write precise academic prose directly. Remove audit-style,
apologetic and defensive phrasing without changing scientific meaning or turning
missing information into facts. Check every quantity and past-tense statement
against the supplied records after polishing.
