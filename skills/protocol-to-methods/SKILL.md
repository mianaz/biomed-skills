---
name: protocol-to-methods
description: Convert a laboratory or computational protocol and experiment records into a publication-ready Methods draft, preserving actual parameters, deviations, citations and reproducibility details. Supports Labmate notebook exports and journal-specific Methods structures.
---
# Protocol to Methods

Read [shared principles](../biomed-shared/core-principles.md).

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
4. Keep published method citations and describe the actual modifications. Use STAR Methods and a Key Resources Table when the verified target journal,
   article type and submission stage require them; otherwise use the applicable
   manuscript structure.
   `submission-check` resolves journal/stage requirements.
5. For a complete Methods deliverable, provide `methods.md`, a source-to-subsection
   mapping and consequential author questions. For a requested paragraph or
   subsection, return that text and only the questions needed to finish it.
   Produce Word or another manuscript format when requested and supported.

For gene sets or signatures, use [gene-set records](../biomed-shared/gene-set-records.md).
For features reused across manuscript components, apply
[analysis consistency](../biomed-shared/analysis-consistency.md) to reconcile the
executed definitions and computations with Results, legends and supplement.

Before drafting, read [writing principles](../biomed-shared/writing-principles.md).
Apply [terminology and citations](../biomed-shared/terminology-and-citations.md)
when revising the Methods. Check every quantity and past-tense statement against
the execution records; put unresolved factual details in the author questions.

Apply [section responsibilities](../biomed-shared/section-responsibilities.md):
keep procedures and necessary design rationale here; place findings and biological
interpretation in the relevant manuscript sections. Reconcile normalization and
statistical comparison wording with supplied Results and legends.

For a statistical Methods subsection, use the shared
[statistical principles](../biomed-shared/statistical-principles.md) to reconcile
the effect, analysis unit, interval definition and comparison family with the
execution records. Use the [shared result fields](../biomed-shared/statistical-analysis.md#retain-the-statistical-result)
to match the model, contrast direction, independent n, interval method, sidedness
and raw/adjusted P reporting to the saved analysis. Report planned and data-selected
analyses with their actual status. Use `biomed-stats` when new analysis is requested;
otherwise identify the missing execution record in the Methods questions.
