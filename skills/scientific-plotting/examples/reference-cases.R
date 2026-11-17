# Synthetic input shapes; each also runs with changed data and labels.
script <- sub('^--file=', '', grep('^--file=', commandArgs(), value = TRUE)[1])
skill <- normalizePath(file.path(dirname(script), '..'))
library(ggplot2)
library(tidyplots)
source(file.path(skill, 'scripts/compact.R'))
source(file.path(skill, 'scripts/tidyplots.R'))
source(file.path(skill, 'scripts/dose_response.R'))
source(file.path(skill, 'examples/nested-replicates.R'))

render_case <- function(case, d, out) {
  if (case == 'nested') render_nested_case(d, out) else render_native_case(case, d, out)
}

args <- commandArgs(trailingOnly=TRUE)
if (length(args)==3) {
  columns <- if (args[1]=='nested') c(unit='character',group='character',subsample='character',observation='character') else NA
  render_case(args[1],read.csv(args[2],check.names=FALSE,colClasses=columns),args[3])
} else if (length(args)==1) {
  dir.create(args[1],recursive=TRUE,showWarnings=FALSE)
  base <- data.frame(unit=paste0('U',1:16),group=rep(c('Control','Drug'),each=8),
    value=c(9,11,8,10,12,10,9,11,12,15,13,16,14,13,17,15))
  paired <- data.frame(unit=rep(paste0('P',1:6),2),condition=rep(c('Before','After'),each=6),
    value=c(6,8,7,10,9,7,9,10,11,12,11,10))
  repeated <- expand.grid(time=c(0,1,4,9),unit=paste0('R',1:6))
  repeated$group <- rep(rep(c('Control','Drug'),each=3),each=4)
  repeated$value <- 8+as.integer(factor(repeated$unit))*.4+repeated$time*ifelse(repeated$group=='Drug',.6,.15)
  repeated$value[6] <- NA
  independent_time <- repeated;independent_time$unit <- paste0('T',seq_len(nrow(repeated)));independent_time$value[6] <- 10
  factorial <- expand.grid(genotype=c('WT','KO'),treatment=c('Vehicle','Drug'),replicate=1:5)
  factorial$unit <- paste0('F',1:nrow(factorial));factorial$value <- 10+2*(factorial$genotype=='KO')+3*(factorial$treatment=='Drug')+rep(c(-1,.5,0,1,-.5),each=4)
  factorial$replicate <- NULL
  dose <- expand.grid(replicate=1:3,dose=c(.01,.04,.16,.63,2.5,10,40,160))
  dose$response <- 5+95/(1+(dose$dose/1.6)^1.15)+rep(c(-1.2,.4,1),8)
  survival <- data.frame(unit=paste0('S',1:24),group=rep(c('Control','Drug'),each=12),
    time=c(4,5,7,8,10,11,14,17,19,21,24,24,7,11,13,16,18,20,22,24,24,24,24,24),event=c(rep(1,9),rep(0,3),rep(1,6),rep(0,6)))
  composition <- expand.grid(sample=paste0('S',1:6),category=c('Type A','Type B','Type C'))
  composition$group <- ifelse(composition$sample %in% paste0('S',1:3),'Control','Drug')
  composition$count <- c(14,17,15,9,8,10,5,3,5,9,12,10,1,2,0,2,0,1)
  heatmap <- expand.grid(feature=paste0('Gene ',LETTERS[1:5]),sample=paste0('S',1:6))
  heatmap$group <- rep(rep(c('Control','Drug'),each=3),each=5)
  heatmap$value <- c(12,35,8,20,50,14,30,11,18,54,11,33,9,22,48,24,17,10,40,34,28,20,9,43,30,25,18,12,38,32)
  nested <- expand.grid(unit=base$unit,subsample=paste0('S',1:3),observation=paste0('O',1:4))
  nested$group <- base$group[match(nested$unit,base$unit)]
  nested$value <- base$value[match(nested$unit,base$unit)]+rep(c(-1,0,1),each=16,times=4)+rep(c(-.6,-.2,.2,.6),each=48)
  cases <- list(independent=base,nested=nested,paired=paired,repeated=repeated,'independent-time'=independent_time,
    factorial=factorial,'dose-response'=dose,distribution=base,
    forest=data.frame(contrast=c('Drug A','Drug B','Drug C'),estimate=c(.7,1.5,2.2),lower=c(.5,1.1,1.5),upper=c(.95,2,3.4)),
    survival=survival,composition=composition,heatmap=heatmap,
    enrichment=data.frame(term=c('Cell cycle','DNA repair','Stress response','Metabolism'),count=c(18,12,9,6),padj=c(.00001,.0001,.001,.03)))
  for (case in names(cases)) {
    d <- cases[[case]];render_case(case,d,file.path(args[1],case,'original'))
    if ('value' %in% names(d)) d$value <- d$value*1.15+.4
    if ('response' %in% names(d)) d$response <- d$response*.91+2
    if ('group' %in% names(d)) d$group <- ifelse(d$group=='Control','Vehicle','Treated')
    if (case=='paired') d$condition <- ifelse(d$condition=='Before','Baseline','Follow-up')
    if (case=='repeated') d$value[14] <- NA
    if (case=='independent') d <- d[-2,]
    if (case=='nested') d <- d[-seq(1, nrow(d), 7),]
    if (case=='independent-time') d$time[d$time==4] <- 5
    if (case=='factorial') d$treatment <- ifelse(d$treatment=='Drug','Treated','Vehicle')
    if (case=='forest') {d[c('estimate','lower','upper')] <- d[c('estimate','lower','upper')]*1.2;d$contrast[1] <- 'Treatment A'}
    if (case=='survival') {d$time <- d$time*1.2;d$event[3] <- 0}
    if (case=='composition') d$count <- d$count+c(1,0,2)
    if (case=='heatmap') d$value[1] <- d$value[1]+20
    if (case=='enrichment') {d$padj <- d$padj*.5;d$term[4] <- 'Energy metabolism'}
    render_case(case,d,file.path(args[1],case,'replacement'))
  }
  writeLines(capture.output(sessionInfo()),file.path(args[1],'session-info.txt'))
} else stop('Use: reference-cases.R OUTPUT_DIR; or reference-cases.R CASE INPUT.csv OUTPUT_DIR')

