# Full scientific plotting database

Build the complete HTML gallery when the user asks to browse the database. It has
one representative per template group, with all variants and their code linked
underneath. Groups span all collections. Source, language and family filters apply
to the variant lists. Full/filtered CSV exports retain every entry and source ID.

From the scientific-plotting folder, with Pillow and PyMuPDF available:

```sh
python3 scripts/template_database.py --output /path/to/local-gallery
```

To include every selected original, supply its private `curated-library` folder:

```sh
python3 scripts/template_database.py \
  --personal-dir /path/to/curated-library --output /path/to/local-gallery
python3 -m http.server 8917 --bind 127.0.0.1 --directory /path/to/local-gallery
```

The personal folder supplies `selected-plots.json`, `source-trace.json` and
`source-previews/`. Its selected originals replace the recipe-only entries in this
view. Recipe IDs remain attached to each mapped original. Registered publication,
MedBioinform and Prism libraries use the existing publication-gallery configuration.
The output contains local source links and private metadata; keep it in the user's
local review workspace. The portable skill contains only the builder and catalogs.

## Similar plots

`scripts/template_groups.py` assigns groups by chart geometry across collections.
Keep distinct structures, such as connected observations, split violins, circular
heatmaps and linked composite panels, in separate groups. Folder names are leads;
use the actual preview and plotting code when they disagree. MedBioinform source
classifications are explicit in that module. Each group has one representative,
all member IDs and its source collections. Filters can select a matching representative.
All implementations retain their input contract and design/review metadata.

Keep grouping decisions in the private library with its recipe keys and source
code. Preserve meaningful FDR columns, row selection, direction arrows, overlays
and native plotting engines as named variants.

Groups without a stored preview use a labeled synthetic R demonstration from
`assets/reference-library/representative-examples.json`. Its input tables, native
plot and code are linked alongside the original variants. These examples have
render and layout review; replacement-data review remains pending.

## MedBioinform layout editions

Supply `--medbio-editions /path/to/medbioinform` to include a local `manifest.json`
and its numbered edition folders. Each edition contains `source-edited.R`, the
original source, `layout.R`, a runnable `template.R`, and available exports/data.
`scripts/medbio_layout.R` edits appearance and renders native R objects. Font size,
plot area and total canvas are separate parameters. Start compact, then allocate
space for actual labels, legends, risk tables and composite panels.

Render from the supplied values or saved analysis results. Inspect the requested exports
and measure text at the saved canvas size. Record the render and visual-review
states separately. A prepared source whose input/package is unavailable keeps its
original preview on the original variant; its edited variant states what is needed.
Use the edition's saved data and code when continuing layout work.

When synthetic inputs are requested, keep the original recipe and add a separate
`source-synthetic.R`, a seeded `synthetic-data.R`, editable `synthetic-inputs/`
tables and `synthetic.json` with the data basis and any plotting substitutions.
Label both the rendered figure and gallery entry as synthetic. Review these
renders at the saved size; their review applies to the demonstration and layout.

## External code galleries

`assets/reference-library/code-galleries.json` contains 62 selected example pages
from 14 sources. Each has an exact code link, attribution, source preview when
available, and a checked date. The gallery view also links each complete source
collection. External example counts describe the pages indexed here.

Sources include tidyplots, ggplot2, ComplexHeatmap, ggpubr, survminer, ggridges,
ggalluvial, ComplexUpset, circlize, R Graph Gallery, Python Graph Gallery, seaborn,
Matplotlib and Bizard. Source pages contain plotting code; local execution and
replacement-data review remain separate. Link to the source terms when adapting
third-party code or artwork. Keep external records at reference status until their
specific implementation and new inputs have been tested.

The HTML shows existing artwork and source-provided previews. Native Prism projects
without a saved preview have a direct project link. Image-only personal originals
stay visible with their current source status.
