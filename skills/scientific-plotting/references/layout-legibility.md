# Layout and Legibility Checklist

Use this before considering a plot finished. The most common failure is not the plot type; it is unreadable labels. Apply the shared rules in [visual standards](../../biomed-shared/visual-standards.md).

## Axis labels

- Follow the plotting default in [visual design](visual-design.md#plan-physical-space-together-with-typography): categorical x-axis labels start at 45° for two or more groups.
- Keep numeric ticks and single-group labels horizontal unless the layout needs another angle.
- Use 90° only when a specific layout, such as a dense heatmap, needs it; inspect the result at final size.
- Wrap long labels before plotting: `stringr::str_wrap(label, width = 18)` for compact axes, `width = 25-40` for pathway names.
- Prefer `coord_flip()` for ranked bars, pathway names, or any category labels longer than a few words.
- Use explicit ordering with `forcats::fct_reorder()`, `factor(levels = ...)`, or tidyplots `reorder_x_axis_levels()`.

## Label overlap

For data labels required by the reading task, use native repulsion or reduce
labels. Use native scales/guides for group keys; see
[native controls](template-first-layout.md#prefer-native-controls-and-data-driven-layout).

```r
library(ggrepel)
p + ggrepel::geom_text_repel(
  aes(label = label),
  box.padding = 0.35,
  point.padding = 0.2,
  max.overlaps = Inf,
  min.segment.length = 0
)
```

For tidyplots:

```r
p |>
  add_data_labels_repel(
    label = gene,
    data = filter_rows(label_me),
    background = TRUE,
    box.padding = 0.25,
    max.overlaps = Inf
  )
```

For dense UMAPs, label broad cell types only. If there are more than 12-15 groups, prefer a legend or split panels over `label = TRUE`. For high-cardinality embeddings (>15 groups) with luminance-adaptive numbered median badges or grey-underlay subset emphasis, read [CNS panel patterns](cns-panel-patterns.md#high-cardinality-embeddings--15-clusters).

## P-values and annotations

- Show numeric P labels such as `0.013`; put the test and adjustment in the caption.
- Follow the visibility policy in [statistics.md](statistics.md) (use `nonsignificant = "value"` for primary or requested contrasts).
- When brackets risk colliding with large markers, log scales or adjacent comparisons, read and apply the **3 pt device-space clearance rule** in [stat-bracket-layout.md](stat-bracket-layout.md).

## Legends

Use native ggplot scales, `guides()` and `theme()`. Keep the key vertical; do not
default to a bottom horizontal key or construct a separate legend plot.

- Place legends and colour keys in existing white space inside the plot when the complete key fits without covering data, intervals, labels or statistics. Otherwise use the right side outside the plot, for both tall and wide panels.
- For many groups, use multiple columns: `guides(color = guide_legend(ncol = 2, override.aes = list(size = 3)))`, leaving explicit right-column margin so long category labels do not touch the next column's badges.
- Remove redundant legends when direct labels or facet labels already identify groups.
- Do not let a legend consume more visual weight than the plotted data.

For a clear upper-right corner in ggplot2, set the location explicitly after
inspecting the plot:

```r
p + theme(legend.position = "inside",
          legend.position.inside = c(0.98, 0.98),
          legend.justification = c(1, 1),
          legend.background = element_blank())
# Fallback when the key does not fit inside:
p + theme(legend.position = "right", legend.justification = "center")
```

## Figure size

- Follow [visual standards](../../biomed-shared/visual-standards.md) and [physical-space guidance](visual-design.md#plan-physical-space-together-with-typography): start within a 50 × 50 mm complete canvas, then reduce unused width while preserving data-panel height.
- Simple grouped comparisons often suit narrow, tall areas. Long labels or many categories need content-based dimensions; wrap labels before adding width.
- For tidyplots on a fixed full canvas, use `adjust_size(width = NA, height = NA)` and explicit export dimensions; inspect the resulting panel aspect ratio.
- For ggplot2/cowplot, use `export_biomedical(p, stem, width_mm, height_mm, placed_width_mm)`.

## Multi-panel composition and Nature tool-comparison format

Individual, standalone panels are first-class. For manuscript-wide PowerPoint figure planning and assembly, route to [figure-plan](../../figure-plan/SKILL.md) and export letter-free panels.

When the user explicitly requests a single-file multi-panel R/Python composite or a **Nature two-column tool-comparison figure** (outside PowerPoint assembly):

- Use the verified dimensions for the named journal and submission stage. Build each panel for its final placement; resize its source typography before assembly when needed.
- Put bold lowercase panel letters (`a`, `b`, `c`) at the top-left of their panels and keep Arial throughout.
- Give each tool family or biological condition one fixed color across every panel (`palette.csv`). Use [color policy](color-policy.md) for user choices, existing maps and new palettes; never rely on red versus green alone.
- Give each shading or intensity scale one meaning throughout the figure.
- Prefer **one hero panel plus subordinate evidence panels** over a uniform grid of equal-sized subplots. Progress overview → deviation → relationship so no two panels duplicate evidence.
- Write the legend separately: one bold title sentence, followed by one sentence per panel in letter order (`a, ... b, ...`), defining all abbreviations, `n`, biological unit, summary and statistical test.

## Final Audit

Before saving final outputs, check:

- Axis titles include units where applicable; complete gene symbols are quoted inside `italic("...")` and proteins/units remain upright.
- Tick labels fit and are not clipped.
- Multi-group categorical x labels use 45° unless a specific override applies; legends use clear internal space or the right-side fallback.
- Every color mapping has a readable legend or direct label and is saved in `palette.csv`.
- Effective text size meets the shared role targets at `placed_width_mm`; record dense-label exceptions and their measured size.
- No panel title, strip label, p-value bracket, or legend overlaps data marks.
- Direct source data and full precision `statistics.csv` have been saved.
