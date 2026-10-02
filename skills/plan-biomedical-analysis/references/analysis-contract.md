# Analysis contract guide

Use the contract to define what must be answered and delivered before execution.
Keep narrative detail out of the JSON unless it changes a decision, method, output,
or validation requirement.

## Convert the request into testable questions

Replace broad comparisons with measurable components.

| Broad request | Contract questions |
|---|---|
| Is model A better than model B? | Does A recover the prespecified cell types? Are matched cell types transcriptomically closer to the reference? Does A reproduce the target functional activity? |
| Find important pathways | Which contrast and direction matter? Which gene universe and multiplicity rule apply? Which pathway score or enrichment statistic will answer the question? |
| Characterize treatment response | Which experimental unit, time point, comparator, covariates, effect measure, and minimum evidence define a response? |

Write each question so a result can be `supported`, `not_supported`, or
`inconclusive`. Preserve meaningful negative results.

## Fill the core fields

| Field | Record |
|---|---|
| `profile` | Analysis mode, assurance level, and permitted autonomy |
| `objective` | One primary decision or knowledge gap |
| `questions` | Specific questions answerable from the planned evidence |
| `inputs` | Logical input roles, not concrete file paths |
| `design` | Study type, nested units, analysis unit, outcomes, analysis sets, factors, contrasts, and covariates |
| `governance` | Compact risk screen, known approvals, and operating restrictions |
| `steps` | Purpose plus a fixed method or a method-selection rule |
| `required_outputs` | Only artifacts needed to answer questions or audit risks |
| `validation` | Observable pass criteria and their severity |
| `constraints` | Data, compute, time, policy, or user limits |
| `audiences` | Intended consumers of the eventual result |

Use stable IDs that remain meaningful after filenames change. Keep concrete input
paths, commands, versions, parameters, and produced artifacts in the run manifest.

## Specify the design

- List `units` from independent or outer units toward nested units and link each
  child with `parent_unit_id`. Set `analysis_unit` to one declared `unit_id`; do not
  substitute cells, reads, lesions, visits, or repeated measurements for independent
  replication.
- Define measurable `outcomes` and label their role. An exploratory study may use an
  empty outcome list when it has no prespecified endpoint; do not invent one.
- Define at least one `analysis_set` with its unit level and inclusion rule. Use
  distinct sets when primary, sensitivity, safety, or per-protocol populations
  differ.
- Define contrast direction in plain language.
- Record pairing, blocking, batches, covariates, and known confounding in the factor,
  contrast, or constraint descriptions.
- State exclusions or missing groups that can change interpretation.
- Mark a design question unresolved when metadata cannot answer it.
- Avoid promising power, causality, or generalization that the design cannot support.

## Screen governance risks

Set each risk flag to `yes`, `no`, `unknown`, or `not_applicable` for human subjects,
animals, sensitive data, and hazardous materials. Use `no` only when the risk was
considered and is absent; use `not_applicable` when the category cannot apply. Record
approval identifiers or statuses and restrictions such as access controls, permitted
environments, export limits, or biosafety boundaries. Treat `unknown` as unresolved,
not as permission. Route decisions to the responsible institution or specialist;
this contract records the boundary but does not grant approval.

## Choose methods without stealing domain ownership

Set `method` when the method is prespecified, required for compatibility, or already
selected by an applicable domain skill. Set `selection_rule` when the executor must
choose from data properties or field guidance. Allow both only when the rule defines
a documented fallback from the named method.

Keep domain-specific thresholds, QC rules, and tool arguments in the domain skill or
execution configuration. Put only choices that affect the scientific contract here.

## Scale safeguards

Treat `analysis_mode` and `assurance` as separate axes:

- `exploratory`: permit adaptive choices and label resulting claims accordingly.
- `confirmatory`: preserve specified endpoints and contrasts; document deviations.
- `basic`: require a valid contract and explicit assumptions.
- `standard`: add ordinary QC, assumption checks, evidence mapping, and review.
- `strict`: declare lockfile, container, reference-freezing, source-caching, and rerun
  requirements in `strict_policy`.

Use strict assurance for high-consequence decisions, long-lived archival results,
fragile multi-step workflows, or explicit exact-rerun requirements—not simply
because more controls are possible.

## Limit questions to the user

Ask when the answer changes a contrast, experimental unit, endpoint, irreversible
step, cost, privacy boundary, or interpretation. Otherwise choose a reversible
default, state it in the contract, and proceed.

Use `autonomy` to encode the working agreement:

- `autonomous`: execute safe defaults and surface assumptions.
- `collaborative`: request input at material decision points.
- `approval_required`: stop before listed consequential choices.

## Calibrate collaboration without guessing

Infer only task-relevant familiarity from the user's language, supplied artifacts,
and prior decisions. Distinguish:

- confident, explicit preferences that should be preserved unless contradicted by
  the objective or evidence;
- questions the user already identifies as uncertain;
- likely unstated preferences that should be tested with examples rather than
  assumed; and
- possible misconceptions or missing considerations that need a concrete,
  verifiable explanation.

When this changes execution, record a compact `extensions.user_context` object with
`domain_familiarity`, `stated_preferences`, `known_unknowns`, and
`assumptions_to_surface`. Do not turn it into a personality profile. Proceed with
safe best-practice defaults when the user is busy or unfamiliar, but expose the
assumption and invite correction at a material decision point.

Put domain-pack configuration in `extensions.profiles`, keyed by a stable profile ID
such as `clinical.cohort` or `imaging.segmentation`. Keep each value an object and let
the owning pack define and validate it. Other compact extension keys remain allowed
for backward compatibility.

## Define outputs and validation

Require the smallest artifact set that answers the questions. Give every output a
stable `output_id`, kind, and purpose. Prefer structured tables for machine handoff
and reserve presentation choices for the communication or figure skill.

Write validation criteria as observable conditions, for example:

- "Every required sample maps to exactly one group."
- "The design matrix is full rank."
- "The requested contrast direction is encoded as treatment minus control."
- "The primary result table contains effect, uncertainty, and adjusted significance."

Do not perform these checks during planning; define what downstream execution and
verification must check.

## Preserve cross-artifact identity

Require downstream artifacts to reuse `contract_id`. Require the run manifest to map
concrete inputs to `input_id`, executions to `step_id`, and products to `output_id`.
Require evidence claims to reuse `question_id` and `contrast_id`. Require the
verification report to cover every `check_id`.
