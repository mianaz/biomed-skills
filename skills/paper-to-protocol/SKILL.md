---
name: paper-to-protocol
description: Turn a paper's Methods and supplements into a sourced step-by-step experimental or computational protocol. Deliver the requested readable or printable format; use the Labmate import route when requested. Use for paper-to-protocol and paper-to-Labmate workflows.
---
# Paper to Protocol

Read [shared principles](../biomed-shared/core-principles.md).

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

## Deliver the requested protocol

Return a readable procedure at the requested scope and format. For a reusable
multi-format bundle or Labmate import, read
[protocol export](references/protocol-export.md). Inspect the actual document or
printable view before delivering it.

## Labmate handoff

For an upload request, read [Labmate handoff](references/labmate.md) and import
`labmate-import.json` through Labmate's existing
Guide → Backup & restore → Import control. It merges custom protocols by ID; use a fresh
ID for a new protocol and preserve an ID only for an intended replacement.
Confirm the title, step count, materials and detailed steps in the app after
import. This creates a local custom protocol, not a public library contribution.
Do not claim upload from file generation alone. If app access is unavailable,
deliver the file and exact import instructions and identify upload as pending.

For Methods writing, hand the protocol plus the actual experiment record to
`protocol-to-methods`; retain completed steps, deviations and actual parameters.
