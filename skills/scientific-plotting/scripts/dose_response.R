# Conditional unweighted Gaussian fits for one dose-response series.
# The caller supplies design-valid observations; this does not establish independence.
dose_response_candidates <- function(dose, response, level = 0.95) {
  stopifnot(is.numeric(dose), is.numeric(response), length(dose)==length(response),
    length(dose)>1, all(is.finite(dose)), all(is.finite(response)), all(dose>0),
    level>0, level<1)
  if(!requireNamespace("drc",quietly=TRUE)) stop("Install/use an available validated dose-response engine; drc is unavailable.")
  d <- data.frame(dose=dose,response=response); n<-nrow(d)
  models <- list(constant=stats::lm(response~1,d))
  attempts <- list(); comparison <- list(); parameters <- list(); predictions <- list(); residuals <- list()
  for(family in c("4PL","5PL")) {
    starts <- list(NULL)
    if(family=="4PL") {
      direction <- if(sum((log(dose)-mean(log(dose)))*(response-mean(response)))>0)-1 else 1
      for(slope in c(1,3)) for(mid in quantile(log(dose),c(.3,.7)))
        starts[[length(starts)+1]] <- c(direction*slope,min(response),max(response),mid)
    } else if(!is.null(models[["4PL"]])) {
      for(asymmetry in c(.5,1,2)) starts[[length(starts)+1]] <- c(unname(coef(models[["4PL"]])),asymmetry)
    }
    trial <- lapply(starts,function(start) {
      messages <- character()
      fit <- withCallingHandlers(tryCatch(drc::drm(response~dose,data=d,
        fct=if(family=="4PL")drc::LL2.4()else drc::LL2.5(),start=start,
        control=drc::drmc(maxIt=1500,noMessage=TRUE)),error=function(e)e),
        warning=function(w){messages<<-c(messages,conditionMessage(w));invokeRestart("muffleWarning")})
      list(fit=fit,warnings=unique(messages))
    })
    valid <- vapply(trial,function(t) inherits(t$fit,"drc") && isTRUE(t$fit$fit$convergence) &&
      all(is.finite(coef(t$fit))) && (family=="4PL" || coef(t$fit)[5]>0),logical(1))
    attempts[[family]] <- trial
    if(any(valid)) {
      eligible <- trial[valid]
      best <- which.min(vapply(eligible,function(t)sum(stats::residuals(t$fit)^2),numeric(1)))
      models[[family]] <- eligible[[best]]$fit
    }
  }
  for(family in c("constant","4PL","5PL")) {
    m <- models[[family]]
    row <- data.frame(model=family,n_records=n,n_doses=length(unique(dose)),converged=!is.null(m),
      rss=NA_real_,rmse=NA_real_,aicc=NA_real_,relative_ed50=NA_real_,ed50_low=NA_real_,ed50_high=NA_real_,
      midpoint_in_range=FALSE,interval_in_range=FALSE,covariance_ok=FALSE,
      covariance_condition=NA_real_,note="No converged candidate; inspect attempts")
    if(!is.null(m)) {
      cf<-coef(m);k<-length(cf)+1;rss<-sum(stats::residuals(m)^2)
      row$rss<-rss;row$rmse<-sqrt(rss/n)
      row$aicc<-if(n>k+1)AIC(m)+2*k*(k+1)/(n-k-1)else NA_real_
      v<-tryCatch(vcov(m),error=function(e)NULL)
      row$covariance_ok<-!is.null(v)&&all(is.finite(v))&&all(diag(v)>0)&&
        min(eigen(v,symmetric=TRUE,only.values=TRUE)$values)>0
      row$note<-if(row$covariance_ok)"Conditional assay-error approximation; inspect coverage, residuals and stability"else "Unstable covariance; interval unavailable"
      se<-rep(NA_real_,length(cf))
      if(row$covariance_ok) {
        se<-sqrt(diag(v));row$covariance_condition<-kappa(cov2cor(v))
      }
      critical<-if(n>length(cf))qt((1+level)/2,n-length(cf))else NA_real_
      parameters[[family]]<-data.frame(model=family,parameter=names(cf),estimate=unname(cf),
        se=se,low=cf-critical*se,high=cf+critical*se,
        interval_method="Wald-t in fitted parameterization; e is natural-log location for LL2 models")
      if(family!="constant") {
        asymmetry<-if(family=="5PL")unname(cf[5])else 1
        a<-log(2)/asymmetry
        log_shift<-if(a>50)a+log1p(-exp(-a))else log(expm1(a))
        log_ed50<-cf[4]+log_shift/cf[1]
        row$relative_ed50<-exp(log_ed50)
        if(is.finite(row$relative_ed50)&&row$relative_ed50>0) {
          midpoint<-predict(m,data.frame(dose=row$relative_ed50))
          stopifnot(abs(midpoint-(cf[2]+cf[3])/2)<1e-5*max(1,abs(cf[2]),abs(cf[3])))
        }
        if(row$covariance_ok) {
          # drc 3.0-1 LL2.5 ED derivative is incorrect; propagate the inverted curve directly.
          gradient<-c(-log_shift/cf[1]^2,0,0,1)
          if(family=="5PL") gradient<-c(gradient,-log(2)/(cf[1]*asymmetry^2*(-expm1(-a))))
          variance<-as.numeric(crossprod(gradient,v%*%gradient))
          if(is.finite(log_ed50)&&is.finite(variance)&&variance>=0&&is.finite(critical)) {
            ci<-exp(log_ed50+c(-1,1)*critical*sqrt(variance))
            row$ed50_low<-ci[1];row$ed50_high<-ci[2]
          }
        }
        row$midpoint_in_range<-is.finite(row$relative_ed50)&&row$relative_ed50>=min(dose)&&row$relative_ed50<=max(dose)
        row$interval_in_range<-is.finite(row$ed50_low)&&is.finite(row$ed50_high)&&row$ed50_low>=min(dose)&&row$ed50_high<=max(dose)
      }
      g<-data.frame(dose=exp(seq(log(min(dose)),log(max(dose)),length.out=150)))
      g$fitted<-as.numeric(predict(m,g));g$low<-NA_real_;g$high<-NA_real_
      if(row$covariance_ok) {
        pr<-tryCatch(suppressWarnings(predict(m,g,interval="confidence",level=level)),error=function(e)NULL)
        if(!is.null(pr)) {g$low<-pr[,2];g$high<-pr[,3]}
      }
      g$model<-family;predictions[[family]]<-g
      residuals[[family]]<-data.frame(model=family,d,fitted=as.numeric(fitted(m)),residual=as.numeric(stats::residuals(m)))
    }
    comparison[[family]]<-row
  }
  list(models=models,comparison=do.call(rbind,comparison),parameters=do.call(rbind,parameters),
    predictions=do.call(rbind,predictions),residuals=do.call(rbind,residuals),attempts=attempts,
    interval_method=paste(level*100,"percent pointwise conditional Gaussian mean-response CI; ED50 uses back-transformed log-Wald-t CI with analytic inverse-curve gradient"))
}
