---
name: maintain-biomedical-skills
description: Audit and evolve a biomedical skill suite without duplication, scope drift, broken resources, stale knowledge, or platform lock-in. Use when creating or updating skills, consolidating overlapping skills, promoting a proven workflow or paper-derived method, reviewing names and triggers, validating a cross-agent release, deprecating old behavior, or cleaning project and long-term memory. Prefer composition before creating a new skill and require provenance, evidence of reuse, tests, ownership, and an explicit approval gate for material promotions.
---

# Maintain biomedical skills

Keep one canonical active implementation for each responsibility. Treat the suite as
maintained software, not an append-only note collection.

## Audit first

Run the deterministic audit before proposing changes:

```bash
python scripts/audit_skill_suite.py /path/to/repository/skills --output skill-audit.json
```

Review errors before warnings. Read `references/scope-and-naming.md` when a name,
trigger, or boundary may change.

## Choose the smallest change

Use this order:

1. Reuse the existing skill unchanged.
2. Add or correct one focused reference, script, or decision rule.
3. Compose two skills through explicit routing.
4. Split a skill whose responsibilities or triggers are genuinely independent.
5. Create a new skill only when no current owner can absorb the capability cleanly.

Do not keep active aliases with copied bodies. Record old names in a migration map
and route users to the canonical skill.

## Promotion gate

Stage a candidate with `assets/promotion-proposal.template.json`. Require:

- a concrete source: repeated successful runs, a meaningful benchmark, a verified
  user failure/fix, or a method-and-code distill with provenance
- evidence that the pattern generalizes beyond one project
- known limitations and failure cases
- an overlap and name-collision check
- the smallest target skill and exact proposed diff
- deterministic validation plus a realistic forward test when practical
- a maintainer and review date
- explicit approval before changing shared behavior

Recurrence alone is insufficient: repeated failure, accidental behavior, or copied
boilerplate must not become policy.

## Lifecycle

Use four states:

1. **Raw:** unreviewed observation, run note, paper extraction, or user feedback.
2. **Staged:** structured proposal with provenance and evidence.
3. **Evergreen:** validated, approved, canonical suite knowledge.
4. **Archived:** superseded or rejected material retained only when it supports
   provenance, migration, or a known limitation.

Keep raw and project-specific material outside active skill bodies. Assign evergreen
knowledge an owner, version, verification date, and next-review date. Archive or
delete stale duplicates rather than accumulating Markdown.

## Release checks

- Folder name equals frontmatter `name`; names are unique and action-oriented.
- Description states both capability and trigger; exclusions prevent overlap.
- `SKILL.md` is concise and detailed material is one reference hop away.
- Every referenced file exists; every bundled script has been executed in a test.
- Platform-specific paths, model names, agent APIs, schedulers, and memory stores live
  in optional adapters, not the core domain skill.
- Machine-readable schemas reject unknown core fields while allowing a documented
  `extensions` object.
- Migration, precedence, and deprecation are explicit.
- A fresh agent can use the skill without leaked design intent or hidden artifacts.

Do not auto-install, publish, overwrite, or delete shared skills during an audit.
Present the proposed changes and their evidence first.
