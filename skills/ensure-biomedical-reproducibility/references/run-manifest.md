# Run manifest guide

Update the manifest during execution. Keep facts machine-readable and use the methods
log only for a concise human narrative.

## Record each provenance class

| Section | Record |
|---|---|
| `inputs` | Every digital or physical input, its logical contract input, locator kind and URI/locator, type, size, and file hash |
| `external_sources` | Database/API/reference name, exact query or resource, retrieval time, mutability, version, and cache artifact |
| `resources` | Protocols, instruments, reagents, calibrations, models, reference standards, and identifying versions/lots/serials |
| `environment` | Runtime and package names with exact versions |
| `steps` | Execution and contract IDs, implementation, invocation, parameters, rationale, direct inputs, upstream artifacts, resources, status, and outputs |
| `artifacts` | Digital or physical products, contract output mapping, locator kind and URI/locator, status, type, size, and file hash |
| `quality` | Whether input QC and assumption checks ran, plus factual check outputs |
| `deviations` | Departure target, reason, and expected impact |
| `strict` | Code, pipeline, or procedure identity; lockfiles; container digest; and frozen references |

Use `locator_kind: file` for one local file, `collection` for a directory, archive,
dataset, or series treated as one input, `remote` for a network-resolved object, and
`physical` for a specimen, instrument output, or other institutional locator. Keep
the locator in `uri` for compatibility. Use relative file paths when possible and
absolute persistent identifiers for remote records. Redact secrets from invocations
and queries.

## Keep stable identities

- Give each concrete input a unique `input_id` and map it to one
  `contract_input_id`.
- Give each attempt or repeated unit its own `execution_id`; reuse the contract
  `step_id` across attempts.
- Link each execution to direct `input_ids`, `upstream_artifact_ids`, and
  `resource_ids`. Use empty arrays when a category does not apply.
- Give every intermediate and final product an `artifact_id`.
- Set `output_id` only when an artifact implements a declared contract output.
- Keep missing, empty, and failed required outputs as explicit artifact records.
- Use deviations for unplanned inputs, steps, or outputs rather than changing IDs to
  hide the difference.

## Record execution faithfully

Use `implementation.ref` for a script path, notebook path, workflow definition, or
tool name. Use `invocation` for the exact redacted command or tool call. Record all
result-affecting parameters in `parameters`, including defaults that may change
between versions. Use `rationale` to distinguish prespecified values, domain-skill
rules, data-driven choices, and user decisions.

Record a failed or skipped execution instead of deleting it. Register useful logs as
artifacts. Do not embed full console output in the manifest.

## Record non-software resources

Use `resources` for dependencies consumed across steps rather than data retrieved
from an external source. Record a protocol version or immutable identifier; an
instrument model and serial; a reagent catalog and lot; a calibration identity; a
model or weights version; or a reference-standard release. Use `details` only for
compact domain fields that lack a canonical top-level field. Link every resource to
the steps that used it.

## Record external sources

Set `mutable` to `true` for live APIs, unversioned web resources, rolling databases,
and search results. In strict assurance, save the response or exported result as an
artifact and set `cache_artifact_id`. For a stable source, record its release in
`version`; cache it as well when the provider cannot guarantee immutability.

Treat a reference genome, annotation, ontology, and pathway collection as a
scientific dependency. Record fixed releases in `strict.references` and include
their content hashes when used.

## Record QC without taking domain ownership

Set `quality.input_qc.status` and `quality.statistical_assumptions.status` to
`performed`, `not_performed`, or `not_applicable`. Supply a reason for the latter two.
Record individual check results with artifact pointers.

Do not decide which domain QC metrics or statistical assumptions are appropriate in
this skill. Record what the domain workflow checked; let the verifier judge coverage
and correctness.

## Apply strict mode conditionally

Infer strict mode from `analysis-contract.json`, or request it explicitly during
validation. In strict mode:

1. Require SHA-256 for every file input and every produced or empty file artifact;
   use stable versions or institutional identifiers for non-file records.
2. Require an exact version for each runtime and package, plus an applicable lockfile
   such as `renv.lock`, `conda-lock.yml`, or `uv.lock`, when software affects results.
3. Require a cached artifact for each mutable external source.
4. Require either a fixed version or cached artifact for every external source.
5. Require a random seed for every stochastic execution.
6. Require code revision, versioned-pipeline identity, or a versioned procedure with
   an immutable definition hash.
7. Apply the contract's lockfile and container requirements.
8. Require lockfile, container, and reference hashes when those records exist.
9. Recompute local file hashes with `--check-files` before archival handoff.

Do not activate containers, caching, or exhaustive capture for low-risk work unless
the contract requests strict assurance.

## Enforce cross-contract invariants

When validating against a contract, require:

- Matching `contract_id` and compatible schema major versions.
- At least one concrete input for every required logical input.
- Every executed `step_id` to exist in the contract unless a deviation documents it.
- Every required output to have an artifact record.
- Every required output to be `produced` when a run is `completed`.
- Every input, upstream artifact, resource, produced artifact, source cache, and
  quality-check artifact referenced by an execution to exist.

Leave claim-to-evidence mapping to the evidence index and scientific assessment to
the verification report.
