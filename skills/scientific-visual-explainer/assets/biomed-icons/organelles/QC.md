# Organelle icon QC

These 12 standalone SVGs are original teaching schematics. Scientific sources informed the structural cues; no BioRender paths or images were traced, copied, or embedded. Exa was unavailable, so web research used the agent-reach fallback route.

## Public BioRender examples

| Exact URL | Review scope | Use in this set |
|---|---|---|
| https://www.biorender.com/template/intracellular-transport | Opened in Chrome. Viewed the template image and read the page description. The image shows ER, Golgi, early and late endosomes, lysosome, and trafficking vesicles. | Compared the overall flat schematic style and relative visual simplicity. It did not set organelle-specific biological claims. |
| https://www.biorender.com/template/endocytosis-in-vertical-cell-layout | Opened in Chrome. Viewed the template image and read its page description. It shows particles entering a cell and a simplified cell outline. | Checked how little context is needed around a small membrane-traffic schematic. |
| https://www.biorender.com/icon/membrane-endocytic-pathway-early-endosome | Opened in Chrome. Visually inspected the public early-endosome membrane preview and read the page text. | Compared the minimal silhouette with the richer sorting/tubulation cues here. No source asset was downloaded or reused. |

## Scientific sources and reading scope

Text was checked in search-indexed chapter excerpts, abstracts, and article excerpts. The full selected text sections of the recycling-endosome and nuclear-pore reviews were also opened and read. Some NCBI Bookshelf and PMC pages returned a browser gate, so this QC does not claim full-text review of those pages.

| Exact URL | Reading scope | Cues applied |
|---|---|---|
| https://www.ncbi.nlm.nih.gov/books/NBK9889/ | Search-indexed chapter excerpt, text | ER as a connected network of tubules and cisternae; rough ER has cytosolic ribosomes and smooth ER lacks them. |
| https://www.ncbi.nlm.nih.gov/books/NBK26841/ | Search-indexed chapter excerpt, text | Ribosomes face the cytosol; the ER lumen lies inside the membrane-bounded cisternae. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC4060825/ | Search-indexed review excerpt, text | Peroxisomes have one limiting membrane and a variable matrix; crystalline cores occur only in some cases. The icon omits a core. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC7264243/ | Search-indexed review abstract and excerpt, text | Autophagosomes enclose cargo with a double membrane; fusion and degradation yield autolysosomes with one limiting membrane. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC1363699/ | Search-indexed review excerpt, text | The autophagosome outer membrane fuses with a lysosome; inner membrane and contents are degraded. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC5494474/ | Search-indexed definitions excerpt, text | Autolysosomes are single-membraned fusion products containing autophagic cargo. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC2810677/ | Search-indexed review excerpt, text | Early endosomes are pleomorphic sorting compartments with vacuolar and tubular domains. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC4176003/ | Search-indexed review excerpt, text | Sorting-endosome vacuoles and recycling tubules are useful schematic cues; endosomal forms vary by cell and assay. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC4529760/ | Opened review text, selected lines 78–117 | Recycling membranes are dynamic and morphologically diverse, with tubulation and vesicular forms. The icon is explicitly schematic, not diagnostic. |
| https://www.ncbi.nlm.nih.gov/books/NBK9932/ | Search-indexed chapter excerpt, text | Most animal-cell centrosomes contain perpendicular centrioles in pericentriolar material. |
| https://www.ncbi.nlm.nih.gov/books/NBK26862/ | Search-indexed chapter excerpt, text | Microtubules are hollow tubulin cylinders; actin filaments consist of two twisting protofilaments. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC9732903/ | Opened review text, selected lines 110–170 and abstract | The pore is an annular scaffold with a central channel embedded in the double nuclear envelope. |
| https://www.ncbi.nlm.nih.gov/books/NBK9927/ | Search-indexed chapter excerpt, text | Nuclear pores are regulated channels in the nuclear envelope. |
| https://www.ncbi.nlm.nih.gov/books/NBK9939/ | Search-indexed chapter excerpt, text | The nucleolus supports rRNA transcription and processing and ribosome assembly. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC4447046/ | Search-indexed review excerpt, text | Mammalian nucleoli can show fibrillar-center, dense-fibrillar, and granular subphases. |

## Per-icon structure and anchor QC

Each anchor has a unit outward normal and lies on the depicted contact contour or membrane midplane. Coordinates use the 160 × 160 SVG viewBox.

| Icon | Structure checked | Anchor | Scope note |
|---|---|---|---|
| rough-er | Three flattened cisternae connect through narrow necks; ribosomes sit on the cytosolic faces. | Membrane [80, 25], normal [0, -1] | Generic rough ER. |
| smooth-er | A branching, connected tubular network with lumen hints and no ribosomes. | Membrane [25, 51], normal [-0.707107, -0.707107] | Tubule pattern is schematic. |
| peroxisome | One limiting membrane encloses a nonuniform granular matrix; no universal crystal core. | Membrane [135, 80], normal [1, 0] | Matrix composition varies. |
| autophagosome | Two separate membrane bands enclose a visible pale intermembrane space and cytoplasmic cargo. | Membrane [141, 80], normal [1, 0] | Generic closed macroautophagosome. |
| autolysosome | One limiting membrane encloses fragmented, degrading cargo. | Membrane [142, 80], normal [1, 0] | Cargo detail is schematic. |
| early-endosome | A vacuolar sorting body has four connected tubular cues and lumenal cargo. | Membrane [127, 80], normal [1, 0] | The silhouette is not diagnostic morphology. |
| recycling-endosome | A connected tubulovesicular network includes small cargo vesicles. | Membrane [140, 63], normal [1, 0] | The silhouette is not diagnostic morphology. |
| centrosome | Two perpendicular centriole cylinders sit within pericentriolar material. | Nucleation [124, 80], normal [1, 0] | Generic animal-cell example. |
| microtubule | A short hollow cylinder has open lumen ends and simplified longitudinal protofilament marks. | Plus end [139, 80], normal [1, 0] | Internal detail is not to scale. |
| actin-filament | Two helical strands of actin subunits form one filament. | Plus end [66, 25.5], normal [0, -1] | Subunit spacing is not to scale. |
| nuclear-pore | An annular scaffold and central channel sit in a removable envelope-context group. | Membrane [80, 38], normal [0, -1] | Generic scaffold schematic, not a molecular reconstruction. |
| nucleolus | Irregular condensate edge surrounds schematic subphases; the outline denotes a condensate boundary, not a lipid bilayer. | Binding [42, 80], normal [-1, 0] | The surrounding nucleus is removable context, listed in context_parts. |

## Render and structural checks

- Rendered all 12 SVGs with the prototype CairoSVG environment and reviewed the contact sheet at organelles/contact-sheet.png.
- Rasterized artwork bounds span x = 13.0–146.75 and y = 18.0–145.75, within the required 12–148 range including strokes.
- Checked all SVG roots for the shared 160 × 160 viewBox and palette, named part groups, and one manifest record per icon. Anchor normals have length 1 within 0.00001.
- Confirmed the SVGs contain no text, raster images, external references, filters, scripts, clipping masks, or gradients.
- The envelope context for nuclear-pore and nucleus context for nucleolus are marked removable in both SVG group metadata and manifest context_parts.
