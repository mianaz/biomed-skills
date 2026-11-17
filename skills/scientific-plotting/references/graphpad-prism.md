# Editable GraphPad Prism output

For a data-table export, deliver `.pzfx` and the direct CSV. For a figure or native-project request, also follow the relevant rendering route below. The bundled base-R writer creates editable Column, Grouped, or XY **data tables**. It preserves numeric values, missing cells, row order, and supplied row IDs. It adds no analyses or graph styling.

```r
source("scripts/prism.R")
write_prism(wide_data, "groups.pzfx")
write_prism(paired_data, "paired.pzfx", id = "donor")
write_prism(time_course, "time_course.pzfx", x = "time")
```

Each numeric Y column is a dataset. `id` names a column of unique row titles; other columns must be numeric. Align paired observations by subject before exporting, retain absent measurements as `NA`, and keep the subject order the same across conditions. Row IDs preserve alignment; they do not configure a paired statistical test in Prism.

For replicate subcolumns, supply a named mapping from input column to dataset:

```r
write_prism(time_course, "replicates.pzfx", x = "time",
  groups = c(control_1 = "Control", control_2 = "Control",
             drug_1 = "Drug", drug_2 = "Drug"))
```

Omitting `x` with replicate subcolumns creates a Grouped table. Give each dataset the same number of replicate subcolumns; use explicit `NA` columns for absent replicates. Include the original wide CSV so subcolumn/sample names remain available. Never invent replicates from summary statistics. Zero remains zero, and `NA` becomes an empty cell. The writer rejects text measurements, `Inf`, `NaN`, duplicate IDs, and incomplete mappings. It preserves input doubles with 17 significant digits; displayed decimals do not change the stored measurements. Existing files are preserved unless `overwrite = TRUE` is explicitly supplied.

## Delivering native graphs

1. Open the exported `.pzfx` in licensed GraphPad Prism.
2. Select **New Graph**, choose the matching data table and graph type, and format the graph in Prism.
3. Use **File → Save As** to save a new `.prism` project or a full `.pzfx` project, then export the graph as PDF.
4. Compare the saved table with the input and inspect the exported PDF for labels, fonts, missing points, ranges, and clipping.

A data-only PZFX file is not a conversion of the R figure into a native Prism graph. `pzfx::write_pzfx()` has the same data-table boundary; `ggprism` produces R graphics. Report Prism analyses only when they were actually run and saved in Prism.

For an existing authorized Prism project, open a copy in Prism and replace the appropriate data table. Preserve the intended dataset count, replicate structure, pairing and exclusions. Use the shared [analysis decisions](../../biomed-shared/statistical-analysis.md) to verify that inherited analysis settings fit the new data and comparison family; rerun linked analyses in Prism after data changes. Appearance-only edits retain valid results. For direct PZFX editing, replace only the selected table block and preserve the opaque `<Template>` graph/analysis payload byte-for-byte; update mirrored `XAdvancedColumn` data when present. A generic XML rewrite or a change to one CSV inside a `.prism` archive does not establish a valid native project. Reconcile existing handwritten P values and annotations with the recomputed results. No third-party template collection is bundled.

## Format check

Compare the exported XML tables with the direct CSV for values, numeric precision,
blank cells, row IDs, XML escaping and replicate subcolumns. The project Info sheet
records the exporter and data-only scope. For a native graph/project request,
also open the actual file in the installed Prism and inspect its saved rendering.
