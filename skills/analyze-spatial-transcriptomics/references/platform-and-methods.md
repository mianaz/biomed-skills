# Spatial platform and method guide

## Match claims to measurement units

| Platform class | Typical unit | Dominant risk | Safe claim shape |
|---|---|---|---|
| Spot-based capture | Mixed-cell spot | Composition and partial-volume mixing | Spatial expression or estimated composition per spot |
| Bead/bin/high-density capture | Bead or chosen bin | Resolution-dependent sparsity and diffusion | Pattern at the declared bin/scale |
| Segmented imaging | Assigned transcripts per segmented cell | Segmentation and transcript assignment | Cell-level expression conditional on segmentation QC |
| Molecule-level imaging | Transcript coordinate | Detection efficiency and cell/compartment assignment | Molecule pattern at observed field and detection process |

Do not transfer thresholds or neighbor definitions between platform classes without
checking physical units, coordinate conventions, and capture geometry.

## Spatial graph decisions

- Use platform topology when it is known; otherwise define radius/k-nearest/Delaunay
  neighbors in physical units tied to the biological question.
- Check edge-length distribution, boundary effects, disconnected components, tissue
  holes, and section mixing.
- Run reasonable graph-scale sensitivity checks. A result that appears only at one
  arbitrary radius is fragile.
- Build and test graphs within sections unless an explicit registration creates a
  meaningful cross-section coordinate system.

## Spatially variable genes and domains

- Define the expression universe and multiplicity family before testing.
- Account for mean expression/detection and section effects; highly expressed genes
  can dominate naive autocorrelation rankings.
- Use domain methods to answer a tissue-partition question, not as mandatory clustering.
- Compare with expression-only clustering and histology without treating visual
  agreement as an independent statistical test.
- Validate domain markers and boundaries across sections or with known anatomy.

## Neighborhood enrichment

The null model must preserve relevant structure: section membership, cell/spot density,
boundaries, and often cell-type abundance. Global label shuffling can be anti-
conservative in heterogeneous tissue. Prefer per-section effects and combine or model
them at the biological-unit level. Report expected and observed contacts, effect size,
uncertainty, and corrected significance—not only a colored matrix.

## Deconvolution and mapping

- Match the reference by organism, tissue, disease/state, and granularity.
- Avoid reference labels finer than the spatial assay can distinguish.
- Check shared genes, identifier mapping, missing states, reconstruction/residuals,
  marker recovery, and proportion sums.
- Compare reasonable references or methods when the result drives a major claim.
- Treat zero proportion, below-detection, and absent reference state distinctly.
- Use orthogonal histology, imaging, or marker panels where available.

## Histology and region assignment

Image segmentation thresholds and morphology settings are section-specific. Do not
port a fixed luminance threshold or pixel radius as a universal recipe. Validate tissue
masks and regions visually on every section, preserve the coordinate transform, record
manual edits, and test downstream conclusions against plausible segmentation changes.

For Visium-style arrays, derive adjacency from platform coordinates or a validated
spatial graph rather than hand-coding one assumed hex-grid convention. Coordinate
schemas and resolutions vary across pipelines and platform generations.

## Output contract

Preserve the analysis-ready spatial object plus section-level QC, spatial graph,
feature-statistics table, domain/neighborhood results, deconvolution proportions and
uncertainty, coordinate tables, and cross-section stability summaries. Figures and
image-display records belong to `create-scientific-figures`; the scientific result
tables remain here.
