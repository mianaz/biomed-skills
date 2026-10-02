---
name: orchestrate-biomedical-work
description: Coordinate multi-step biomedical work across planning, domain execution, provenance, verification, and communication. Use when a request spans multiple skills or artifacts, benefits from delegation, requires independent review, or needs roles and safeguards scaled to scientific risk; also use to run the workflow safely when only one agent is available.
---

# Orchestrate Biomedical Work

Coordinate the work without taking ownership away from domain skills. Keep one lead
accountable for scope, user contact, adjudication, and final synthesis.

## Start from the contract

1. Read `.ai-scientist/current/analysis-contract.json`. If it is missing or the
   objective has materially changed, use `plan-biomedical-analysis` first.
2. Preserve all contract, question, unit, outcome, analysis-set, contrast, step,
   output, and check IDs.
3. Decompose the contract into artifact-bounded tasks. Give each task one objective,
   defined inputs, deliverables, decision rights, and acceptance checks.
4. Consult the suite registry when available. Match `scopes` and `stage`, use router
   `routes_to` entries for broad requests, and select the most specific applicable
   leaf skill. Treat `requires`, `recommends`, and `optional_capabilities` as distinct.
   Use
   `ensure-biomedical-reproducibility` for the run record and
   `verify-biomedical-analysis` for independent checking.

## Scale roles to risk

Use the contract assurance level, consequence of error, reversibility, novelty,
privacy constraints, and workflow length to choose the smallest safe arrangement.

| Situation | Arrangement |
|---|---|
| Contained, reversible, `basic` work | One capable worker may lead, execute, and self-check. Record that review was not independent. |
| Ordinary research or `standard` assurance | Lead plus domain executor; use an isolated verifier before reporting material scientific claims. |
| `strict`, high-consequence, novel, or fragile work | Lead plus the necessary specialists, an isolated verifier, and a fresh executor for corrections. Add a second independent judgment only for a defined unresolved decision. |

Do not create roles merely to appear rigorous. Add a role only when it contributes a
distinct capability, independent check, or context boundary.

## Select workers by capability

Match the task against observable needs rather than model or vendor names. A worker
may be an agent, analyst, clinician, laboratory operator, instrument workflow, or
versioned procedure; assign only decision rights it can legitimately exercise.

- domain and method expertise;
- input/output formats and existing analysis stack;
- access to required tools, documentation, compute, and protected data;
- ability to produce the required structured artifacts and deterministic checks;
- context capacity and independence from prior decisions.
- authority, training, approvals, and safe access required for human, clinical,
  laboratory, animal, hazardous-material, or protected-data work.

If no worker satisfies the task, narrow the assignment, change the method within the
contract's decision rights, or surface the blocker. Never hide a capability gap by
giving an unqualified worker a broader prompt.

## Issue a structured handoff

Write each assignment as a structured record under
`.ai-scientist/current/handoffs/<task_id>.json` or an equivalent project-controlled
location. Include at minimum:

```json
{
  "task_id": "task-id",
  "role": "executor",
  "actor_kind": "agent | human | instrument | procedure",
  "objective": "One bounded outcome",
  "contract_ids": ["q-primary", "primary-analysis"],
  "read_artifacts": [],
  "deliverables": [],
  "constraints": [],
  "decision_rights": [],
  "acceptance_checks": [],
  "escalate_when": [],
  "out_of_scope": []
}
```

Require the worker to return status, produced artifact paths, checks performed,
decisions and rationales, deviations, unresolved items, and a short handoff summary.
Reject prose-only completion when the task requires files, tables, code, or checks.

## Preserve verifier independence

- Use a fresh worker or context that did not author the result.
- Pass the contract, run manifest, declared outputs, claim-evidence mapping, and
  acceptance checks—not the executor's persuasive narrative or full conversation.
- Keep verification read-only. Run machine-checkable tests before interpretive review.
- Send accepted findings to a fresh executor for correction, then re-verify affected
  checks. Let the lead adjudicate disagreements from evidence.

When only one agent is available, perform separate artifact-based execution and review
passes, prioritize deterministic checks, and state that independence was unavailable.
For high-consequence work, do not present that fallback as equivalent to independent
verification.

## Use ensembles narrowly

Use independent repeated judgments only when the output is bounded, comparable, and
individually checkable, such as classification, relevance screening, candidate
ranking, or a discrete method choice. Give every worker the same rubric, prevent them
from seeing one another's answers, and report disagreement. Aggregate categorical
labels by vote, rankings by a stated rank method, or retain a consensus set when
precision matters.

Do not ensemble open-ended hypothesis generation, narrative writing, full analysis
pipelines, or multi-step statistical modeling. For those tasks, compare specific
decisions or independently verify shared artifacts instead.

## Close the loop

1. Confirm every required output and check in the contract has an owner and status.
2. Stop adding work when the questions are answered at the requested assurance level.
3. Route verified artifacts to `communicate-biomedical-results`.
4. Report unresolved failures, constraints, and non-independent checks explicitly.

Do not duplicate domain method rules, alter results to force consensus, or expand the
study with optional work that cannot change a claim or decision.
