# Review the assembled figures

Review both the saved slide objects and their rendered output. Inspect a contact
sheet for rhythm across the paper, every figure at its intended manuscript width,
and close views for clipping or image artifacts. Browser zoom alone does not
establish physical size; use the recorded dimensions and a calibrated view or
print when needed.

## Space, spacing and hierarchy

Use the panel inventory's placed bounding boxes, including axes and legends.
Treat a placeholder as a panel footprint. Treat each reversible panel group as
one footprint; count overlapping parts only once. Measure labels and shared
legends separately or include them in a documented footprint convention.

| Measure | Definition | What to inspect |
|---|---|---|
| Outer canvas fraction | `1 − envelope_area / canvas_area`; the envelope is the smallest rectangle containing every panel, letter and shared legend | Large unused side strips or excess page height. Record canvas and envelope width × height. |
| Space within the envelope | `1 − union_footprint_area / envelope_area` | Gutters, deliberate group separation and unfilled parts of staggered rows. This excludes blank space inside each asset. |
| Total external whitespace | `1 − union_footprint_area / canvas_area` | A combined diagnostic. Keep its outer and within-envelope components visible when canvas sizes differ. |
| Internal blank space | Inspect rendered panels for unused export padding and empty plotting regions; label any pixel-based estimate as approximate | White backgrounds and sparse data are not automatically wasted space. Trim export padding before changing data geometry. |
| Gutter size and ratio | Horizontal/vertical edge gaps between adjacent panels in each row/column; report mm and gap / figure width or height | Accidental narrow gaps, disconnected comparisons and inconsistent spacing. |
| Gutter-area fraction, if useful | Union area of the explicitly defined between-panel gutter strips / canvas area; exclude outer margins | Disproportionate separation. Gutter area overlaps the external whitespace measure; do not add the two percentages. |
| Panel size balance | Panel width/height and area fraction; compare primary evidence with supporting panels | Primary plots too small, a large low-information panel, or unequal sizing that distorts a comparison. |
| Display distribution | Counts of chart/image/schematic types and their consecutive runs | Monotonous redundant views or an opportunity for complementary evidence. No minimum number of chart types. |

Record the measurement convention with the values. Give gutter median/range for
the actual adjacent pairs; do not calculate gaps between every possible pair.
For staggered layouts, state which rows, columns or groups define adjacency.
Inspect overlaps and out-of-canvas objects separately; a low whitespace fraction
can also reflect crowding.

If `O` is the outer canvas fraction and `G` is space within the envelope, total
external whitespace is `O + (1 − O) × G`. The fractions use different denominators;
adding them directly is incorrect. A crop at unchanged panel scale changes `O`
but leaves `G`, embedded font size and panel geometry unchanged. Compare layouts
at the same screen scale, with their physical dimensions shown. A fit-to-width
view enlarges narrower figures and must be labeled separately.

Read the figure in letter order. Each row or visual group should advance a
question: design → observation → quantification is one useful pattern, not a
required recipe. Use a large image beside compact quantitative panels or a wide
trajectory above small comparisons when the content benefits. Align plot areas
and comparable baselines where possible, not just outer image edges. Keep paired
images and their quantification close. Preserve equal scale and size where direct
visual comparison requires them.

Choose deliberate hierarchy rather than arbitrary size variation. An aligned
grid can be the best layout. Do not change an appropriate chart merely to increase
diversity, or add panels just to fill space. Fix excess margins, long labels or
export padding before shrinking type or enlarging the whole canvas.
Check how much reading each panel requires. A simple scatterplot can occupy more
space than a dense comparison while leaving that comparison unreadable. Compare
these panels directly; total fill and group adjacency do not resolve this tradeoff.

## Typography, color and graphic style

Run the [effective typography audit](effective-typography.md) for source sizes,
final scaling, per-role ranges and unknown text coverage. Check both extremes
and cross-panel consistency before accepting a layout.

- Use the scaling rules in
  [PowerPoint assembly and export](powerpoint-and-export.md#verify-effective-size-before-export).
  Compare equivalent roles: axes with axes, ticks with ticks, letters with letters.
  Uniformity does not require a panel letter to match a tick label in size.
- Check Arial and its actual rendered glyphs, including italic genes, upright
  proteins, Greek letters, subscripts and superscripts. Inspect letters, axis
  labels, P values, legends and scale-bar labels at final viewing size.
- Keep group → color mappings fixed across main and supplemental decks. Save a
  shared `palette.csv`; subset panels reuse the same mapping. Related continuous
  scales use matching units and ranges, or a visible reason for differing ranges.
  Use shape/line style or direct labels when color alone cannot carry identity.
- Compare line width, point size, error bars, tick direction, numerical precision,
  abbreviation spelling, annotation style, borders and backgrounds across related
  panels. Keep repeated encodings consistent while allowing different evidence
  types to use their appropriate conventions.
- Check grayscale/color-vision previews through the plotting workflow when color
  carries group identity. Inspect actual marks and legends, not only the palette.
- Preserve image crops, aspect ratios, channels, comparable display ranges and
  calibrated scale bars. Fix a panel's embedded labels in its plotting source;
  enlarging only the PPT letter does not improve its internal type.
- Mark rasterized text size as unmeasured when its source size is unavailable.
  An imputed font size may serve an experimental model input, but cannot pass a
  typography check. Higher export DPI does not recover missing source detail.

## Save a short review

Use one row per figure. The plan template includes suitable fields. Report
external whitespace %, gutter median/range and normalization, panel area balance,
display counts, effective font range by role, minimum raster PPI, palette/style
issues and the resulting edit or justified choice. Use `unmeasured` for unavailable
values, with the specific reason. Do not invent precise measurements from a glance.

Record which renderer produced the inspected images and whether PowerPoint was
opened. Add a small annotated HTML review when it makes an issue easier to locate.
The contact sheet must show the actual deck renders. A coded layout sketch can
supplement this review but cannot serve as proof that the PPTX rendered correctly.

Fix observed problems and inspect the affected final exports again. A pass means
readable, faithful evidence and a coherent figure at the chosen size; whitespace
or chart diversity alone cannot establish it.
