# Worked examples

Read an example when a concrete input-to-result walkthrough would clarify the
method choice. These are constructed teaching data, separate from article examples
or research results. They do not set default sample sizes or error thresholds.

Open the [HTML walkthrough](../examples/index.html) to select a case and expand
its inputs, decisions, results and code.

| Task | Example | Choice illustrated |
|---|---|---|
| Analyze | Six donors, two matched conditions, three technical wells per condition | Equal-weight donor summaries and a paired mean contrast; retain n = 6 pairs |
| Plan | Meaningful paired effect 5 percentage points, difference SD 8, alpha 0.05, power 0.8 | Prospective power in pairs, feasible rounding and uncertainty in planning assumptions |
| Review | 1,000 held-out units, 10 positives; fixed predictions versus an all-negative baseline | Match metrics to purpose, retain denominators and report sensitivity/PPV uncertainty |

Run from the package root:

```sh
Rscript skills/biomed-stats/examples/run.R
```

The [script](../examples/run.R) uses base R/stats and generates the constructed
observation tables, analysis summaries, full-precision CSV results, fitted/test
objects, session information and the HTML page. `report-template.html` holds its
presentation. Adapt the scientific design and assumptions before reusing code.

For the paired example, the independent donors and roughly suitable difference
model are explicit assumptions. Technical wells come from the same preparation
with equal precision. Inspect the donor differences and leave-one-donor-out
summary; normality is not established by a small-sample test. The power scenario
is specified independently of the completed paired example. The classifier
example evaluates fixed, constructed predictions; no model training is claimed.

The calculations were executed in R. This verifies these examples, not autonomous
agent behavior across all methods. The broader manual routing cases retain their
separate status.
