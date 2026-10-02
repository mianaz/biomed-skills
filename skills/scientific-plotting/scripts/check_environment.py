"""Run with the same Python interpreter used to draw the figure."""
import importlib
import sys

missing = []
for package, module in [("matplotlib", "matplotlib"), ("numpy", "numpy"),
                        ("pandas", "pandas"), ("scipy", "scipy"), ("pymupdf", "pymupdf")]:
    try:
        loaded = importlib.import_module(module)
        print("OK     ", package, getattr(loaded, "__version__", ""))
    except (ImportError, OSError) as error:
        missing.append(package)
        print("MISSING", package, "—", error)

arial = None
if "matplotlib" not in missing:
    arial = False
    from matplotlib import font_manager
    try:
        path = font_manager.findfont("Arial", fallback_to_default=False)
        arial = font_manager.FontProperties(fname=path).get_name() == "Arial"
    except ValueError:
        pass
print("NOT CHECKED" if arial is None else "OK     " if arial else "MISSING", "Arial font family")
if missing:
    print("Install into this interpreter's environment:")
    print(sys.executable, "-m pip install", " ".join(missing))
if arial is False:
    print("Install a licensed Arial font, then restart Python. Export checks verify the embedded font.")
sys.exit(1 if missing or arial is not True else 0)
