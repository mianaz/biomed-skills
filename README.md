# biomed-skill

Biomedical research and writing skills. Version **0.1.0**.

| Skill | Deliverable |
|---|---|
| `paper-framing` | Central contribution, biological significance, conceptual model and overall figure sequence |
| `paper-writing` | Manuscripts, narrative Reviews, Perspectives and reviewer responses drafted from evidence |
| `paper-polishing` | Existing prose polished, translated or compressed with its meaning preserved |
| `paper-review` | Prioritized scientific review findings with evidence locations, repairs and resolution checks |
| `citation-audit` | Claim-to-source verification with source locators, support verdicts and coverage |
| `biomed-stats` | Study design, sample size, statistical analysis and review with effects, uncertainty and reusable R outputs |
| `scientific-plotting` | R/tidyplots, ggplot2/cowplot or Prism figures, editable source, direct plotting data and rendered checks |
| `figure-plan` | Manuscript figure story, evidence/gap inventory, separate main/supplemental PowerPoint decks and inspected PNG/TIFF exports |
| `graphpad-prism` | Native Prism workflow, template editing and accurately labeled PZFX exports |
| `scientific-reproducibility` | Shared analysis outputs, source data, parameters and Methods records |
| `paper-distill` | Paper contribution, experimental logic, reusable methods and project-specific next steps |
| `paper-evidence-map` | Editable claim–experiment–result graph, evidence tables and visual preview |
| `scientific-visual-explainer` | Interactive HTML lessons for concepts, reviews and papers; visual slides or animated video when requested |
| `paper-to-protocol` | Sourced step-by-step protocol, printable HTML/Markdown and Labmate import JSON |
| `protocol-to-methods` | Publication-style Methods based on protocol plus actual experiment records |
| `submission-check` | Current journal/stage checklist and organized submission files for Cell, Nature or Science journals |
| `literature-library` | Question-led library, reading queue and cross-paper synthesis |
| `research-ideation` | Interesting research questions, working models and informative first tests |
| `experiment-design` | Biological comparisons, controls, pilot plan and outcome decisions |
| `research-project` | Priorities, feasible task/calendar plan and a top-level HTML result dashboard |
| `lab-records` | Linked runs, protocol versions, samples/reagents and raw-data locations |


## Install

For Codex:

```sh
codex plugin marketplace add https://github.com/mianaz/biomed-skills.git
codex plugin add biomed-skill@biomed-skill
```

For Claude Code:

```sh
claude plugin marketplace add mianaz/biomed-skills
claude plugin install biomed-skill@biomed-skill
```

For a directory-based installation, copy the complete `skills/` contents to the
agent's skill directory. Keep `biomed-shared/` and section references beside their
consumers. R, Python, Prism or connected applications are needed by the workflows
that use them. Private libraries and project outputs stay in their own locations.

## Choose a workflow

Choose by the requested result. Framing chooses the scientific story; writing
creates prose or rebuilds its argument; polishing preserves the claims and
reasoning chain while improving existing text. Review, citation audit and
submission checking produce their respective assessments. Each entry links only
the guidance relevant to its task.

Examples:

- Draft Results from supplied figures, or synthesize studies into a Review.
- Polish a title, translate a Discussion, or revise replies to reviewers.
- Check scientific logic or verify claims against their cited passages.
- Write Methods from execution records or prepare initial submission files.
- Choose a new biological direction and design informative experiments.
- Produce scientific figures with editable code, direct data and inspected exports.

The repository distributes the skills, runtime references, scripts, assets,
installation metadata and license. Development notes and evaluation records are
maintained outside the published package.
