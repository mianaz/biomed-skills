# Full distribution verification

Date: October 14, 2026.

## Input integrity

The supplied v2.2 ZIP contains 216 files. ZIP CRC verification passed.
All 215 entries in its original CHECKSUMS.json matched their SHA-256 values;
the remaining file is that manifest. Every original file, including the original
manifest, is included byte for byte in this distribution.

## Fresh checks performed for this packaging task

| Check | Result |
|---|---|
| Core and layout unit tests | 28 / 28 passed |
| Chromium interactions and label checks | 96 / 96 passed |
| Layout and regression checks | 39 / 39 passed; 363 distinct sampled animation states |
| Painted-extent audits | 17 / 17 passed |
| Declared topology checks | 18 / 18 passed |
| New annotation validator | 8 / 8 positive/negative cases passed |
| New launcher | All 8 local navigation targets exist |

The original checks ran in a separate working copy; their fresh logs and machine
reports are in this directory. Original example files and reports remain intact.
The new annotation checks cover a valid synthetic example and rejection of
unreviewed training eligibility, missing scientific evidence, occlusion cycles,
duplicate IDs, unsupported measured timing, parent cycles, and unknown entities.

## Delivery

All example HTML, SVG/PNG output, two current MP4 exports, scripts, asset records,
source snapshots, licenses, templates, prior comparison snapshots and original
reports are retained. Additions include the roadmap, pilot protocol, annotation
schema and example, correction candidates, validators, launcher, environment
record, and these verification logs.

The original CHECKSUMS.json verifies the original payload. FULL_CHECKSUMS.json
verifies all distribution files except itself. Run `python verify_bundle.py` from
the extracted root. Hashes establish integrity against the included manifest;
they are not a digital signature or an authentication of the author.

## Scope

This packaging task reran executable checks and added documentation and data
preparation tools. It did not train a model, collect a paper-figure dataset, or
benchmark external research systems. The historical visual comparison and reading
scope are in ../qc-report.md. The finite checks do not establish universal visual
quality or biological accuracy. Chromium checks use inline document loading;
direct file navigation was not retested.
