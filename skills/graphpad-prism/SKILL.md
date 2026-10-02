---
name: graphpad-prism
description: Create or edit GraphPad Prism figures and native projects, populate existing Prism templates, and export editable Column, Grouped or XY data tables. Use when the requested deliverable is a Prism project or Prism figure.
---
# GraphPad Prism

Read the companion `scientific-plotting` skill for design, statistics and delivery,
including its `references/graphpad-prism.md`. Use the user's installed Prism and
supplied template when available. For the existing template collection, consult
[references/template_catalog.md](references/template_catalog.md). Locate templates from the current project or
user-provided folder; do not assume a private template collection is installed.

1. Identify table type, independent units, pairing, replicate subcolumns, missing
   values and existing analyses. Preserve the original project; edit a copy.
2. Populate the matching native table using Prism or a verified format-specific
   editor. Preserve graph/table links and analysis settings. Do not treat binary
   `.pzf` files as text. For template `.pzfx`, preserve the embedded Template block,
   table IDs and referenced column structure; a newly written data-only PZFX does
   not retain template styling or analyses. For `.prism` archives, inspect the
   actual contents/version before editing linked JSON and CSV files.
3. Use Arial with all text >10 pt at final placement. Preserve requested colors,
   canvas and geometry in appearance-only edits. Do not enlarge the canvas to
   compensate for undersized text.
4. Open the saved result in Prism, inspect the graph and values, and export the
   requested PDF/PNG. Deliver the editable project, direct plotting CSV and
   statistics/settings. If Prism is unavailable, deliver explicitly labeled
   data-only PZFX plus an R figure using cowplot; state that native rendering was
   not checked. Do not describe a table export as a finished native graph.

R helpers already live in `scientific-plotting/scripts/prism.R`; reuse them.
