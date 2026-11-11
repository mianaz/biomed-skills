# Writing smoke evaluation — 10 November 2026

This is a recorded single-condition agent smoke run using the 12 fictional cases
in [writing-regression-cases.json](../writing-regression-cases.json). The writing
agent received each prompt, input and named primary skill, with assessor criteria
withheld. The primary agent then compared the saved outputs with those criteria.
Automatic skill selection was not tested.

- Runtime: Codex desktop; one separate default agent with no inherited chat history.
  The exact model identifier was not exposed in the evaluation result.
- Repository base: `ec2c24c`, with existing local changes. This was a working-tree
  evaluation, not an evaluation of the committed release.
- Initial seven cases used the snapshot in
  `dist/biomed-writing-20261110.zip`. After a targeted revision-fidelity change,
  BRIDGE-01 was repeated and five additional cases were run. The updated snapshot
  is `dist/biomed-writing-20261110-v2.zip`.
- Inputs and source-status records are fictional. No external lookup took place.
- Resource lists below are agent-reported. Workspace prefixes and temporary input
  links were normalized for portability; generated prose is otherwise preserved.

## Assessment by the primary agent

| Case | Observed result |
|---|---|
| BRIDGE-01 | Both mechanism–injury pairs and the broader synthesis were repaired. Initial growth was 31 to 44 whitespace-delimited words (+41.9%). After adding an explicit count and redundancy check, the same agent produced 37 words (+19.4%), preserving both links. |
| BRIDGE-02 | Surface-antigen change connects lineage change to delivery; efficacy remains at culture scope. |
| SEMANTICS-01 | Reporter, dose, time, partial negation and untested dependence are preserved; the accurate original stays unchanged. |
| SEMANTICS-02 | Translation preserves absence-of-evidence meaning, partial negation, 300 total cells and three independent patients. |
| CONTROL-01 | The accurate sentence, effect, independent cultures and test remain unchanged. |
| CONTROL-02 | The connected long sentence, meaningful “significantly,” matching and P value remain unchanged. |
| CONCEPT-01 | Transcript abundance and dosing duration replace incorrect entities; dependence is reported at its tested status. |
| REVIEW-01 | Source-located priorities identify the contradicted receptor claim and model generalization, while developing the persistence finding's significance. Repairs include resolution checks. |
| VERSION-01 | The abstract count is resolved to eight against designated v3; the excluded control and correct statements are retained. |
| CITATION-01 | All four sentences and five atomic claim–source relationships are included. The unread source remains unverified; the corrected 12% value is used. |
| CITATION-02 | Per-study versus total counts are resolved using 200 + 300 + 400 = 900 and original-source locators. Cohort independence is left as an additional unverified question, separate from the confirmed count error; source status remains unverified. |
| STORY-01 | Persistent altered response leads the story; assay reliability moves to a supporting role, with molecular storage retained as an open question. |

These observations support completion of this smoke run. They do not establish
comparative improvement: baseline skills and a no-skill condition were not run,
the retest used the same agent, cases shared an evaluation session, and no blinded
human prose-quality assessment was performed. A full comparison remains pending.
The routing cases in `writing-cases.json` also remain unevaluated on an agent.

## Initial seven outputs

# Biomedical writing forward test

All seven tasks use fictional evidence. Source contents and status notes are taken only from the supplied [requests.json](../writing-regression-cases.json). No external verification was performed.

## BRIDGE-01 — Minimal polishing

Conjugate design shapes toxicity. In early studies, plasma payload release by agent A was linked to dose-limiting marrow suppression; uptake of plasma-stable agent B by antigen-positive normal epithelium was linked to dose-limiting epithelial injury. These observations link tolerability to payload release and target biology.

**Consequential edit:** Each agent now carries its source-reported exposure mechanism and injury (Source A, Results paragraph 2; Source B, Results paragraph 4). The conclusion includes both payload release and target biology. The added mechanism clauses make the passage longer than the usual local growth target; they supply the premises needed for its conclusion.

## SEMANTICS-01 — Polishing

At 10 nM for 24 h, compound C increased ARE-reporter activity in line M. This increase was not solely explained by more reporter-positive cells. Endogenous AR target transcripts were unchanged, and AR dependence was not tested.

The passage is already clear; it is retained unchanged.

## SEMANTICS-02 — Translation

At the doses tested, we have not yet observed evidence of liver injury. This effect was not solely attributable to changes in cell number. We measured a total of 300 cells from three patient samples, with each patient serving as an independent biological unit.

## CONTROL-01 — Publication check

X depletion reduced colony number by 30% relative to vehicle in four independent cultures (two-sided Welch test, P = 0.01).

Retained unchanged.

## REVIEW-01 — Scientific review

The washout and later-challenge results provide a compelling basis for a model in which prior exposure changes later responses in line M. The central interpretation of R-dependent transcription conflicts with the supplied endogenous-transcript and R-depletion results.

**Material reviewed:** The complete supplied fictional record: Abstract sentence 2; Results paragraphs 1–2; Figs. 1–2; Methods paragraph 3; Discussion paragraph 1. Findings below are limited to this record. No section rewrite is provided.

| Priority | Manuscript location and claim | Evidence location | Finding and consequence | Feasible repair | Resolution check |
|---|---|---|---|---|---|
| P0 — Central conclusion at risk | Abstract sentence 2: C restores R-dependent transcription. Discussion paragraph 1: the reporter increase establishes R reactivation. | Results paragraph 1: 40% reporter increase. Fig. 2: endogenous R-target transcripts unchanged; reporter increase persists after R depletion. | The receptor-reactivation interpretation conflicts with the assays that address endogenous transcription and R dependence. It changes the meaning of the main result. | Align the central claim with the observed reporter response and retain the Fig. 2 results in the interpretation. Build the study's contribution around the persistent response and later-challenge effect where supported. | Abstract and Discussion identify the reporter endpoint and agree with both Fig. 2 findings. R-dependent transcription is no longer asserted as an established result. |
| P1 — Major revision | Abstract sentence 2: response occurs “across tumors.” | Methods paragraph 3: one tumor-derived line M. Fig. 1: three independent cultures in that line. | Replication across cultures establishes the result within line M; the manuscript expands its scope to tumors more broadly. | Limit the observed response to the tested tumor-derived line M. Retain the three-culture replication as the study's independent experimental units. | Abstract, Results and figure descriptions use the same model scope and distinguish cultures from tumor models. |
| P1 — Major revision | Discussion paragraph 1: persistence is “merely descriptive.” | Results paragraph 2 and Fig. 1: response persists after washout and changes the later challenge response. | This wording obscures the functional consequence of treatment history and undersells the strongest available discovery. | Connect washout persistence to the altered challenge response. Develop a clearly identified treatment-history or cellular-memory model and the specific question of how the effect persists. The current evidence supports this repair without new experiments. | Discussion explains why persistence matters for the later response, retains both observations, and labels the proposed memory mechanism as a model. |

## VERSION-01 — Consistency before submission

The designated v3 source table resolves the active-compound count now: **eight active compounds, A–H**, with PC recorded as an excluded positive control.

**Material reviewed:** Supplied manuscript v3 Abstract sentence 3, Results paragraph 4, Fig. 3 legend; designated source table v3; historical source table v2. All refer to fictional records in requests.json.

| Priority | Conflicting locations | Owning source and decision | Repair | Resolution check |
|---|---|---|---|---|
| P2 — Local revision | Abstract sentence 3 reports nine; Results paragraph 4 and Fig. 3 legend report eight. | Designated source table v3 lists A–H as eight active compounds and excludes PC. Old v2 included PC among nine. | Change the Abstract count to eight. Keep the matching Results and legend counts. | All three manuscript locations report eight active compounds, matching A–H in source table v3; PC remains identified as the excluded positive control. |

No timestamp is needed to resolve this discrepancy: the source set explicitly designates v3. No unresolved count remains within the supplied record.

## CITATION-01 — Claim-to-source audit

This audit covers all four cited manuscript statements in the supplied fictional record. I2 contains two distinct propositions, giving **five claim–source relationships**. Source locators below refer to the CITATION-01 entry in [requests.json](../writing-regression-cases.json). Access consists of the supplied source excerpts, identity notes and complete simulated status record, checked **2026-11-10**.

| Claim ID / manuscript location | Exact claim | Source ID and version | Source locator | Access level | Identity check | Support verdict | Source status and date | Reason | Targeted repair |
|---|---|---|---|---|---|---|---|---|---|
| I1 | A improves survival in all patients. | S1; supplied version | S1, Results paragraph 2 | Supplied Results excerpt | Bibliography and source header agree on title, authors, year and local ID | Scope mismatch | No notices in simulated record; 2026-11-10 | S1 reports an association with longer progression-free survival in a biomarker-selected cohort. The claim changes the population, broadens the endpoint and strengthens association to improvement caused by A. | State: “A was associated with longer progression-free survival in a biomarker-selected cohort [S1].” |
| I2a, component of I2 | A binds receptor R directly. | S2; supplied version | S2, Fig. 2 legend | Supplied legend and explicit measurement note | Bibliography and source header agree on title, authors, year and local ID | Unsupported | No notices in simulated record; 2026-11-10 | Direct binding was not measured in the supplied source record. | Remove the direct-binding component. A direct-binding claim would need an accessible source that measures that relationship. |
| I2b, component of I2 | A suppresses reporter Q. | S2; supplied version | S2, Fig. 2 legend | Supplied legend | Bibliography and source header agree on title, authors, year and local ID | Supported | No notices in simulated record; 2026-11-10 | The legend reports suppression of the Q reporter by A. | Retain this component with S2: “A suppresses reporter Q [S2].” |
| I3 | B is safe at every dose. | S3; content/version inaccessible | S3 content unavailable; identity metadata and status-access note supplied | Metadata only; content inaccessible | Identity metadata supplied; match to source content/header unverified | Unverified | Status unavailable; recorded 2026-11-10 | No accessible evidence supports a decision about safety or the universal dose claim. | Obtain the relevant dose and safety results and source-status record before retaining the claim. Leave this entry unresolved; no substitute safety statement can be derived from the supplied evidence. |
| I4 | C reduces colony number by 20%. | S4; corrected version | S4, corrected Table 1; simulated correction record | Supplied corrected table result and correction note | Bibliography and source header agree on title, authors, year and local ID | Contradicted | Correction replaces 20% with 12% in Table 1; 2026-11-10 | The corrected source gives a 12% reduction. The correction directly changes the cited numerical result. | Change 20% to 12% and use the corrected S4 record. |

**Coverage:** Four of four cited manuscript statements are included. Five of five claim–source relationships have audit entries: one Supported, one Scope mismatch, one Unsupported, one Contradicted and one Unverified. Support decisions are resolved for four relationships; I3 remains unresolved. Identity agreement is documented for S1, S2 and S4. S3 identity verification, support and status remain open. The main repairs are to align I1 with its selected cohort and progression-free-survival endpoint, remove I2's direct-binding claim, and apply S4's corrected 12% result.

## Resources actually read

- `../writing-regression-cases.json`
- `skills/paper-polishing/SKILL.md`
- `skills/paper-review/SKILL.md`
- `skills/citation-audit/SKILL.md`
- `skills/biomed-shared/writing-principles.md`
- `skills/biomed-shared/revision-fidelity.md`
- `skills/biomed-shared/terminology-and-citations.md`
- `skills/biomed-shared/paragraphs-and-revision.md`
- `skills/biomed-shared/argument-bridges.md`
- `skills/biomed-shared/evidence-and-interpretation.md`
- `skills/biomed-shared/scientific-semantics.md`
- `skills/biomed-shared/section-responsibilities.md`
- `skills/biomed-shared/biomedical-examples.md`

All seven requested tasks were completed at the supplied-evidence scope. The unresolved S3 audit entry is recorded above.

## Targeted retest

# BRIDGE-01 — Minimal polishing retest

In early studies, agent A’s plasma payload release was linked to dose-limiting marrow suppression; plasma-stable agent B’s uptake by antigen-positive normal epithelium was linked to dose-limiting epithelial injury. These findings implicate release and target biology in tolerability.

**Consequential notes:** Source A, Results paragraph 2, links plasma payload release to marrow suppression; Source B, Results paragraph 4, links uptake of the payload-retaining agent by antigen-positive normal epithelium to epithelial injury. The conclusion now covers release and target biology. The repeated topic sentence and separate injury list were integrated into the examples. The passage grows from 31 to 37 words (19.4%). All agents and sources are fictional; only the supplied notes were used.

## Resources read

- `../writing-regression-cases.json`
- `skills/paper-polishing/SKILL.md`
- `skills/biomed-shared/writing-principles.md`
- `skills/biomed-shared/revision-fidelity.md`
- `skills/biomed-shared/terminology-and-citations.md`
- `skills/biomed-shared/paragraphs-and-revision.md`
- `skills/biomed-shared/argument-bridges.md`
- `skills/biomed-shared/evidence-and-interpretation.md`
- `skills/biomed-shared/scientific-semantics.md`

## Five additional outputs

# Additional biomedical writing tasks

All evidence is fictional and comes only from [remaining-requests.json](../writing-regression-cases.json). The tasks below are independent. No external sources were consulted.

## BRIDGE-02 — Review transition

Therapy-induced lineage change rewires transcription and chromatin and changes the surface antigens available for drug delivery. Lineage-switched cells lose antigen L and acquire antigen N (Source C, Fig. 2 and Results paragraph 3). An N-directed conjugate enters N-positive cells and inhibits their growth in culture (Source D, Fig. 4), supporting a strategy to redirect delivery toward the lineage-switched state.

**Consequential choice:** The transition now links lineage change to altered surface targeting and then to conjugate uptake and growth inhibition. The therapeutic opportunity is stated as a strategy supported by the culture results.

## CONTROL-02 — Local polishing

Although treatment A significantly reduced colony number relative to vehicle in six donor-matched cultures (paired t-test, P = 0.004), treatment B preserved colony number while reducing colony area, indicating distinct effects on colony establishment and expansion under these conditions.

Retained unchanged. The connected comparison, statistical significance, matching, sample size and assay endpoints remain explicit.

## CONCEPT-01 — Scientific terminology

Drug A reduced X and Y transcript abundance. Dosing lasted 24 h rather than 48 h; pathway dependence was not tested.

**Consequential edits:** The qPCR endpoint is transcript abundance. The time change concerns dosing duration. The supplied measurements support these statements; systemic drug concentration was unmeasured, and the claim that pathway dependence was eliminated has been replaced with its actual assay status.

## CITATION-02 — Citation audit

**Scope:** The one sentence in manuscript Results paragraph 2 is split into two propositions: C2a, the study-level response finding, and C2b, the number of patients per study. R is the cited review; its empirical attribution is traced to the supplied primary-study records P1–P3. The source locators below refer to the CITATION-02 entry in remaining-requests.json. Source headers match the cited identities. Access is to the supplied fictional source records for this exercise. Versions and publisher status notices were not supplied; current source status remains unverified for all four sources. No status lookup was performed.

| Claim ID / location | Exact claim component | Source ID and version | Source locator | Access level | Identity check | Support verdict | Source status / check date | Reason | Targeted repair |
|---|---|---|---|---|---|---|---|---|---|
| C2a / Results paragraph 2 | “Across three independent studies, A increased response” | R; version unspecified | R, paragraph 5 | Supplied review record | Source header matches cited identity | Partial | Unverified; no external check | R identifies three primary studies and their response findings. The supplied record does not establish independence of the study cohorts. | Attribute the finding to three studies and cite the inspected primary sources. |
| C2a / Results paragraph 2 | “Across three independent studies, A increased response” — P1 contribution | P1; version unspecified | P1, Table 1 and supplied response finding | Supplied primary-study record | Source header matches cited identity | Supported for P1's contribution | Unverified; no external check | P1 reports increased response in its cohort. It supplies one of the three study findings. | Retain the P1 result at its own cohort scope. |
| C2a / Results paragraph 2 | “Across three independent studies, A increased response” — P2 contribution | P2; version unspecified | P2, Table 1 and supplied response finding | Supplied primary-study record | Source header matches cited identity | Supported for P2's contribution | Unverified; no external check | P2 reports increased response in its cohort. It supplies one of the three study findings. | Retain the P2 result at its own cohort scope. |
| C2a / Results paragraph 2 | “Across three independent studies, A increased response” — P3 contribution | P3; version unspecified | P3, Table 1 and supplied response finding | Supplied primary-study record | Source header matches cited identity | Supported for P3's contribution | Unverified; no external check | P3 reports increased response in its cohort. It supplies one of the three study findings. | Retain the P3 result at its own cohort scope. |
| C2b / Results paragraph 2 | “900 patients per study” | R; version unspecified | R, paragraph 5 | Supplied review record | Source header matches cited identity | Contradicted | Unverified; no external check | R gives 900 patients in total across the three studies. | Replace the per-study denominator with the total and the separate cohort sizes. |
| C2b / Results paragraph 2 | “900 patients per study” — P1 | P1; version unspecified | P1, Table 1 | Supplied primary-study record | Source header matches cited identity | Contradicted | Unverified; no external check | P1 reports n = 200. | Give P1's cohort as 200 patients. |
| C2b / Results paragraph 2 | “900 patients per study” — P2 | P2; version unspecified | P2, Table 1 | Supplied primary-study record | Source header matches cited identity | Contradicted | Unverified; no external check | P2 reports n = 300. | Give P2's cohort as 300 patients. |
| C2b / Results paragraph 2 | “900 patients per study” — P3 | P3; version unspecified | P3, Table 1 | Supplied primary-study record | Source header matches cited identity | Contradicted | Unverified; no external check | P3 reports n = 400. | Give P3's cohort as 400 patients. |

**Targeted sentence repair:** Three studies reported increased response to A, with 900 patients in total (P1, n = 200; P2, n = 300; P3, n = 400) [P1–P3].

The replacement citations have been checked against the supplied primary-source records. The corrected sentence keeps the response claim at study-cohort level and uses the review's total consistently with the primary-study counts.

**Coverage:** One cited sentence, two component propositions and eight source relationships are included. Three relationships support the individual primary-study response findings; one is partial because cohort independence is unspecified; four contradict the per-study denominator. The numerical discrepancy is resolved: 200 + 300 + 400 = 900 in total. Independence and the four sources' current status remain unverified.

## STORY-01 — Framing brief

### Central contribution

A transient exposure establishes a persistent organoid state that changes sensitivity to a later challenge.

**Illustrative title:** Organoids retain a functional memory of transient exposure

### Scientific significance

Exposure history becomes a determinant of future sensitivity. The persistence result gives the state a temporal dimension; the later-challenge result gives it a functional consequence. Together, they support a view of treatment response in which a transient intervention can continue to shape how organoids respond after washout. This makes the sequence and timing of exposure biologically meaningful variables for treatment design.

### Recommended story and model

Lead with functional memory of exposure. The established chain is transient exposure → a state that persists after washout → altered sensitivity to a later challenge. We propose that this state carries a form of cellular memory that connects past exposure to future response. The open mechanistic question is which molecular features store that state. The central contribution is complete enough to frame around the observed persistence and changed challenge sensitivity using the existing experiments.

### Claims and figures

The figure roles below are proposed; the supplied notes give no existing figure or panel IDs.

| Claim | Scientific question | Decisive supplied evidence | Inference | Proposed figure role |
|---|---|---|---|---|
| S1 | Does the exposure-induced state outlast exposure? | STORY-01: transient exposure creates a state that persists after washout | The treatment history leaves a persistent biological state | Open the main sequence with exposure, washout and persistence; include the compact assay controls needed to assess the result. |
| S2 | Does the retained state change a later response? | STORY-01: the state changes sensitivity to a later challenge | Persistence has a functional consequence for future sensitivity | Follow with the later-challenge response, making the temporal connection to S1 explicit. |
| S3 | Are the assay measurements technically reliable? | STORY-01: screen and reporter are technically reproducible | The measurements provide a reliable basis for the biological findings | Keep essential controls beside S1–S2; place extended assay-performance material in Methods or supplementary figures. |

### Editorial decisions

Move persistence and challenge response to the front of the main figure sequence. Compress the two opening assay-performance figures around the controls needed to interpret those discoveries, and move the remaining technical support to Methods or supplementary material. The story can be completed with the current data. Keep molecular storage as the specific question opened by the functional-memory model.

## Resources read

- `../writing-regression-cases.json`
- `skills/paper-writing/SKILL.md`
- `skills/paper-polishing/SKILL.md`
- `skills/citation-audit/SKILL.md`
- `skills/paper-framing/SKILL.md`
- `skills/paper-framing/assets/framing-brief.md`
- `skills/biomed-shared/writing-principles.md`
- `skills/biomed-shared/revision-fidelity.md`
- `skills/biomed-shared/terminology-and-citations.md`
- `skills/biomed-shared/paragraphs-and-revision.md`
- `skills/biomed-shared/argument-bridges.md`
- `skills/biomed-shared/evidence-and-interpretation.md`
- `skills/biomed-shared/scientific-semantics.md`
- `skills/biomed-shared/logic-review.md`
- `skills/biomed-shared/main-text-and-supplement.md`
- `skills/biomed-shared/biomedical-examples.md`

All five requested outputs were completed using the supplied evidence. The unresolved citation-audit entries are identified above.
