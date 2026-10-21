# Pilot protocol: fewer errors and less manual repair

**Status: proposed experiment. No pilot dataset has been collected or trained.**

## Question

Does access to reviewed visual motifs and explicit geometry repair reduce errors
and manual work when generating new biomedical schematics and animations?

Run a first study with the current generation model fixed. This tests the proposed
representation and example retrieval separately from model weight training. The
research rationale and primary sources are in `../docs/future-learning-roadmap.md`.

## Collection

Target about 200 schematic panels from at least 100 papers and 50 reviewed
editable icons or motifs. These are planning targets, not power calculations or
guaranteed training requirements. Cover membrane signaling, transcription and
chromatin, immune interactions, experimental/tissue workflows, and transport.
Include a range of label lengths, viewing sizes, aspect ratios, and densities.
Use source-qualified scientific evidence and a separate record of visual rights.

Record why each positive example is useful. Keep deliberately difficult valid
contacts, weaves, and crossings to test whether the system wrongly forbids them.
Set aside raw images, captions, relevant source passages, editable source when
available, source hashes, and licenses. Record reconstructed areas explicitly.
Do not equate a later paper version with an improved drawing without review.

## Splits and leakage prevention

Build groups using paper/version families, shared template families, and near-
duplicate artwork. Assign groups to approximately 70% development, 15% validation,
and 15% locked test. Group integrity takes priority over exact proportions.

All crops, restyled variants, corruptions, and revisions from one group remain in
that group. Assign groups before generating synthetic data. Retrieval for a test
request can use approved development examples, but cannot use its own target,
related versions, or near duplicates. Freeze a split manifest with random seed and
hashes. Report contamination that cannot be excluded, including a base model's
unknown pretraining overlap. Add original held-out scenes as a complementary test.

## Candidate tasks

Use the same input for each system: manuscript evidence, requested meaning,
available assets, and output dimensions. Evaluate three task types independently:
new static composition, local repair, and motion on an existing reviewed figure.
For paper explanation, also evaluate the choice of claims and comparisons before
testing the rendering.

Suggested local repairs include channel-axis displacement, excess ion diameter,
reversed part order, missing DNA depth treatment, nested viewport clipping,
incorrect binding anchor, external-label collision, and ungrouped moving labels.
Confirm the visibility and category of every generated defect. Synthetic positives
must include correct intentional overlaps.

## Systems

| ID | System | What the comparison estimates |
|---|---|---|
| A | Current v2.2 instructions and renderer | Baseline. |
| B | A plus retrieval of reviewed motif cards | Benefit of relevant examples. |
| C | B plus reusable constraint repair operations | Benefit of formal scene representation and repair. |
| D | C plus validation-selected skill updates | Benefit of instruction/recipe learning. |
| E | C plus a trained defect ranker or patch model | Optional benefit of neural training. |

Separate D and E initially so their effects can be attributed. Hold model version,
asset pool, output size, rendering environment, and allowed review budget constant.
Record all prompts, selected references, iterations, tool calls, and corrections.

## Outcomes

Use per-figure and per-scene outcomes. Many assertions on one icon are not many
independent examples. A sampled frame count is not a count of independent videos.

| Outcome | Proposed measurement |
|---|---|
| Critical biological errors | Fraction of figures with incorrect entity, compartment, direction, stoichiometry when asserted, or unsupported causal/temporal claim. |
| Visible defects | Fraction with clipping, unreadable label, unintended crossing, ambiguous declared occlusion, or wrong contact. Report defect types and objects. |
| Request completion | Fraction of requested edits completed without breaking an active earlier requirement. |
| Manual effort | Reviewer correction time and number/type of manual edits per accepted figure. Record full distributions. |
| Readability/style | Blinded pairwise preference at intended display size, with ties and reasons. Match scientific content before comparing style. |
| Retrieval | Recall@k of a reviewed suitable motif, plus a rating of morphology, view, and rights suitability. |
| Animation | Errors per scene and event: contact/compartment failures, label detachment, identity loss, collisions, or unsupported kinetics. |
| Editability | Retained native text, stable semantic groups and ability to move a named object with its label. |

Use two independent perspectives in visual review: a biologist and someone with
scientific illustration experience. Mask the system identity. Use an adjudicated
scientific checklist and record disagreement instead of folding it into a global
score. General aesthetic embeddings or a VLM critic may assist review; human
assessment calibrates their use on this task.

For uncertainty, resample or summarize at the independent paper/group level.
Avoid treating frame counts or many synthetic derivatives as independent sample
sizes. Report paired comparisons on identical inputs and show failure examples.

## Candidate acceptance

Select candidate instructions and models on validation data only. A promotion
requires a reduction in relevant defects or manual work without an observed
increase in critical biological errors, and passing the existing regression suite.
Any critical defect in the reviewed validation cases requires inspection before
promotion. Define the target improvement before testing; determine a larger study
size using pilot variability rather than inventing a guaranteed sample count.

After choosing a candidate, run the locked test once. Publish or retain both
successful and failed examples with their source scope and permissions. A zero
observed failure count is a property of that finite test set, not a proof of
universal correctness.

## Learning cycle

A proposal cycle records: current version, development cases, traces, local patches,
validation measurements, accept/reject decision, and reason. Preserve the last
accepted version. Do not automatically promote user-unreviewed fixes to the gold
corpus. Keep retrospective tests that exposed earlier blind spots.

Only start weight adaptation after identifying a repeatable remaining defect or
cost. Use learning curves, frozen-model baselines, and controlled ablations to
choose training scale. Log model/license versions and hardware compatibility when
an actual model is selected.
