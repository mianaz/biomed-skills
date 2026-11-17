script <- sub('^--file=', '', grep('^--file=', commandArgs(), value = TRUE)[1])
skill <- normalizePath(file.path(dirname(script), '../../../..'))
source(file.path(skill, 'examples/native-representative-cases.R'))
render_representative_case('cumulative-incidence', 'input.csv', '.', NULL, NULL)
