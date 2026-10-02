---
name: verify-biomedical-analysis
description: Independently audit a biomedical analysis for design errors, statistical inconsistencies, missing or empty artifacts, broken provenance, unsupported claims, and rerun risk. Use when reviewing an analysis run, checking manuscript-critical results, validating a pipeline before delivery, investigating silent failure, or acting as a fresh-context verifier after another agent executed the work. Prioritize machine-verifiable checks of samples, groups, replicates, contrasts, design rank, confounding, p-values, corrections, effect signs, enrichment universes, figure/table consistency, and claim-to-evidence links. Do not use to plan the analysis or silently repair it.
---

# Verify biomedical analysis

Audit the run from raw artifacts. Treat the executor's interpretation as a claim to
test, not as ground truth.

## Inputs

Request or locate the current run bundle:

- `analysis-contract.json`
- `run-manifest.json`
- `evidence-index.json`
- the files referenced by those artifacts

Use `assets/evidence-index.template.json` only when an evidence index must be
created before review. Follow `references/evidence-index.schema.json` and
`references/verification-report.schema.json`. Read `references/check-catalog.md`
for universal checks. If a registered domain profile is active, load its referenced
catalog as well. Use `assets/rerun-record.template.json` and
`references/rerun-record.schema.json` for strict rerun evidence.

## Workflow

1. **Isolate the review.** Start from the contract, manifest, evidence index, and
   artifacts. Do not reuse the executor's hidden reasoning or accept its summary as
   evidence. Explicitly assert verifier independence only when it is true; otherwise
   record that it is false or not asserted.
2. **Run deterministic checks first.** Execute:

   ```bash
   python scripts/verify_bundle.py --bundle .ai-scientist/current --root .
   ```

   Add `--independent-of-executor` only for a genuinely separate verifier, or pass
   `--verifier-metadata verifier.json` with `verifier_id`, `kind`, and
   `independent_of_executor`. Use `--not-independent-of-executor` to make the
   opposite explicit. Inspect every failure and warning; do not downgrade a machine
   failure with prose.
3. **Reconstruct the study.** Independently determine sample counts, experimental
   units, groups, replicates, exclusions, contrasts, covariates, and batch structure.
   Compare them with the contract and manifest.
4. **Check scientific validity.** Apply the relevant design, statistics,
   enrichment, and figure/table checks from the core catalog. Activate a registered
   extension with `--domain-profile PROFILE_ID`; contract
   `extensions.profiles` entries activate their matching resource profiles
   automatically. Record results in manifest `quality.checks` using the declared
   check ID or required category. Verify assumptions and correction methods rather
   than merely checking that they were mentioned.
5. **Trace every consequential claim.** Follow each claim to a specific artifact
   and locator, confirm the sample set and contrast, recompute simple quantities when
   safe, and mark the claim `supported`, `not_supported`, `inconclusive`, or
   `technical_failure`.
6. **Check rerunnability.** Confirm code, parameters, versions, references, inputs,
   and outputs are recoverable at the assurance level in the contract. For strict
   runs, enforce hashes, frozen dependencies, required source caches, seeds, and the
   strict policy. If rerun is required, independently rerun, calculate recorded
   numeric differences, and pass `--rerun-record PATH`; the verifier rejects
   comparisons outside the contract tolerance.
7. **Issue a verdict.** Preserve the generated JSON report and provide a short human
   summary: verdict, blocking findings, important warnings, and the smallest concrete
   remediation. Use `SHIP`, `HOLD`, or `REWORK` only as a presentation label; the
   machine status remains `pass`, `pass_with_warnings`, or `fail`.

## Finding format

For each non-pass finding record:

- check ID, contract check ID when applicable, and severity
- exact artifact, field, row, or command involved
- observed evidence
- concrete failure scenario or scientific consequence
- smallest verifiable remediation

Do not give vague advice such as “validate more” or “consider robustness.” Separate
required corrections from optional sensitivity analyses.

## Boundaries

- Remain read-only during review. Send accepted fixes to a fresh executor.
- Keep universal checks in the core catalog. Add modality-specific categories and
  checks through `references/domain-check-profile.schema.json`. Register portable
  profiles in suite `resource_profiles`; keep the bundled registry as a standalone
  fallback.
- Do not replace deterministic checks with a panel of models.
- Use multiple independent reviewers only when stakes or ambiguity justify the cost;
  adjudicate disagreements from evidence rather than votes.
- Do not require strict-mode controls for routine exploratory work unless a result is
  being promoted to a manuscript, grant, clinical, or other high-consequence claim.
