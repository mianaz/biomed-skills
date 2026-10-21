# Generic biomedical primitives

18 native SVG icons following the current flat palette and 1.6-unit outline:

- Five protein nodes: rounded rectangle, capsule, circle, connected domains and complex.
- Three ligand shapes: circle, downward triangle and diamond.
- Four receptor symbols: Y, cup, single-pass and paired stems.
- Four RNA notations: wavy single strand, one-sided comb, duplex ladder and hairpin.
- A bilayer segment and a bilayer vesicle.

Open [preview.html](preview.html) to select a symbol, change its name/color and export a labeled SVG. Rounded protein and capsule width/height are adjustable. The canonical icons contain no text; the editor adds a separate annotation group. Edited protein dimensions also update exported anchor metadata. PNG downloads are transparent renders of the vector, not generated source images. The editor is self-contained and works offline.

## Reference scope

BioRender public lightboxes for [Blank Pathway (Linear)](https://www.biorender.com/template/blank-pathway-linear) and [RNA Secondary Structures](https://www.biorender.com/template/rna-secondary-structures) were visually inspected. Only their symbol conventions informed the new, directly authored geometry. No BioRender artwork was copied or traced. Existing package native membrane, ligand and mRNA symbols were also checked before extending the native family. Original SVG geometry uses the package MIT license.

Primary structure metadata for [RNA duplex 1RNA](https://www.rcsb.org/structure/1RNA) and [RNA tetraloop 1ZIH](https://www.rcsb.org/structure/1ZIH) was read to check paired versus looped strand topology. Coordinates were not used. The flat ladder is a duplex symbol, not a representation of RNA helical geometry. The hairpin has one continuous backbone; its rung count is illustrative. Y-shaped receptor identity is set by the consuming label and must not be inferred from shape alone.

## Rebuild

With Python and CairoSVG, run from the package root:

```sh
python skills/scientific-visual-explainer/assets/biomed-icons/generic-primitives/build.py
python skills/scientific-visual-explainer/assets/biomed-icons/generic-primitives/build_preview.py
python skills/scientific-visual-explainer/scripts/build_icon_atlas.py
```

`build.py` writes the 18 SVGs, 480-pixel alpha PNG previews and manifest/catalog entries. `build_preview.py` embeds the source SVGs and shared motion engine into the offline editor, and writes its two assembly models. Reuse the registered partner scales: triangle ligand 0.6 with Y receptor 1.0; circular ligand 0.7 with cup receptor 1.0. The membrane plane is y=105 in either receptor's local coordinates. Direction and sequence labels remain separate annotations.
