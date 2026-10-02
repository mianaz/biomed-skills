# Run from the repository root; optional first argument selects a fresh output directory.
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args)) args[1] else tempfile("figure-colour-preview-")
dir.create(out, recursive = TRUE, showWarnings = FALSE)
script <- "skills/create-scientific-figures/scripts/color_preview.R"
input <- file.path(out, "source.png")
stem <- file.path(out, "preview")
source <- array(1, c(70L, 360L, 4L))
source[1:20, 1:100, 1:3] <- 128 / 255
source[21:40, 1:100, 2:3] <- 0 # Opaque red.
source[41:60, 1:100, 1:2] <- 0 # Blue with partial alpha.
source[41:60, 1:100, 4] <- 128 / 255
source[61:70, 1:100, 1:3] <- 0
source[61:70, 1:100, 4] <- 0 # Invisible black must become white.
png::writePNG(source, input)
before <- readBin(input, "raw", file.info(input)$size)
run <- function(...) system2(file.path(R.home("bin"), "Rscript"),
  c("--vanilla", shQuote(script), shQuote(c(...))), stdout = TRUE, stderr = TRUE)
result <- run(input, stem)
stopifnot(is.null(attr(result, "status")))
names <- c("original", "grayscale", "protan", "deutan", "tritan", "comparison")
paths <- setNames(paste0(stem, "_", names, ".png"), names)
stopifnot(all(file.exists(paths)),
          identical(before, readBin(input, "raw", file.info(input)$size)),
          identical(before, readBin(paths["original"], "raw", file.info(paths["original"])$size)))
views <- lapply(paths, png::readPNG)
stopifnot(all(vapply(views[1:5], function(x) identical(dim(x)[1:2], c(70L, 360L)), logical(1))),
          identical(dim(views$original), c(70L, 360L, 4L)))
for (name in names[2:5]) {
  stopifnot(all(views[[name]][10, 10, ] == 128 / 255),
            all(views[[name]][65, 10, ] == 1))
}
# Representative full-severity Machado/colorspace values for opaque red.
expected <- list(protan = c(109, 95, 0), deutan = c(163, 144, 0), tritan = c(255, 0, 15))
for (name in names(expected)) stopifnot(all(round(255 * views[[name]][30, 10, ]) == expected[[name]]))
stopifnot(all(views$grayscale[, , 1] == views$grayscale[, , 2]),
          all(views$grayscale[, , 2] == views$grayscale[, , 3]))
# Exact tile content catches rescaling, transposition and changed alpha compositing.
stopifnot(identical(dim(views$comparison)[1:2], c(400L, 1080L)))
original_tile <- views$comparison[41:110, 1:360, 1:3]
for (channel in 1:3) {
  expected <- round(255 * (source[, , channel] * source[, , 4] + 1 - source[, , 4])) / 255
  stopifnot(all(original_tile[, , channel] == expected))
}
stopifnot(all(views$comparison[41:110, 361:720, 1:3] == views$grayscale),
          any(views$comparison[1:40, , 1:3] < 0.5))
refused <- suppressWarnings(run(input, stem))
stopifnot(identical(attr(refused, "status"), 1L),
          identical(before, readBin(input, "raw", file.info(input)$size)))
cat("Rendered colour preview checks passed:", paths["comparison"], "\n")
