# PI3K–AKT–mTOR icon family

Eight additions to collection v0.8, following the v0.7 flat drawing guidelines:
PI3K (class IA p110α/p85α), AKT1, PTEN, PDPK1, mTOR, RAPTOR, mLST8 and RHEB.
Open [preview.html](preview.html) for 64/96/160 px views and four pairwise contact previews.

Each icon has an original built-in-generated alpha PNG, the exact prompt, a fixed-palette tracing input, editable SVG paths, semantic fill regions and anchors. Source PNGs remain unchanged; final vectors remove source gradients and standardize line weights. `domain-seams.json` records the curated structure seams. The AKT connector belongs to the kinase region rather than its regulatory tail.

The public BioRender PI3K pathway preview was visually inspected for flat diagram style. No BioRender art was copied or traced. RCSB structure metadata and linked primary-publication summaries were read separately to check domain architecture; scientific references are attached to each icon in `manifest.json`. The p85 schematic extends beyond the regulatory fragment resolved in 2RD0. The mTOR panel shows one module, not a complete mTORC1 dimer. RHEB nucleotide state, phosphorylation marks and labels belong to the consuming scene.

## Rebuild

Use Python with Pillow, NumPy, VTracer 0.6.15, OpenCV, Shapely and CairoSVG.
Run `trace_icon.py` for each entry in `source-specifications.json` when changing a source image. Register the traced entries, then run:

```sh
python skills/scientific-visual-explainer/assets/biomed-icons/pi3k-akt-imagegen/refine.py
python skills/scientific-visual-explainer/assets/biomed-icons/pi3k-akt-imagegen/build_preview.py
python skills/scientific-visual-explainer/scripts/build_icon_atlas.py
```

`refine.py` fits the continuous body contours using `interfaces.json`, restores domain seams, and updates the manifest/catalog. `assembly-models.json` uses the existing `domain-motion.js` engine; edit its start positions and fixed view boxes together when changing geometry. `contour-check.json` and `assembly-check.json` retain the reviewed geometry and frame-sampling results. Filled silhouette intersections include the shared stroked contact border; review the actual images as well as the numbers.

Semantic fill groups support recoloring. They share an outer body outline; independently moving domains needs additional rigging. Contact shapes and anchor normals are teaching geometry, not measured molecular interfaces or kinetics. Original generated artwork and derived vectors use the package MIT license.
