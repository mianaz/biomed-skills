# Data readiness report

Produce a concise human summary plus machine-readable tables.

## Required sections

1. **Intended use:** contract/question IDs and analyses this audit covers.
2. **Inventory:** object ID, role, locator, format, size/count, hash/version, sensitivity.
3. **Unit hierarchy:** unit types, parent relationships, identifier fields, counts.
4. **Accounting:** eligible, expected, received, duplicated, excluded, missing,
   unevaluable, and analyzable counts with reasons.
5. **Schema:** observed fields/types/units/categories versus expected definitions.
6. **Integrity:** file, relationship, identity, range, chronology, and alignment checks.
7. **Missingness:** amount and pattern by important group, site, batch, time, and unit.
8. **Leakage:** target/future/group overlap and split-boundary findings.
9. **Transformations:** source → output mapping, rule, authorization, before/after count.
10. **Issues:** stable issue table and readiness decision.

## Issue fields

| Field | Meaning |
|---|---|
| `issue_id` | Stable identifier |
| `severity` | blocking, material, minor, informational |
| `category` | identity, schema, missingness, range, relationship, leakage, provenance, governance, other |
| `objects` | Affected object and unit IDs |
| `evidence` | Exact file/table/field/row-range or generated check artifact |
| `impact` | Which question, model, or population can change |
| `action` | Repair, restrict, obtain clarification, or stop |
| `status` | open, accepted, resolved, not_applicable |

## Completion logic

`ready` requires no unresolved blocking or material issue for the intended use.
`ready_with_conditions` requires explicit restrictions and owners. `scope_only` names
the narrower valid use. `not_ready` names the blocking condition without attempting a
scientific analysis.

Do not collapse issue counts into a quality score. One identity or leakage failure can
matter more than hundreds of clean range checks.
