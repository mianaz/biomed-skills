# Human marker seeds

These are coarse verification seeds, not exhaustive definitions. Extend them for the
actual tissue and disease, and verify current citations before manuscript use.

## General compartments

| Cell type | Canonical markers | Context | Citation |
|---|---|---|---|
| CD4 T cell | CD3D, CD3E, CD4, IL7R | PBMC/general | PMID 34062119 |
| CD8 T cell | CD3D, CD8A, CD8B, GZMK | PBMC/general | PMID 34062119 |
| NK cell | NCAM1, NKG7, GNLY, KLRD1 | PBMC/general | PMID 34062119 |
| B cell | CD19, MS4A1, CD79A, CD79B | PBMC/general | PMID 34062119 |
| Plasma cell | SDC1, MZB1, XBP1, PRDM1 | general | PMID 36300619 |
| Monocyte/macrophage | CD14, LYZ, FCGR3A, CD68 | PBMC/tissue | PMID 34062119 |
| Dendritic cell | FCER1A, CST3, CLEC9A, LILRA4 | PBMC/tissue | PMID 34062119 |
| Mast cell | TPSAB1, CPA3, KIT | tissue | DOI 10.1093/database/baz046 |
| Endothelial | PECAM1, VWF, CLDN5 | tissue | DOI 10.1093/database/baz046 |
| Fibroblast | COL1A1, DCN, LUM, PDGFRB | tissue | DOI 10.1093/database/baz046 |
| Epithelial | EPCAM, KRT8, KRT18 | tissue | PMID 36300619 |

## Liver and liver-tumor context

The following panels derive from Xue et al., *Nature* 2022,
DOI 10.1038/s41586-022-05400-x.

| Cell type | Canonical markers |
|---|---|
| Neutrophil/TAN | CSF3R, S100A8, S100A9, FCGR3B, CXCR2 |
| Macrophage/Kupffer | CD68, CD163, C1QC, MARCO; resident VSIG4, CD5L, TIMD4 |
| Monocyte | FCN1, S100A8, CD14; CD163 for mono-macrophage states |
| Dendritic | LILRA4 pDC, CLEC9A cDC1, CD1C cDC2, LAMP3 mature DC |
| Endothelial/LSEC | VWF, PLVAP; sinusoidal CLEC4G, STAB2, OIT3, FCN3 |
| Fibroblast/HSC | COL1A1, ACTA2; pericyte or HSC RGS5 |
| Hepatocyte | ALB, APOA1, APOE, TTR, GPC3, AFP |
| Cholangiocyte | EPCAM, KRT7, KRT19, SOX9, PROM1 |

## Liver-specific cautions

- Malignant HCC cells may retain ALB/HNF4A, while malignant cholangiocarcinoma cells
  may express KRT19/EPCAM and mixed hepatobiliary programs. Use inferred copy-number
  structure and patient-specific clonality; `KRT19+` does not prove normal duct.
- Neutrophils are fragile and low-RNA, and are often depleted in droplet data and
  nearly absent from nuclei data. S100A8/S100A9 overlap monocytes; use FCGR3B, CSF3R,
  and CXCR2 for discrimination.
- Liver sinusoidal endothelial cells may express little VWF. Confirm with CLEC4G and
  STAB2 rather than rejecting the identity from VWF alone.
