# Writing provenance

Reviewed on 13 October 2026. The framing workflow and examples are original
instructions developed for this biomedical suite. The following materials
informed the editorial design. This page records attribution for maintainers;
it is outside the installed skills and is not a runtime instruction.

## Governing source

The author supplied `AGENTS(1).md`, titled “Biomedical research writing”. Its
content is retained verbatim in `skills/biomed-shared/writing-principles.md`.
The root `AGENTS.md` points to that source. The primary commitments are
scientific interest, biological significance, creative interpretation, positive
scientific value, removal of defensive writing and exact reporting.

## Editorial sources read

| Source | Files inspected | Contribution to this design |
|---|---|---|
| [Paper StoryCraft](https://github.com/ChenXiangYpily1234/paper-storycraft-skills) | README.md; EDITORIAL_PLAYBOOK.md | Relate questions, evidence and interpretation; make genuine contribution visible; organize paragraphs and place supporting detail by scientific function |
| [Nature writing](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-writing) | SKILL.md; static/core/workflow.md | Work at the requested scope; establish the argument; keep terminology and section structure coherent through revision |
| [Nature Results and Discussion guidance](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-shared/core/nature-results-discussion.md) | nature-results-discussion.md | Advance distinct scientific inferences through Results and develop a broader explanation in Discussion |

The inspected file blob identifiers were:

- StoryCraft EDITORIAL_PLAYBOOK.md: `9ef4e6f892a6bbb83d458c535e5b37b5e2c4183a`.
- Nature writing SKILL.md: `15824495c1ff934b12c1f2ba65ccf4296f8a563a`.
- Nature writing workflow.md: `d050fab184a1be779a23e50dde6d6151188c5d15`.
- Nature Results and Discussion: `11631fb861f557f9253ed07557f5aa2b2dcaccf9`.

The suite expresses the editorial ideas in its own instructions and fictional
biomedical examples. The referenced projects are not installed, fetched or
invoked by the writing workflow. Editorial guidance is distinct from official
journal policy; current requirements are verified for the actual submission.

## Architecture sources read for the refactoring

- [Writing for agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents): SKILL.md and SKILL-MECHANICS.md. Used its guidance on independent invocation, conditional references, explicit completion and a single authoritative home for each rule.
- [Nature Skills](https://github.com/Yuan1z0825/nature-skills): nature-writing/manifest.yaml, nature-polishing/SKILL.md, nature-shared/SKILL.md, nature-reviewer/SKILL.md, nature-response/SKILL.md and the README architecture/installation sections. Used its separation of task entries, section-specific references and shared support files.

These sources were inspected in the preceding architecture review. The
refactoring implements that agreed design in original instructions. It adds no
runtime fetch or invocation of the source projects. No platform-specific invocation
flags are inferred from a source project's recommendations.

## Suite independence

The dedicated framing, writing and polishing workflows use the bundled
biomed-shared directory. Common guidance in four existing writing consumers now
points to those same files. Section guidance is local to paper-writing. Shared
support is distributed with the selected skills; the standalone boundary is the
installed package. Source attribution remains here for maintainers.

See writing-architecture.md for responsibility boundaries, migration and test scope.
