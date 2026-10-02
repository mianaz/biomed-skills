# Marker verification

This is the mandatory final gate for every cell-type label.

## Verify a label

1. Select a context-appropriate panel with several canonical positive markers,
   discriminating markers against nearby types, and known contradictory markers.
2. Attach a PMID, DOI, or authoritative atlas/database reference to each panel row.
3. Inspect expression prevalence and level by proposed type, cluster, donor, and
   sample in the uncorrected normalized expression space.
4. Confirm that the pattern is coherent, not driven by one sample, a few cells,
   ambient RNA, or a doublet-rich subset.
5. Record `verified`, `provisional`, `mixed`, or `unknown`, with supporting and
   contradictory evidence.

Use a two-level default:

1. assign and verify coarse compartments;
2. subcluster within each verified compartment; and
3. assign and verify fine subtypes.

## Adjudicate disagreement

- Favor coherent, cited marker evidence over an automated confidence score.
- Coarsen when a fine subtype lacks discriminatory evidence.
- Preserve `unknown` when no candidate is supported.
- Revisit QC, ambient RNA, doublets, integration, or clustering when incompatible
  lineages co-occur.
- Do not use the same marker panel both to define labels and as independent proof of
  their discriminatory power.

For each final label retain the candidate methods, canonical markers, contradictory
markers, citations, reference vocabulary, annotator rationale, and annotation
version.
