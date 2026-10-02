---
name: paper-distill
description: Read a biomedical paper and its supplements or code to explain its scientific contribution, experimental logic, methods and reusable ideas. Use for general paper distillation or journal-club notes; use sc-paper-distill for single-cell-specific method curation.
---
# Paper Distill

Read supplied local assets first, then retrieve missing full text, relevant
supplements and code when accessible. Record title, authors/year, DOI/PMID or URL
and the material actually read. Read figures and captions alongside the relevant
Results and Methods. An abstract supports an abstract-level summary only.

Produce a human-readable `paper-digest.md` with:

- The question, main contribution and closest prior approaches discussed in the paper.
- The argument, organized by question: claim → experiment/comparison and controls
  → observed result → interpretation. Cite exact panels, pages or Methods sections.
- The experimental/computational recipe: biological system, independent unit,
  sample sizes, inputs, tools/versions, key parameters and source/code locators.
- What transfers to the user's project, what must change, and the next concrete
  analysis or experiment. Distinguish author findings from proposed extensions.

Read full-text details of the closest prior work before making a firm novelty
judgment. Preserve and strengthen a useful idea through its substantive addition;
if the central contribution overlaps, identify the specific overlap directly.

For signatures, deliver `gene-sets.tsv` containing all original and actually used
genes, species, mapping/filtering changes, missing genes and literature/database
identifier/version. Document scoring software/function/version, input layer and
normalization, unit and parameters. Separate score calculation from display
scaling; include z-score axis/reference or GSEA ranking statistic/contrast.

Route requested outputs: `paper-evidence-map` for an editable argument graph,
`paper-to-protocol` for executable steps, `protocol-to-methods` for manuscript
Methods, and `scientific-plotting` for figures. Propose reusable skill changes
only when requested; a paper-reading task does not require modifying the suite.
For academic prose, apply nature-writing, nature-polishing and humanizer when
available; write direct, specific sentences tied to the observed evidence.
