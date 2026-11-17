# Basic mechanism figures and animations

This is the default rendering mode. First inspect a relevant BioRender public example and a published mechanism figure when available, using local PDFs and curated galleries as useful sources. Use the [basic examples](../assets/basic-mechanisms/index.html) as editable composition references.

## Palette

Use **Nord mist** for the default basic library, mechanism figures and animations. Read the semantic roles in [palettes.json](../assets/basic-mechanisms/palettes.json); keep protein, ligand/P, membrane and nucleic-acid roles consistent. Add colors only when the user requests a new distinction. Alternative color collections remain reference material. `review-slate` and
`template-sage` are candidates sampled from inspected Nature Reviews figures and
BioRender previews, then assigned to the shared semantic roles. They are project
adaptations, not official publisher or vendor palettes. Keep Nord as the default;
use a candidate when the user selects it. Preserve source colors in fidelity
comparisons and compare candidate colors on the same geometry before adoption.

## Symbol grammar

- Every generic protein uses `generic-protein-capsule`. Name it with a separate SVG text element. Keep the capsule silhouette stable across states; color and P badges express the requested state.
- Receptors use `generic-receptor-y` or `generic-receptor-cup`. Their dimers use `generic-receptor-dimer-y` and `generic-receptor-dimer-u`, with two independently named receptor parts. Use the same monomer glyph during approach and in the final dimer.
- Protein complexes use adjacent capsule instances. A complex does not become an irregular protein blob.
- Keep ligand shapes simple, and use the existing matched triangle/Y and circle/U conventions.
- Choose RNA notation by topology. A wave or one-sided comb is single-stranded; a ladder is paired; a hairpin has one continuous looped backbone. Keep direction labels separate.
- Put membrane receptors through the membrane midplane. Nuclear import passes through a visible gap. Place phospho badges with their protein during movement.
- Separate activation arrows, inhibition T-bars and transport arrows in the figure key. A basic pathway arrow is a relation, not a requirement to model molecular surface docking.

Use the [38-symbol editor](../assets/biomed-icons/generic-primitives/preview.html) and [three generic assemblies](../assets/biomed-icons/generic-primitives/compositions.html) for chromatin/expression, protein turnover and membrane traffic. Use functional structure symbols for ribosomes, proteasomes and organelles; generic protein nodes remain capsules. Each icon has named parts and anchors.

## Deliver a mechanism

1. Save a compact node/event model and storyboard. Use source-based relationships for real pathways; label hypothetical teaching models once.
2. Compose the full static figure with readable labels, compartments and a complete causal or transport route. Show intermediate states when necessary, and identify repeated entities as sequential states.
3. When animation is requested, animate the same figure: ligand binding, receptor association, state changes, complex formation, transport or RNA output. Provide pause, replay and seeking. Keep the complete-figure view one click away.
4. Inspect the static figure at final placement; for animation, also inspect beginning/middle/end states and condition changes. Keep interactive views readable on narrow screens. Follow the SKILL deliverable route for requested formats and retain the reusable source model.

Detailed molecular silhouettes and image generation are optional when the user requests structural detail. They do not replace this default symbolic mode.
