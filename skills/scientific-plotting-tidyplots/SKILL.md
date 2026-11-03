---
name: scientific-plotting-tidyplots
description: Use when the user requests the tidyplots-specific biomedical plotting entry by name. This compatibility entry delegates figure work to scientific-plotting with its tidyplots route; general chart selection and figure repair use scientific-plotting.
---

# Scientific Plotting with tidyplots

Use [scientific-plotting](../scientific-plotting/SKILL.md) as the owning workflow
for data, design, statistics, appearance, verification and delivery. Apply its
[tidyplots route](../scientific-plotting/references/tidyplots.md) for implementation.
Keep requested formats and existing validated analyses. This compatibility entry
adds no separate review, output contract or approval step.

The retained `scripts/tidyplots.R` helper and `examples/run.R` support existing
consumers. Run examples only when testing or a worked example is requested.
