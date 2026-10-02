# Catalog record

Use one row or structured object per distinct study-assay-cohort combination. A
single publication may therefore have several records.

## Core fields

| Field | Meaning |
|---|---|
| `dataset_id` | stable local identifier |
| `repository` / `accession` | primary public source and accession |
| `related_accessions` | sample, subseries, superseries, or sibling records |
| `title` / `publication_id` | publication linkage, preferably DOI or PMID |
| `species` / `tissue` / `disease` | biological scope |
| `assay` / `platform` / `chemistry` | measurement technology |
| `specimen_type` | cells, nuclei, sorted population, tissue section, or other |
| `n_individuals` / `n_specimens` / `n_libraries` | distinct replication counts |
| `conditions` | disease, treatment, time, genotype, or other design factors |
| `file_classes` | raw droplets, filtered counts, count table, processed object, reads, normalized-only |
| `metadata_completeness` | availability of sample-, donor-, and cell-level annotations |
| `access` | open, controlled, manual, unavailable, or unknown |
| `validation_status` | verified, conflict, or unverified |
| `inclusion_status` | included, excluded, candidate, or manual-review |
| `evidence` | source, retrieval date, and exact locator for material claims |
| `notes` | concise caveats not represented elsewhere |

Use structured lists rather than comma-packed free text for conditions, file
classes, evidence, and related accessions.

## Keep statuses orthogonal

- `validation_status` describes whether the factual record is supported.
- `inclusion_status` describes whether the dataset satisfies the current question.
- `access` describes the acquisition barrier.

A verified study can be excluded, and an unverified study can remain a candidate.
Do not collapse these states into a single “good/bad” field.

## Deduplicate without erasing structure

1. Exact accession match: update the existing record unless the accession contains
   distinct assays or cohorts that need child records.
2. Exact DOI with different accessions: link records; inspect whether they are
   mirrors, modalities, subseries, or independent cohorts.
3. Similar title or author/year only: flag as a possible duplicate for review.
4. Parent series and subseries: retain both relationships and promote only the
   sample-level scope that matches the inclusion criteria.

Never merge on title similarity alone. Preserve aliases so later searches find the
record under any public identifier.
