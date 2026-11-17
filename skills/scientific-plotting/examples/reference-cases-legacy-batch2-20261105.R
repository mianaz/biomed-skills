# Twelve synthetic input shapes; each also runs with changed data and labels.
script <- sub('^--file=', '', grep('^--file=', commandArgs(), value = TRUE)[1])
skill <- normalizePath(file.path(dirname(script), '..'))
library(ggplot2)
library(tidyplots)
source(file.path(skill, 'scripts/compact.R'))
source(file.path(skill, 'scripts/tidyplots.R'))
source(file.path(skill, 'scripts/dose_response.R'))
source(file.path(skill, 'examples/native-reference-cases.R'))

render_case <- function(case, d, out) {
  if (case %in% c('independent', 'forest', 'heatmap')) return(render_native_case(case, d, out))
  dir.create(out, recursive = TRUE, showWarnings = FALSE)
  write.csv(d, file.path(out, 'input.csv'), row.names = FALSE, na = '')
  groups <- if ('group' %in% names(d)) unique(d$group) else c('Control', 'Drug')
  if ('group' %in% names(d)) d$group <- factor(d$group, levels=groups)
  pal <- biomedical_palette(groups, control = groups[1])
  theme <- biomedical_theme(12) + theme(legend.position = 'top',
    legend.text = element_text(size = 11), legend.key.width = grid::unit(3, 'mm'))
  width <- 76; height <- 74
  if (case == 'paired') {
    stopifnot(!anyDuplicated(d[c('unit','condition')]), all(table(d$unit) == 2))
    d$condition <- factor(d$condition, levels = unique(d$condition))
    pal <- biomedical_palette(levels(d$condition), control = levels(d$condition)[1])
    d$position <- as.numeric(d$condition) + seq(-.08,.08,length.out=length(unique(d$unit)))[match(d$unit,unique(d$unit))]
    p <- ggplot(d, aes(position, value, group = unit)) + geom_line(colour = 'grey70', linewidth = .4) +
      geom_point(aes(colour = condition), size = 2) + scale_colour_manual(values = pal, guide = 'none') +
      scale_x_continuous(breaks=1:2,labels=levels(d$condition),limits=c(.6,2.4)) +
      labs(x = NULL, y = 'Response (a.u.)') + theme
  } else if (case == 'repeated') {
    stopifnot(!anyDuplicated(d[c('unit','time')]))
    d <- d[order(d$unit,d$time), ]
    d$segment <- ave(is.na(d$value), d$unit, FUN = cumsum)
    visible <- d[!is.na(d$value), ]
    p <- ggplot(visible, aes(time,value,colour=group)) +
      geom_line(aes(group=interaction(unit,segment)), linewidth=.4, alpha=.6) + geom_point(size=1.5) +
      facet_wrap(~group, nrow=1) + scale_colour_manual(values=pal,guide='none') +
      scale_x_continuous(breaks=sort(unique(d$time))) + labs(x='Day',y='Response (a.u.)') + theme
    write.csv(visible, file.path(out,'connected_segments.csv'), row.names=FALSE)
    width <- 102
  } else if (case == 'independent-time') {
    stopifnot(!anyDuplicated(d$unit))
    s <- aggregate(value ~ group + time,d,function(x)c(mean=mean(x),sd=sd(x)))
    s <- data.frame(s[1:2],s$value)
    p <- ggplot(s,aes(time,mean,colour=group)) +
      geom_errorbar(aes(ymin=mean-sd,ymax=mean+sd),width=.15,linewidth=.4) +
      geom_line(linewidth=.6) + geom_point(size=1.8) + scale_colour_manual(values=pal) +
      scale_x_continuous(breaks=sort(unique(d$time))) + labs(x='Day',y='Response (a.u.)') + theme
    write.csv(s,file.path(out,'summary.csv'),row.names=FALSE)
  } else if (case == 'factorial') {
    stopifnot(!anyDuplicated(d$unit))
    d$treatment <- factor(d$treatment,levels=unique(d$treatment))
    pal <- biomedical_palette(levels(d$treatment), control=levels(d$treatment)[1])
    p <- ggplot(d,aes(genotype,value,fill=treatment,colour=treatment)) +
      stat_summary(fun=mean,geom='col',position=position_dodge(.75),width=.6,alpha=.3) +
      stat_summary(fun.data=mean_sdl,fun.args=list(mult=1),geom='errorbar',position=position_dodge(.75),width=.18) +
      geom_point(position=position_jitterdodge(jitter.width=.12,dodge.width=.75,seed=12),size=1.7) +
      scale_colour_manual(values=pal)+scale_fill_manual(values=pal)+labs(x=NULL,y='Response (a.u.)')+theme
    width <- 86
  } else if (case == 'dose-response') {
    fit <- dose_response_candidates(d$dose,d$response)
    eligible <- subset(fit$comparison,converged & covariance_ok & midpoint_in_range & interval_in_range)
    stopifnot(nrow(eligible)>0)
    selected <- eligible$model[which.min(eligible$aicc)]
    g <- subset(fit$predictions,model==selected)
    p <- ggplot(d,aes(dose,response)) + geom_ribbon(data=g,aes(y=NULL,ymin=low,ymax=high),fill='#A6CEE3',alpha=.4) +
      geom_line(data=g,aes(y=fitted),colour='#1F78B4',linewidth=.65) + geom_point(size=1.5,colour='#1F78B4') +
      scale_x_log10(breaks=c(.01,.1,1,10,100),labels=c('.01','.1','1','10','100')) +
      labs(x='Dose (µM)',y='Response (%)') + theme
    for (field in c('comparison','parameters','predictions','residuals'))
      write.csv(fit[[field]],file.path(out,paste0(field,'.csv')),row.names=FALSE)
    saveRDS(fit,file.path(out,'models.rds'))
  } else if (case == 'distribution') {
    p <- ggplot(d,aes(group,value,colour=group)) + geom_boxplot(width=.5,outlier.shape=NA,linewidth=.45) +
      geom_point(position=position_jitter(width=.09,seed=12),size=1.4,alpha=.75) +
      scale_colour_manual(values=pal,guide='none') + labs(x=NULL,y='Response (a.u.)') + theme
  } else if (case == 'survival') {
    stopifnot(!anyDuplicated(d$unit),all(d$event %in% c(0,1)))
    f <- survival::survfit(survival::Surv(time,event)~group,d,conf.type='log-log')
    s <- summary(f,censored=TRUE)
    curve <- data.frame(time=s$time,survival=s$surv,low=s$lower,high=s$upper,n_risk=s$n.risk,
      censor=s$n.censor,group=sub('group=','',as.character(s$strata)))
    starts <- data.frame(time=0,survival=1,low=1,high=1,n_risk=as.numeric(table(d$group)),censor=0,group=names(table(d$group)))
    curve <- rbind(starts,curve);curve <- curve[order(curve$group,curve$time),]
    curve$group <- factor(curve$group,levels=groups)
    steps <- do.call(rbind,lapply(split(curve,curve$group),function(z) {
      rows <- z[rep(seq_len(nrow(z)),each=2),]
      rows$time <- c(0,rep(z$time[-1],each=2),tail(z$time,1))
      rows
    }))
    p <- ggplot(curve,aes(time,survival,colour=group)) +
      geom_ribbon(data=steps,aes(ymin=low,ymax=high,fill=group),colour=NA,alpha=.15) +
      scale_fill_manual(values=pal) + geom_step(linewidth=.65) +
      geom_point(data=subset(curve,censor>0),shape=3,size=2) + scale_colour_manual(values=pal) +
      scale_y_continuous(limits=c(0,1),breaks=c(0,.5,1)) + labs(x='Time (months)',y='Survival probability') + theme +
      theme(plot.margin=margin(2,4,2,2,unit='mm'))
    write.csv(curve,file.path(out,'survival_estimates.csv'),row.names=FALSE)
    saveRDS(f,file.path(out,'model.rds'))
    height <- 78
  } else if (case == 'composition') {
    stopifnot(!anyDuplicated(d[c('sample','category')]),all(d$count>=0))
    d$denominator <- ave(d$count,d$sample,FUN=sum);stopifnot(all(d$denominator>0))
    d$fraction <- d$count/d$denominator
    pal <- biomedical_palette(unique(d$category))
    p <- ggplot(d,aes(sample,fraction,fill=category)) + geom_col(width=.7) +
      facet_grid(.~group,scales='free_x',space='free_x') + scale_fill_manual(values=pal) +
      scale_y_continuous(limits=c(0,1),breaks=c(0,.5,1),expand=expansion(0)) +
      labs(x='Sample',y='Fraction') + theme
    write.csv(d,file.path(out,'fractions.csv'),row.names=FALSE)
    width <- 90
  } else if (case == 'enrichment') {
    stopifnot(all(d$padj>0 & d$padj<=1))
    d$neg_log10_padj <- -log10(d$padj)
    d$term <- factor(d$term,levels=rev(d$term))
    p <- ggplot(d,aes(neg_log10_padj,term)) + geom_col(width=.65,fill='#1F78B4') +
      labs(x=expression(-log[10](italic(P)[adj])),y=NULL) + theme +
      theme(axis.title.x=element_text(size=16))
    write.csv(d,file.path(out,'display_values.csv'),row.names=FALSE)
    width <- 108;height <- 76
  } else stop('Unknown case')
  export_biomedical(p,file.path(out,'figure'),width,height,width)
  write.csv(data.frame(group=names(pal),color=unname(pal)),file.path(out,'palette.csv'),row.names=FALSE)
  caption <- switch(case,
    paired='Matched units at two visits; lines connect the same unit ID.',
    repeated='Repeated observations; lines connect visits within unit ID and break at missing visits. Facets show groups.',
    'independent-time'='Different units at each time; points show group means and error bars show SD. Numeric time spacing is retained.',
    factorial='Independent units across two factors; bars show means, error bars show SD and points show units.',
    'dose-response'='Synthetic technical measurements from one assay; selected dose-response fit and 95% model confidence band. Model comparisons and conditional parameters are saved.',
    distribution='Independent units; boxes show median and quartiles, whiskers extend to 1.5 IQR and points show all units.',
    survival='One row per subject; Kaplan-Meier estimates with 95% log-log confidence intervals and censor marks. Risk counts and full estimates are saved.',
    composition='Each bar is one sample; segment fractions use that sample’s total count as denominator.',
    enrichment='Supplied adjusted P values displayed as minus log10. Term counts and complete source values are saved.')
  writeLines(paste('Synthetic demonstration data.', caption, 'Input rows:',nrow(d)),file.path(out,'caption.txt'))
}

args <- commandArgs(trailingOnly=TRUE)
if (length(args)==3) {
  render_case(args[1],read.csv(args[2],check.names=FALSE),args[3])
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
  cases <- list(independent=base,paired=paired,repeated=repeated,'independent-time'=independent_time,
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

