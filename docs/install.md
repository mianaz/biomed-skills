# Install into an agent harness

For figures only, run from the repository root:

```bash
python3 tools/install_skills.py \
  --target "${CODEX_HOME:-$HOME/.codex}/skills" \
  --skill create-scientific-figures
```

For Claude Code, use `--target "$HOME/.claude/skills"`. For another harness, use
its configured skill directory. Start a new session after installation.
Then follow the [figure quickstart](../skills/create-scientific-figures/references/quickstart.md)
to check R/Python and Arial and run the three examples, including editable Prism
tables. The installer copies skill files; it does not provision analysis software.

The repository is the canonical source. The installer uses `suite.json` schema 2 to
select portable skill packages and always includes their transitive hard requirements.
Pass the destination harness's skill directory explicitly; no platform-specific path
is built into the suite.

## Install a bundle

Preview the general biomedical pack:

```bash
python tools/install_skills.py \
  --target /path/to/agent/skills \
  --bundle general \
  --dry-run
```

Available bundles are:

| Bundle | Intended use |
|---|---|
| `core` | Modality-neutral planning, provenance, verification, orchestration, figures, and communication |
| `general` | Core plus cross-domain study, data, evidence, and modeling methods |
| `single-cell` | Complete single-cell and Perturb-seq pack |
| `spatial` | Focused spatial-transcriptomics pack |
| `clinical` | Clinical and epidemiologic analysis |
| `imaging` | Medical-imaging and general model evaluation |
| `experimental` | Experimental design and dose-response analysis |
| `governance` | Method distillation and controlled skill maintenance |

Multiple `--bundle` options may be combined. Included bundles and each selected
skill's `requires` graph are resolved automatically.

## Install individual skills

`--skill` remains useful for a focused installation. Hard requirements are still
included, so this command installs the verifier together with its planning and
provenance foundations:

```bash
python tools/install_skills.py \
  --target /path/to/agent/skills \
  --skill verify-biomedical-analysis
```

Legacy names are accepted and resolve to their canonical replacement. For example,
`--skill distill-omics-papers` selects `distill-biomedical-methods`.

Recommendations are deliberately opt-in because they broaden an installation. Add
`--include-recommended` to recursively include every selected skill's `recommends`
relations and those skills' hard requirements:

```bash
python tools/install_skills.py \
  --target /path/to/agent/skills \
  --skill evaluate-medical-imaging-models \
  --include-recommended
```

With neither `--skill` nor `--bundle`, the installer selects the entire registered
suite.

## Copy, link, and collision behavior

Copying is the default. In a development environment, use `--mode symlink` so edits
in this repository are visible immediately. Existing destinations are refused by
default. `--replace` moves each collision to a timestamped backup before installing;
it never deletes the old package.

Use `--registry /path/to/suite.json` and `--source /path/to/skills` only when testing
an alternate registry or canonical source.

## Registry semantics and audit

Each schema-2 skill declares:

- `kind`: `foundation`, `router`, `leaf`, `adapter`, or `governance`;
- `scopes`: scientific domains in which it applies, with `any` reserved for
  modality-neutral skills;
- `stage`: its primary research-lifecycle stage;
- `requires`: hard installation and composition dependencies;
- `recommends`: optional companions selected only on request;
- `routes_to`: valid destinations owned by router skills;
- `optional_capabilities`: useful but non-mandatory runtime facilities;
- `legacy_names`: aliases that resolve to the canonical package.

Bundles contain direct `skills` and may compose other bundles through `includes`.
Optional top-level `resource_profiles` map profile IDs to files relative to the suite
root; a skill may reference those IDs with `resource_profiles`. The audit rejects
missing or escaping profile paths, unresolved relations, hard-requirement or routing
cycles, invalid bundle references, bundle cycles, and ambiguous legacy aliases.

A profile manifest is a JSON object of this form; its schema and catalog paths are
resolved relative to the manifest itself:

```json
{
  "schema_version": "1.0.0",
  "profile_id": "domain-task",
  "scope": "domain",
  "contract_extension": {
    "key": "domain_task",
    "schema": "analysis-contract-extension.schema.json"
  },
  "verification": {
    "catalog": "verification-catalog.json",
    "required_categories": ["data_integrity", "statistical_validity"]
  }
}
```

The audit validates this shape and the existence of both referenced files.

Run it before installation:

```bash
python skills/maintain-biomedical-skills/scripts/audit_skill_suite.py \
  skills \
  --registry suite.json
```
