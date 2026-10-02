# Validate an accession

Validate at the sample level before downloading. Repository summaries are useful
leads, not sufficient evidence for every field.

## Minimum checks

1. **Identity:** accession resolves, publication title/authors match, and related
   accessions are understood.
2. **Biology:** organism, tissue, disease, treatment, genotype, age/stage, and
   specimen type match the intended cohort.
3. **Assay:** measurement is single-cell or single-nucleus transcriptomics, with the
   expected platform and chemistry where reported.
4. **Replication:** distinguish individuals, specimens, libraries, lanes, and files.
   Do not treat repeated libraries from one donor as independent donors.
5. **Data kind:** identify raw droplets, filtered counts, count tables, processed
   objects, sequencing reads, and normalized-only values separately.
6. **Publication scope:** confirm that the chosen samples were analyzed in the linked
   paper and note any samples added or omitted in later repository updates.

Record each material claim as verified, conflict, or unverified with its exact
evidence locator. Keep inclusion status separate.

## Common traps

- **Spatial wording:** a true spatial assay usually has spatial coordinates and
  platform-specific outputs such as tissue-position tables, histology images, or a
  spatial pipeline directory. A paper that maps dissociated scRNA-seq cells to space
  is still a single-cell assay.
- **Sample caps:** a request for a maximum number of samples does not authorize
  promoting the first files encountered. Rank eligible biological samples and state
  the subset rule.
- **Superseries:** a parent series can contain bulk, spatial, and single-cell
  subseries. Resolve the relevant child records and sibling modalities explicitly.
- **Publication mismatch:** similar titles or shared authors do not establish that an
  accession belongs to the cited cohort.
- **Cell-count inflation:** reported cells may combine assays, species, conditions,
  or excluded samples; reconcile the count for the selected subset.
