# Run from the repository root; optional first argument selects the output directory.
library(ggplot2)
source("skills/create-scientific-figures/scripts/compact.R")
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args)) args[1] else tempfile("figure-typography-r-")
dir.create(out, recursive = TRUE, showWarnings = FALSE)
keyed <- c(missing=NA_real_, change=0.0144, unchanged=0.7)
hidden <- p_labels(keyed, adjusted=TRUE, missing_label="n.e.")
stopifnot(identical(hidden, c(missing="n.e.", change="P adj. = 0.014", unchanged="")),
          identical(p_labels(keyed, TRUE, "n.e.", "ns"), replace(hidden, 3, "ns")),
          identical(p_labels(keyed, TRUE, "n.e.", "value"), replace(hidden, 3, "P adj. = 0.7")),
          identical(p_labels(c(0.05, 0.04999999)), c("", "P < 0.05")),
          identical(p_labels(c(0.01, 0.00999999), alpha=0.01), c("", "P = 0.00999999")),
          identical(p_labels(c(0.0499, 0.0501, 0.05000001, 0.05), nonsignificant="value"),
                    c("P = 0.0499", "P = 0.0501", "P > 0.05", "P = 0.05")),
          identical(p_labels(c(5e-7, 1e-6, 1.0000000001e-6, 2e-6), alpha=1e-6, nonsignificant="value"),
                    c("P < 1e-06", "P = 1e-06", "P > 1e-06", "P = 2e-06")),
          identical(p_labels(0.123456789, alpha=0.123456789, nonsignificant="value"), "P = 0.123456789"),
          identical(p_labels(c(NA_real_, NaN), missing_label="n.e.", nonsignificant="ns"), c("n.e.", "n.e.")),
          identical(p_labels(numeric()), character()))
for (value in list(NA_real_, Inf, -0.1, 1.1))
  stopifnot(inherits(try(p_labels(value), silent=TRUE), "try-error"))
for (options in list(list(nonsignificant="stars"), list(alpha=0), list(alpha=1), list(alpha=NaN)))
  stopifnot(inherits(try(do.call(p_labels, c(list(p=0.1), options)), silent=TRUE), "try-error"))
annotations <- data.frame(comparison=names(keyed), x1=c(2,0,30), x2=c(3,1,40),
                          y=c(2,1.5,900), p=c(NA,0.001,0.001), p_holm=unname(keyed))
annotations <- annotations[c(3,1,2), ]
base <- ggplot(data.frame(x=0:1, y=0:1), aes(x,y)) + geom_point()
for (mode in c("hide", "ns", "value")) {
  layers <- p_brackets(annotations, p_col="p_holm", adjusted=TRUE,
                       missing_label="n.e.", nonsignificant=mode)
  expected <- if (mode == "hide") c("missing", "change") else c("unchanged", "missing", "change")
  stopifnot(identical(layers[[1]]$data$comparison, expected))
  built <- ggplot_build(base + layers)
  expected_labels <- if (mode == "hide") c("n.e.", "P adj. = 0.014") else
    c(if (mode == "ns") "ns" else "P adj. = 0.7", "n.e.", "P adj. = 0.014")
  stopifnot(identical(built$data[[5]]$label, expected_labels),
            identical(tail(built$data[[5]]$x,2), c(2.5,0.5)))
  stopifnot(if (mode == "hide") built$layout$panel_params[[1]]$y.range[2] < 3 else
              built$layout$panel_params[[1]]$y.range[2] > 900)
}
all_ns <- p_brackets(annotations[1, ], p_col="p_holm")
repeated_ns <- data.frame(x1=1:5 - 0.2, x2=1:5 + 0.2, y=900, p_holm=rep(0.18, 5))
stopifnot(identical(p_brackets(repeated_ns, p_col="p_holm", adjusted=TRUE), list()),
          identical(ggplot_build(base + p_brackets(repeated_ns, p_col="p_holm"))$layout$panel_params[[1]]$y.range,
                    ggplot_build(base)$layout$panel_params[[1]]$y.range))
stopifnot(identical(all_ns, list()),
          identical(p_brackets(transform(annotations[1, ], label="")), list()),
          identical(ggplot_build(base + all_ns)$layout$panel_params[[1]]$y.range,
                    ggplot_build(base)$layout$panel_params[[1]]$y.range))
annotations$label <- p_labels(annotations$p_holm, TRUE, "n.e.", "value")
stopifnot(inherits(try(p_brackets(annotations, p_col="p_holm", adjusted=TRUE,
                                 missing_label="n.e."), silent=TRUE), "try-error"))
labels <- data.frame(
  context = c("Human gene", "Human protein", "Mouse gene", "Mouse protein",
              "Protein name", "Concentration", "Chemical", "Potency",
              "Log base", "Rate unit", "Genotype", "Greek letters"),
  label = c('italic("TP53")', 'plain("TP53")', 'italic("Trp53")',
            'plain("TRP53")', 'plain("β-catenin")', 'plain("Ca")^{plain("2+")}*plain(" (μM)")',
            'plain("H")[2]*plain("O")', 'plain("IC")[50]', 'plain("log")[2]',
            'plain("s")^{plain("−1")}', 'italic("Trp53")^{plain("−/−")}',
            'plain("α β γ δ Δ")'),
  y = 12:1)
write.csv(labels, file.path(out, "labels.csv"), row.names = FALSE)
p <- ggplot(labels, aes(y = y)) +
  geom_text(aes(x = 0, label = context), hjust = 0, family = "Arial", size = 11, size.unit = "pt") +
  geom_text(aes(x = 0.52, label = label), parse = TRUE, hjust = 0,
            family = "Arial", size = 16, size.unit = "pt") +
  scale_x_continuous(limits = c(0, 1.15), expand = expansion(0)) +
  scale_y_continuous(limits = c(0.3, 12.7), expand = expansion(0)) +
  biomedical_theme() + theme(axis.line = element_blank(), axis.ticks = element_blank(),
                            axis.text.x = element_blank(), axis.text.y = element_blank(),
                            axis.title = element_blank())
stem <- file.path(out, "typography_r")
export_biomedical(p, stem, width_mm = 90, height_mm = 100, placed_width_mm = 90)
txt <- pdftools::pdf_data(paste0(stem, ".pdf"), font_info = TRUE)[[1]]
stopifnot(all(grepl("Arial", txt$font_name)), min(txt$font_size) > 10,
          nrow(subset(txt, text == "TP53" & grepl("Italic", font_name))) == 1,
          nrow(subset(txt, text == "TP53" & !grepl("Italic", font_name))) == 1,
          nrow(subset(txt, text == "Trp53" & grepl("Italic", font_name))) == 2,
          all(c("β-catenin", "(μM)", "α", "β", "γ", "δ", "Δ", "−1", "−/−") %in% txt$text))
stopifnot(txt$y[txt$text == "2+"] < txt$y[txt$text == "Ca"],
          txt$y[txt$text == "50"] > txt$y[txt$text == "IC"],
          abs(txt$font_size[txt$text == "2+"] - 11.2) < 0.05,
          abs(txt$font_size[txt$text == "50"] - 11.2) < 0.05)
small <- p
small$layers[[2]]$aes_params$size <- 14
failure <- tryCatch({export_biomedical(small, file.path(out, "small_scripts"), 90, 100); NULL},
                    error = identity)
stopifnot(inherits(failure, "error"), grepl("at or below 10 pt", conditionMessage(failure)))
fallback <- p + annotate("text", x = 0.8, y = 0.5, label = "font", family = "Courier", size = 11, size.unit = "pt")
failure <- tryCatch({export_biomedical(fallback, file.path(out, "wrong_font"), 90, 100); NULL},
                    error = identity)
stopifnot(inherits(failure, "error"), grepl("non-Arial", conditionMessage(failure)))
cat("R typography checks passed:", stem, "\n")
