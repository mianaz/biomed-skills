from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INSTALLER_PATH = ROOT / "tools" / "install_skills.py"
AUDITOR_PATH = ROOT / "skills" / "maintain-biomedical-skills" / "scripts" / "audit_skill_suite.py"

SPEC = importlib.util.spec_from_file_location("install_skills", INSTALLER_PATH)
assert SPEC and SPEC.loader
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)


def entry(name: str, *, requires: list[str] | None = None, recommends: list[str] | None = None) -> dict:
    return {
        "name": name,
        "kind": "leaf",
        "scopes": ["any"],
        "stage": "analysis",
        "requires": requires or [],
        "recommends": recommends or [],
        "routes_to": [],
        "optional_capabilities": [],
        "legacy_names": [],
    }


class InstallerResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        core = entry("core-skill")
        leaf = entry("leaf-skill", requires=["core-skill"], recommends=["recommended-skill"])
        leaf["legacy_names"] = ["old-leaf"]
        recommended = entry("recommended-skill", requires=["core-skill"])
        self.registry = {
            "schema_version": "2.0.0",
            "skills": [core, leaf, recommended],
            "bundles": {
                "base": {"description": "base", "includes": [], "skills": ["core-skill"]},
                "pack": {"description": "pack", "includes": ["base"], "skills": ["leaf-skill"]},
            },
        }

    def test_bundle_adds_hard_requirement_but_not_recommendation(self) -> None:
        self.assertEqual(
            INSTALLER.resolve_selection(self.registry, requested_bundles=["pack"]),
            ["core-skill", "leaf-skill"],
        )

    def test_include_recommended_is_recursive_and_legacy_names_resolve(self) -> None:
        self.assertEqual(
            INSTALLER.resolve_selection(
                self.registry,
                requested_skills=["old-leaf"],
                include_recommended=True,
            ),
            ["core-skill", "leaf-skill", "recommended-skill"],
        )

    def test_no_selector_installs_all(self) -> None:
        self.assertEqual(
            INSTALLER.resolve_selection(self.registry),
            ["core-skill", "leaf-skill", "recommended-skill"],
        )

    def test_bundle_cycle_is_refused(self) -> None:
        self.registry["bundles"]["base"]["includes"] = ["pack"]
        with self.assertRaisesRegex(INSTALLER.RegistryError, "bundle inclusion cycle"):
            INSTALLER.resolve_selection(self.registry, requested_bundles=["pack"])


class RegistryAuditTests(unittest.TestCase):
    def run_audit(
        self,
        registry: dict,
        extra_files: dict[str, str] | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], dict]:
        with tempfile.TemporaryDirectory(prefix="registry-v2-test-") as temporary:
            temporary_path = Path(temporary)
            skills_root = temporary_path / "skills"
            skill_root = skills_root / "alpha-skill"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\n"
                "name: alpha-skill\n"
                "description: Use when testing a complete registry audit fixture safely.\n"
                "---\n\n"
                "# Alpha skill\n",
                encoding="utf-8",
            )
            registry_path = temporary_path / "suite.json"
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            for relative_path, content in (extra_files or {}).items():
                destination = temporary_path / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(content, encoding="utf-8")
            output_path = temporary_path / "audit.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(AUDITOR_PATH),
                    str(skills_root),
                    "--registry",
                    str(registry_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
            )
            return completed, json.loads(output_path.read_text(encoding="utf-8"))

    def test_valid_v2_registry_passes(self) -> None:
        alpha = entry("alpha-skill")
        registry = {
            "schema_version": "2.0.0",
            "resource_profiles": {},
            "skills": [alpha],
            "bundles": {
                "core": {"description": "test bundle", "includes": [], "skills": ["alpha-skill"]}
            },
        }
        completed, report = self.run_audit(registry)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(report["summary"]["error"], 0)

    def test_valid_resource_profile_and_relative_references_pass(self) -> None:
        alpha = entry("alpha-skill")
        alpha["resource_profiles"] = ["alpha-analysis"]
        registry = {
            "schema_version": "2.0.0",
            "resource_profiles": {"alpha-analysis": "profiles/alpha/profile.json"},
            "skills": [alpha],
            "bundles": {
                "core": {"description": "test bundle", "includes": [], "skills": ["alpha-skill"]}
            },
        }
        profile = {
            "schema_version": "1.0.0",
            "profile_id": "alpha-analysis",
            "scope": "any",
            "contract_extension": {"key": "alpha", "schema": "contract.schema.json"},
            "verification": {
                "catalog": "checks.json",
                "required_categories": ["data_integrity"],
            },
        }
        completed, report = self.run_audit(
            registry,
            {
                "profiles/alpha/profile.json": json.dumps(profile),
                "profiles/alpha/contract.schema.json": "{}",
                "profiles/alpha/checks.json": "{}",
            },
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(report["summary"]["error"], 0)

    def test_invalid_relations_profiles_and_bundle_cycles_are_reported(self) -> None:
        alpha = entry("alpha-skill", requires=["missing-skill"])
        registry = {
            "schema_version": "2.0.0",
            "resource_profiles": {"large-memory": "profiles/missing.json"},
            "skills": [alpha],
            "bundles": {
                "first": {"description": "first", "includes": ["second"], "skills": ["alpha-skill"]},
                "second": {"description": "second", "includes": ["first"], "skills": []},
            },
        }
        completed, report = self.run_audit(registry)
        codes = {finding["code"] for finding in report["findings"]}
        self.assertEqual(completed.returncode, 1)
        self.assertIn("registry-requires-missing", codes)
        self.assertIn("registry-resource-profile-missing", codes)
        self.assertIn("registry-bundle-cycle", codes)


if __name__ == "__main__":
    unittest.main()
