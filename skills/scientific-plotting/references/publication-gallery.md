# Retrieve and adapt a publication panel

Use this route for new charts and publication-style requests after reading the data.
The bundled metadata catalog indexes 1,000 independent panels from Cell, Nature and Science:
836 reviewed reproductions and 164 original-artwork references.
The 2026-11-14 batch adds 200 panels from 24 previously unindexed Nature papers,
with 58 panel-mapped author-code records and 4 partial mappings. Thirty-six adapters
passed individual source-image comparison, original and replacement-data execution,
font/export checks, and cross-language statistical checks on 2026-11-15. Titles,
coloured strips, palettes, statistical labels, legends and shared axes retain the
published design. Two Wright–Fisher panels use a documented 1,000-run reanalysis
with a new seed because the published seed is unavailable.
The other 22 mapped panels await missing or inaccessible numerical inputs.
See `assets/publication-gallery/batch-20261114.json` for sources and counts.
R and Python versions of one panel count once. Search results retain source and review status.
Original crops and R/Python adapters stay in a separately connected local library.
Search works without that library; copying and original-versus-replica previews need it.

## Select from the question and data

Infer the task and design from the user's question and table. Translate Chinese
requests into the task names below; the search script's optional keyword matching
uses English field names. Do not ask the user to choose a task code.

| Reading task | `--task` |
|---|---|
| Compare outcomes between groups | `group-comparison` |
| Inspect spread, tails or heterogeneity | `distribution` |
| Compare two quantities or show effect estimates | `association` |
| Follow an outcome over measured time | `time-course` |
| Show response across concentrations | `dose-response` |
| Show time-to-event estimates | `survival` |
| Compare feature-by-sample patterns or two-summary dot matrices | `matrix` |
| Show differential effects or enrichment results | `enrichment` |
| Show category counts, fractions or flows | `composition` |
| Display supplied low-dimensional coordinates | `embedding` |
| Display spatial values or classes | `spatial` |
| Show a supplied hierarchy | `hierarchy` |
| Display flow-cytometry profiles | `flow` |
| Show genomic coordinates and features | `genomic` |
| Show relationships, edges or connectivity | `network` |
| Display supplied vector fields or phase portraits | `dynamics` |
| Compare set membership and intersections | `intersection` |
| Inspect supplied ROC, precision-recall or calibration results | `prediction` |

Run from this skill folder, or use the script's absolute path:

```sh
python3 scripts/publication_gallery.py recommend \
  --task group-comparison --design independent \
  --query "cell viability treatment control percent" --language R \
  --limit 3 --html /path/to/output/gallery-candidates.html
```

Set `--design` to `independent`, `paired`, `repeated` or `unspecified` from the
actual study; arbitrary row IDs do not establish pairing. A template's design
support describes its input and rendering capability for new data, not the design
of the source study. Unreviewed design support stays `unspecified`; a time axis
alone does not establish repeated units. Retrieval filters on task, reviewed design
support, language and completed review. Among compatible panels it ranks verified
source data plus panel-mapped author code first, panel-mapped author code second,
verified data third, then other reproductions. Keyword overlap and simpler input
contracts break ties. An explicit
`--chart` can retrieve a reviewed named style; circular decorative layouts do not
gain priority merely because they appeared in a journal.

Inspect the candidate's design evidence, `inputs`, `method` and `input_note`. Map
the user's columns, units, group levels and pair/subject IDs to the required fields;
check that the renderer retains the intended comparisons and identities. A familiar chart name
can require summary intervals, density profiles, sampled curves or linkage tables.
Compute those from the user's data in the shared analysis workflow when supported;
the adapter only displays them. In particular, survival adapters do not fit survival
models, dose adapters do not fit response models, and embedding adapters do not
compute coordinates. Keep the user's experimental units and valid supplied results.

For each new chart, show 2–3 compatible candidates when available in
`gallery-candidates.html`, with the original, R/Python preview, input fields and
design evidence. Show fewer when fewer fit. Choose the encoding that exposes the
primary contrast, explain its fit in one sentence, and retain its key and DOI in
figure notes. Continue with that choice unless the user requested a selection step.
Appearance-only repairs keep the existing layout.

When specific-design results are scarce, `--design unspecified` can find additional
visual references. Label them as requiring a design/input check before adaptation;
only treat them as compatible after inspecting the schema and rendering code.
For supplied matrices, embeddings or upstream model results whose rendering does
not encode experimental pairing, use `unspecified` and retain the upstream design
in the analysis record. If nothing fits, use `analysis-to-chart.md` and `visual-gallery.md`; paired
points are preferable to forcing paired data into an independent-group template.
For Prism deliverables, use `graphpad-prism`; these adapters supply R/Python sources.

## Connect and use local sources

Connect a supplied panel library once:

```sh
python3 scripts/publication_gallery.py register \
  --id cns-20261016 --library /path/to/panel-library
```

This saves only a local path in `~/.config/biomed-skills/publication-gallery.json`.
Alternatively pass `--library /path/to/panel-library` to `recommend` or `stage`.
The package contains no original crops, estimated numerical tables or private paths.
If the library is unavailable, show metadata candidates and state that the source
previews and adapter files are unavailable. Use a connected library or the standard
plotting route for execution.

Copy a selected template into a new output folder:

```sh
python3 scripts/publication_gallery.py stage cns-20261016/D09-p03 \
  --language R --output /path/to/new-panel
```

Read the copied `adapt-data/README.md`, `schema.json` and `method.json`. Map the
user's measured values or valid upstream outputs to those fields. Replace all source
significance labels, intervals, groups and units with current results before presenting
a new figure. The original is retained for comparison. Staging copies example inputs;
it neither converts the user's data nor executes an analysis.

For ordinary figures apply the project palette, Arial and the shared effective-size
rules. For requested original-style replication preserve the reference geometry and
style, then assess its intended placement. The unified R route prefers tidyplots
for ordinary encodings; use native template code when its specialized geometry or
the requested reference fidelity requires it. Run the selected code, retain direct
shared source data and rerunnable code (object when useful), and inspect the saved result as usual.

## Expand the catalog

Prioritize verified source data with panel-mapped author plotting code, followed
by panel-mapped author code. Record an exact figure/panel locator, repository commit, file and mapping
basis in the panel context. A repository link alone does not establish that its
code draws the selected panel. Retain the original artwork beside both native
implementations. Distinguish deposited data, supplied upstream results and
image-derived estimates in the input guide and `data_basis`.

The dated `assets/publication-gallery/source-evidence.json` records verified
panel-code mappings and which author tables feed the current adapter. Preserve
separate annotation provenance when printed labels use a different source or
revision. Recheck this evidence when the adapter or source mapping changes.
The shared search and publication-only search use the same source-priority rule;
see [reference-libraries.md](reference-libraries.md) for cross-library selection.

Inspect every crop against its full source page. Remove neighboring lines and
partial text by correcting the crop bounds. Omit publication panel letters from
reconstructions; retain biological labels. Prefer mapped author tables, then
calibrated visible values or native PDF geometry. Keep data in shared editable
inputs and style in each script. Never invent hidden observations or replay chart
pixels as data. Test changed values and category names in both languages.

Expand underrepresented encodings: annotated matrices, genomic tracks, spatial
maps, networks, hierarchies, vector fields, intersections and quantitative
composites. Preserve their layers and input relationships. Do not turn them into
generic scatter plots, split one composite into multiple entries, or repeatedly
add simple charts from the same paper to meet a count.

A library has `manifest.json` and `panels/<id>/` folders containing `context.json`,
`method.json`, `adapt-data/schema.json`, input guides, and language-specific
`R/adapt.R` or `python/adapt.py` sources and exports. Index an additional batch into
an editable catalog copy:

```sh
python3 scripts/publication_gallery.py index --id cns-next-batch \
  --library /path/to/next-library --catalog /path/to/catalog.json
```

Start that catalog by copying `assets/publication-gallery/catalog.json` to retain
the bundled entries. Reindexing replaces only the named library namespace. Pass
`--catalog /path/to/catalog.json` to searches and staging. Connect its path with
`register` for local previews. New chart families need a reviewed task mapping in
`classify()`; unclassified entries remain outside automatic recommendations.

Record explicit design support with its schema/code evidence when curating an
adapter. Keep the bundled `design-support.json` alongside the catalog when
installing or packaging so reindexing retains reviewed capability annotations.

An adapter is eligible only when both language sources/previews and an input contract
exist, and its `adapt-review.json` has `verdict: "pass"` plus explicit true values for
`visually_reviewed`, `style_reviewed`, `code_second_reviewed` and
`data_replacement_passed`. These fields record completed work, not checks performed
by the indexer. Pending batches remain searchable metadata, excluded from automatic
recommendations and execution. Reindex after review or source changes. Staging
checks the current per-panel review again.

New batches may instead keep `visual-review.json`, `code-review-2.json` and
`replacement-check.json` as separate evidence. Each must pass against the current
files. The indexer reads these records; it does not perform their reviews.
