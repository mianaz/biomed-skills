# Choose the record owner

Checked 2026-11-17 against official documentation and source. Choose the tool
around the lab's established workflow, required record types, available support
and export needs. Recheck version and account capabilities when implementing.

| Tool | Useful role | Current source and practical boundary |
|---|---|---|
| Labmate | Local bench companion: protocols, notebook, calendar, sample locations and evidence maps | [Maintainer repository](https://github.com/mianaz/labmate); inspected commit `45855d3b84f302d3443ee6da9e3c189cb6a323b5`. [Backup code](https://github.com/mianaz/labmate/blob/45855d3b84f302d3443ee6da9e3c189cb6a323b5/src/lib/backup.js) exports experiments and evidence maps in a version-3 envelope. Inspect the deployed app before writing. Local storage needs an independent backup. |
| Benchling | Shared Notebook, Registry entities and Inventory locations/containers | [Notebook](https://help.benchling.com/hc/en-us/articles/39971013709965-Plan-experiments-and-collect-data-in-the-Notebook), [Registry](https://help.benchling.com/hc/en-us/articles/39953982240397-Create-and-manage-entities-with-the-Registry), [Inventory](https://help.benchling.com/hc/en-us/articles/39943809066637-Create-and-track-samples-with-the-Inventory), [exports](https://help.benchling.com/hc/en-us/articles/39943855017229-Share-data-in-Benchling). Check the account's actual modules, academic/commercial plan and API access. |
| eLabFTW | Open-source ELN, inventory and resource booking | [Official documentation](https://doc.elabftw.net/), [inventory](https://doc.elabftw.net/docs/usage/inventory/), [scheduler](https://doc.elabftw.net/docs/usage/user-guide/scheduler/), [export](https://doc.elabftw.net/docs/usage/import-export/). Version 6.0 documentation includes containers, locations and quantities. Self-hosting needs a service and backup owner. |
| openBIS | Linked materials, experiments and large datasets | [Official overview](https://openbis.ch/), [installation](https://openbis.ch/index.php/downloads/), [Python API](https://openbis.readthedocs.io/en/7.x/software-developer-documentation/apis/python-v3-api.html). Useful where an institution already supports the data service. |
| SciNote | Project, experiment and task workflows with inventory and protocols | [Product](https://www.scinote.net/product/), [open-source repository](https://github.com/scinote-eln/scinote-web), [protocol versions](https://knowledgebase.scinote.net/en/knowledge/how-to-save-different-versions-of-a-protocol). Verify the selected deployment: commercial features are not all included in the open-source version; [whole-project export](https://knowledgebase.scinote.net/en/knowledge/how-to-export-your-projects-data) is described as Premium. |
| protocols.io | Reusable protocol authoring, versioned reference and publication | [Official introduction](https://www.protocols.io/help/getting-started/quick-intro), [version API](https://apidoc.protocols.io/protocols). Link the precise version used; unversioned endpoints can resolve to the latest procedure. |

Start integration with stable links or an export of one experiment. Check that
its result reaches the raw data, run, sample, reagent lot and protocol version.
Build an API adapter only after the destination and data model are established.
Keep the root dashboard as a navigation view of these records.

For Labmate protocol import, use the maintained
[protocol contract](../../paper-to-protocol/references/labmate.md). The current
`protocolImport.js` initializes steps as incomplete, with blank deviations and
actual parameters. Retain those distinctions when a planned protocol becomes
an execution record. File generation alone does not establish a live import.
