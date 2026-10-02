# Authors' upstream processing

Recover what the data authors actually did so downstream users know which operations
have already changed the values or cell set. Sources commonly include repository
sample pages, data-processing fields, paper methods, supplements, and deposited
code.

Capture, when available:

- chemistry and read structure;
- reference genome and annotation release;
- alignment or pseudoalignment tool and version;
- gene-counting mode, including exon-only versus intron-inclusive counting;
- cell-calling and barcode filtering;
- cell- and gene-level QC thresholds;
- ambient-RNA correction and input matrix class;
- doublet detection and whether flagged cells were removed;
- normalization, variable-feature selection, scaling, and regression;
- batch integration or reference mapping;
- clustering and annotation method; and
- the exact deposited object or matrix stage corresponding to those steps.

For each field, distinguish direct documentation from inference. If the paper and
repository conflict, retain both statements and flag the conflict. This summary is
method context; file, command, version, and source lineage belong in
`ensure-biomedical-reproducibility`.
