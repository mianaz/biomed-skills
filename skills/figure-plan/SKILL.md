---
name: figure-plan
description: Plan biomedical main and supplemental figures from a manuscript story and journal requirements, then assemble separate editable PowerPoint decks from individual panels. Use for figure storyboards, evidence inventories with missing-data placeholders, manuscript figure layout, and whole-figure export or visual review. Route single-panel plotting to scientific-plotting.
---

# Figure Plan

Turn the manuscript's scientific contribution into a figure sequence and two
editable PowerPoint files. One slide is one complete figure. Each panel is an
independent asset; each panel letter is a separate PowerPoint text box.

For a planning-only request, deliver the story and panel inventory. Otherwise,
carry the work through assembly, export and rendered inspection. Missing data
become labeled spaces in the plan, so they do not prevent a useful draft.

## 1. Establish the story and figure count

Read the full available manuscript, figure legends and existing figure/data
inventory. Start from the current files. If the manuscript is incomplete, build
a proposed story from the supplied findings and identify the unread sections.

Write the central discovery in one sentence: what was found, what understanding
changes, and why it matters. Build the figure sequence around the biological
questions and their answers. Develop the conceptual contribution; an incomplete
mechanism can still support an important discovery. Distinguish measured results
from proposed explanations at the point where that distinction changes a claim.

If a target journal is known, establish article type and submission stage. Use
[submission-check](../submission-check/SKILL.md) to retrieve current official
limits on main figures, combined display items, supplemental/Extended Data items,
dimensions, typography and formats. Save the source, date and applicable rule.
Use a supplied editorial instruction when it changes the general guidance.
Without a journal, record design assumptions and proceed; do not invent a limit.

Propose an explicit count of main and supplemental figures, with a reason for
each. Main figures carry the discoveries needed to follow the central argument.
Supplemental figures carry relevant depth, supporting controls, validation and
technical detail. Keep a control in main when the main inference needs it there.
Retain consequential conflicting evidence. Preserve the journal's distinction
between Extended Data and Supplementary Figures in names and cross-references.

Use the removal test: if omitting an experiment changes the central claim or
leaves its strongest alternative explanation unresolved, retain its decisive
comparison in main or explicitly link the supporting evidence. Derive figure
counts from these argument units and available space, not a literature median.
When learning from reference papers or choosing between layout patterns, read
[literature patterns](references/literature-patterns.md).

Compare the proposed sequence with a shorter alternative before fixing counts.
Keep an extra main figure when it adds a distinct discovery, protects an essential
comparison, or prevents unreadable crowding. A source-pending image alone does
not earn another main figure. For each figure, connect an observed comparison
to its biological meaning; a list of assays is not yet an argument.

Use [the plan template](assets/figure-plan-template.md) as a compact starting
point. For every figure record its claim or open question, role in the story,
panel sequence, main/supplement decision and linked supporting figure. Resolve
redundant figures and unsupported conclusions before detailed layout.

**Done:** the plan states both counts, one argument per figure, and how the
sequence supports the central discovery within known journal limits.

## 2. Map each panel to evidence and a display

Inspect existing plots/images as well as their source records. Reuse finished
panels directly when they fit the claim and final placement. For available data,
produce the needed individual plot through
[scientific-plotting-tidyplots](../scientific-plotting-tidyplots/SKILL.md),
[scientific-plotting](../scientific-plotting/SKILL.md) or
[graphpad-prism](../graphpad-prism/SKILL.md). Preserve valid existing analyses.
Keep direct plotting data and the editable plot object, script or Prism project.

Give each panel a stable ID, separate from its movable display letter. Record
its question, comparison/readout, source path, evidence state, proposed chart
type and next action. Name the missing experiment or analysis precisely enough
that a collaborator can supply it. Choose chart types for the evidence: images
with quantification, paired observations, trajectories, effect estimates, heatmaps
or other suitable displays. Repeated comparisons may need the same chart type.

Check deposited units and observation levels against the experiment record.
Preserve an unresolved source scale explicitly; a published axis title alone
does not supply a missing normalization. Technical repeats, simulation frames
and measured cells retain their relationship to the biological sample.

Group panels by the inference they support before placing them. Record the
relationship: design → readout, image ↔ quantification, matched comparison,
orthogonal support, or alternative-explanation test. Specify group reading order
and which members must stay adjacent. One lettered panel may contain several
fields, axes or facets; count these separately from independently lettered panels.
Make each support link identify the supporting panel, target panel and inference
it supports. A control for one perturbation does not validate another merely
because they involve the same gene; list unmatched technical checks as context.

| State | PowerPoint treatment |
|---|---|
| `ready` | Insert the actual independent panel. |
| `data-ready` | Plot the available data, then insert the panel. Until plotted, use a solid rectangle labeled “Data available — plot pending”. |
| `missing` | Use a dashed rectangle labeled “Data pending”. |
| `needs-source` | Use a solid rectangle labeled “Source/export needed” when the available asset cannot be used at the required quality or separated safely. |

Every placeholder contains the intended comparison/readout and chart type, for
example “Data pending: perturbation + rescue; paired response plot”. Keep labels
short; put sample details and next actions in the inventory or slide notes.
Use neutral outlines for status, preserving biological colors for data. A missing
result is a question to test, not an assumed positive outcome. Illustrative mock
data belong only in an explicitly labeled layout example, outside research panels.

**Done:** every planned panel has a source or named gap, a display choice and a
clear state. Existing usable evidence appears in the draft.

## 3. Assemble figures in PowerPoint

Read [PowerPoint assembly and export](references/powerpoint-and-export.md) when
building or changing the decks. Read [canvas sizing](references/canvas-sizing.md)
when choosing or revising figure dimensions. Choose panel placement and canvas
size together: constrain width from the intended use, derive height from the
evidence groups, and verify the final export rectangle. Use Arial and start
ordinary plot areas near 50 × 50 mm. Aim for text above
10 pt at final viewing size. Plot labels may use an explicitly agreed smaller
size, with 8 pt as the floor; use a stricter project/journal rule when applicable.

- Deliver `main-figures.pptx` and `supplemental-figures.pptx`. Their slide counts
  equal the planned figure counts. Include no cover or section-divider slides.
  If a planned count is zero, state that explicitly; do not invent a figure.
- Generate/export each panel separately and import it as its own PowerPoint
  object. A chart, image or schematic can be a panel; independently lettered
  panels remain separately movable.
- Export panel assets without figure letters. Add every letter as a separate,
  editable PowerPoint text box. Store figure claims and long legends in notes
  and the plan unless the requested figure design includes them.
- Match every placement ID to the source inventory before assembly. Keep display
  letters out of this mapping. Resolve unknown, omitted or duplicate IDs; record
  intentional reuse explicitly.
- Build placeholders as native PowerPoint rectangles and text. Arrange panels
  with align/distribute and a small set of deliberate gutters. Give primary
  evidence enough space; use larger spans or staggered rows when these improve
  the reading order.
- Place evidence groups first, then their member panels. Choose row-wise or
  column-wise reading deliberately. Geometry-only packing is a layout sketch;
  check that it preserves the planned evidence relationships before accepting it.
- Code may generate individual panels, a layout sketch, or native PPT objects.
  The final composition lives in PowerPoint. Do not import a precomposed whole
  figure from R, Python, SVG, HTML or a screenshot as the slide's figure.

Apply the selected plotting skill to each panel; this skill owns figure order,
PowerPoint assembly, letter placement and whole-figure export. Reuse its data,
color and source-delivery rules without adopting its composite-figure examples.

**Done:** both decks match the inventory, each figure has a recorded export
width and height, and each panel, placeholder and letter can be selected
independently in the saved PPTX.

When testing or optimizing this skill against published figures, read
[blinded evaluation](references/blinded-evaluation.md) before preparing cases.
When training or applying a layout ranker, also read
[trained ranking](references/trained-ranking.md) for label provenance, held-out
testing and the limit between a ranking suggestion and an accepted figure.

## 4. Review at final viewing size

Read [layout review](references/layout-review.md) and run the
[effective typography audit](references/effective-typography.md) during candidate
generation and final review. Check small text, oversized text and differences
between equivalent roles; unmeasured embedded text remains a QC gap.
Inspect every rendered slide,
then the full main/supplemental sequence. Separate canvas margins from space
between panels and blank space inside panels. Record dimensions, gutters,
panel size balance and chart-type distribution with their definitions. Use these
measurements to find problems, not as universal beauty scores.
Inspect blank space inside panels too. Enlarging a sparse plot can reduce the
external-whitespace metric without improving the figure. Reconsider figure
grouping or canvas dimensions when the argument occupies only a small part of it.

Check reading order, deliberate size variation, internal blank space, alignment,
uniform effective font sizes, semantic colors and graphic style. Preserve chart
geometry and image integrity. Ask the plotting skill to repair the source panel
when the problem is inside it; fix placement and letters in PowerPoint. Inspect
the affected slide again after changes.
Check the longest category labels at final size, including labels repeated within
facets. Panel-box separation does not establish label clearance. Wrap labels,
change the panel allocation or split the display before reducing type size.

**Done:** each figure has a short review record with observed measurements,
resolved defects and any specific remaining issue. The visual review is based
on actual rendered artifacts, not just object coordinates.

## 5. Export and hand off

Export each complete slide from the saved PPTX. The export reference covers
PowerPoint → PDF → lossless PNG/TIFF at the intended physical size, with 600 dpi
as the raster default unless the journal calls for another resolution. Keep
the PDF and editable PPTX. The bundled export helper also creates an HTML
contact sheet for review; it never assembles panels.

Deliver the two decks, per-figure exports, plan/panel inventory, source assets
and a concise visual review. Use the project's existing folders when present.
Link the HTML preview and primary editable files in the handoff. Figures with
unresolved placeholders remain clearly named draft exports; a complete figure
plan does not imply completed experiments or submission-ready figures.

**Done:** files open, counts and physical/pixel sizes agree, exported appearance
matches the PPTX, and draft versus ready status is explicit for each figure.
