# Ambient RNA

Ambient correction depends on the input representation and capture process. Run it
per sample because the soup profile and loading conditions are sample-specific.

## Choose by available data

- **Raw unfiltered droplets:** a generative method such as CellBender can model empty
  and cell-containing droplets. Estimate expected cells and the modeled droplet range
  from the barcode-rank curve, loading record, and cell-calling evidence; do not copy
  fixed values across samples.
- **Filtered counts only:** a method such as DecontX can estimate contamination from
  cell clusters or latent populations. Treat its output as an estimate and inspect
  sensitivity to the initial grouping.
- **Plate-based data:** do not use empty-droplet soup models; there is no shared
  droplet pool with the same assumptions.
- **Nuclei:** use nucleus-appropriate expectations and recognize that abundant
  cytoplasmic transcripts may appear as ambient signal.

## Validation gate

Compare uncorrected and corrected values for:

- expected contaminant markers in implausible cell types;
- canonical markers in the cell types that genuinely express them;
- library sizes, detected features, and fraction of counts removed;
- sample-specific contamination estimates; and
- rare populations that might be erased by overcorrection.

Keep the original counts and store corrected counts in a separate named layer. Reject
an output with negative values, unexplained large count loss, or loss of genuine
lineage markers. Ambient correction reduces contamination; it does not establish cell
identity.
