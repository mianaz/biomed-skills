# biomed-skill

General biomedical workflows. Repository: [mianaz/biomed-skills](https://github.com/mianaz/biomed-skills).
The suite includes scientific framing, manuscript writing, figures, paper reading,
protocols and submission preparation. Version 0.5.0.

| Skill | Deliverable |
|---|---|
| `paper-framing` | Central contribution, biological significance, conceptual model and overall figure sequence |
| `paper-writing` | Manuscript text drafted or restructured from evidence |
| `paper-polishing` | Existing prose polished, translated or compressed with its meaning preserved |
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

## Demos and examples

[Open the GitHub Pages demo site](https://mianaz.github.io/biomed-skills/).
It includes detailed guides for all 14 skills, seven browser demos, nine plotting
examples, copyable prompts, teaching data and a downloadable skill bundle.
Writing and study examples are fictional; literature-based mechanism lessons
include their sources and reading scope.

Build the static site with `python3 scripts/build_pages.py`, then serve `_site/`
with a local HTTP server. The build uses tracked skill resources and the explicit
teaching fixtures in `site/`; local prototypes and benchmark outputs are excluded.
GitHub Actions publishes the same build through `.github/workflows/pages.yml`.
Set repository **Settings → Pages → Source → GitHub Actions** for first deployment.

## Use

For Claude Code:

```bash
claude plugin marketplace add mianaz/biomed-skills
claude plugin install biomed-skill@biomed-skill
```

For Codex or Cursor, copy complete directories under `skills/`, including
`biomed-shared/`, into the configured skill directory. The shared directory is a
support package without an independent task entry point. The suite supplies all
its writing guidance; external editorial projects are recorded as design sources.
R, Python, Prism and application connections are needed for tasks using those tools.

Install `scientific-plotting-tidyplots` together with `scientific-plotting`; the
variation uses its shared standards and export helpers.

- “Use $scientific-plotting-tidyplots to compare these groups and verify text at the final figure size.”
- “Use $figure-plan to assemble main and supplemental figures in editable PowerPoint decks.”
- “Use $scientific-visual-explainer to teach this paper through an interactive HTML lesson.”

For a focused writing installation, run:

```bash
python3 scripts/build_writing_bundle.py /tmp/biomed-writing.zip
```

The bundle includes `paper-framing`, `paper-writing`, `paper-polishing` and
`biomed-shared`. Keep all four directories together. Copying one of these skills
requires copying the shared directory beside it. Installation instructions are
included in the bundle; installation is performed in the user's agent environment.

- “Use $paper-framing to develop the biological story and overall figure sequence.”
- “Use $paper-writing to draft Results from these figures.”
- “Use $paper-polishing to improve the English in this paragraph.”
- “Use $paper-distill and $paper-evidence-map to explain this paper.”
- “Use $protocol-to-methods with my protocol and completed experiment record.”
- “Use $submission-check to prepare the submission files.”

The protocol exporter uses Labmate's existing **Guide → Backup & restore → Import**
workflow. It creates a local custom protocol. A new ID adds an item; the same ID
replaces that item. The printable copy and import file come from one JSON source.

## Writing approach

Framing develops the scientific argument. Writing develops manuscript text.
Polishing improves existing prose. Shared principles govern all three tasks.
The workflows support descriptive,
mechanistic, methods and resource studies according to their scientific purpose.
Results develop discoveries and their local interpretation; Discussion builds a
broader explanation and specific research questions. Facts, numerical results,
source attribution and consequential counterevidence remain exact.

Design provenance is recorded in [docs/writing-provenance.md](docs/writing-provenance.md).

## Runnable examples

Open [the animated Cas9 paper lesson](skills/scientific-visual-explainer/assets/jinek2012.html)
in a browser. It uses a black stage, CMU Serif, four seekable scenes and a
source-linked mutant comparison. It runs offline with an embedded open font.
The [smaller causal-model lesson](skills/scientific-visual-explainer/assets/causal-models.html)
is an illustrative alternative.

```bash
python3 scripts/check_writing.py --integration
python3 -m unittest discover -s tests -v
python3 skills/paper-to-protocol/scripts/test_export.py
python3 skills/paper-to-protocol/scripts/export_protocol.py \
  skills/paper-to-protocol/assets/example.json /tmp/protocol-example
python3 skills/paper-evidence-map/scripts/render_map.py --self-test
```

The writing check validates the three entry points, bundled references and shared
links in four existing workflows. Tests cover isolated installation and structural
regressions. Agent routing and manuscript quality require separate evaluation;
see [task boundaries](docs/writing-architecture.md) and `tests/writing-cases.json`.
The protocol fixture is fictional teaching content, not an experimental recipe.
Publisher instructions are retrieved for the target journal and submission stage
when used. No live protocol upload or journal
submission is performed by installation.
