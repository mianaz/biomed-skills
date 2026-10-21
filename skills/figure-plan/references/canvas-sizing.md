# Choose the figure dimensions

Treat the canvas as a layout variable. A square page is useful only when the
content and intended placement call for one. Record width and height in mm,
the target manuscript width, and the basis for each choice.

## Choose width, then solve height with placement

1. Retrieve applicable journal dimensions when a journal is given. Use its
   permitted column widths and maximum height. Without them, state provisional
   widths for comparison; a literature median is an observation, not a rule.
2. Allocate each evidence group enough space for readable labels and comparable
   data. Start ordinary plots near 50 × 50 mm, retaining the panel's aspect ratio.
   Dense heatmaps, images and diagrams need their own allocations. Panel count
   alone cannot determine figure area. Run the source-panel scaling check in
   [effective typography](effective-typography.md) before packing; an internal
   type mismatch requires source repair, even on an unconstrained canvas.
3. Compare a few arrangements at the allowed widths. Derive height from panel
   heights, letter bands, gutters and margins. Reflow when height exceeds the
   limit or labels become too small. Repair dense panels at their source when
   needed; preserve the claim and required comparisons when splitting a figure.
4. Find the envelope of all panels, letters and shared legends. Add deliberate
   margins, initially 3–5 mm. If an allowed width must stay fixed, adjust the
   layout or center the content; trimming width is a diagnostic, not permission
   to ignore the target width. Fit height to the content unless it is constrained.
5. Render the actual PPT at the proposed dimensions. Check effective typography,
   group adjacency, visual balance and source resolution. Save the accepted
   export rectangle and its rationale with the figure plan.

**Done:** the chosen width meets the intended use, height follows the evidence
layout, all objects fit, and type is readable at the final manuscript scale.

## Use literature dimensions correctly

Measure a figure's artwork bounds in PDF points and convert with `25.4 / 72`.
Record whether the boundary is a manually reviewed object envelope, a raster
image boundary or a thresholded ink estimate. Record page and figure identifiers,
main/Extended Data/supplement status, panel count when known, and caption bounds.
Keep body text, captions and page furniture out of the measurement.

Published width and height describe the typeset artwork. They do not reveal the
author's original PowerPoint size, submission canvas or journal maximum. Pool
figures within a paper cautiously: record paper-level ranges and the spread at
similar panel counts. Retain uncertain extractions outside reviewed summaries.
Measure different journals and display types; full-width figures and embedded
supplemental pages need separate descriptions.

Use these distributions to propose candidate dimensions. Choose among candidates
using the current evidence groups and effective text size, not a target fill
percentage. A compact layout can still be unreadable.

## Diagnose a size mismatch

Render the original and a crop-only version at the same screen scale. Preserve
every panel's dimensions, all letters, gutters and content. The crop removes
only unused outer canvas. Record outer margin area, space within the content
envelope and internal panel blank space separately using the
[layout review definitions](layout-review.md).

Offer fit-to-width as a separate preview mode. Enlarging a cropped image changes
the viewing size; it cannot serve as the crop-only control. Higher DPI changes
sampling, not font size. Keep genuine negative space around sparse data and
between evidence groups when it improves reading.

**Done:** the comparison identifies what changes with canvas size, what remains
inside the layout, and whether later resizing would meet the font requirement.
