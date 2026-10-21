# Slides and video

Read the branch that matches the requested deliverable. Keep the same scene IDs,
scientific claims and source locators as the HTML lesson.

## Slides

For browser slides, use one scene per screen with previous/next controls, arrow
key navigation, progress and a print stylesheet that exposes all slides. Keep
controls from intercepting arrow keys while the user operates an input. Give
each build a clear final state for print/export. Retain citations on the slide
or in linked speaker notes.

When PowerPoint is requested, deliver an editable PPTX plus an HTML preview when
tools permit. Use available presentation tooling and inspect rendered slides.
Keep diagrams editable where practical; avoid turning all content into screenshots.
Each slide should carry one visual argument. Fit content by splitting scenes,
not by reducing labels below the viewing-size requirement.

## Video

Turn the storyboard into timed beats: scene ID, duration, visual action,
narration/caption and source locator. Introduce each object when it is named.
Keep time for the viewer to inspect the result before the next change.

Use available local tooling: HTML/SVG capture for browser-native scenes, or
Manim for transformations that benefit from mathematical animation. Inspect
installed versions and their documentation before using tool-specific APIs.
Use a reproducible timeline with a seekable `renderAt(seconds)` or equivalent
when capturing frames; viewport size, frame rate and duration must be explicit.
Prefer 1920 × 1080 at 30 fps unless the user needs another format.

For narration, use an available authorized TTS service or local voice and retain
the script. Use a neutral narrator rather than impersonating a named educator.
Default to a captioned silent video if voice is unspecified and no voice tooling
is available. If narration was requested, report its absence and retain the
script for completion. Do not silently substitute synthetic narration for an
actual speaker's recording. External upload, paid services and publication need
the user's applicable authorization.

Render the requested MP4/WebM and retain editable scene code, narration text and
caption timing (VTT/SRT). Include a local HTML player with controls and captions
when practical. Verify playback, duration, first/last scenes, key transitions,
readability and audio/caption alignment. Sample frames alone cannot verify sound.
If encoding is blocked, deliver the working HTML and timed source as a clearly
labeled fallback; state that the requested video export is incomplete.
