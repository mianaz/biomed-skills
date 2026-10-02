---
name: curate-single-cell-datasets
description: Discover, compare, deduplicate, and catalog public single-cell datasets using repository records and publication evidence, with explicit assay, organism, tissue, disease, sample, donor, access, and file-availability fields. Use when searching for scRNA-seq or snRNA-seq cohorts, building a reusable dataset catalog, screening studies against inclusion criteria, or deciding which accessions merit retrieval. For a known accession or local file collection, use retrieve-single-cell-data instead.
---

# Curate Single-Cell Datasets

Build an evidence-linked catalog before downloading large files or promoting a study
as suitable.

## Choose the mode

- **Discover:** find candidate studies for stated biological and technical criteria.
- **Browse:** filter, compare, or audit an existing catalog.
- **Hand off:** when an accession is already known and accepted, send it to
  `retrieve-single-cell-data`; do not repeat the catalog workflow.

## Curate candidates

1. Convert the request into explicit inclusion, exclusion, and preference fields:
   organism, tissue, disease or perturbation, assay, platform, specimen type,
   age/stage, treatment, minimum biological replication, and access constraints.
2. Search a local catalog first. Expand to public expression archives, sequence
   archives, cell atlases, and literature indexes only where coverage is thin.
3. Read the linked publication when available. Prefer full text and supplements;
   fall back to abstract and repository metadata while marking unresolved fields.
4. Cross-check study-level claims against sample-level repository records. Confirm
   that the relevant samples, not merely the series title, meet the criteria.
5. Create or update records using `references/catalog-record.md`. Keep factual
   validation status separate from the user's inclusion decision.
6. Deduplicate conservatively by accession, DOI, and normalized title. Link likely
   duplicates or parent/subseries relationships; never auto-merge records that may
   represent different assays or cohorts.
7. Rank candidates by scientific fit, biological replication, usable count data,
   metadata completeness, access burden, and domain match. Do not rank by cell count
   alone.

## Evidence rules

- Label each material field `verified`, `conflict`, or `unverified` and retain the
  evidence locator. Absence of evidence is not a negative finding.
- Distinguish number of files, libraries, samples, specimens, and individuals.
- Distinguish actual spatial assays from papers that apply computational spatial
  methods to dissociated single-cell data.
- Record controlled-access, manual-download, or reads-only studies without implying
  that usable counts are immediately available.
- Treat repository availability as mutable; record the retrieval date through
  `ensure-biomedical-reproducibility` rather than copying general provenance fields
  into prose.

## Deliver the catalog

Return a machine-readable catalog plus a concise comparison of included, excluded,
candidate, and manual-review records. For every exclusion, preserve the criterion
and evidence. Hand accepted accessions and their sample-level scope to
`retrieve-single-cell-data`.

Use `verify-biomedical-analysis` when the catalog defines a systematic review,
benchmark, atlas, or other consequential dataset universe.
