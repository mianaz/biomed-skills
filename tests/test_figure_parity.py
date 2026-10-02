"""Synthetic R/Python agreement check; no benchmark models or external data.

Run from the repository root with .venv-comparison-figures/bin/python.
"""
from pathlib import Path
import subprocess
import sys
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "skills/create-scientific-figures/scripts"))
from compact import biomedical_palette, p_labels, p_brackets

with tempfile.TemporaryDirectory(prefix="figure-parity-") as temp:
    out = Path(temp)
    data = pd.DataFrame({"group": ["Control"]*5 + ["A"]*6 + ["B"]*7,
                         "value": [0.9, 1, 1.05, 1.1, 0.95, 1.8, 2, 2.1, 2.2, 1.9, 2.05,
                                   0.95, 1.05, 1, 1.15, 0.9, 1.1, 1.02]})
    data.to_csv(out / "data.csv", index=False)
    cases = pd.DataFrame([dict(alpha=alpha, p=p) for alpha in
                          [0.05, 0.01, 1e-4, 1e-6, 1.23456789e-6, 0.123456789,
                           np.finfo(float).tiny, 5e-324]
                          for p in [0, alpha*0.998, np.nextafter(alpha, 0), alpha,
                                    np.nextafter(alpha, 1), alpha*1.002, 1, np.nan]])
    # Hex fixtures preserve adjacent floating-point values across CSV parsers.
    pd.DataFrame({name: cases[name].map(lambda value: "NA" if np.isnan(value) else float(value).hex())
                  for name in cases}).to_csv(out / "cases.csv", index=False)
    r_script = out / "parity.R"
    r_script.write_text(r'''
args <- commandArgs(trailingOnly=TRUE)
source(args[1])
out <- args[2]
library(ggplot2)
d <- read.csv(file.path(out, "data.csv"))
results <- do.call(rbind, lapply(c("original", "reversed"), function(order) {
  rows <- if (order == "original") d else d[nrow(d):1, ]
  controls <- rows$value[rows$group == "Control"]
  result <- do.call(rbind, lapply(c("B", "A"), function(group) {
    values <- rows$value[rows$group == group]
    test <- t.test(values, controls, var.equal=FALSE, alternative="two.sided", conf.level=0.95)
    data.frame(order=order, comparison=group, n=length(values), control_n=length(controls),
      estimate=unname(test$estimate[1]-test$estimate[2]), low=test$conf.int[1], high=test$conf.int[2], p=test$p.value)
  }))
  result$p_holm <- p.adjust(result$p, "holm")
  result
}))
write.csv(results, file.path(out, "statistics_r.csv"), row.names=FALSE)
groups <- c("Control", sprintf("Group %02d", 1:11))
pal <- biomedical_palette(groups, control="Control")
palettes <- list(original=pal, reversed=biomedical_palette(rev(groups), control="Control"),
  subset=biomedical_palette(groups[c(12,1,9)], existing=pal),
  extended=biomedical_palette(groups, existing=biomedical_palette(groups[1:9], control="Control")),
  custom=biomedical_palette(c("Control", "A", "B"), existing=c(Control="#555555", A="#AA4499"), control="Control"),
  pair=biomedical_palette(c("B", "A")),
  legacy=biomedical_palette(c("B", "A", "C"), existing=c(A="#0072B2", B="#D55E00")))
stopifnot(inherits(try(biomedical_palette(sprintf("Group %02d", 1:12)), silent=TRUE), "try-error"),
          inherits(try(biomedical_palette(c(groups, "Group 12"), control="Control"), silent=TRUE), "try-error"))
write.csv(do.call(rbind, lapply(names(palettes), function(scenario)
  data.frame(scenario=scenario, group=names(palettes[[scenario]]), color=unname(palettes[[scenario]])))),
  file.path(out, "palettes_r.csv"), row.names=FALSE)
cases <- read.csv(file.path(out, "cases.csv"))
cases[] <- lapply(cases, as.numeric)
labels <- do.call(rbind, lapply(c("hide", "ns", "value"), function(mode)
  data.frame(mode=mode, id=seq_len(nrow(cases)), label=vapply(seq_len(nrow(cases)), function(i)
    p_labels(cases$p[i], alpha=cases$alpha[i], nonsignificant=mode, missing_label="n.e."), character(1)))))
write.csv(labels, file.path(out, "labels_r.csv"), row.names=FALSE)
annotations <- data.frame(comparison=c("hidden", "missing", "change"), x1=c(30,2,0), x2=c(40,3,1),
  y=c(900,2,1.5), p=c(0.001,NA,0.001), p_holm=c(0.7,NA,0.0144))
drawn <- do.call(rbind, lapply(c("hide", "ns", "value"), function(mode)
  do.call(rbind, lapply(c("original", "reversed"), function(order) {
    rows <- if (order == "original") annotations else annotations[3:1, ]
    layers <- p_brackets(rows, p_col="p_holm", adjusted=TRUE, missing_label="n.e.", nonsignificant=mode)
    text <- ggplot_build(ggplot() + layers)$data[[4]]
    data.frame(mode=mode, order=order, comparison=layers[[1]]$data$comparison, label=text$label, x=text$x, y=text$y)
  }))))
write.csv(drawn, file.path(out, "annotations_r.csv"), row.names=FALSE)
''')
    subprocess.run(["Rscript", "--vanilla", str(r_script),
                    str(root / "skills/create-scientific-figures/scripts/compact.R"), str(out)],
                   check=True, cwd=root)

    statistics = []
    for order, rows in [("original", data), ("reversed", data.iloc[::-1])]:
        controls = rows.loc[rows.group == "Control", "value"].to_numpy()
        records = []
        for group in ["B", "A"]:
            values = rows.loc[rows.group == group, "value"].to_numpy()
            test = ttest_ind(values, controls, equal_var=False, alternative="two-sided")
            ci = test.confidence_interval(confidence_level=0.95)
            records.append(dict(order=order, comparison=group, n=len(values), control_n=len(controls),
                                estimate=values.mean()-controls.mean(), low=ci.low, high=ci.high, p=test.pvalue))
        for row, adjusted in zip(records, multipletests([row["p"] for row in records], method="holm")[1]):
            statistics.append(dict(row, p_holm=adjusted))
    python_stats = pd.DataFrame(statistics).set_index(["order", "comparison"])
    r_stats = pd.read_csv(out / "statistics_r.csv").set_index(["order", "comparison"])
    assert python_stats.index.equals(r_stats.index)
    np.testing.assert_allclose(python_stats, r_stats, rtol=1e-10, atol=1e-14)
    np.testing.assert_allclose(python_stats.loc["original"], python_stats.loc["reversed"], rtol=1e-12, atol=1e-14)

    groups = ["Control"] + [f"Group {i:02d}" for i in range(1, 12)]
    palette = biomedical_palette(groups, control="Control")
    palettes = dict(original=palette, reversed=biomedical_palette(groups[::-1], control="Control"),
                    subset=biomedical_palette([groups[i] for i in [11, 0, 8]], existing=palette),
                    extended=biomedical_palette(groups, existing=biomedical_palette(groups[:9], control="Control")),
                    custom=biomedical_palette(["Control", "A", "B"],
                                              existing={"Control": "#555555", "A": "#AA4499"}, control="Control"),
                    pair=biomedical_palette(["B", "A"]),
                    legacy=biomedical_palette(["B", "A", "C"], existing={"A": "#0072B2", "B": "#D55E00"}))
    for scenario, rows in pd.read_csv(out / "palettes_r.csv").groupby("scenario", sort=False):
        assert dict(zip(rows.group, rows.color)) == palettes[scenario]
    assert all(palettes[scenario] == palette for scenario in ["reversed", "subset", "extended"])
    assert list(palette.values()) == ["#666666", "#7F3C8D", "#11A579", "#3969AC", "#F2B701", "#E73F74",
                                      "#80BA5A", "#E68310", "#008695", "#CF1C90", "#F97B72", "#A5AA99"]
    assert palettes["pair"] == {"A": "#7F3C8D", "B": "#11A579"}
    assert palettes["legacy"] == {"A": "#0072B2", "B": "#D55E00", "C": "#7F3C8D"}
    assert len(set(palette.values())) == 12
    for too_many, control in [([f"Group {i:02d}" for i in range(1, 13)], None),
                              (groups + ["Group 12"], "Control")]:
        try:
            biomedical_palette(too_many, control=control)
        except ValueError as error:
            assert "explicit larger named palette" in str(error)
        else:
            raise AssertionError("Default palette silently recycled or invented colors")
    for mode, rows in pd.read_csv(out / "labels_r.csv", keep_default_na=False).groupby("mode", sort=False):
        expected = [p_labels([row.p], alpha=row.alpha, nonsignificant=mode, missing_label="n.e.")[0]
                    for row in cases.itertuples()]
        assert rows.label.tolist() == expected, (mode, rows.label.tolist(), expected)
    keyed = {"third": 0.05000001, "first": 0.04999999, "missing": None}
    for mode in ["hide", "ns", "value"]:
        expected = p_labels(keyed, nonsignificant=mode, missing_label="n.e.")
        reordered = {key: keyed[key] for key in reversed(keyed)}
        assert p_labels(reordered, nonsignificant=mode, missing_label="n.e.") == {key: expected[key] for key in reordered}

    annotations = [dict(comparison="hidden", x1=30, x2=40, y=900, p=0.001, p_holm=0.7),
                   dict(comparison="missing", x1=2, x2=3, y=2, p=None, p_holm=None),
                   dict(comparison="change", x1=0, x2=1, y=1.5, p=0.001, p_holm=0.0144)]
    drawn = []
    for mode in ["hide", "ns", "value"]:
        for order, rows in [("original", annotations), ("reversed", annotations[::-1])]:
            fig, ax = plt.subplots()
            artists = p_brackets(ax, rows, p_col="p_holm", adjusted=True, missing_label="n.e.", nonsignificant=mode)
            visible = [row for row in rows if mode != "hide" or row["comparison"] != "hidden"]
            for row, text in zip(visible, artists[1::2], strict=True):
                drawn.append(dict(mode=mode, order=order, comparison=row["comparison"],
                                  label=text.get_text(), x=text.xy[0], y=text.xy[1]))
            plt.close(fig)
    pd.testing.assert_frame_equal(pd.DataFrame(drawn), pd.read_csv(out / "annotations_r.csv"), check_dtype=False)
    assert all("label" not in row for row in annotations)
print("R/Python parity passed: CARTO Bold 11 colors + control gray, pair defaults, legacy mapping, palette reorder/subset/extension/overflow, threshold-aware labels, annotation keys/geometry, Welch estimates/95% CI/P and complete-family Holm.")
