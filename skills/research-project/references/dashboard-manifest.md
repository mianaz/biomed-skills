# Static dashboard inventory

Use `scripts/render_dashboard.py` when a project needs a new static dashboard.
Keep an existing suitable HTML entry and update its own template instead.
The renderer reads a JSON file and writes an offline HTML page. It does not
modify source files, publish a site or synchronize an external service.

All local paths are relative to the **output HTML's directory**. Prefer relative
paths for portability. Paths can contain spaces and Unicode. Absolute local paths
become `file://` links; they suit a locally opened page. HTTP hosting requires
project-relative assets or usable remote URLs. External links are retained but
their availability is not checked by the renderer.

```json
{
  "title": "Project name",
  "updated": "2026-11-17",
  "question": "The biological question",
  "finding": "The latest interpreted result",
  "next_decision": "The useful decision or next action",
  "coverage": "All delivered outputs through the stated date; raw data linked from run records",
  "sources": [{"label": "Task and decision record", "href": "project.md"}],
  "tasks": [{
    "id": "T01", "title": "Compare the two model predictions",
    "status": "ready", "owner": "Researcher",
    "timing": "Proposed work block: 19 Nov, 09:00–11:00, America/Indiana/Indianapolis",
    "purpose": "Choose the first informative experiment",
    "dependency": "Pilot results available", "source": "project.md#t01"
  }],
  "artifacts": [{
    "id": "R01", "title": "Pilot result", "kind": "figure",
    "status": "current", "summary": "What this result shows",
    "path": "results/pilot.pdf", "thumbnail": "results/pilot-preview.png",
    "links": [
      {"label": "Data", "href": "results/pilot.csv"},
      {"label": "Code", "href": "analysis/pilot.R"},
      {"label": "Run", "href": "runs/run01.md"}
    ]
  }]
}
```

Required project fields are `title`, `updated`, `question`, `finding`,
`next_decision`, `coverage` and `artifacts`. Each artifact needs a unique `id`,
`title`, `kind`, `status`, `summary` and `path`; `thumbnail` and `links` are optional.
Use `current`, `draft`, `superseded` or `failed` for artifact status. `sources` and
`tasks` are optional; tasks use the fields in the example. Put a durable path or
an accession in the summary when the remote storage has no usable web link.
The renderer adds a directory link for local result files.

The default gallery shows current outputs. Status, type and text filters reveal
other versions; with JavaScript disabled all artifacts remain readable. Sources
and task records are linked rather than editable. If another system owns the
records, refresh this file as a dated snapshot of that system.

Before writing, the renderer checks local file targets and unique artifact IDs.
It overwrites only an HTML page carrying its own generator marker; an existing
manual page needs a deliberate edit or a separately named preview. After writing,
open the page and verify the display and representative destination contents.
