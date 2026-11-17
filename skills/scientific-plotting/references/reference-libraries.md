# Choose a template across the reference libraries

Use the scientific question to choose a chart family, then use a reference to solve
its geometry and implementation. A reference is useful when its input structure and
reading task match the current figure.

Use the supplied source first. When none is specified, first check the personal
original-source library if available, then the other compatible collections.
Read catalog-maintenance sections only when updating that catalog.

## Collections and input contracts

| Source | Best use | Inspect before adapting |
|---|---|---|
| Personal original-source library | Reuse the actual plotting implementation of selected figures | Original PNG, exact script and lines, native inputs, preserved variants and source/replay status; see [custom-library.md](custom-library.md) |
| CNS published-panel reproductions | A real visual precedent, dense evidence layers, layout and label placement | Original panel, reproduction, DOI/panel locator, input contract, current review and adapter design support |
| MedBioinform R recipes | Familiar biomedical/omics recipes and package-specific geometry | R script, example inputs/object, preview, transformations, statistical calls and packages |
| GraphPad Prism templates | Native Column, Grouped, XY and survival projects | Actual data tables, replicate layout, linked analyses, exclusions, graph settings and saved native export |
| Bundled worked examples | Simple comparison, pairing, time, dose or matrix patterns | The example's stated design and direct plotting tables |
| External code galleries | Package-author examples and established plotting galleries | Exact example/code links, source preview, checked date and source terms |

The shared index combines the publication catalog, MedBioinform/Prism metadata,
13 tested R input shapes, traced personal source recipes and external code examples.
Use the [full template database](template-database.md) to browse every entry by family
and expand similar variants. Run a shortlist search from this skill folder:

```sh
python3 scripts/reference_library.py recommend \
  --task group-comparison --design independent --kind observations \
  --language R --query "treatment effect on measured response" --width-mm 50 \
  --limit 3 --html /path/to/candidates.html
```

Set `--kind` to `observations`, `estimates`, `matrix`, `curve` or `unspecified`.
Use `--design supplied-results` when the renderer consumes upstream estimates or
matrices. Keep the upstream study design in the analysis record. For an exact input
contract, supply `--columns unit,group,value` after mapping the user's columns.
Use `--collection Custom`, `Publication`, `MedBioinform`, `Prism`, `Worked example` or `External code` to narrow
sources. Forest plots use `--task effect-estimates` in the shared search.

`candidates` have compatible, reviewed contracts. `references` need the listed
input, design or execution checks. The HTML shows up to three candidates, or three
reference leads when none qualify. Current publication review is checked against
connected files. MedBioinform and Prism records stay at reference status until
their selected recipes/native projects are exercised and inspected.

Personal source recipes appear as references until their input context and new-data
adaptation are checked. Their R excerpts are copied from the original scripts.
The private selection map retains all original artwork, paths and full scripts.
Superseded synthetic reconstructions are excluded from both candidates and leads.

Connect local resources without copying third-party source collections:

```sh
python3 scripts/reference_library.py register --id medbio --path /path/to/MedBioinform_R_plot
python3 scripts/reference_library.py register --id prism --path /path/to/Prism-templates
```

Publication-library registration and staging use
[publication-gallery.md](publication-gallery.md). Inspect a selected MedBioinform
recipe in its source folder; use the [Prism catalog](../../graphpad-prism/references/template_catalog.md)
and native Prism workflow for `.pzf` files. Refresh the external metadata with
`reference_library.py index --medbio PATH --prism PATH` after the collections change.

Keep machine-specific library paths in local configuration or figure notes. Keep
source artwork, private data and third-party template binaries in their original
libraries unless redistribution is permitted.

## Selection rules

The native worked examples include all thirteen input shapes plus lollipops,
competing-risk curves and a matrix with linked quantitative tracks. Each was
tested with original, replacement and stress inputs on 2026-11-05. The matrix
composite uses `columns.csv` (`feature`, `block`) and joins tracks by row names.
`native-source-adaptations.json` adds source-result adapters for MedBioinform 36,
78 and 80: corrected GO log-base labeling, unrestricted count axes, and GSEA ranks
with named highlights and native label repulsion. These adapters preserve supplied
results; replacement/stress fixtures are modified demonstrations.

The full HTML separates native replacement tests, static source-code inventory,
and archived implementations. Source-bound coordinate candidates remain references
until adapted to new data. `source-audit.json` records source lines; an empty scan
does not establish scientific or visual quality. Archives retain the original code
and preview and are excluded from the active recommendation index.

1. **Question:** identify what the reader must compare: magnitude, change, spread,
   association, composition, pattern, uncertainty or performance. Select the family
   from [visual-design.md](visual-design.md) and
   [analysis-to-chart.md](analysis-to-chart.md).
2. **Study design:** establish the biological unit and any pairing, repeated times
   or nesting. Check that the candidate preserves those identities. Keep the source
   paper's design separate from the adapter's demonstrated capabilities.
3. **Inputs:** map actual columns, identifiers, units and transformations. Distinguish
   raw observations from estimates, interval bounds, curves, density grids, matrices
   and coordinates. An adapter for model results consumes those results; fitting
   belongs to the analysis workflow.
4. **Output:** match R/Python/native Prism editability and available dependencies.
   Prefer a working implementation of the required geometry.
5. **Readability:** compare the main contrast at the intended size. Check category
   count, label length, crossings, dynamic range and the space needed for annotations.
6. **Source priority:** among compatible published panels prefer (1) verified source
   data plus panel-mapped author code, (2) panel-mapped author code, (3) verified
   source data, then (4) other reproductions. Within a tier, compare query fit,
   tested placement and adaptation work.

These are ordered decisions, not a weighted quality score. Source journal and
visual novelty do not add suitability. Use a specialized layout when it reveals a
relationship that the simpler candidate would obscure.

Show up to three useful previews in HTML. Each card should name the reading task,
source, required columns, design support, execution status and selection reason.
Use the original/replica pair for a publication reference, the existing preview
for an R recipe, or a native export for a Prism template. For routine repairs,
compare the original and revised figure at the same physical size.

## Data replacement and review

Before using an untested recipe, inspect the code and run a working copy with
explicit inputs and an output directory. Separate its plotting section from
upstream analysis, package installation, workspace clearing and hard-coded paths.

Check the numerical transformation against the plotted label: log versus log10,
fraction versus percent, row scaling, normalization denominator and interval bounds
versus error-bar distances. Retain source statistics only when they describe the
current input. Recompute dynamic annotation positions and axes after replacement.

Promote a template for routine use after these task-specific checks:

- Its example executes and the saved render is inspected.
- A second valid dataset changes values and category labels correctly.
- Claimed paired/repeated support retains unit IDs and missing segments.
- Its relevant narrow or dense case remains readable at the intended placement.
- The direct plotting data, editable source and output format are verified.

Record review per implementation. A reviewed R recipe can be used for R; add a
Python or native Prism adapter when that output is needed and verify it separately.
The current CNS catalog retains its existing two-language review contract.

## Maintain the selection metadata

The shared loader combines the publication catalog with `external.json`,
`code-galleries.json`, `curation.json` and `worked-examples.json` under `assets/reference-library/`.
Export one normalized index with `reference_library.py dump --output PATH`.
The source collections remain separate; their metadata use one record shape.

| Field group | Information that changes selection |
|---|---|
| Identity | Stable ID, source library, original/adapted relationship |
| Scientific task | Reading task, outcome/estimand, chart family, assay context |
| Design | Source design, adapter design support and its schema/code evidence |
| Inputs | Required fields, row unit, value type, units, transformation, missing-value handling |
| Encoding | Position, color, size, group connections, interval semantics |
| Layout | Tested placed dimensions, effective type sizes, group/series counts and label lengths |
| Implementation | Language/package, entry script or native filename, dependencies |
| Provenance | DOI/panel, mapped author code/commit, data basis, source license |
| Review | Example run, replacement run, visual inspection, review date, file version |
| Use history | Chosen for which task, successful layout and a concrete failure/fix |

Use `unspecified` for unreviewed design or input kind and explicit false verification flags for source evidence. Searchable visual references and
tested executable templates are useful at different stages; show that status on
the candidate card.

Prioritize coverage gaps over raw counts: paired and repeated observations, nested
replicates, factorial comparisons, unequal group sizes, missing time points, long
labels and compact annotated matrices. Group cosmetic variants under a shared
parent recipe. Add a new entry when it supplies a new data relationship or reading
task. Preserve a link to the exact successful example when a real project improves
a recipe.

To assess selection quality, use a small fixed set of real input shapes and accept
all defensible chart families for each question. Check correct routing, data and
unit preservation, readable final size and required editability. A package/link
check alone measures packaging, not better plot choice.

## Verify source priority

Record author code at the exact panel scope with a pinned repository commit, file,
and mapping basis. A figure-level route, related method or repository homepage is
kept as a lead until the panel mapping is checked. A data file listed beside code
is recorded as data, with the code file identified separately.

For the top tier, verify that current plotting inputs match the preserved author
data or the recorded author preparation outputs. State whether each input contains
observations or upstream summaries. Keep printed annotations and public-data
revision differences visible in `data_scope` and `data_basis`. Record the review
date and recheck source evidence after changing inputs, preparation or panel mapping.
`assets/publication-gallery/source-evidence.json` supplies the same ranking to both
search commands.

## Checked input shapes

`examples/reference-cases.R` covers independent groups, matched pairs, repeated
visits with missing values, independent sampling over time, factorial comparison,
dose response, distribution, forest estimates, survival, per-sample composition,
ComplexHeatmap, enrichment and nested replicates. These are synthetic, first-party examples. Each
indexed card names its exact required fields, row unit, tested size and replacement
check. Their data are examples to replace with the current study's data.

For measurements within subsamples within independent biological units, use
`worked/nested` and [nested-replicates.R](../examples/nested-replicates.R).
Its columns are `unit,group,subsample,observation,value`; subsample and observation
IDs are scoped within their parent IDs. This two-group example first averages
observations within each subsample, then gives subsample means equal weight within
each biological unit. Bars, SD, points and the comparison use those unit means.
It saves both intermediate levels and original measurements. Use it when this
estimand matches the study; shared statistical guidance covers other weighting,
paired or model-based hierarchical analyses. Set the outcome label and units for
the actual data.

```sh
python3 scripts/reference_library.py recommend --task group-comparison --design nested \
  --columns unit,group,subsample,observation,value --language R
Rscript --vanilla examples/nested-replicates.R /path/to/measurements.csv /path/to/panel
```

The independent-group, odds-ratio forest and heatmap cases route to
`examples/native-reference-cases.R`. Their 5 November 2026 review includes changed
value ranges, reordered groups and a different matrix shape. Independent comparisons
accept an explicit `group1,group2` CSV as a fourth argument; it is required for more
than two groups. Heatmap RDS files retain the heatmap and its native drawing arguments.
The heatmap runtime uses the registered ArialMT PostScript metrics for measurement
and Arial glyphs in Cairo exports; the saved session records the tested environment.

The three earlier implementations are retained in `superseded_records` in
`worked-examples.json`, with the preserved `reference-cases-legacy-20261105.R`
and successor IDs. They are excluded from the active index and recommendations.

```sh
Rscript --vanilla examples/reference-cases.R /path/to/test-output
Rscript --vanilla examples/reference-cases.R paired /path/to/input.csv /path/to/panel
```

The enrichment example uses `-log10(padj)` consistently with its axis label.
The repeated example breaks lines at missing visits. The paired example connects
unit IDs, and the independent-time example summarizes separate units at each time.
The input-shape checks validate this routing and these renders; evaluate open-ended
chart choice separately with real scientific requests.
