# Basic mechanism figures and animations

Open [index.html](index.html) for three complete figures, animation timelines and block-A comparisons. Generic proteins always use capsules. Receptors use Y/U monomers and matching dimers. Static figures and animations share the same SVG renderer and declarative source models.

- [Y cascade](figures/cascade-normal.svg)
- [U complex import and RNA output](figures/import-normal.svg)
- [Y/U convergence](figures/convergence-normal.svg)

The figures directory also contains block-A versions and PNG previews. SVG text, arrows, P badges and glyph parts stay editable. English protein/state labels use Arial; Chinese labels use a CJK font fallback. The browser player is self-contained and needs no dependencies.

Edit models.json and player.js, then run `python build.py` to rebuild the offline HTML. Optional `node render_figures.cjs` (with jsdom available) exports all six figure states and checks capsule identity, P counts, unique SVG IDs and one second of playback at 60 fps. state-check.json records those checks. The storyboard and model file identify the illustrative rules and the scope of inspected BioRender references.
