# Immune icon morphology QC

Reviewed 2026-10-13. These are original educational vector schematics in the shared icon palette. Scientific sources informed the anatomy. Public BioRender previews were inspected for broad visual conventions only; no proprietary paths, silhouettes, or artwork were traced or included.

## Sources and inspection

| Source | Inspection | Use |
|---|---|---|
| [ASH Image Bank: Normal Blood Smear](https://imagebank.hematology.org/collection/64070) | Visually inspected in the browser, including the microscopy image and cell callouts. | Compared neutrophil segmentation, basophil granularity, and monocyte appearance. |
| [ASH Image Bank: Eosinophil](https://imagebank.hematology.org/image/60933/eosinophil?type=atlas) | Visually inspected in the browser, including the microscopy image and description. | Compared the bilobed nucleus and coarse orange granules. |
| [BioRender: Adaptive Immunity](https://www.biorender.com/template/adaptive-immunity) | Visually inspected in the browser. | Reviewed cell scale and the broad depiction of dendritic, B, plasma, and T cells in a flat explanatory scene. |
| [BioRender: Dendritic cell icon](https://www.biorender.com/icon/dendritic-cell-1-01) | Visually inspected in the browser; the preview is watermarked. | Reviewed branching-process readability and flat icon styling. |
| [NCBI Bookshelf: Histology, White Blood Cell](https://www.ncbi.nlm.nih.gov/books/NBK563148/) | Text-only review. | Lymphocyte, monocyte, and granulocyte morphology; lineage and marker context. |
| [NCBI Bookshelf: Histology, Plasma Cells](https://www.ncbi.nlm.nih.gov/books/NBK556082/) | Text-only review. | Eccentric round nucleus, cartwheel chromatin, abundant cytoplasm, and perinuclear Golgi clearing. |
| [NCBI Bookshelf: Histology, Natural Killer Cells](https://www.ncbi.nlm.nih.gov/books/NBK565844/) | Text-only review. | Large granular lymphocyte appearance. |
| [NCBI Bookshelf: T Cells and MHC Proteins](https://ncbi.nlm.nih.gov/books/NBK26926/) | Text-only review. | Dendritic-cell processes and antigen-presenting cell context. |
| [NCBI Bookshelf: Histology, Mast Cells](https://www.ncbi.nlm.nih.gov/books/NBK499904/) | Text-only review. | Central mononuclear nucleus and dense granulated cytoplasm. |
| [PMC: IgE, Mast Cells, Basophils, and Eosinophils](https://pmc.ncbi.nlm.nih.gov/articles/PMC2847274/) | Text-only review. | Eosinophil bilobation and granule convention. |
| [PMC: Foxp3 and regulatory T-cell identification](https://pmc.ncbi.nlm.nih.gov/articles/PMC2862733/) | Text-only review. | Treg identity depends on marker combinations; no single surface marker is uniquely diagnostic. |

## Per-icon checks

| Icon | Morphology checked | Result and scope |
|---|---|---|
| T cell | Large round nucleus and scant cytoplasm, following the general lymphocyte form. | One surface receptor symbol is a schematic lineage cue. T-cell identity is not claimed from naked morphology. |
| B cell | Large round nucleus and scant cytoplasm, following the general lymphocyte form. | Paired receptor symbols cue B-cell context; they are not diagnostic morphology. |
| Plasma cell | Eccentric round nucleus, spoke-like chromatin, abundant cytoplasm, and adjacent pale Golgi hof. | Present as a simplified mature plasma-cell schematic. |
| NK cell | Expanded cytoplasm, round nucleus, and cytotoxic granules. | Large granular lymphocyte convention is shown without implying activation or target engagement. |
| Dendritic cell | Central body and long branching processes. | Generic dendritic-cell schematic; no specific subtype is implied. |
| Macrophage | Broad irregular phagocyte body, folded nucleus, and a cargo-containing phagosome. | Tissue geometry and phagosome are schematic; no named macrophage state or pathogen is implied. |
| Monocyte | Abundant cytoplasm, kidney-shaped nucleus, and sparse vacuoles. | Generic circulating monocyte; cell and nuclear contours are simplified. |
| Neutrophil | Four separate rounded nuclear lobes, connected by narrow chromatin bridges, with fine cytoplasmic granules. | Segmentation and fine granules are simplified. |
| Eosinophil | Bilobed nucleus and coarse eosinophilic granules. | Granule color follows the staining convention and does not encode molecular composition. |
| Basophil | S-shaped nucleus partly obscured by coarse basophilic granules. | Granules are schematic and partially cover the nucleus. |
| Mast cell | Central mononuclear nucleus and dense metachromatic granules. | Generic intact tissue mast cell; subtype, location, and activation state are unspecified. |
| Regulatory T cell | Same lymphocyte body and nucleus as the T-cell icon, with repeated surface-marker symbols. | The surface symbols are schematic marker cues. Treg identity is not implied by naked morphology or by one marker. |

The contact sheet was rendered from the SVGs with CairoSVG and reviewed after the neutrophil segmentation refinement. The anchor coordinates are on the visible cell or process contour, with outward unit normals and `cell-contact` kind.
