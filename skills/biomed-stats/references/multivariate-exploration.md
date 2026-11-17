# Multivariate exploration

Use for PCA, clustering or a high-dimensional overview. Define which rows are
independent units, which columns are features, the measurement scale and the
biological structure being sought. Use [prediction and learning](prediction-and-learning.md)
when a transformation will feed a predictive model.

## Choose the representation

| Target | Candidate | Decisions to record |
|---|---|---|
| Summarize major linear variation | PCA | Centering, scaling, feature set, loadings and retained variance |
| Group objects by similarity | Hierarchical clustering | Distance, linkage, cut level and feature preprocessing |
| Partition objects around centroids | k-means | Squared-Euclidean geometry, k, scaling and initialization |

Center and scale for the question and units. Standardizing all variables gives
small-variance features equal opportunity to influence the fit; this can help
mixed units or amplify measurement noise. Log transformations and feature filters
change the geometry. Retain their definitions and fit them within training data
when evaluating prediction.

For PCA, inspect explained variance and loadings alongside scores. Centered PCA
has rank at most min(n-1, p). Batch effects can dominate a component, and useful
biological variation can occur outside the first two components. Examine whether
the retained representation preserves the contrasts of interest. Report how new
data are centered, scaled and projected using the learned transformation.

For clustering, select a distance that represents the intended similarity and a
compatible algorithm. Standard k-means minimizes within-cluster squared Euclidean
distance. Hierarchical linkage choices impose different grouping behavior.
Investigate stability under reasonable feature, scaling, initialization and unit
resampling choices. There is no universal best k or distance for biological data.

## Interpret and deliver

Show the units, transformations, distance/linkage or PCA loadings, and evidence
for stable patterns. Use information not used to construct the grouping when
assessing biological support. A separation produced using selected features is
exploratory evidence; a test of the same selected features needs to account for
the selection. Align any resampling with the independent sampling unit.

Deliver the processed matrix or reproducible transformation, fitted object,
loadings/cluster membership and stability summaries needed for the conclusion.
High dimensionality increases selection opportunities and sparse coverage; use
scientific relevance and independent validation to guide follow-up.

## Sources

- *Clustering*, pp. 545–546: [nmeth.4299](https://doi.org/10.1038/nmeth.4299).
- *Principal component analysis*, pp. 641–642: [nmeth.4346](https://doi.org/10.1038/nmeth.4346).
- *The curse(s) of dimensionality*, pp. 399–400: [s41592-018-0019-x](https://doi.org/10.1038/s41592-018-0019-x).

Stability, selection and training-only transformations are suite implementation
checks. Do not reuse the clustering column's simplified RMS/correlation identity.
