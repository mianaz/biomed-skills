---
name: synthesize-biomedical-evidence
description: Answer a biomedical question by systematically finding, screening, extracting, appraising, and synthesizing literature and other citable evidence. Use for systematic, scoping, rapid, or structured narrative reviews; evidence maps; guideline or background evidence summaries; meta-analysis planning; PICO or PECO questions; or reconciling conflicting studies. Preserve reproducible searches, eligibility decisions, risk of bias, corrections or retractions, heterogeneity, and certainty. Do not use merely to mine reusable methods into the skill suite—that belongs to distill-biomedical-methods—or to write a narrative before the evidence review is complete.
---

# Synthesize Biomedical Evidence

Build the answer from traceable sources and explicit eligibility decisions. Match the
review depth to the decision: do not label a convenience search systematic, and do
not impose full systematic-review ceremony when a bounded rapid review is sufficient.

## Specify the review

1. Frame the question with the appropriate structure: PICO for interventions, PECO
   for exposures, population/index test/reference standard for diagnosis, population/
   predictor/outcome/time for prognosis, or a clearly bounded concept framework.
2. Choose systematic, scoping, rapid, or structured narrative review from the user's
   decision, required completeness, time, and expected evidence. State the limitations
   created by that choice.
3. Prespecify sources, search concepts, date and language limits, inclusion/exclusion,
   outcomes, eligible designs, screening process, extraction fields, risk-of-bias
   method, and synthesis plan before interpreting results.

Read `references/review-design.md` before choosing the review type or protocol depth.

## Search, screen, and extract reproducibly

1. Save every database or source, exact query, filters, search date, result count, and
   export or cached response. Search more than one appropriate source when completeness
   is claimed.
2. Deduplicate by stable identifiers plus title/author/year checks. Preserve the raw
   records and the deduplication mapping.
3. Screen title/abstract and full text against the same rules. Record exclusion reasons
   at full text and unresolved reviewer disagreements.
4. Check versions, errata, expressions of concern, retractions, protocols, registrations,
   supplements, data records, and code when they affect interpretation.
5. Extract design, population, units, interventions/exposures, comparators, outcomes,
   time, estimates, uncertainty, missingness, analysis method, funding/conflicts, and
   limitations into a structured table.

Read `references/screening-and-extraction.md` before screening or accepting a study's
reported number as comparable evidence.

## Appraise and synthesize

- Apply a risk-of-bias tool appropriate to the design; do not create a single opaque
  quality score when domain judgments matter.
- Separate direct evidence, indirect evidence, mechanistic plausibility, and expert
  interpretation. Journal prestige is not a substitute for internal validity.
- Combine results quantitatively only when effect definitions, populations, outcomes,
  time horizons, and designs are sufficiently compatible. Preserve study-level data,
  model choice, heterogeneity, influence, and small-study-bias assessments.
- Use a structured qualitative synthesis when pooling would conceal incompatibility.
  Explain conflicting direction, precision, bias, setting, or measurement.
- Rate certainty per consequential outcome and distinguish absence of evidence from
  evidence of no meaningful effect.

Read `references/synthesis-and-certainty.md` before meta-analysis or certainty claims.

## Deliver the evidence packet

Fill `assets/evidence-synthesis.template.md` or an equivalent structured artifact.
Include the review question and type, protocol deviations, search log, study-flow
counts, eligibility table, extraction table, risk-of-bias judgments, synthesis,
certainty, claim-evidence map, conflicts, and practical limits. Register search and
source provenance with `ensure-biomedical-reproducibility`, verify the evidence packet
with `verify-biomedical-analysis`, and route final audience adaptation to
`communicate-biomedical-results`.

Do not promote method rules from this review automatically. Route reusable paper-and-
code patterns to `distill-biomedical-methods` and `maintain-biomedical-skills`.
