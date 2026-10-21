# Biomed Icons · flat vector family v0.7

Editable educational schematics. From v0.3 onward, BioRender is the single visual reference standard; scientific papers check biology separately. Earlier entries retain their original provenance. Reuse or adapt suitable openly licensed vectors when possible, retaining their license and attribution. For original drawings, study reference silhouettes and domain proportions before defining smooth curves. Existing source artwork remains separately credited. Original paths follow the package MIT license; they do not claim resolved molecular geometry.

## Shared drawing contract

- Every file is standalone SVG: `viewBox="0 0 160 160"`, width/height160, transparent background. Artwork normally stays inside [12,148] on both axes (stroke included). Registered mating tabs may use the outer margin while keeping at least 4 units of transparent padding.
- Rounded organic contours; flat fills; consistent outline #3D5963 (generated refinements: 1.6 drawing units at consuming scale; legacy artwork: about 2.5 source units), round joins/caps. Fine internal marks use the same stroke, 1.1 drawing units in generated refinements. Broad colored strokes may represent strands, ribbons or tubular bodies; their width is anatomy, not outline weight. No gradients, shadows, raster images, text, labels, external references, scripts, SVG filters or raster masks. A local body clip may contain semantic colors. Mating contours belong to the complete closed body; do not paste independently stroked contact patches. Keep all clip IDs unique when instancing an icon.
- Palette: protein #69ADB5; cofactor/cargo #E4BE78; membrane/cytoplasm #B3D7CC; nucleic acid #B2A6CD; cell/organelle interior #EDF5F1; detail #D7E8EC; outline #3D5963; optional active state #D98E83. White #FFFFFF is allowed for negative-space channels.
- Shape must communicate the entity: domain-bearing proteins, connected nucleic strands, membrane topology, or recognizable organelle architecture. Do not give every molecule the same bean shape. Keep at most 2–3 colors per icon, and avoid tiny ornament.
- Separate logical parts into named `<g id="ICONID-part" data-part="part">` groups for later reuse. Keep labels outside the artwork in the consuming scene.
- Docking anchors lie on the visible contact contour. A binding patch must be reachable without passing through the entire body. A membrane anchor marks the membrane midplane; surface normal points toward the ectodomain. These are teaching anchors, not atomic contact sites. For fitted contacts, store the shared profile and partner scale in `interfaces.json`; move the anchor onto the fitted contour.

## Per-group metadata

Write `manifest.json` as an array with one object per SVG:
`{"id":"single-pass-receptor","label":"Single-pass receptor","label_zh":"单跨膜受体","file":"membranes/single-pass-receptor.svg","category":"membranes","description":"...","parts":["body","binding-domain","tail"],"anchors":{"binding":{"point":[80,25],"normal":[0,-1],"kind":"binding"},"membrane":{"point":[80,105],"normal":[0,-1],"kind":"membrane"}},"scope":"Generic schematic, not a named molecular structure.","provenance":{"mode":"original-vector","references":["https://bioart.niaid.nih.gov/","https://bioicons.com/"],"license":"MIT"}}`

Use English names and short Chinese labels. Each entity has at least one meaningful anchor. Use biologically conventional forms as reference. Keep proprietary reference art separate from redistributable source vectors; a BioRender example does not by itself grant an open license. Shared anchors and compatible shapes matter more than decorative detail. Main integration combines group manifests; workers do not edit the root catalog.

## Finish and visual QC

Prefer a small number of smooth, deliberate curves over many small segments. Remove decorative C-shaped highlights and uneven scribbles. Domain seams must clarify architecture. Avoid disconnected beads for a single multidomain protein. Inspect at 64, 96 and 160 pixels beside the reference; check silhouette, contour joins, spacing and domain continuity. Passing bounds/palette checks is not sufficient for visual acceptance.

## Generated mechanism extensions

Keep the flat mechanism-figure language above when extending the library with built-in image generation. Convert accepted images to true editable SVG paths, preserve source PNGs and prompts, and curate palette roles, contact anchors and membrane guides. Follow [generated-icons.md](../../references/generated-icons.md). A static figure should communicate the mechanism; animation adds the supported sequence and state changes. Color-traced parts need manual refinement before independent domain motion.
