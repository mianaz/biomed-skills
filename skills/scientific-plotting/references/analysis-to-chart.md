# Match analysis outputs to charts

Choose from the input's quantities, experimental units and reading task. An assay
name does not determine a chart: qPCR, immunoblot, ELISA and viability endpoints
can all be group comparisons. A template name is not evidence that an analysis was
performed. Preserve validated supplied results; recompute only with sufficient data
and design information. A visualization request does not require rebuilding a
sequencing, integration or pathway-analysis pipeline.

| Available evidence | Useful candidate | What must remain interpretable |
|---|---|---|
| Small continuous assay groups | Bars with observations or beeswarm plus summary; matched points for paired units | Biological/technical unit, normalization control, pairing and the measured scale |
| Repeated OCR, growth or other time series | Unit trajectories or supported summaries; derived endpoint comparisons when they add a distinct result | Actual times, intervention/injection events, repeated units and definition of derived components |
| Pharmacologic dose series or assay standards | Observations plus a justified response/calibration model; see `dose-response.md` for logistic fits | Concentration units, blanks, tested range, relative versus absolute potency; not every calibration is sigmoidal |
| Large distributions | ECDF, histogram, density, or points with a distribution summary | Absolute values, tails, zeros and n; identify binning, smoothing or subsampling |
| Sample-by-feature matrix | Heatmap with sample/group annotations | Units and transformations, selected rows, missing values, zeros and sample identities; row scaling hides between-feature magnitude |
| Differential-expression estimates | Volcano for effect versus evidence; MA for effect versus abundance | Contrast, all tested features, supplied adjusted versus raw P, effect size and selected labels; do not recreate tests from coefficients |
| Overrepresentation results | Dot/bar plot of enrichment magnitude with count and adjusted evidence; membership matrix when gene sharing matters | Tested background, gene-set version, selection rule, denominator and distinction between input-gene and background ratios |
| Ranked gene-set enrichment | Running enrichment score with membership hits and ranking metric; NES overview across sets | Rank direction, score, adjusted evidence and leading-edge genes; retain the underlying ranked values |
| Per-sample gene-set scores | Sample-level points/distributions or a score matrix | Scoring method and scale, sample IDs and contrast; these scores are not enrichment P values |
| Expression and detection by cell group | Dot plot for expression magnitude plus fraction detected; distributions if heterogeneity is central | Both summaries and their definitions, zero versus missing, transformations and donor structure |
| Composition or observed/expected counts | Per-unit stacked counts/fractions, aligned fraction plots or observed/expected matrix | Denominator, totals, absent categories and independent units; pooled cell counts do not create donor replication |
| PCA or supplied embedding coordinates | Coordinate scatter, feature overlay or justified density | Preserve supplied geometry, point identities and coverage; report explained variance only for methods that define it |
| Pseudotime/branch results | Ordered expression trends, branch heatmap or density along supplied pseudotime | Root, direction, branch assignment and support; inferred ordering is not measured elapsed time |
| Cell-communication or other network estimates | Keyed edge/bubble matrix; network diagram when topology is the reading task | Sender/receiver or edge identity, estimate definition, filtering and support; an inferred edge is not direct causal evidence |
| Clinical effect estimates or spline predictions | Forest plot or predicted association curve with intervals | Effect/reference units, adjustment model and predictor support; an XY template does not fit a spline |
| Prediction scores and outcomes | ROC/precision–recall across thresholds; confusion display at a fixed operating point | Evaluation cohort, thresholds, denominators and paired predictions; one confusion matrix cannot recover a ROC curve or AUC |
| Membership in several sets | Intersection counts/membership display; small Venn when readable | Set universe and exact intersections; avoid an unreadable collection of overlapping regions |

For an open-ended figure request, add a second panel when it answers a different question or exposes evidence hidden
by a summary. Examples include an embedding plus per-donor composition, enrichment
overview plus the relevant gene-level evidence, or OCR trajectories plus defined
respiration components. Several simple panels can be appropriate; do not add all
available chart variants. A circular heatmap, decorative swarm, rotated volcano or
dual-axis overlay earns no preference merely because it exists in a template library.

Do not copy template transformations, cutoffs, tests, group assignments or selected
genes without checking their meaning in the present data. Match sample tables by
IDs. Preserve original values in exports when using display saturation, and identify
the saturation. Keep uncertainty unavailable when the required information is absent.

These are chart-selection rules, not appearance references. Apply the current
`visual-design.md` and `color-policy.md` to whichever chart is chosen; follow a
supplied example's styling only when the user designated it as a style reference.

When plotting gene sets or signatures, include the complete gene-set and scoring
record from `figure-delivery.md`. A set name, size or abbreviated leading edge does
not replace its original and actually used membership lists.

Method references: [Seurat DotPlot](https://satijalab.org/seurat/reference/dotplot)
defines expression and detection as distinct summaries;
[GSEA user guide](https://docs.gsea-msigdb.org/GSEA/GSEA_User_Guide/)
defines enrichment-score, membership-hit, rank-metric and leading-edge displays;
[clusterProfiler manual](https://bioconductor.org/packages/release/bioc/manuals/clusterProfiler/man/clusterProfiler.pdf)
documents the enrichment input and background parameters.
