"""Structural regression tests; these do not evaluate manuscript quality."""
from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_package", SOURCE / "scripts/check_package.py")
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class PackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "paper-framing"
        shutil.copytree(SOURCE, self.root, ignore=shutil.ignore_patterns("__pycache__"))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def append(self, text: str) -> None:
        with (self.root / "SKILL.md").open("a", encoding="utf-8") as handle:
            handle.write("\n" + text + "\n")

    def test_isolated_install(self) -> None:
        self.assertEqual(CHECKER.check_package(self.root), [])

    def test_missing_resource(self) -> None:
        (self.root / "references/section-writing.md").unlink()
        self.assertTrue(CHECKER.check_package(self.root))

    def test_external_dependency(self) -> None:
        self.append("Apply `nature-writing` before drafting.")
        self.assertTrue(CHECKER.check_package(self.root))

    def test_parent_resource(self) -> None:
        self.append("[External resource](../another-skill/SKILL.md)")
        self.assertTrue(CHECKER.check_package(self.root))

    def test_wrong_name(self) -> None:
        entry = self.root / "SKILL.md"
        entry.write_text(entry.read_text().replace("name: paper-framing", "name: wrong"))
        self.assertTrue(CHECKER.check_package(self.root))

    def test_missing_frontmatter(self) -> None:
        entry = self.root / "SKILL.md"
        entry.write_text(entry.read_text().split("---\n", 2)[-1])
        self.assertTrue(CHECKER.check_package(self.root))

    def test_missing_metadata(self) -> None:
        (self.root / "agents/openai.yaml").unlink()
        self.assertTrue(CHECKER.check_package(self.root))

    def test_source_url_is_allowed(self) -> None:
        self.append("[Official source](https://example.org/article)")
        self.assertEqual(CHECKER.check_package(self.root), [])


if __name__ == "__main__":
    unittest.main()
