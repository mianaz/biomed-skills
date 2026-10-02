# Run with the same Rscript used to draw the figure.
required <- c("ggplot2", "cowplot", "ragg", "pdftools", "systemfonts")
present <- vapply(required, requireNamespace, logical(1), quietly = TRUE)
for (pkg in required) cat(if (present[pkg]) "OK     " else "MISSING", pkg,
  if (present[pkg]) as.character(utils::packageVersion(pkg)) else "", "\n")
cairo <- isTRUE(capabilities("cairo"))
arial <- present["systemfonts"] && "Arial" %in% systemfonts::system_fonts()$family
cat(if (cairo) "OK     " else "MISSING", "Cairo PDF device\n")
cat(if (arial) "OK     " else "MISSING", "Arial font family\n")
cat("Optional dose-response package drc:",
  if (requireNamespace("drc", quietly = TRUE)) "available" else "not installed", "\n")
if (any(!present)) cat("Install missing packages with install.packages(c(",
  paste(sprintf('"%s"', required[!present]), collapse = ", "), "))\n", sep = "")
if (!arial) cat("Install a licensed Arial font, then restart R. Export checks verify the embedded font.\n")
if (!cairo) cat("Use an R build with Cairo support for the PDF exporter.\n")
quit(status = if (all(present) && cairo && arial) 0 else 1)
