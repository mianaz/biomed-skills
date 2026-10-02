---
name: submission-check
description: Distill current Cell, Nature or Science journal requirements into an actionable checklist and prepare a manuscript submission package. Use for initial submission, revision or final-file preparation, including figures, source data, reporting forms and declarations.
---
# Submission Check

Establish the exact journal, article type and stage: initial, revision or final
accepted files. Infer these from the user's files or decision letter when clear;
otherwise ask while inventorying the package. “CNS” means the Cell, Nature and
Science families, not a single shared specification.

Read [references/publishers.md](references/publishers.md), then retrieve the current
journal-specific author instructions and relevant forms. Follow the editorial
letter for that submission. Record source URL, section and retrieval date for each
requirement. Separate requirements, recommendations and items conditional on
study design or stage. Do not apply final-production rules to an initial submission.
If a page is inaccessible, use a supplied official checklist or mark the affected
requirements unverified; do not substitute a sister journal or old blog silently.

## Prepare the package

Read the actual manuscript, figures, supplements and supplied metadata. Distill
only applicable requirements into `submission-checklist.tsv` with columns:
`item`, `requirement`, `journal`, `article_type`, `stage`, `required_or_recommended`,
`source_url`, `source_section`, `checked_date`, `status`, `file_or_location`,
`next_action`. Use `ready`, `needs-edit`, `missing`, `not-applicable` or `unverified`.
Give a reason for not-applicable items.

Cover the categories needed for this submission:

- Manuscript structure, title/abstract and length, references, Methods and legends.
- Authors, affiliations, corresponding/lead contact, contributions, funding,
  competing interests, ethics/consent and registration where applicable.
- Figure dimensions/formats/resolution, editable source, readable labeling,
  source data and original image evidence when required.
- Supplementary files, numbering, legends, multimedia and cross-references.
- Data/code availability, accessions, repository links and reviewer access.
- Reporting summary/checklists, resource identifiers and design/statistics reporting.
- Cover letter, revision response, marked/clean versions and journal-specific
  extras only when requested or required at this stage.

Make authorized formatting/file-preparation changes in a separate
`submission-package/` directory; retain original files. Include a short
`package-index.md` mapping files to upload slots and list the remaining author
inputs. Draft declarations from supplied facts; author agreement, approvals,
consent and conflicts require author-provided information. Check figure labels,
supplement references and data links against the final prepared files.

For academic text use nature-writing, nature-polishing and humanizer when
available. Present the package and a short prioritized action list. Preparing a
package does not authorize submitting it, signing declarations or messaging editors.
