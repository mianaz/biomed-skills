# Unified icon library

Run `python3 scripts/icon_library.py "mouse"` from this skill directory. Add
`--json` to retrieve files, source coordinates, anchors and states. Archived
alternatives are hidden unless `--include-archived` is set.

The loader combines the portable `assets/biomed-icons/catalog.json` with an
optional private `assets/biomed-icons/local-registry.json`. Keep private artwork,
source images and generation records in the user's existing library. Preserve
its asset keys and provenance when reusing an icon. A palette changes fills on
the same geometry; a distinct view or anatomical state uses its own asset key.

For a reproducible layout, pass a scene JSON to `scripts/layout_icons.py`:
`assets` is a list of `{key, label}`, `kind` is `workflow`, `matrix` or
`comparison`, and `columns` controls matrices. Save with `--out figure.svg`.
The companion `.layout.json` records positions, measured asset bounds and label
size. The renderer preserves aspect ratios and namespaces SVG IDs.

Preserve accepted artwork and source rights. Review a new adaptation before
replacing an existing asset. Keep the portable catalog and private overlays
separate when distributing the skill.
