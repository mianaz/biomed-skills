# Signaling icon QC

Reviewed 2026-10-13. All 16 icons are original, flat-vector educational schematics using the shared palette and MIT license. They show recognizable domain topology and interaction surfaces, not atomic structures or molecular scale.

## Sources and visual scope

| Source | Inspection | Use |
|---|---|---|
| [BioRender: T-cell signaling](https://www.biorender.com/template/t-cell-signaling) | Opened the public page and visually inspected its preview screenshot. The overall T-cell/APC scene and pathway layout were readable; individual molecule details were too small to inspect. No BioRender geometry was traced or included. | Broad scene context only. |
| [Su et al., Science 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4892427/) | Reviewed searchable paper text and figure descriptions. | LAT–Grb2–SOS clustering and TCR pathway context. |
| [T-cell signaling review](https://pmc.ncbi.nlm.nih.gov/articles/PMC5801066/) | Reviewed searchable article text. | TCR/CD3, coreceptors, proximal kinase and adaptor topology. |
| [TCR signaling review](https://pmc.ncbi.nlm.nih.gov/articles/PMC2857167/) | Reviewed searchable article text. | TCR/CD3 ITAMs and proximal signaling context. |
| [PLCγ1 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC2740335/) | Reviewed searchable article text. | PLCγ1 regulatory and catalytic domain architecture. |
| [Ras signaling review](https://pmc.ncbi.nlm.nih.gov/articles/PMC102173/) | Reviewed searchable article text. | Ras membrane association and effector-facing switch surface. |

## Structure checks

| Icon | Visible feature checked |
|---|---|
| TCR–CD3 | Paired αβ variable and constant ectodomains above membrane-spanning chains; CD3 ITAM tails extend cytosolically. |
| Peptide–MHC II | Two-chain peptide groove faces up; paired Ig-like domains, membrane helices, and tails face down. Rotate 180° for an APC-facing scene. |
| CD4 | Four serial Ig-like domains, one transmembrane helix, and cytosolic tail. |
| Lck | Separate membrane tether; SH3, SH2, linker, two kinase lobes, and activation loop. |
| ZAP70 | Tandem SH2 domains, interdomain regions, bilobed kinase domain, and activation loop. |
| LAT | Membrane-spanning N terminus and long intracellular scaffold with separated phosphotyrosine sites. |
| Grb2 | SH3–SH2–SH3 arrangement. |
| SOS | Large multidomain GEF body with distinct Ras-facing surface and Grb2-binding tail. |
| Ras | Compact GTPase with nucleotide pocket, switch/interface surfaces, and membrane anchor. |
| Raf | Ras-binding region and separate kinase domain. |
| MEK | Bilobed kinase and activation-loop feature. |
| ERK | Bilobed kinase, docking surface, and activation loop. |
| PLCγ1 | Connected PH, EF-hand, C2, catalytic X/Y, tandem SH2, and SH3 domains; narrow linkers connect peripheral domains to the core. |
| PIP₂ | Inositol head group with two phosphates and two membrane tails. |
| IP₃ | Inositol ring with three phosphate groups. |
| DAG | Glycerol head group with two membrane tails. |

## Render and anchor checks

- Parsed all 16 SVGs and rendered each with the project prototype CairoSVG environment. Reviewed the contact sheet at `signaling/contact-sheet.png`.
- SVGs use the shared 160 × 160 viewBox, shared palette, named `data-part` groups, and no embedded labels or external assets. Manifest records match each SVG's part groups and declare the signaling category, scope, provenance, and source URLs.
- Each anchor has a two-coordinate point and a unit outward normal. Binding and enzyme surfaces are schematic contact cues; the membrane anchors identify the membrane midplane. Context membranes are listed in `context_parts` for omission when needed.
- Rasterized artwork remains within x/y = 12–148, including strokes. The SVGs contain no raster images, filters, scripts, gradients, or external references.
