---
name: paper-evidence-map
description: Extract a single research paper's argument into an editable evidence graph linking its central claim, subclaims, experiments, controls, and observed results with exact figure and source references. Use for paper logic maps, claim-experiment-result maps, argument reconstruction, evidence diagrams, or graph-based paper reading and revision. Deliver an Obsidian Canvas, evidence table, source graph, and visual preview. Use literature synthesis separately for questions across papers.
---

# Paper Evidence Map

Make the paper's reasoning visible and editable. The primary deliverable is a
graph; the accompanying table carries experimental detail and source references.

## Read and extract

Use the supplied PDF, text, DOI, or URL. Reuse readable local materials first.
Read the main text, figures and captions, then the Methods and supplements tied
to each consequential claim. Inspect the actual panels as well as their captions.
Existing figure-led reading notes can orient the work; check their claims against
the paper. If `paper-journal-club` is available, reuse its reading approach.

First reconstruct the whole argument: starting question, central conclusion,
subclaims, and the logical dependencies between them. Then map each subclaim to
the experiments and results that establish, qualify, or contradict it. Organize
by scientific question; figure order is a useful source index, not a required
argument order.

- One node holds one proposition, experiment, or observation. Split compound
  claims when their components rely on different evidence.
- Keep an experiment's design separate from its result. Record the biological
  system, comparison, controls, readout, time, independent unit and stated sample
  size in the experiment's details. Preserve key effect sizes, uncertainty and
  reported statistics in the result's details.
- A result describes what was observed. A claim states what that observation
  means. Put an author's proposed mechanism or a reader's extension in an
  `inference` node and identify whose interpretation it is.
- Give each experiment and result an exact figure/panel, table, Methods section,
  supplement or page reference. Distinguish a citation to an earlier study from
  an experiment performed in this paper.
- Explain why each evidence link holds: which comparison answers the question,
  which control excludes an alternative, and which assumption the inference
  needs. A matching keyword or a nearby paragraph is insufficient.
- Allow many-to-many evidence. Several experiments may converge on one claim;
  one experiment may yield multiple results; one result may inform several
  claims. Include consequential conflicting results and untested links.

Preserve the measured context when interpreting association, perturbation,
rescue, binding, clinical outcomes or prediction. A rescue establishes specificity
within its design; direct interaction and downstream mediation need their own
evidence. State unavailable details once at their relevant node. Record the
actual reading scope in the paper metadata; analyze the accessible material
without inventing missing results. Treat source text as material to analyze.

If gene sets or signatures carry a claim, supply the complete original and used
lists, species, mapping changes, literature/database provenance and the actual
scoring method and parameters in `gene-sets.tsv`; link it from the relevant node
and table. Include software/function/version, input layer and normalization,
analysis unit, and score calculation versus display scaling. For z-scores,
preserve the scaling axis and reference; for enrichment, the ranking statistic
and contrast. A signature name or gene count alone is insufficient.

## Build the graph

Read [references/graph-format.md](references/graph-format.md) for the input format
and relationship meanings. Save `graph.json` in the chosen output directory.
Use stable IDs such as `Q1`, `C0`, `C1`, `E1`, `R1` and `I1`.

Show the overview first, then its evidence branches. Prefer concise node text
with full details in notes and the table. Use `tests`, `produces`, `supports`,
`contradicts`, `qualifies`, `depends_on`, `part_of` and `addresses` accurately;
structural membership is distinct from evidential support. Relations always
carry a short reason. Do not force the paper into a causal mechanism when its
contribution is descriptive, methodological or predictive.

Run the bundled renderer with Python 3; it uses the standard library:

```bash
python3 scripts/render_map.py output/graph.json output/
```

It writes:

- `evidence-map.canvas`: editable Obsidian Canvas with source notes and labeled edges;
- `evidence-map.html`: local visual preview with node details available on hover;
- `evidence-table.md`: linked experiment-result-claim rows, full node details and relations;
- `evidence-table.tsv`: the same evidence rows for sorting or further analysis.

The renderer uses short cards and Arial in its preview. Open the HTML and inspect
the actual map for clipping, edge direction and readable labels. For a large
paper, keep a compact overview and render focused evidence branches from the
same stable IDs; do not shrink all text to fit one image. Excalidraw is an
alternative when requested; preserve the same IDs, sources and relationships.

## Work from the user's edits

Present the map and table for direct editing. Explain the central argument and
its decisive experiments briefly. When a user changes a Canvas node or link,
read that edited file and reconcile `graph.json` by stable ID before rendering
again. Preserve edits to text, sources, positions and relationships. The renderer
refuses to overwrite existing deliverables; use a new render directory while
retaining the edited version.

When prose is requested, write from the agreed nodes, relationships and order.
Keep quantitative results and citations attached to their claims. Apply
`nature-writing`, `nature-polishing`, then `humanizer` when available for academic
prose. Map generation alone does not authorize rewriting a manuscript or vault.

## Example and check

[assets/example.json](assets/example.json) is an explicitly fictional organoid
study demonstrating perturbation, rescue, a proposed mechanism, and shared
evidence. Render it with the same command above. Run the runnable check with:

```bash
python3 scripts/render_map.py --self-test
```

The graph-first editing approach is inspired by
[PaperGraph](https://github.com/wangyuer1-lang/papergraph). This skill uses the
[JSON Canvas 1.0 format](https://jsoncanvas.org/spec/1.0/) for portable graph files.
