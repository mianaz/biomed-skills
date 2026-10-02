# Quality control

QC should identify technical failures without deleting legitimate biology. Work
within sample or chemistry strata whenever their distributions differ.

## Metrics

At minimum inspect:

- total counts and detected features per cell;
- mitochondrial fraction, with species-appropriate gene definitions;
- ribosomal fraction and, where relevant, hemoglobin or dissociation-response signal;
- cell-calling evidence for raw droplets;
- doublet scores and ambient-contamination estimates;
- per-sample cell yield, median counts/features, and fraction flagged; and
- relationships among metrics rather than isolated cutoffs.

Mitochondrial, ribosomal, hemoglobin, stress, and cell-cycle signals can be biological
as well as technical. Interpret them in tissue, assay, and disease context.

## Derive flags

1. Plot or summarize distributions per sample and assay stratum.
2. Use robust rules such as deviations from the median in MAD units where suitable,
   selecting the direction and multiplier from the observed distribution and known
   assay behavior.
3. Add absolute biological safeguards only when justified, such as impossible
   library sizes or clear empty droplets.
4. Review cells flagged by several metrics, sample-specific tails, and clusters
   dominated by QC failures.
5. Store one Boolean flag per rule plus a combined status and reason list.
6. Create the retained set separately; do not overwrite the raw object or erase
   rejected cells from the QC table.

## Sample-level gate

Escalate samples with markedly different yield, complexity, ambient burden, doublet
rate, or composition. A failed sample cannot be repaired by deleting enough cells.
Decide sample exclusion at the biological-replicate level and document its impact on
the design.

## Transformation cautions

- Preserve counts before normalization, scaling, or variance stabilization.
- Fit transformations in a way consistent with later integration and testing.
- Regress a covariate only when it is unwanted, measured reliably, and not
  confounded with the target biology.
- Evaluate cell-cycle regression with before/after marker and structure checks when
  proliferation is not itself the question.
