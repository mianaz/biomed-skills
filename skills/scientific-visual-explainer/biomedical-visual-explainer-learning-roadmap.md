# Learning better biomedical illustration from papers and corrections

**Proposal for Scientific Visual Explainer · October 14, 2026**

## 1. Starting point and intended result

The available v2.2 package implements editable SVG scenes, a 15-object starter
library, asset registration, label fitting, animation playback, and checks for
specified geometry and interaction conditions. The host agent reads the scientific
material and authors the scene. Its raster route animates focus regions; it does
not recover an arbitrary raster figure's complete object structure.

The original skill already requires evidence locations, a distinction between
scientific and visual references, and review of actual rendered output. Keep those
requirements when adding learning. The new objective is to make fewer corrective
edits necessary and to make improvements generalize to unfamiliar structures.
See `../archive/SKILL.original.md`, `../SKILL.md`, and `qc-report.md` for the source
requirements and the documented current implementation.

I recommend a combination of a richer graphics representation, retrieved examples,
and learning from reviewed corrections. Use neural training for a measured
bottleneck after establishing the baseline. The proposals and numerical pilot
sizes below are design choices; they are not results from a completed experiment.

## 2. Improve representation and repair before increasing generation complexity

Represent biological statements, visual placement, and occlusion explicitly:

| Representation | What it should record | Example |
|---|---|---|
| Biological graph | Entity identity, compartment, state, stoichiometry when established, relation type, evidence locator | A ligand binds the extracellular domain of a receptor. |
| Visual graph | Asset and part IDs, label ownership, contact anchors, alignment references, intended projection | A short label belongs inside the kinase domain. |
| Occlusion graph | Which drawable part covers which other part, joins, containment, and crossings without contact | Rear DNA is covered by the core; front DNA covers the core. |
| Animation model | Stable identities, state changes, permitted motion, presentation timing, source of temporal claims | An ion follows the pore axis in an illustrative transport demonstration. |

The v2.2 skill specifies several of these ideas and checks selected motifs. The
next implementation should make them reusable across asset types and return
localized repair actions, rather than only pass/fail checks.

Use a directed acyclic order of drawable parts for occlusion. An alternating weave
cannot generally be represented by a single global ordering of two whole objects:
split the paths into front and rear segments. Detect cycles and request a part
split rather than choosing an arbitrary paint order. A crossing must declare
whether it represents a junction, a projection of separate objects, or an error.
Represent the channel's permeable region explicitly and keep membrane tiles out
of it. Record intentional physical contact separately from accidental overlap.

Compute bounds after transformation and include stroke width, caps, joins,
arrowheads, text, and nested SVG clipping. Check the actual rendered result after
applying masks and clipping paths. Keep transparent backgrounds in the test set:
painting a white patch over a crossing can conceal a problem on one background.
Perform collision checks between relevant subparts, with exceptions tied to exact
relationships and time windows. Test labels and relation endpoints as a group.

For layout, keep hard constraints for required containment, readable labels,
valid contact endpoints, and biological relations. Optimize soft preferences such
as balance, spacing, connector bends, and compactness only within the feasible
set. Give an infeasible layout a concrete explanation. Allow enlargement, a
changed arrangement, or a different asset before reducing text to an unreadable
size. An optimizer still needs independent rendering checks.

Penrose's explicit separation of domain, relationships, and style is a useful
architectural reference for compiling diagram specifications into constraints [S7].
SBGN provides defined biological relation semantics and complementary views of
biological systems; selectively map appropriate relations into the internal graph
while retaining the desired rounded illustration style [S8]. Neither reference
supplies a complete biomedical animation system for this package.

Define repair operations such as `align_to_anchor`, `expand_viewport`,
`reroute_connector`, `split_rear_path`, `reorder_parts`, and `resize_label_container`.
An agent proposes a small patch; the renderer applies it; tests check the corrected
area and the rest of the scene. Preserve an explicit record of all active user
requirements so a later change can be tested against earlier requests.

## 3. What to learn from published papers

Use three kinds of information from each selected figure.

**Scientific content.** Record the biological objects, experimental conditions,
comparisons, and claim supported by each relevant panel. Link the panel to its
caption and the specific Results or Methods passage. Record a proposed model as a
proposed model. An illustrative mechanism panel is not independent evidence for
every reaction drawn in it.

**Visual construction.** Record the reusable solution: how a receptor joins a
membrane, how a nucleosome shows front and rear DNA, how a complex keeps its
members distinguishable, how labels occupy a curved shape, and how a connector
avoids unrelated objects. Preserve the actual reference crop for authorized uses.
Extract a structural recipe that can be applied to a new biological scene.

**Explanatory sequence.** Record the question the visual addresses, the comparison
that resolves it, and the minimum set of visual changes needed to explain it.
A static arrangement supplies no measured trajectory or kinetic rate. Add temporal
claims only from suitable experimental evidence, authorized supplementary videos,
or explicit author input; mark pedagogical sequencing as illustrative.

The original skill already separates scientific and visual references. The
proposed annotation format keeps that distinction in `scientific_evidence` and
`visual_provenance`, and adds review status for both.

### Build a small, useful collection first

For a pilot, target about **200 carefully reviewed schematic panels from at least
100 papers**, covering membrane signaling, transcription/chromatin, immune cell
interactions, tissue or experimental workflows, and transport or organelle
processes. Include dense examples and legitimate overlaps. This is an annotation
and retrieval pilot, not a claimed sufficient sample size for training a general
figure generator. Broader paper coverage needs further categories and evaluation.

For each record, keep a paper/version ID, DOI or PMCID where available, panel ID,
caption, relevant text passage, source location, asset license, third-party credit,
raw file checksum, derivative history, type of visual, graph annotation, and human
review status. Native SVG or an author's editable source is particularly useful
for part boundaries and ordering. When only a raster exists, annotate visible
parts and uncertainty; do not pretend that an occluded contour is observed.

Use PMC's approved automated services for permitted content. Its Open Access
Subset includes material with differing licenses, and freely readable articles
are not uniformly available for reuse. Individual figures can contain third-party
material even inside an open article [S5, S6]. For a maintainable public dataset,
record separate decisions for reference viewing, model training, adaptation, and
redistribution. Require a documented basis for each intended use. Treat uncertain
rights as pending review rather than inferring permission from a citation. This
is a conservative project policy; ambiguous rights require appropriate review.

Prefer native XML/HTML captions and downloadable figure assets when available.
Split compound figures into panels and link each crop to the correct caption
segment. Filter microscopy, photographs, and plots into their own categories so
the schematic retrieval set is not dominated by unrelated image types. Review
text extracted by any automated parser against the actual source.

Published quality is a selection signal, not a gold label. Review whether a
figure's graphical relationships are understandable and whether its claims
follow from the accompanying text. Select examples for a specific reason and
record that reason. Keep weak examples as labeled negatives only when useful.

## 4. A staged learning strategy

### A. Retrieve reviewed examples with an existing model

Build an index over panel crops, captions, entity names, motif descriptions,
structure tags, and rights metadata. Query it with the desired biological
relationship and view. Apply rights, species, compartment, and motif filters, then
rank candidates using text and image similarity. Let an independent review step
select a small set of complementary examples.

BiomedCLIP is a concrete candidate for the image/text encoder: its primary paper
reports biomedical retrieval and other tasks after training on figure-caption
pairs [S4]. Benchmark it on schematic-specific retrieval. A high semantic match
does not certify drawing quality, exact molecular identity, or topological
correctness. Compare it with a simple keyword/caption baseline and another
available visual embedding model on the same reviewed queries.

Store a compact reference card with the selected figure, reusable recipe, active
license decisions, and example of a known failure. This improves the information
available at generation time without changing any model weights. Persistent
reference cards and reviewed rules are one practical meaning of learning.

### B. Learn the skill from execution traces and corrections

Save a complete edit record whenever a figure is corrected: before SVG/scene and
render, request, localized defect, proposed patch, after SVG/scene and render,
regression tests, reviewers, and acceptance. Keep user feedback and inferred
intent distinct. An author's later version may contain a new scientific claim;
that change must not automatically become a style preference.

SciDiagramEdit studies before/after paper revisions and evolves an SVG editing
agent's skill specification from execution traces and reference revisions [S1].
This motivates proposing small updates to this package's rules and examples,
then evaluating them on held-out figures. Its dataset emphasizes general
scientific diagrams, so transfer to biological icons needs its own benchmark.

Keep the generation model fixed initially. Let a separate process propose changes
to a concise instruction, motif recipe, or test. Score the candidate on validation
figures and preserve the best verified version. Keep the final test set untouched.
Skill evolution is an optimization of the agent's instructions and tools; it is
different from neural weight training.

PaperBanana-Interact reports quality drift and loss of earlier requirements during
iterative diagram editing, and uses a critic with accumulated interaction memory
[S2]. For this skill, keep explicit requirement IDs and test every new patch
against the active requirement record.

### C. Train a defect detector and ranker

If review or candidate selection remains a measured bottleneck, train a model to
predict localized defect categories. Suitable labels include ambiguous occlusion,
unintended crossing, clipped painted extent, wrong anchor, misplaced label,
incorrect compartment, missing/extra component, and unsupported motion.

Create synthetic negatives from reviewed valid scenes: displace an ion, remove a
rear-path gap, swap paint order, shrink a viewBox, move a label, or detach one
member of a moving complex. Preserve valid overlap examples. Verify that a
perturbation actually introduces the intended visible error; random changes do
not always make a figure incorrect. Add difficult real corrections, not just
synthetic defects with easily detected artifacts.

Use a frozen image/text encoder plus a small classifier as a first trained
baseline. Add pairwise ranking on biologically equivalent alternatives where
reviewers prefer one composition. A possible preference objective is
`-log sigmoid(score(accepted) - score(rejected))`. This is a proposed loss, not a
trained component in v2.2. Use the ranker after semantic and geometry checks so
attractiveness cannot compensate for a false biological relationship. Measure
calibration and false negatives, particularly on genuine contacts and crossings.

### D. Fine-tune an agent to produce repairs or scene descriptions

Once there are enough reviewed examples to measure a learning curve, train on
`(current scene, render, request, evidence) -> reviewed patch`. A second task can
map an evidence graph and selected assets to a structured scene. Parameter
adaptation such as LoRA is an experiment to consider; required data volume and
hardware depend on the selected model and cannot be inferred from the package.

Constrain targets to an explicit patch or scene schema, canonicalize IDs and
coordinates, and render every predicted patch. Training should cover both a
correct change and preservation of other active requirements. Do not use an SVG
string's token match as the sole measure of success: equivalent geometry can have
many different serializations.

### E. Evaluate a dedicated vector generator only when needed

StarVector offers an existing approach to generating SVG code from images or
text, with compact primitives rather than only traced curves [S9]. It is a
candidate for missing simple assets or reconstruction experiments. Evaluate its
actual released checkpoint on the intended icon types and inspect its limits.
A generic SVG benchmark does not establish biomedical anatomy or mechanism
accuracy.

The proposed training target for a specialized biomedical generator is an editable
asset with named parts, anchors, safe label regions, and an occlusion specification.
Use image appearance together with geometry and semantic supervision. A raster
style adapter can be evaluated for optional illustration drafts, but its output
still needs an editable and reviewed representation before object animation.

## 5. Animation needs its own supervision

A static SVG often fragments a recognizable biological object into multiple paths.
Assign semantic part groups before motion and attach labels and relevant marks
to the correct moving parent. Vector Prism explicitly studies semantic grouping
for SVG animation; the abstract is the scope reviewed for that source [S10].

Build motion examples around explicit state transitions: binding, dissociation,
recruitment, transport, localization, or reveal of a comparison. Distinguish a
visual entrance from a physical event. Preserve identity and test anchor alignment,
pore clearance, contacts, compartment boundaries, and label attachment throughout
the transition. Verify only the stoichiometric claims the scene is intended to
make; symbolic population illustrations may not represent individual molecule
counts.

For a flattened figure, prioritize focus/reveal and translation of genuinely
separated regions. Record segmentation uncertainty and inspection of any newly
exposed background. Fully occluded structure cannot be recovered uniquely from a
single image. Where the scientific question needs that structure, retrieve a
suitable independent source or request author input.

## 6. Evaluate improvements at the level of the user's goal

The current motif tests should remain a regression suite. Add a held-out set of
new icons, new multi-object scenes, and new static-to-animation tasks. Group data
by paper, version family, duplicated artwork, and template family before splitting.
Create augmentations only after assigning their source groups. Otherwise variants
of one figure could enter both training and test sets.

Report several outcomes rather than averaging everything into one aesthetic
score. Separate biological errors, visible defects, edit success, animation
continuity, and human effort. Show the number of affected figures as well as the
number of test assertions. Sample animation around events, fast motion, and
narrow clearances; the existing sampled checks do not cover continuous time.

Use blind pairwise comparisons at the intended display size with scientific and
illustration review. Report both review perspectives, allow ties, and retain
reasons for disagreement. Require the same biological content for a fair style
comparison. A beautifully simplified but scientifically incomplete figure is not
an equivalent candidate.

The proposed pilot compares:

1. The current v2.2 package.
2. v2.2 plus reviewed motif retrieval.
3. Retrieval plus systematic constraint repair.
4. The preceding system with evolved skill instructions or a learned defect ranker.

Add weight fine-tuning only when those comparisons identify a remaining problem.
Keep rendering settings, model version, task inputs, and review budget controlled.
Report manual edits and reviewer time alongside accuracy. See
`../learning/pilot-protocol.md` for the runnable-study specification and promotion
rules.

## 7. Development order

| Stage | Deliverable | Evidence required to proceed |
|---|---|---|
| Reusable geometry | General part/occlusion schema, anchor repair, contour-aware routing, rendering checks | New unseen assets obey declared relations without special-case patching. |
| Reference collection | Reviewed panels, licenses, captions, structured recipes, retrieval baseline | Relevant and drawable references are found for held-out scene requests. |
| Correction history | Before/after artifacts, localized errors, active requirements, human decisions | Repaired examples are reproducible and correctly labeled. |
| Skill evolution | Small instruction/recipe updates tested against a validation suite | Improvement repeats across unseen papers without regression on known cases. |
| Targeted neural training | Defect ranker or patch model with controlled ablations | A measurable gain over the frozen-model and retrieval baselines. |
| Broader animation | Reviewed semantic groups and source-qualified transition examples | Motion preserves the intended biology and previously satisfied constraints. |

My first development priorities are the reusable geometry and reference collection.
The correction history should be recorded from the start. That produces useful
supervision for both instruction learning and later model training.

## Sources and reading scope

The sources below were checked on October 14, 2026. Research systems were reviewed
from primary text and project documentation; none was installed or benchmarked in
this packaging task. Preprint findings remain the authors' reported results.
This document proposes adaptations and does not claim that these methods have
already improved the bundled biomedical skill.

- **[S1] SciDiagramEdit: Learning to Edit Scientific Diagrams from Paper Revisions.**
  Sun et al., arXiv:2607.15272v1, July 16, 2026. Reviewed HTML introduction, dataset,
  methodology, and validation strategy. https://arxiv.org/html/2607.15272v1
- **[S2] PaperBanana-Interact: Scientific Diagram Refinement with Multi-Turn Human Feedback.**
  Wu et al., arXiv:2608.30241, August 31, 2026. Reviewed abstract and author project
  page; full PDF was not reviewed. https://arxiv.org/abs/2608.30241 and
  https://shirley-wu.github.io/PaperBanana-Interact/
- **[S3] PaperBanana: Automating Academic Illustration for AI Scientists.**
  Zhu et al., arXiv:2601.23265v1, January 30, 2026. Reviewed HTML framework and
  benchmark scope. Its methodology-diagram benchmark is based on NeurIPS papers.
  https://arxiv.org/html/2601.23265v1
- **[S4] BiomedCLIP: a multimodal biomedical foundation model pretrained from fifteen million scientific image-text pairs.**
  Zhang et al., arXiv:2303.00915, HTML v3. Reviewed abstract and retrieval/method
  sections. https://arxiv.org/html/2303.00915v3
- **[S5] NLM/PMC Open Access Subset.** Reviewed retrieval and terms-of-use guidance.
  https://pmc.ncbi.nlm.nih.gov/tools/openftlist/
- **[S6] NLM/PMC Copyright Notice.** Reviewed reuse and third-party illustration
  provisions. https://pmc.ncbi.nlm.nih.gov/about/copyright/
- **[S7] Penrose reference documentation.** Reviewed domain/substance/style
  separation and constraint optimization overview.
  https://penrose.cs.cmu.edu/docs/ref
- **[S8] Systems Biology Graphical Notation specifications.** Reviewed official
  descriptions of Process Description, Entity Relationship, and Activity Flow.
  https://sbgn.github.io/specifications
- **[S9] StarVector: Generating Scalable Vector Graphics Code from Images and Text.**
  Rodriguez et al., CVPR 2025 per the author repository. Reviewed abstract,
  repository README and released image-to-SVG model card; full conference PDF
  was not reviewed. https://arxiv.org/abs/2312.11556 and
  https://github.com/joanrod/star-vector and
  https://huggingface.co/starvector/starvector-8b-im2svg
- **[S10] Vector Prism: Animating Vector Graphics by Stratifying Semantic Structure.**
  Yun and Choo, arXiv:2512.14336, December 16, 2025. Abstract reviewed; full text
  was unavailable through the attempted HTML route.
  https://arxiv.org/abs/2512.14336
