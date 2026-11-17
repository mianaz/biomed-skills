---
name: figure-plan
description: Plan biomedical figure storyboards and panel inventories, assemble requested manuscript figures as editable PowerPoint decks, or review an existing whole-figure layout. Use for 文章配图规划、主图附图排版、Figure布局设计 and figure assembly. Planning-only requests finish with the plan. Route scientific-story selection to paper-framing, individual data plots to scientific-plotting and mechanism panels to scientific-visual-explainer.
---

# Figure Plan

Read [shared principles](../biomed-shared/core-principles.md).

Deliver the requested figure plan, assembly or layout review. For a complete
manuscript assembly, default to `main-figures.pptx` and `supplemental-figures.pptx`;
for a specified figure or subset, deliver that subset. One slide holds one complete
figure, with independent panel assets and separate editable letters.

## Prepare

Read [writing principles](../biomed-shared/writing-principles.md) when developing
the scientific story, and [visual standards](../biomed-shared/visual-standards.md)
when designing, assembling or reviewing artwork.
Reuse an existing `paper-framing` brief, claim IDs and overall figure order when
present; otherwise develop the argument from the available findings.

For a planning-only request, deliver the story and panel inventory. Otherwise,
for assembly, carry the requested figures through panel preparation, PowerPoint
assembly, export and inspection. For an audit, inspect the supplied assembly and
report or repair at the requested scope. Reuse established story and panel decisions
for local layout work. Missing data can use labeled placeholders in a draft.

## 1. Establish the story and figure count

Read the available manuscript, figure legends and figure/data inventory. Write
the central discovery in one sentence: what was found, what understanding changes,
and why it matters. Build the figure sequence around the biological questions and
their answers. Distinguish measured results from proposed explanations where that
distinction changes a claim.

If a target journal is known, use [submission-check](../submission-check/SKILL.md)
to retrieve current official limits on main figures, Extended Data / supplemental
items, column widths and typography. Save the source, date and rule. Without a
journal, record provisional width assumptions and proceed.

Propose an explicit count of main and supplemental figures with a reason for each:

- Read [result placement](../biomed-shared/main-text-and-supplement.md) and apply
  the **removal test**: if omitting an experiment changes the central claim or
  leaves its strongest alternative explanation unresolved, keep its decisive
  comparison in main or link the supporting figure explicitly.
- Read [literature patterns](references/literature-patterns.md) when choosing
  multi-panel pairing archetypes or aspect-ratio priors from the 500-panel CNS corpus.
- Use [the plan template](assets/figure-plan-template.md) to record each figure's
  claim, role, panel sequence, main/supplement decision and linked supporting figure.

**Done:** the plan states both counts, one argument per figure, and how the
sequence supports the central discovery within known journal limits.

## 2. Map each panel to evidence and a display

Inspect existing plots/images and their source records. Reuse valid finished
panels directly when they fit the claim and final placement. Produce new panels
through their responsible skill (always exported **without** publication letters):

- Quantitative R/Python panels: [scientific-plotting](../scientific-plotting/SKILL.md).
- Native Prism panels: [graphpad-prism](../graphpad-prism/SKILL.md).
- Mechanism schematics, workflow diagrams or graphical abstract panels: [scientific-visual-explainer](../scientific-visual-explainer/SKILL.md).

Keep each quantitative panel linked to its analysis cohort and full result record.
For features repeated across main and supplemental panels, apply
[analysis consistency](../biomed-shared/analysis-consistency.md) and reconcile each
panel with the same primary feature definition or its explicitly named adaptation.
Use the shared [family-scope rules](../biomed-shared/statistical-analysis.md#define-families-across-datasets)
when selecting panels: moving or omitting a panel alone leaves its comparison
family unchanged. Record result-driven selection; route unresolved inference to
`biomed-stats`.

Give each panel a stable placement ID separate from its movable display letter.
Group panels by the inference they support (`design → readout`, `image ↔ quantification`,
`matched comparison`, `orthogonal support`, or `alternative-explanation test`) and
specify reading order and required adjacencies.

| Evidence state | PowerPoint treatment |
|---|---|
| `ready` | Insert the actual independent letter-free panel asset. |
| `data-ready` | Plot the available data via the plotting skill, then insert the panel (or use a solid rectangle labeled `"Data available — plot pending"` for a layout-only pass). |
| `missing` | Use a dashed neutral rectangle labeled `"Data pending: <comparison/readout>; <chart type>"`. |
| `needs-source` | Use a solid neutral rectangle labeled `"Source/export needed"` when the asset cannot be separated or used at required quality. |

**Done:** every planned panel has a stable ID, source or named gap, chart/schematic
type, evidence group and clear state.

## 3. Assemble figures in PowerPoint

Read [canvas sizing](references/canvas-sizing.md) to choose figure width and solve
height from the evidence groups, and [PowerPoint assembly and export](references/powerpoint-and-export.md)
when building or modifying the decks.

- Deliver the requested decks with slide counts matching the requested figure
  inventory (no cover or section-divider slides).
- Import each panel as its own independent PowerPoint object preserving its native
  aspect ratio; reflow rows instead of flattening or stretching panels.
- Add every panel letter as a separate, editable PowerPoint text box in Arial.
- Arrange evidence groups first, then member panels, using deliberate gutters and
  visual hierarchy (e.g., hero overview or schematic paired with compact narrow/tall
  comparisons). Never import a precomposed whole figure from R, Python, SVG or HTML
  as the slide's figure.

When running blinded benchmark comparisons or training a layout ranker, read
[blinded evaluation](references/blinded-evaluation.md) and [trained ranking](references/trained-ranking.md).

**Done:** the requested decks match the inventory, each figure has a recorded export width
and height, and each panel, placeholder and letter is independently selectable in
the saved PPTX.

## 4. Review at final viewing size and export

Read [layout review](references/layout-review.md) and run the
[effective typography audit](references/effective-typography.md) on the rendered slides.

- Verify effective text size (> 10 pt target, 8 pt floor), scientific typography
  (complete gene italics, upright proteins/units), fixed `palette.csv` mappings,
  label clearance, internal blank space and outer/within-envelope whitespace.
- Repair panel-internal defects in the plotting/schematic source and placement/letter
  defects in PowerPoint, then re-render and re-inspect the affected slide.
- Export each slide via PowerPoint → PDF → lossless PNG/TIFF at the intended
  physical size (600 dpi default) and build the HTML contact sheet for handoff.

**Done:** files open cleanly, each figure has a rendered QC record, exported
appearance matches the PPTX at final manuscript scale, and draft versus ready
status is explicit.
