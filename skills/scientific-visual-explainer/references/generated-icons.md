# Generate a missing mechanism icon

Use this branch when the library has no suitable icon, or the user requests a coherent visual refresh. The target is a clean mechanism figure that also supports animation. Preserve the user's chosen native artwork when that is the task.

## Generate, convert, register

1. Search `assets/biomed-icons/catalog.json` by entity, domain role and compartment. Reuse a suitable registered asset. For a missing or unsuitable asset, inspect the relevant biology and a public visual example, then use the **built-in image generation tool**. Generate one asset per call; use an accepted asset as a style reference when needed.
2. Brief the icon for its biological job: domain order, membrane sidedness, contact regions, empty assembly space, orientation and omitted detail. Use a flat front view, smooth contours, a shared outline and 2–4 solid family colors. Keep text, arrows, nucleotides and state badges as separate SVG overlays. Request a transparent background. Save the original PNG and exact prompt under the icon family's `sources/` and `prompts.json`.
3. Convert the PNG into real SVG paths. Use `scripts/trace_icon.py` with a small source specification; this helper uses Pillow, NumPy and VTracer. It normalizes the artwork to the family's 160 × 160 canvas, applies a chosen palette, preserves path paint order and transforms source-pixel anchors. A PNG inside an SVG wrapper is not an editable vector conversion.
4. Inspect the generated biology before registration. Correct a wrong domain, membrane count or contact orientation with the built-in image editor and trace the corrected source. Design binding partners as a pair: reserve assembly space and fit complementary visible contours at the intended scales. Curate meaningful palette roles, extra motion parts, contact points and normals. Auto-traced color regions are not automatically complete biological domains; retain a shared outline or refine parts when independent domain movement is needed. Keep P circles, nucleotide labels and arrows outside the generated bitmap as editable overlays.
5. Register the SVG, parts, anchors, scientific scope and provenance in the family manifest and root catalog. Review the source PNG, vector, 64–160 px renders and actual bound/reaction frames. Reuse the existing animation engine to test the intended contact or transport event. A complete static mechanism figure and its animated states should share the same assets.

If the built-in image tool is unavailable, report the missing capability. Use API/CLI generation only when the user explicitly selects that fallback.

## Conversion helper

A source specification contains the normal catalog fields plus a palette map and anchors in **source PNG pixels**:

```json
{
  "id": "example-receptor",
  "label": "Example receptor",
  "label_zh": "示意受体",
  "category": "my-family",
  "description": "Receptor with a distinct recruitment tail.",
  "palette": {
    "outline": "#3D5963",
    "ectodomain": "#69ADB5",
    "tail": "#E4BE78"
  },
  "anchors": {
    "membrane": {"point": [512, 872], "normal": [0, -1], "kind": "membrane"},
    "binding": {"point": [641, 1426], "normal": [0, 1], "kind": "binding"}
  },
  "scope": "Domain-level teaching schematic, not atomic geometry.",
  "provenance": {
    "mode": "built-in-imagegen-traced",
    "source": "my-family/sources/example-receptor.png",
    "prompt": "my-family/prompts.json",
    "license": "MIT"
  },
  "visual_references": [],
  "scientific_references": []
}
```

The numbers are format examples; select anchors on the actual new artwork. Put binding anchors on accessible contact contours, membrane anchors at the insertion plane, and normals in the local outward direction. Record which references were visually inspected and which were read as text.

```sh
python scripts/trace_icon.py \
  assets/biomed-icons/my-family/sources/example-receptor.png \
  assets/biomed-icons/my-family/example-receptor.svg \
  --spec example-receptor.json
```

This writes the SVG and an adjacent catalog-entry JSON for review. After review, add `--register assets/biomed-icons` to add or update the matching family manifest and root catalog entry. Registration does not change the model's scientific status. Rebuild the atlas after registration so the browser and catalog contain the same assets. Run the bundled `python scripts/build_icon_atlas.py` to rebuild `assets/biomed-icon-library.html` from the registered family manifests.

The [EGFR family](../assets/biomed-icons/egfr-imagegen/manifest.json) is a worked example. It retains original PNGs, fixed-palette tracing inputs, prompts, source specifications and the corrected domain-II dimerization arm.
Its [interfaces.json](../assets/biomed-icons/egfr-imagegen/interfaces.json) pairs
eight contact types. Use [fit_interfaces.py](../scripts/fit_interfaces.py) for
continuous whole-body vector refinements after tracing; it preserves source PNGs,
uses OpenCV/Shapely to rebuild connected bodies and records the assembly scales. Review the fit in the complete complex, not only
in separate icon thumbnails.

The [complete EGF–ERK lesson](../assets/egfr-generated.html) uses these assets with the existing engine. Its source model is [mechanism-example.json](../assets/biomed-icons/egfr-imagegen/mechanism-example.json).

The [TGFβ family](../assets/biomed-icons/tgfb-imagegen/manifest.json) is the second worked example. In its [interfaces.json](../assets/biomed-icons/tgfb-imagegen/interfaces.json), `duplicatePorts` repeats a profile at symmetric sites, and optional `extent` controls its outer blending width. Fit at the consuming scales and inspect the approach as well as the final contact. Keep biological stoichiometry in the event model; duplicated ports do not by themselves establish a stoichiometry.

Use `MechanismAnnotations.phosphorylation(core, frame, marks)` from [the shared helper](../scripts/mechanism-annotations.js) for state-driven P circles. A mark specifies `entity`, `state`, optional `anchor`, world-space `offsets` and optional `sites`. Use two separate badges for two identified sites; keep long residue labels in a clear figure key. Do not infer phosphorylation from an `active` label: SMAD4 is not given an activation P badge, and ALK5 GS-P can persist in the catalytic-block comparison while downstream SMAD3 P is absent.

The [shared engine](../scripts/domain-motion.js) accepts `approach` waypoints on `dock` and `reaction` events. Route the whole cargo clear of the pore rim and DNA; keep its attached badges inside the passage. Briefly hide names during movement when that gives a cleaner figure, then restore them after the actor settles. Preserve labels, colors and compartment topology across conditions.

For outline repair, fit the body rather than layering another outline on top. The helper emits closed cubic body contours and separate color regions. Its single color clip keeps fills inside the body; contact cutting clips and rectangular patches are absent. Draw only the outer body edge and genuine internal domain seams. Review the [contour comparison](../assets/contour-review.html).
