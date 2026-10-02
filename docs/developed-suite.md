# Developed skills suite

Snapshot: 2 October 2026. Suite version **0.2.0**; **32 canonical skill packages**, arranged into **8 install bundles**. The figure skill is version **3.17.1**.

The deliverable is a portable agent skill suite: instructions, method references, templates, schemas, examples and selected executable helpers. Most analysis packages guide an agent through choosing and running scientific tools; they are not standalone analysis pipelines.

## What is implemented

- **Figures:** R/Python plotting helpers, dose-response helpers, environment checks, color previews, editable Prism table export, and runnable synthetic examples.
- **Paper evidence maps:** a renderer for linked claims, experiments and results, with editable map outputs.
- **Shared execution support:** analysis-contract validation, run-context capture, provenance validation and verification of analysis bundles.
- **Installation and maintenance:** dependency-aware bundle installation, registry checks, resource checks and tests.
- **Scientific workflows:** written methods and supporting references across single-cell analysis, evidence synthesis, study design, model evaluation, survival, imaging and dose response.

## Shared research skills (12)

| Skill | Purpose |
|---|---|
| [plan-biomedical-analysis](../skills/plan-biomedical-analysis/SKILL.md) | Turn an ambiguous biomedical research request into a compact, executable JSON analysis contract covering objectives, questions, nested study units, outcomes, analysis sets, governance risks, inputs, planned steps, outputs, validation, constraints, audiences, and operating profile. |
| [design-biomedical-study](../skills/design-biomedical-study/SKILL.md) | Design a biomedical study before data collection or before an existing study is analyzed by defining the decision, target population, unit hierarchy, intervention or exposure, controls, endpoints, allocation, blinding, replication, precision, bias controls, governance, and analysis handoff. |
| [ensure-biomedical-reproducibility](../skills/ensure-biomedical-reproducibility/SKILL.md) | Capture platform-neutral provenance and result lineage for computational, experimental, clinical, and imaging analyses in a validated JSON run manifest, including digital or physical inputs, external sources, protocols, instruments, reagents, models, code or procedures, runtime versions, parameters, QC status, artifacts, deviations, and strict locks. |
| [validate-biomedical-data](../skills/validate-biomedical-data/SKILL.md) | Audit biomedical data before analysis by checking inventory, identity, schema, granularity, unit hierarchy, file integrity, cross-table relationships, duplicates, missingness, ranges, units, timestamps, labels, leakage, provenance, and analysis readiness. |
| [verify-biomedical-analysis](../skills/verify-biomedical-analysis/SKILL.md) | Independently audit a biomedical analysis for design errors, statistical inconsistencies, missing or empty artifacts, broken provenance, unsupported claims, and rerun risk. |
| [orchestrate-biomedical-work](../skills/orchestrate-biomedical-work/SKILL.md) | Coordinate multi-step biomedical work across planning, domain execution, provenance, verification, and communication. |
| [communicate-biomedical-results](../skills/communicate-biomedical-results/SKILL.md) | Turn completed biomedical analyses into concise, audience-aware, evidence-backed stories, briefs, reports, manuscripts, or presentations. |
| [create-scientific-figures](../skills/create-scientific-figures/SKILL.md) | Turn biomedical research data into figures in R, Python or GraphPad Prism, including editable Prism PZFX tables. Choose charts and design-supported statistics, export editable sources, and inspect the rendered result. |
| [synthesize-biomedical-evidence](../skills/synthesize-biomedical-evidence/SKILL.md) | Answer a biomedical question by systematically finding, screening, extracting, appraising, and synthesizing literature and other citable evidence. |
| [paper-evidence-map](../skills/paper-evidence-map/SKILL.md) | Extract a single research paper's argument into an editable evidence graph linking its central claim, subclaims, experiments, controls, and observed results with exact figure and source references. |
| [evaluate-biomedical-models](../skills/evaluate-biomedical-models/SKILL.md) | Evaluate a biomedical predictive, prognostic, diagnostic, classification, regression, or risk model against its intended use using leakage-safe validation, appropriate comparators, discrimination, calibration, error, uncertainty, subgroup performance, domain shift, and decision usefulness. |
| [analyze-pathway-enrichment](../skills/analyze-pathway-enrichment/SKILL.md) | Analyze biological pathways and gene sets from thresholded hit lists, complete ranked differential-statistic tables, or sample-level expression profiles. |

## Single-cell skills (15)

| Skill | Purpose |
|---|---|
| [analyze-single-cell](../skills/analyze-single-cell/SKILL.md) | Coordinate an end-to-end single-cell transcriptomics analysis by identifying the assay and study design, choosing a canonical object, and routing public-data discovery, retrieval, preprocessing, integration, annotation, testing, trajectories, communication, and verification to the appropriate specialist skills. |
| [apply-single-cell-conventions](../skills/apply-single-cell-conventions/SKILL.md) | Keep single-cell objects, count layers, cell and feature identifiers, metadata fields, embeddings, label vocabularies, factor orders, and R/Python round trips consistent across a project. |
| [curate-single-cell-datasets](../skills/curate-single-cell-datasets/SKILL.md) | Discover, compare, deduplicate, and catalog public single-cell datasets using repository records and publication evidence, with explicit assay, organism, tissue, disease, sample, donor, access, and file-availability fields. |
| [retrieve-single-cell-data](../skills/retrieve-single-cell-data/SKILL.md) | Validate a known public single-cell accession or file collection, identify the correct samples and assay, choose the least-transformed usable count representation, acquire it safely, load it without losing raw counts or metadata, and document the authors' upstream processing. |
| [preprocess-single-cell-rna](../skills/preprocess-single-cell-rna/SKILL.md) | Convert raw or author-processed scRNA-seq and snRNA-seq counts into an analysis-ready object through assay-aware cell calling, ambient-RNA handling, gene-identifier cleanup, doublet scoring, adaptive quality control, explicit exclusions, normalization, and feature selection. |
| [integrate-single-cell-data](../skills/integrate-single-cell-data/SKILL.md) | Decide whether single-cell batch correction or reference integration is scientifically justified, select and run an embedding- or model-based method, and evaluate technical mixing against preservation of cell identity, rare populations, condition effects, and trajectories. |
| [annotate-single-cell-types](../skills/annotate-single-cell-types/SKILL.md) | Assign and verify hierarchical cell-type identities in scRNA-seq or snRNA-seq data using cluster markers, reference transfer, classifiers, curated marker panels, concordance checks, and explicit uncertainty. |
| [test-single-cell-expression](../skills/test-single-cell-expression/SKILL.md) | Test condition-associated expression changes in single-cell RNA-seq at the biological-replicate level by aggregating raw counts per sample or sample-by-cell-type and fitting an explicit pseudobulk design. |
| [test-single-cell-abundance](../skills/test-single-cell-abundance/SKILL.md) | Test whether annotated cell populations or local neighborhoods change in relative abundance across biological conditions using replicate-aware compositional methods. |
| [infer-single-cell-trajectories](../skills/infer-single-cell-trajectories/SKILL.md) | Infer and validate single-cell state progressions using graph topology, pseudotime, RNA velocity, and fate probabilities. |
| [infer-cell-cell-communication](../skills/infer-cell-cell-communication/SKILL.md) | Infer candidate ligand-receptor signaling between annotated cell populations from single-cell or spatial expression data. |
| [infer-single-cell-regulation](../skills/infer-single-cell-regulation/SKILL.md) | Infer putative transcription-factor regulons, regulatory activity, and enhancer-linked programs from single-cell RNA or paired RNA-ATAC data. |
| [analyze-spatial-transcriptomics](../skills/analyze-spatial-transcriptomics/SKILL.md) | Analyze spatially resolved transcriptomics across spot-based, bead/bin-based, and segmented imaging platforms, including spatial QC, tissue domains, spatially variable genes, neighborhood enrichment, reference-based deconvolution, and cross-section comparisons. |
| [analyze-perturb-seq](../skills/analyze-perturb-seq/SKILL.md) | Analyze pooled CRISPR perturbation experiments with single-cell readouts, including Perturb-seq, CROP-seq, CRISP-seq, CRISPRi/a, knockout, and combinatorial designs. |
| [prioritize-single-cell-targets](../skills/prioritize-single-cell-targets/SKILL.md) | Prioritize disease-relevant cell states and therapeutic target candidates by integrating single-cell expression with human genetics, variant-to-gene evidence, regulatory context, perturbation results, tractability, and safety. |

## Focused domain workflows (3)

| Skill | Purpose |
|---|---|
| [model-time-to-event-outcomes](../skills/model-time-to-event-outcomes/SKILL.md) | Analyze survival, failure-time, event-time, or time-to-event outcomes with explicit eligibility, time zero, event and censoring definitions, delayed entry, competing events, recurrent events, covariates, estimands, diagnostics, and sensitivity analyses. |
| [evaluate-medical-imaging-models](../skills/evaluate-medical-imaging-models/SKILL.md) | Evaluate medical-imaging or digital-pathology models with patient-, examination-, lesion-, reader-, site-, and device-aware validation. |
| [analyze-dose-response](../skills/analyze-dose-response/SKILL.md) | Design, validate, fit, compare, and interpret concentration- or dose-response experiments from plate, assay, animal, ex vivo, or other repeated biological measurements. |

## Suite maintenance (2)

| Skill | Purpose |
|---|---|
| [maintain-biomedical-skills](../skills/maintain-biomedical-skills/SKILL.md) | Audit and evolve a biomedical skill suite without duplication, scope drift, broken resources, stale knowledge, or platform lock-in. |
| [distill-biomedical-methods](../skills/distill-biomedical-methods/SKILL.md) | Extract reusable, provenance-rich methods, decision rules, validation patterns, figure strategies, implementation details, failure modes, and limitations from biomedical papers together with supplements, protocols, registrations, data records, and code. |

## Install bundles

`core`, `general`, `single-cell`, `spatial`, `clinical`, `imaging`, `experimental`, `governance`. Bundles overlap and reuse the same canonical packages.

## Validation and release scope

`python3 tools/check_suite.py` passes: all 32 packages are registered, resource and dependency checks have zero errors or warnings, seven suite tests pass, and the example analysis bundle passes 27 checks. These checks establish package integrity and fixture behavior; scientific performance across real datasets is not established by these tests.

This release includes the skills, their supporting resources and synthetic examples, the registry, installer, suite checks and relevant tests. Benchmark experiments, manuscript drafts, research planning, local outputs, virtual environments, credentials and historical working notes are excluded.
