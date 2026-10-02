# Candidate annotation methods

Use candidate methods to generate hypotheses at the same intended vocabulary level.
Do not compare one method's fine subtypes with another method's coarse compartments.

## Cluster markers

Rank positive and negative markers for each cluster against relevant neighboring
clusters. Use effect size, detection fraction, specificity, and donor consistency;
do not rank by p-value alone. These markers feed the verification gate.

## Reference label transfer

Seurat anchor transfer or analogous nearest-reference mapping can work when query and
reference share species, tissue, age/stage, assay, and cell states. Preserve mapping
scores and an unmatched option. A transferred label is a candidate, especially under
domain shift.

## Reference classifiers

- SingleR with a suitable celldex or custom reference compares transcriptomic
  profiles to labeled reference populations.
- Azimuth and SCimilarity provide atlas-oriented pretrained references where their
  supported domains match the query.
- Garnett-style marker-file classifiers can be portable and auditable when their
  marker rules are documented.

Check reference provenance, vocabulary, training tissue, species, assay, age, disease,
and version. Never choose a classifier solely because it returns a label for every
cell.

## Model-assisted interpretation

A general reasoning model may independently propose candidates from the tissue,
species, cluster's positive and negative markers, and enriched pathways. Request a
structured result containing candidate label, confidence, rationale, contradictory
evidence, and an `unknown` option. Do not supply patient identifiers or unpublished
sensitive data. Treat the output as one bounded opinion; it neither cites markers
reliably by default nor replaces the verification gate.

## Combine candidates

Keep each method's call and score. Harmonize labels to a shared vocabulary, compare
agreement on the same cells, then adjudicate with canonical markers and biological
context. Majority vote cannot rescue a shared reference-domain error.
