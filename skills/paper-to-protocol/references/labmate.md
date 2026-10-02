# Labmate protocol import

Source checked 2026-10-02 against
[mianaz/labmate, commit 45855d3](https://github.com/mianaz/labmate/tree/45855d3).
The contract comes from `src/lib/backup.js`, `src/lib/protocolImport.js`,
`src/components/RecipeDetail.jsx` and `src/features/refs/RefsTab.jsx`.
The public library template is separately maintained in
[mianaz/labmate-recipes](https://github.com/mianaz/labmate-recipes/blob/b0f2515/templates/protocol_template.json).

## Import path

Open Labmate → **Guide → Backup & restore → Import** and choose
`labmate-import.json`. The importer reloads the app. Find the item under Protocols
and inspect its detailed steps. The import file contains only
`data.labmate_customProtocols`; it does not restore preferences, inventory,
notebooks or credentials. Import merges by ID and replaces a matching custom
protocol. Give a new protocol a unique `custom_<slug>_<version-or-uuid>` ID.

This is an existing local import path, not a server upload API or public recipe
publication. Check the deployed app exposes this import control before using it;
GitHub source alone does not establish which version a particular browser runs.

## Recipe fields

| Field | Shape / meaning |
|---|---|
| `id`, `name`, `category` | Unique ID, display title, literal `protocol` |
| `_isCustom` | Exporter sets true |
| `status` | Draft, confirmed plan, or other accurate status; exporter also puts it in visible notes |
| `usage`, `notes` | Objects with `en` text; optional `zh` |
| `ref`, `doi` | Citation text and optional DOI |
| `materials` | Objects with `name`, optionally `amount`, `unit`, `note` |
| `detailedSteps` | Ordered objects with `en`, optional `zh`, `time`, `temp`; headers have `isHeader: true` |
| `source` on each action | Source locator or explicit user-supplied/proposed label; exporter embeds it in displayed step text |
| `briefSteps` | Exporter derives localized summaries from actions |
| `safeStops` | Optional objects with `afterStep` and localized `note` |

`afterStep` is the **zero-based detailedSteps array index**, including headers.
Do not derive it from the printed one-based action number. Leave the array empty
when no stop is established. The library contribution checklist asks for a safe
stop, but a private draft must not invent one to meet that publication convention.

The existing custom editor expects plain-string brief steps and may flatten rich
protocols. Edit the source `protocol.json`, regenerate and deliberately reimport
the same ID to retain detailed steps, provenance and stopping points.

## Envelope

```json
{
  "schemaVersion": 3,
  "exportedAt": "2026-10-02T12:00:00+00:00",
  "data": {"labmate_customProtocols": []}
}
```

The exporter fills the array with one recipe. Keep parameters in the action text
as well as optional time/temp fields: Labmate's timers detect duration text.
Notebook conversion uses detailed action steps (excluding headers), with
`completed: false`, empty `deviation` and empty `actualParams` initially. Planned
instructions therefore remain distinguishable from an execution record.
