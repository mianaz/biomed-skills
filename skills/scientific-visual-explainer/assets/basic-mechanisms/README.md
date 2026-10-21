# Basic mechanism figures and animations

Open [index.html](index.html) for three complete figures, animation timelines and block-A comparisons. Generic proteins always use capsules. Receptors use Y/U monomers and matching dimers. Static figures and animations share the same SVG renderer and declarative source models.

- [Y cascade](figures/cascade-normal.svg)
- [U complex import and RNA output](figures/import-normal.svg)
- [Y/U convergence](figures/convergence-normal.svg)

The figures directory also contains block-A versions and PNG previews. SVG text, arrows, P badges and glyph parts stay editable. English protein/state labels use Arial; Chinese labels use a CJK font fallback. The browser player is self-contained and needs no dependencies.

Edit models.json and player.js, then run `python build.py` to rebuild the offline HTML. Optional `node render_figures.cjs` (with jsdom available) exports all six figure states and checks capsule identity, P counts, unique SVG IDs and one second of playback at 60 fps. state-check.json records those checks. The storyboard and model file identify the illustrative rules and the scope of inspected BioRender references.

## Palette comparison

Open `palettes.html` to compare the original palette with Nord, Radix and Rosé Pine adaptations on all three mechanisms and both conditions. `palettes.json` records role colors, source links and tint recipes. These are application-specific role mappings, not official biomedical palettes. The main player has the same palette selector; exports preserve the selected colors. The existing default stays unchanged.

Build HTML with `python3 build.py`. After changing scene geometry, run `render_figures.cjs` with jsdom available, then rebuild HTML so the comparison page embeds the updated static figures.
