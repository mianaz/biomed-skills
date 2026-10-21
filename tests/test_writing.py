"""Structural regression tests. Agent behavior is evaluated separately."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_writing import CONSUMERS, WRITING, check
from build_writing_bundle import build


class WritingPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / 'suite'
        shutil.copytree(ROOT / 'skills', self.repo / 'skills', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        shutil.copy2(ROOT / 'LICENSE', self.repo / 'LICENSE')
        self.skills = self.repo / 'skills'
        self.entry = self.skills / 'paper-framing/SKILL.md'

    def tearDown(self):
        self.temp.cleanup()

    def append(self, text):
        with self.entry.open('a', encoding='utf-8') as handle:
            handle.write('\n' + text + '\n')

    def test_writing_package(self):
        self.assertEqual(check(self.skills), [])

    def test_integrated_consumers(self):
        self.assertEqual(check(self.skills, True), [])

    def test_missing_shared_directory(self):
        shutil.rmtree(self.skills / 'biomed-shared')
        self.assertTrue(check(self.skills))

    def test_missing_shared_principles(self):
        (self.skills / 'biomed-shared/writing-principles.md').unlink()
        self.assertTrue(check(self.skills))

    def test_missing_section(self):
        (self.skills / 'paper-writing/references/results.md').unlink()
        self.assertTrue(check(self.skills))

    def test_parent_escape(self):
        self.append('[Outside](../../../private.md)')
        self.assertTrue(check(self.skills))

    def test_encoded_escape(self):
        self.append('[Outside](%2e%2e/%2e%2e/private.md)')
        self.assertTrue(check(self.skills))

    def test_shared_sibling_allowed(self):
        self.append('[Principles](../biomed-shared/writing-principles.md)')
        self.assertEqual(check(self.skills), [])

    def test_external_skill_name(self):
        self.append('Apply nature-writing before drafting.')
        self.assertTrue(check(self.skills))

    def test_external_skill_link(self):
        self.append('[Required](https://example.org/other/SKILL.md)')
        self.assertTrue(check(self.skills))

    def test_literature_url_allowed(self):
        self.append('[Paper](https://example.org/article)')
        self.assertEqual(check(self.skills), [])

    def test_wrong_name(self):
        self.entry.write_text(self.entry.read_text().replace('name: paper-framing', 'name: wrong'))
        self.assertTrue(check(self.skills))

    def test_missing_description(self):
        self.entry.write_text('\n'.join(line for line in self.entry.read_text().split('\n') if not line.startswith('description:')))
        self.assertTrue(check(self.skills))

    def test_missing_metadata(self):
        (self.skills / 'paper-framing/agents/openai.yaml').unlink()
        self.assertTrue(check(self.skills))

    def test_shared_is_not_entry(self):
        (self.skills / 'biomed-shared/SKILL.md').write_text('Accidental entry')
        self.assertTrue(check(self.skills))

    def test_consumer_requires_shared_pointer(self):
        p = self.skills / f'{CONSUMERS[0]}/SKILL.md'
        p.write_text(p.read_text().replace('../biomed-shared/writing-principles.md', '../biomed-shared/README.md'))
        self.assertTrue(check(self.skills, True))

    def test_symbolic_reference(self):
        p = self.skills / 'paper-writing/references/results.md'
        p.unlink()
        p.symlink_to(self.skills / 'biomed-shared/README.md')
        self.assertTrue(check(self.skills))

    def test_bundle_isolated_install(self):
        destination = self.repo / 'bundle.zip'
        build(self.repo, destination)
        with zipfile.ZipFile(destination) as handle:
            handle.extractall(self.repo / 'isolated')
        installed = self.repo / 'isolated/skills'
        self.assertEqual(check(installed), [])
        self.assertEqual({p.name for p in installed.iterdir()}, set(WRITING) | {'biomed-shared'})
        self.assertEqual((installed / 'biomed-shared/writing-principles.md').read_bytes(), (self.skills / 'biomed-shared/writing-principles.md').read_bytes())

    def test_archive_overwrite_refused(self):
        p = self.repo / 'bundle.zip'
        p.write_bytes(b'existing')
        with self.assertRaises(FileExistsError):
            build(self.repo, p)
        self.assertEqual(p.read_bytes(), b'existing')

    def test_archive_inside_sources_refused(self):
        with self.assertRaises(ValueError):
            build(self.repo, self.skills / 'paper-framing/bundle.zip')

    def test_license_required(self):
        (self.repo / 'LICENSE').unlink()
        with self.assertRaises(FileNotFoundError):
            build(self.repo, self.repo / 'bundle.zip')

    def test_evaluation_cases_well_formed(self):
        data = json.loads((ROOT / 'tests/writing-cases.json').read_text())
        self.assertEqual(data['status'], 'not_run_on_agent')
        cases = data['cases']
        self.assertEqual(len({c['id'] for c in cases}), len(cases))
        for c in cases:
            self.assertTrue(c['prompt'] and c['primary'] and c['completion'])
            for path in c.get('required_resources', []):
                self.assertTrue((self.skills / path).is_file(), path)
        self.assertTrue(set(WRITING).issubset({c['primary'] for c in cases}))


if __name__ == '__main__':
    unittest.main()
