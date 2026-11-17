# methods.md discipline

Maintain the project's existing analysis record; `methods.md` is a suitable
default for a new project. For each consequential analysis step, record:

```markdown
## <date> — <step name>
- **Question & design:** outcome, independent unit and target effect/contrast.
- **Method:** what was done (tool + version).
- **References:** PMID/DOI for the method.
- **Parameters & rationale:** key params and WHY these values.
- **Analysis choices:** dataset and analysis-cohort definition; comparison-family
  scope; dataset/result selection basis; which choices preceded or followed
  inspection of outcomes, and why the plan changed.
- **Results:** interpretation of what was observed.
- **Troubleshooting:** for unexpected results, what was tried and the outcome.
```

Use the design and analysis-choice fields when statistical inference is involved,
following the shared [statistical principles](../../biomed-shared/statistical-principles.md).
Link an existing design record rather than copying it into every entry.

This is an analysis record used to prepare manuscript sections. When drafting
Methods, extract the procedures, parameters and analysis choices. Place findings
and biological interpretations in Results or Discussion; retain troubleshooting
in the analysis record unless it changes a procedure that must be reported.

## Self-documenting runs

Make runs reconstructable from disk, not just from memory:

- **Encode key params in output filenames** for swept steps, e.g.
  `com.hvg2000_PC10_res0.6.rds` or `model_lr1e-3_bs256_ep50.pt`. The filename then states the run.
- **Write a per-unit run/QC log table** (one row per sample / run / fold: inputs, key counts,
  thresholds applied, outputs) next to the results — turns a many-unit batch into an auditable
  table instead of buried console output.
