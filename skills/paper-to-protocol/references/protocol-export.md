# Reusable protocol export

Use for a reusable multi-format bundle or Labmate import. Read
[Labmate fields](labmate.md), then use [the example schema](../assets/example.json)
to save `protocol.json`. Its teaching content is fictional.

From the skill directory, run:

```bash
python3 scripts/export_protocol.py protocol.json output/
```

The exporter writes `protocol.md`, printable `protocol.html` and
`labmate-import.json` from the same ordered steps and metadata. Open the HTML and
inspect the printed layout. Use Print → Save as PDF when PDF is requested. Preserve
readable Arial text, numbered steps, source notes and page breaks. Retain the JSON
for future edits and deliver the formats needed for the requested handoff.
