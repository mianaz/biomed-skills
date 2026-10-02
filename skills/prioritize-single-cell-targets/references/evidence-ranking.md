# Target evidence and ranking guide

## Keep evidence components distinct

| Component | Example evidence | Principal limitation |
|---|---|---|
| Cell-state relevance | scDRS, cell-type heritability enrichment | Association and gene-set dependence |
| Variant-to-gene | Fine-mapping, eQTL/sQTL colocalization, chromatin links | LD, context mismatch, multiple causal signals |
| Expression/state | Replicate-aware expression or abundance in relevant cells | Disease consequence may be downstream, not causal |
| Regulation | TF activity, motif/enhancer support | Inferred network, often non-causal |
| Perturbation | Perturb-seq, CRISPR, pharmacology, rescue | Assayed context, efficacy, and off-target limits |
| Tractability | Modality, binding pocket, cell-surface accessibility, existing drugs | Feasibility does not imply efficacy |
| Safety | Normal-tissue expression, essentiality, human genetics, toxicology | Incomplete tissues and context dependence |

## Genetics checks

- Harmonize genome build, variants, alleles, effect direction, ancestry, and LD
  reference. Flag palindromic/ambiguous variants and sample overlap.
- Use fine-mapped credible sets or conditional signals when available. Single-signal
  colocalization assumptions can fail at loci with allelic heterogeneity.
- Prefer tissue/cell-state-matched QTL evidence; absence in a bulk QTL resource is not
  evidence of no regulation in a rare state.
- Treat nearest-gene mapping as one weak component, not the default answer.
- Separate evidence for gene identity from evidence for whether inhibition or
  activation is desirable.

## scDRS and cell-state relevance

Keep cell-type heritability enrichment and per-cell scoring distinct. LDSC-style
partitioned-heritability analyses ask whether GWAS heritability is enriched in
annotations derived for a cell type or state; scDRS scores individual cells from a
GWAS-derived gene set relative to matched control gene sets. The methods answer
different questions and do not validate one another merely by agreeing.

Document the GWAS-derived gene-score construction, gene-set size, matched control gene
sets, covariates, species/identifier mapping, and aggregation from cells to biological
units or states. Test sensitivity to defensible gene-score/set choices. Avoid declaring
a rare visual UMAP hotspot a disease cell type without replicate-level support.

## Mutable evidence resources

Open Targets, GTEx/QTL catalogs, DepMap, drug databases, and literature indexes change.
Query through an available trusted connector or documented API, cache the returned
records, and register release/retrieval details with
`ensure-biomedical-reproducibility`. Verify current official schemas instead of copying
an embedded GraphQL query into the skill.

Aggregator scores often reuse genetics, literature, pathway, and drug evidence already
present elsewhere in the matrix. Track original evidence IDs and sources so correlated
components are not counted repeatedly.

## Transparent ranking

Prefer an evidence matrix plus component-specific ranks. If a composite is needed:

1. transform only comparable metrics;
2. prespecify direction and weight for each component;
3. make hard gates explicit;
4. keep missing values distinct from negative evidence;
5. repeat across reasonable weights and missing-data treatments; and
6. report rank ranges, conflicts, and which component drives each top candidate.

Use a consensus set only when candidates remain strong across defensible specifications.
Do not present a majority vote among correlated evidence sources as independent
confirmation.

## Minimum handoff for top candidates

For each candidate provide the disease and cell context, proposed intervention
direction, supporting genetic locus and variant-to-gene evidence, single-cell support,
regulatory/perturbational evidence, tractability, safety/liability evidence, conflicting
findings, missing evidence, rank stability, and the next discriminating experiment.
