# Visual language: a lesson on a blackboard

## Stage and type

Default to black (#000), off-white (#eee), and two or three stable semantic
colors. Useful Manim colors: blue #58C4DD, yellow #FFFF00, green #83C167,
red #FC6255. Highlight the relationship being discussed; dim other components.
Use an open drawing field, one short heading and one caption. Keep navigation
quiet and place detailed evidence below the stage. Card grids, decorative
borders, gradients and dashboard counters add little to this teaching mode.
For biomedical scenes, use the BioRender-style vector guidance in
[illustrations.md](illustrations.md): clear biological silhouettes and soft flat
fills within this same stage. Keep the colors stable across scenes.

Use **CMU Serif** for lesson headings, labels and prose, with Computer Modern
math where needed. The bundled [font](../assets/fonts/cmunrm.woff) uses the
[SIL Open Font License](../assets/fonts/OFL.txt); preserve that license when
redistributing or embedding it. Use Arial for small controls and source notes.
Publication plots keep their separate Arial convention.

At a roughly 1100–1200 px-wide lesson, start with 40–48 px headings, 26–32 px
labels and 22–26 px captions, normal weight. These are browser design targets,
not a claim that every 3Blue1Brown video uses one size. In a 1080p video, start
around 60–72 px headings and 36–48 px labels, then inspect at playback size.
Keep every visible label above 10 pt at actual viewing size. On phones, rearrange
the geometry and reduce scene detail; never scale a desktop diagram until its
labels become illegible. Use generous empty space to direct attention.

## Motion

Use motion to assemble parts, expose a connection, trace a process, compare a
condition or transform a representation. Preserve object identity, color and
spatial continuity across those changes. Show biological motion only to the
extent supported; schematic teaching order is not a measured reaction timeline.

Use time-based interpolation. For a short reveal, 0.4–1.2 seconds plus a reading
hold is a useful starting point. Keep the same camera unless a closer view
answers the current question. Avoid perpetual pulsing and decorative drifting.

Provide play/pause, replay, scene navigation and a seek control for timed lessons.
Start paused; stop on completion and when hidden. Reduced motion uses readable
still states and working navigation. Touch and keyboard must reach the same
controls. Keep live screen-reader announcements at scene changes, not every frame.

Inspect an intermediate frame as well as each endpoint: a readout and its drawing
must describe the same state, and a connector must remain attached as parts move.

## Influences and provenance

- [3Blue1Brown's configuration](https://github.com/3b1b/videos/blob/306a1346a356c7a7b097875ceb51c5cd67d0a56c/custom_config.yml)
  specifies a black background, CMU Serif, centered text and 30 fps. The
  [teaching notes](https://www.3blue1brown.com/about/) explain purposeful visuals.
- [Anatomy](https://github.com/wheresryan22/anatomy/tree/be2fa9b47a7e4b05dec468be9ffc42e830c2101c)
  informed component decomposition, consistent geometry and a shared model for
  motion/readouts. Its dense machine-detail, card and idle-tour defaults are not
  defaults here. No Anatomy code is bundled.
- [Answer me with HTML](https://github.com/QingYunA/answer-me-with-html) informed
  portable visual answers. No runtime dependency is required.
