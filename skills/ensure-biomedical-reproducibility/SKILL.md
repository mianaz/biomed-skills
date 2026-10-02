---
name: ensure-biomedical-reproducibility
description: Capture platform-neutral provenance and result lineage for computational, experimental, clinical, and imaging analyses in a validated JSON run manifest, including digital or physical inputs, external sources, protocols, instruments, reagents, models, code or procedures, runtime versions, parameters, QC status, artifacts, deviations, and strict locks. Use while executing or reconstructing biomedical work, preparing an auditable handoff, or making a workflow rerunnable.
---

# Ensure Biomedical Reproducibility

Maintain `.ai-scientist/current/run-manifest.json` while work proceeds. Treat it as
the canonical machine record; do not reconstruct provenance from memory at the end.

## Record the run

1. Copy `assets/run-manifest.json` when execution begins. Reuse the
   `contract_id` from `analysis-contract.json` and assign one stable `run_id`.
2. Register every concrete input read or used. Set `locator_kind` to `file`,
   `collection`, `remote`, or `physical`, retain its locator in `uri`, and map it to
   its logical contract input.
3. Register each database, API, reference, or literature source with the exact
   resource or query, retrieval time, version when available, and mutability.
4. Register result-affecting protocols, instruments, reagents, calibrations, models,
   and reference standards under `resources` with available versions, lots, serials,
   identifiers, or hashes.
5. Append an execution record immediately after every step. Record the
   implementation, exact invocation with secrets redacted, parameters, rationale,
   status, direct input IDs, upstream artifact IDs, resource IDs, and produced
   artifact IDs.
6. Record runtime and package versions. Record both defaults and explicit values
   when they can affect results.
7. Register digital, remote, collection, and physical intermediate or final
   artifacts. Map required products to contract output IDs.
8. Record deviations with their target, reason, and impact.
9. Record whether input QC and statistical-assumption checks were performed. Link
   their outputs, but leave check selection and scientific adequacy to domain and
   verification skills.
10. Update the human-readable methods log after each material step when manuscript
   methods, troubleshooting, or repeated-run history will be useful.
11. Validate the manifest before handoff and after any material update.

```bash
python3 scripts/validate_run_manifest.py \
  .ai-scientist/current/run-manifest.json \
  --contract .ai-scientist/current/analysis-contract.json \
  --check-files --root .
```

Read `references/run-manifest.md` for field rules, strict-mode requirements, and
cross-artifact invariants. Use `references/methods-log.md` for the narrative log.

## Capture file facts

Use the capture helper to compute file sizes, media types, SHA-256 checksums, the
Python runtime, and requested installed-package versions without third-party
dependencies:

```bash
python3 scripts/capture_run_context.py --root . \
  --input counts-file primary-data data/counts.tsv \
  --artifact de-results primary-results table results/de.tsv \
  --package scanpy > provenance-fragment.json
```

Merge the fragment by ID into the manifest; do not replace execution history.

## Apply strict assurance

- Hash every file input and produced file artifact. Identify non-file collections,
  remote objects, and physical items with immutable versions or institutional
  identifiers when available.
- Record exact package versions and a lockfile when software affects results.
- Record the immutable container digest when the contract requires a container.
- Freeze reference genome, annotation, and pathway-resource releases with content
  hashes when used.
- Cache mutable database and API responses as registered artifacts.
- Record code revision, versioned pipeline identity, or a versioned and hashed
  procedure definition.
- Record random seeds for stochastic executions.
- Preserve enough data for the verifier to perform the requested rerun comparison.

Infer strict assurance from the linked contract or pass `--strict` to the validator.

## Keep the methods log

- Append the method and version, references, inputs, parameters and rationale,
  deviations, artifact IDs, factual observed result, and troubleshooting outcome.
- Use a per-sample, per-run, or per-fold TSV/CSV log for repeated executions instead
  of burying unit-level history in console output.
- Encode only identity-defining parameters in filenames; keep the complete parameter
  set in the manifest.
- Link log entries to `execution_id` and artifact IDs.

## Keep boundaries

- Do not choose methods or decide whether a scientific conclusion is correct.
- Do not perform independent verification or silently repair failed analyses.
- Do not prescribe plotting aesthetics, export DPI, scheduler behavior, cluster
  queues, or agent orchestration.
- Do not store credentials, access tokens, private URLs, or unredacted secrets.
- Do not create extra provenance documents when the manifest or methods log already
  owns the information.

## Resources

Resolve all resource paths relative to this skill directory.

- `assets/run-manifest.json`: valid starter artifact.
- `references/run-manifest.md`: provenance and strict-mode guidance.
- `references/methods-log.md`: concise human methods-log discipline.
- `references/run-manifest.schema.json`: canonical JSON Schema.
- `scripts/validate_run_manifest.py`: dependency-free validator.
- `scripts/capture_run_context.py`: deterministic file and environment capture.
