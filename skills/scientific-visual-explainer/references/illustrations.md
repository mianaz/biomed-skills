# Choose the illustration by its scientific job

## Biomedical artwork and licensing

Inspect actual reference artwork before biomedical illustration work. NIH BioArt,
Bioicons and Servier can inform recognizable biological forms; verify each
retrieved asset's license. Keep source references, reading/inspection scope and
asset provenance. A catalog entry alone does not establish visual suitability.

Select one of two modes. For **native source reuse**, retain the original vector
and attribution, preserving its appearance unless the requested edit requires a
change. For a **unified family**, use [Biomed Icons](../assets/biomed-icons/README.md)
and its shared style. For a missing or unsuitable icon, use the built-in image generation tool, then
convert to reusable SVG paths with named parts and source-space anchors and add
the result to the library. Follow [generated-icons.md](generated-icons.md). Avoid tracing
proprietary figures; an adaptation must retain its source license and attribution.
Do not describe an adapted source path as an original MIT drawing.

Keep an icon stable across scenes. Recolor only through deliberate family/state
conventions. Keep the visible art separate from invisible contact anchors,
membrane paths and camera controls. Reuse the family's phospholipid and membrane
parts during budding and fusion. Do not fall back to a new arbitrary blob just
because it is easier to animate. Labels remain separate and must pass layout
checks. Generic proteins/domains are useful teaching symbols, with their scope
recorded; they must not imply a solved structure or atomic interface.

Review a contact sheet for palette, line weight, detail level and readability.
Then inspect actual binding, membrane insertion and transport scenes. A visually
consistent library still needs biologically meaningful anchors and orientation.

Preserve actual compartments, membrane topology, strand identity and documented
interactions. Use cutaways only when they clarify a real relationship. Do not add
organelles, binding pockets or molecular contacts merely to make an icon richer.
Prefer SVG for diagrams. Image generation may supply a more complex illustration
when its critical details can be checked against sources. Keep generated artwork
separate from data and editable annotations. Use supplied proprietary assets only
when the user provides them or their terms allow the requested use; do not trace or
recreate restricted artwork.

## Asset method

| Job | Preferred method |
|---|---|
| Molecular connections, pathway order, compartments, strand polarity, experimental comparisons | Use registered unified-family icons or selected native assets; keep labels, arrows and contact marks separate. Generate and vectorize a missing icon through the shared family workflow. |
| Exact molecular or anatomical structure | Render a cited structure/segmentation or use a verified source figure. Record accession, chain/state and rendering choices where relevant. |
| Literal biological context or a spatial overview that benefits from drawing | Image generation can help, with a source-grounded brief and visual inspection. Label the result as an illustration. |
| Motivation, a conceptual aside or a cover | Optional orange-line editorial art: sparse ink, white background, one orange accent. Keep it separate from the mechanism stage. |

For generated art, write the scientific brief first: entities, counts,
compartments, orientation, connections, required details and known omissions.
Use the available image-generation tool. Keep labels, numerical values and
causal arrows in the HTML/SVG overlay so they remain correctable. Save the prompt,
source references and image together. Inspect against the brief before use;
regenerate or use a vector schematic if a critical relationship is wrong. Generated
art does not replace a requested native icon in an asset-led animation or remake.

Generated imagery does not establish atomic geometry, stoichiometry, a binding
interface, microscopy appearance or an experimental result. Exact structures
need structural evidence. A photograph-like image of invented experimental data
is unsuitable for a paper explanation.

Orange-line art works best for a supporting idea rather than a biological
mechanism. Borrow its restraint, not a mandatory metaphor or tiny character.
Prefer the actual molecule, tissue or apparatus when it already explains the
point. The main stage should keep one visual vocabulary. When available, the
`imagegen` or `orange-line-illustration` skill can assist; neither is required.

## Icon QC with references

Check biology and visual language separately. Use a scientific figure, structure or
morphology atlas to check defining features (membrane count, nucleus shape, domain
order, sidedness). Use an inspected BioRender or other public illustration example
to check legibility, level of detail and composition. Keep source URLs and visual
versus text-only reading scope beside each new family. A public preview permits
visual comparison; it does not make the artwork an openly licensed asset.

For related cell types, distinguish demonstrated morphology from symbolic category
cues. For example, T-cell subtype badges are teaching conventions, not a claim that
the subtype can be recognized from an unstained cell outline. Check each binding
anchor against its intended named part and the rendered contact frame.
