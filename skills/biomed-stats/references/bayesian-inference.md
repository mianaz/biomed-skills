# Bayesian inference

Use when the question needs probability updating, a posterior distribution or a
model that combines prior knowledge with new data. A Bayesian framework still
needs the outcome model and dependence structure required by the study design.

## Choose the required quantity

| Question | Work needed |
|---|---|
| How does a test result change the probability of a condition? | Bayes' theorem using the target prevalence and the test likelihood |
| What effect sizes are plausible given data and prior information? | Likelihood, explicit prior, posterior estimation and sensitivity |
| What might a new subject's outcome be? | Posterior predictive distribution, including individual variation |
| How do linked variables support probabilistic inference? | A Bayesian network with justified conditional dependencies |

For a known-probability calculation, state the conditioning direction and base
rate. For repeated evidence, use the joint likelihood; multiplying separate
likelihoods requires the relevant conditional independence. The same information
must not enter twice through both the prior and the likelihood.

## Specify and assess the model

1. Define the estimand, likelihood, sampling units and dependence. Name parameters
   on their biological scales and state any transformations.
2. State each prior and its basis. Examine the outcomes and effects the priors
   imply; compare scientifically plausible alternatives when information is weak.
3. Compute the target posterior quantities with an established implementation.
   If sampling is needed, inspect convergence, mixing, effective sample size and
   relevant sampler diagnostics before interpreting the draws.
4. Check whether posterior predictions reproduce important features of the data.
   Assess sensitivity to consequential prior and likelihood choices.

Give the posterior estimate, credible level and interval definition, such as
equal-tail or highest-density. A credible interval is not always the shortest
interval. State a posterior probability only for a defined event, such as an effect
exceeding a biologically meaningful value. Specify the prior and likelihood that
make this interpretation possible.

For model or hypothesis comparison, posterior odds equal prior odds multiplied by
the Bayes factor. State all three when relevant. Comparing a point null needs a
specified model/prior that assigns it probability; a continuous posterior interval
containing zero does not itself supply that comparison. Verify the method and
prior sensitivity of marginal-likelihood calculations when using Bayes factors.

## Use networks for the intended interpretation

A Bayesian network represents a joint distribution through a directed acyclic
graph and conditional distributions. Distinguish a chain, a common cause and a
collider when reasoning about conditioning. A causal reading of arrows needs
causal assumptions and an appropriate design; use
[causal observational analysis](causal-observational.md) for that task. Dynamic
networks can represent feedback across time while the time-expanded graph is
acyclic. Retain the graph, conditional models and their scientific justification.

Deliver the model/prior specification, posterior summaries, predictive checks,
sensitivity and reproducible computation. Advanced hierarchical priors, sampling
or model comparison need current primary method and software documentation. The
diagnostic workflow above is a suite implementation requirement beyond the brief
introductory examples in these columns.

## Sources

- *Bayes' theorem*, pp. 277–278: [nmeth.3335](https://doi.org/10.1038/nmeth.3335).
- *Bayesian statistics*, pp. 377–378, with the 2015 likelihood-curve correction:
  [nmeth.3368](https://doi.org/10.1038/nmeth.3368).
- *Bayesian networks*, pp. 799–800: [nmeth.3550](https://doi.org/10.1038/nmeth.3550).
