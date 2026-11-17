---
name: research-project
description: Organize a biomedical project's current question, priorities, tasks, calendar and result navigation. Use for project planning, weekly research review, 科研项目管理、待办排期 or creating/updating a top-level HTML research dashboard. Reuse existing task and experiment records.
---

# Research Project

Read [shared principles](../biomed-shared/core-principles.md).

Keep the next research decision and all project results easy to find. Read
[research principles](../biomed-shared/research-principles.md). For active project
management, inspect its root, dashboard, task board, experiment records and actual
outputs. For a planning-only request, work from the supplied records and constraints.
Establish the current question, strongest finding and next useful
outcome from those sources. Preserve manual priorities and agreed commitments.

## Choose the next work

Interpret new results before generating tasks: what was learned, what became
interesting, which explanation changed and what decision is now useful? Give
each research task a question or decision and a concrete deliverable. Logistics
tasks link to the experiment or milestone they enable.

Order executable tasks by scientific importance, information gained, dependency,
effort and real urgency. Address critical blockers before choosing easy work.
Keep promising exploration visible at a scale the user can afford. A compact
Now / Next / Later view is often enough. Use `research-ideation` for new directions
and `experiment-design` for the biological comparison behind a task.

Reuse the existing task system. If none exists, a short table needs only task ID,
question/purpose, action or output, owner, status, dependency, source link and
date when meaningful. Add an effort estimate or completion criterion where it
changes planning. Suggestions remain proposals until adopted; a user request
already supplies authority for the requested work.

## Make a feasible schedule

Separate genuine deadlines from preferred work dates and estimates. Inspect
existing availability before writing calendar events. Schedule backwards from
fixed milestones and resource bookings; include reagent lead time, specimen
availability, instrument slots and analysis time.

For bench work distinguish hands-on time, incubation/waiting and the full
elapsed span. Preserve linked time windows and source-supported stopping points.
Avoid placing simultaneous hands-on steps on the same person or instrument.
Use the user's timezone and leave a stated, adjustable capacity buffer.
An unscheduled task belongs in the task queue; the calendar holds a concrete
time commitment. Link both to the same task or run ID.
When an ELN calendar and notebook share records, use that same record for the
scheduled work. Keep an undated design in the queue until its dependencies are
ready. A multi-day treatment can need separate hands-on blocks and a fixed harvest
window; do not enter the full incubation span as operator effort.

A planning request can deliver a proposed calendar table or import file. When
the user requests live scheduling, use the available calendar tool, check
availability, write the authorized entries and verify them. Record external
event IDs to update them without duplication. A reminder, recurring review or
scheduled worker requires its own requested scheduling action; a written plan
does not establish that an automation exists.

For a calendar import, verify timezone, start/end, status and stable event IDs in
the exported file. A floating time needs an explicit interpretation before use
in another calendar. A successful file export is separate from an imported event.

## Maintain the root dashboard

When creating or updating project files, apply
[the dashboard contract](../biomed-shared/project-dashboard.md). Keep one
HTML entry at the project root and refresh it whenever project results are
delivered. It shows the scientific question, latest finding, next decision,
current work and a searchable gallery of results with their exact locations.

Reuse an existing root page. For a new static page, the optional renderer accepts
an explicit inventory; it does not crawl a drive or infer the preferred version:

```bash
python3 scripts/render_dashboard.py /path/to/project/dashboard.json \
  --output /path/to/project/index.html
```

Read [the manifest guide](references/dashboard-manifest.md) only when using this
renderer. It runs offline and links to the existing files. When another system
owns tasks and results, `dashboard.json` is a derived snapshot with source links.
For a simple file-based project it may be the one maintained project record.

## Review and deliver

At a requested weekly review, summarize discoveries, model changes, important
blockers and a small set of feasible next outcomes. Reconcile tasks with actual
outputs; preserve unfinished and deliberately deferred work. Task completion and
scientific support have separate meanings. Report progress as concrete findings
and delivered outputs; use percentages only with an agreed, visible denominator.

Deliver the requested plan or updated project records with the next useful action.
When a dashboard was created or updated, include its root HTML link; verify
representative figure, source-data, code, run-record and directory links, all local
inventory targets, search/filter behavior and desktop and narrow layouts.
