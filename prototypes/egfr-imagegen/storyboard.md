# EGF–EGFR–RAS–RAF–MEK–ERK

Audience: biomedical researchers using a clear mechanism figure with optional event animation.

Goal: connect an extracellular growth-factor input to the activated ERK endpoint while preserving receptor topology, GRB2–SOS association and the RAS nucleotide switch.

| Phase | Change shown | Main visual argument | Source key |
|---|---|---|---|
| EGF binding | Two EGF instances contact two EGFR ectodomains | Ligand recognition occurs outside the cell | ogiso |
| Receptor dimer | Domain-II contact anchors align; bound EGF moves with EGFR | Receptor association connects the extracellular input to intracellular signaling | ogiso, zhang |
| Tail phosphorylation | Representative pY state appears at the recruitment tail | Tail state supplies docking sites, while kinase asymmetry is stated in the caption | zhang |
| GRB2–SOS recruitment | A prelinked GRB2–SOS1 complex docks through GRB2 SH2 | Adaptor interactions bring the exchange factor to membrane RAS | grb2 |
| RAS exchange | GDP leaves, GTP is loaded; RAS remains membrane anchored | Exchange changes a nucleotide state, not GDP phosphorylation | sos |
| RAF recruitment | RAF regulatory region binds RAS–GTP | Effector recruitment is distinct from catalytic activation | rasraf |
| RAF activation | Aggregate active-state mark appears | Dimer/regulatory assembly is combined into this step | rafreg |
| RAF→MEK | A transient encounter changes MEK state, then releases MEK | Catalytic relay retains substrate identity | rafmek |
| MEK→ERK | Transient contact leaves ERK with pT/pY state | The canonical core reaches activated ERK | mekerK |

`references.json` records sources and reading scope. `mechanism.json` records entities, initial complex membership, events, dependencies and presentation timing. The 42-second sequence is one teaching arrangement; the static final diagram is the primary figure. The optional EGFR-kinase block keeps ligand binding and receptor association while removing the downstream core events. It is a diagram-level comparison, not a drug-response simulation.
