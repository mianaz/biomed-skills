# Audit effective typography

Run this check during candidate generation and again on the final saved deck.
Measure each text role at the intended manuscript size. Use source plot/PDF
font sizes or native PPT text. Record the source width, placed width, export
width and manuscript width:

`effective_pt = source_pt × placed_width / source_width × manuscript_width / export_width`

Use the cropped export width when the figure is exported from part of a shared
working slide. DPI does not enter this calculation. Check the actual PDF page
dimensions and native letter sizes after rendering; the declared values alone
do not establish the final scale.

Set role targets before comparing candidates. Without a different project
requirement, use 11 pt ordinary labels and letters, with ordinary text above
10 pt. Report minimum, 10th percentile, median and maximum by role. Compare
numeric ticks with ticks, ordinary labels with labels, and headings with
headings. Report superscripts and statistical marks separately.

Flag both small and large text. An initial review tolerance is a 20% difference
between equivalent-role panel medians, or a median above 13.2 pt for an 11 pt
ordinary-label target. These are declared consistency checks, not evidence of
beauty. A justified hierarchy can use different role targets; record the reason.
Do not let a large heading hide small ticks inside the same panel.

Before packing, test whether each source panel can meet its type targets by
uniform scaling. For ordinary text, the scale must exceed `floor / minimum`
and must not exceed `median_upper / largest_role_median`. If those intervals do
not overlap, changing the canvas cannot solve that panel's type mismatch.
Check the role assignments, then repair the source plot. Keep this failure
separate from crowding caused by the layout. Recheck headings, statistical
marks and superscripts visually; the helper's ordinary-text gates do not
certify those other roles.

Raster or outlined text without a recoverable source size remains unmeasured.
Native PDF spans can measure only part of a mixed figure. Save text-coverage
status and inspect image labels, scale bars and legends. OCR may locate missed
text; it does not by itself supply exact point sizes. Font family and glyph
rendering require their own check. A pass on measured spans is not a pass on
unmeasured text.

Use [the audit helper](../scripts/audit_typography.py) with one object per figure:
`id`, `export_width_mm`, `manuscript_width_mm`, `letter_pt`, and `panels`. Each
panel supplies `id`, `source_width_mm`, `placed_width_mm`, `text_coverage`
(`complete` only after verification), and `role_profiles`. Each role profile
contains `min`, `q10`, `median`, and `max` in source points. Empty profiles stay
unknown. Save the helper's per-panel rows and flags in the HTML review.

If no layout satisfies size and typography, mark the figure repair-required.
Replot dense panels at the target type size, shorten/wrap labels, split a
composite panel, or revise the evidence grouping. Preserve the failed version
when benchmarking. A preferred draft remains a draft until its source and
rendered typography pass.

**Done:** every text role has measured effective sizes or an explicit unknown,
size inconsistencies have been resolved or justified, and the final manuscript
scale matches the exported artifact.
