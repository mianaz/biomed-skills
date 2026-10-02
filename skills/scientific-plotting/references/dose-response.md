# Fit concentration-response data

Use this path for pharmacologic dilution/dose series. A smooth curve alone is not
an analysis. Fit the response, diagnose the fit, and retain the numerical results.
Time courses, arbitrary ordered categories and clearly nonmonotonic responses do
not automatically call for logistic models.

## Fit and select

- Start with a four-parameter logistic (4PL): two plateaus, slope and midpoint.
  Consider asymmetric 5PL when transition and plateau coverage can identify the
  additional parameter. Compare it with 4PL, rather than always choosing 5PL.
- Retain actual concentration units and spacing. Plot positive doses on a log axis;
  handle vehicle/zero separately. Do not log already log-transformed concentrations.
  Fit individual observations with the known experiment/plate/unit structure.
- Do not fix plateaus to 0 and 100 merely because the response was normalized.
  Fix a parameter only with a control or assay justification and assess sensitivity.
  For bounded/ordinal outcomes, choose an appropriate likelihood or identify an
  empirical mean-response fit and check its predictions against the outcome support.
- Compare candidate models on identical observations, weights and error likelihood.
  Include a constant-response model when the curve may be flat. AICc includes the
  residual-variance parameter for Gaussian fits; it is undefined if n <= k + 1.
  Report close alternatives. A small AICc advantage does not establish identifiability.
- Check convergence from plausible alternative starts, residuals by dose/fitted
  response, heteroscedasticity, parameter covariance, boundary estimates and plateau
  coverage. A nested 5PL candidate should include the converged 4PL solution with
  asymmetry = 1 as a starting point. R-squared alone cannot validate the model.
  Filter by the optimizer's convergence status before ranking attempts; an `nls`
  object returned with `warnOnly = TRUE` can still be a failed fit. Keep attempt
  identities aligned when filtering. Numerical parameter bounds and a midpoint
  inside tested doses do not establish identifiability; flag boundary estimates and
  do not give them ordinary interior-solution confidence intervals.

Prefer an established engine such as `drc` or Prism over rebuilding a bounded
nonlinear optimizer for each figure. In R, inspect installed help and use the
log-midpoint parameterization when computing back-transformed intervals:

```r
source("<skill-directory>/scripts/dose_response.R")
# One series, after design-specific QC; finite observations and positive doses.
fit <- dose_response_candidates(d$dose, d$response)
fit$comparison   # constant / 4PL / 5PL, AICc, RMSE, relative ED50 and log-Wald CI
fit$parameters   # plateaus, slope, log-location, asymmetry and parameter intervals
saveRDS(fit, "output/dose_models.rds")
```

For an ordinary unweighted continuous-response series, use this helper as the
starting fit. It uses installed `drc`, keeps multiple starts and rejected candidates,
verifies midpoint arithmetic, and exports unchanged confidence limits in the returned
tables. It does not choose biological units, certify identifiability or select a
final model. Read its comparison and attempt diagnostics; retain its tables, model
objects, predictions and residuals. For weights, hierarchical/bounded likelihoods,
shared-control joint fits or profile/cluster intervals, use the appropriate engine
directly and explain the departure. The helper's intervals are approximations.

Python has a native SciPy route in `scripts/dose_response.py`, with the same
constant/4PL/5PL candidate families and relative ED50 definition:

```python
from dose_response import dose_response_candidates
import pandas as pd

# One identifiable experiment/compound/model series; finite positive doses.
fit = dose_response_candidates(d["dose"], d["response"])
for name in ("comparison", "parameters", "predictions", "residuals", "attempts"):
    pd.DataFrame(fit[name]).to_csv(f"output/dose_{name}.csv", index=False)
```

Import from the assigned skill's scripts directory as in `r-and-python.md`.
The Python helper uses multistart `scipy.optimize.curve_fit`, analytic Jacobians,
Gaussian AICc including residual variance, and conditional log-Wald-t ED50
intervals. Keep the script, fitted parameters/covariance and package versions.
R and Python use different optimizers; numerical equivalence is not assumed.
Both helpers currently accept finite positive doses only: preserve zero-dose
controls in the data/display and describe their exclusion from these fits, or use
an engine that supports the intended joint model. Neither helper pools experiment
IDs or chooses the experimental unit; split by the full design before calling.
Boundary solutions and poorly identified asymmetry require an explicit diagnostic
decision before reporting intervals.

Save the 4PL/5PL comparison, or a specific reason that the 5PL candidate cannot be
identified. Do not silently omit that decision. Retain rejected model diagnostics.

In `drc`, 5PL is `c + (d-c)/(1 + exp(b*(log(x)-loge)))^f`.
For `LL2.5`, the fourth parameter is `loge`. The relative half-response dose is
`exp(loge) * (2^(1/f) - 1)^(1/b)`, not simply `exp(loge)` when f differs from 1.
Invert the fitted curve and verify that its prediction at the reported relative
ED50 equals `(c+d)/2`. Software parameterizations and slope signs differ.
The helper propagates covariance through the analytic gradient of log(ED50), checked
against central finite differences. The installed `drc` 3.0-1 has an incorrect
asymmetry derivative in its `LL2.5` effective-dose routine, so its 5PL `ED()` intervals
must not be used as an unchecked reference. This finding concerns that interval
routine; it does not invalidate all `drc` fits or establish a problem in Prism.

## Quantify what is estimable

Report EC50/IC50/ED50 with units and a definition: relative half-change between
fitted plateaus differs from reaching an absolute 50% of control. For 5PL, the
location parameter need not be either quantity. Report both plateaus, slope,
asymmetry when used, and confidence intervals with the method and confidence level.
Prefer profile-based or design-respecting bootstrap intervals for nonlinear potency;
if using approximate log-Wald intervals, name that approximation. Do not exponentiate
a standard error as if it were an interval or silently substitute a symmetric dose CI.
Do not clip confidence limits to zero or the outcome maximum and still label them
as the original model's CI. Use a justified bounded model or preserve and explain
the model interval; plotting limits must not silently change the reported uncertainty.

Distinguish a mean-response confidence band from a new-observation prediction band.
Resample independent experiments/units when their identities are known. With missing
unit hierarchy, an empirical fit and conditional assay-error uncertainty remain
possible; label the assumed error model and do not call the records independent
biological replicates. Unknown dependence limits both CI and model-selection evidence.

Flat responses, partial transitions, unstable asymmetry and unbounded intervals are
results. Keep their observations and fit diagnostics; mark potency not estimable or
report a justified bound. An estimated midpoint outside tested support is not a
measured potency. Do not force a finite CI, hide failed fits, or turn a parameter's
test against zero into a comparison between drugs.

Decide curve support separately from potency identifiability. If a converged 4PL
describes a transition but its parameter covariance or ED50 interval is unstable,
retain the empirical fitted shape with its limitation, or show observations without
a claimed fitted shape. Do not replace it with a flat line solely because ED50 is
unresolved. Choose a constant response from model/data evidence; its selection is
not proof of no dose effect. A tiny AICc difference deserves an explicit near-tie note.

For a supported curve comparison, name the estimand: relative potency, plateau,
slope or full curve. Use joint shared-versus-separate parameter models (for example
an extra-sum-of-squares F test under its assumptions), or compare independent
experiment-level log potencies. Preserve pairing/shared controls and define the
multiplicity family. Share parameters only with scientific justification.

## Plot and deliver

Show observations with supported fitted curves over each compound's tested range;
use confidence bands when estimable and readable. Do not substitute an ordinary
line joining dose means for the fitted model. Put a concise potency estimate and
95% CI beside its identified curve or in a compact keyed table in the delivered
figure set. A CSV alone does not make the estimate visible to the reader. Use an
unavailable-estimate label when needed; keep the full fit table outside the data
area. Keep model comparisons and statistical annotations
attached to the correct outcome and compound. A curve P value is not a bracket
between two arbitrary doses. Avoid large blocks of fit diagnostics over the plot.

Save source data, model objects, candidate comparison, parameters and intervals,
predictions, residuals, exclusions, software versions and a caption defining the
error model and uncertainty. Preserve unavailable estimates as such in the table.
Fit once and save these results before plotting. During layout-only revisions,
load the saved models/tables instead of repeating every nonlinear optimization.

Primary references: [Prism model choice](https://www.graphpad.com/guides/prism/latest/curve-fitting/reg_choosing_a_dr_equation.htm),
[Prism asymmetric dose response](https://www.graphpad.com/guides/prism/latest/curve-fitting/reg_asymmetric_dose_response_ec_2.htm),
[drc 5PL](https://doseresponse.github.io/drc/reference/LL.5.html),
[drc effective-dose intervals](https://doseresponse.github.io/drc/reference/ED.drc.html),
[Prism curve comparison](https://www.graphpad.com/guides/prism/latest/curve-fitting/reg_example_global_nonlin.htm).
