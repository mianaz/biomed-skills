#!/usr/bin/env python3
"""Build a portable writing bundle containing its shared references."""
from __future__ import annotations

import argparse
import tempfile
import zipfile
from pathlib import Path

from check_writing import SHARED, WRITING, check

INSTALL = '''# Install the biomedical writing skills

Copy the four complete directories under `skills/` into your agent's configured
skill directory. Keep `biomed-shared/` beside `paper-framing/`, `paper-writing/`
and `paper-polishing/`. The shared folder supplies references and is not a task.

Use paper-framing to develop the scientific story, paper-writing to draft text,
and paper-polishing to improve existing prose. This package supplies the writing
guidance. Related analysis and protocol workflows are in the complete suite.

When replacing the earlier framing bundle, back up the old paper-framing folder
and replace it with this complete folder. This removes the old section-writing
reference and package checker, whose responsibilities have moved. Activate the
updated skills using the instructions for your agent.
'''


def build(repo: Path, destination: Path) -> None:
    repo = repo.resolve()
    errors = check(repo / 'skills')
    if errors:
        raise ValueError('; '.join(errors))
    sources = [p for name in WRITING + (SHARED,) for p in (repo / 'skills' / name).rglob('*')
               if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc']
    for source in sources:
        if source.is_symlink() or any(p.is_symlink() for p in source.parents if p != repo):
            raise ValueError(f'Symbolic resource cannot be packaged: {source}')
    destination = destination.resolve()
    if destination.is_relative_to((repo / 'skills').resolve()):
        raise ValueError('Write the archive outside the skill directories')
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(f'Archive already exists: {destination}')
    license_file = repo / 'LICENSE'
    if not license_file.is_file():
        raise FileNotFoundError('Repository LICENSE is required for distribution')
    with tempfile.TemporaryDirectory() as work:
        archive = Path(work) / 'writing.zip'
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as handle:
            for source in sorted(sources):
                handle.write(source, source.relative_to(repo).as_posix())
            handle.write(license_file, 'LICENSE')
            handle.writestr('INSTALL.md', INSTALL)
        with zipfile.ZipFile(archive) as handle:
            handle.extractall(Path(work) / 'check')
        errors = check(Path(work) / 'check/skills')
        if errors:
            raise ValueError('Archive validation failed: ' + '; '.join(errors))
        with destination.open('xb') as output:
            output.write(archive.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        build(Path(__file__).resolve().parents[1], args.destination)
    except (OSError, ValueError, UnicodeError) as exc:
        parser.exit(1, f'ERROR: {exc}\n')
    print(f'Created and checked {args.destination}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
