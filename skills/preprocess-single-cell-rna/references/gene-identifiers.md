# Gene identifiers

Preserve a stable feature identity from acquisition through analysis. Display
symbols can change with annotation releases; stable IDs and original labels make the
mapping auditable.

## Standardize

1. Record species, genome build, annotation release, original feature ID, original
   symbol, feature type, and standardized symbol.
2. Correct aliases with a species-appropriate authority. For human symbols,
   `HGNChelper` can flag and update known aliases, but inspect ambiguous mappings.
3. Remove version suffixes from stable IDs only into a separate normalized field.
4. Resolve duplicate display symbols before conversion. Sum raw counts only when
   records represent the same biological feature under the chosen annotation;
   otherwise retain stable IDs as row names.
5. Keep immunoglobulin and T-cell receptor features identifiable even when they do
   not fit ordinary protein-coding filters.

For cross-species work, delay ortholog restriction until
`integrate-single-cell-data`. Record the orthology database and release, prefer
one-to-one mappings for direct expression comparison, and keep unmapped features in
the species-specific source objects.
