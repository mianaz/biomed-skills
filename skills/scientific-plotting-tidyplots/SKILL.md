---
name: scientific-plotting-tidyplots
description: Create or refine biomedical research figures in R with tidyplots as the default. Use for a tidyplots workflow with Arial, readable text at final placement, design-supported statistics, editable plots and direct source data. Shares the scientific-plotting standards in this package.
---

# Scientific Plotting with tidyplots

Version 1.1.2

Use tidyplots for ordinary biomedical plots from tidy tables. Use cowplot for the
theme and, when needed, assembly. Honor an explicit tool choice or an existing
validated analysis. Use a specialized plotter when tidyplots would change or hide
the required evidence; explain that choice briefly.

This variation ships with `scientific-plotting`. Read its
[shared workflow](../scientific-plotting/SKILL.md) before plotting; apply its scope,
data, statistics, color, scientific typography, inspection and delivery rules.
Use the construction and sizing defaults in the
[tidyplots route](../scientific-plotting/references/tidyplots.md). Resolve those
shared workflow paths relative to the `scientific-plotting` folder.

## Apply the R route

1. Identify the experimental unit, units, pairing, missing values and supported
   comparison. Preserve supplied valid results. Select tests from the study design
   before plotting; a package default does not establish a valid analysis.
2. Check the chosen R environment once. Add `tidyplots` to the core R packages in
   the shared quickstart. Check the installed API with `packageVersion()` and help;
   the online development reference can contain functions absent from a release.
3. Build with `tidyplot()` and its `add_*()` functions. Draw summaries behind
   observations. Retain actual numeric time/dose spacing and matched unit IDs.
   For incomplete trajectories, break lines at missing observations.
4. Apply the shared cowplot theme, then `adjust_font(fontsize = 14, family = "Arial")`.
   Set sizes for text layers separately. Start scientific script-bearing labels
   at 16 pt and measure the result. Keep all text strictly above 10 pt at the
   intended placement, including facets, legends, P values and scripts.
5. Default each plot area to 50 × 50 mm and keep the font sizes above. Axes and
   legends add to the complete export size. Use `scripts/tidyplots.R` with the
   shared export helper to measure that outer size on a Cairo device and verify
   the saved figure at the same placement. Wrap labels and space annotations within
   the fixed plot area. Honor requested dimensions and an existing figure canvas.
   For a fixed outer canvas, use `width = NA, height = NA` for the panels and pass
   the full dimensions to `export_biomedical()`; inspect whether the labels fit.
6. Compute inference outside the drawing pipeline and save the full results. Use
   the shared `p_labels()` / `p_brackets()` helpers to show keyed, precomputed results
   with the shared annotation policy. Default P-value labels to 12 pt. Add about
   0.8 mm of space above the bracket with `text_gap` in y-axis units.
7. Save PDF/PNG, `.rds`, plotting code, direct plotting tables, summaries/intervals,
   full statistics, palette, versions and a concise caption. Inspect the actual
   export and final assembly for typography, overlap, clipping, colors and data
   fidelity. Measure effective type size at the intended placement before delivery.

## Run the examples

From this skill folder:

```bash
Rscript --vanilla examples/run.R /tmp/tidyplots-examples
```

The three synthetic teaching examples cover independent groups, paired donors
with scientific notation, and faceted trajectories with uneven time spacing and
missing observations. They save editable sources and data, and use the shared
export checks. Open every saved image; automated checks cannot detect all defects.
