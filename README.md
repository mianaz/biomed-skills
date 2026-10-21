# biomed-skill

General biomedical workflows. Repository: [mianaz/biomed-skills](https://github.com/mianaz/biomed-skills).
Single-cell analysis is maintained separately in [sc-skills](https://github.com/mianaz/sc-skills).

| Skill | Deliverable |
|---|---|
| `scientific-plotting` | R/cowplot or Prism figures, editable source, direct plotting data and rendered checks |
| `scientific-plotting-tidyplots` | tidyplots R figures with 50 mm plot areas and shared scientific, font and delivery standards |
| `figure-plan` | Manuscript figure story, evidence/gap inventory, separate main/supplemental PowerPoint decks and inspected PNG/TIFF exports |
| `graphpad-prism` | Native Prism workflow, template editing and accurately labeled PZFX exports |
| `scientific-reproducibility` | Shared analysis outputs, source data, parameters and Methods records |
| `paper-distill` | Paper contribution, experimental logic, reusable methods and project-specific next steps |
| `paper-evidence-map` | Editable claim–experiment–result graph, evidence tables and visual preview |
| `scientific-visual-explainer` | Interactive HTML lessons for concepts, reviews and papers; visual slides or animated video when requested |
| `paper-to-protocol` | Sourced step-by-step protocol, printable HTML/Markdown and Labmate import JSON |
| `protocol-to-methods` | Publication-style Methods based on protocol plus actual experiment records |
| `submission-check` | Current journal/stage checklist and organized submission files for Cell, Nature or Science journals |

## Use

For Claude Code:

```bash
claude plugin marketplace add mianaz/biomed-skills
claude plugin install biomed-skill@biomed-skill
```

For Codex or Cursor, copy `skills/*` into your agent's skill directory. A Claude plugin manifest and
local marketplace are included. There are no required code dependencies between
this package and sc-skills. R, Prism and other execution tools are installed only
when the requested work needs them. Academic-writing workflows use nature-writing,
nature-polishing and humanizer when available, with self-contained prose guidance
for environments without those optional skills.

Install `scientific-plotting-tidyplots` together with `scientific-plotting`; the
variation uses its shared standards and export helpers.

- “Use $scientific-plotting-tidyplots to compare these groups and verify all text at the final figure size.”
- “Use $figure-plan to plan this manuscript's main and supplemental figures, place available panels and missing-data boxes in separate PowerPoint decks, and export the assembled figures.”
- “Use $paper-distill and $paper-evidence-map to explain this paper.”
- “Use $scientific-visual-explainer to teach this paper through a 3Blue1Brown-style interactive HTML lesson.”
- “Use $scientific-visual-explainer to turn this review into visual slides, or explain this concept as a captioned video.”
- “Use $paper-to-protocol to turn these Methods and supplements into a printable protocol and import it into Labmate.”
- “Use $protocol-to-methods with this protocol and my completed Labmate experiment record.”
- “Use $submission-check to prepare this manuscript for an initial Nature submission.”

The protocol exporter uses Labmate's existing **Guide → Backup & restore → Import**
workflow. It creates a local custom protocol. A new ID adds an item; the same ID
replaces that item. The printable copy and import file come from one JSON source.

## Runnable examples

Open [the animated Cas9 paper lesson](skills/scientific-visual-explainer/assets/jinek2012.html)
in a browser. It uses a black stage, CMU Serif, four seekable scenes and a
source-linked mutant comparison. It runs offline with an embedded open font.
The [smaller causal-model lesson](skills/scientific-visual-explainer/assets/causal-models.html)
is an illustrative alternative.

```bash
python3 skills/paper-to-protocol/scripts/test_export.py
python3 skills/paper-to-protocol/scripts/export_protocol.py \
  skills/paper-to-protocol/assets/example.json /tmp/protocol-example
python3 skills/paper-evidence-map/scripts/render_map.py --self-test
```

The protocol fixture is fictional teaching content, not an experimental recipe.
Publisher instructions are retrieved for the target journal and submission stage
when used. No live protocol upload or journal
submission is performed by installation.
