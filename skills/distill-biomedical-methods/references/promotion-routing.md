# Route promotion proposals

| Proposal content | Canonical owner |
|---|---|
| Study units, controls, endpoint, allocation, or precision rule | `design-biomedical-study` |
| Analysis question, profile, required output, or validation criterion | `plan-biomedical-analysis` |
| Input, resource, code, environment, or lineage requirement | `ensure-biomedical-reproducibility` |
| Data integrity or readiness check | `validate-biomedical-data` |
| Cross-artifact or independent validity check | `verify-biomedical-analysis` |
| Figure encoding, image integrity, export, or render QA | `create-scientific-figures` |
| Domain method, parameter rule, or diagnostic | Narrowest domain action skill |
| Model performance or leakage rule | `evaluate-biomedical-models` or narrower domain skill |
| Evidence-review search, appraisal, or synthesis rule | `synthesize-biomedical-evidence` |
| Agent role, handoff, or isolation pattern | `orchestrate-biomedical-work` |
| Audience, story, or evidence placement pattern | `communicate-biomedical-results` |
| Promotion, deprecation, or suite-memory rule | `maintain-biomedical-skills` |

Do not promote one requirement to several owners. Put it in the narrowest coherent
owner and add routing language elsewhere only when triggering would otherwise fail.

Every promoted item retains:

```text
source_digest: <stable path or URI>
source_locator: <method/figure/section ID>
publication_id: <DOI, registry, accession, or other stable ID>
code_or_protocol_version: <commit/version/not_available>
evidence_level: <source tag>
verified_on: <date>
```

If later evidence strengthens or contradicts a rule, update its provenance and
limitations; do not clone it.
