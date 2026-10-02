#!/usr/bin/env python3
"""Deterministic cross-domain routing, contract, profile, and compatibility tests."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "universal"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


INSTALLER = load_module("universal_install_skills", ROOT / "tools" / "install_skills.py")
CONTRACT_VALIDATOR = load_module(
    "universal_validate_analysis_contract",
    ROOT / "skills" / "plan-biomedical-analysis" / "scripts" / "validate_analysis_contract.py",
)
VERIFIER = load_module(
    "universal_verify_bundle",
    ROOT / "skills" / "verify-biomedical-analysis" / "scripts" / "verify_bundle.py",
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class UniversalSuiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = read_json(ROOT / "suite.json")
        cls.entries, cls.aliases = INSTALLER.registry_indexes(cls.registry)
        cls.router = cls.entries["orchestrate-biomedical-work"]
        cls.scenarios: dict[str, tuple[dict, dict]] = {}
        for scenario_path in sorted(FIXTURES.glob("*/scenario.json")):
            scenario = read_json(scenario_path)
            contract = read_json(scenario_path.with_name("analysis-contract.json"))
            cls.scenarios[scenario["scenario_id"]] = (scenario, contract)

    def test_four_realistic_cross_domain_contracts_and_routes(self) -> None:
        self.assertEqual(
            set(self.scenarios),
            {
                "clinical-time-to-event",
                "imaging-model-evaluation",
                "dose-response",
                "biomedical-evidence-synthesis",
            },
        )
        for scenario_id, (scenario, contract) in self.scenarios.items():
            with self.subTest(scenario=scenario_id):
                self.assertEqual(CONTRACT_VALIDATOR.validate(contract), [])
                schema = read_json(
                    ROOT
                    / "skills"
                    / "plan-biomedical-analysis"
                    / "references"
                    / "analysis-contract.schema.json"
                )
                self.assertEqual(VERIFIER.validate_schema(contract, schema), [])

                primary = scenario["primary_skill"]
                self.assertIn(primary, self.entries)
                self.assertIn(scenario["expected_scope"], self.entries[primary]["scopes"])
                self.assertIn(primary, self.router["routes_to"])

                resolved = INSTALLER.resolve_selection(
                    self.registry, requested_bundles=[scenario["bundle"]]
                )
                self.assertIn(primary, resolved)
                for required in scenario["supporting_skills"]:
                    self.assertIn(required, resolved)
                for forbidden in scenario["forbidden_skills"]:
                    self.assertNotIn(forbidden, resolved)

    def test_registered_domain_profiles_resolve_and_validate_extensions(self) -> None:
        for scenario_id, (scenario, contract) in self.scenarios.items():
            profile_id = scenario["resource_profile"]
            extension_key = scenario["extension_key"]
            if profile_id is None:
                with self.subTest(scenario=scenario_id):
                    self.assertIsNone(extension_key)
                    self.assertEqual(contract["extensions"]["profiles"], {})
                continue

            with self.subTest(scenario=scenario_id):
                primary = self.entries[scenario["primary_skill"]]
                self.assertIn(profile_id, primary["resource_profiles"])
                relative_profile_path = self.registry["resource_profiles"][profile_id]
                profile_path = ROOT / relative_profile_path
                profile = read_json(profile_path)
                self.assertEqual(profile["profile_id"], profile_id)
                self.assertEqual(profile["contract_extension"]["key"], extension_key)

                extension_schema = read_json(
                    profile_path.parent / profile["contract_extension"]["schema"]
                )
                extension = contract["extensions"]["profiles"][extension_key]
                self.assertEqual(VERIFIER.validate_schema(extension, extension_schema), [])

    def test_bundle_resolution_is_deterministic_and_keeps_core_safeguards(self) -> None:
        core = {
            "plan-biomedical-analysis",
            "ensure-biomedical-reproducibility",
            "verify-biomedical-analysis",
            "orchestrate-biomedical-work",
        }
        for scenario_id, (scenario, _) in self.scenarios.items():
            with self.subTest(scenario=scenario_id):
                first = INSTALLER.resolve_selection(
                    self.registry, requested_bundles=[scenario["bundle"]]
                )
                second = INSTALLER.resolve_selection(
                    self.registry, requested_bundles=[scenario["bundle"]]
                )
                self.assertEqual(first, second)
                self.assertTrue(core.issubset(first))
                registry_order = [item["name"] for item in self.registry["skills"]]
                self.assertEqual(first, [name for name in registry_order if name in first])

    def test_pseudobulk_is_not_clinical_survival(self) -> None:
        scenario, _ = self.scenarios["clinical-time-to-event"]
        self.assertEqual(scenario["primary_skill"], "model-time-to-event-outcomes")
        self.assertNotIn("clinical", self.entries["test-single-cell-expression"]["scopes"])
        self.assertNotIn("test-single-cell-expression", self.router["routes_to"])

    def test_perturb_seq_is_not_dose_response(self) -> None:
        scenario, _ = self.scenarios["dose-response"]
        self.assertEqual(scenario["primary_skill"], "analyze-dose-response")
        self.assertNotIn("experimental", self.entries["analyze-perturb-seq"]["scopes"])
        self.assertNotIn("analyze-perturb-seq", self.router["routes_to"])

    def test_method_distillation_is_not_literature_synthesis(self) -> None:
        scenario, _ = self.scenarios["biomedical-evidence-synthesis"]
        self.assertEqual(scenario["primary_skill"], "synthesize-biomedical-evidence")
        self.assertEqual(self.entries["distill-biomedical-methods"]["kind"], "governance")
        self.assertEqual(self.entries["synthesize-biomedical-evidence"]["kind"], "leaf")
        self.assertNotIn("distill-biomedical-methods", self.router["routes_to"])

    def test_version_1_contract_and_run_bundle_remain_supported(self) -> None:
        contract = read_json(
            FIXTURES / "backward-compatibility-v1.0" / "analysis-contract.json"
        )
        self.assertEqual(contract["schema_version"], "1.0.0")
        self.assertEqual(CONTRACT_VALIDATOR.validate(contract), [])
        schema = read_json(
            ROOT
            / "skills"
            / "plan-biomedical-analysis"
            / "references"
            / "analysis-contract.schema.json"
        )
        self.assertEqual(VERIFIER.validate_schema(contract, schema), [])

        with tempfile.TemporaryDirectory(prefix="universal-v1-verifier-") as temporary:
            output = Path(temporary) / "verification-report.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(
                        ROOT
                        / "skills"
                        / "verify-biomedical-analysis"
                        / "scripts"
                        / "verify_bundle.py"
                    ),
                    "--bundle",
                    str(ROOT / "tests" / "fixtures" / "minimal-run"),
                    "--root",
                    str(ROOT),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            report = read_json(output)
            self.assertEqual(report["overall_status"], "pass")


if __name__ == "__main__":
    unittest.main(verbosity=2)
