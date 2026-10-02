---
name: paper-to-protocol
description: Turn a paper's Methods and supplements into a sourced step-by-step experimental or computational protocol, with a human-readable printable copy and a Labmate-compatible import file. Use for paper-to-protocol and paper-to-Labmate workflows.
---
# Paper to Protocol

Read the paper's relevant Methods, supplements and referenced protocols. Reuse
local files first. Identify the procedure and intended biological system from the
request; for several independent procedures, make separate protocols.

## Extract and adapt

Write numbered actions in execution order, grouped into stages when useful.
Include purpose, materials/equipment, preparation, quantities/concentrations,
temperatures, durations, centrifugation force, instrument settings, controls,
readouts, expected observations and documented stopping/storage points. For a
computational protocol, include input formats, software/version, commands,
parameters and expected outputs. Keep reported, user-supplied and proposed details
visibly distinct. Mark missing critical values as “not reported”; never turn a
plausible default into a paper-derived fact. Do not invent safe stops to fill a
field. Write original procedural wording with source citations.

Record paper citation/DOI and exact Methods/page/supplement locators for each
step. Include adaptations and unresolved questions in the notes and next to the
relevant action. Copying a published protocol describes a plan, not a performed
experiment. A draft with missing execution-critical parameters remains a draft.

## One source, three outputs

Read [references/labmate.md](references/labmate.md). Use the recipe-shaped JSON
shown in [assets/example.json](assets/example.json) as the field guide; its
fictional teaching content is not a biological protocol. Save `protocol.json`.

```bash
python3 scripts/export_protocol.py protocol.json output/
```

This produces `protocol.md`, printable `protocol.html`, and `labmate-import.json`
from the same ordered steps and metadata. Open the HTML and inspect the printed
layout; use browser Print → Save as PDF if a PDF is requested. Preserve readable
Arial text, numbered steps, source notes and page breaks. Deliver the JSON too so
future edits can regenerate both outputs consistently.

## Labmate handoff

For an upload request, import `labmate-import.json` through Labmate's existing
Guide → Backup & restore → Import control. It merges custom protocols by ID; use a fresh
ID for a new protocol and preserve an ID only for an intended replacement.
Confirm the title, step count, materials and detailed steps in the app after
import. This creates a local custom protocol, not a public library contribution.
Do not claim upload from file generation alone. If app access is unavailable,
deliver the file and exact import instructions and identify upload as pending.

For Methods writing, hand the protocol plus the actual experiment record to
`protocol-to-methods`; retain completed steps, deviations and actual parameters.
