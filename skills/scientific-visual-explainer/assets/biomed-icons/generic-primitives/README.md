# Generic biomedical symbols

38 current native SVG symbols use the Nord mist palette. Generic proteins remain capsules; Y/U receptor monomers have separate matching dimer assets. The six archived alternatives remain available for compatibility.

Open `preview.html` for the icon picker, labels and SVG/PNG downloads. `compositions.html` shows expression, ubiquitin/proteasome turnover and membrane traffic using the same icons. Each assembly has an editable SVG under `assemblies/`.

`references.json` links public visual examples and scientific references. The package contains original vector geometry; local papers and third-party reference images stay outside the distribution.

Build icons with `python3 build.py` using CairoSVG, then run `python3 build_preview.py` and `python3 build_compositions.py`. Palette roles come from `../../basic-mechanisms/palettes.json`. Keep text and biological annotations in the consuming figure.
