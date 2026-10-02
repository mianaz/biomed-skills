---
name: communicate-biomedical-results
description: Turn completed biomedical analyses into concise, audience-aware, evidence-backed stories, briefs, reports, manuscripts, or presentations. Use when interpreting and packaging results, translating broad claims into precise answers, mapping claims to artifacts, choosing main versus supplemental material, explaining negative or inconclusive findings, or adapting the same evidence for scientific peers, cross-domain collaborators, or executive audiences.
---

# Communicate Biomedical Results

Communicate the strongest defensible answer supported by the completed analysis. Do
not maximize the number of findings or turn every limitation into another project.

## Assemble the evidence packet

Read the analysis contract, verification report, run manifest, result tables, and
figures. Treat files and computed values as evidence; treat prior narrative as a draft.
Preserve question, contrast, output, and check IDs so each statement remains traceable.

Do not communicate a material claim that failed verification. Label unresolved or
unverified evidence plainly.

## Turn broad claims into answerable questions

Restate vague comparisons as components that the available evidence can settle. For
example, replace "model A is better" with questions such as:

- Does it recover the prespecified cell types?
- Are matched populations transcriptomically closer to the reference?
- Are maturation states comparable?
- Is the target functional program reproduced?

Use the questions already defined in the analysis contract. If a new question changes
scope or requires new analysis, return it to `plan-biomedical-analysis` rather than
quietly adding it during storytelling.

## Build the claim-evidence map

Create a compact table before drafting prose or slides:

| Field | Record |
|---|---|
| Claim ID and question ID | Stable identifiers from the contract or a local claim ID |
| Exact claim | One falsifiable statement without promotional language |
| Status | `supported`, `not_supported`, `inconclusive`, or `technical_failure` |
| Direct evidence | Artifact path plus table rows, statistic, or figure panel |
| Key result | Effect or direction, uncertainty, sample unit, and multiplicity-aware significance when relevant |
| Boundary | Design limitation, excluded population, assumption, or practical constraint |

Separate direct results from interpretation and literature context. A plausible
mechanism without direct support is a hypothesis, not a result. Resolve conflicting
numbers before writing; one quantity must have one canonical value across text,
figures, and tables.

## Shape the story

Use a simple hierarchy:

1. State the decision-relevant question and one-sentence answer.
2. Present two to four claims that jointly support the answer.
3. Name the evidence and uncertainty for each claim.
4. State the boundary of the conclusion.
5. End with the implication or next decision.

Keep negative results when they answer the question or rule out an explanation. Drop
results that add no unique evidence, even if technically interesting.

## Adapt to the audience

| Audience | Lead with | Keep available but secondary |
|---|---|---|
| Scientific peer | Question, design, analysis unit, effect, uncertainty, and validity limits | Implementation detail already documented in methods or supplement |
| Cross-domain collaborator | Biological meaning, plain-language method, visual workflow, and what the result changes | Specialized terminology and exhaustive diagnostics |
| Executive, administrator, or funder | Why it matters, answer, confidence, impact, constraint, and requested decision | Technical workflow, package detail, and sensitivity analyses |

Define unfamiliar terms once. Prefer a schematic for study design or mechanism, a
plot for quantitative evidence, and a table for exact mappings or values. Delegate
figure construction and formatting to `create-scientific-figures`.

## Handle negative results and constraints honestly

Distinguish four outcomes:

- **Supported:** evidence meets the stated criterion.
- **Not supported:** adequate evidence does not support the prespecified claim.
- **Inconclusive:** uncertainty, power, missing data, or confounding prevents a clear
  answer.
- **Technical failure:** the assay or analysis did not yield interpretable evidence.

Describe what a negative result rules out and what remains possible. Treat sample,
funding, compute, technology, access, and timing limits as boundaries on the claim—not
as automatic reasons to demand more work. Recommend new data only when it could change
an important decision and is realistically obtainable.

## Separate main and supplemental material

Put in the main story the central question, decisive biological or clinical evidence,
effect and uncertainty, and any validity caveat needed to interpret them. Put detailed
QC, method benchmarks, parameter sweeps, sensitivity analyses, extended tables, and
technical diagnostics in supplemental material.

Do not bury a check that determines whether the headline result is valid. Summarize
that check in the main story and place its detailed evidence in the supplement.

## Finish instead of extending indefinitely

Deliver once every headline claim has a status, direct evidence, a bounded limitation,
and audience-appropriate wording, with no unresolved contradiction that invalidates
the answer. Offer at most three prioritized next actions, and only when each could
change interpretation, confidence, or a real decision.

Do not append generic calls for more experiments, repeat robustness checks without a
material risk, or keep optimizing presentation after the evidence hierarchy is clear.
Return disputed results to `verify-biomedical-analysis` and genuine scope changes to
`plan-biomedical-analysis`.
