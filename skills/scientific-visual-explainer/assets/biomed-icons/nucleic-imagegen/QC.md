# DNA/RNA refresh · 2026-10-20

Both icons were generated with the built-in image tool, then converted with trace_icon.py into palette-controlled SVG paths. sources/ retains the accepted transparent PNGs and quantized tracing inputs. prompts.json retains the initial, unsuccessful correction and accepted DNA regeneration prompts, and the accepted RNA prompt. specs.json retains source-pixel anchors and semantic colors.

Visual references: BioRender [DNA (2D, short)](https://www.biorender.com/icon/dna-2d-short) and [mRNA](https://www.biorender.com/icon/mrna). Their public watermarked previews were visually inspected for restrained contours, line weight and detail level. This is newly generated artwork, not a copy or trace of BioRender artwork.

DNA uses broad teal/lavender ribbons, pale base-pair rungs and alternating teal/lavender/teal foreground crossings. No specific sequence, handedness or atomic geometry is asserted. The surface-contact anchor is on the lower outline for a consuming protein complex; geometry and relative sizes are schematic.

RNA is one continuous lavender curve with unpaired teal/mint nucleotide tabs. Unlike the reference mature mRNA icon, this generic transcription-output icon omits cap and poly-A features. It does not assert sequence, processing state or a particular secondary structure.

The refreshed assets are registered as dna-ig and rna-ig; older DNA/mRNA icons remain for existing consumers. The TGFβ lesson now uses these two horizontal icons. Actual source, traced vector and complete bound/transcription frames were inspected. The output arrow was repositioned to clear the shifted SMAD3 label. At 1,023 timeline samples, there were zero detected text/arrow/P-badge collisions. The previously documented ligand–RII recruitment contact overlap is unchanged. All 134 library SVGs passed canvas, palette, named-part, local-reference, normal and alpha-bound checks. No icon SVG contains a raster image, text or filter.

## v0.7 continuous-outline repair

Source PNGs are unchanged. Complete closed cubic body contours replace the contact patches and cutting clips. Chord-length tangents prevent curve overshoot; protected contact knots preserve the actual mating profile. Color cores are cleaned before extension to the body boundary. A single body clip contains semantic colors, and only genuine domain boundaries receive internal lines.

All 16 generated icons render as one connected body each. Across 17 contact instances, the maximum measured actual SVG outline separation is 0.039 drawing units; the maximum tangent-direction mismatch after coordinate rounding is 0.096 degrees. The scene uses outer weight 1.6 and internal weight 1.1 drawing units, normalized by actor scale. Magnified unbound/assembled forms and whole-figure frames were visually inspected. These are schematic geometric checks, not molecular structure measurements.

See the [before/after contact review](../../contour-review.html) and [actual curve checks](../contour-validation.json).
