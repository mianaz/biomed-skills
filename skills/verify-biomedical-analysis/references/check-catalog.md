# Verification check catalog

Load only the sections relevant to the run. Execute objective checks before
narrative critique.

## Bundle and artifact integrity

- Contract, manifest, and evidence IDs agree and use compatible schema versions.
- Required inputs, planned steps, and required outputs resolve across artifacts.
- Produced local files exist, are nonempty, and match recorded hashes when present.
- Failed, skipped, or unplanned steps are explicit; deviations name their impact.
- Package/runtime versions, parameters, rationale, and code entry points are present.
- No output is accepted solely because a command exited successfully.

## Units and design

- Reconstruct the analysis-set membership, unique experimental units, groups,
  replicates, missing units, repeated measures, exclusions, and technical batches
  from raw metadata.
- Confirm the analysis unit matches the experimental unit; cells, fields, wells, or
  repeated measurements are not treated as independent biological replicates.
- Confirm contrast direction and reference level.
- Confirm the design matrix is full rank and quantify group/batch confounding.
- Confirm randomization, blocking, pairing, nesting, and covariates are handled as
  specified.

## Statistical results

- Check test choice against outcome type, design, dependence, sample size, and model
  assumptions.
- Verify p-values and adjusted p-values lie in `[0, 1]`; identify the multiplicity
  family and correction method.
- Recompute a small sample of effects, signs, counts, confidence intervals, and
  adjusted p-values from the saved source table.
- Confirm effect direction is consistent across tables, figures, captions, and prose.
- Distinguish biological from technical replication and report the definition of `n`.
- Treat assumption failures as design/model findings, not formatting omissions.

## Enrichment and external knowledge

- Confirm the tested feature universe is the set that could have been selected, not
  every known feature by habit.
- Record database or ontology name, release/version, applicable population or
  organism, identifier system, query, and multiple-testing correction.
- Confirm mapping losses, duplicated identifiers, set-size filters, and direction of
  ranking statistics are visible.
- Literature support must substantiate the exact biological interpretation; method
  popularity or journal prestige is not evidence of fit.

## Figures, tables, and claims

- A figure and its source table use the same analysis set, units, exclusions, contrast,
  transformation, and statistic.
- Titles/captions do not claim more than the plotted rows support.
- Each key conclusion links to a number, table row, model output, or figure source-data
  locator.
- Image crops, adjustments, scale calibration, and reuse are recorded.
- QC, benchmark, method-concordance, and integration-metric panels do not displace the
  biological evidence in the main story unless they answer the primary question.

## Domain extensions

Keep the core catalog modality-neutral. Load registered profiles only for domains in
scope. A profile declares categories, check IDs, criteria, and default severities;
record results in `run-manifest.json` quality checks using either the profile
`check_id` or `contract_check_id`.

The bundled `single-cell-analysis` profile is registered in
`domain-check-profiles.json`. Activate it with
`--domain-profile single-cell-analysis` or
the matching entry under contract `extensions.profiles`. Register another domain
through suite `resource_profiles`; do not add its checks here.

## Verdict mapping

- `fail`: any missing required output, invalid core design, unresolved artifact/hash
  failure, unsupported headline claim, or strict-policy violation.
- `pass_with_warnings`: no blocking error, but one or more limitations could change
  interpretation or reproducibility.
- `pass`: all required checks pass; remaining limitations are already bounded in the
  claim language.
