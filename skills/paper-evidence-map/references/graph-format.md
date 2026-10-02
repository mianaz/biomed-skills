# Evidence graph format

Write UTF-8 JSON with `title`, `paper`, `nodes` and `edges`. Use
[assets/example.json](../assets/example.json) as a concrete starting point.

`paper` has `citation`, `source` (PDF path or source link), and `read_scope`.
Record the DOI in the citation or source when available. The reading scope says
which text, figures, Methods and supplements were actually examined.

Each node has:

| Field | Meaning |
|---|---|
| `id` | Stable unique string, e.g. `C1`, `E1`, `R1` |
| `type` | `question`, `main_claim`, `subclaim`, `experiment`, `result`, `inference`, or `premise` |
| `text` | One short proposition or experiment title; one sentence is usually enough |
| `details` | Full interpretation or experimental detail, including context and units |
| `source` | Exact page, section, figure/panel, table, supplement or source link |
| `x`, `y` | Optional integer Canvas coordinates; supplied positions are preserved |

Write an unavailable value explicitly where it matters. Keep author statements,
measured observations and reader inferences distinguishable in `details`.
Experiments describe design and controls; results describe the observed readout.
An inference can be an author's working model or a reader's interpretation.

Each edge has `from`, `to`, `relation` and `reason`; `source` is optional when the
endpoints already carry the relevant references. Edges point as follows:

| Relation | Direction and meaning |
|---|---|
| `tests` | experiment → claim/inference; the design examines this proposition |
| `produces` | experiment → result; the experiment yielded this observation |
| `supports` | evidence or subclaim → claim/inference; explain the inferential bridge |
| `contradicts` | result → claim/inference; conflicts with its stated prediction or scope |
| `qualifies` | result/premise → claim/inference; narrows the interpretation |
| `depends_on` | dependent claim/inference → prerequisite; direction is toward what is needed |
| `part_of` | subclaim/inference → larger claim; expresses decomposition, without asserting support |
| `addresses` | central claim → research question; records the question it answers |

Use a real contradictory result only when it conflicts with the claim under the
relevant conditions. An inconclusive test or insensitive negative assay usually
qualifies a claim. Note the distinction in the edge's reason.

The evidence table has one row per result-to-claim evidence link and its producing
experiment. It retains separate rows for multiple producing experiments and for
shared results. Claims supported through other claims and experiments with no
available results remain visible in the node and relation sections.

The default visual places experiments, results, subclaims and the central claim
in four columns, with the research question above. Premises share the experiment
column and inferences share the subclaim column. Set `x`/`y` for a better layout
when cross-links warrant it. The preview shows the short node text; Canvas notes
and the evidence table retain the full details. Preview edges use the displayed
letter legend to keep labels readable; hover shows the relation and reason.
Canvas edges retain the complete relation names.

Keep `graph.json`, the editable Canvas and the evidence table together. After
Canvas edits, reconcile its node text and edges with the source JSON before
making a new rendered version. No software-specific paper-reading or model
service is needed to use this format.
