# NF-κB icon family QC

## References and scope

- **Visual design reference:** [BioRender TNF Pathway template](https://www.biorender.com/template/tnf-pathway). I inspected its public preview for overall scientific-illustration style and component grouping. It is a visual reference only; no BioRender artwork or paths were copied or traced.
- **Scientific check:** Ting AT, Bertrand MJ. [More to life than NF-κB in TNFR1 signaling](https://pmc.ncbi.nlm.nih.gov/articles/PMC5076853/). *Trends Immunol.* 2016;37(8):535–545. I visually inspected Figure 1 around the TNFR1 complex-I and canonical NF-κB branches and read the corresponding review text on receptor recruitment, RIPK1 ubiquitylation, TAK1/IKK activation, IκBα degradation, and p50/p65 translocation. This review is the pathway check, not a visual style source.

All 11 SVGs are original editable teaching schematics released under the package MIT license. The scientific reference checks pathway identity and domain order; it does not establish atomic geometry. No third-party icon vectors were adapted.

## Per-icon inspection

| Icon | Distinguishing structure checked | Scope retained in the manifest |
|---|---|---|
| TNF trimer | Three joined ligand subunits | Trimer and receptor-facing interface are schematic. |
| TNFR1 | Four extracellular cysteine-rich modules, membrane helix, cytosolic linker and death domain | Domain shapes are simplified; cytosolic continuity is explicit. |
| TRADD | N-terminal TRAF-interacting region, linker and C-terminal death domain | Domain order is shown; no atomic fold is implied. |
| RIPK1 | Kinase domain, continuous intermediate region and death domain | Ubiquitin chain is a TNFR1-signaling context cue, not a constitutive RIPK1 state. |
| TRAF2 | RING region, three-chain coiled-coil and three TRAF domains | Subunit interfaces are illustrative. |
| TAK1 | Bilobal kinase, activation loop and C-terminal regulatory region | Domain geometry is illustrative. |
| IKK complex | IKKα/IKKβ kinase pair attached to a shared NEMO scaffold | Component diagram only; it does not encode exact stoichiometry or resolved geometry. |
| IκBα | Six ankyrin-repeat units, N-terminal phosphodegron and PEST tail | Repeat curvature and degron positions are schematic. |
| RELA / p65 | Joined two-lobe Rel homology domain, DNA-contact loops and C-terminal tail | Rel domain is simplified; the transactivation region is flexible/disordered. |
| NFKB1 / p50 | Joined two-lobe Rel homology domain and DNA-contact loops | Mature p50 only; p105 processing is outside the icon. |
| 26S proteasome | 19S caps, 20S core barrel and axial channel | Architecture is schematic; subunit geometry and stoichiometry are simplified. |

## Render checks

`build_icons.py` writes each SVG, `manifest.json`, and `contact-sheet.png`. I rendered every icon at 64, 96, and 160 px and inspected the three sheets. The reviewed silhouettes have no decorative C-shaped highlight strokes; connected domains meet visibly, including the TNFR1 cytosolic linker, RIPK1 backbone, and p65/p50 lobe junctions. The IKK icon reads as two kinase units over one NEMO scaffold. Manifest part IDs match SVG groups, and rendered artwork stays within the shared 12–148 px bounds at 160 px. Anchors were placed on visible contact contours and topology guides.
