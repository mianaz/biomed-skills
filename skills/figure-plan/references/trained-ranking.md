# Train or use a layout ranker

A small ranker can select among existing layouts. Keep candidate generation,
biological reasoning, source repair and figure acceptance as separate steps.
Use the [R prototype](../../../prototypes/figure-layout-ranker/README.md) when a
pairwise linear model is sufficient. The model consumes a feature table; it does
not assemble or render figures.

## Freeze the study

Split papers before fitting. Freeze the panel assets, evidence groups, candidate
pool, comparator, feature definitions and evaluation endpoints. Give all
selectors the same candidates. Keep the original figure outside their inputs.
State which parts of the input were annotated by someone who saw the reference.
Paper-disjoint tests do not certify absence from model pretraining or reused data.

Audit source crops before labeling. Give every selector the same factual input
packet: dimensions, evidence groups, measured font profiles and unknown text
coverage. A comparator that sees only images has different information from a
ranker using exact font measurements. Preserve an input defect if found after
freezing; label its correction as a supplemental run on reused test papers.

Include figure width and height in candidate generation. A fixed-size experiment
tests selection only at that size. Save width, height, final font scale, the
content envelope and internal spacing separately. Crop the same layout without
scaling as a diagnostic control for canvas-induced whitespace. Learned size
priors must use training papers only; record published geometry separately from
the unavailable authoring canvas. Repeated layouts from one paper do not replace
independent papers, and geometry measurements do not add preference labels.

Identify the label source: human preference, visual LLM weak preference, or a
mechanical rule. Keep them separate. A model trained on a rule learns that rule;
neither its score nor visual LLM agreement establishes human aesthetic quality.
Retain ties and the original reasons. Preserve rejected and failed layouts.

**Done:** every candidate and label has a paper ID, provenance and an assigned
split; no held-out preference enters model fitting or hyperparameter selection.

## Fit and compare

Start with a pairwise linear model and paper-level cross-validation. Fit feature
normalization within each training fold. Save the weights, normalizer, feature
definitions, raw labels and held-out predictions. A small file alone says
nothing about the quality of its preferences.

Compare selected outputs with a fixed rule and the frozen figure-plan condition.
Randomize method identity and left/right position for visual review. Include
reversed-position repeats and identical-layout controls. Report paper-level
outcomes, disagreement and failures. Label repeated sessions of the same model
as model judgments, including any shared teacher/selector/judge family.

Keep integrity, readability and preference separate. A relative preference can
favor a layout that still fails the font floor. Preserve unknown measurements
as unknown. If all candidates are inadequate, improve the source panels or
candidate pool in a new development version and test on fresh papers.

Report pair-label prediction and selected-layout comparisons separately. Better
pairwise agreement need not produce better final figures. Plot actual fits over
nested training-paper subsets, with test-paper uncertainty and all failures.
Do not choose a training size or rewrite a threshold from the test curve.

**Done:** the comparison includes every held-out paper, all failed controls and
readability failures, and a clear statement of what was not tested.

## Use the result

Treat the ranker as a suggestion until its selected figure passes rendered
review. Inspect dense labels and complex comparisons next to simple panels.
Scalar area, font and adjacency summaries can favor an oversized simple panel.
Use plot-reading tasks and human pair labels to test that failure directly.

An initial 10-training/4-test-paper pilot fixed every candidate to 180 × 180 mm.
Its fill features mixed canvas choice with placement quality. A later study
used 39 admitted training papers, six new test papers and size-varying layouts.
Twenty weights learned from 234 visual LLM weak pairs. Across 25 actual fits,
test-pair agreement rose from 76.7% at five training papers to 88.9% at 39, but
log loss stopped improving consistently after about 20. Final selections had
two wins, two losses and two identical ties against the rule. No selected
figure passed the declared typography checks. More samples improved this
prediction endpoint without establishing better accepted figures.

Both studies exposed oversized simple panels beside small dense comparisons.
The later study also found an input-parity defect and retained a separately
labeled corrected comparison on the same six papers. These weights remain
optional research support, with no human aesthetic validation. Repair source
typography and broaden the candidate pool before testing the next version.

**Done:** the selected figure has a separate review decision. Changes learned
from a test case enter development; the frozen test result remains unchanged.
