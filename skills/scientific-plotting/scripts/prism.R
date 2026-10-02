# Editable Prism data tables. Source this file; no R package is required.
write_prism <- function(data, path, x = NULL, id = NULL, title = "Data", groups = NULL,
                        overwrite = FALSE) {
  stopifnot(is.data.frame(data), nrow(data) > 0L, ncol(data) > 0L,
            length(path) == 1L, grepl("\\.pzfx$", path, ignore.case = TRUE),
            length(title) == 1L, !is.na(title), is.logical(overwrite),
            length(overwrite) == 1L, !is.na(overwrite))
  if (file.exists(path) && !overwrite) stop("Choose a new output path or set overwrite = TRUE.")
  if (anyDuplicated(names(data))) stop("Column names must be unique.")
  for (key in list(x, id))
    if (!is.null(key) && (length(key) != 1L || is.na(key) || !key %in% names(data)))
      stop("x and id must name columns in data.")
  if (!is.null(x) && identical(x, id)) stop("x and id must be different columns.")
  ys <- setdiff(names(data), c(x, id))
  numeric_columns <- c(x, ys)
  if (!length(ys) || !all(vapply(data[numeric_columns], is.numeric, logical(1))))
    stop("X and Y columns must be numeric; use NA for missing values.")
  if (any(vapply(data[numeric_columns], function(v) any(is.infinite(v) | is.nan(v)), logical(1))))
    stop("Use finite values or NA; Inf and NaN are not supported.")
  if (!is.null(id) && (anyNA(data[[id]]) || anyDuplicated(data[[id]]) || any(data[[id]] == "")))
    stop("Row IDs must be present and unique; align paired observations before export.")
  if (!is.null(x) && anyNA(data[[x]])) stop("Each XY row requires an X value.")
  if (is.null(groups)) groups <- setNames(ys, ys)
  if (is.null(names(groups)) || anyDuplicated(names(groups)) || !setequal(names(groups), ys) ||
      anyNA(groups) || any(groups == ""))
    stop("groups must map every Y-column name to a dataset name exactly once.")
  groups <- groups[ys]
  datasets <- unique(unname(groups))
  counts <- vapply(datasets, function(g) sum(groups == g), integer(1))
  if (length(unique(counts)) != 1L)
    stop("Replicate counts must match across datasets; add explicit NA columns for absent replicates.")
  replicates <- counts[1]
  type <- if (!is.null(x)) "XY" else if (replicates > 1L) "TwoWay" else "OneWay"
  escape_xml <- function(v) {
    v <- gsub("&", "&amp;", as.character(v), fixed = TRUE)
    v <- gsub("<", "&lt;", v, fixed = TRUE)
    gsub(">", "&gt;", v, fixed = TRUE)
  }
  cells <- function(v) paste0("<d>", ifelse(is.na(v), "", escape_xml(v)), "</d>", collapse = "")
  subcolumn <- function(v) paste0("<Subcolumn>", cells(v), "</Subcolumn>")
  # 17 significant digits preserve input doubles; Decimals controls display only.
  numeric_subcolumn <- function(v) subcolumn(ifelse(is.na(v), NA_character_, sprintf("%.17g", v)))
  row_titles <- if (is.null(id)) "" else
    paste0('<RowTitlesColumn Width="100">', subcolumn(data[[id]]), '</RowTitlesColumn>')
  x_column <- if (is.null(x)) "" else paste0(
    '<XColumn Width="100" Decimals="6" Subcolumns="1"><Title>', escape_xml(x),
    '</Title>', numeric_subcolumn(data[[x]]), '</XColumn>')
  y_columns <- vapply(datasets, function(g) paste0(
    '<YColumn Width="100" Decimals="6" Subcolumns="', replicates, '"><Title>', escape_xml(g),
    '</Title>', paste0(vapply(data[ys[groups == g]], numeric_subcolumn, character(1)), collapse = ""),
    '</YColumn>'), character(1))
  xml <- paste0('<?xml version="1.0" encoding="UTF-8"?>\n',
    '<GraphPadPrismFile PrismXMLVersion="5.00">\n',
    # Prism requires its compatibility header; the actual writer is recorded in Info.
    '<Created><OriginalVersion CreatedByProgram="GraphPad Prism" CreatedByVersion="6.0f.254" Login="" ',
    'DateTime="', format(Sys.time(), "%Y-%m-%dT%H:%M:%S+00:00", tz = "UTC"), '"></OriginalVersion></Created>\n',
    '<InfoSequence><Ref ID="Info0" Selected="1"></Ref></InfoSequence>\n',
    '<Info ID="Info0"><Title>Export details</Title><Notes><Font Face="Arial" Color="#000000">',
    'Editable data tables exported by scientific-plotting. Graphs and analyses are not embedded.',
    '</Font></Notes></Info>\n',
    '<TableSequence><Ref ID="Table0" Selected="1"></Ref></TableSequence>\n',
    '<Table ID="Table0" XFormat="', if (is.null(x)) 'none' else 'numbers',
    '" YFormat="replicates" Replicates="', replicates, '" TableType="', type, '" EVFormat="AsteriskAfterNumber">',
    '<Title>', escape_xml(title), '</Title>', row_titles, x_column,
    paste0(y_columns, collapse = ""), '</Table>\n</GraphPadPrismFile>\n')
  xml <- gsub("><", ">\n<", xml, fixed = TRUE)
  writeLines(enc2utf8(gsub("<d>\n</d>", "<d></d>", xml, fixed = TRUE)), path, useBytes = TRUE)
  invisible(path)
}
