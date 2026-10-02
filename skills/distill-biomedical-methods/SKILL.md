---
name: distill-biomedical-methods
description: Extract reusable, provenance-rich methods, decision rules, validation patterns, figure strategies, implementation details, failure modes, and limitations from biomedical papers together with supplements, protocols, registrations, data records, and code. Use when learning from a high-quality clinical, imaging, experimental, omics, computational, diagnostic, or evidence-synthesis study; when a user supplies a DOI, PDF, repository, protocol, or supplement; or when proposing evidence-backed skill updates. Produce a fixed-schema method digest and staged promotion proposals, but do not answer a literature-review question or edit shared skills without governance approval.
---

# Distill Biomedical Methods

Turn study-specific methods into structured evidence for reuse without converting
every published choice into suite policy.

## Assemble the source packet

1. Gather the primary paper, supplement, protocol or registration, statistical
   analysis plan, data record and dictionary, code, model weights, figure sources,
   corrections, and retraction status when applicable.
2. Pin code and mutable resources to a commit, version, date, or cached artifact.
   Record absent materials and do not imply that reconstructed implementation was
   published.
3. Tag each extracted statement as `full-text`, `methods-only`, `protocol`,
   `supplement`, `registry`, `captions-only`, `abstract-only`, `repo-only`, or
   `reconstructed`.

Read `references/source-evaluation.md` before treating a method as reusable evidence.

## Distill with one schema

Copy `assets/method-digest.template.md` to the active knowledge store and fill every
applicable section. For each method, preserve:

- scientific purpose, study design, intended use, population or biological context;
- independent and nested units, sampling or allocation, analysis sets and outcomes;
- acquisition, preprocessing, QC, exclusions, missingness, and leakage controls;
- instruments, reagents/lots, protocols, reference standards, software, versions,
  models, parameters, and rationale;
- diagnostics, internal and external validation, uncertainty, sensitivity analyses,
  and contradictory evidence;
- exact source and code locators, implementation gaps, limitations, and reuse boundary.

For figures, capture the claim, source data, units, encoding, exclusions, statistics,
integrity requirements, code locator, and whether the recipe is published or
reconstructed. Route visual rules to `create-scientific-figures`.

## Evaluate fit, not prestige

Separate methodological quality from biological, clinical, or operational validity.
A computational paper may strongly support an implementation and weakly support a
mechanism; an experimental paper may show the inverse. A diagnostic or clinical study
may be internally strong but not transport to the intended population. Journal name
alone changes none of these judgments.

Use `references/domain-evidence.md` for clinical, imaging, experimental, computational,
and evidence-synthesis appraisal prompts.

## Stage bounded promotion proposals

Each proposal must name one owner skill, the smallest exact change, source locator,
evidence strength, target reuse case, known failures, and validation plan. Read
`references/promotion-routing.md` and route proposals through
`maintain-biomedical-skills`.

Require complete provenance, an overlap check, evidence that the pattern generalizes,
deterministic validation, a realistic forward test when practical, and explicit
maintainer approval. Retain rejected proposals in the digest. Never auto-edit shared
skills, copy project paths or unexplained defaults, or treat one paper as a universal
rule.

Use `synthesize-biomedical-evidence` when the output should answer a research question
across studies. This skill instead mines methods and patterns for governed reuse.
