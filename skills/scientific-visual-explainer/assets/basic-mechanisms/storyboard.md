# Basic-mode examples

Audience: readers learning to build simple biomedical mechanism figures and animations.
Goal: demonstrate one capsule protein vocabulary and distinct Y/U receptor monomers/dimers in complete figures.

These are authored teaching models with named causal rules, not experiments or named natural pathways. BioRender public previews were visually inspected for symbol grammar and composition; no artwork was copied. Reading scope is recorded in models.json.

| Example | Figure route | Animated sequence | Block-A comparison |
|---|---|---|---|
| Y cascade | Ligand → Y dimer → A → B → C | ligand approach, receptor association, separate receptor and protein P badges | receptor P persists; A/B/C P absent |
| U import | Ligand → U dimer → A/B → complex → nuclear gap → gene/RNA | association, A/B P, capsule-complex formation, nuclear import with P badges, RNA output | B P persists; A P, complex import and RNA absent |
| Y/U convergence | two receptor dimers → A/B → common C | parallel input routes and convergent C P | B keeps C P through the OR rule |

Generic proteins share the capsule silhouette. Repeated A/B icons in the import figure depict different sequential states. In animation the moving complex is accompanied by a faded intermediate state. The gap is sized for both capsules and their badges. The static view retains the full relation map; arrows indicate relations or transport as described in the figure key.

All three views share models.json, player.js and native generic-primitives SVG assets. Run build.py to embed them into index.html. Current-frame exports keep symbols, labels, arrows and P circles as independent SVG elements.
