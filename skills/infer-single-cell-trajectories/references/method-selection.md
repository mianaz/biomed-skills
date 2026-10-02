# Trajectory method selection and failure checks

## Select by target output

| Need | Suitable family | Required support | Common failure |
|---|---|---|---|
| Coarse connectivity/topology | PAGA or graph abstraction | Stable neighborhood graph and meaningful groups | Reading an edge as direction or ancestry |
| Relative order in one continuum | Diffusion pseudotime | Connected lineage and justified root | Root inversion; disconnected cells forced into one path |
| Smooth one/multiple lineages | Slingshot | Credible clusters and reduced space | Curves depend on cluster labels or distorted embedding |
| Learned principal graph | Monocle3 | Coherent partitions and defensible roots | Overbranching or graph fit to technical structure |
| RNA direction/latent time | scVelo steady-state or dynamical models | Compatible spliced/unspliced layers and kinetic diagnostics | Violated kinetics, low counts, boundary artifacts |
| Fate probabilities | CellRank | Credible transition kernel and terminal states | Precise-looking probabilities from weak upstream dynamics |

Do not choose a method from the desired picture. Decide what inferential object is
needed, then ask whether the data satisfy its assumptions.

## Separate topology, ordering, and direction

- A neighborhood graph estimates similarity.
- A topology method proposes connections or branches.
- Pseudotime orders cells after a root/orientation choice.
- Velocity estimates local direction under an RNA kinetic model.
- Fate models propagate a transition kernel toward specified or inferred endpoints.

These outputs can disagree without one being a software error. Report the disagreement
and identify which assumptions differ.

## Validate the lineage subset

- Remove or explicitly model doublets, obvious outliers, and unrelated compartments.
- Check that samples and donors populate the path rather than occupying separate
  segments that mimic progression.
- Compare known stage/time metadata without using it as circular proof when it was
  used to build the trajectory.
- Confirm that branch-defining states have adequate support across biological units.
- Avoid fitting on an aggressively integrated representation without checking that
  biological progression and local neighborhoods were preserved.

## Validate roots, branches, and terminal states

- Define roots from external knowledge or observed time and repeat with other
  defensible roots.
- Refit after cell/feature subsampling and reasonable graph changes. Summarize branch
  recurrence and rank-order stability.
- Inspect whether terminal states are boundary populations with expected markers,
  observed later time points, or tracing/perturbation support.
- Do not use the same markers both to force an endpoint and then claim those markers
  independently validate it.

## Validate RNA velocity and fate

- Confirm spliced/unspliced layers, gene identifiers, and cells remain aligned.
- Inspect informative genes rather than relying only on arrows over UMAP.
- Check velocity confidence, consistency across donors, and sensitivity to gene
  filters/model mode.
- Treat arrows at sparse boundaries, isolated clusters, or low-count cells with
  particular caution.
- For CellRank, report the kernel components, terminal states, macrostates, and
  sensitivity of fate rankings to reasonable kernel weights and endpoints.

## Topology-faithful display

A PAGA-initialized force-directed graph can display branching topology more faithfully
than UMAP when UMAP tears or merges branches. It is a visualization of the fitted graph,
not new lineage evidence. Keep the PAGA graph and initialization explicit, preserve the
same node identities across panels, and route export/source-data rules to
`create-scientific-figures`.

## Report limits

Use language such as “cells were ordered along a model-inferred continuum,” “the data
support a candidate branch,” or “transition probabilities favored state X under this
kernel.” Reserve developmental ancestry or causal fate claims for independent lineage,
time-series, or perturbational evidence.
