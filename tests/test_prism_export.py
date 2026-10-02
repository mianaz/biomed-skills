"""Run: python3 tests/test_prism_export.py (base R + Python standard library)."""
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["Rscript", "-e", '''
source(commandArgs(TRUE)[1]); out <- commandArgs(TRUE)[2]
paired <- data.frame(id=c("s2", "s1", "s3"), before=c(0, NA, pi), after=c(2, 4, 6))
write_prism(paired, file.path(out,"paired.pzfx"), id="id", title="A & B <C>")
xy <- data.frame(time=c(0, 1), a1=c(0, 2), a2=c(NA, 3), b1=c(4, 5), b2=c(6, 7))
mapping <- c(a1="Control", a2="Control", b1="Drug", b2="Drug")
write_prism(xy, file.path(out,"xy.pzfx"), x="time", groups=mapping)
write_prism(xy[-1], file.path(out,"grouped.pzfx"), groups=mapping)
stopifnot(inherits(try(write_prism(paired,file.path(out,"paired.pzfx"),id="id"),silent=TRUE),"try-error"))
write_prism(paired,file.path(out,"paired.pzfx"),id="id",title="A & B <C>",overwrite=TRUE)
for (bad in list(transform(paired, id=c("s1","s1","s3")), transform(paired, before=c(Inf,1,2)),
                 transform(paired, before=c("0","missing","1"))))
  stopifnot(inherits(try(write_prism(bad,file.path(out,"bad.pzfx"),id="id"),silent=TRUE),"try-error"))
stopifnot(inherits(try(write_prism(xy,file.path(out,"bad.pzfx"),x="missing"),silent=TRUE),"try-error"))
stopifnot(inherits(try(write_prism(xy,file.path(out,"bad.pzfx"),x="time",groups=mapping[-1]),silent=TRUE),"try-error"))
''', str(root / "skills/create-scientific-figures/scripts/prism.R"), tmp], check=True)
    paired = ET.parse(Path(tmp) / "paired.pzfx").getroot()
    table = paired.find("Table")
    assert table.get("TableType") == "OneWay"
    assert table.findtext("Title") == "A & B <C>"
    assert [d.text for d in table.findall("RowTitlesColumn/Subcolumn/d")] == ["s2", "s1", "s3"]
    values = table.findall("YColumn/Subcolumn/d")
    assert values[0].text == "0" and values[1].text is None
    assert float(values[2].text) == 3.141592653589793
    assert paired.find("Template") is None
    for filename, kind in [("xy", "XY"), ("grouped", "TwoWay")]:
        table = ET.parse(Path(tmp) / f"{filename}.pzfx").getroot().find("Table")
        assert table.get("TableType") == kind and table.get("Replicates") == "2"
        assert [y.findtext("Title") for y in table.findall("YColumn")] == ["Control", "Drug"]
        assert [[d.text for d in s] for s in table.findall("YColumn/Subcolumn")] == [
            ["0", "2"], [None, "3"], ["4", "5"], ["6", "7"]]
        if kind == "XY":
            assert [d.text for d in table.findall("XColumn/Subcolumn/d")] == ["0", "1"]
print("PASS: Prism values, precision, missing cells, row IDs, grouped/XY replicates, and invalid input checks")
