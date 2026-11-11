---
name: citation-audit
description: Audit specific biomedical manuscript claims against their cited sources, checking identity, original support, scope, numbers and source status. Use for reference verification or a claim-to-source citation audit. Deliver a source-located audit table and targeted repairs; formatting-only edits belong to the writing task.
---

# Citation Audit

## Bound the audit

Read [writing principles](../biomed-shared/writing-principles.md) and
[terminology and citations](../biomed-shared/terminology-and-citations.md).
Use the designated manuscript and reference list. Establish whether the request
covers a passage, selected references or all cited claims. Reuse existing claim
IDs, evidence maps and source records. Inventory the in-scope claims before
checking them; include every requested claim in the final table, including those
whose sources remain inaccessible.

Split compound statements when their components require different evidence.
Keep one claim–source relationship per row, linking components of the same
sentence. When multiple sources jointly support a claim, record what each adds
and assess their combined coverage. Distinguish the number of claims from the
number of relationships checked; a paper cited repeatedly can support different
statements.

## Retrieve and compare

Use supplied papers and supplements first, then retrieve missing primary sources
through available literature tools, repositories or publisher pages. Read the
relevant Results, Methods, figures or tables. A title, search snippet or citation
in another review can locate a source; support assessment needs the relevant
source content. Record the actual access level, including abstract-only access.
Use [scientific semantics](../biomed-shared/scientific-semantics.md) and
[evidence and interpretation](../biomed-shared/evidence-and-interpretation.md)
when comparing measured objects, causal claims and scope.

Check each relationship at four levels:

| Level | Check |
|---|---|
| Identity | Authors, title, year, DOI/PMID or other stable identifier refer to the same work. |
| Support | Locate the original result or analysis that supports the exact proposition; distinguish a source's own finding from its citation to prior work. |
| Scope and inference | Compare population/model, treatment, dose/time, comparator, endpoint, denominator, numerical values and inferential strength as relevant. |
| Version and status | Identify the version used and check current publisher/repository notices for corrections, retractions or replacement. Record the lookup date and unresolved status access. |

Trace a review's specific empirical attribution to the original study when the
manuscript presents it as a primary result. A review can itself support a synthesis
at that scope. Check the manuscript's framing of both kinds of source. Keep
quantities tied to the correct study and denominator; do not combine several
papers into a result that none reported. For a proposed mechanism, distinguish
the measured link from the author's synthesis and locate support for each
consequential premise.

Unavailable source content leaves support unverified. Failure to find a result
in accessible material is reported at that access scope. Mark a claim unsupported
only after inspecting the material needed to judge it. Check corrections against
the specific cited result; state what a notice changes. Keep identity, support and
source-status checks separate so a verified DOI cannot imply verified support.

## Deliver the audit

Return a readable table at the requested scope, and a TSV when the audit is large
or a reusable file is requested. Include:

`claim ID / manuscript location`, `exact claim`, `source ID and version`,
`source locator`, `access level`, `identity check`, `support verdict`,
`source status and checked date`, `reason`, `targeted repair`.

Use these support verdicts:

- **Supported:** the source supports the proposition at its stated scope.
- **Partial:** the source supports an identified component; name the remaining gap.
- **Scope mismatch:** a material population, condition, endpoint or denominator differs.
- **Overstated:** the inference is stronger than the source supports.
- **Contradicted:** the relevant source reports an incompatible result.
- **Unsupported:** the inspected source does not supply the claimed support.
- **Unverified:** the evidence needed for a decision is unavailable or unread.

Use exact panel/table/section/page locators with a stable link or supplied file
pointer. Brief excerpts are optional; obey source quotation limits. Describe the
support in the auditor's words. Give a precise repair: match the source's scope,
split a claim, correct a value or attribution, or identify the missing source.
Verify any proposed replacement citation before recommending it as support.

Report coverage in claims and claim–source relationships, supported and unresolved
counts, and the most consequential repairs. A bounded or abstract-only audit
states that scope. A fictional exercise retains that label and its simulated
source status. Make authorized manuscript changes only when requested; preserve
the original and unresolved author choices. Completion is an auditable decision
for every in-scope relationship, including explicit unresolved entries.
