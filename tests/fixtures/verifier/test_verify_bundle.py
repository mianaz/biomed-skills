#!/usr/bin/env python3
"""Dependency-free positive and adversarial checks for verify_bundle.py."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "verify-biomedical-analysis" / "scripts" / "verify_bundle.py"
BASE = ROOT / "tests" / "fixtures" / "minimal-run"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(bundle: Path, output_name: str, *extra: str) -> tuple[int, dict]:
    output = bundle / output_name
    result = subprocess.run(
        [
            "python3",
            "-B",
            str(SCRIPT),
            "--bundle",
            str(bundle),
            "--root",
            str(ROOT),
            "--output",
            str(output),
            *extra,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if not output.exists():
        raise AssertionError(f"verifier did not write a report\n{result.stdout}\n{result.stderr}")
    return result.returncode, read(output)


def check_map(report: dict) -> dict[str, dict]:
    return {item["check_id"]: item for item in report["checks"]}


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="verify-bundle-test-") as temporary:
        temp = Path(temporary)

        positive = temp / "positive"
        shutil.copytree(BASE, positive)
        code, report = run(positive, "report.json")
        assert code == 0
        assert report["overall_status"] == "pass"
        assert report["verifier"]["independent_of_executor"] is False
        assert report["verifier"]["independence_assertion"] == "not_asserted"
        assert check_map(report)["schema-report"]["status"] == "pass"

        universal = temp / "universal-v1-1"
        shutil.copytree(BASE, universal)
        contract = read(universal / "analysis-contract.json")
        contract["schema_version"] = "1.1.0"
        contract["design"]["units"] = [
            {"unit_id": "participant", "description": "One enrolled participant."}
        ]
        contract["design"]["outcomes"] = [
            {
                "outcome_id": "primary-outcome",
                "role": "primary",
                "definition": "Prespecified fixture outcome.",
                "unit_id": "participant",
            }
        ]
        contract["design"]["analysis_sets"] = [
            {
                "analysis_set_id": "primary-set",
                "unit_id": "participant",
                "definition": "All participants with observed outcomes.",
            }
        ]
        contract["governance"] = {
            "human_subjects": "no",
            "animals": "no",
            "sensitive_data": "no",
            "hazardous_materials": "no",
            "approvals": [],
            "restrictions": [],
        }
        contract["extensions"]["profiles"] = {}
        write(universal / "analysis-contract.json", contract)
        manifest = read(universal / "run-manifest.json")
        manifest["schema_version"] = "1.1.0"
        manifest["inputs"][0]["locator_kind"] = "file"
        manifest["artifacts"][0]["locator_kind"] = "file"
        manifest["resources"] = [
            {
                "resource_id": "protocol-1",
                "kind": "protocol",
                "name": "Fixture protocol",
                "version": "1.0.0",
            }
        ]
        manifest["steps"][0]["input_ids"] = ["input-file"]
        manifest["steps"][0]["upstream_artifact_ids"] = []
        manifest["steps"][0]["resource_ids"] = ["protocol-1"]
        write(universal / "run-manifest.json", manifest)
        evidence = read(universal / "evidence-index.json")
        evidence["schema_version"] = "1.1.0"
        evidence["evidence_items"][0]["data_context"].update(
            {
                "outcome_id": "primary-outcome",
                "analysis_set_id": "primary-set",
                "unit_type": "participant",
                "unit_set_artifact_id": "artifact-result",
            }
        )
        evidence["evidence_items"][0]["statistics"][0].update(
            {
                "count_basis": "participants in the primary analysis set",
                "denominator": 4,
            }
        )
        write(universal / "evidence-index.json", evidence)
        code, report = run(universal, "report.json")
        assert code == 0
        assert report["overall_status"] == "pass"
        checks = check_map(report)
        assert checks["design-unit-refs"]["status"] == "pass"
        assert checks["manifest-step-resources"]["status"] == "pass"
        assert checks["evidence-resolution"]["status"] == "pass"

        mapped = temp / "mapped"
        shutil.copytree(BASE, mapped)
        contract = read(mapped / "analysis-contract.json")
        contract["validation"].append(
            {
                "check_id": "manual-design-check",
                "criterion": "A reviewer reconstructs the design.",
                "severity": "error",
            }
        )
        contract["validation"].append(
            {
                "check_id": "missing-warning-check",
                "criterion": "An optional sensitivity check is recorded.",
                "severity": "warning",
            }
        )
        write(mapped / "analysis-contract.json", contract)
        manifest = read(mapped / "run-manifest.json")
        manifest["quality"]["checks"].append(
            {
                "check_id": "observed-design-review",
                "contract_check_id": "manual-design-check",
                "category": "design",
                "status": "pass",
                "summary": "The design was independently reconstructed.",
                "artifact_ids": [],
            }
        )
        write(mapped / "run-manifest.json", manifest)
        code, report = run(mapped, "report.json")
        assert code == 0
        assert report["overall_status"] == "pass_with_warnings"
        mapped_check = check_map(report)["planned-manual-design-check"]
        assert mapped_check["status"] == "pass"
        assert mapped_check["severity"] == "error"
        assert mapped_check["contract_check_id"] == "manual-design-check"
        warning_check = check_map(report)["planned-missing-warning-check"]
        assert warning_check["status"] == "warn"
        assert warning_check["severity"] == "warning"

        domain = temp / "domain"
        shutil.copytree(BASE, domain)
        contract = read(domain / "analysis-contract.json")
        contract["extensions"]["profiles"] = {
            "single_cell_analysis": {
                "assay": "scRNA-seq",
                "biological_unit": "donor",
                "sample_id_field": "sample_id",
                "cell_id_field": "cell_id",
            }
        }
        write(domain / "analysis-contract.json", contract)
        manifest = read(domain / "run-manifest.json")
        profile = read(
            ROOT
            / "skills"
            / "verify-biomedical-analysis"
            / "references"
            / "profiles"
            / "single-cell.json"
        )
        for item in profile["checks"]:
            manifest["quality"]["checks"].append(
                {
                    "check_id": item["check_id"],
                    "category": item["category"],
                    "status": "pass",
                    "summary": f"Fixture result for {item['check_id']}.",
                    "artifact_ids": [],
                }
            )
        write(domain / "run-manifest.json", manifest)
        verifier_metadata = domain / "verifier.json"
        write(
            verifier_metadata,
            {
                "verifier_id": "independent-agent-1",
                "kind": "agent",
                "independent_of_executor": True,
            },
        )
        code, report = run(
            domain,
            "report.json",
            "--verifier-metadata",
            str(verifier_metadata),
        )
        assert code == 0
        assert report["overall_status"] == "pass"
        assert report["extensions"]["domain_profiles"] == ["single-cell-analysis"]
        assert set(report["extensions"]["domain_categories"]) == {
            "single-cell-inference",
            "single-cell-qc",
        }
        assert report["verifier"]["independence_assertion"] == "metadata_file"

        adversarial = temp / "adversarial"
        shutil.copytree(BASE, adversarial)
        contract = read(adversarial / "analysis-contract.json")
        contract["questions"].append(
            {"question_id": "q-missing", "text": "Was the second question answered?"}
        )
        contract["steps"].append(
            {
                "step_id": "step-missing",
                "purpose": "Exercise planned-step coverage.",
                "method": "Fixture method",
            }
        )
        contract["validation"].append(
            {
                "check_id": "missing-error-check",
                "criterion": "A required manual check is recorded.",
                "severity": "error",
            }
        )
        write(adversarial / "analysis-contract.json", contract)
        manifest = read(adversarial / "run-manifest.json")
        del manifest["quality"]["input_qc"]["status"]
        write(adversarial / "run-manifest.json", manifest)
        evidence = read(adversarial / "evidence-index.json")
        evidence["evidence_items"].append(dict(evidence["evidence_items"][0]))
        write(adversarial / "evidence-index.json", evidence)
        code, report = run(adversarial, "report.json")
        checks = check_map(report)
        assert code == 1
        assert report["overall_status"] == "fail"
        assert checks["schema-manifest"]["status"] == "fail"
        assert checks["identifier-uniqueness"]["status"] == "fail"
        assert checks["contract-step-coverage"]["status"] == "fail"
        assert checks["contract-question-coverage"]["status"] == "fail"
        assert checks["planned-missing-error-check"]["status"] == "fail"
        assert checks["planned-missing-error-check"]["severity"] == "error"

        strict = temp / "strict"
        shutil.copytree(BASE, strict)
        contract = read(strict / "analysis-contract.json")
        contract["profile"]["assurance"] = "strict"
        contract["strict_policy"] = {
            "require_lockfile": False,
            "require_container": False,
            "require_fixed_references": False,
            "require_cached_sources": True,
            "require_rerun": True,
            "numeric_tolerance": 0.01,
        }
        write(strict / "analysis-contract.json", contract)
        manifest = read(strict / "run-manifest.json")
        input_path = ROOT / manifest["inputs"][0]["uri"]
        result_path = ROOT / manifest["artifacts"][0]["uri"]
        manifest["inputs"][0]["sha256"] = sha256(input_path)
        manifest["artifacts"][0]["sha256"] = sha256(result_path)
        manifest["environment"]["runtimes"][0]["version"] = "3.12.4"
        manifest["artifacts"].append(
            {
                "artifact_id": "artifact-cache",
                "kind": "cache",
                "uri": manifest["artifacts"][0]["uri"],
                "status": "produced",
                "media_type": "text/tab-separated-values",
                "sha256": sha256(result_path),
            }
        )
        manifest["external_sources"].append(
            {
                "source_id": "source-live",
                "kind": "database",
                "name": "Fixture database",
                "resource": "https://example.test/data",
                "retrieved_at": "2026-07-15T00:00:00Z",
                "mutable": True,
                "cache_artifact_id": "artifact-cache",
            }
        )
        write(strict / "run-manifest.json", manifest)
        rerun = {
            "schema_version": "1.0.0",
            "artifact_type": "rerun_comparison",
            "contract_id": contract["contract_id"],
            "run_id": manifest["run_id"],
            "performed_at": "2026-07-15T01:00:00Z",
            "tolerance_used": 0.01,
            "comparisons": [
                {
                    "comparison_id": "cmp-result",
                    "baseline_artifact_id": "artifact-result",
                    "metric": "max_absolute_difference",
                    "observed_difference": 0.005,
                }
            ],
            "extensions": {},
        }
        rerun_path = strict / "rerun.json"
        write(rerun_path, rerun)
        code, report = run(
            strict,
            "report-pass.json",
            "--rerun-record",
            str(rerun_path),
            "--independent-of-executor",
            "--context-isolated",
        )
        checks = check_map(report)
        assert code == 0
        assert report["overall_status"] == "pass"
        assert checks["strict-policy"]["status"] == "pass"
        assert checks["schema-rerun-record"]["status"] == "pass"
        assert report["strict"]["rerun"]["maximum_observed_difference"] == 0.005
        assert report["verifier"]["independence_assertion"] == "cli"

        rerun["comparisons"][0]["observed_difference"] = 0.02
        write(rerun_path, rerun)
        manifest["external_sources"][0].pop("cache_artifact_id")
        write(strict / "run-manifest.json", manifest)
        code, report = run(
            strict,
            "report-fail.json",
            "--rerun-record",
            str(rerun_path),
            "--independent-of-executor",
        )
        checks = check_map(report)
        assert code == 1
        assert checks["strict-policy"]["status"] == "fail"
        assert "lacks required cached artifact" in checks["strict-policy"]["message"]
        assert checks["schema-rerun-record"]["status"] == "fail"
        assert "exceeds tolerance" in checks["schema-rerun-record"]["message"]

    print("verify_bundle.py positive and adversarial checks passed")


if __name__ == "__main__":
    main()
