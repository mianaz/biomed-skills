# Basic mechanism figures and animations

This is the default rendering mode. First inspect a relevant BioRender public example for visual grammar. Use the [basic examples](../assets/basic-mechanisms/index.html) as editable composition references.

## Symbol grammar

- Every generic protein uses `generic-protein-capsule`. Name it with a separate SVG text element. Keep the capsule silhouette stable across states; color and P badges express the requested state.
- Receptors use `generic-receptor-y` or `generic-receptor-cup`. Their dimers use `generic-receptor-dimer-y` and `generic-receptor-dimer-u`, with two independently named receptor parts. Use the same monomer glyph during approach and in the final dimer.
- Protein complexes use adjacent capsule instances. A complex does not become an irregular protein blob.
- Keep ligand shapes simple, and use the existing matched triangle/Y and circle/U conventions.
- Choose RNA notation by topology. A wave or one-sided comb is single-stranded; a ladder is paired; a hairpin has one continuous looped backbone. Keep direction labels separate.
- Put membrane receptors through the membrane midplane. Nuclear import passes through a visible gap. Place phospho badges with their protein during movement.
- Separate activation arrows, inhibition T-bars and transport arrows in the figure key. A basic pathway arrow is a relation, not a requirement to model molecular surface docking.

## Deliver a mechanism

1. Save a compact node/event model and storyboard. Use source-based relationships for real pathways; label hypothetical teaching models once.
2. Compose the full static figure with readable labels, compartments and a complete causal or transport route. Show intermediate states when necessary, and identify repeated entities as sequential states.
3. Animate the same figure: ligand binding, receptor association, state changes, complex formation, transport or RNA output. Provide pause, replay and seeking. Keep the complete-figure view one click away.
4. Inspect the figure and beginning/middle/end of every animation and condition. Keep the rendered figure readable on narrow screens through internal pan or zoom. Export the current frame as editable SVG and retain the offline HTML and source model.

Detailed molecular silhouettes and image generation are optional when the user requests structural detail. They do not replace this default symbolic mode.
