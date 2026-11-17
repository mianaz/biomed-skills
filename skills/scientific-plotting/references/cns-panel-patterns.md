# CNS 500-Panel Reproduction & Adaptation Patterns

Load this reference when adapting a template from `publication_gallery.py`, building a complex multi-layer biomedical plot (annotated matrices, high-cardinality embeddings, genomic tracks, enrichment running scores, networks, hierarchies), or debugging data-replacement failures.

These rules distill empirical findings from reproducing and second-reviewing 500 independent quantitative panels across 49 *Cell*, *Nature* and *Science* papers.

## 1. Bridge raw user data to template input contracts

Gallery adapters in `assets/publication-gallery/catalog.json` separate **upstream statistical/geometric calculation** from **panel rendering**. Before staging a template with `publication_gallery.py stage`, inspect its `inputs` and `example_basis`:

| Template input archetype | Typical `adapt-data/` tables | How to adapt for new user data |
|---|---|---|
| **Raw / summary measurement adapter** | `data.csv` (observations + group summaries), `annotations.csv` (P brackets) | Compute group means/SD/CI and design-appropriate tests in R/Python first, then write both tables matching the schema column names. |
| **Precomputed density / violin / ridgeline profile** | `violin_shape.csv` or `density_height` curves + `box_summary.csv` + `markers.csv` | Either compute kernel density coordinates (`density()` / `scipy.stats.gaussian_kde`) and quartiles from the user's raw observations to populate the profile tables, or switch to a native `geom_violin()` / `ggridges::geom_density_ridges()` layer if exact source profile geometry is unnecessary. |
| **Survival knot / trajectory curve adapter** | `curve_knots.csv` (`day`, `survival_percent`), `annotations.csv` | Fit `survival::survfit()` / `lifelines.KaplanMeierFitter` on raw censored event times first, export the step coordinates and risk counts, and replace the printed log-rank P value. |
| **Embedding + backdrop / velocity adapter** | `data.csv` (`umap1`, `umap2`, feature), `ellipses.csv` or vector field grid | Supply real upstream PCA/UMAP/RNA-velocity coordinates; never invent coordinates. Recompute cluster hull/ellipse bounds from the new coordinate range. |
| **Hierarchy / network / flow adapter** | `nodes.csv`, `edges.csv` or `flows.csv`, `source-selection.csv` | Read `id` and `parent_id` explicitly as strings (`colClasses = "character"` in R; `dtype={"id": str, "parent_id": str}` in pandas) so leading-zero labels (`001`, `002`) never collapse into integers. |

## 2. Dynamic resilience when replacing data

When writing or adapting any plotting script so it survives new categories, larger sample sizes or shifted numeric ranges, enforce these six invariants learned from the 500-panel second code reviews:

1. **Dynamic axis windows (`display-view.csv` / data-driven bounds)**:
   - Never hardcode fixed `xlim` / `ylim` that clip new observations or extended error bars. Compute lower and upper limits from the union of observations, summary interval endpoints (`ymin`, `ymax`), and bracket labels (`range(c(obs$y, summary$upper, brackets$top), na.rm = TRUE)`).
2. **Dynamic size-legend and color-bar bounds**:
   - In dot matrices and bubble plots (e.g., Seurat-style `% expressed` × `average expression`), derive size-legend breaks from the observed maximum when new values exceed the reference range (e.g., if reference breaks stop at `0.25` and new data reach `0.35`, append or rescale up to the observed maximum rather than clipping larger bubbles).
3. **Graceful palette extension for added categories**:
   - Preserve explicit group → hex mappings from `palette.csv`. If replacement data introduce more categories than the fixed palette contains and no explicit colors are supplied, either require an extended named palette (`biomedical_palette()`) or generate deterministic evenly spaced HSV/HCL fallback colors for unmapped categories so R and Python never silently recycle a 6-color vector or drop groups to `NA` gray.
4. **Data-driven facet grid dimensions**:
   - In multi-panel facet grids ( especially Matplotlib `subplots`), compute `panel_rows = math.ceil(len(observed_panels) / panel_columns)` dynamically from the observed levels in the data, iterate over all observed panels, and hide only trailing unused axes (`ax.set_visible(False)`).
5. **Metadata-driven annotations and panel cues**:
   - Never branch on hardcoded biological strings in plotting code (e.g., `if (cluster == "T_EX CD8+") nudge_x = 0.08` or `if (tissue == "Liver")`). Store label nudges, guide-line heights, conditional flow denominators and axis-cue panel indices (`cue_panel_order`) as columns in editable table inputs with neutral fallbacks for new groups.
6. **Never infer sample size from digitized or subsampled display rows**:
   - When a plot title or caption reports total cells or samples (e.g., `n = 4,403 cells`), read the true upstream count from metadata (`display-settings.csv`) rather than `nrow(display_points)` if the scatter layer was downsampled or density-binned.

## 3. High-impact CNS encoding recipes

### High-cardinality embeddings (> 15 clusters)
- **Numbered median badges + separate key**: Place circle badges (`shape = 21`, `size = 5–6`) at each cluster's median `(DR1, DR2)` coordinate with cluster index `1..K` centered inside.
- **Luminance-adaptive numeral contrast**: Compute relative luminance $L = 0.2126 R + 0.7152 G + 0.0722 B$ of each cluster's fill color; draw the numeral in black (`#000000`) when $L > 0.5$ and white (`#FFFFFF`) when $L \le 0.5$.
- **Right-side legend clearance**: When rendering a multi-column circle-key legend alongside the embedding, add explicit right-column text margin so long cell-type names never collide with the adjacent legend column's badges.
- **Subset emphasis (grey underlay)**: To highlight one lineage or time stage, map background cells to `#E6E6E6` (`grey85`), **sort the table so background rows draw first**, and draw highlighted cells on top.

### Annotated matrices and two-summary dot plots
- **Dot matrix (expression × detection)**: Map mean expression (or z-score) to continuous fill/color and fraction detected (`% expressed`) to **circle area** (`scale_size_area()`, never radius). Keep zero-expression/zero-detection cells unplotted or below the minimum size threshold.
- **Complex heatmaps with covariate tracks**: Keep the main matrix fixed-aspect or aligned to row/column dendrograms. Use distinct palettes for categorical sample annotations vs. continuous expression scale (`z-score` diverging scale requires an explicit `0` center). Expand canvas height/width proportionally when rows or columns are added.

### Enrichment and multi-omics composites
- **GSEA running-score composite**: Preserve the three linked layers sharing one gene-rank x-axis: (1) running enrichment score curve with peak/NES annotation, (2) vertical membership hit ticks per pathway, and (3) ranked list metric profile at the bottom. Never reduce a GSEA curve to a bar chart of rank indices.
- **Volcano / MA plots with selective repulsion**: Plot all tested features first (nonsignificant in `#D9D9D9` / `grey85`), overlay threshold lines corresponding to the exact y-axis statistic (raw $P$ vs. adjusted $P$), and label only the top or biologically specified hits using `ggrepel::geom_text_repel(..., min.segment.length = 0, box.padding = 0.35)`.
