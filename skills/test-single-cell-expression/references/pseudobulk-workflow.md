# Pseudobulk workflow

## Contents

1. Aggregation
2. Design and diagnostics
3. edgeR pattern
4. DESeq2 pattern
5. Required outputs

## 1. Aggregation

Use the annotated count object as the source of truth and align every column with a
sample metadata row. This Seurat-oriented pattern avoids parsing biological metadata
back out of concatenated column names:

```r
library(Seurat)
library(Matrix)

counts <- GetAssayData(seu, assay = "RNA", layer = "counts")
cell_meta <- seu[[]][, c("sample_id", "condition", "cell_type", "batch")]
stopifnot(identical(colnames(counts), rownames(cell_meta)))

group <- interaction(cell_meta$sample_id, cell_meta$cell_type,
                     drop = TRUE, sep = "__")
membership <- sparse.model.matrix(~ 0 + group)
colnames(membership) <- levels(group)
pb_counts <- counts %*% membership
pb_n_cells <- as.integer(table(group))
names(pb_n_cells) <- levels(group)

pb_meta <- unique(cell_meta[, c("sample_id", "condition", "cell_type", "batch")])
pb_meta$column_id <- interaction(pb_meta$sample_id, pb_meta$cell_type,
                                drop = TRUE, sep = "__")
pb_meta <- pb_meta[match(colnames(pb_counts), pb_meta$column_id), ]
stopifnot(identical(as.character(pb_meta$column_id), colnames(pb_counts)))
pb_meta$n_cells <- pb_n_cells[colnames(pb_counts)]
```

Adapt the metadata columns to the contract. Confirm the installed Seurat and Matrix
APIs before running; for multi-layer assays, join or select the intended raw-count
layer explicitly.

Do not silently discard thin pseudobulks. Add `included` and `exclusion_reason`
columns to `pb_meta`, then retain that complete table as provenance and figure source
data.

## 2. Design and diagnostics

Before fitting:

- cross-tabulate condition, batch, donor, pairing, and cell type;
- verify each modeled cell type has biological samples in every requested contrast;
- create the exact design matrix and check `qr(design)$rank == ncol(design)`;
- inspect library sizes and sample-level PCA/MDS after normalization;
- state the factor reference level and the sign of the requested contrast.

A default minimum such as ten cells per sample-by-cell-type is only a starting
diagnostic. Raise or lower it from count depth, dispersion stability, cell rarity, and
sensitivity analysis; record the choice and samples affected.

## 3. edgeR quasi-likelihood pattern

```r
library(edgeR)

keep_columns <- pb_meta$included
y <- DGEList(pb_counts[, keep_columns, drop = FALSE])
model_meta <- droplevels(pb_meta[keep_columns, ])
design <- model.matrix(~ 0 + condition + batch, data = model_meta)
stopifnot(qr(design)$rank == ncol(design))

keep_genes <- filterByExpr(y, design = design)
y <- y[keep_genes, , keep.lib.sizes = FALSE]
y <- calcNormFactors(y)
y <- estimateDisp(y, design)
fit <- glmQLFit(y, design, robust = TRUE)

# Define and inspect an explicit named contrast for the contract direction.
contrast <- makeContrasts(condition_treated_vs_control =
                           conditiontreated - conditioncontrol,
                         levels = design)
test <- glmQLFTest(fit, contrast = contrast[, "condition_treated_vs_control"])
result <- topTags(test, n = Inf, sort.by = "none")$table
```

Coefficient names depend on factor coding; print `colnames(design)` and construct the
contrast from the actual matrix. Do not copy the example contrast blindly.

## 4. DESeq2 pattern

```r
library(DESeq2)

keep_columns <- pb_meta$included
dds <- DESeqDataSetFromMatrix(
  countData = round(pb_counts[, keep_columns, drop = FALSE]),
  colData = droplevels(pb_meta[keep_columns, ]),
  design = ~ batch + condition
)
dds <- DESeq(dds)
result <- results(dds, contrast = c("condition", "treated", "control"))
```

Use the same aggregation, metadata, contrast checks, and exclusions for either
engine. Choose the engine from the design and desired inference, not convenience.

## 5. Required outputs

- raw pseudobulk count matrix and aligned metadata, including excluded columns;
- design matrix, named contrast, factor levels, and rank check;
- gene and pseudobulk filtering tables;
- normalization and dispersion/model diagnostics;
- complete unthresholded result table with effect, uncertainty where available,
  raw p-value, adjusted p-value, and method metadata;
- per-cell-type sample counts and explicit reasons for untestable contrasts;
- sample-set and contrast identifiers shared with the evidence index.
