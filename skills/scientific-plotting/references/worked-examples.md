# Worked figure decisions

Use the matching pattern to connect an experimental question, analysis and readable
display. These patterns are development examples, not universal test assignments or
evidence that the skill outperforms another method. Preserve the user's task scope.

The [visual gallery](visual-gallery.md) links each pattern to an actual preview and
portable R source. Use it when choosing or adapting the figure's appearance.

| Situation and question | Analysis and figure decision | What establishes a complete result |
|---|---|---|
| Independent assay groups: how much does treatment change the response? | When mean-based inference is justified, estimate treatment minus reference with a Welch interval/test. For several justified contrasts, define the correction family first. Show independent observations with the defined center/spread. | Group identities, independent n, effect direction, uncertainty, complete results and keyed annotations agree. Reordering rows leaves results unchanged. |
| Paired assay: how did the same units change? | Join by stable unit ID, display matched points/lines and analyze within-unit changes. Specify the treatment of incomplete pairs. | Every line joins the same unit; the analysis uses the matching rather than row order. Save both measurements and differences. |
| Repeated measurement: how do trajectories differ? | Keep true sampling times and unit identities. Use a supported repeated-measures model for the trajectory question; draw individual paths or defined summaries and uncertainty. | The model represents repeated units and the claimed term; time-point contrasts do not stand in for a treatment-by-time interaction. Save unique observations and model results. |
| Dose response: what response and potency does the tested range support? | Follow `dose-response.md` for model choice, identifiability and uncertainty. Show observations and the supported fitted curve on the actual concentration scale, with zero controls handled explicitly. | Save parameter estimates, intervals, residuals and model diagnostics. Report extrapolated or unidentified potency as such; a joining line is not a fitted dose model. |
| Time to event: how does event-free follow-up differ? | Define the event and time origin from metadata, retain censor indicators, and draw Kaplan–Meier steps with censor marks. Use a named survival comparison when the design supports it. | Risk counts, events/censors and step coordinates agree with source data. Distinguish endpoint type and test method; add a risk table when it informs the comparison. |
| Heatmap: how do the supplied features vary across samples? | Preserve sample/feature identities, distinguish zero from missing, and label transformations. Save the exact matrix and displayed order. Scaling within features changes the reading task. | Color values and limits match the saved matrix. Gene/protein labels retain their meaning; any gene-set score includes the full membership and scoring record in `figure-delivery.md`. |

Keep a compact source-to-result package: direct data, analysis/plotting code, editable
object, vector figure, preview and caption. For an appearance repair, reuse that
package and change only the requested properties. A successful development example
establishes that its particular workflow and rendered output were checked; broader
performance requires independent evaluation.
