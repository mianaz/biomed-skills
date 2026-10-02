# Identity ledger

Maintain one small, versioned table for names that recur across objects and outputs.
The ledger prevents semantically identical labels from fragmenting analyses and
prevents provisional labels from silently becoming facts.

## Recommended fields

For cell labels, keep:

- `canonical_label`, `parent_label`, and accepted aliases;
- `label_kind`: identity, state, program, cluster, or technical flag;
- species and tissue scope;
- `status`: provisional, verified, mixed, unknown, or deprecated;
- supporting and contradictory evidence; and
- the annotation version in which the label became active.

Keep companion mappings for sample aliases, donor IDs, conditions, batch variables,
gene symbols and stable IDs, and metric names when those differ across inputs.

## Apply a vocabulary change

1. Add the new canonical label and its mapping; never delete the previous spelling
   from history.
2. Check whether the change merges, splits, or merely renames categories. A split
   requires new cell-level evidence, not a text substitution.
3. Update the canonical object by cell ID.
4. Sweep all consumers: derived objects, contrasts, tables, source data, plot labels,
   filenames, and narrative claims.
5. Re-run affected tests when a merge or split changes group membership.
6. Verify factor order and name-bound color mappings after the sweep.

Do not invent a fine label to fill a vocabulary gap. Use a parent label, `unknown`,
or a clearly marked provisional label until `annotate-single-cell-types` verifies it.
