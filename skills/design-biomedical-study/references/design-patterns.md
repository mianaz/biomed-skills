# Design patterns

Choose the simplest design that identifies the target quantity under realistic
operations. State what remains unidentifiable.

## Experimental designs

| Design | Use when | Protect against | Key limitation |
|---|---|---|---|
| Parallel randomized | Independent units can receive one condition | Measured and unmeasured baseline imbalance | Requires allocation at the true independent unit |
| Blocked or stratified | A known factor strongly affects outcome | Imbalance across batch, sex, site, plate, or baseline severity | Blocks must enter analysis and not become tiny fragments |
| Factorial | Two or more interventions and interaction matter | Separate experiments that cannot estimate interaction | Power for interaction is often lower than for main effects |
| Fractional factorial or screening | Many factors must be screened with limited runs | One-factor-at-a-time inefficiency | Effects are aliased; state the design resolution and alias structure |
| Response surface | The goal is optimization and curvature is plausible | Missing an interior optimum with only low/high settings | Requires a supported operating region and enough center/axial information |
| Crossover | Effects are reversible and carryover is controllable | Stable between-unit heterogeneity | Period, sequence, washout, and carryover must be modeled |
| Cluster randomized | Intervention is delivered to groups | Contamination between members | Effective sample size follows clusters, not members |
| Repeated measures | Change within a unit is informative | Stable unit-level heterogeneity | Repeated observations are dependent, not extra replicates |
| Split-plot or multistage | Some factors can only be randomized to large units | Pretending every factor has the same randomization unit | Whole-plot and subplot errors must remain distinct |
| Latin-square or order-balanced | Two nuisance axes or treatment order must be balanced | Confounding with row, column, period, or sequence | Assumes the planned balance is operationally achievable |
| Sequential or adaptive | Accrual can be monitored and decisions may change prospectively | Unplanned repeated looks or wasteful fixed sampling | Adaptation, error control, information timing, and stopping rules must be prespecified |
| Space-filling | A continuous experimental or simulation region must be explored | Sparse coverage of multidimensional settings | Supports exploration, not automatic causal identification |

For laboratory work, randomize treatment and measurement order when possible. Balance
conditions across plates, days, operators, litters, cages, instruments, and acquisition
runs rather than assigning condition to batch.

For factorial and optimization work, define factors in operational units, admissible
ranges, prohibited combinations, center points, replication, run-order randomization,
and the effects or interactions that must be estimable. A fractional design is not
interpretable until its generators, resolution, and alias structure are recorded.
When randomization occurs at more than one level, carry every randomization unit into
the analysis model. For sequential or adaptive work, lock the adaptation rule,
information schedule, error-spending or decision criterion, and operational firewall
before observing comparative outcomes.

## Observational designs

- **Prospective cohort:** define eligibility and time zero before outcomes occur.
- **Retrospective cohort:** reconstruct a common eligibility, assignment, and follow-up
  origin; avoid immortal time and future information.
- **Case-control:** sample from a defined source population and use an analysis
  compatible with the sampling scheme.
- **Cross-sectional:** estimate prevalence or association at one period; do not infer
  temporal order by habit.

Name exposure, comparator, outcome, confounders, mediators, and post-exposure variables
before modeling. A larger adjustment set is not automatically less biased.

## Diagnostic and method-comparison designs

Define the index test, intended population, reference standard, reader or operator,
time interval, positivity threshold, and handling of indeterminate results. Apply the
reference standard without knowledge of the index test when feasible. Avoid spectrum,
partial-verification, differential-verification, and incorporation bias.

For method comparison, span the intended measurement range, include replicates needed
to estimate repeatability, and distinguish agreement from correlation.

## Prediction-model studies

Separate model development, internal validation, external validation, and prospective
impact evaluation. Choose split boundaries from deployment: participant, site, time,
family, device, or batch. All preprocessing and feature selection belong inside the
training resample.

## Pilots

Use a pilot to assess feasibility, variability, recruitment, process failure, or
measurement performance. Do not treat a small pilot as a definitive efficacy study or
use its unstable observed effect as the sole confirmatory sample-size assumption.
