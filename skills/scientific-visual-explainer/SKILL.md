---
name: scientific-visual-explainer
description: Build scientific mechanism figures and animated HTML lessons. Default to BioRender-referenced basic symbols: capsule proteins, Y/U receptors and matching dimers. Use structural illustration when requested.
---

# Scientific Visual Explainer

Make the scientific idea visible. For biomedical mechanisms, first make a clean,
complete static figure, then animate the events that explain it. Begin from the
learning goal and choose a visual argument that fits the evidence. A question-
led open stage is useful, not mandatory. If the user gives no format, a short
offline HTML lesson is a good default; follow their language and audience.

## 1. Establish what the lesson can show

Read supplied material first. Retrieve missing sources when possible.

| Input | Reading focus |
|---|---|
| Concept | An authoritative account of the relationship and its assumptions. |
| Review | The competing explanations and the primary studies behind central claims. Attribute claims to the review when their primary source is unread. |
| Paper | Figures and captions with the relevant Results, Methods and supplements. Identify the comparison that supports each teaching point. |

Keep measured results, interpretations and teaching models distinct. Preserve
units, controls, biological units and uncertainty when showing data. Link each
consequential claim to an exact panel, section or page. Label invented examples
**illustrative**, model outputs **simulation**, and traced data **digitized**.
Record actual reading scope and consequential access gaps once in source notes.
An abstract alone supports an abstract-level lesson.

## 2. Plan the visual argument

Save `storyboard.md`: audience, learning goal, and a compact scene table with
question / objects / visual change / takeaway / source. Each scene resolves one
question. Arrange scenes by learning order; paper figure order is a source index.
For a review, preserve disagreement instead of forcing one causal chain.

Use literal biological entities and their documented relationships. Preserve
compartments, molecular direction, strand identity and species. Identify whether
an arrow means transport, reaction, measured effect or proposed mechanism.
Expression, association and prediction retain their original evidence meaning.

For this unified icon family, use BioRender as the single visual reference
standard. Inspect its actual public example before drawing. Use scientific
literature separately to check biological structure and mechanism; label
`visual_references` and `scientific_references` separately in each new manifest.
Choose the asset mode with the user's visual goal. **Basic mode is the default**
for mechanism figures and animations. Read [basic-mode.md](references/basic-mode.md)
and start from the [three complete basic examples](assets/basic-mechanisms/index.html).

- **Basic mode (default):** generic proteins use the same capsule symbol, with
  separate names and state badges. Use Y/U receptors; draw a Y dimer from two Y
  monomers and a U dimer from two U monomers. Complexes contain multiple capsules.
  Use native SVG geometry, directional arrows, compartments and simple nucleic
  acid symbols. Build the complete mechanism figure, then animate that figure.
- **Detailed mode (on request):** use domain-bearing and structure-informed assets
  when that detail explains the user's biological question.

For detailed illustration, choose the relevant source route:

- **Native artwork:** inspect the requested source and preserve its proportions, palette and details.
- **Unified icon family:** use the reusable [Biomed Icons](assets/biomed-icons/README.md)
  first. If no suitable icon exists, use the **built-in image generation tool**,
  convert the result to editable SVG paths, curate parts and anchors, and add it
  to the library. Follow [generated-icons.md](references/generated-icons.md) for
  generation, conversion and registration. Use the same route for a requested
  style refresh; keep each accepted asset stable across scenes.

Keep a contact sheet and per-asset source/license record. Distinguish reference-
informed original drawings from adapted source vectors. Preserve recognizable
biology, compartment topology and useful domain structure. Keep labels as separate SVG text; names may be centered inside capsules. Keep
artwork separate from the motion rig. Use anchors and membrane guides
to animate registered assets or parts. For icon QC, compare distinguishing structures against a cited scientific figure
or morphology atlas, and compare clarity/composition against an inspected BioRender
public example. Record what was visually inspected versus text-only.
Treat illustration examples as design references, not mechanistic evidence.
Compare the library contact sheet and actual interaction frames at viewing size; a source-fidelity request still
requires the original source artwork.

In detailed physical-contact scenes, design binding partners together: their visible contours must fit at the actual
assembly scales, like complementary puzzle pieces. Matching anchor points alone
is insufficient. Preserve one smooth, closed body contour through each contact;
blend its shoulders with matching tangents. Do not paste separately outlined tabs
onto a traced outline. Normalize outer line weight at the final assembly scale;
keep internal domain lines lighter. Inspect free and bound forms at viewing size
and magnified contact scale. Keep phosphorylation as separate **P circles** attached to the
modified component; show residue type or multiple sites when the mechanism needs
them. Keep nucleotide exchange and generic activation as distinct states. See
[composition.md](references/composition.md) for contact and state overlays.

Borrow anatomical cutaways or separated components when they reveal how parts
fit and function. Name what moves and what its movement means. Add detail only
when it explains the science. A schematic protein outline is not a solved
structure; label its geometry and timing as illustrative where relevant.

## 3. Build the lesson

Read [visual-language.md](references/visual-language.md) when its stage, type and
motion defaults fit the requested medium; these are options, not a required
template. Use direct HTML/CSS/JavaScript and editable SVG; keep assets embedded or
local. Scientific analysis and publication plots use R
(prefer tidyplots) or Prism, with direct data and editable plot source retained.

Drive drawing, captions and readouts from one scene state. Prefer a small
`renderAt(time)` function for replayable, seekable animation. When the reader
changes a condition, show the corresponding comparison; separate simulated
outcomes from reported measurements. Keep the baseline available.

For a biomedical mechanism, read [composition.md](references/composition.md) for
adaptable scene grammar, identity and contact cues, alternatives, camera and layout.
For biomedical icon animation, follow the reference-and-library-first method above and
[illustrations.md](references/illustrations.md) before scene layout. If requested
source art is unavailable, record the gap; do not silently replace it with
hand-drawn anatomy. Use the unified family for original schematics when the user requests style consistency. For slides, PPTX or video, read
[media.md](references/media.md). These are optional branches; HTML needs no
external skill or service.

The [Cas9 paper example](assets/jinek2012.html) demonstrates a minimal animated
stage, component assembly and a source-linked mutant comparison. Its
[storyboard](assets/jinek2012-storyboard.md) records the evidence scope. Reuse
patterns that fit the new lesson, not its molecular geometry. The smaller
[causal-model example](assets/causal-models.html) is a toy-model alternative.

The [EGF–ERK worked lesson](assets/egfr-generated.html) pairs eight generated SVG
icons with the shared engine, a complete static figure and a kinase-block
comparison. Its [source model](assets/biomed-icons/egfr-imagegen/mechanism-example.json)
and [icon specifications](assets/biomed-icons/egfr-imagegen/specs.json) are editable.

The [TGFβ–SMAD3/SMAD4 lesson](assets/tgfb-generated.html) tests the same system
on a second pathway: eight generated icons, including refreshed DNA/RNA, two receptor pairs, a 2:1 SMAD
heterotrimer, nuclear import and transcription. Its two controls distinguish
receptor GS phosphorylation from downstream SMAD3 phosphorylation. Read its
[storyboard](assets/tgfb-storyboard.md), [model](assets/biomed-icons/tgfb-imagegen/mechanism-example.json)
and [QC](assets/biomed-icons/tgfb-imagegen/QC.md). The reusable
[engine](scripts/domain-motion.js) supports waypoint approaches for docking
and transient substrate reactions.

## 4. Inspect the result

Open every scene in a browser at the intended size and a narrow viewport.
Inspect beginning, transition and final states. Check labels, contact marks,
biological geometry, pause/replay, seeking, keyboard controls and reduced motion.
Check displayed values against source data or the stated model, including an
informative extreme. A polished image is not evidence of scientific correctness.
Fix observed defects; state any inspection that could not be performed.
Inspect the full animation for text/text, text/icon, arrow/icon and badge
collisions. Include approach, bound, reaction and release states; refine the
approach path when a moving complex crosses an unrelated component. Keep labels
clear without abrupt side changes. Inspect matched contours at contact scale.

Deliver the working HTML, storyboard and editable source/assets. Put citations
and reading scope inside the lesson. Open a preview and link the result. For
requested slides or video, deliver and inspect that format too; a timed
storyboard is not a video export.
