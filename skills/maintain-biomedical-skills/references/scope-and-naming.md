# Scope and naming review

## Boundary test

Write one sentence for each candidate skill:

> This skill owns **[decision or action]** and explicitly does not own **[nearest
> neighboring responsibility]**.

If two skills produce the same sentence, merge them. If one sentence contains two
independent triggers, split it. Cross-cutting policy belongs in one foundation skill;
domain workflows reference it rather than copying it.

## Names

- Use lowercase hyphen-case under 64 characters.
- Prefer a verb plus a specific object: `annotate-single-cell-types`, not
  `sc-annotation`; `ensure-biomedical-reproducibility`, not `reproducibility`.
- Do not name a method-independent scientific action after one package.
- Keep legacy names only in a migration map; do not maintain cloned alias skills.
- Match the folder name and frontmatter name exactly.

## Descriptions

The description is the trigger. Include:

1. What outcome the skill produces.
2. Concrete user phrasings, artifacts, or contexts that should trigger it.
3. The nearest exclusions or routing boundaries.

Do not rely on a body section titled “When to use”; the body is loaded only after the
skill triggers.

## Progressive disclosure

- Keep essential workflow and routing in `SKILL.md`.
- Put detailed methods, variants, schemas, and examples in shallow `references/`.
- Put repeatable deterministic operations in tested `scripts/`.
- Put output templates and reusable deliverable material in `assets/`.
- Avoid README, changelog, installation guide, and quick-reference files inside a
  skill package.

## Overlap resolution

When two skills overlap, compare trigger, decision owner, output, and required tools.

- Same trigger + same output: merge.
- Same trigger + different outputs: create a router or sharpen descriptions.
- Different triggers + shared policy: extract the policy once.
- Tool-specific implementation of a domain action: keep it as an optional specialist,
  with the domain skill choosing when to route to it.
