---
name: validate-biomedical-data
description: Audit biomedical data before analysis by checking inventory, identity, schema, granularity, unit hierarchy, file integrity, cross-table relationships, duplicates, missingness, ranges, units, timestamps, labels, leakage, provenance, and analysis readiness. Use for clinical tables, assay or plate data, imaging collections and labels, experimental measurements, omics matrices and metadata, public datasets, or an unfamiliar multi-file delivery. Produce a machine-readable issue inventory and readiness decision; do not perform domain preprocessing, repair values silently, fit scientific models, or interpret biological results.
---

# Validate Biomedical Data

Determine what the data actually contain, whether their identities and relationships
are coherent, and which planned questions they can support. Preserve the received
data; write repaired or standardized versions as new artifacts with explicit lineage.

## Build the inventory

1. Enumerate every file, collection, table, image series, label source, data dictionary,
   and external reference. Record size, format, checksum or stable locator, ownership,
   sensitivity, and expected role.
2. Identify the independent units and every nested or repeated level. State one row,
   column, image, record, field, or measurement's actual granularity rather than its
   presumed meaning.
3. Reconcile identifiers across sources. Detect missing, duplicated, reused, malformed,
   or many-to-many keys and distinguish legitimate repeated measures from accidental
   duplication.

Read `references/validation-catalog.md` for cross-domain and modality-specific checks.

## Test structure and content

- Compare observed fields, types, categories, dimensions, and units with the delivery
  specification or inferred schema. Record every inference.
- Quantify missingness by variable, unit, group, time, site, batch, and acquisition
  source where relevant. Distinguish structural, censored, unavailable, and unexpected
  missingness when the metadata permit.
- Check impossible values, range violations, inconsistent units, timestamp order,
  duplicated content, encoding problems, truncated files, empty outputs, and broken
  foreign-key relationships.
- Reconcile cohort or sample accounting from eligible and received through excluded,
  missing, and analyzable. Never let the final row count substitute for this flow.
- Detect target, future, participant, site, image-slice, technical-replicate, or
  preprocessing leakage before any split or model is accepted.
- Verify that labels, outcomes, exposure definitions, acquisition parameters, and
  reference standards have traceable sources and usable definitions.

## Classify findings without silent repair

Assign each issue a stable ID, severity, affected objects, evidence locator, likely
impact, and proposed action. Use:

- `blocking`: planned analysis would be invalid or identities cannot be trusted;
- `material`: interpretation or a major subset can change;
- `minor`: correction is mechanical and does not change the scientific unit;
- `informational`: useful context with no required change.

Apply only reversible, rule-based corrections that the user or contract authorizes.
Save the transformation, mapping, before/after counts, and excluded records. Escalate
identity collisions, unexplained losses, protected-data exposure, and changes to
outcome or group definitions.

## Issue the readiness decision

Follow `references/readiness-report.md`. Produce an inventory, schema summary, unit
hierarchy, accounting table, missingness and range summaries, relationship checks,
leakage assessment, issue table, authorized transformations, and one decision:

- `ready`: no unresolved issue can invalidate the planned use;
- `ready_with_conditions`: named restrictions or repairs are required;
- `not_ready`: a blocking issue prevents the planned use;
- `scope_only`: the data support a narrower descriptive question.

Register inputs and transformed artifacts with `ensure-biomedical-reproducibility`,
return design-changing findings to `plan-biomedical-analysis`, and send domain QC to
the relevant domain skill. Passing this audit does not mean a clinical endpoint,
image label, assay, or biological measurement is scientifically valid by itself.
