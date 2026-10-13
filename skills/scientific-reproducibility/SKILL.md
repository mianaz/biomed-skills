---
name: scientific-reproducibility
description: "Use when producing a figure, saving an analysis object, or making an analytical choice in ANY data-analysis / computational-science work (R or Python) — the universal output & reproducibility contract: dual-version figures, source-data export, exact p-values (not stars), publication dpi/vector, a running methods.md log, param-encoded output filenames, and routing compute-heavy steps through the job scheduler. Domain suites (single-cell, bulk RNA-seq, proteomics) inherit this and add their own deltas. Use for analysis outputs intended for reporting or reuse."
---

# Scientific reproducibility — the output contract

## Overview
Analysis outputs must be **rebuildable and auditable by someone who wasn't there** — including future-you. Every figure ships in two forms with its source data; every choice lands in a log; every expensive run states itself on disk. These are correctness/reproducibility rules, not style preferences.

## When to use
Any analysis step that produces a figure, saves a results object, or makes an analytical choice (test, threshold, parameter) — in R or Python. Apply the reporting contract to outputs intended for reporting or reuse. Application and infrastructure implementation are outside this workflow.

## Quick reference
| Concern | Rule | Detail |
|---|---|---|
| Layout | `figures/  source_data/  objects/  methods.md` at project root | below |
| Every figure | save `_titled` (title + full stat details) AND `_clean` (no title); PNG ≥600 dpi + vector PDF | references/figure-output-contract.md |
| Every figure | export the tidy data behind it → `source_data/<plot>.csv` + `.rds` | references/figure-output-contract.md |
| Comparisons | run the appropriate test, show the **exact p-value**, not significance stars (unless stars requested) | references/figure-output-contract.md |
| Logging | append method+version, refs, params+rationale, results to `methods.md` after each step | references/methods-log.md |
| Swept runs | encode key params in output filenames; write an auditable run/QC log table | references/methods-log.md |
| Naming | cluster/sample/category names = letters, digits, `_` only | inline |
| Compute-heavy | never run heavy/GPU steps on a login node — submit via the scheduler | inline |

## Compute-heavy steps go through the scheduler
Alignment, model training/integration, large simulations, GPU jobs, and atlas-scale runs belong in a batch job, not an interactive/login shell — login nodes are shared and may lack the CPU features (e.g. AVX-512) the compute nodes have, so code can silently run slow or crash with opaque illegal-instruction errors. Right-size CPU/memory/time and submit through the job scheduler. On a Slurm cluster, prepare a job script using the project's confirmed account,
partition, environment and resource limits. Set CPU, memory, wall time, GPU needs,
working directory, command and separate stdout/stderr paths explicitly. Reuse the
project's submission conventions, record the job ID and inspect completion logs
before reporting success. Resolve unknown cluster settings from the project or
administrator documentation; use allocated compute resources for heavy work.

## Naming hygiene
Fix names at creation time (annotation, sample sheet), not after outputs exist: letters, digits, `_` only. Slashes, spaces, `@`, and other special characters break file paths, classifiers, and regex parsing with vague downstream errors.

## Preserve reproducibility during code revision
Retain required figure versions, source-data exports, exact statistical results,
vector output and the `methods.md` log when revising analysis code. Improve code
clarity while preserving scientific meaning, provenance and reproducibility.

## Project conventions
Apply the project's documented object formats, R/Python interfaces, category
ordering and other domain conventions alongside this contract. Keep those
choices in the project records so that this workflow can be used independently.
