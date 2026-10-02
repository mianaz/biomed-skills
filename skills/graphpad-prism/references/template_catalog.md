# GraphPad Prism Template Catalog

Catalog of 115 templates from the existing local Prism skill. Template binaries
are not included. Locate the matching filename in a user-supplied collection;
confirm the actual table shape before using it.

## Survival & Clinical

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 1 | 1.Survival_Curve.pzf | Kaplan-Meier survival curve with HR, 95% CI, risk table | Survival: time + status per group |
| 82 | 82.KM_Survival_CI.pzf | KM survival with confidence interval bands, 4 groups | Survival: time + status, 4 groups |
| 35 | 35.Restricted_Cubic_Spline_RCS.pzf | Restricted cubic spline plots (4 panels: CRP, Lymphocyte, Leukocyte, Platelet) | XY: continuous predictor vs HR with 95% CI |
| 91 | 91.Clinical_Feature_Heatmap.pzf | Clinical characteristics oncoplot-style heatmap (treatment response, stage, sequencing) | Categorical matrix: patients x features |

## Volcano & Differential Expression

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 17 | 17.Volcano_Plot.pzf | Standard volcano plot with gene labels, FC and p-value thresholds | XY: log2FC vs -log10(padj), gene labels as row titles |
| 74 | 74.Protein_Differential_Volcano.pzf | Protein differential volcano (green/orange dots, labeled genes) | XY: log2FC vs -log10(P) |
| 98 | 98.Gradient_Volcano.pzf | Gradient volcano with bubble size=-log10(Padj), color=log2FC | XY: log2FC vs -log10(Padj) + size + color columns |

## Heatmaps

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 6 | 6.Correlation_Heatmap.pzf | Correlation heatmap (5x5 matrix, blue-red diverging) with r values | Matrix: variables x variables |
| 10 | 10.Heatmap.pzf | Standard heatmap (yellow-purple gradient, conditions x treatments) | Matrix: rows x columns |
| 21 | 21.Triangle_Correlation_Heatmap.pzf | Lower-triangle correlation heatmap (6x6, tissue types) | Matrix: symmetric correlation |
| 41 | 41.Split_Heatmap.pzf | Split heatmap (two-color: red=high, blue=low, cell types x samples) | Matrix: cell types x conditions |
| 56 | 56.qPCR_Heatmap.pzf | qPCR gene expression heatmap (red-blue, genes x conditions) | Matrix: genes x treatment groups |
| 62 | 62.WB_Protein_Quant_Heatmap.pzf | Western blot quantification heatmap (with WB image placeholder) | Matrix: proteins x samples (relative intensity) |
| 66 | 66.Color_Bubble_Heatmap.pzf | Bubble correlation heatmap (size+color encode coefficient, brain regions) | Matrix: regions x regions (r values) |
| 71 | 71.WB_Multi_Marker_Heatmap.pzf | Multi-band WB heatmap (2 cell types, blue gradient) | Matrix: proteins x samples |
| 76 | 76.PCR_Multi_Gene_Expression_Heatmap.pzf | Multi-gene expression heatmap (large grid, fold change) | Matrix: genes x conditions |

## Forest Plots

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 15 | 15.Color_Forest_Plot.pzf | Color-coded forest plot (HR with 95% CI, colored by biomarker category) | Grouped: variable, HR, lower CI, upper CI |
| 45 | 45.Regression_Forest_Plot.pzf | Regression forest plot (clinical variables, cDNA, proteomics sections, with table) | Grouped: variable, HR (95% CI), P-value |
| 63 | 63.Color_Label_Forest_Plot.pzf | Labeled forest plot (odds ratios, colored diamonds by significance) | Grouped: variable, OR, CI bounds, P-value |

## Bar Charts

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 12 | 12.Multi_Group_Scatter_Bar.pzf | Multi-group bar + scatter (5 treatments, colored bars, individual dots) | Grouped: replicates per group |
| 29 | 29.Multi_Group_Intervention_Bar.pzf | Intervention bar chart (WT/KO x Control/Efferocytic, with +/- indicators) | Two-factor grouped |
| 33 | 33.Two_Factor_Bar.pzf | Two-factor grouped bar (AUROC by cancer type x model) | Two-factor: models x cancer types |
| 47 | 47.Multi_Factor_Bar.pzf | Multi-factor bar (4 groups x 2 conditions, with significance) | Two-factor grouped |
| 52 | 52.Two_Group_Comparison_Bar.pzf | Two-group comparison bars (4 panels: Vehicle vs Treatment) | Paired: 2 groups, replicates |
| 67 | 67.qPCR_Segmented_Bar.pzf | qPCR segmented bar (Ctrl/OE/Scrl/KD x PBS/PFFs) | Two-factor: treatments x conditions |
| 81 | 81.Many_Group_Scatter_Bar.pzf | Many-group scatter bar (10 groups: A0-A9, with P-values) | Column: replicates per group |
| 90 | 90.Multi_Factor_Two_Group_Bar.pzf | Multi-factor 2-group bar (Confounded vs Balanced x 5 methods, 4 panels) | Multi-panel two-factor |
| 93 | 93.CCK8_Bar.pzf | CCK8 multi-timepoint bar (3 groups x 3 days) | Two-factor: groups x time |
| 101 | 101.BCA_Protein_Quant_Bar.pzf | BCA protein quantification (PF vs PC at 5 FBS concentrations) | Two-factor: condition x concentration |
| 103 | 103.Categorized_Bar.pzf | Categorized horizontal bar (sample types, colored by category) | Grouped: categories with values |
| 106 | 106.WB_Single_Marker_Bar.pzf | WB single-marker bar (4 groups, with p-values) | Column: replicates per group |
| 111 | 111.CCK8_Bar_Alt.pzf | CCK8 cell survival bar (5 treatments) | Column: replicates per group |
| 114 | 114.IF_Imaging_Bar.pzf | IF imaging quantification bar (4 groups, colored by interaction type) | Column: replicates per group |

## Stacked Bar Charts

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 2 | 2.Percent_Stacked_Bar.pzf | Percentage stacked bar (Alive/Dead, 2 groups) | Stacked: categories per group (%) |
| 8 | 8.Stacked_Bar_ErrorBars.pzf | Stacked bar with error bars (Apical/Basolateral/Attached x 4 strains) | Stacked with error: mean+SD per layer |
| 16 | 16.Stacked_Bar.pzf | Area stacked bar (5 regions over time, gradient colors) | Stacked: regions x years |
| 25 | 25.Horizontal_Percent_Stacked_Bar.pzf | Horizontal percentage stacked (mRS scores, 2 groups) | Horizontal stacked: scores per group (%) |
| 54 | 54.Faceted_Stacked_Bar.pzf | Faceted stacked bar (SPF/GF/FMT x A-D, cell types) | Multi-panel stacked: cell fractions |
| 57 | 57.Stacked_Butterfly.pzf | Butterfly stacked bar (adverse events, 2 vaccines x 3 grades, bidirectional) | Bidirectional stacked: L/R percentages |
| 83 | 83.Color_Percent_Stacked_Bar.pzf | Colored percentage stacked (Unsuc/Suc/Multiple/Single) | Stacked: categories per group (%) |
| 109 | 109.Dual_Y_Stacked_Bar_Line.pzf | Dual-Y stacked bar + line (concentration stacked + selectivity line) | Stacked + XY overlay |

## Violin & Box Plots

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 3 | 3.Scatter_Boxplot.pzf | Scatter boxplot (4 groups, colored dots) | Column: replicates per group |
| 9 | 9.Violin_Plot.pzf | Violin plot (3 groups: blue/orange/red) | Column: replicates per group |
| 34 | 34.Scatter_Violin.pzf | Scatter violin (2 groups: WT vs KO, with P-value) | Column: replicates per group |
| 37 | 37.Multi_Group_Scatter_Violin.pzf | Multi-group scatter violin (15+ drug groups, colored by category) | Column: replicates per many groups |
| 39 | 39.Multi_Factor_Scatter_Boxplot.pzf | Multi-factor scatter box (Static/Shear x Control/LPS/ATP/PMA) | Two-factor: condition x treatment |
| 69 | 69.Box_Violin.pzf | Box-violin hybrid (4 groups: Pre-R/Post-R/Pre-NR/Post-NR) | Column: replicates per group |
| 79 | 79.IF_Staining_Violin.pzf | IF staining violin (Control/FMOD/IL1B/IL1B+FMOD, with P-values) | Column: replicates per group |
| 84 | 84.Watercolor_Scatter_Boxplot.pzf | Watercolor scatter boxplot (5 groups: Q0-Q4, colored) | Column: replicates per group |
| 96 | 96.Multi_Factor_Watercolor_Boxplot.pzf | Multi-factor watercolor boxplot (2 markers x 5 groups) | Two-factor: markers x quartiles |
| 100 | 100.WB_Multi_Marker_Violin.pzf | WB multi-marker violin (3 proteins, DMSO vs Yoda1) | Two-factor: proteins x treatment |
| 102 | 102.Multi_Indicator_Multi_Group_Boxplot.pzf | Multi-indicator grouped boxplot (5 cell states x 5 timepoints) | Two-factor: cell state x time |
| 105 | 105.ELISA_Violin.pzf | ELISA violin (4 groups with all pairwise P-values) | Column: replicates per group |

## Line & Time Series Plots

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 4 | 4.Scatter_Line.pzf | Scatter line plot (4 shear stress conditions over time) | XY: time vs measurement per group |
| 5 | 5.Segmented_Line.pzf | Segmented line plot (3 cycles, with break in x-axis) | XY: time vs measurement with axis break |
| 7 | 7.Trend_Line.pzf | Trend line plot (dual-panel: density + nematic order vs radius) | XY: radius vs measurement, multiple groups |
| 40 | 40.Dual_Y_Time_Series.pzf | Dual-Y time series (E-cadherin-GFP + DRAQ7, with CI bands) | XY: time vs 2 measurements + error |
| 44 | 44.Multi_Group_Line.pzf | Multi-group line (4 groups x timepoints, with shaded intervention zone) | XY: day vs measurement per group |
| 48 | 48.Tumor_Growth_Curve.pzf | Tumor growth curves (spaghetti plot: Low vs High, individual animals) | XY: day vs tumor volume per animal |
| 60 | 60.Multi_Group_CI_Line.pzf | Multi-group CI line (4 conditions, dashed/solid, with error bars) | XY: day vs mean+SEM per group |
| 61 | 61.Flower_Line.pzf | Flower line plot (individual trajectories + group means, 2 timepoints) | Paired XY: before/after per subject |
| 64 | 64.Color_Card_Line.pzf | Colored card line (6 panels with colored backgrounds, gene expression) | Multi-panel XY: genes x conditions |
| 75 | 75.Multi_Group_Smooth_Curve.pzf | Multi-group smooth line (relative abundance across GI tract sites) | XY: site vs abundance per genus |
| 86 | 86.CI_Waveform.pzf | Waveform plot with CI bands (Vehicle vs BRP, food intake over hours) | XY: time vs measurement + error |
| 92 | 92.WB_Band_Line.pzf | WB band line (Parkin/SOD2 relative density across 4 conditions) | Grouped: conditions x proteins + replicates |
| 107 | 107.Two_Group_Line.pzf | Two-group line (weight change over days, with error bars) | XY: day vs mean+SEM, 2 groups |
| 112 | 112.Seahorse_OCR_Line.pzf | Seahorse OCR line (3 groups with Oligomycin/FCCP/Antimycin A injections) | XY: minutes vs OCR per group |

## Scatter & Correlation

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 13 | 13.Multi_Group_CI_Scatter.pzf | Multi-group scatter with CI band + regression line (7 cancer types) | XY: factor vs score, colored by type |
| 30 | 30.Multi_Indicator_Classified_Scatter.pzf | Multi-indicator classified scatter (8 clinical variables, shape+color coded) | XY: % vs -log10(Padj) per indicator |
| 50 | 50.Correlation_Scatter.pzf | Correlation scatter (4 panels: regression lines with r, P, beta) | XY per panel: x vs y with stats |
| 73 | 73.Dual_Y_Correlation_Scatter.pzf | Dual-Y correlation scatter (2 panels: SUVA + pH vs phenol oxidative activity) | XY: x vs y1 + y2 (dual axis) |

## Dot / Bubble / Lollipop Plots

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 11 | 11.Dumbbell_Plot.pzf | Dumbbell/paired plot (GBM vs PDGC, lines connecting paired values) | Paired: group1 vs group2 per item |
| 22 | 22.Enrichment_Bubble.pzf | Enrichment bubble (pathways x annotations, size=count, color=-log10FDR) | Matrix: pathway x annotation + count + FDR |
| 24 | 24.Column_Dumbbell.pzf | Column dumbbell (Pre-stimulus vs Stimulus, with connecting lines) | Paired: before vs after per subject |
| 27 | 27.Color_Bubble.pzf | Color bubble plot (fold enrichment vs -log10FDR, size=count) | XY: enrichment vs significance + size |
| 31 | 31.Grouped_Lollipop.pzf | Grouped lollipop (2 genes x tissues, colored dots on stems) | Grouped: tissue x gene nTPM values |
| 49 | 49.Bubble_Swarm.pzf | Bubble swarm (2 groups, large+small dots mixed) | Column: replicates per group |
| 55 | 55.Enrichment_Bubble_Bar.prism | Enrichment bubble + bar combo (GO categories, ranked by -log10padj) | Grouped: pathway, -log10p, count, category |
| 58 | 58.WB_Protein_Quant_Bubble.pzf | WB protein quantification bubble (bands + dot intensity plot) | Matrix: proteins x samples (intensity) |
| 59 | 59.Enrichment_Lollipop_Bar.pzf | Enrichment lollipop + bar (cell markers left, GO terms right) | Dual panel: counts + -log10P per item |
| 85 | 85.Bidirectional_Lollipop.pzf | Bidirectional lollipop (microbiome coefficients: positive/negative) | Column: items with signed values |
| 87 | 87.qPCR_Gene_Expression_Bubble.pzf | qPCR expression bubble (genes x treatments, size=expression level) | Matrix: genes x treatments |
| 88 | 88.WB_Multi_Band_Bubble.pzf | WB multi-band bubble (proteins x conditions, color=intensity) | Matrix: proteins x samples |
| 89 | 89.Multi_Factor_Column_Dumbbell.pzf | Multi-factor dumbbell bar (Pre/Post x 2 neuron types) | Two-factor paired |
| 97 | 97.MTT_Cell_Viability_Bubble.pzf | MTT cell viability bubble (plate layout: 4 conditions, size+color=viability) | Matrix: rows x columns (96-well plate layout) |
| 99 | 99.GO_Enrichment_Bubble.pzf | GO enrichment bubble (pathways, size=gene number, color=p-value) | Table: pathway, rich factor, gene count, p-value |
| 110 | 110.WB_Multi_Band_Color_Bubble.pzf | WB multi-band color bubble (protein levels, sized dots) | Matrix: proteins x conditions |

## Enrichment & Pathway Analysis

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 19 | 19.Enrichment_Lollipop.pzf | Enrichment lollipop (GO:MF/BP/CC/KEGG, colored by category) | Table: term, -log10P, category |
| 23 | 23.Enrichment_Bar.pzf | GSEA enrichment bar (NES bars, 3 panels: positively/negatively/COSMIC enriched) | Grouped: pathway, NES per panel |
| 46 | 46.Bidirectional_Bar.pzf | Bidirectional bar (up=red pathways, down=blue pathways, -log10 q-value) | Signed values: pathway, direction, -log10q |
| 68 | 68.Butterfly_Lollipop.pzf | Butterfly lollipop (Region T1 up, T2 down; immune cell proportions) | Bidirectional: cell types with signed fractions |
| 80 | 80.Gene_Ranking.pzf | Gene ranking plot (NormZ score vs rank, highlighted pathway genes) | XY: rank vs score, colored by pathway |
| 115 | 115.GO_Enrichment_Gene_Heatmap.pzf | GO enrichment gene heatmap (pathways + gene-level heatmap) | Matrix: genes x pathways |

## Swarm / Bee / Rain Plots

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 36 | 36.Multi_Group_Beeswarm.pzf | Multi-group beeswarm (8 genes, colored, with all pairwise P-values) | Column: replicates per group |
| 42 | 42.Flower_Swarm.pzf | Flower swarm (2 groups, large flower dots with error bars) | Column: replicates per group |
| 51 | 51.Raincloud_Plot.pzf | Cloud-rain plot (half-violin + dot swarm + error bar, 2 groups) | Column: replicates per group |
| 65 | 65.Multi_Factor_Beeswarm.pzf | Multi-factor swarm (4 groups x 2 conditions, with significance) | Two-factor: group x condition |
| 70 | 70.Multi_Group_Flower_Swarm.pzf | Multi-group flower swarm (5 groups, large colored dots) | Column: replicates per group |
| 95 | 95.Raincloud_ErrorBars.pzf | Cloud-rain with error bars (2 groups, half-violin + dots + mean+SEM) | Column: replicates per group |
| 113 | 113.OCR_Beeswarm.pzf | OCR beeswarm (3 panels: Basal/Proton leak/Maximal, 3 groups) | Multi-panel column: replicates per group |

## Dose-Response / IC50 / EC50

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 20 | 20.Dose_Response_Curve.pzf | Dose-response curves (6 concentrations, cell viability %, log2 x-axis) | XY: log(concentration) vs response per dose |
| 43 | 43.IC50_Curve.pzf | IC50 curve (2 siRNA conditions, sigmoidal fit, annotated IC50 values) | XY: log[drug] vs viability, 2 curves |
| 78 | 78.EC50_Curve.pzf | EC50 curve (3 peptides, sigmoidal fit, annotated EC50 values) | XY: log(concentration) vs % efficacy |
| 104 | 104.Multi_Group_IC50_Curve.pzf | Multi-group IC50 (3 drugs, log10 x-axis, annotated IC50 values) | XY: log10(M) vs viability, 3 curves |

## ROC Curves

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 28 | 28.Multi_ROC_Curve.pzf | Multi-group ROC (5 models with AUC values in legend) | XY: FPR vs TPR per model |
| 108 | 108.Single_ROC_Curve.pzf | Single-group ROC (3 panels, each with diagonal reference) | XY: 1-Specificity vs Sensitivity |

## Donut & Proportion

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 26 | 26.Donut_Chart.pzf | Donut chart (2 donuts: gene regulation proportions with total counts) | Categories: label + count per segment |

## Error Bar & Dual-Axis Plots

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 14 | 14.Bidirectional_Error_Scatter_Line.pzf | Bidirectional error scatter-line (5 drug conditions, time series with SEM) | XY: time vs mean+SEM per group |
| 32 | 32.Dual_Error_Bar.pzf | Dual error bar plot (6 neuron types, X+Y error bars, dashed connecting lines) | XY: delta speed vs delta spikes + X/Y error |
| 72 | 72.Multi_Factor_Error_Bar.pzf | Multi-factor error bar (3 MAF groups x 3 variant types) | Grouped: MAF group x variant type + CI |

## Confusion Matrix

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 18 | 18.Confusion_Matrix.pzf | Confusion matrix (3 models: RF, NN, XGBoost; Survivor vs Deceased) | Matrix: 2x2 per model (counts or %) |

## UMAP & Dimensionality Reduction

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 38 | 38.UMAP_Cluster.pzfx | UMAP clustering scatter (colored cell types, labeled clusters) | XY: UMAP1 vs UMAP2 + cluster labels. **XML editable** |

## Western Blot Quantification

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 58 | 58.WB_Protein_Quant_Bubble.pzf | WB bubble (single protein, dot size = intensity) | Matrix: proteins x samples |
| 62 | 62.WB_Protein_Quant_Heatmap.pzf | WB heatmap (with band image placeholder) | Matrix: proteins x samples (relative) |
| 71 | 71.WB_Multi_Marker_Heatmap.pzf | Multi-band WB heatmap (2 cell types) | Matrix: proteins x conditions |
| 88 | 88.WB_Multi_Band_Bubble.pzf | Multi-band bubble (5 proteins x 4 conditions) | Matrix: proteins x conditions |
| 92 | 92.WB_Band_Line.pzf | WB band line (relative density across treatments) | Grouped: conditions x proteins |
| 94 | 94.WB_Multi_Marker_Bar.pzf | WB multi-marker bar (3 groups x 2 proteins) | Two-factor: group x protein |
| 100 | 100.WB_Multi_Marker_Violin.pzf | WB multi-marker violin (3 proteins, 2 conditions) | Two-factor: protein x treatment |
| 110 | 110.WB_Multi_Band_Color_Bubble.pzf | WB color bubble (sized dots by intensity) | Matrix: proteins x conditions |

## CCK8 / MTT / Cell Viability

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 77 | 77.CCK8_Cell_Proliferation.pzf | CCK8 proliferation line (4 conditions over 96h) | XY: time vs OD450 per group |
| 93 | 93.CCK8_Bar.pzf | CCK8 bar (3 groups x 3 timepoints) | Two-factor: group x day |
| 97 | 97.MTT_Cell_Viability_Bubble.pzf | MTT plate-layout bubble (96-well style) | Matrix: plate layout |
| 111 | 111.CCK8_Bar_Alt.pzf | CCK8 survival bar (5 treatments) | Column: replicates per treatment |

## qPCR

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 56 | 56.qPCR_Heatmap.pzf | qPCR heatmap (6 genes x 5 conditions) | Matrix: genes x conditions (fold change) |
| 67 | 67.qPCR_Segmented_Bar.pzf | qPCR segmented bar (Ctrl/OE/Scrl/KD x 2 treatments) | Two-factor grouped |
| 76 | 76.PCR_Multi_Gene_Expression_Heatmap.pzf | Multi-gene PCR heatmap (large gene list, fold change) | Matrix: genes x conditions |
| 87 | 87.qPCR_Gene_Expression_Bubble.pzf | qPCR bubble (genes x treatments, bubble size=expression) | Matrix: genes x treatments |

## Seahorse / Metabolic

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 112 | 112.Seahorse_OCR_Line.pzf | OCR time-course (3 groups + injection markers) | XY: time vs OCR per group |
| 113 | 113.OCR_Beeswarm.pzf | OCR bar panels (Basal/Proton leak/Maximal, 3 groups) | Multi-panel column |

## Cumulative / Distribution

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 53 | 53.Cumulative_Frequency_Distribution.pzf | Cumulative frequency distribution (2 groups + inset bar) | XY: interval vs cumulative frequency |

## Special / Composite

| # | File | Description | Data Format |
|---|------|-------------|-------------|
| 38 | 38.UMAP_Cluster.pzfx | UMAP scatter (XML editable, cell type clusters) | XY: UMAP1 vs UMAP2 + color labels |
| 55 | 55.Enrichment_Bubble_Bar.prism | Enrichment combo (ZIP editable: JSON+CSV) | GO terms + counts + p-values |
