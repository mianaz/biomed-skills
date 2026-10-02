---
name: plan-biomedical-analysis
description: Turn an ambiguous biomedical research request into a compact, executable JSON analysis contract covering objectives, questions, nested study units, outcomes, analysis sets, governance risks, inputs, planned steps, outputs, validation, constraints, audiences, and operating profile. Use before starting a new analysis, revising a study plan, translating a broad prompt into a testable specification, or handing work to a domain-analysis skill or executor.
---

# Plan Biomedical Analysis

Create `.ai-scientist/current/analysis-contract.json` before execution. Keep the
contract short enough to inspect, precise enough to execute, and independent of any
agent vendor.

## Build the contract

1. Inspect the request, available metadata, prior decisions, and practical limits.
2. Rewrite the objective as one decision or knowledge gap.
3. Split broad aims into answerable questions with observable outcomes.
4. Define the unit hierarchy, primary analysis unit, outcomes, analysis sets,
   factors, contrasts, covariates, pairing, and known confounders. Mark missing
   information explicitly.
5. Screen human-subject, animal, sensitive-data, and hazardous-material risks.
   Record known approvals and operating restrictions; never infer clearance.
6. Choose the operating profile from scientific risk, reversibility, novelty, and
   reproducibility needs.
7. Define each planned step by purpose. Fix a method only when already justified;
   otherwise write a selection rule and defer the choice to the relevant domain
   skill.
8. Tie every required output and validation criterion to a question or material
   risk.
9. Record resource, data, policy, timing, and user constraints. Plan around the data
   that can realistically be obtained.
10. Add domain-specific configuration only under a named `extensions.profiles`
    entry; let the owning domain pack validate its contents.
11. Create the JSON from `assets/analysis-contract.json` and follow
   `references/analysis-contract.schema.json`.
12. Validate the result before handoff.

```bash
python3 scripts/validate_analysis_contract.py \
  .ai-scientist/current/analysis-contract.json
```

## Choose the profile

- Use `exploratory` analysis mode for discovery. Allow documented best-practice
  choices and label conclusions as exploratory.
- Use `confirmatory` analysis mode when contrasts, endpoints, or claims are
  prespecified. Require deviations to be recorded downstream.
- Use `basic` assurance for low-risk orientation, `standard` for ordinary research,
  and `strict` for high-risk, archival, regulated, or exact-rerun work.
- Use `autonomous` when reasonable defaults are safe, `collaborative` when a few
  scientific choices benefit from user input, and `approval_required` only when a
  choice is consequential or hard to reverse.

Read `references/analysis-contract.md` when choosing profiles, operationalizing a
broad question, or deciding what belongs in the contract.

## Resolve uncertainty

- Ask only questions whose answers materially change the design or interpretation.
- Infer reversible details from field practice, record the assumption, and continue.
- Respect defensible user preferences; challenge contradictions with the objective,
  data, or accepted design constraints.
- Distinguish facts, preferences, assumptions, unresolved decisions, and unavailable
  resources.
- Prefer a narrow question answerable by current data over an undefined claim such
  as "better," "important," or "similar."

## Hand off

- Pass the validated contract to the selected domain skill or executor.
- Preserve `contract_id`, question IDs, step IDs, output IDs, contrast IDs, and check
  IDs in downstream artifacts.
- Revise the contract only for an intentional scope change; record execution-time
  departures in the run manifest instead.

## Keep boundaries

- Do not execute the analysis in this skill.
- Do not duplicate domain-specific QC or method-selection rules.
- Do not add provenance, package capture, plotting style, scheduler policy, result
  interpretation, or independent verification.
- Do not treat the governance screen as ethics, privacy, biosafety, or regulatory
  approval.
- Do not expand the plan with optional analyses that lack decision value.

## Resources

Resolve all resource paths relative to this skill directory.

- `assets/analysis-contract.json`: valid starter artifact.
- `references/analysis-contract.md`: planning and field guidance.
- `references/analysis-contract.schema.json`: canonical JSON Schema.
- `scripts/validate_analysis_contract.py`: dependency-free validator.
