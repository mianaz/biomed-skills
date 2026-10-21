#!/usr/bin/env python3
"""Validate writing-package files and internal references; no agent evaluation."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

WRITING = ('paper-framing', 'paper-writing', 'paper-polishing')
SHARED = 'biomed-shared'
CONSUMERS = ('paper-distill', 'paper-evidence-map', 'protocol-to-methods', 'submission-check')
LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
EXTERNAL_SKILL = re.compile(r'\b(?:nature-writing|nature-polishing|nature-shared|humanizer|paper-storycraft|paper-journal-club|sc-paper-distill)\b', re.I)


def check(skills: Path, integration: bool = False) -> list[str]:
    """Check three writing skills; optionally check shared links in four consumers."""
    skills = skills.resolve()
    errors: list[str] = []
    for name in WRITING + (SHARED,):
        folder = skills / name
        if not folder.is_dir() or folder.is_symlink():
            errors.append(f'Missing or symbolic package directory: {name}')
    if errors:
        return errors
    if (skills / SHARED / 'SKILL.md').exists():
        errors.append('Shared references must not expose an independent SKILL.md')

    names = WRITING + (CONSUMERS if integration else ())
    for name in names:
        entry = skills / name / 'SKILL.md'
        if not entry.is_file():
            errors.append(f'Missing entry point: {name}/SKILL.md')
            continue
        text = entry.read_text(encoding='utf-8')
        if f'../{SHARED}/writing-principles.md' not in LINK.findall(text):
            errors.append(f'Missing explicit writing-principles pointer: {name}')
        if name in WRITING:
            front = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
            if not front or not re.search(rf'^name: {re.escape(name)}$', front[1], re.M):
                errors.append(f'Invalid name or frontmatter: {name}')
            if not front or not re.search(r'^description: \S.+$', front[1], re.M):
                errors.append(f'Missing description: {name}')
            if not (entry.parent / 'agents/openai.yaml').is_file():
                errors.append(f'Missing agent metadata: {name}')

    docs = [p for name in WRITING + (SHARED,) for p in (skills / name).rglob('*.md')]
    if integration:
        docs += [skills / name / 'SKILL.md' for name in CONSUMERS]
    for path in docs:
        if not path.is_file():
            continue
        relative = path.relative_to(skills)
        if path.is_symlink():
            errors.append(f'Symbolic resource: {relative}')
            continue
        text = path.read_text(encoding='utf-8')
        if EXTERNAL_SKILL.search(text):
            errors.append(f'External skill dependency in runtime prose: {relative}')
        for link in LINK.findall(text):
            address = link.strip().split(' ', 1)[0]
            parts = urlsplit(address)
            if parts.scheme or parts.netloc:
                if parts.path.lower().endswith('/skill.md'):
                    errors.append(f'External skill link: {relative}: {link}')
                continue
            if not parts.path:
                continue
            # Existing consumers retain their other, separately maintained resources.
            if path.parent.name in CONSUMERS and not parts.path.startswith(f'../{SHARED}/'):
                continue
            target = path.parent / unquote(parts.path)
            if target.is_symlink() or any(p.is_symlink() for p in target.parents if p != skills):
                errors.append(f'Symbolic link target: {relative}: {link}')
                continue
            try:
                target.resolve().relative_to(skills)
            except ValueError:
                errors.append(f'Resource leaves the installed suite: {relative}: {link}')
                continue
            if not target.is_file():
                errors.append(f'Missing local file: {relative}: {link}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-root', type=Path, default=Path(__file__).resolve().parents[1] / 'skills')
    parser.add_argument('--integration', action='store_true', help='Also check shared pointers in four existing consumers')
    args = parser.parse_args()
    try:
        errors = check(args.skills_root, args.integration)
    except (OSError, UnicodeError, ValueError) as exc:
        errors = [str(exc)]
    for error in errors:
        print(f'ERROR: {error}')
    if not errors:
        print('PASS: writing package structure and bundled reference paths')
    print('Agent routing and manuscript quality are not evaluated by this check.')
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
