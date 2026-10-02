# Units, endpoints, and precision

## Define the unit hierarchy

Assign each level one or more roles:

- **sampling unit:** selected from the target population or system;
- **allocation unit:** receives intervention or exposure assignment;
- **independent unit:** contributes independent information for the primary effect;
- **measurement unit:** produces one observation;
- **analysis unit:** enters the model after valid aggregation or dependence modeling.

Examples include participant → visit → lesion → image, animal → organ → section →
field, donor → specimen → aliquot → well, and independent experiment → plate → well.
Technical repetition improves measurement precision but does not increase biological
or participant-level replication.

Record nesting, crossing, pairing, clustering, repeated time, and shared controls.
Plan analysis and sample size using the dependence structure, not the number of rows.

## Specify endpoints

For every endpoint record:

- construct and operational definition;
- unit, scale, direction, timing, and aggregation;
- acquisition instrument or assessor;
- reference standard, calibration, or validation evidence;
- handling of values below/above detection, indeterminate results, death, dropout,
  missing visits, or competing events;
- primary, key secondary, exploratory, safety, or process role.

Use one primary endpoint or a prespecified multiplicity strategy. A convenient
surrogate is not a patient-relevant outcome unless its relationship is justified for
the intended decision.

## Plan sample size or precision

Base calculations on the planned estimand and model. Include the expected effect or
target interval width, variability, event/prevalence rate, allocation ratio,
clustering or repeated-measure correlation, attrition, exclusions, multiplicity, and
model degrees of freedom.

Report a sensitivity grid rather than one fragile number. Show how sample size changes
under plausible event rates, variances, intraclass correlations, and losses. Use
simulation when closed-form approximations do not reflect the design.

When resources set a fixed maximum, invert the question: report the detectable effect
or attainable precision and which claims remain feasible. For a pilot, size the
feasibility parameter—such as recruitment, failure rate, or variance precision—not a
confirmatory treatment claim.
