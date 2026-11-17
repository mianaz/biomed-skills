---
name: lab-records
description: Organize biomedical experiment runs, raw data, sample/reagent inventories and protocol versions with links between what was planned and performed. Use for ELN setup, 实验记录、原始数据、样本、试剂 or protocol management in Labmate, Benchling or another existing lab system.
---

# Lab Records

Read [shared principles](../biomed-shared/core-principles.md).

Read [research principles](../biomed-shared/research-principles.md). For setup or
updates to an existing system, inspect its ELN, inventory and data locations.
Use supplied facts directly for a standalone record. Keep one authoritative home for each
record type and connect them through stable identifiers. Read
[tool selection](references/tool-selection.md) when choosing or connecting systems.

## Connect the records

Use fields that serve the actual experiment. A small laboratory can start with
one run note and a sample/reagent table; a shared platform can own the same fields.

| Record | Useful minimum |
|---|---|
| Protocol | ID, version, source, ordered procedure, adaptations, status |
| Run | Run ID, question, protocol version, date/operator, input sample IDs, actual parameters, deviations, observations, output locations |
| Sample/aliquot | Stable ID, parent sample when relevant, material, preparation, amount/unit, storage location, status |
| Reagent | Name, supplier/catalogue, lot, concentration/unit, preparation or expiry when relevant, storage location, availability |
| Raw dataset | Run and sample IDs, acquisition time, instrument/settings, original path or accession, metadata and format |
| Result | Run/input IDs, analysis/source location, output and interpretation, next decision |

Use plate/well, freezer/rack/box/position or other spatial coordinates where
needed. Keep identity stable when a sample moves. Link aliquots to parents and
retain the reagent lot actually used. Model a reservation separately from
consumption if inventory quantities are managed.

## Record execution and preserve data

Create a run from its chosen protocol version. Record actual steps, deviations,
parameters and observations during execution. A later protocol edit creates a
new version; the completed run retains the procedure it used. Preserve failed
runs, informative null results and reasons for repeating work.

For retrospective records, distinguish the acquisition date from the date the
record was assembled. Preserve plate/well and source-row coordinates when sample
identity is incomplete. Leave unavailable protocol versions, operators, lots and
biological replicate IDs explicit; do not reconstruct them from a plot filename.

Keep instrument exports and original metadata in the established raw-data
location. Put processing and analysis outputs separately, linked to the inputs;
retain sample-ID mappings and the records needed to interpret files. Large data
can remain on an established server or repository with a durable location.
Use the lab's backup and access arrangements; for a new setup, include an
independent backup and a practical restore check. Avoid copying large datasets
solely to populate a dashboard.

When entering records into Labmate, use its current supported import or UI path.
The protocol exporter belongs to `paper-to-protocol`; read its
[Labmate contract](../paper-to-protocol/references/labmate.md) for that operation.
Inspect current source or documentation before inventing an inventory, calendar
or notebook adapter. Verify an authorized import in the destination and preserve
existing records. Report file preparation and successful import separately.
For Notebook/Calendar records, read the tested
[Labmate notebook mapping](references/labmate-notebook.md). Use the dedicated
experiment import when that is the intended scope, then export the destination
records and use that snapshot for the dashboard.

## Close the loop

After a run, connect the observation to its question and interpretation; identify
the next useful decision. Use `scientific-reproducibility` for analysis outputs
and `protocol-to-methods` for Methods from the actual execution record.
When saving project records, link runs, inventories, protocol versions and result galleries from the
[project dashboard](../biomed-shared/project-dashboard.md).

Deliver the usable records and clear locations. Confirm that a result can be
traced back to its run, protocol version, sample/reagent identity and raw input.
