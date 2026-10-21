# Same observations. Different mechanisms.

Audience: scientifically literate reader new to causal models.

Learning goal: explain why two models can agree on observations yet predict
different outcomes after the same intervention.

| Scene | Reader's question | Visual change | Takeaway | Source |
|---|---|---|---|---|
| Observe | Does co-occurrence identify the mechanism? | Compare chain and shared-cause diagrams; vary signal prevalence. | Both toy models give X = Y = U during observation. | Original binary models, equations in the HTML source notes. |
| Intervene | What happens if X is forced off? | Dim the input arrows to X; update Y bars while retaining baseline labels. | The chain predicts Y = 0; the shared-cause model leaves Y = U. | Pearl 2009, section 3.2.1, equations 5–7; original worked example. |
| Explain | What information did the intervention add? | Retain both diagrams and state the difference; toggle back to baseline. | A comparison can distinguish these models under their stated assumptions. | Same section; the experiment note states the ideal-intervention assumptions. |

Source read: [Pearl, Causal inference in statistics: An overview (2009)](https://escholarship.org/content/qt36w8n7pg/qt36w8n7pg.pdf#page=12),
section 3.2.1, pp. 107–109. The example has no measured data. All displayed values
are calculated expectations from the two stated binary models.
