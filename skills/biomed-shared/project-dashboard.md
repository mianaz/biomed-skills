# Project root HTML dashboard

For research work conducted in a project, always keep one HTML entry at its top
level. Reuse the existing entry name and design; otherwise use `index.html`.
Identify the real project root from its records rather than treating each dated
analysis folder as a new project. A one-off answer without a project does not
need a new directory tree.

## What the entry must make easy

- Understand the question, latest finding, unresolved decision and next action.
- Browse all delivered results and figures, grouped by question or analysis,
  with a readable preview when the format allows it.
- Open each result, its direct source data, analysis/plotting code or native
  project, and the relevant run/method record. Show exact paths and a directory
  link for locating files. Label unavailable or remote locations accurately.
- Distinguish current, draft, superseded and failed work. Retain old versions
  through an archive view. Choose the current version from project decisions;
  a newer modification time alone does not establish that choice.
- Reach the literature map, experiment plan, task board, calendar, protocol and
  inventory at their existing locations. Display the snapshot date and sources.

The result inventory defines coverage. Include each delivered result or link to
a complete child gallery with its scope. State what is included; preserve gaps
when the inventory is partial. Search and filters help larger galleries, while a
small project can use a compact list. Keep thumbnails separate from originals so
viewing the page does not require loading every full-resolution image.

## Keep the view dependable

Generate or update the page from the authoritative records. When a task board or
ELN already exists, avoid maintaining a second editable queue in HTML. Show
links back to those sources and refresh the snapshot after relevant work.
Update the root entry as part of delivering a result, without requiring a separate
dashboard request. Preserve manual sections and unrelated project content.
Use stable artifact and run IDs across manuscript renumbering; retain current
display labels and historical file labels as aliases. If a source app has no
record-level URL or clickable file links, show a local linked record plus its
searchable ID and app entry. Test the actual destination before calling a link a
direct record link.

For an ELN-derived snapshot, export after a representative edit, match the same
record IDs and regenerate the view. Keep the export time visible. Do not import
an older snapshot over newer notebook edits merely to refresh the dashboard.

Prefer a static, offline-readable page with relative local links. HTTP-served pages
cannot reliably open `file://` targets; use project-relative assets, established
remote links or a displayed path in that mode. Do not imply that a web link can
open Finder. Public sharing requires a deliberately prepared shareable copy.

Verify local links, preview images, version labels and search/filter behavior.
Include stable IDs in search where records use them. For a known unavailable
legacy target, preserve its location and label its availability without promoting
a different file to the accepted version. Keep newly delivered links usable.
Open the page and inspect readable text at normal desktop and narrow widths.
The optional `research-project` renderer supports a compact explicit inventory;
other existing project templates can satisfy this same contract.
