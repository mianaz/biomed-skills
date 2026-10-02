"""Run with a Python environment containing matplotlib, numpy, scipy and PyMuPDF."""
from pathlib import Path
import sys
import tempfile
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"skills/create-scientific-figures/scripts"))
from compact import biomedical_palette, biomedical_theme, p_labels, p_brackets, export_biomedical
from dose_response import dose_response_candidates, log_logistic, relative_ed50


def test_python_figure_helpers():
    output = Path(tempfile.mkdtemp(prefix="figure-python-"))
    groups = ["Drug B", "Control", "Drug A"]
    palette = biomedical_palette(groups, control="Control")
    assert palette == biomedical_palette(groups[::-1], control="Control")
    assert palette == {"Control": "#666666", "Drug A": "#7F3C8D", "Drug B": "#11A579"}
    assert biomedical_palette(["Drug B"], existing=palette) == palette
    assert biomedical_palette(["B", "A"]) == {"A": "#7F3C8D", "B": "#11A579"}
    old_colors = {"A": "#0072B2", "B": "#D55E00"}
    assert biomedical_palette(["B", "A", "C"], existing=old_colors) == dict(old_colors, C="#7F3C8D")
    assert len(set(biomedical_palette([f"Group {i}" for i in range(11)]).values())) == 11
    try:
        biomedical_palette([f"Group {i}" for i in range(12)])
    except ValueError as error:
        assert "explicit larger named palette" in str(error)
    else:
        raise AssertionError("Default palette silently recycled or invented a twelfth color")
    keyed = {"missing": None, "change": 0.0144, "unchanged": 0.7}
    labels = p_labels(keyed, adjusted=True, missing_label="n.e.")
    assert labels == {"missing": "n.e.", "change": "P adj. = 0.014", "unchanged": ""}
    assert p_labels(keyed, True, "n.e.", "ns") == dict(labels, unchanged="ns")
    assert p_labels(keyed, True, "n.e.", "value") == dict(labels, unchanged="P adj. = 0.7")
    assert p_labels([0.05, 0.04999999]) == ["", "P < 0.05"]
    assert p_labels([0.01, 0.00999999], alpha=0.01) == ["", "P = 0.00999999"]
    assert p_labels([0.0499, 0.0501, 0.05000001, 0.05], nonsignificant="value") == [
        "P = 0.0499", "P = 0.0501", "P > 0.05", "P = 0.05"]
    assert p_labels([5e-7, 1e-6, 1.0000000001e-6, 2e-6], alpha=1e-6, nonsignificant="value") == [
        "P < 1e-06", "P = 1e-06", "P > 1e-06", "P = 2e-06"]
    assert p_labels([0.123456789], alpha=0.123456789, nonsignificant="value") == ["P = 0.123456789"]
    assert p_labels([None, np.nan], missing_label="n.e.", nonsignificant="ns") == ["n.e.", "n.e."]
    assert p_labels([]) == [] and p_labels({}) == {}
    assert p_labels([1e-6, 0.01]) == ["P < 0.0001", "P = 0.01"]
    for values in ([None], [np.inf], [-0.1], [1.1]):
        try:
            p_labels(values)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid or undeclared missing P was accepted")
    for options in [dict(nonsignificant="stars"), dict(alpha=0), dict(alpha=1), dict(alpha=np.nan)]:
        try:
            p_labels([0.1], **options)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid annotation mode or threshold was accepted")
    annotations = [dict(comparison="hidden", x1=30, x2=40, y=900, p=0.001, p_holm=0.7),
                   dict(comparison="missing", x1=2, x2=3, y=2, p=None, p_holm=None),
                   dict(comparison="change", x1=0, x2=1, y=1.5, p=0.001, p_holm=0.0144)]
    for mode in ["hide", "ns", "value"]:
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1])
        artists = p_brackets(ax, annotations, p_col="p_holm", adjusted=True,
                             missing_label="n.e.", nonsignificant=mode)
        assert [a.get_text() for a in artists[1::2]] == (
            ["n.e.", "P adj. = 0.014"] if mode == "hide" else
            ["ns" if mode == "ns" else "P adj. = 0.7", "n.e.", "P adj. = 0.014"])
        assert [a.xy for a in artists[1::2]][-2:] == [(2.5, 2), (0.5, 1.5)]
        assert ax.get_ylim()[1] < 3 if mode == "hide" else ax.get_ylim()[1] > 900
        plt.close(fig)
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    before = (ax.get_xlim(), ax.get_ylim(), len(ax.lines), len(ax.texts))
    repeated_ns = [dict(x1=i-0.2, x2=i+0.2, y=900, p_holm=0.18) for i in range(5)]
    assert p_brackets(ax, repeated_ns, p_col="p_holm", adjusted=True) == []
    assert (ax.get_xlim(), ax.get_ylim(), len(ax.lines), len(ax.texts)) == before
    assert p_brackets(ax, [annotations[0]], p_col="p_holm") == []
    assert p_brackets(ax, [dict(annotations[0], label="")]) == []
    assert (ax.get_xlim(), ax.get_ylim(), len(ax.lines), len(ax.texts)) == before
    try:
        p_brackets(ax, [annotations[2], dict(annotations[0], label="P adj. = 0.7")],
                   p_col="p_holm", adjusted=True)
    except ValueError:
        pass
    else:
        raise AssertionError("Contradictory hidden-row label was accepted")
    assert (ax.get_xlim(), ax.get_ylim(), len(ax.lines), len(ax.texts)) == before
    assert "label" not in annotations[0]
    plt.close(fig)
    previous_size = matplotlib.rcParams["font.size"]
    with biomedical_theme():
        fig, ax = plt.subplots(layout="constrained")
        ax.plot([0, 1, 2, 3], [1, 2, 2, 3], "o", color=palette["Drug A"])
        ax.set(xlabel="Dose", ylabel="Response", ylim=(0, 4.5), xticks=[0, 1, 2, 3])
        rows = [dict(x1=0, x2=3, y=3.5, p=0.0144)]
        artists = p_brackets(ax, rows, p_col="p", tip=0.06)
        assert artists[-1].get_text() == "P = 0.014"
        assert artists[-1].xy == (1.5, 3.5)
        try:
            p_brackets(ax, [dict(rows[0], label="P = 0.7")], p_col="p")
        except ValueError:
            pass
        else:
            raise AssertionError("Numeric P/label mismatch was accepted")
        audit = export_biomedical(fig, output/"valid", 90, 75)
        assert audit["min_font_pt"] > 10 and audit["min_placed_font_pt"] > 10
        with fitz.open(output/"valid.pdf") as pdf:
            assert abs(pdf[0].rect.width*25.4/72-90) < 0.01
            assert "Arial" in " ".join(font[3] for font in pdf[0].get_fonts())
        overlap = [ax.text(1.5, 1, word) for word in ("alpha", "beta")]
        with warnings.catch_warnings(record=True) as caught:
            collision = export_biomedical(fig, output/"collision", 90, 75)
        assert collision["candidate_overlaps"] > 0 and caught
        for text in overlap:
            text.remove()
        clipped = ax.text(1, 4.45, "clipped", clip_on=True)
        try:
            export_biomedical(fig, output/"clipped", 90, 75)
        except ValueError as error:
            assert "clipping boundary" in str(error), str(error)
        else:
            raise AssertionError("Internally clipped text was accepted")
        clipped.remove()
        for name, width in (("wide", 180), ("small", 90)):
            if name == "small":
                ax.xaxis.label.set_fontsize(9)
            try:
                export_biomedical(fig, output/name, width, 75)
            except ValueError as error:
                assert "10 pt" in str(error), str(error)
            else:
                raise AssertionError("Undersized saved/placed PDF text was accepted")
            assert (output/f"{name}.pdf").exists() and (output/f"{name}.png").exists()
        plt.close(fig)
    assert matplotlib.rcParams["font.size"] == previous_size
    with biomedical_theme(size=16):
        fig = plt.figure()
        labels = [r"Human gene: $\mathit{TP53}$", "Human protein: TP53",
                  r"Mouse gene: $\mathit{Trp53}$", "β-catenin", r"$\mathrm{Ca}^{2\!+}$",
                  r"$\mathrm{H}_{2}\mathrm{O}$", r"$\mathrm{IC}_{50}$", r"$\mathrm{μM}$",
                  r"$\mathrm{s}^{-1}$", r"$\mathit{Trp53}^{-\!/\!-}$"]
        for index, label in enumerate(labels):
            fig.text(0.07, 0.91-index*0.088, label, va="baseline")
        typography = export_biomedical(fig, output/"typography", 90, 75)
        with fitz.open(output/"typography.pdf") as pdf:
            lines = [line["spans"] for block in pdf[0].get_text("dict")["blocks"]
                     for line in block.get("lines", [])]
            assert np.isclose(pdf[0].rect.width*25.4/72, 90)
        assert len(lines) == 10
        assert ["".join(s["text"] for s in line).replace(" ", "") for line in lines] == [
            "Humangene:TP53", "Humanprotein:TP53", "Mousegene:Trp53", "β-catenin",
            "Ca2+", "H2O", "IC50", "μM", "s−1", "Trp53−/−"]
        assert all("Arial" in span["font"] for line in lines for span in line)
        assert lines[0][-1]["flags"] & 2 and lines[0][-1]["text"] == "TP53"
        assert not lines[1][0]["flags"] & 2
        assert lines[2][-1]["flags"] & 2 and lines[2][-1]["text"] == "Trp53"
        assert lines[9][0]["flags"] & 2
        assert all(not span["flags"] & 2 for line in lines[3:9] for span in line)
        for index in (4, 5, 6, 8, 9):
            base, script = lines[index][:2]
            assert np.isclose(base["size"], 16) and np.isclose(script["size"], 11.2)
            assert not script["flags"] & 2
            shift = script["origin"][1]-base["origin"][1]
            assert shift > 1 if index in (5, 6) else shift < -2
        assert typography["candidate_overlaps"] == 0
        assert np.isclose(typography["min_placed_font_pt"], 11.2)
        for text in fig.texts:
            text.set_fontsize(14)
        try:
            export_biomedical(fig, output/"typography_small", 90, 75)
        except ValueError as error:
            assert "10 pt" in str(error), str(error)
        else:
            raise AssertionError("A 9.8-pt scientific subscript was accepted")
        plt.close(fig)
    cf = np.array([1.6, 5, 95, np.log(3), 1.8])
    ed50, gradient = relative_ed50(cf)
    assert np.isclose(log_logistic(ed50, *cf), 50)
    numeric = []
    for index in range(5):
        shift = np.zeros(5); shift[index] = 1e-5
        numeric.append((np.log(relative_ed50(cf+shift)[0])-np.log(relative_ed50(cf-shift)[0]))/2e-5)
    assert np.allclose(gradient, numeric, rtol=1e-5, atol=1e-6)
    dose = np.geomspace(0.03, 300, 36)
    response = log_logistic(dose, *cf) + np.random.default_rng(53).normal(0, 0.25, len(dose))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        result = dose_response_candidates(dose, response)
    rows = {row["model"]: row for row in result["comparison"]}
    assert set(rows) == {"constant", "4PL", "5PL"} and all(row["converged"] for row in rows.values())
    assert rows["5PL"]["rss"] <= rows["4PL"]["rss"] < rows["constant"]["rss"]
    assert rows["5PL"]["ed50_low"] < ed50 < rows["5PL"]["ed50_high"]
    assert np.isclose(rows["5PL"]["relative_ed50"], ed50, rtol=0.03)
    assert len(result["predictions"]) == 450 and len(result["residuals"]) == 3*len(dose)
    short = dose_response_candidates([1, 2], [1, 2])
    assert list(short["models"]) == ["constant"]
    print(f"Python figure + dose-response checks passed; rendered artifacts: {output}")


if __name__ == "__main__":
    test_python_figure_helpers()
