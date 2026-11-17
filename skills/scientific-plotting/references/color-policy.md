# Resolve and retain the color mapping

Choose colors before drawing the first plot. A palette is a mapping from semantic
levels to colors, not a list assigned anew by row order or plotting defaults.

## Precedence

1. Apply explicit user colors or the user's selected reference figure. An override
   for one condition changes that condition; preserve the other known mappings.
2. Reuse the current project's saved palette or supplied contextual figures. Within
   a figure set, keep each condition's color across outcomes, subsets and chart types.
   Match conditions by identity, including documented aliases, not legend position.
3. With no specification or usable context, choose a suitable categorical or
   continuous family for the task and keep it consistent across the figure set.

For categorical data, consider ggsci NPG, AAAS, NEJM, Lancet or JCO, Brewer palettes,
or a user-supplied palette. NPG is inspired by Nature Reviews Cancer figures; it
is not a Nature-wide requirement ([ggsci documentation](https://nanx.me/ggsci/reference/pal_npg.html)).
Evaluate category count, contrast and scientific meaning rather than journal branding.

`biomedical_palette()` accepts `palette="npg"` (helper fallback), `"aaas"`, `"nejm"`,
`"lancet"`, `"jco"`, `"paired"`, a color vector, a named identity-to-color mapping,
or a function taking the required color count. R and Python share
`assets/palettes.json`; package callbacks and explicit hex vectors extend these choices.

```r
pal <- biomedical_palette(all_groups, existing = known_colors, palette = "npg")
pal <- biomedical_palette(all_groups, palette = ggsci::pal_jco())
pal <- biomedical_palette(all_groups, existing = known_colors,
                         palette = c(Treatment = "#6A3D9A"))
```

Python uses `palette="npg"`, a sequence of hex values, a dictionary of named
overrides, or a callable `palette(n)`. A named user override takes precedence over
`existing` for those identities; unnamed pools fill only unmapped identities.

An explicitly identified control/reference can use `#666666`. Match the condition's
bar, sample points and lines.

New levels are sorted by name for deterministic assignment. Existing mappings are
retained unless explicitly overridden; unused selected colors extend the map without
recoloring existing levels. R and Python use the same values. Supply the same complete
level set and existing mapping to obtain the same assignments in both languages.
When unused colors run out, supply a larger explicit named palette and additional
visual encoding; never silently recycle colors.

Build the mapping from all conditions in the supplied dataset/figure set before
filtering panels. Save it, and pass it back as `existing` for later figures. Two
separately initialized subsets cannot recover a shared mapping without this context.
Keep separate maps for different variables, such as condition and cell type. Use
stable data IDs as map keys; shorten or add `%` to display labels via the scale's
`labels` argument, without changing keys after assigning colors.

Choose a continuous scale by quantity: sequential for increasing magnitude,
diverging for deviations around a meaningful reference. Examples include viridis
or Brewer Blues for sequential values, and RdBu or another balanced diverging
scale for signed effects or gene z-scores. Supply native scale functions or
`circlize::colorRamp2()` with user-selected colors and explicit limits. Discrete
NPG colors do not form a universal continuous scale. Record direction and center;
retain comparable mappings across panels and supplied assay/channel conventions.

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
unused colors from the selected family.

## Apply, save and check

Use the same named vector for a condition's fill, point/line color, legend key and
direct statistical label. Keep any intentional alpha differences explicit. Adding
a new plot, changing legend order or dropping a group must not reassign colors.

Save one reusable `palette.csv` with `variable`, `level`, `color`, and `source`
(e.g. ggsci NPG, user choice, or reference file and panel); record approximate extraction
in `source` or the notes. Retain the full known mapping, including levels absent
from the current panel. A figure set shares this file instead of inventing separate
maps for each panel. Existing project formats can be retained if equally explicit.

## Optional color diagnostics

Separate palette audits, grayscale/CVD simulations and comparison sheets are not
part of ordinary plotting. Run `scripts/color_preview.R` only when the user asks
for that specific diagnostic. Preserve the selected template or project mapping.
