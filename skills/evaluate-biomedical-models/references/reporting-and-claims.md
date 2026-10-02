# Model evaluation reporting and claims

## Required artifacts

- frozen model identifier, code revision, weights/checksum, and dependencies;
- intended-use statement and eligibility flow;
- unit hierarchy and split membership with leakage audit;
- outcome/reference definition and blinded adjudication status;
- preprocessing, missingness, unevaluable cases, and data exclusions;
- prediction table linked safely to outcomes and subgroups;
- primary and secondary metrics with denominator and uncertainty;
- calibration source data and threshold-performance table;
- baseline/model comparisons on the same analysis set;
- site, time, subgroup, and distribution-shift results;
- deviations and all post hoc analyses labeled.

## Claim boundaries

Use “internally validated,” “externally validated in…,” or “prospectively evaluated”
only when the design matches. Avoid “generalizable” from one convenience cohort,
“clinically useful” without a decision analysis or impact study, and “unbiased” from
resampling alone.

A nonsignificant difference between models does not establish equivalence. A higher
AUROC does not guarantee better calibration, threshold performance, or utility. A
subgroup result without adequate support is exploratory, whether favorable or adverse.

## Completion gate

Require one canonical evaluation population and prediction table, no unresolved split
leakage, exact metric definitions, denominators, uncertainty, missing-prediction
accounting, calibration, intended comparator, and bounded transportability claim.
