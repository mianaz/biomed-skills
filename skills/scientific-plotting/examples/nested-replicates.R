# Measurements within subsamples within independent biological units.
nested_script <- sub('^--file=', '', grep('^--file=', commandArgs(), value = TRUE)[1])
nested_file <- if (sys.nframe() > 0) sys.frame(1)$ofile else nested_script
nested_skill <- normalizePath(file.path(dirname(nested_file), '..'))
source(file.path(nested_skill, 'examples/native-reference-cases.R'))

render_nested_case <- function(d, out) {
  stopifnot(all(c('unit','group','subsample','observation','value') %in% names(d)),
    !anyNA(d[c('unit','group','subsample','observation','value')]),
    all(is.finite(d$value)), !anyDuplicated(d[c('unit','subsample','observation')]),
    all(vapply(split(d$group, d$unit), function(x) length(unique(x)) == 1L, logical(1))))
  subsamples <- aggregate(value ~ unit + group + subsample, d, mean)
  counts <- aggregate(value ~ unit + group + subsample, d, length)
  names(counts)[4] <- 'n_observations'
  subsamples <- merge(subsamples, counts, by = c('unit','group','subsample'))
  units <- aggregate(value ~ unit + group, subsamples, mean)
  units <- units[order(match(units$group, unique(d$group)), units$unit), ]
  render_native_case('independent', units, out)
  write.csv(d, file.path(out, 'measurements.csv'), row.names = FALSE)
  write.csv(subsamples, file.path(out, 'subsample-means.csv'), row.names = FALSE)
  write.csv(units, file.path(out, 'unit-means.csv'), row.names = FALSE)
  caption <- sub('^Synthetic demonstration data\\. ', '',
    readLines(file.path(out, 'caption.txt')))
  writeLines(c('Nested measurements: observations are averaged within each subsample, then subsample means receive equal weight within each biological unit.',
    'Bars, SD, points and the Welch comparison use biological-unit means. n counts biological units.',
    caption), file.path(out, 'caption.txt'))
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  render_nested_case(read.csv(args[1], colClasses = c(unit='character',group='character',
    subsample='character',observation='character')), args[2])
}
