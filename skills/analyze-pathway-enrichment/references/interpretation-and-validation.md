# Interpretation and validation

## Read each result according to its method

ORA reports whether a thresholded list overlaps a set more than expected under its
declared universe. Report the overlap count, mapped set size, effect measure, p-value,
and adjusted p-value. ORA does not supply pathway direction; direction exists only if
the query list itself was defined as positive or negative.

Ranked GSEA reports whether set members accumulate near one end of the complete rank.
Report the enrichment score definition used by the chosen implementation, normalized
score when available, p-value, adjusted value, and leading-edge genes. Interpret the
sign only after restating what a positive input statistic means.

Per-sample methods yield relative scores whose scale depends on normalization,
method, collection, and cohort. Do not compare absolute scores across separately
processed datasets unless calibration supports it.

## Control multiplicity and redundancy

- Declare the tested collections, contrasts, cell types, and directions before
  filtering results.
- Record the exact family over which adjusted values were computed. A correction
  performed separately within each library does not control errors across a larger
  collection of libraries or contrasts.
- Keep the complete table and distinguish prespecified confirmatory pathways from
  exploratory discovery.
- Quantify term overlap using shared genes, leading edges, ontology ancestry, or a
  declared similarity measure. Cluster correlated terms and choose representative
  labels by an explicit rule; retain membership of every cluster.
- Do not count related GO children or nested Reactome pathways as independent
  biological replications.

## Validate sample-level pathway claims

For each reported activity difference:

1. Show scores by biological sample, not only group means or cells.
2. Fit a design that preserves pairing, repeated measures, batch, and relevant
   covariates; report biological `n` and uncertainty.
3. Check that multiple signature genes contribute coherently rather than one highly
   weighted or abundant gene determining the score.
4. Inspect influential samples and repeat the summary with leave-one-sample or
   leave-one-donor sensitivity when replication permits.
5. Compare reasonable normalization, set-size, mapping, and release choices. Label a
   conclusion unstable when its sign or support changes materially.
6. Seek an independent cohort, orthogonal assay, or targeted functional readout for
   external validation. A score and GSEA derived from the same data are concordance,
   not independent replication.

For single-cell data, cell-level heatmaps or embeddings can localize a program, but
condition-level inference must retain donor/specimen replication. Do not feed derived
activity scores into a raw-count differential-expression model.

## Preserve pathway-specific provenance

Retain:

- source, exact release/version or retrieval date, organism, and unmodified gene-set
  file checksum when available;
- any set edits, namespace conversion, ortholog mapping, and mapping resource release;
- the eligible universe, hit rule or rank formula and direction, tied-feature rule,
  gene-set size bounds, permutation settings and seed when relevant;
- multiplicity family, redundancy rule, complete results, overlap/leading-edge genes,
  sample-level score matrix, design, diagnostics, and sensitivity results.

Use these records to distinguish “not supported” from “inconclusive because coverage
or power was inadequate” and from a technical failure such as an organism mismatch.
