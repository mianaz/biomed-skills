#!/usr/bin/env python3
"""Run the repository's dependency-free structural and artifact-contract checks."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    python = sys.executable
    fixture = root / "tests" / "fixtures" / "minimal-run"
    with tempfile.TemporaryDirectory(prefix="ai-scientist-check-") as temporary:
        temporary_path = Path(temporary)
        commands = [
            [
                python,
                "-B",
                str(root / "skills/maintain-biomedical-skills/scripts/audit_skill_suite.py"),
                str(root / "skills"),
                "--registry",
                str(root / "suite.json"),
                "--output",
                str(temporary_path / "skill-audit.json"),
            ],
            [
                python,
                "-B",
                str(root / "skills/plan-biomedical-analysis/scripts/validate_analysis_contract.py"),
                str(fixture / "analysis-contract.json"),
            ],
            [
                python,
                "-B",
                str(root / "skills/ensure-biomedical-reproducibility/scripts/validate_run_manifest.py"),
                str(fixture / "run-manifest.json"),
                "--contract",
                str(fixture / "analysis-contract.json"),
                "--check-files",
                "--root",
                str(root),
            ],
            [
                python,
                "-B",
                str(root / "skills/verify-biomedical-analysis/scripts/verify_bundle.py"),
                "--contract",
                str(fixture / "analysis-contract.json"),
                "--manifest",
                str(fixture / "run-manifest.json"),
                "--evidence",
                str(fixture / "evidence-index.json"),
                "--output",
                str(temporary_path / "verification-report.json"),
                "--root",
                str(root),
            ],
            [
                python,
                "-B",
                str(root / "tests/test_universal_suite.py"),
            ],
            [
                python,
                "-B",
                str(root / "tools/install_skills.py"),
                "--target",
                str(temporary_path / "agent-skills"),
                "--skill",
                "plan-biomedical-analysis",
                "--skill",
                "verify-biomedical-analysis",
            ],
        ]
        for command in commands:
            completed = subprocess.run(command, cwd=root, text=True, capture_output=True)
            label = Path(command[2]).name if len(command) > 2 else command[0]
            if completed.stdout:
                print(f"[{label}] {completed.stdout.strip()}")
            if completed.stderr:
                print(f"[{label} stderr] {completed.stderr.strip()}", file=sys.stderr)
            if completed.returncode:
                print(f"FAILED: {' '.join(command)}", file=sys.stderr)
                return completed.returncode
        for skill_name in ("plan-biomedical-analysis", "verify-biomedical-analysis"):
            installed = temporary_path / "agent-skills" / skill_name / "SKILL.md"
            if not installed.is_file():
                print(f"FAILED: installer did not create {installed}", file=sys.stderr)
                return 1
    print("PASS: suite structure, registry, artifact contracts, verification, and installer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
