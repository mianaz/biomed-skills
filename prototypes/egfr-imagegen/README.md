# Generated EGF–ERK mechanism figure

Open `preview.html` for a complete static mechanism figure and its 42-second animation. Eight new generated icon types, represented by ten instances, cover EGF, EGFR, GRB2, SOS1, RAS, RAF1, MEK1/2 and ERK1/2. The same SVGs drive both views through the skill's `scripts/domain-motion.js` engine. The core supports pause, replay, seeking, phase selection, recoloring, current-frame SVG export and an illustrative EGFR kinase-block comparison.

## Editable sources

- `preview-template.html`: page and figure layout.
- `mechanism.json`: generated source model with events and dependencies.
- `build.py`: compose the model and offline HTML from the registered family.
- `references.json` and `storyboard.md`: source-to-event mapping and teaching scope.
- `../../skills/scientific-visual-explainer/assets/biomed-icons/egfr-imagegen/`: original PNGs, corrected EGFR, prompts, tracing inputs, source specifications, SVGs and registration manifest.
- `qa/` (create before running the checks): local output for reviewed states and browser/geometry checks; not tracked.

Run `python build.py` to rebuild the lesson from registered SVGs. This step uses only the Python standard library. Image conversion uses the skill's `scripts/trace_icon.py` and requires Pillow, NumPy and VTracer; source specifications are in the icon family's `specs.json`. Reuse the saved PNGs for vector tuning; regenerate through the built-in image tool when biological shape needs correction.

The viewer preserves a minimum figure width on narrow screens so labels remain readable. Export uses Arial at 190 mm width. All figure text is separate from the icon paths. The lesson deliberately shows the canonical core; the source notes identify combined regulation and illustrative timing.

The current revision uses matched SVG contact curves from the family's `interfaces.json`, separate P-circle state overlays, and an unobstructed recruitment route. `check-layout.cjs` samples both normal and kinase-block conditions, checks contour coincidence, and prepares timeline states. `render-review.py` checks actual silhouette/text/arrow/glyph intersections and writes the 23-frame HTML review and static exports; it needs Pillow, NumPy and CairoSVG. Run `check-model.cjs` and `check-arrows.cjs` for the existing contact/state and connector checks. Browser playback/control evidence from the earlier version is retained separately from the current local rendering checks.
