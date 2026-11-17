---
name: experiment-design
description: Turn a biomedical question or working model into informative experiments, controls, predicted outcomes and a feasible first pilot. Use for 实验设计、验证方案 or choosing decisive follow-up experiments. Biomed-stats owns allocation, sample size and statistical analysis; paper-to-protocol owns sourced procedural steps.
---

# Experiment Design

Read [shared principles](../biomed-shared/core-principles.md).

Read [research principles](../biomed-shared/research-principles.md). Reuse the
question, evidence, model and existing experiment IDs. Begin with the biological
decision and the user's actual material, time and equipment constraints.

## Choose the comparison

Write the question and what each plausible model predicts. Select a comparison
that separates those predictions. A short outcome table often reveals a missing
control before any work begins. Specify the biological system, intervention,
comparison, measurement, time point and analysis target.
When connecting existing assays, retain their actual run, sample and treatment
relationships. Use a matched follow-up where those conditions need to be joined.
Inspect existing dose-response or assay-range data before carrying a historical
dose into the new comparison.

Choose controls for the inference: baseline, assay competence, intervention
delivery, specificity or an orthogonal readout, as appropriate. Reuse completed
experiments. Develop a rescue or independent perturbation when it answers a real
alternative explanation; justify the needed control through the decision.
For an exploratory screen, define the search space, selection rule and follow-up
comparison without inventing a fully resolved mechanism.

## Make it executable

- Identify the experimental and sampling units, independent replication,
  pairing, batches and repeated measurements. Use `biomed-stats` for allocation,
  randomization/blocking, blinding, sample-size scenarios, contrasts and analysis.
  Keep that plan attached to this experiment rather than copy it into two records.
- Name the primary readout, relevant secondary readouts and meaningful effect.
  Distinguish assay qualification from testing the biological model.
- Link a protocol and version, required samples and reagent lots, equipment,
  operator availability and lead times. Use `paper-to-protocol` when source
  Methods must become a procedure. Critical quantities and safe stopping points
  must come from a source or an explicit proposed adaptation.
- Plan a small pilot when assay range, variance, timing or feasibility is unknown.
  State what the pilot will establish and what decision follows. Where useful,
  rehearse the planned analysis on a labeled mock dataset with the real nesting
  and missingness structure; use R and the statistics workflow.

## Plan the interpretation

Before execution, describe informative positive, contrary, mixed and technically
uninterpretable outcomes. Connect each to the model and next decision. A failed
positive control changes the assay decision; a technically valid contrary result
changes the biological interpretation. Define practical continue, adapt or stop
criteria where they help the project.

Rank the proposed experiments by the importance of the question, information
gained, dependencies and cost/time. Give a clear first action and explain which
experiments can wait. Use [the planning sheet](assets/experiment-plan.md) for a
whole plan; a local follow-up question can use a compact table.

Deliver a usable plan with source links, chosen comparisons, controls, readouts,
resource needs and outcome implications. Link it from the
[root dashboard](../biomed-shared/project-dashboard.md). `research-project` owns
the work schedule; `lab-records` owns what actually happened during each run.
