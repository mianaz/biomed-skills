# Statistical Bracket Layout and Device-Space Clearance

Load this reference when placing pairwise P-value brackets or statistical comparison lines on categorical, grouped, dodged, log-scale or faceted plots.

## Why data-proportion offsets fail

Standard helpers (`rstatix::add_xy_position()`, `ggpubr::stat_pvalue_manual()`, `ggsignif::stat_signif()`, Python `statannotations`) space brackets using a fraction of the y-axis data range (`step.increase`). When canvas height changes, y-limits are adjusted, log transformations are applied, or facets have free y-scales, range-proportion offsets either collide with point strokes/error bars or waste vertical space.

Use native annotation functions for new publication figures. Tune their spacing
and inspect the rendered clearance. The custom device-space algorithm below is
reserved for an explicit custom-layout request or exact source replication.

## 1. Native package route

- **R (`rstatix` + `ggpubr`)**: Compute positions from the actual summary or max observation, accounting for dodge and `y.trans`:
  ```r
  stat.test <- df |>
    rstatix::t_test(value ~ group, ref.group = "Control", var.equal = FALSE) |>
    rstatix::adjust_pvalue(method = "holm") |>
    rstatix::add_xy_position(x = "group", fun = "max", step.increase = 0.12)
  ```
  Filter according to the visibility rule (primary/requested contrasts use `nonsignificant = "value"`) **before** assigning lanes so hidden comparisons never reserve blank vertical headroom.
- **R (`tidyplots`)**: Compute inference outside the drawing pipeline and pass keyed results to `ggpubr::stat_pvalue_manual()` through `add()`, or tune `padding_top`, `step.increase` and `bracket.nudge.y` in `add_test_pvalue()` and verify rendered clearance.
- **Python (`statannotations`)**: Pass precomputed adjusted P values via `Annotator.set_pvalues_and_annotate()` with `text_offset = 3` (in points), then inspect the saved PDF to verify the first bracket clears the highest visible mark.

## 2. Explicitly requested custom device-space layout

When brackets collide with large point markers, log-scale ticks or neighboring comparisons, compute bracket coordinates in **final device space** (`1 pt = 1/72 inch`; `bigpts` in R `grid`, renderer `get_window_extent()` in Matplotlib):

1. **Filter visible comparisons first**: Apply `p_labels(..., nonsignificant = "hide")` (or explicit `"ns"` / `"value"` when justified). Drop hidden rows before computing geometry; zero visible comparisons means zero bracket headroom.
2. **Order by span**: Sort visible comparisons from shortest horizontal group span (`|x2 - x1|`) to longest so local adjacent contrasts sit closest to the data and wider brackets stack cleanly above them.
3. **Measure the true upper mark envelope**: Within the horizontal span `[x1, x2]`, find the highest visible graphical element—not just the data numeric maximum (`max(y)`), which ignores point radius and stroke width:
   - Include point marker radius + half stroke width (e.g., in SVG/device points), upper error-bar cap stroke, or violin/boxplot upper tip.
   - On log axes (`log10`), convert the data coordinate to device y-position *before* adding point radius and clearance in points.
4. **Apply 3 pt vertical clearances**:
   - Place the lower ends of the vertical bracket tips **3 pt above** the highest visible mark edge in `[x1, x2]`.
   - Make vertical bracket tips **3 pt tall** (so the horizontal bar sits 6 pt above the highest visible mark edge).
   - Place the **bottom of the P-value text bounding box** (including descenders such as the tail of lowercase `p` or subscript `adj`) **3 pt above** the upper stroke edge of the horizontal bracket bar.
5. **Stack overlapping horizontal spans**:
   - Compute each comparison's horizontal occupancy as the union of its bracket span `[x1, x2]` and its rendered P-value text width `[label_left, label_right]`.
   - If a comparison's horizontal occupancy intersects any already-placed comparison, shift the entire bracket + label assembly upward so its tip bottom sits at least **3 pt above** the top of the lower comparison's text bounding box.
6. **Recompute per output device and facet**:
   - Run the device-space pass for the target physical dimensions (`width_mm`, `height_mm`) on each output device (PDF, PNG, SVG) and independently within each `free_y` facet.
   - Expand panel y-limits (`expand` / `ylim`) to enclose the highest text bounding box plus a 3 pt top margin so `clip = "on"` never truncates the top P-value label.

## 3. Continuous curves, trajectories and survival plots

- **Never draw a horizontal x-axis bracket across time or concentration** to represent a between-group curve comparison; a horizontal bracket implies a contrast between two time points.
- Use a native model annotation or keyed native guide label for a requested curve comparison. Keep explanatory result text in the caption when the native layout has no suitable location.
- Place global/interaction model terms (e.g., `Group × Time P = 0.0042`) in the separate caption, or a suitable native annotation layer—never on a pairwise bracket.
