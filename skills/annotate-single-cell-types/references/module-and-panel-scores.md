# Module and panel scores

Module scores describe programs or states on top of discrete identities. They are
relative to the dataset, method, background genes, and expression depth.

## Score responsibly

1. Use a published or otherwise justified gene set and retain its citation, species,
   direction, and version.
2. Map symbols and orthologs before scoring; report missing and duplicated genes.
3. Use a rank-based method such as UCell when robustness to library size is important,
   or a background-matched method such as Seurat `AddModuleScore` when its assumptions
   fit. Keep the exact implementation and controls.
4. Inspect score distributions across cell type, donor, sample, QC, and condition.
5. Call the result a program score, not a cell type or pathway-activation proof.

## Example immune and TLS seeds

- A TLS-imprint panel may combine immunoglobulin genes; B/plasma markers such as
  CD79A, MZB1, XBP1, FCRL5, and SSR4; T-cell genes such as TRBC2 and IL7R; stromal
  genes such as CXCL12 and LUM; and complement genes such as C1QA and C7. Use the
  exact published species-specific set rather than reconstructing it from this seed.
- A 12-chemokine TLS signature contains CCL2/3/4/5/8/19/21, CXCL9/10/11/13, and
  CCL17 in a human-oriented representation. Orthology is not one-to-one for every
  chemokine; document any mouse substitution instead of silently renaming genes.
- For a compact naive/B-cell seed, MS4A1, CXCR5, SELL, CD19, LTB, CD79B, CD37, CD79A,
  and TCL1A can support a context-specific module, but it is not a universal TLS
  definition.

## Bulk-to-single-cell bridge

When a signature originates from bulk differential expression:

1. select genes with a prespecified direction, effect, evidence, and size rule;
2. map them to the single-cell feature universe and score cells;
3. verify enrichment in plausible cell types and check ambient/QC associations; and
4. reverse-validate by pseudobulking single-cell counts with
   `test-single-cell-expression` and comparing replicate-level fold-change direction
   with the bulk result.

Enrichment without reverse fold-change concordance can reflect library size, ambient
RNA, or cell-composition effects rather than the intended program.
