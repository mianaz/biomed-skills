"""Conditional unweighted Gaussian fits for one design-valid dose series."""
import warnings
import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning
from scipy.special import expit
from scipy.stats import t


def log_logistic(dose, b, c, d, e, f=1):
    """LL2.4/LL2.5 form; e is a natural-log location, not generally log(ED50)."""
    return c + (d-c)*np.exp(-f*np.logaddexp(0, b*(np.log(dose)-e)))


def _jacobian(dose, b, c, d, e, f=1):
    u = np.log(dose)-e
    z = b*u
    log_term = np.logaddexp(0, z)
    q = np.exp(-f*log_term)
    common = (d-c)*q*f*expit(z)
    return np.column_stack((-common*u, 1-q, q, common*b, -(d-c)*q*log_term))


def relative_ed50(parameters):
    """Invert the fitted curve at (c+d)/2 and return ED50 plus its log gradient."""
    parameters = np.asarray(parameters, dtype=float)
    if parameters.ndim != 1 or len(parameters) not in (4, 5):
        raise ValueError("Supply four or five fitted LL2 parameters.")
    b, c, d, e = parameters[:4]
    f = parameters[4] if len(parameters) == 5 else 1.0
    if not np.isfinite(parameters).all() or b == 0 or f <= 0:
        raise ValueError("ED50 requires finite parameters, nonzero slope and positive asymmetry.")
    a = np.log(2)/f
    shift = a + np.log1p(-np.exp(-a)) if a > 50 else np.log(np.expm1(a))
    log_ed50 = e + shift/b
    gradient = [-shift/b**2, 0, 0, 1]
    if len(parameters) == 5:
        gradient.append(-np.log(2)/(b*f**2*(-np.expm1(-a))))
    with np.errstate(over="ignore", under="ignore"):
        return float(np.exp(log_ed50)), np.array(gradient)


def dose_response_candidates(dose, response, level=0.95):
    """Fit constant/4PL/5PL candidates; report all, without choosing a biological model."""
    dose, response = np.asarray(dose, dtype=float), np.asarray(response, dtype=float)
    if dose.ndim != 1 or response.shape != dose.shape or len(dose) < 2 or not np.isfinite(dose).all() or not np.isfinite(response).all() or (dose <= 0).any() or not 0 < level < 1:
        raise ValueError("Supply equal finite 1D series, positive doses, n > 1, and 0 < level < 1.")
    n = len(dose)
    mean = np.mean(response)
    models = {"constant": dict(parameters=np.array([mean]), covariance=np.array([[np.var(response, ddof=1)/n]]))}
    attempts = []
    direction = -1 if np.sum((np.log(dose)-np.log(dose).mean())*(response-mean)) > 0 else 1
    for family in ("4PL", "5PL"):
        starts = [[direction*slope, min(response), max(response), mid]
                  for slope in (1, 3) for mid in np.quantile(np.log(dose), [0.3, 0.7])]
        if family == "5PL":
            starts = [list(models["4PL"]["parameters"])+[f] for f in (0.5, 1, 2)] if "4PL" in models else [start+[1] for start in starts]
        best_rss = np.inf
        for start in starts:
            attempt = dict(model=family, start=start, converged=False, message="")
            if n < len(start):
                attempt["message"] = "Fewer records than fitted mean-response parameters"
                attempts.append(attempt)
                continue
            try:
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter("always", OptimizeWarning)
                    function = (lambda x, b, c, d, e: log_logistic(x, b, c, d, e)) if family == "4PL" else log_logistic
                    jac = (lambda x, b, c, d, e: _jacobian(x, b, c, d, e)[:, :4]) if family == "4PL" else _jacobian
                    bounds = (-np.inf, np.inf) if family == "4PL" else ([-np.inf]*4+[1e-8], [np.inf]*5)
                    cf, covariance = curve_fit(function, dose, response, p0=start, jac=jac,
                                               bounds=bounds, maxfev=15000)
                attempt["message"] = "; ".join(str(w.message) for w in caught)
                fitted = log_logistic(dose, *cf)
                rss = float(np.sum((response-fitted)**2))
                attempt.update(converged=bool(np.isfinite(cf).all() and np.isfinite(rss)), rss=rss)
                if attempt["converged"] and rss < best_rss:
                    models[family] = dict(parameters=cf, covariance=covariance)
                    best_rss = rss
            except (RuntimeError, ValueError, FloatingPointError) as error:
                attempt["message"] = str(error)
            attempts.append(attempt)
    comparison, parameters, predictions, residuals = [], [], [], []
    grid = np.geomspace(min(dose), max(dose), 150)
    for family in ("constant", "4PL", "5PL"):
        model = models.get(family)
        row = dict(model=family, n_records=n, n_doses=len(np.unique(dose)), converged=model is not None,
                   rss=np.nan, rmse=np.nan, aicc=np.nan, relative_ed50=np.nan, ed50_low=np.nan,
                   ed50_high=np.nan, midpoint_in_range=False, interval_in_range=False,
                   covariance_ok=False, covariance_condition=np.nan, note="No converged candidate; inspect attempts")
        if model is not None:
            cf, covariance = model["parameters"], model["covariance"]
            fitted = np.repeat(cf[0], n) if family == "constant" else log_logistic(dose, *cf)
            rss = float(np.sum((response-fitted)**2))
            k = len(cf)+1
            with np.errstate(divide="ignore"):
                aic = n*(np.log(2*np.pi)+1+np.log(rss/n))+2*k
            covariance_ok = bool(np.isfinite(covariance).all() and (np.diag(covariance) > 0).all() and np.linalg.eigvalsh(covariance).min() > 0)
            row.update(rss=rss, rmse=np.sqrt(rss/n), aicc=aic+2*k*(k+1)/(n-k-1) if n > k+1 else np.nan,
                       covariance_ok=covariance_ok,
                       note="Conditional assay-error approximation; inspect coverage, residuals and stability" if covariance_ok else "Unstable covariance; interval unavailable")
            se = np.sqrt(np.diag(covariance)) if covariance_ok else np.full(len(cf), np.nan)
            if covariance_ok:
                row["covariance_condition"] = np.linalg.cond(covariance/np.outer(se, se))
            critical = t.ppf((1+level)/2, n-len(cf)) if n > len(cf) else np.nan
            names = ["mean"] if family == "constant" else list("bcde") + (["f"] if family == "5PL" else [])
            parameters.extend(dict(model=family, parameter=name, estimate=value, se=error,
                                   low=value-critical*error, high=value+critical*error,
                                   interval_method="Wald-t in fitted parameterization; e is natural-log location")
                              for name, value, error in zip(names, cf, se))
            if family != "constant" and cf[0] != 0:
                ed50, gradient = relative_ed50(cf)
                row["relative_ed50"] = ed50
                if np.isfinite(ed50) and ed50 > 0:
                    if not np.isclose(log_logistic(ed50, *cf), (cf[1]+cf[2])/2, rtol=1e-5, atol=1e-5):
                        raise ValueError("Inverse-curve midpoint check failed.")
                    if covariance_ok:
                        variance = float(gradient @ covariance @ gradient)
                        if np.isfinite(variance) and variance >= 0 and np.isfinite(critical):
                            with np.errstate(over="ignore", under="ignore"):
                                row["ed50_low"], row["ed50_high"] = np.exp(np.log(ed50)+np.array([-1, 1])*critical*np.sqrt(variance))
                row["midpoint_in_range"] = bool(np.isfinite(ed50) and min(dose) <= ed50 <= max(dose))
                row["interval_in_range"] = bool(np.isfinite([row["ed50_low"], row["ed50_high"]]).all() and min(dose) <= row["ed50_low"] and row["ed50_high"] <= max(dose))
            values = np.repeat(cf[0], len(grid)) if family == "constant" else log_logistic(grid, *cf)
            errors = np.full(len(grid), np.nan)
            if covariance_ok:
                jac = np.ones((len(grid), 1)) if family == "constant" else _jacobian(grid, *cf)[:, :len(cf)]
                variance = np.einsum("ij,jk,ik->i", jac, covariance, jac)
                errors = critical*np.sqrt(np.maximum(variance, 0))
            predictions.extend(dict(model=family, dose=x, fitted=y, low=y-error, high=y+error)
                               for x, y, error in zip(grid, values, errors))
            residuals.extend(dict(model=family, dose=x, response=y, fitted=pred, residual=y-pred)
                             for x, y, pred in zip(dose, response, fitted))
        comparison.append(row)
    return dict(models=models, comparison=comparison, parameters=parameters, predictions=predictions,
                residuals=residuals, attempts=attempts,
                interval_method=f"{100*level:g}% pointwise conditional Gaussian mean-response CI; ED50 uses back-transformed log-Wald-t CI with analytic inverse-curve gradient")
