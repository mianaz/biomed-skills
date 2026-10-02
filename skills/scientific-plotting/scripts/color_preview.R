# Diagnostic PNG views at native pixel size. The original copy retains alpha;
# previews assume sRGB, composite on white and use 8-bit RGB. No pass/fail.
args <- commandArgs(trailingOnly = TRUE)
if (identical(args, "--help")) {
  cat("Usage: Rscript --vanilla color_preview.R input.png output_prefix\n",
      "Writes original, grayscale, protan, deutan, tritan and comparison PNGs.\n",
      "Input/original copy unchanged; diagnostic views use white-composited 8-bit RGB.\n",
      "Assumes sRGB PNG input.\n",
      "Native pixel dimensions are retained, including in the labelled comparison.\n",
      "CVD: colorspace severity=1, linear=TRUE; no accessibility pass/fail.\n", sep = "")
  quit(status = 0)
}
if (length(args) != 2L || any(!nzchar(args)))
  stop("Usage: Rscript --vanilla color_preview.R input.png output_prefix")
input <- args[1]
stem <- args[2]
if (!file.exists(input) || dir.exists(input) || !grepl("\\.png$", input, ignore.case = TRUE))
  stop("Input must be an existing PNG file.")
for (package in c("png", "colorspace", "ragg"))
  if (!requireNamespace(package, quietly = TRUE)) stop("Required package: ", package)
names <- c("original", "grayscale", "protan", "deutan", "tritan")
paths <- setNames(paste0(stem, "_", c(names, "comparison"), ".png"), c(names, "comparison"))
if (any(file.exists(paths))) stop("Output already exists; choose another prefix.")

image <- png::readPNG(input)
size <- dim(image)
if (length(size) < 2L || any(size[1:2] < 1L) ||
    (length(size) == 3L && !size[3] %in% 1:4)) stop("Unsupported PNG dimensions/channels.")
height <- size[1]
width <- size[2]
pixels <- matrix(image, nrow = height * width)
channels <- ncol(pixels)
alpha <- if (channels %in% c(2L, 4L)) pixels[, channels] else 1
rgb <- if (channels < 3L) pixels[, rep(1L, 3L), drop = FALSE] else pixels[, 1:3, drop = FALSE]
rgb <- rgb * alpha + (1 - alpha)
hex <- grDevices::rgb(rgb[, 1], rgb[, 2], rgb[, 3])
colours <- unique(hex)
index <- match(hex, colours)
views <- list(original = colours, grayscale = colorspace::desaturate(colours),
              protan = colorspace::protan(colours, severity = 1, linear = TRUE),
              deutan = colorspace::deutan(colours, severity = 1, linear = TRUE),
              tritan = colorspace::tritan(colours, severity = 1, linear = TRUE))

dir.create(dirname(stem), recursive = TRUE, showWarnings = FALSE)
if (!file.copy(input, paths["original"], overwrite = FALSE)) stop("Could not copy original PNG.")
for (name in names[-1]) {
  pixels <- t(grDevices::col2rgb(views[[name]][index])) / 255
  png::writePNG(array(pixels, c(height, width, 3L)), paths[name])
}

# Keep every source pixel; padding makes labels readable even for tiny inputs.
label_size <- max(11, width / 55)
label_height <- max(40L, ceiling(label_size * 8 / 3))
cell_width <- max(width, 320L)
cell_height <- max(height + label_height, 200L)
sheet_width <- 3L * cell_width
sheet_height <- 2L * cell_height
ragg::agg_png(paths["comparison"], width = sheet_width, height = sheet_height,
              units = "px", res = 96, background = "white")
grid::grid.newpage()
labels <- c("Original (white background)", "Grayscale", "Protan (severity 1)",
            "Deutan (severity 1)", "Tritan (severity 1)")
for (i in seq_along(names)) {
  left <- ((i - 1L) %% 3L) * cell_width
  top <- ((i - 1L) %/% 3L) * cell_height
  grid::grid.text(labels[i], x = (left + 12) / sheet_width,
                  y = 1 - (top + label_height / 2) / sheet_height, just = "left",
                  gp = grid::gpar(fontfamily = "Arial", fontsize = label_size))
  grid::grid.raster(matrix(views[[i]][index], height, width),
                    x = (left + floor((cell_width - width) / 2)) / sheet_width,
                    y = 1 - (top + label_height) / sheet_height,
                    width = width / sheet_width, height = height / sheet_height,
                    just = c("left", "top"), interpolate = FALSE)
}
grid::grid.text(paste("Diagnostic views: native pixels (1:1)",
                      "Alpha composited on white; 8-bit RGB",
                      "sRGB input; CVD severity 1; linear RGB",
                      paste("colorspace", utils::packageVersion("colorspace")),
                      "Review labels, lines and group identity.",
                      "No accessibility pass/fail.", sep = "\n"),
                x = (2 * cell_width + 12) / sheet_width,
                y = 1 - (cell_height + 20) / sheet_height,
                just = c("left", "top"),
                gp = grid::gpar(fontfamily = "Arial", fontsize = label_size, lineheight = 1.3))
invisible(grDevices::dev.off())
cat("Colour previews written:", paths["comparison"], "\n")
