# Labmate Notebook and Calendar

Use this for experiment-record imports and project snapshots. The protocol import
is documented separately in `paper-to-protocol`. Verified against the live
Labmate v2.2.0 UI and [source](https://github.com/mianaz/labmate) on 2026-11-17;
recheck the relevant source when the app changes.

## Import only the intended records

Notebook → Import JSON accepts `{ "exportedAt": "ISO timestamp",
"type": "experiments", "data": [records] }` or a record array. It upserts by
`id`: the same ID replaces its existing record. Inspect/export existing records
before an update; a new pilot uses distinct IDs. The Guide backup importer uses a
different envelope and can also modify settings, protocols and inventory.

The [record source](https://github.com/mianaz/labmate/blob/main/src/lib/experiments.js)
defines these useful fields:

| Field | Mapping |
|---|---|
| `id`, `title`, `titleZh` | Stable task/run ID; include the ID in a visible title for search |
| `date`, `startTime`, `duration` | Local `YYYY-MM-DD`, `HH:mm`, minutes; use empty date/time and zero duration for an undated design |
| `status`, `priority` | `planned` / `in-progress` / `completed` / `cancelled`; `high` / `medium` / `low` |
| `protocolRef` | An actual Labmate protocol ID, or null |
| `plan` | `objectives`, `notes`: question, design ID, owner, dependencies, timezone and source locations |
| `materials` | `reagents`, `equipment`, `plateLayout`, `checklist`; preserve unknown stock and lot values |
| `procedure` | `mode`, `protocolSteps`, `freeText`; actual execution or clearly labeled plan |
| `results` | `summary`, `dataProcessing`, `figures`, `backupStatus` |
| `createdAt`, `updatedAt` | Millisecond timestamps for record creation/editing; acquisition date is separate |

Use the current empty-record shape for nested arrays. Reagent `amount` is a
quantity, not a concentration field. Put treatment concentration/time in the
procedure or linked protocol. An undated design remains visible in Notebook and
does not appear as a scheduled calendar event.

## Verify the shared record

Notebook → View in calendar and Calendar → Open in Notebook refer to the same
record. Test one authorized edit, then check the ID, status, time and retained
content in the other view and in a fresh Notebook JSON export. Updating a field
on screen alone does not prove it was saved. Keep the fresh export as the
dashboard source; retain the initial import only as history.

The current UI has no external record-specific URL and renders note paths as
plain text. Link the dashboard to a local read-only record with clickable data,
code and figure paths. Provide the Notebook entry and searchable ID alongside
it. Records are browser-local; another browser needs an explicit import.

## Calendar export

The current `.ics` export retains IDs as event UIDs and planned work as
`TENTATIVE`, but writes floating times without a timezone. It also supplies
09:00/60 minutes for missing values. Export only the intended scheduled scope.
Before importing elsewhere, use the confirmed timezone to produce correct
timezone-aware or UTC start/end values; retain the UID and tentative status.
Check elapsed end dates for overnight work. Do not export an unknown historical
start time as a fabricated appointment. A 72-hour incubation is a treatment
window; operator work blocks and sampling deadlines need their own timing.

Sources: [Notebook](https://github.com/mianaz/labmate/blob/main/src/features/notebook/NotebookTab.jsx),
[Calendar](https://github.com/mianaz/labmate/blob/main/src/features/calendar/CalendarTab.jsx),
[backup importer](https://github.com/mianaz/labmate/blob/main/src/lib/backup.js).
