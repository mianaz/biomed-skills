# Pathway-guided illustration

Use a pathway database to seed the biological graph and relative layout. Select
the figure's message, branch and endpoint before placing artwork.

## Import and map

For a saved KEGG KGML file, run:

```sh
Rscript --vanilla scripts/pathway_layout.R pathway.xml pathway-layout.json
```

This requires R packages `pathview`, `xml2` and `jsonlite`. It retains source entry
IDs, full gene-family membership, node geometry, groups and typed relations.
Keep the input KGML with the output. Pathview is the parser and data-overlay tool;
KEGG supplies the pathway map.

Map each selected entry to a named biological entity, compartment, state and icon
role. Keep a family entry intact until the figure explicitly selects a member.
Give repeated visual instances separate scene IDs. Describe complexes through
their component identities and stoichiometry. Link each activation, inhibition,
binding, reaction or transport event to its scientific source.

## Compose

1. Preserve upstream/downstream order and useful branch relationships from the
   source. Use normalized coordinates as initial positions.
2. Select a layout recipe: membrane-to-nucleus, metabolic chain, organelle
   transport, feedback loop, or a signal–programme–outcome graphical abstract.
3. Fix compartment membership and membrane orientation. Align an icon's named
   membrane, binding or transport anchor to the matching feature in the scene.
4. Expand space for complexes and labels, then route event-specific connectors
   around their visible bounds. The source coordinates remain soft preferences.
5. Keep labels and state marks editable. Render the complete figure and inspect
   contacts, arrow meaning, compartment crossing and effective text size.

A kinase box can represent several genes; a pathway edge can summarize several
events. Resolve these cases in the biological model before choosing a detailed
icon. A graphical abstract can collapse events into a meaningful module while
the mechanism view retains the intermediate steps.

## Source options

| Source | Useful input | Adapter state |
|---|---|---|
| KEGG + Pathview | KGML IDs, relations, groups and starting positions | R importer included |
| Reactome | Diagram JSON geometry and connectors; graph JSON entity identities and complexes | Use source specifications; no portable importer included |
| WikiPathways | GPML nodes, interactions, anchors and groups | Proposed adapter |
| SBGN / SBGNview | Standard process and entity glyphs with layout | Proposed adapter |

Retain each source's attribution and redistribution terms. Keep original library
art and accepted source-reference designs in their own provenance collections.

## Inspect and deliver

When a selected Reactome pathway has no diagram, resolve its enclosing diagram
before requesting layout JSON. Retain source-relative order and select the branch
and compartment view that serve the figure's message. Use measured icon bounds
and label widths to set spacing and route connectors around them.

Check text against text and artwork, including its own icon; arrow shafts and
heads against artwork and labels; filled paths and strokes against the frame;
closed fill contours; compartment titles; and effective text size. Inspect the
rendered result at working, small and enlarged sizes. Record intentional overlaps
inside complexes separately from accidental collisions.

Deliver the source layout, selected entity/event model, editable SVG/PPTX and an
HTML preview. Record the actual visual checks and scientific reading scope.

References: [Pathview](https://bioconductor.org/packages/release/bioc/html/pathview.html),
[KGML](https://www.kegg.jp/kegg/xml/docs/),
[Reactome diagram specification](https://reactome.org/dev/diagram/pathway-diagram-specs),
[GPML](https://vocabularies.wikipathways.org/gpml),
[SBGNview](https://bioconductor.org/packages/release/bioc/html/SBGNview.html).
