# Method selection and input construction

## Choose from the available statistical object

| Available object | Appropriate analysis | Required safeguards |
|---|---|---|
| Predefined hit list | ORA | Explicit eligible universe, declared hit rule, threshold sensitivity |
| Complete signed gene-level statistic | Ranked GSEA | No prefiltering by significance, declared rank direction, duplicate resolution |
| Normalized genes × biological samples | Per-sample scoring | One score definition, replicate-aware downstream model, sample diagnostics |
| Cell-level expression | Exploratory cell scores only | Do not test cells as replicates; summarize or model at the donor/specimen level |

For single-cell condition contrasts, prefer a complete pseudobulk rank table within
each adequately replicated cell type. The ranking statistic must come from the
sample-level design and retain its sign. A marker ranking computed across cells does
not become replicate-aware merely because enrichment is run afterward.

## Construct ranks and lists

- Prefer a signed model test statistic when available because it combines direction
  with model-based uncertainty. State which condition is positive.
- Do not rank by raw p-value, adjusted p-value, or absolute effect: each loses
  direction. Fold change alone can over-rank unstable, low-information features.
- If a signed statistic is unavailable, define and justify a monotone signed score,
  then test sensitivity. Never substitute zeros or extreme values for missing tests.
- Apply ORA hit thresholds before viewing enrichment results. If up- and down-hit
  lists are separate, correct and report them as declared testing families.

## Define the ORA universe

Use features that could have become hits under the upstream assay and test:

- RNA sequencing: genes retained and actually tested after expression filtering;
- proteomics: proteins quantified and eligible for the contrast;
- genetic screens: perturbations represented and evaluable after screen QC.

Map the hit list and universe through the same identifier pipeline. A whole-genome or
library-default universe is not interchangeable with the assay-accessible universe.
For ranked enrichment, the analogous domain is every gene with a finite eligible
ranking statistic.

## Select collections

- **Hallmark:** broad programs with reduced redundancy; useful as a first summary.
- **Reactome:** curated pathways with parent-child structure and substantial overlap.
- **GO BP/MF/CC:** ontology annotations with nested, correlated terms; choose the
  namespace that matches the question and record any evidence-code restrictions.
- **Other curated collections:** use only when their scope, organism, license, and
  release answer the stated question.

Choose gene-set size bounds before analysis. Very small sets are unstable and large
generic sets can dominate; justify bounds from collection content and mapped
coverage rather than treating one numerical default as universal.

## Map identifiers without hiding attrition

Freeze the organism, annotation build where relevant, source namespace, target
namespace, and mapping release. Remove version suffixes only when they are known to
be suffixes for that identifier system. Prefer stable one-to-one mappings; when
features collapse to one gene or one feature maps to several genes, record the full
mapping and the deterministic resolution rule. Report unmatched fractions and gene
set coverage before interpreting an empty or weak result.
