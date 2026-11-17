# Biomedical icon library

Basic mode uses capsule proteins and Y/U receptors with matching dimers. Open the
[basic mechanism examples](../basic-mechanisms/index.html),
[basic symbol editor](generic-primitives/preview.html), or
[offline icon gallery](../biomed-icon-library.html).

Search `scripts/icon_library.py QUERY` from the skill directory. The portable
`catalog.json` supplies asset keys, editable SVG paths, named parts, anchors and
scientific scope. Optional private overlays stay in their own library; see
[icon search and layout](../../references/unified-library.md).

Select by biological role, compartment and state. Keep names editable; size a
capsule to its name. Uniformly scale the whole icon or a named part. Dock compatible
contact anchors and align membrane anchors to the membrane. Omit `context_parts`
when the scene supplies that membrane or DNA.

Detailed families include [EGFR](egfr-imagegen/usage.md),
[TGFβ–SMAD](tgfb-imagegen/usage.md) and [DNA/RNA](nucleic-imagegen/usage.md).
Use their scientific scope and source links when adapting a mechanism. The
[generic references](generic-primitives/references.json) credit visual and
scientific sources; original SVG geometry is covered by the package MIT license.

Register new assets in the matching manifest, then check the rendered figure and
rebuild the portable catalog with `scripts/build_icon_atlas.py`. For generated
artwork, use the [image-to-SVG workflow](../../references/generated-icons.md).
Keep private source images, reading notes and development logs outside releases.
