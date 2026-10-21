# Composition for scientific scenes

Use these as adaptable decisions, not a required style or scene order. Choose
composition to make the evidence and learning goal legible.

## Choose the visual argument

- Decide whether the lesson explains a measured transition, an association, a
  proposed mechanism, or competing alternatives. Animate a transition only when
  the source supports it; display alternatives as branches or side-by-side states
  unless a temporal order is supported.
- Name what changes and what remains context. Preserve the identity, color,
  orientation and spatial role of an entity across scenes so viewers can track it.
  Change only the objects needed to explain the current event.
- A reusable scene grammar is **context → active event → evidence or comparison →
  hold to explain**. Reorder, combine, or omit parts when the argument calls for it.
  It is a planning aid, not a template.

For a mechanism that can be described as entities moving or changing state, keep
the biological description separate from drawing coordinates: record entities,
states, compartments, events, and source links first. Give events explicit
dependencies when only a partial order is supported; do not use JSON array order
as biological evidence. Retain alternative paths as branches. This graph is a
useful input format for some mechanisms, not a required ontology for every
lesson.

## Place and group objects

Manim provides layout primitives; it does not choose the scientific composition.
In 3Blue1Brown's source, `VGroup.arrange()` places each object next to the previous
one and recenters the group; `next_to`, `move_to`, and `to_edge` express placement
choices ([Mobject source](https://github.com/3b1b/manim/blob/master/manimlib/mobject/mobject.py),
[frame coordinates](https://3b1b.github.io/manim/documentation/constants.html)).
Use a few direct coordinates for important anchors, then place labels and related
objects relative to those anchors. Group parts that should move together. For
example, a molecule can group its body and separately addressable domains; a
biological comparison can share a scaffold while varying only the supported
condition. Keep this visual consistency without implying the alternatives occur
in sequence.

When using an event graph, derive placement from entity roles and compartments,
then apply deliberate composition choices. Keep membrane-spanning entities on
the membrane through budding and fusion; preserve cargo on the correct lumenal
or exterior side. Treat those as topology constraints only when supported by
the mechanism. Keep layout rules independent of molecule names so a changed
entity label or event list does not change the underlying biology.

## Rig reusable artwork

Inspect suitable source art before choosing or drawing an entity. For native reuse,
retain the selected asset and record edits. For a consistent family, start from
[Biomed Icons](../assets/biomed-icons/README.md); generate, vectorize and register missing parts
once through [generated-icons.md](generated-icons.md). Original family drawings are a first-class option,
not a fallback. Keep source-derived adaptations distinct from original paths.

Attach contact, membrane and transport anchors to reusable icon parts. A docking
operation aligns compatible points and opposing normals, then moves the complete
object. Membrane guides constrain phospholipid instances and membrane-bound
proteins; they do not replace the icon with an unrelated shape. Keep object identity
through association, release and complex membership changes. Camera bounds include
the active operation, and an overview can reuse the same scene graph.

Inspect native/reference art, the family contact sheet, and interaction frames.
Shared colors do not establish biological equivalence: preserve entity-specific
morphology and state what is schematic. A missing library entry should trigger a
small reusable addition, not a new whole-mechanism template.

## Show contacts and motion

- Animate the event, not a decorative path. Use a directed move for a supported
  transition and a static comparison or separate branches for alternatives.
  Simultaneous changes belong in one animation beat; distinct events can use
  successive beats. Use holds for captions and inspection.
- For schematic docking, attach contact glyphs to named regions. Place their
  anchors on the facing edges, and use each local outward normal to orient the
  glyph toward its partner. Pair complementary convex and concave contours at
  their final drawing scales. Fit a shared curve along the visible interface;
  two coincident points alone do not establish a fit. Preserve each component's
  recognizable body and reserve room for its partner. Complementary abstract ports can make an intended
  interaction readable, but label them schematic; do not make them resemble a
  reconstructed pocket or solved protein surface. If an experimental structure
  resolves the interface, use that geometry and cite its model and limits.
- Keep state labels synchronized with the drawing. A proposed assembly order is
  not measured kinetics. A knockout or domain-deletion assay is a comparison
  condition; do not animate it as a live molecular deletion unless that process is
  itself the supported subject.

3Blue1Brown's scene sources illustrate author-chosen object and camera motion: the
[chapter-list scene](https://github.com/3b1b/videos/blob/master/_2016/eola/chapter7.py)
uses grouped, aligned text; the
[cosmic-distance scene](https://github.com/3b1b/videos/blob/master/_2025/cosmic_distance/part2.py)
moves a camera, dims context, and highlights a selected example. Manim's
[animation source](https://github.com/3b1b/manim/blob/master/manimlib/animation/animation.py)
sets `smooth` as the default rate function; easing controls presentation, not
biological rate. These links use ManimGL. Treat their logic as examples, not
copy-ready code for Manim Community Edition or HTML.

## Direct attention and check layout

- Let the camera follow the active event while preserving enough whole-system
  context to identify where it occurs. A persistent overview plus a detail view is
  useful when the local interface matters; it is optional when one view is clear.
  Keep the overview, detail crop and scene state synchronized.
- Reserve stable regions for labels, captions and controls. Anchor those regions
  to the viewport when the scene moves. Check projected bounds for every label,
  contact glyph and object over transitions, not only at endpoints. Inspect the
  smallest supported viewport and prevent labels from covering active contacts.
- Validate actual drawn shapes against compartment and membrane boundaries;
  bounding boxes alone can miss a lobe or ligand crossing the wrong side. Check
  intermediate event states as well as the start and end states. For a
  data-driven renderer, test a renamed entity, reordered event records, and a
  changed or branched event graph to confirm that IDs and dependencies, rather
  than hard-coded names or list position, control the result.
- Use a consistent palette to preserve identity. Use contrast or scale to focus
  attention on the active event, and reduce emphasis elsewhere. BioRender's
  [pathway illustration webinar](https://www.biorender.com/learn/drawing-biological-pathways)
  discusses flow, contrast, and scale as figure-design tools; these are useful
  options, not requirements to use BioRender or imitate one style.

## Practical review

Before rendering, verify that each motion has a clear scientific meaning, each
caption names the claim boundary, alternatives remain distinguishable, and camera
movement does not remove context. Review a beginning, transition, and final frame
at actual viewing size. If the geometry is illustrative, label it; do not let
smooth movement, a close crop, or a well-fitting glyph imply measured timing,
affinity, or structural resolution.

## Extend beyond known examples

For an unfamiliar mechanism, write the pre-event and post-event biological
relations first: attachment, containment, membrane side, identity, state and
quantity. Decompose the change into transformations of those relations. Reuse
placement, grouping, route and camera rules; do not look for a whole-scene
template with the same biological name. If a new operation is needed, add one
small operation defined by its inputs and pre/postconditions, then test it with
renamed objects and changed counts. Never silently substitute a familiar event
for a different biological process.

For the current video style, use a white background and Arial throughout, with
one short explanatory sentence per beat. Nature's figure guidance recommends
[Helvetica or Arial](https://www.nature.com/nature/for-authors/final-submission).
Put full provenance and scientific scope in the adjacent source notes; show a
qualification in the film where it changes the meaning of that specific event.
For text inside a molecule or domain, check containment in its actual filled
outline with padding, including rotated intermediate states. Put longer names
outside the shape when they cannot fit at the minimum readable size.

### Reaction connectors

Size arrowheads with `markerUnits="userSpaceOnUse"` so their size stays independent
of the shaft width. Connect the current contact surfaces with a clean line and
leave space before each contour. Fade a causal connector out when its molecules
come into direct contact; suppress inactive reaction arrows. Inspect start,
contact and released states for backward arrows, oversize heads and paths through
other artwork. [mechanism-arrows.js](../scripts/mechanism-arrows.js) provides the EGF–ERK example's small
connector renderer; the molecular motion engine remains separate.

### State marks and fitted interfaces

Use a small filled circle containing **P** for phosphorylation. Attach it to the
modified component and reveal it at the state-change event. Two P circles can
show MEK's two serines or ERK's threonine and tyrosine; label S, T and Y outside
the badges and explain them once in the figure key. A representative receptor
badge does not count every phosphorylated tyrosine. Keep RAS GDP/GTP exchange
and aggregate RAF activation as separate text states rather than P badges.

The EGF–ERK example keeps these overlays in
[mechanism-annotations.js](../scripts/mechanism-annotations.js). Its
[paired-interface specification](../assets/biomed-icons/egfr-imagegen/interfaces.json)
records counterpart scales and a shared contour. The vector refinement helper
[fit_interfaces.py](../scripts/fit_interfaces.py) rebuilds a complete closed cubic
body from the preserved generated source, replaces its contact arc with a smooth
shared curve, and updates the contact
anchors. It requires Pillow, NumPy, OpenCV and Shapely. Rerun it when changing the paired
scales or contact artwork, then inspect the actual bound silhouettes. Prefix both
SVG IDs and their local `url(#...)` references when placing multiple copies.

Check badges and nucleotide glyphs against text as well as against bodies.
For dense nucleotide exchange, separate the moving dots from a stable short
label such as “GDP out · GTP in”. Sample the whole timeline and render important
approach/contact/release frames; a clean final frame does not clear a transition.


### Continuous body contours

A fitted contact must also look natural when the components are apart. Blend the shared curve into the existing body with continuous endpoint tangents. Keep the mating depth shallow and reserve enough shoulder length; avoid small stamped bumps, hard cut edges and disconnected seam fragments. Use a complete closed body outline, with named color regions inside it. A single body clip may contain those colors, but do not use cutting rectangles plus independently stroked contact patches.

Preserve long straight sections and thin membrane stalks. Limit interpolation handles by adjacent segment lengths so smoothing cannot pinch a stalk or create ears.

Normalize structural outlines at the consuming scale. The generated family uses outer weight 1.6 and internal domain weight 1.1 drawing units; [mechanism-icons.js](../scripts/mechanism-icons.js) divides those weights by the actor scale before drawing. Colored strands, membranes and scaffold columns are anatomy, so their widths are separate from outline weight.

Verify the actual SVG curves and rendered connectivity, not only anchor coordinates or saved profile samples. Compare unbound and assembled states, inspect contact shoulders at magnification, and then judge the whole figure at viewing size. The [contour comparison](../assets/contour-review.html) shows the corrected examples.
