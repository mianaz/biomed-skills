# biomed-skill

General biomedical workflows. Repository: [mianaz/biomed-skills](https://github.com/mianaz/biomed-skills).
The suite includes scientific framing, manuscript writing, figures, paper reading,
protocols and submission preparation. Version 0.4.0.

| Skill | Deliverable |
|---|---|
| `paper-framing` | Biological story, scientific significance, conceptual model, figure sequence and manuscript prose |
| `scientific-plotting` | R/cowplot or Prism figures, editable source, direct plotting data and rendered checks |
| `graphpad-prism` | Native Prism workflow, template editing and accurately labeled PZFX exports |
| `scientific-reproducibility` | Shared analysis outputs, source data, parameters and Methods records |
| `paper-distill` | Paper contribution, experimental logic, reusable methods and project-specific next steps |
| `paper-evidence-map` | Editable claim–experiment–result graph, evidence tables and visual preview |
| `paper-to-protocol` | Sourced step-by-step protocol, printable HTML/Markdown and Labmate import JSON |
| `protocol-to-methods` | Publication-style Methods based on protocol plus actual experiment records |
| `submission-check` | Current journal/stage checklist and organized submission files for Cell, Nature or Science journals |

## Use

For Claude Code:

```bash
claude plugin marketplace add mianaz/biomed-skills
claude plugin install biomed-skill@biomed-skill
```

For Codex or Cursor, copy the complete directories under `skills/` into your
agent's skill directory, including their references, scripts and assets. A Claude
plugin manifest and local marketplace are included. The suite supplies its own
writing guidance and requires no separately installed skill collection. Companion
workflows named by an entry point are included in this repository. R, Python,
Prism and application connections are needed only for work that uses those tools.

`paper-framing` can also be installed by copying its complete directory alone.
It includes its own framing workflow, section guidance, biomedical examples and
template. Its governing priority is scientific interest and biological
significance: develop the strongest scientific idea the findings can sustain,
make its positive value explicit, and preserve that ambition during revision.
The repository's [AGENTS.md](AGENTS.md) records the same biomedical writing
principles; the installed framing skill carries its essential instructions.

- “Use $paper-framing to develop the biological story, explain the scientific significance, arrange the figures and revise the abstract.”
- “Use $paper-distill and $paper-evidence-map to explain this paper.”
- “Use $paper-to-protocol to turn these Methods and supplements into a printable protocol and import it into Labmate.”
- “Use $protocol-to-methods with this protocol and my completed Labmate experiment record.”
- “Use $submission-check to prepare this manuscript for an initial Nature submission.”

The protocol exporter uses Labmate's existing **Guide → Backup & restore → Import**
workflow. It creates a local custom protocol. A new ID adds an item; the same ID
replaces that item. The printable copy and import file come from one JSON source.

## Writing approach

Framing covers the contribution, the biological explanation, the progression of
claims and figures, and the requested prose. It supports descriptive,
mechanistic, methods and resource studies according to their scientific purpose.
Results develop discoveries and their local interpretation; Discussion builds a
broader explanation and specific research questions. Facts, numerical results,
source attribution and consequential counterevidence remain exact.

Design provenance is recorded in [docs/writing-provenance.md](docs/writing-provenance.md).

## Runnable examples

```bash
python3 skills/paper-framing/scripts/check_package.py
python3 skills/paper-to-protocol/scripts/test_export.py
python3 skills/paper-to-protocol/scripts/export_protocol.py \
  skills/paper-to-protocol/assets/example.json /tmp/protocol-example
python3 skills/paper-evidence-map/scripts/render_map.py --self-test
```

The framing package check validates file structure, local resources and isolation.
Editorial behavior cases are included for human review; the check does not score
writing quality. The protocol fixture is fictional teaching content, not an experimental recipe.
Publisher instructions are retrieved for the target journal and submission stage
when used. No live protocol upload or journal
submission is performed by installation.
