# Generic biomedical primitives

Basic mode offers 14 current symbols: one capsule protein, three ligands, Y/U receptor monomers, matching Y/U dimers, four RNA notations, a membrane segment and a vesicle. Generic protein complexes are multiple capsule instances.

Open [preview.html](preview.html) to edit a symbol, or the [three complete mechanisms](../../basic-mechanisms/index.html) to see the default vocabulary used in figures and animations. Canonical SVGs are text-free; the editor adds separate labels. Capsule dimensions and exported anchors can be adjusted.

The source manifest retains six archived alternatives for compatibility. They are excluded from current basic pickers and examples.

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

`build.py` writes 20 registered SVGs (14 current, six archived), 480-pixel alpha PNG previews and manifest/catalog entries. `build_preview.py` embeds the source SVGs and shared motion engine into the offline editor, and writes its two assembly models. Reuse the registered partner scales: triangle ligand 0.6 with Y receptor 1.0; circular ligand 0.7 with cup receptor 1.0. The membrane plane is y=105 in either receptor's local coordinates. Direction and sequence labels remain separate annotations.
