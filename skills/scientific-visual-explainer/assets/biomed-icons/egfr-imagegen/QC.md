# Generated EGFR family · source and visual review

Eight original built-in imagegen outputs extend the flat icon library. Source PNGs, exact prompts, the EGFR correction prompt, fixed-palette tracing inputs and source-pixel specifications are retained. Each SVG has editable paths, palette-assisted named groups and normalized contact/membrane anchors. No raster or proprietary source paths are embedded.

## Biology and interfaces

| Icon | Feature checked | Primary source |
|---|---|---|
| EGF / EGFR | Selected 2:2 ligand-bound ectodomain complex; ligand between domains I and III, domain-II dimerization arm; single transmembrane region, cytoplasmic kinase and tail | [Ogiso et al., Cell 2002](https://pubmed.ncbi.nlm.nih.gov/12297050/), [Zhang et al., Cell 2006](https://pubmed.ncbi.nlm.nih.gov/16777603/) |
| GRB2 | One SH2 and two SH3 domains; receptor-pY and proline-rich SOS contacts | [Li et al., Nature 1993](https://pubmed.ncbi.nlm.nih.gov/8479541/), [Rozakis-Adcock et al., Nature 1993](https://pubmed.ncbi.nlm.nih.gov/8479540/) |
| SOS1 | Separate exchange-factor and proline-rich functions; nucleotide release/rebinding | [Boriack-Sjodin et al., Nature 1998](https://www.nature.com/articles/28548) |
| RAS | Membrane localization, GDP/GTP state and GTP-dependent RAF contact | [Warne et al., Nature 1993](https://pubmed.ncbi.nlm.nih.gov/8332195/) |
| RAF1 | RAS-binding/regulatory region and kinase region; activation separate from recruitment | [Warne et al., Nature 1993](https://pubmed.ncbi.nlm.nih.gov/8332195/), [Rajakulendran et al., Nature 2009](https://pubmed.ncbi.nlm.nih.gov/19727074/) |
| MEK / ERK | Kinase architecture; RAF→MEK→ERK phosphorylation relay | [Kyriakis et al., Nature 1992](https://pubmed.ncbi.nlm.nih.gov/1322500/), [Crews et al., Science 1992](https://pubmed.ncbi.nlm.nih.gov/1411546/), [Crews et al., PNAS 1992](https://pubmed.ncbi.nlm.nih.gov/1381507/) |

Reading scope: primary abstracts/records and the EGFR author-PDF summary, rather than complete experimental figure audits. The [public BioRender MAPK/ERK preview](https://www.biorender.com/template/simplified-mapkerk-signalling) was visually inspected for compartments, external labels and cascade layout. Its artwork was not traced or embedded. The generated EGFR initially placed the protruding arm on domain III; the built-in image editor moved it to domain II before tracing.

## Rendering and motion

The SVGs pass the shared family checks for 160 × 160 canvas, family palette, named groups, unit normals, alpha bounds and absence of embedded raster. Source/vector comparisons and 64, 96 and 160 px renders are in the full mechanism preview's QA folder. Contact points were selected on the generated contours and snapped to the source alpha edge; membrane anchors remain interior guide points.

The worked lesson reuses `domain-motion.js`. GRB2–SOS1 begins as a linked complex. The RAS exchange contact is calibrated to the recruited SOS1 position while preserving the RAS inner-membrane anchor. RAF recruitment precedes a separate aggregate activation step. Transient MEK/ERK reactions release the substrate while retaining its activated state. Static and animated modes share the same assets and model.

The small RAS anchor is a lipid-attachment symbol, not an isoform-specific chemical diagram. Contacts, domain spacing and proportions are illustrative. The complete figure shows the selected canonical core; atomic EGFR kinase asymmetry, RAF dimer/regulatory complexes, SHC, phosphatases and feedback are not expanded. Named color groups preserve paint order and a shared outline; independent domain motion may require further part refinement.

## Paired contour and state update

The eight interface types in `interfaces.json` use a shared contact curve at the recorded counterpart scales. The original traced body remains in a named group; editable vector patches and local clip paths refine its contact contour. `interface.framePoint` retains the refinement frame while the anchor itself sits on the fitted contour. Preserve both IDs and local URL references when placing repeated copies. Rerun `scripts/fit_interfaces.py` after a scale or contact-art change.

The complete lesson checks 512 normal/kinase-block states for annotation/arrow intersections and filled-body penetration, and renders 23 review frames. Matched contour samples agree within floating-point precision. Separate P-circle overlays show representative receptor phosphorylation, MEK S/S and ERK T/Y; RAS exchange and aggregate RAF activation remain distinct. These curves express a teaching interface rather than a solved molecular surface.

## v0.7 continuous-outline repair

Source PNGs are unchanged. Complete closed cubic body contours replace the contact patches and cutting clips. Chord-length tangents prevent curve overshoot; protected contact knots preserve the actual mating profile. Color cores are cleaned before extension to the body boundary. A single body clip contains semantic colors, and only genuine domain boundaries receive internal lines.

All 16 generated icons render as one connected body each. Across 17 contact instances, the maximum measured actual SVG outline separation is 0.039 drawing units; the maximum tangent-direction mismatch after coordinate rounding is 0.096 degrees. The scene uses outer weight 1.6 and internal weight 1.1 drawing units, normalized by actor scale. Magnified unbound/assembled forms and whole-figure frames were visually inspected. These are schematic geometric checks, not molecular structure measurements.

See the [before/after contact review](../../contour-review.html) and [actual curve checks](../contour-validation.json).
