"""The setup command must fail usefully in a Python without site packages."""
from pathlib import Path
import subprocess
import sys

checker = Path(__file__).resolve().parents[1] / "skills/create-scientific-figures/scripts/check_environment.py"
result = subprocess.run([sys.executable, "-S", str(checker)], capture_output=True, text=True)
assert result.returncode == 1, result.stdout + result.stderr
assert all("MISSING " + package in result.stdout for package in
           ("matplotlib", "numpy", "pandas", "scipy", "pymupdf")), result.stdout
assert "NOT CHECKED Arial" in result.stdout, result.stdout
assert "pip install" in result.stdout, result.stdout
print("Missing-runtime guidance passed")
