---
name: analyze-spatial-transcriptomics
description: Analyze spatially resolved transcriptomics across spot-based, bead/bin-based, and segmented imaging platforms, including spatial QC, tissue domains, spatially variable genes, neighborhood enrichment, reference-based deconvolution, and cross-section comparisons. Use for Visium/Visium HD, Slide-seq, Stereo-seq, Xenium, MERFISH, MERSCOPE, and related data. Preserve section/donor replication, coordinate-image alignment, platform resolution, and geometry-aware null models; do not equate a spot with a cell or spatial autocorrelation/proximity with biological causation.
---

# Analyze Spatial Transcriptomics

Start from the measurement unit the platform actually provides. A spot, bead, bin,
segmented cell, transcript, and inferred cell-type proportion support different claims.

## Classify the platform and question

1. Identify platform class, resolution, capture/segmentation unit, coordinate system,
   tissue image, section, donor, condition, and available reference data.
2. State whether the question concerns spatial expression, domains, cell composition,
   neighborhood association, ligand-receptor plausibility, or alignment across
   sections.
3. Preserve every section and donor as a biological/technical unit. Spots or cells
   within one section are not independent condition replicates.
4. Use a matched single-cell reference only when deconvolution or label transfer is
   necessary, and document species, tissue, state coverage, and platform compatibility.

## Gate analysis by platform

- For spot-based assays, quantify tissue coverage, library complexity, spot mixture,
  and image/coordinate registration. Treat cell-type output as proportions or
  composition estimates unless single-cell resolution is independently established.
- For bead/bin/high-density assays, justify binning or aggregation and test whether
  conclusions change with resolution.
- For segmented imaging assays, prioritize segmentation, transcript assignment,
  cell-boundary, negative-control, and field-of-view QC before biological clustering.

Read `references/platform-and-methods.md` before choosing a spatial graph, null model,
domain method, or deconvolution workflow.

## Run the analysis

1. Perform platform-appropriate QC per section and preserve spatial coordinates,
   tissue masks, transformations, and image alignment.
2. Normalize or model counts without erasing section structure; avoid pooling sections
   before examining section-specific effects and coverage.
3. Build a spatial graph from the platform geometry and biological scale of interest.
   Do not assume a hard-coded hex grid, radius, or neighbor count applies to all data.
4. Test spatially variable features with a method and null that account for spatial
   autocorrelation; correct across the tested feature family.
5. Infer domains only when expression and spatial continuity are scientifically useful.
   Compare expression-only and spatially informed results and assess parameter and
   section stability.
6. For neighborhood enrichment, preserve cell/spot density and section structure in
   the null. Summarize effects across biological sections rather than pooling all
   neighbor pairs.
7. For deconvolution, check reference coverage, reconstruction, marker plausibility,
   residuals, uncertainty, and sensitivity to reference/method. Proportions are
   estimates, not observed cell counts.
8. Route spatially constrained ligand-receptor questions to
   `infer-cell-cell-communication` after spatial and annotation QC.

## Validate and interpret

- Require recurrence across sections/donors or label single-section findings as
  descriptive.
- Distinguish tissue architecture, density, and segmentation effects from biological
  neighborhood preference.
- Moran's I or another spatial statistic measures pattern/autocorrelation, not function
  or causation.
- A spatial domain is a model-dependent partition, not automatically an anatomical
  compartment.
- Colocalization or proximity supports opportunity for interaction, not signaling.
- Report resolution, graph scale, null model, uncertainty, section support, and any
  histology-guided decisions with every major claim.

## Compose with the suite

- Use `annotate-single-cell-types` for reference labels and cell identities.
- Use `integrate-single-cell-data` only for justified expression-space correction
  whose scRNA/snRNA assumptions fit; it does not perform spatial registration.
  Preserve coordinates and raw section identities, and use platform-aware
  image/coordinate registration separately.
- Use `create-scientific-figures` for spatial maps, image integrity, common scales,
  source coordinates, and export.
- Use `ensure-biomedical-reproducibility` for platform files, coordinate transforms,
  references, parameters, and artifacts.
- Require `verify-biomedical-analysis` to audit section replication, spatial nulls,
  deconvolution assumptions, coordinate/image alignment, and claim language.
