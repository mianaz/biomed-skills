#!/usr/bin/env python3
"""Check the paper-framing folder's structure and local resource links.

This validates packaging, not scientific accuracy or writing quality.
Only Python's standard library is required.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


def check_package(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    entry = root / "SKILL.md"
    if not entry.is_file():
        return [f"Missing entry point: {entry}"]
    text = entry.read_text(encoding="utf-8")
    match = re.search(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append("SKILL.md is missing YAML frontmatter")
    else:
        frontmatter = match.group(1)
        name = re.search(r"^name:\s*([^\n]+)$", frontmatter, re.M)
        if not name or name.group(1).strip() != root.name:
            errors.append("The frontmatter name must match the directory name")
        if not re.search(r"^description:\s*\S", frontmatter, re.M):
            errors.append("The frontmatter description is missing")

    # Runtime prose should not require any upstream skill. Provenance is kept
    # in the repository's docs/ directory, outside the installed skill.
    external = re.compile(
        r"nature-(?:writing|polishing|shared)|humanizer|paper-storycraft|"
        r"paper-journal-club|sc-paper-distill|hpc-etiquette|ponytail|simplify",
        re.I,
    )
    files = [entry, *sorted((root / "references").glob("*.md")),
             *sorted((root / "assets").glob("*.md"))]
    for path in files:
        content = path.read_text(encoding="utf-8")
        if external.search(content):
            errors.append(f"External skill reference in {path.relative_to(root)}")
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            address = link.strip().split(" ", 1)[0]
            parts = urlsplit(address)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            target = (path.parent / unquote(parts.path)).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                errors.append(f"Resource leaves the skill directory: {link}")
                continue
            if not target.exists():
                errors.append(f"Missing local resource: {link}")
    for required in ["agents/openai.yaml", "tests/behavior-cases.md"]:
        if not (root / required).is_file():
            errors.append(f"Missing packaged resource: {required}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = check_package(root)
    if errors:
        print("Package check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PASS: frontmatter, local resource links and skill isolation")
    print("Writing behavior and scientific accuracy were not evaluated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
