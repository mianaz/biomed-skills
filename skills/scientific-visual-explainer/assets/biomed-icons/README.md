# Biomed Icons

The default is **basic mode**: generic proteins are capsules; Y/U receptors have matching Y/U dimers. [Three complete mechanism figures and animations](../basic-mechanisms/index.html) demonstrate this vocabulary. The [basic symbol editor](generic-primitives/preview.html) offers 14 current symbols. Detailed domain-bearing illustrations are optional.

Collection v1.0 contains 162 registered assets, including compatibility artwork. The current public gallery has 14 basic symbols and 24 detailed assets. Six older generic alternatives remain registered as archived; current basic scenes use the capsule protein exclusively.

[PI3K–AKT–mTOR icons and contact preview](pi3k-akt-imagegen/preview.html) include eight original PNGs, editable SVGs, exact prompts and four pairwise assembly models.

## Use

Read `catalog.json`; select by entity role rather than by the name of a whole pathway. Each entry points to a standalone, transparent SVG plus named parts, source-space anchors and scientific scope. Place text outside the artwork. Uniformly scale the complete icon or a named part; do not recreate its shape for each scene.

A docking operation aligns compatible contact points and opposing normals. A membrane anchor follows the local membrane position and normal. The optional `context_parts` field identifies static contextual drawing that can be omitted when a scene supplies its own membrane or DNA. These teaching anchors do not assert atomic geometry.

The [offline icon gallery](../biomed-icon-library.html) can be opened directly. Build it with the skill's `scripts/build_icon_atlas.py`; the result is saved as `assets/biomed-icon-library.html`. It contains search, categories, an anchor inspector, SVG downloads, binding/release and membrane-traffic demos. Its traffic demo reuses the existing event/camera kernel with new assets and anchor metadata.

## Extend

1. Inspect a suitable public BioRender example as the sole visual reference. Use scientific literature separately to check biological features. Record both scopes in separate manifest fields.
2. If no suitable icon exists, follow [the built-in imagegen → SVG workflow](../../references/generated-icons.md), or retain source attribution/license when adapting a requested native source.
3. Register parts, anchors, context parts and scope in the matching group manifest.
4. Review it beside the whole family and in an interaction, check SVG structure, manifest paths and visible contacts, then rebuild the gallery/catalog.

Keep a biological distinction only when it helps the explanation. Do not claim a generic receptor is a particular solved structure, a decorative notch is a measured interface, or an illustrative release route applies to every receptor.

## Provenance

Original SVG paths in this family use the parent package MIT license. They are reference-informed schematic drawings, not traced BioArt/Servier assets. Relevant visual references inspected during development include NIH BioArt [430](https://bioart.niaid.nih.gov/bioart/430), [473](https://bioart.niaid.nih.gov/bioart/473), [477](https://bioart.niaid.nih.gov/bioart/477), [481](https://bioart.niaid.nih.gov/bioart/481), and open phospholipid/LDL source files from a development collection that is not distributed with this package. That collection keeps its own Public Domain/CC BY licensing. The v3 TF animation informed the restrained flat composition.

The library contains original diagrams, not experimental measurements. Broad coverage means these thirteen families; it does not imply complete anatomical or molecular coverage.

## v0.2 reference QC and mechanism

The signaling, immune and organelles folders each contain `QC.md` with scientific
references, public BioRender examples, actual visual-versus-text reading scope and
per-icon criteria. Original drawings are not BioRender exports. A TCR–LAT–RAS/ERK
development lesson, not distributed here, used the
new domain icons with `domain-motion.js`, including nested docking, transient
reaction, state change and branch-aware timing. The model remains separate from
the shared operations; rename/reorder and branch-removal checks accompanied it.

## v0.3 reference policy and nuclear transport

All 42 new entries use BioRender-only visual references, smooth continuous contours, reusable parts and named contact anchors. Older source records above remain historical provenance; they are not the design brief for new icons. The STAT1 nuclear-transport HTML reuses domain-motion operations and adds generic waypoint transport, release and product growth. See the `wnt`, `tgfb`, `nfkb` and `jakstat` QC notes.

## Imagegen mechanism-figure pilot

The refresh targets clean biomedical mechanism figures that can animate through the existing shared engine. Use flat, readable symbols; keep contact areas, membrane anchors and assembly space available for binding, recruitment and translocation. A static frame should already be a complete mechanism figure. Motion should explain a biological event.

The mechanism-first development pilot uses three built-in imagegen assets traced into editable SVG. Its development preview switches between the same static figure and a short binding/activation/recruitment sequence, using the existing `domain-motion.js` engine. Original PNGs, prompts, color paths and anchors are retained. This is a generic design trial; the registered catalog remains active.

The earlier 3D scene-sticker experiment is retained as a visual test, not the main library direction.

## EGF–ERK generated family (v0.4)

The [eight-icon family](egfr-imagegen/manifest.json) is registered in the catalog and atlas. It retains [prompts](egfr-imagegen/prompts.json), source PNGs, editable paths, curated anchors and [source/QC notes](egfr-imagegen/QC.md). The [complete mechanism lesson](../egfr-generated.html) uses the existing engine for EGF binding, EGFR dimerization and phosphorylation, GRB2–SOS1 recruitment, RAS exchange and RAF–MEK–ERK reactions. The static figure, animation and kinase-block comparison share the same assets and event model.

## TGFβ–SMAD generated family (v0.5)

The [six-icon family](tgfb-imagegen/manifest.json) adds TGFβ1, TGFβRII, ALK5, SMAD3, SMAD4 and SMAD2. The [58-second lesson](../tgfb-generated.html) follows the SMAD3 branch, reuses DNA/RNA/nuclear-pore icons, and includes ALK5 catalytic-block and SMAD3 C-terminal 2SA comparisons. SMAD2 is available in the library but is not substituted for SMAD3 in this lesson. Paired contours, symmetric duplicate ports and separate P circles work across receptor assembly, substrate contact, heterotrimer formation and nuclear import. Read [QC and scope](tgfb-imagegen/QC.md) before reuse.

## DNA/RNA refresh (v0.6)

[Open the two-icon preview](../nucleic-icons.html) to recolor and download the new SVGs.

Prefer [dna-ig](nucleic-imagegen/dna-ig.svg) and [rna-ig](nucleic-imagegen/rna-ig.svg) for the refreshed mechanism style. They replace the earlier line-only DNA/RNA in the TGFβ lesson. DNA has alternating front/back ribbon crossings and base-pair rungs; RNA has one continuous curved backbone and attached unpaired nucleotide tabs. Both retain generated PNGs, exact prompts, semantic color groups and anchors. Legacy DNA/RNA remain available for existing consumers. See [QC](nucleic-imagegen/QC.md).

## Whole-contour refinement (v0.7)

All 16 generated icons now use complete closed cubic body outlines. Contact arcs blend into the body; there are no contact-patch strokes or cutting clips. Structural outlines use a consistent weight at assembly scale, with lighter internal domain seams. Source PNGs remain intact. See the [before/after contact review](../contour-review.html), and each family’s contour-check.json for body connectivity and geometry.
