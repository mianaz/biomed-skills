# Verification · 2026-10-19 · contour and annotation update

- The full 42-second normal pathway and 9-second kinase-block comparison were sampled every 0.1 seconds: 512 states. Actual SVG silhouettes, Arial text bounds, arrow shafts/heads, phosphorylation circles and nucleotide glyphs had no detected annotation/arrow collisions. Filled-body overlaps above 24 square drawing units were absent at those samples. Shared outline seams are excluded from the filled-body measurement.
- Eight schematic contact types share complementary contour samples at their intended assembly scales. Across 194,530 matched contour samples, maximum separation was 2.35e-13 drawing units. This checks illustrative curve agreement, not atomic protein geometry. Original traced bodies, editable contact paths and local vector clips are retained; each fitted anchor lies on its new contour.
- Recruitment now routes the GRB2–SOS1 complex below RAS before docking. Ligands approach the extracellular sites from the outer sides. RAF labels keep one side/anchor convention through recruitment. GDP/GTP circles move separately from a stable exchange caption.
- P circles appear on both receptor tails after phosphorylation. Two MEK badges carry S/S and two ERK badges carry T/Y. RAS GDP/GTP and aggregate RAF activation retain distinct text states. The kinase-block comparison retains GDP-bound RAS and no downstream phosphorylation badges.
- Twenty-three complete SVG states, including approach, docking, exchange, reaction, release, final and blocked states, were rendered into `qa/animation-review.html`. Important frames and the independent PDF render were visually inspected. These are local SVG renders; live browser playback was not rerun because browser access to the local file is blocked. The earlier `browser-check.json` records the previous playback/control test, not this update.
- All 126 library SVGs passed canvas, palette, named-part, anchor-normal, local vector-clip reference and alpha-bound checks. Fitted tabs may use the reserved canvas margin; none is clipped by the 160-unit canvas. Icons contain no raster, text, filters or scripts.
- The static SVG/PDF uses ArialMT only. Minimum text size is 10.95 pt at 190 mm width. Mechanism geometry and final/blocked states passed the existing model check; arrow direction, spacing and embedded script syntax passed the connector check.
- Skill metadata, bundled local references and archive integrity were checked before delivery. The package includes the complete offline HTML, reusable SVG library, generation/tracing workflow, contour fitting helper, annotation helper and source specifications.

## v0.7 whole-contour refinement · 2026-10-20

Sixteen generated icons were rebuilt from their preserved PNGs as complete closed cubic bodies. Independently outlined contact patches and rectangular cuts were removed. Bounded interpolation handles preserve the widths of long straight membrane stalks. Contact knots remain protected during simplification. Semantic color cores remove tiny tracing fringes, while genuine domain boundaries keep lighter internal lines. A single body clip contains colors inside each closed silhouette.

The final actual SVG check found one rendered connected body in every generated icon, maximum rounded tangent-direction mismatch 0.096 degrees, and maximum actual outline separation 0.039 drawing units across 17 contacts. Outer scene weight is 1.6; internal domain weight is 1.1, divided by actor scale before drawing. These are schematic geometry checks. Magnified contact and complete-figure frames were inspected; source imagery is preserved.

Timeline annotation/arrow checks found zero collisions in the 1,023-state TGFβ comparison and 512-state EGFR regression. The filled-body report retains these coupled-partner contact overlaps (24-square-unit reporting floor):

{
  "normal/r1/l1": {
    "first": 2.5,
    "last": 42,
    "maxArea": 40
  },
  "blocked/r1/l1": {
    "first": 2.5,
    "last": 9,
    "maxArea": 40
  }
}

No unrelated filled-body overlap was recorded. The EGFR ligand contact shoulder has a small persistent filled overlap, while its paired core outline fits; this is a teaching illustration, not a rigid-body docking simulation. Membrane, state, pore, arrow and embedded script checks passed. The final SVG/PDF remains Arial with minimum 10.95 pt at 190 mm width.
