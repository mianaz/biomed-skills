# Methods log discipline

Maintain `.ai-scientist/current/methods.md` when a human-readable running account is
useful. Keep `run-manifest.json` canonical for machine use. Append each entry as the
step completes; do not defer the log until manuscript preparation.

```markdown
## YYYY-MM-DD — <execution_id> — <step name>

- **Purpose:** question or contract step addressed.
- **Method:** tool or procedure and exact version.
- **Implementation:** script, notebook, workflow, redacted command, or procedure.
- **References:** DOI, PMID, RRID, or canonical documentation when applicable.
- **Inputs:** manifest input IDs and relevant upstream artifact IDs.
- **Resources:** protocol, instrument, reagent, calibration, model, or reference-standard IDs.
- **Parameters and rationale:** result-affecting values, defaults, and why used.
- **Deviations:** departure ID and reason, or `none`.
- **Outputs:** intermediate and final artifact IDs.
- **Observed result:** factual summary and pointer to the supporting artifact.
- **QC and assumptions:** recorded status and check/artifact IDs; no adequacy verdict.
- **Troubleshooting:** unexpected behavior, attempted fix, and outcome, or `none`.
```

For a batch, cross-validation, sample-wise, or parameter-sweep workflow, also write a
machine-readable TSV or CSV with one row per unit. Include at least:

```text
execution_id,unit_id,input_ids,parameter_set,status,qc_status,artifact_ids,notes
```

Encode only a few identity-defining parameters in filenames when that prevents
confusion, for example `cluster_res0.6.rds`. Keep the full parameter set and rationale
in the manifest.

Do not add plotting style, scheduler policy, agent assignments, or judgments about
scientific correctness to the methods log.
