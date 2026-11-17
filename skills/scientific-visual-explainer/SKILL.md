---
name: scientific-visual-explainer
description: "Build biomedical mechanism schematics, graphical abstracts, experimental workflow panels, and interactive or animated scientific lessons (PNG, editable SVG sources, requested PPTX, offline HTML, and Manim video). Use for Figure 1A schematics, pathway models, 机制图、信号通路图、Graphical Abstract、实验流程图, redrawing static mechanism figures into editable components, or teaching papers/concepts visually. Default new schematics to Nord mist, capsule proteins and Y/U receptors; use domain-bearing structural detail when requested."
---

# Scientific Visual Explainer

Read [shared principles](../biomed-shared/core-principles.md).

Make biological mechanisms, experimental workflows and scientific models visible.
Read [visual standards](../biomed-shared/visual-standards.md) for shared Arial
typography, nomenclature and independent panel rules.

## Choose the deliverable route

First choose the [explanatory purpose](references/composition.md#choose-the-visual-argument):
graphical abstract, review schematic, mechanism model or visual explainer. Then
select the output mode from the user's request before planning scenes:

The table gives defaults for each mode; a narrower requested format takes priority.
For planning-only work, deliver the requested storyboard or plan and stop there.

| Request | Deliverable route | Primary references |
|---|---|---|
| **Static manuscript schematic, graphical abstract, or workflow panel** (e.g., for Figure 1A, pathway summary, or `figure-plan` assembly) | 600 dpi PNG with a reusable editable SVG/scene source; add PDF, delivered SVG or native PPTX when requested or needed for assembly. Export without a publication panel letter | [basic-mode.md](references/basic-mode.md), [composition.md](references/composition.md) |
| **Redraw or animate an existing static mechanism figure / graphical abstract** | Source-preserving component extraction (`scene.json`), original-vs-reconstruction comparison, editable PPTX, offline HTML and optional Manim MP4 | [figure-to-scene.md](references/figure-to-scene.md) |
| **Interactive concept, review or paper explanation** (or when no format is specified for a teaching request) | Seekable offline HTML lesson (`renderAt(time)`) coupling the complete static mechanism figure with step-by-step animated events and condition comparisons | [basic-mode.md](references/basic-mode.md), [visual-language.md](references/visual-language.md), [composition.md](references/composition.md) |
| **Domain-detailed molecular interaction or animated video** | Reusable SVG icon rig from [Biomed Icons](assets/biomed-icons/README.md) (or generated/vectorized via [generated-icons.md](references/generated-icons.md)) with fitted contact contours, plus HTML/PPTX/Manim export | [illustrations.md](references/illustrations.md), [generated-icons.md](references/generated-icons.md), [composition.md](references/composition.md), [media.md](references/media.md) |

## 1. Establish the scientific model and evidence scope

For a graphical abstract, read [graphical abstract](references/graphical-abstract.md)
to select and compress the contribution before choosing assets.

For a pathway database or predefined pathway layout, read
[pathway-assembly.md](references/pathway-assembly.md) to import identities and
geometry, then map them to reviewed mechanism events and biological anchors.

Read the supplied manuscript, paper, review or figure first:

- Keep measured results, proposed mechanisms and illustrative teaching models distinct.
  Link each consequential claim to an exact panel, section or page.
- Preserve literal biological entities, compartments, membrane topology, strand
  direction and species nomenclature. Identify whether each arrow represents
  transport, biochemical reaction, measured effect or proposed regulation (`activation`
  arrow vs. `inhibition` T-bar).
- Save `storyboard.md` recording the target audience, visual goal, entity/compartment
  inventory, and scene or panel table (`question / entities / visual change / takeaway / source`).

**Done:** `storyboard.md` defines the exact entities, compartments, arrow meanings
and source evidence boundaries.

## 2. Select symbol mode and rig assets

Search the [unified icon registry](references/unified-library.md) before drawing
new assets. Reuse the same asset key for the same subject across figures; choose
its recorded view, state and palette. Local reference redraws join the existing
catalog without replacing accepted geometry or creating a separate scene library.

Inspect relevant BioRender public examples and published CNS mechanism figures (from
local PDFs or curated galleries) to choose clear compartment layouts and symbol flow;
record `visual_references` separately from `scientific_references`.

- **Basic symbolic mode (default for new schematics, graphical abstracts and lessons)**:
  Read [basic-mode.md](references/basic-mode.md) and start from the
  [38-symbol primitive library](assets/biomed-icons/generic-primitives/preview.html)
  and [three basic mechanism examples](assets/basic-mechanisms/index.html).
  - Use **Nord mist** (`assets/basic-mechanisms/palettes.json`), `generic-protein-capsule`
    for proteins, `generic-receptor-y` / `generic-receptor-cup` (and their dimers)
    for receptors, adjacent capsules for complexes, and separate **P** circles for
    phosphorylation.
- **Detailed structural mode (when requested or required by domain-specific mechanism)**:
  Read [illustrations.md](references/illustrations.md) and reuse
  [Biomed Icons](assets/biomed-icons/README.md) first (`egfr-imagegen`, `tgfb-imagegen`).
  - When a new structural icon is needed, follow [generated-icons.md](references/generated-icons.md)
    to generate, vectorize, curate parts/anchors and register it.
  - When molecules physically dock, read the contact-contour rules in
    [composition.md](references/composition.md#state-marks-and-fitted-interfaces) so
    binding partners share a smooth closed interface at assembly scale.
- **Existing static figure import**:
  Follow [figure-to-scene.md](references/figure-to-scene.md) (`scripts/figure_to_scene.py`,
  `scripts/build_figure_lesson.cjs`, `scripts/export_figure_pptx.mjs`) to recover
  grouped SVG/raster components into `scene.json`.

**Done:** all required icons, compartments and anchors are selected or registered
with a contact sheet and provenance record.

## 3. Build the schematic or animated lesson

Compose a **clean static view at the selected explanatory level** before adding
animation beats. A graphical abstract uses the content selected above. Apply the
[artwork title rule](references/composition.md#titles-and-biological-labels) to
GA/review schematics and [shared source/export policy](../scientific-plotting/references/figure-delivery.md#reuse-inputs-and-save-objects-selectively)
to reusable sources and requested formats:

- Keep labels as separate editable SVG/PPTX text in Arial. Put protein names
  inside their capsules and size the capsule to fit. Keep compartment and complex
  labels outside. Check the text against the capsule boundary and adjacent bodies.
- Fit a ligand's contact contour to the corresponding receptor opening. Preserve
  the accepted receptor geometry and check the mating curves, contact clearance,
  and fill boundaries in both free and bound states.
- For **static manuscript panels / graphical abstracts**, export a letter-free
  600 dpi PNG at its intended placed size, retaining the editable scene/SVG source.
  Use `export_figure_pptx.mjs` or a native shape builder when editable PowerPoint
  assembly is requested; generate other formats only for the requested delivery.
- For **interactive HTML lessons**, drive drawing, captions and condition comparisons
  from a single state via `renderAt(time)` using [scripts/domain-motion.js](scripts/domain-motion.js),
  [scripts/mechanism-arrows.js](scripts/mechanism-arrows.js) and
  [scripts/mechanism-annotations.js](scripts/mechanism-annotations.js). Keep the
  complete static overview one click away. Reference worked lessons:
  [EGF–ERK](assets/egfr-generated.html), [TGFβ–SMAD](assets/tgfb-generated.html),
  and [Cas9](assets/jinek2012.html).
- For **slides or Manim video**, follow [media.md](references/media.md) and
  `scripts/render_figure_manim.py`.

**Done:** the static schematic and any requested HTML/PPTX/video outputs are
built from a single consistent scene model.

## 4. Inspect at viewing size and deliver

Open every static frame, PPTX slide, or interactive scene in its intended use:
graphical-abstract thumbnail, manuscript column, presentation or interactive viewport.
For responsive lessons, also inspect a narrow viewport. Reflow detail for that use
while preserving the model and the shared effective-size rules:

- Check for text/text, text/icon, arrow/icon and phospho-badge collisions across
  initial, intermediate approach, bound and released states.
- Verify compartment topology (receptors span the membrane midplane; nuclear import
  crosses a visible pore; cargo stays on the correct lumenal/cytosolic side).
- Verify that displayed quantitative readouts match source data or are explicitly
  labeled **illustrative** / **simulation** / **digitized**.

Apply [reader read-back](../biomed-shared/reader-feedback.md) to the final view and
caption as part of this inspection.

**Done:** visual defects are resolved on the rendered artifacts. Deliver the
requested formats and link the reusable source, storyboard and model. A static
PNG delivery does not require extra PPTX/PDF/HTML exports.
