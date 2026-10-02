# Migration map

Old names remain documented here and in `suite.json` for searchability. Duplicate
compatibility skills are not kept active.

## Vault names to canonical skills

| Vault or former suite name | Canonical owner | Change |
|---|---|---|
| `scientific-reproducibility` | `ensure-biomedical-reproducibility` | Narrowed to provenance, lineage, audit, and consistency |
| `research-provenance` | `ensure-biomedical-reproducibility` | Consolidated the partial redesign under the portable action name |
| `research-verification` | `verify-biomedical-analysis` | Consolidated under the canonical verification owner |
| `scientific-plotting` | `create-scientific-figures` | Renamed to an action and made canonical |
| `sc-plotting` | `create-scientific-figures` | Duplicate retired; single-cell recipes retained as references |
| `scientific-visualization` | `create-scientific-figures` | Unique publication/export guidance distilled; monolith retired |
| `pathway-enrichment` | `analyze-pathway-enrichment` | Retains defensible ORA, ranked enrichment, and sample-score interpretation without tool-specific setup in the core |
| `single-cell` | `analyze-single-cell` | Router renamed to state the action |
| `sc-conventions` | `apply-single-cell-conventions` | Scope made explicit |
| `sc-catalog` | `curate-single-cell-datasets` | Discovery/catalog behavior made explicit |
| `sc-dataretrieval` | `retrieve-single-cell-data` | Acquisition/validation behavior made explicit |
| `sc-preprocessing` | `preprocess-single-cell-rna` | Modality and action made explicit |
| `sc-integration` | `integrate-single-cell-data` | Action made explicit |
| `sc-annotation` | `annotate-single-cell-types` | Outcome made explicit |
| `sc-pseudobulk` | `test-single-cell-expression` | Scientific question replaces implementation nickname |
| `sc-differential-abundance` | `test-single-cell-abundance` | Scientific question replaces acronym-oriented name |
| `sc-trajectory` | `infer-single-cell-trajectories` | Action made explicit |
| `sc-cellchat` | `infer-cell-cell-communication` | Method-independent scientific action replaces a package name |
| `sc-grn` | `infer-single-cell-regulation` | Outcome replaces acronym |
| `sc-spatial` | `analyze-spatial-transcriptomics` | Domain and action made explicit |
| `sc-crispr` | `analyze-perturb-seq` | Assay and action made explicit |
| `sc-target` | `prioritize-single-cell-targets` | Outcome made explicit |
| `autoskill` | `maintain-biomedical-skills` | Conceptual self-growth is replaced by tested, approval-gated governance |
| `sc-paper-distill` | `distill-biomedical-methods` | Generalized across biomedical study types and routed through governance |
| `distill-omics-papers` | `distill-biomedical-methods` | Expanded from omics papers to papers, protocols, registrations, data records, and code across biomedical domains |

## New universal capabilities

These are new canonical suite responsibilities, not necessarily topics absent from
the vault. Some vault packages overlap them but combine scientific policy with a
particular language, library, database, or document workflow; those remain optional
specialists or adapters rather than one-to-one retired aliases.

| Skill | Scope |
|---|---|
| `design-biomedical-study` | Units, estimands, sampling/allocation, bias controls, analysis sets, and study readiness |
| `validate-biomedical-data` | Domain-neutral structural integrity, missingness, chronology, identifiers, units, and analysis readiness |
| `synthesize-biomedical-evidence` | Answer a research question across studies with traceable search, appraisal, and uncertainty |
| `evaluate-biomedical-models` | Leakage-resistant evaluation, calibration, uncertainty, operating points, subgroups, and transportability |
| `model-time-to-event-outcomes` | Clinical/epidemiologic event-time estimands, censoring, competing events, models, and diagnostics |
| `evaluate-medical-imaging-models` | Patient/specimen-aware imaging validation, acquisition, geometry, reference standards, leakage, and task metrics |
| `analyze-dose-response` | Replicate-aware experimental dose-response QC, curve fitting, comparisons, and bounded potency/efficacy claims |

The last three are reference vertical slices: each combines a focused skill, a
contract-extension schema, and a domain verification profile. They demonstrate how
to add a domain without turning the foundation into a universal monolith.

## Registry version 1 to version 2

| Earlier concept | Version 2 representation |
|---|---|
| One overloaded `layer` | `kind` for operational shape, `stage` for workflow position, and `scopes` for scientific applicability |
| One dependency list | `requires` for hard dependencies and `recommends` for optional composition |
| Router behavior implicit in prose | Explicit `routes_to` |
| Runtime/tool assumptions embedded in skills | `optional_capabilities` with adapter fallbacks |
| Compatibility directories | `legacy_names` aliases without duplicate active skills |
| Manual install groupings | Top-level bundles with `includes` and `skills` |
| Domain checks embedded in the core | Named `resource_profiles` linking contract extensions and verification catalogs |

All canonical packages remain flat under `skills/`. Bundles such as `core`,
`general`, `single-cell`, `spatial`, `clinical`, `imaging`, `experimental`, and
`governance` are registry selections rather than filesystem hierarchies.

## Artifact migration

New analyses should create schema-version 1.1 run bundles. Version 1.1 adds nested
units, outcomes, analysis sets, governance declarations, physical/computational
resources, generic unit-set evidence, explicit denominators, verifier independence,
strict rerun records, and top-level `extensions` objects.

Do not rewrite archived 1.0 bundles merely to update their label. For an active
analysis, create a new 1.1 bundle, preserve old artifacts as immutable sources, and
record the migration as provenance. Activate a registered resource profile when the
analysis needs single-cell, clinical time-to-event, medical-imaging, or dose-response
fields and checks.

The pre-existing generic statistics, literature, plotting-library, and file-format
skills remain optional specialists or adapters. They are not copied into this suite
unless a future audit shows that a biomedical rule cannot live cleanly in the
foundation, cross-domain, domain, or governance layers.
