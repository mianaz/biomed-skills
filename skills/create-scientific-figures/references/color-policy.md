# Resolve and retain the color mapping

Choose colors before drawing the first plot. A palette is a mapping from semantic
levels to colors, not a list assigned anew by row order or plotting defaults.

## Precedence

1. Apply explicit user colors or the user's selected reference figure. An override
   for one condition changes that condition; preserve the other known mappings.
2. Reuse the current project's saved palette or supplied contextual figures. Within
   a figure set, keep each condition's color across outcomes, subsets and chart types.
   Match conditions by identity, including documented aliases, not legend position.
3. With no specification or usable context, use the same default family for a
   standalone plot and a new figure set. Do not choose a new palette for each task.

For a new categorical mapping, `biomedical_palette()` uses the full 11-color
[CARTO Bold palette](https://carto.com/carto-colors/), in its original order
(`rcartocolor::carto_pal(11, "Bold")`):

`#7F3C8D`, `#11A579`, `#3969AC`, `#F2B701`, `#E73F74`, `#80BA5A`,
`#E68310`, `#008695`, `#CF1C90`, `#F97B72`, `#A5AA99`.

An ordinary two-condition comparison starts with purple/green. For an identified
control/reference, reserve `#666666` and start the other conditions with purple;
do not invent a control. Blue and orange remain part of larger mappings. This is a
default ordering, not a ban on either color or a requirement to install a palette package.

New levels are sorted by name for deterministic assignment. Existing mappings always
win, including earlier blue/orange pairs; unused default colors extend the map without
recoloring existing levels. R and Python use the same values. Supply the same complete
level set and existing mapping to obtain the same assignments in both languages.
When unused colors run out, supply a larger explicit named palette and additional
visual encoding; never silently recycle colors. Inspect distinguishability at the
actual size, including small marks and color-vision/grayscale views; add shape or
line encoding when needed. The palette name alone does not establish accessibility.

Build the mapping from all conditions in the supplied dataset/figure set before
filtering panels. Save it, and pass it back as `existing` for later figures. Two
separately initialized subsets cannot recover a shared mapping without this context.
Keep separate maps for different variables, such as condition and cell type. Use
stable data IDs as map keys; shorten or add `%` to display labels via the scale's
`labels` argument, without changing keys after assigning colors.

The categorical default does not replace continuous, ordered-dose or signed-effect
scales. Without context, use viridis option D (low to high) for continuous magnitude;
for signed effects around zero, use blue `#2166AC`, neutral `#F7F7F7`, red `#B2182B`.
Reuse the palette, direction, center and limits for the same comparable quantity
across panels. Preserve a supplied channel or assay color convention.

## Recover colors from supplied figures

Inspect available context automatically; do not ask for hex codes when the mapping
can be recovered. Use only files or figures provided/authorized as task context.
For a blinded task, evaluator-only reference figures are not palette context.
Templates supplied only for analysis/chart-type reference are also excluded from
palette inheritance. Use their data/encoding ideas within the user's stated scope.

- Prefer a saved palette, plotting source, Prism project or RDS. Recover the named
  condition mapping, not just the set of hex codes. For a ggplot object, inspect the
  trained color/fill scale and its labels; check which variable that scale encodes.
- With SVG/PDF only, inspect the legend/direct labels and recover the corresponding
  vector fill/stroke colors where possible. Distinguish data colors from axes/text.
- With a raster image only, view it, identify each labeled legend key or unambiguous
  group mark, and sample representative interior pixels using available image tools.
  Avoid antialiased edges, text, the background and transparency-blended pixels.
  Retain the closest supported colors and record raster-derived values as approximate;
  visual matching alone is not an exact source-color extraction. Pixel frequency
  does not establish which condition a color represents.

Verify the recovered colors against the reference image before using them. If
references disagree, follow an explicitly selected/current canonical figure. If no
reference resolves a material condition-color conflict, ask only about that mapping;
do not silently swap identities. Extend a partial known map for new conditions using
unused colors from the default family.

## Apply, save and check

Use the same named vector for a condition's fill, point/line color, legend key and
direct statistical label. Keep any intentional alpha differences explicit. Adding
a new plot, changing legend order or dropping a group must not reassign colors.

Save one reusable `palette.csv` with `variable`, `level`, `color`, and `source`
(e.g. CARTO Bold default, user choice, or reference file and panel); record approximate extraction
in `source` or the notes. Retain the full known mapping, including levels absent
from the current panel. A figure set shares this file instead of inventing separate
maps for each panel. Existing project formats can be retained if equally explicit.

Check actual plotted marks and legends against this map after rendering. In R,
inspect `ggplot_build(p)$data` and the trained scales; an unknown level turning gray
is a mapping failure even when export succeeds. Check cross-panel consistency by
condition identity, not by the left-to-right sequence of colors.

## Preview the rendered colors

For color-encoded groups or values, run this on the final PNG from either plotting
language. Paths are relative to the skill folder; the helper uses R packages `png`,
`colorspace` and `ragg`. An equivalent installed simulation tool can be used in a
Python-only environment; keep the plotting language and dependencies unchanged.

```bash
Rscript --vanilla scripts/color_preview.R output/figure.png output/figure-color
```

The helper preserves the original and writes grayscale, protan, deutan and tritan
views plus a labelled comparison sheet. Individual views retain the input pixel
dimensions; compare them at the figure's intended placement rather than shrinking
the whole sheet to a single-panel width. Transparent pixels are composited on white
for the diagnostic views, which assume sRGB input and use 8-bit RGB. CVD simulations
use severity 1; they are viewing aids,
not a certification of accessibility or a prediction of every reader's perception.

Check actual overlapping curves, small points, heatmap ranges and their keys. When
identity becomes unclear, use one targeted cue such as direct labels, distinguishable
line types or point shapes, then inspect again. Preserve established colors unless
the user requests a change. Keep these diagnostic images outside manuscript exports.
