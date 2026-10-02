# Screening and extraction

## Search record

For each source retain database/platform, interface, exact query, controlled vocabulary,
filters, coverage dates, execution time, result count, export format, and cached result
or checksum. Record citation chaining, registry searches, preprints, grey literature,
author contact, and manual additions separately.

Pilot each major query against a small set of known relevant and known irrelevant
records. If a claimed-comprehensive search misses a sentinel study, revise the concepts,
controlled vocabulary, field restrictions, or source coverage before screening. Save
the pilot result and any query change as a protocol decision.

## Deduplication and screening

- Preserve raw records and assign stable review IDs before deduplication.
- Match identifiers first, then normalized title/author/year; review uncertain matches.
- Pilot eligibility rules on a mixed sample and refine them before full screening.
- Keep title/abstract exclusions at aggregate level and one explicit reason for every
  full-text exclusion.
- Resolve disagreements by a declared process. Report single-reviewer stages and their
  verification sample rather than implying duplicate review.
- Automated or AI-assisted screening may prioritize records or propose decisions, but
  it must preserve every record, score, model/tool version, prompt or rule, and final
  disposition. Do not silently exclude records from an unvalidated score threshold.
  Validate exclusion performance against independently reviewed records—including
  known eligible and difficult borderline studies—and require traceable human or
  independent verification wherever a missed study could change a consequential claim.
- Link companion papers, protocols, follow-ups, corrections, and analyses to one study
  so they are not counted as independent evidence.

## Extraction

Extract at the study, report, outcome, and estimate levels as needed:

- design, setting, dates, recruitment/sampling, eligibility, sample and unit hierarchy;
- intervention/exposure/index test, comparator/reference standard, allocation/blinding;
- outcome definition, time, analysis set, missingness, exclusions, and follow-up;
- effect/metric, denominator, uncertainty, adjustment set, multiplicity, model;
- validation, subgroup and sensitivity analyses, adverse events or failures;
- funding, conflicts, registration, protocol deviations, data/code availability;
- risk-of-bias evidence and exact source locator.

Retain reported units and definitions before harmonization. Every converted effect or
imputed statistic must keep the formula, assumptions, and source fields.

## Verify sources and citations

- Resolve persistent identifiers where available and compare title, authors, year,
  version, journal or repository, correction status, and retraction status against the
  cited report—not only against a secondary bibliography.
- Link every extracted result to the exact table, figure, page, supplement, registry
  field, or data record from which it came. An identifier that resolves does not verify
  the scientific claim or the extracted number.
- Reconcile in-text claims, extraction rows, and the final reference list. Flag
  inaccessible full text, abstract-only evidence, translated material, and metadata
  conflicts instead of silently filling gaps.
- Repeat source-status and metadata checks at finalization for consequential evidence,
  especially preprints, corrected reports, and living-review updates.
