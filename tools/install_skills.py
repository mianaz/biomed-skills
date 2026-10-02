#!/usr/bin/env python3
"""Install canonical skill packages, individual skills, or registry bundles."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


class RegistryError(ValueError):
    """Raised when a requested selection cannot be resolved safely."""


def skill_name(skill_dir: Path) -> str:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise ValueError(f"missing SKILL.md in {skill_dir}")
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"missing frontmatter in {skill_file}")
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip("'\"")
            if name != skill_dir.name:
                raise ValueError(f"name/folder mismatch: {skill_dir.name} != {name}")
            return name
    raise ValueError(f"missing frontmatter name in {skill_file}")


def load_registry(path: Path) -> dict:
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RegistryError(f"cannot read registry {path}: {exc}") from exc
    if not isinstance(registry, dict) or not str(registry.get("schema_version", "")).startswith("2."):
        raise RegistryError("installer requires suite registry schema major 2")
    if not isinstance(registry.get("skills"), list):
        raise RegistryError("registry skills must be an array")
    if not isinstance(registry.get("bundles"), dict):
        raise RegistryError("registry bundles must be an object")
    return registry


def registry_indexes(registry: dict) -> tuple[dict[str, dict], dict[str, str]]:
    entries: dict[str, dict] = {}
    aliases: dict[str, str] = {}
    for item in registry["skills"]:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise RegistryError("every registry skill must be an object with a name")
        name = item["name"]
        if name in entries:
            raise RegistryError(f"duplicate registry skill: {name}")
        entries[name] = item
    for name, item in entries.items():
        legacy_names = item.get("legacy_names", [])
        if not isinstance(legacy_names, list):
            raise RegistryError(f"legacy_names must be an array for {name}")
        for alias in legacy_names:
            if not isinstance(alias, str) or not alias:
                raise RegistryError(f"invalid legacy name for {name}")
            if alias in entries:
                raise RegistryError(f"legacy name is also canonical: {alias}")
            if alias in aliases and aliases[alias] != name:
                raise RegistryError(f"legacy name has multiple owners: {alias}")
            aliases[alias] = name
    return entries, aliases


def expand_bundle(name: str, bundles: dict, trail: tuple[str, ...] = ()) -> set[str]:
    if name not in bundles:
        raise RegistryError(f"unknown bundle: {name}")
    if name in trail:
        cycle = " -> ".join((*trail[trail.index(name) :], name))
        raise RegistryError(f"bundle inclusion cycle: {cycle}")
    bundle = bundles[name]
    if not isinstance(bundle, dict):
        raise RegistryError(f"bundle definition must be an object: {name}")
    skills = bundle.get("skills", [])
    includes = bundle.get("includes", [])
    if not isinstance(skills, list) or any(not isinstance(value, str) for value in skills):
        raise RegistryError(f"bundle skills must be an array of strings: {name}")
    if not isinstance(includes, list) or any(not isinstance(value, str) for value in includes):
        raise RegistryError(f"bundle includes must be an array of strings: {name}")
    resolved = set(skills)
    for included in includes:
        resolved.update(expand_bundle(included, bundles, (*trail, name)))
    return resolved


def resolve_selection(
    registry: dict,
    requested_skills: list[str] | None = None,
    requested_bundles: list[str] | None = None,
    include_recommended: bool = False,
) -> list[str]:
    """Resolve aliases, bundle inclusion, hard requirements, and recommendations."""
    entries, aliases = registry_indexes(registry)
    bundles = registry["bundles"]
    requested_skills = requested_skills or []
    requested_bundles = requested_bundles or []

    if not requested_skills and not requested_bundles:
        selected = set(entries)
    else:
        selected: set[str] = set()
        for requested in requested_skills:
            canonical = requested if requested in entries else aliases.get(requested)
            if canonical is None:
                raise RegistryError(f"unknown skill: {requested}")
            selected.add(canonical)
        for bundle_name in requested_bundles:
            selected.update(expand_bundle(bundle_name, bundles))

    unresolved_selection = sorted(selected - set(entries))
    if unresolved_selection:
        raise RegistryError(f"bundle references unknown skills: {', '.join(unresolved_selection)}")

    resolved: set[str] = set()
    pending = list(selected)
    while pending:
        name = pending.pop()
        if name in resolved:
            continue
        item = entries.get(name)
        if item is None:
            raise RegistryError(f"registry relation references unknown skill: {name}")
        resolved.add(name)
        relations = list(item.get("requires", []))
        if include_recommended:
            relations.extend(item.get("recommends", []))
        if any(not isinstance(value, str) for value in relations):
            raise RegistryError(f"requires/recommends must contain strings for {name}")
        unknown = sorted(set(relations) - set(entries))
        if unknown:
            raise RegistryError(f"unresolved registry relations for {name}: {', '.join(unknown)}")
        pending.extend(relations)

    # Preserve registry order for stable previews and installation reports.
    return [name for name in entries if name in resolved]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="Destination skill directory")
    parser.add_argument("--source", type=Path, help="Canonical skills directory")
    parser.add_argument("--registry", type=Path, help="Suite registry; defaults to suite.json beside this tool")
    parser.add_argument("--skill", action="append", dest="selected", help="Install this skill and its hard requirements; repeat as needed")
    parser.add_argument("--bundle", action="append", dest="bundles", help="Install a named bundle; repeat as needed")
    parser.add_argument(
        "--include-recommended",
        action="store_true",
        help="Also install recursively recommended skills and their hard requirements",
    )
    parser.add_argument("--mode", choices=("copy", "symlink"), default="copy")
    parser.add_argument("--replace", action="store_true", help="Move collisions to timestamped backups before installing")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repository = Path(__file__).resolve().parents[1]
    source = (args.source or repository / "skills").resolve()
    registry_path = (args.registry or repository / "suite.json").resolve()
    target = args.target.expanduser().resolve()

    try:
        registry = load_registry(registry_path)
        selected_names = resolve_selection(registry, args.selected, args.bundles, args.include_recommended)
    except RegistryError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2

    source_directories = {name: source / name for name in selected_names}
    missing_packages = sorted(name for name, path in source_directories.items() if not (path / "SKILL.md").is_file())
    if missing_packages:
        print(json.dumps({"error": "selected skills are absent from source", "skills": missing_packages}), file=sys.stderr)
        return 2

    actions: list[dict] = []
    errors: list[str] = []
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for name in selected_names:
        source_dir = source_directories[name]
        try:
            canonical_name = skill_name(source_dir)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        destination = target / canonical_name
        action = {"skill": canonical_name, "source": str(source_dir), "destination": str(destination), "mode": args.mode}
        if destination.is_symlink() and destination.resolve() == source_dir.resolve() and args.mode == "symlink":
            action["action"] = "unchanged"
        elif destination.exists() or destination.is_symlink():
            if not args.replace:
                action["action"] = "collision"
                errors.append(f"destination exists: {destination}")
            else:
                backup = target / f"{canonical_name}.backup-{stamp}"
                if backup.exists():
                    errors.append(f"backup path already exists: {backup}")
                    action["action"] = "collision"
                else:
                    action["action"] = "replace"
                    action["backup"] = str(backup)
        else:
            action["action"] = "install"
        actions.append(action)

    selection = {
        "requested_skills": args.selected or [],
        "requested_bundles": args.bundles or [],
        "include_recommended": args.include_recommended,
        "resolved_skills": selected_names,
    }
    if errors and not args.dry_run:
        print(json.dumps({"status": "refused", "selection": selection, "errors": errors, "actions": actions}, indent=2))
        return 1

    if not args.dry_run:
        target.mkdir(parents=True, exist_ok=True)
        for action in actions:
            if action["action"] in {"unchanged", "collision"}:
                continue
            source_dir = Path(action["source"])
            destination = Path(action["destination"])
            if action["action"] == "replace":
                destination.rename(action["backup"])
            if args.mode == "copy":
                shutil.copytree(source_dir, destination)
            else:
                os.symlink(source_dir, destination, target_is_directory=True)

    status = "dry_run" if args.dry_run else "installed"
    print(json.dumps({"status": status, "selection": selection, "errors": errors, "actions": actions}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
