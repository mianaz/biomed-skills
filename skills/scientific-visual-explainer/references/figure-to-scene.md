# Static figure to explanation

Use this branch for an existing mechanism diagram or graphical abstract. Keep
the original figure beside its component reconstruction. Preserve layout,
silhouettes, labels and arrow meanings before adding motion or changing style.

## Recover components and meaning

Read the image, caption and relevant text. Use a visual model to propose entities,
instances, compartments, relations and events; check them against the source.
The import script recovers geometry, not biological meaning. A duplicate drawing
can be another copy or a later state of one entity. Keep those cases distinct.

Prefer an author's grouped SVG when available. The first importer supports flat
paths, ordinary shapes, nested transforms and unrotated text. It converts them
to native paths/text while keeping the original SVG. Include context/background
groups in the annotation. Groups must not overlap. Unsupported SVG references,
filters, masks, gradients and active content need separately exported components.
Expand dashed strokes and even-odd fills to plain paths, or use transparent assets.
PPTX/PDF source extraction is not implemented in this importer; use other available
tools to obtain components, then prepare the scene.

For PNG/JPEG, supply reviewed component regions and transparent assets or full-size
masks. `asset` and `mask` paths are relative to the source image. `crop:true` explicitly
allows a rectangular crop; it retains its background and text. It is not a clean
segmentation. The script does not run OCR or a segmentation model. Use available
tools or agent-assisted annotation, then inspect the assembled result. Preserve
occluded regions as unknown or mark any completed contour as reconstructed.

Keep objects, labels and state badges grouped by identity. Keep relation arrows
separate from physical contacts. An activation arrow can be highlighted without
docking its proteins. Put each event's claim locator in `source`; timing defaults
to teaching sequence, not measured kinetics. Image-only input can support a visual
tour while unresolved mechanism claims await a caption or other evidence.

## Small annotation file

Start from [the complete example](../assets/figure-to-scene/annotations.json) and
[its original SVG](../assets/figure-to-scene/source.svg). This is a generic teaching
example, not a recovered published mechanism.

An SVG entity needs `id` and an optional `source_id` (defaults to `id`), plus its
reviewed `kind` and `label`. The importer discovers top-level named objects if no
entity list is supplied; missing IDs are assigned during import. Those objects
remain `unclassified`, with no invented events.
A raster entity needs `id`, `bbox:[x,y,width,height]` and an `asset`, `mask`, or
explicit `crop:true`. Optional `texts` restore native labels after the old text
has been removed from the raster asset. Each text needs `text`, `x`, `y`, `fontSize`
and `bbox`; the default font is Arial.

`relations` store meaning (`from`, `to`, `kind`) separately from drawing order.
The first imported-figure event set is deliberately small:

- `move`: `actor`, `to:[dx,dy]`, optional `via:[[dx,dy],…]` and `carry:[ids]`.
  Offsets use original figure pixels. A label inside its entity already moves with it.
- `reveal`: a gradual appearance; set the entity's `hidden:true` initially.
- `state`: change the actor's filled paths to `fill`, halfway through the event.
  Raster parts need a separate state badge or a supplied alternate asset instead
  of this native-path recoloring operation.
- `highlight`: select the actor during the event without changing its geometry.

Every event has a unique `id`, positive `duration`, `title`, `caption` and `source`.
Use `after:[event IDs]` and optional `delay` to arrange teaching order. Existing
domain-motion scheduling supplies dependency handling. It does not establish
biological causality. Use finite event sequences for feedback diagrams.

## Build from the skill directory

The SVG importer needs `svgelements`; raster parts need `Pillow`. Use an existing
environment when possible; optional import/PPT dependencies are listed in
`scripts/requirements-figure.txt`. The HTML build needs only Node.js.

```sh
python scripts/figure_to_scene.py assets/figure-to-scene/source.svg \
  --annotations assets/figure-to-scene/annotations.json --output output/scene.json
node scripts/build_figure_lesson.cjs output/scene.json output/lesson.html
```

The scene JSON embeds source artwork and components. The offline HTML offers an
original/reconstruction view, component selection, seeking and step controls. Its
current SVG is downloadable. `lesson.frames.json` and `lesson.vtt` contain states
and caption timing from exactly the same evaluator for the video backend. Do not
put private source figures into
a public skill bundle without the user's intended sharing scope.

For editable PPT, use an available `@oai/artifact-tool` runtime and a Python with
`lxml`. If the module is not on Node's package path, set `ARTIFACT_TOOL_MODULE` to
its module file. `SCENE_PYTHON` selects the Python executable.

```sh
node scripts/export_figure_pptx.mjs output/scene.json output/lesson.pptx
```

This creates a slide at each event boundary, each routed movement bend, transient
highlight midpoints, and the initial state. Waypoint slides keep straight-line
Morph segments on the intended route instead of cutting through a compartment. SVG paths
and text are native editable objects, grouped under stable `!!entity` names.
Raster parts remain images. Morph transitions include a Fade fallback; actual
PowerPoint playback needs inspection. Intermediate renders live in `.figure-build/`.
There is no conversion from MP4 to editable PPT objects.

For Manim, use an environment with Manim Community and NumPy:

```sh
python scripts/render_figure_manim.py output/scene.json output/lesson.frames.json \
  --output output/lesson.mp4
```

The adapter renders the baked geometry/visibility states and captions. Keep the
existing Manim assembly and membrane-traffic tools for detailed continuous shape
changes. Changing a scene requires rebuilding its frame file before rendering.

## Inspect and deliver

Compare the reconstruction with the actual original at viewing size. Check all
objects and arrowheads, labels, inherited transforms and layer order. Inspect
approach, contact, compartment crossings, state markers and final output. Move
and rewind the time control; labels and state badges must follow their owner.

Inspect the actual PPT slides and a transition in PowerPoint. Test selection of
a whole component and editing its text or path. Inspect the video, not only its
render log. Deliver the requested formats, scene JSON and original/annotation
sources. Report which parts remain raster and any unsupported input feature.
