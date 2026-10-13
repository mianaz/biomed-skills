# Writing responsibilities

## Task selection

Choose the entry by the requested result. The existing document, sources and
scope determine the work; a skill name is optional in the user's request.

| Request | Primary entry | Completion |
|---|---|---|
| Find the study's contribution, significance or strongest story | paper-framing | Recommended argument, model and overall figure sequence with sources |
| Draft or substantially rebuild manuscript text from evidence | paper-writing | Requested prose with factual and cross-reference checks |
| Polish, translate or tighten an existing passage | paper-polishing | Revised passage preserving meaning and scientific ambition |
| Explain a published paper | paper-distill | Sourced digest and requested reusable ideas |
| Map claims to experiments and results | paper-evidence-map | Editable graph and sourced evidence table |
| Render data or repair figure appearance | scientific-plotting | Inspected figure, source data and plotting source |
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
the verbatim author source and governs scientific interest, biological significance
and preservation of conceptual ambition. `AGENTS.md` points to it. The support
directory has no independent skill trigger and is distributed with its consumers.

Each entry includes its execution steps and completion criteria. Conditional
links select the relevant evidence, manuscript placement, terminology, paragraph
or biomedical example guidance. Writing keeps section-specific guidance under
its own `references/` directory. A task reads the resources its decisions require.

A framing brief can supply the selected claim, model and figure order. An evidence
map supplies source relationships and existing IDs. Writing and polishing reuse
these records when present. Creating those artifacts is an optional task choice.

## Migration from the first 0.4.0 proposal

- Narrow paper-framing to contribution, significance, conceptual explanation and
  overall figure order.
- Add paper-writing for manuscript text and paper-polishing for existing prose.
- Move the original AGENTS content to biomed-shared/writing-principles.md without
  changing its bytes. Replace AGENTS.md with a short conditional pointer.
- Move the biomedical examples to shared references and split section guidance
  into paper-writing references. Move paragraph revision into shared references.
- Replace duplicated prose policy in paper-distill, paper-evidence-map,
  protocol-to-methods and submission-check with explicit shared pointers.
- Remove the old framing-only package checker, tests and section-writing file.
  Check the installed writing package and its shared resources instead.

Install the full suite with its support directory, or use the bundled writing
subset. Replace the previous paper-framing directory as a unit after backing it
up so retired references and tests do not remain in a local installation.
The proposed package version stays 0.4.0 because the earlier PR was unreleased.

## Verification

`check_writing.py` validates the three writing skill entry points and every local
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
