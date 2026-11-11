# Focus, voice and flow smoke run — 10 November 2026

Six fictional polishing tasks were run by a separate default agent with no
inherited chat history, using the 0.6.1 candidate instructions. The named skill,
prompt and source material were supplied; assessor criteria were withheld.
The exact model identifier was not exposed. Resource paths are normalized below.
The development harness requested skill-creator guidance; the biomedical runtime
instructions themselves use only the bundled writing references.

## Assessment by the primary agent

| Case | Observed result |
|---|---|
| VOICE-01 | Antibody A remains the topic through uptake and delivery in passive clauses; proteases and payload action then carry the mechanism. Route, destination, agent and sequence are retained. |
| VOICE-02 | Crosslinks connect actively to obstruction of replication; the affected neighboring cells lead the second passage, with conjugate A explicit as the killing agent. |
| FOCUS-01 | Population M remains the subject. Profiling supplies context, and the targets remain expression-level observations. |
| FLOW-01 | The repeated bridge is removed. The dependence question follows directly; seven days, 40% versus 10%, exposure history and the R-depletion result remain intact. |
| STYLE-01 | Repeated openings are varied with a connected first sentence and a shorter persistence sentence; abundance and receptor activity remain distinct. No voice quota is imposed. |
| CONTROL-02 | The effective long comparison and its statistical meaning are retained, with only typography adjusted. |

This single-condition smoke run records the observed behavior on these tasks.
It does not measure comparative improvement or automatic skill selection.
Baseline/no-skill comparison and blinded human assessment remain pending.

## Preserved agent outputs

# Polished passages

All passages below use only the supplied fictional material.

## VOICE-01

After binding antigen T, antibody A was internalized by macropinocytosis and delivered to lysosomes by vesicular transport. There, lysosomal proteases released its payload, which damaged DNA.

## VOICE-02

**Passage 1:** In culture, payload P produced crosslinks that obstructed DNA replication.

**Passage 2:** Neighboring antigen-negative cells outside the antigen-positive compartment were also killed by conjugate A in culture.

## FOCUS-01

Population M persisted during treatment and, in the profiling data, retained expression of targets T1 and T2 while losing expression of T3.

Edit note: Specified target expression to retain the measured endpoint.

## FLOW-01

After washout, the induced state persisted for seven days. A later challenge reduced viability by 40% in previously exposed cultures and 10% in controls.

We next asked whether this altered response depended on receptor R. R depletion left the challenge response unchanged.

## STYLE-01

In donor-matched cultures, treatment A reduced transcript X abundance and increased protein Y abundance but did not alter receptor R activity. Both abundance changes persisted after washout.

## CONTROL-02

Although treatment A significantly reduced colony number relative to vehicle in six donor-matched cultures (paired *t*-test, *P* = 0.004), treatment B preserved colony number while reducing colony area, indicating distinct effects on colony establishment and expansion under these conditions.

## Resources read

- `../writing-regression-cases.json`
- `$CODEX_HOME/skills/.system/skill-creator/SKILL.md`
- `skills/paper-polishing/SKILL.md`
- `skills/biomed-shared/writing-principles.md`
- `skills/biomed-shared/revision-fidelity.md`
- `skills/biomed-shared/terminology-and-citations.md`
- `skills/biomed-shared/paragraphs-and-revision.md`
- `skills/biomed-shared/main-text-and-supplement.md`
- `skills/biomed-shared/argument-bridges.md`
- `skills/biomed-shared/scientific-semantics.md`

## Completion

All six requests are complete.
