# Evaluate method and source evidence

Assess relevance, transparency, validation, and implementation separately. Do not
collapse quality to a journal, citation count, or one score.

## Method evidence

- Is the method central to the study and intended use?
- Are population/system, units, acquisition, inputs, preprocessing, parameters,
  versions, controls, exclusions, and analysis sets recoverable?
- Were alternatives compared on representative data with leakage-safe design?
- Are uncertainty, dependence, missingness, multiplicity, and negative results handled?
- Is validation internal, external, orthogonal, interventional, prospective, or only
  apparent on the development data?
- Can code, protocol, or instrument settings be mapped to reported outputs?
- Which failure cases, subgroup limits, or operational constraints are visible?

## Source status

Check version of record, corrections, expressions of concern, retractions, protocol
or registration, supplement, analysis plan, data dictionary, data availability, and
repository license. Record inaccessible sources and the consequence for confidence.

## Code and procedural coverage

Classify implementation as:

- `complete`: acquisition/inputs through analysis and reported output are recoverable;
- `analysis-only`: numerical analysis is recoverable but acquisition or output code is absent;
- `procedure-only`: protocol/SOP is recoverable but computational processing is absent;
- `partial`: only selected stages, cohorts, experiments, or figures are recoverable;
- `interface-only`: a package or device interface exists without study configuration;
- `unavailable`.

Pin repository commit, environment, entry points, licenses, model weights, protocol
version, instrument/software version, and exact locators. Label reconstructed material
and validate it before proposing promotion.
