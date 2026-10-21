# IFNγ–JAK–STAT icon QC

## Visual design reference

- BioRender is the sole visual design source for this family. The [Type 2 Interferon (IFNγ) pathway](https://www.biorender.com/template/type-2-interferon-ifng-canonical-pathway) guides the pathway assets. For `nuclear-pore-cutaway`, the dedicated [Components of the Nuclear Pore Complex template](https://www.biorender.com/template/components-of-the-nuclear-pore-complex) was inspected: its side cutaway uses two membrane bands and a compact stack of scaffold rings around an open channel. Each SVG is independently drawn; no BioRender paths or shapes were copied.

## Scientific quality checks

- [RCSB 6E3K](https://www.rcsb.org/structure/6E3K) and the associated [open paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6561087/) were used to check the IFNγ dimer and full 2 IFNγ:2 IFNGR1:2 IFNGR2 stoichiometry.
- [RCSB 1BF5](https://www.rcsb.org/structure/1BF5) and Chen et al., *Cell* (1998), were used to check parallel DNA-bound STAT1 and reciprocal phosphotyrosine–SH2 contact.
- The STAT1 importin-α5 studies ([PMC125956](https://pmc.ncbi.nlm.nih.gov/articles/PMC125956/), [PMC2930068](https://pmc.ncbi.nlm.nih.gov/articles/PMC2930068/)) informed the exposed DNA-binding-domain transport surface.
- JAK domain layout was checked against the review at [PMC6396335](https://pmc.ncbi.nlm.nih.gov/articles/PMC6396335/). Importin-β transport context was checked against [PMC2683581](https://pmc.ncbi.nlm.nih.gov/articles/PMC2683581/).
- Nuclear-pore channel layout and membrane continuity were checked against [Structure and Function of the Nuclear Pore Complex](https://pmc.ncbi.nlm.nih.gov/articles/PMC9732903/).

These papers and structures were consulted only for biological accuracy, not visual design. All 13 symbols are original editable SVG schematics under the package MIT license. Anchors encode teaching-scale contacts rather than atomic interfaces. STAT1’s `dimer-interface` marks the reciprocal pY–SH2 region; its DNA and importin anchors identify schematic contact surfaces. The pore channel has a 44-unit open width with membrane-midplane and channel-wall anchors.

All SVGs were rendered at 256 × 256 px with the biomedical-manim CairoSVG environment and reviewed visually in [contact-sheet.png](contact-sheet.png). Review checked continuous silhouette, IFNγ subunit contact, receptor and kinase domains, exposed STAT importin surface, opposing GAS strands and motif, polymerase cleft, and the pore’s stacked scaffold rings, membrane bands and open channel. Pol II’s embedded duplex is contextual and can be omitted when the scene supplies promoter DNA.
