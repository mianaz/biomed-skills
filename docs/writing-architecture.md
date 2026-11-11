# Writing responsibilities

## Task selection

Choose the entry by the requested result. The existing document, sources and
scope determine the work; a skill name is optional in the user's request.

| Request | Primary entry | Completion |
|---|---|---|
| Find the study's contribution, significance or strongest story | paper-framing | Recommended argument, model and overall figure sequence with sources |
| Draft or substantially rebuild manuscript text from evidence | paper-writing | Requested prose with factual and cross-reference checks |
| Polish, translate or tighten an existing passage | paper-polishing | Revised passage preserving meaning and scientific ambition |
| Review manuscript logic or scientific support | paper-review | Prioritized, source-located findings, repairs and resolution checks |
| Verify cited claims against sources | citation-audit | Claim–source audit with locators, coverage and targeted repairs |
| Explain a published paper | paper-distill | Sourced digest and requested reusable ideas |
| Map claims to experiments and results | paper-evidence-map | Editable graph and sourced evidence table |
| Render, repair or audit scientific figures | scientific-plotting | Scientific review, measured and visually inspected exports, source data and plotting source |
| Plan panels and assemble main/supplemental figure decks | figure-plan | Evidence inventory, independent panels and letters, inspected whole-figure exports |
| Explain a concept or mechanism visually | scientific-visual-explainer | Source-linked HTML lesson and editable assets |
| Create or edit a native Prism project | graphpad-prism | Verified native project or accurately labeled export |
| Convert paper Methods to a procedure | paper-to-protocol | Sourced protocol and requested export |
| Write Methods from execution records | protocol-to-methods | Methods traceable to actual work |
| Check journal rules and prepare submission files | submission-check | Verified checklist and organized package |
| Record an analysis and its reproducible outputs | scientific-reproducibility | Data, parameters, methods and reusable output records |

For a mixed request, finish each requested product using its responsible workflow.
Reuse the existing framing, claim IDs, source locators and manuscript decisions.
A simple writing task develops its own necessary argument. A local polishing task
finishes with the revised passage. Formal framing approval is needed only when
explicitly requested. Each skill owns completion of its named deliverable.

## Reference loading

All biomedical prose consumers load `biomed-shared/writing-principles.md`. It is
the maintained author guidance and governs scientific interest, biological significance
and preservation of conceptual ambition. `AGENTS.md` points to it. The support
directory has no independent skill trigger and is distributed with its consumers.

Each entry includes its execution steps and completion criteria. Conditional
links select the relevant evidence, manuscript placement, terminology, paragraph
or biomedical example guidance. Writing keeps section-specific guidance under
its own `references/` directory. A task reads the resources its decisions require.

`argument-bridges.md` covers example-to-judgment links and transitions.
`scientific-semantics.md` protects measured objects and proposition scope.
`revision-fidelity.md` governs edit scope, semantic comparison and manuscript
versions. Local polishing uses a 15–20% growth target within one language;
translation and substantive restructuring follow their requested scope.

A framing brief can supply the selected claim, model and figure order. An evidence
map supplies source relationships and existing IDs. Writing and polishing reuse
these records when present. Creating those artifacts is an optional task choice.

## Logic review

Shared paragraph and section guidance defines clarity, forward movement and
content placement. `biomed-shared/logic-review.md` defines one independent reviewer
for substantive section drafting and broader structural work, with the primary writer owning
all edits. This is an internal review role, not another user-facing skill or a
mandatory pipeline for short edits. It uses available context and reports the
scope actually reviewed. The writing bundle includes these shared references.

`paper-review` owns an explicit scientific manuscript review. It applies the
shared checks directly and does not launch another reviewer. `citation-audit`
checks claim–source relationships and retains unread sources as unverified.
Both reuse claim IDs and source records; neither is a compulsory drafting stage.

## Distribution

Install the full suite with its shared support directory, or use the focused
writing bundle. Keep the shared references beside their consumers. The current
plugin version is recorded in `.claude-plugin/plugin.json`.

## Verification

`check_writing.py` validates the five writing/review skill entry points and every local
Markdown reference in those directories and biomed-shared. `--integration` also
checks shared references in four existing consumers. Their other resources and
runnable scientific code are outside this check. The bundle builder validates its
own archive after extraction into an isolated directory and includes the license.

`test_writing.py` tests packaging and faults. `writing-cases.json` describes agent
routing and editorial evaluations; the Python tests validate that fixture's
structure only. To evaluate behavior, run each prompt in an actual agent session,
record the selected skills and resources, retain its output, and assess the stated
completion criteria. Record model, runtime and version. Report measured outcomes
only after that evaluation. Structural success does not certify manuscript quality.

`--suite` checks all entry points and instruction references for local resource
closure, external skill links and retired external routes. Historical credits
remain in maintainer documentation outside installed instructions.

`writing-regression-cases.json` contains 17 self-contained fictional cases and
correct-text controls. Withhold assessor criteria from the writing agent, retain
its outputs and resource report, and compare scientific fidelity, logic repairs,
new claims, preservation, length and prose quality. A full comparison requires
baseline, revised and no-skill conditions on the same cases.

The [10 November smoke record](../tests/evaluations/writing-smoke-20261110.md)
preserves the initial 12 outputs and a targeted retest. Comparative evaluation remains
pending.

The [style and flow follow-up](../tests/evaluations/style-flow-smoke-20261110.md)
records six tasks covering focus-led voice, sentence variation and direct transitions.
