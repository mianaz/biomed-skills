#!/usr/bin/env python3
"""Audit a directory of agent skills for structure, collisions, and portability."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESOURCE_RE = re.compile(r"(?<![A-Za-z0-9_.-])((?:references|scripts|assets)/[A-Za-z0-9_./-]+)")
FORBIDDEN_DOCS = {"README.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md", "CHANGELOG.md"}
REGISTRY_FIELDS = {
    "name",
    "kind",
    "scopes",
    "stage",
    "requires",
    "recommends",
    "routes_to",
    "optional_capabilities",
    "legacy_names",
}
REGISTRY_OPTIONAL_FIELDS = {"resource_profiles"}
SKILL_KINDS = {"foundation", "router", "leaf", "adapter", "governance"}
LIFECYCLE_STAGES = {
    "planning",
    "acquisition",
    "preparation",
    "analysis",
    "verification",
    "interpretation",
    "communication",
    "orchestration",
    "governance",
    "cross-cutting",
}
COUPLING = {
    ".claude/skills": "Claude-specific skill path",
    ".codex/skills": "Codex-specific skill path",
    "Agent tool": "provider-specific agent API",
    "claude code": "provider-specific harness name",
    "sonnet": "provider-specific model name",
    "opus": "provider-specific model name",
    "localhost:": "fixed local service endpoint",
    "/tmp/": "ephemeral absolute path",
}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, ["missing opening YAML frontmatter delimiter"]
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return {}, text, ["missing closing YAML frontmatter delimiter"]
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"unparseable frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith(('"', "'")) and value.endswith(value[0]):
            value = value[1:-1]
        if key in values:
            errors.append(f"duplicate frontmatter key: {key}")
        values[key] = value
    return values, "\n".join(lines[end + 1 :]).strip(), errors


def normalized_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills_root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--registry", type=Path, help="Optional suite.json registry; defaults to the parent directory")
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args()

    root = args.skills_root.resolve()
    output = (args.output or root.parent / "skill-audit.json").resolve()
    findings: list[dict] = []
    records: list[dict] = []
    names: dict[str, list[str]] = defaultdict(list)
    descriptions: dict[str, list[str]] = defaultdict(list)
    bodies: dict[str, list[str]] = defaultdict(list)

    def add(severity: str, code: str, skill: str, message: str, path: Path | None = None) -> None:
        findings.append(
            {
                "severity": severity,
                "code": code,
                "skill": skill,
                "message": message,
                "path": str(path) if path else None,
            }
        )

    if not root.is_dir():
        print(f"skills root does not exist: {root}", file=sys.stderr)
        return 2

    for skill_md in sorted(root.glob("*/SKILL.md")):
        folder = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8")
        frontmatter, body, frontmatter_errors = parse_frontmatter(text)
        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        for message in frontmatter_errors:
            add("error", "frontmatter-parse", folder, message, skill_md)
        unknown_keys = sorted(set(frontmatter) - {"name", "description"})
        if unknown_keys:
            add("error", "frontmatter-extra-fields", folder, f"unsupported keys: {', '.join(unknown_keys)}", skill_md)
        if not name:
            add("error", "name-missing", folder, "frontmatter name is missing", skill_md)
        elif name != folder:
            add("error", "name-folder-mismatch", folder, f"frontmatter name '{name}' differs from folder", skill_md)
        if name and (len(name) > 63 or not NAME_RE.fullmatch(name)):
            add("error", "name-invalid", folder, "name must be lowercase hyphen-case and under 64 characters", skill_md)
        if not description:
            add("error", "description-missing", folder, "frontmatter description is missing", skill_md)
        elif len(description) < 40:
            add("warning", "description-short", folder, "description may not explain capability and trigger", skill_md)
        if description and not re.search(r"\b(use|when|whenever|for)\b", description, re.I):
            add("warning", "description-trigger", folder, "description lacks an explicit trigger/context", skill_md)
        if "TODO" in text:
            add("error", "placeholder", folder, "unresolved TODO placeholder", skill_md)
        line_count = len(text.splitlines())
        if line_count > 500:
            add("warning", "skill-too-long", folder, f"SKILL.md has {line_count} lines; split details into references", skill_md)

        for match in RESOURCE_RE.finditer(text):
            relative = match.group(1).rstrip(".,);:'\"`")
            target = skill_md.parent / relative
            if not target.exists():
                add("error", "resource-missing", folder, f"referenced resource does not exist: {relative}", target)

        for path in skill_md.parent.iterdir():
            if path.is_file() and path.name in FORBIDDEN_DOCS:
                add("warning", "extraneous-doc", folder, f"skill package contains {path.name}", path)

        agent_yaml = skill_md.parent / "agents" / "openai.yaml"
        if not agent_yaml.exists():
            add("warning", "agent-metadata-missing", folder, "agents/openai.yaml is absent", agent_yaml)
        else:
            agent_text = agent_yaml.read_text(encoding="utf-8")
            if name and f"${name}" not in agent_text:
                add("warning", "agent-default-prompt", folder, "default prompt does not mention the skill name", agent_yaml)

        scan_files = [skill_md]
        reference_dir = skill_md.parent / "references"
        if reference_dir.is_dir():
            scan_files.extend(path for path in reference_dir.rglob("*") if path.is_file())
        for path in scan_files:
            content = path.read_text(encoding="utf-8", errors="replace").lower()
            for token, label in COUPLING.items():
                if token.lower() in content:
                    add("warning", "platform-coupling", folder, f"{label}: {token}", path)

        if name:
            names[name].append(folder)
        if description:
            descriptions[normalized_hash(description)].append(folder)
        if body:
            bodies[normalized_hash(body)].append(folder)
        records.append(
            {
                "folder": folder,
                "name": name,
                "description": description,
                "skill_lines": line_count,
                "reference_files": len(list(reference_dir.rglob("*"))) if reference_dir.is_dir() else 0,
            }
        )

    for name, folders in names.items():
        if len(folders) > 1:
            add("error", "name-collision", name, f"duplicate frontmatter name in: {', '.join(folders)}")
    for folders in descriptions.values():
        if len(folders) > 1:
            add("warning", "description-duplicate", folders[0], f"identical descriptions: {', '.join(folders)}")
    for folders in bodies.values():
        if len(folders) > 1:
            add("warning", "body-duplicate", folders[0], f"identical normalized bodies: {', '.join(folders)}")

    registry_path = (args.registry or root.parent / "suite.json").resolve()
    if registry_path.is_file():
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            add("error", "registry-invalid", "suite", f"cannot read registry JSON: {exc}", registry_path)
            registry = {}
        if not isinstance(registry, dict):
            add("error", "registry-root", "suite", "registry root must be an object", registry_path)
            registry = {}

        schema_version = registry.get("schema_version")
        if not isinstance(schema_version, str) or not schema_version.startswith("2."):
            add("error", "registry-schema-version", "suite", "schema_version must use registry schema major 2", registry_path)

        entries = registry.get("skills", [])
        if not isinstance(entries, list):
            add("error", "registry-skills", "suite", "registry skills must be an array", registry_path)
            entries = []
        registry_names = [str(item.get("name")) for item in entries if isinstance(item, dict) and item.get("name")]
        duplicate_registry_names = sorted({name for name in registry_names if registry_names.count(name) > 1})
        if duplicate_registry_names:
            add("error", "registry-name-collision", "suite", f"duplicate registry names: {', '.join(duplicate_registry_names)}", registry_path)
        active_names = {record["name"] for record in records if record["name"]}
        registry_name_set = set(registry_names)
        missing_from_registry = sorted(active_names - registry_name_set)
        missing_from_disk = sorted(registry_name_set - active_names)
        if missing_from_registry:
            add("error", "registry-missing-entry", "suite", f"skills absent from registry: {', '.join(missing_from_registry)}", registry_path)
        if missing_from_disk:
            add("error", "registry-missing-skill", "suite", f"registry entries absent from disk: {', '.join(missing_from_disk)}", registry_path)

        profile_paths = registry.get("resource_profiles", {})
        if not isinstance(profile_paths, dict):
            add("error", "registry-resource-profiles", "suite", "resource_profiles must be an object mapping profile IDs to relative files", registry_path)
            profile_paths = {}
        registry_directory = registry_path.parent
        for profile_id, relative_path in profile_paths.items():
            profile_name = str(profile_id)
            if not NAME_RE.fullmatch(profile_name):
                add("error", "registry-resource-profile-id", "suite", f"invalid resource profile ID: {profile_name}", registry_path)
            if not isinstance(relative_path, str) or not relative_path:
                add("error", "registry-resource-profile-path", "suite", f"resource profile '{profile_name}' must name a relative file", registry_path)
                continue
            candidate = Path(relative_path)
            if candidate.is_absolute():
                add("error", "registry-resource-profile-path", "suite", f"resource profile '{profile_name}' uses an absolute path", registry_path)
                continue
            resolved = (registry_directory / candidate).resolve()
            try:
                resolved.relative_to(registry_directory)
            except ValueError:
                add("error", "registry-resource-profile-path", "suite", f"resource profile '{profile_name}' escapes the suite directory", registry_path)
                continue
            if not resolved.is_file():
                add("error", "registry-resource-profile-missing", "suite", f"resource profile file does not exist: {relative_path}", resolved)
                continue
            try:
                profile = json.loads(resolved.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                add("error", "registry-resource-profile-invalid", "suite", f"cannot read resource profile '{profile_name}': {exc}", resolved)
                continue
            if not isinstance(profile, dict):
                add("error", "registry-resource-profile-invalid", "suite", f"resource profile '{profile_name}' must be a JSON object", resolved)
                continue
            required_profile_fields = {"schema_version", "profile_id", "scope", "contract_extension", "verification"}
            missing_profile_fields = sorted(required_profile_fields - set(profile))
            if missing_profile_fields:
                add("error", "registry-resource-profile-fields", "suite", f"resource profile '{profile_name}' is missing: {', '.join(missing_profile_fields)}", resolved)
            if profile.get("profile_id") != profile_name:
                add("error", "registry-resource-profile-id-mismatch", "suite", f"resource profile ID does not match registry key '{profile_name}'", resolved)
            if not isinstance(profile.get("schema_version"), str) or not profile.get("schema_version"):
                add("error", "registry-resource-profile-version", "suite", f"resource profile '{profile_name}' needs a schema_version", resolved)
            if not isinstance(profile.get("scope"), str) or not profile.get("scope"):
                add("error", "registry-resource-profile-scope", "suite", f"resource profile '{profile_name}' needs a scope", resolved)

            contract_extension = profile.get("contract_extension")
            verification = profile.get("verification")
            if not isinstance(contract_extension, dict) or not isinstance(contract_extension.get("key"), str) or not contract_extension.get("key"):
                add("error", "registry-resource-profile-contract", "suite", f"resource profile '{profile_name}' needs contract_extension.key", resolved)
            if not isinstance(verification, dict):
                add("error", "registry-resource-profile-verification", "suite", f"resource profile '{profile_name}' needs a verification object", resolved)
                verification = {}
            categories = verification.get("required_categories")
            if not isinstance(categories, list) or not categories or any(not isinstance(value, str) or not value for value in categories):
                add("error", "registry-resource-profile-categories", "suite", f"resource profile '{profile_name}' needs non-empty verification.required_categories", resolved)

            referenced_files = []
            if isinstance(contract_extension, dict):
                referenced_files.append(("contract_extension.schema", contract_extension.get("schema")))
            referenced_files.append(("verification.catalog", verification.get("catalog")))
            for field, referenced_path in referenced_files:
                if not isinstance(referenced_path, str) or not referenced_path:
                    add("error", "registry-resource-profile-reference", "suite", f"resource profile '{profile_name}' needs {field}", resolved)
                    continue
                reference = Path(referenced_path)
                if reference.is_absolute():
                    add("error", "registry-resource-profile-reference", "suite", f"resource profile '{profile_name}' uses an absolute {field} path", resolved)
                    continue
                reference_resolved = (resolved.parent / reference).resolve()
                try:
                    reference_resolved.relative_to(registry_directory)
                except ValueError:
                    add("error", "registry-resource-profile-reference", "suite", f"resource profile '{profile_name}' {field} escapes the suite directory", resolved)
                    continue
                if not reference_resolved.is_file():
                    add("error", "registry-resource-profile-reference-missing", "suite", f"resource profile '{profile_name}' {field} does not exist: {referenced_path}", reference_resolved)

        relation_graphs: dict[str, dict[str, list[str]]] = {
            "requires": {},
            "routes_to": {},
        }
        legacy_owners: dict[str, list[str]] = defaultdict(list)

        def string_list(item: dict, field: str, name: str, *, nonempty: bool = False) -> list[str]:
            value = item.get(field)
            if not isinstance(value, list) or any(not isinstance(entry, str) or not entry for entry in value):
                add("error", f"registry-{field.replace('_', '-')}", name, f"{field} must be an array of non-empty strings", registry_path)
                return []
            if nonempty and not value:
                add("error", f"registry-{field.replace('_', '-')}", name, f"{field} must not be empty", registry_path)
            duplicates = sorted({entry for entry in value if value.count(entry) > 1})
            if duplicates:
                add("error", f"registry-{field.replace('_', '-')}-duplicate", name, f"duplicate {field}: {', '.join(duplicates)}", registry_path)
            return list(value)

        for item in entries:
            if not isinstance(item, dict) or not item.get("name"):
                add("error", "registry-entry", "suite", "every skill entry must be an object with a name", registry_path)
                continue
            name = str(item["name"])
            missing_fields = sorted(REGISTRY_FIELDS - set(item))
            unknown_fields = sorted(set(item) - REGISTRY_FIELDS - REGISTRY_OPTIONAL_FIELDS)
            if missing_fields:
                add("error", "registry-entry-fields", name, f"missing required fields: {', '.join(missing_fields)}", registry_path)
            if unknown_fields:
                add("error", "registry-entry-fields", name, f"unsupported fields: {', '.join(unknown_fields)}", registry_path)
            if not NAME_RE.fullmatch(name):
                add("error", "registry-name-invalid", name, "registry name must be lowercase hyphen-case", registry_path)

            kind = item.get("kind")
            if kind not in SKILL_KINDS:
                add("error", "registry-kind", name, f"kind must be one of: {', '.join(sorted(SKILL_KINDS))}", registry_path)
            stage = item.get("stage")
            if stage not in LIFECYCLE_STAGES:
                add("error", "registry-stage", name, f"stage must be one of: {', '.join(sorted(LIFECYCLE_STAGES))}", registry_path)
            scopes = string_list(item, "scopes", name, nonempty=True)
            invalid_scopes = sorted(scope for scope in scopes if not NAME_RE.fullmatch(scope))
            if invalid_scopes:
                add("error", "registry-scopes-invalid", name, f"invalid scopes: {', '.join(invalid_scopes)}", registry_path)
            if "any" in scopes and len(scopes) > 1:
                add("error", "registry-scopes-any", name, "scope 'any' cannot be combined with narrower scopes", registry_path)

            relations: dict[str, list[str]] = {}
            for field in ("requires", "recommends", "routes_to"):
                relations[field] = string_list(item, field, name)
                unresolved = sorted(set(relations[field]) - registry_name_set)
                if unresolved:
                    add("error", f"registry-{field.replace('_', '-')}-missing", name, f"unresolved {field}: {', '.join(unresolved)}", registry_path)
                if name in relations[field]:
                    add("error", f"registry-self-{field.replace('_', '-')}", name, f"skill references itself in {field}", registry_path)
            overlap = sorted(set(relations["requires"]) & set(relations["recommends"]))
            if overlap:
                add("error", "registry-relation-overlap", name, f"skills cannot be both required and recommended: {', '.join(overlap)}", registry_path)
            relation_graphs["requires"][name] = relations["requires"]
            relation_graphs["routes_to"][name] = relations["routes_to"]
            if kind == "router" and not relations["routes_to"]:
                add("error", "registry-router-empty", name, "router skills must declare at least one routes_to target", registry_path)
            if kind != "router" and relations["routes_to"]:
                add("error", "registry-route-owner", name, "only router skills may declare routes_to targets", registry_path)

            capabilities = string_list(item, "optional_capabilities", name)
            invalid_capabilities = sorted(value for value in capabilities if not NAME_RE.fullmatch(value))
            if invalid_capabilities:
                add("error", "registry-capability-invalid", name, f"invalid optional capabilities: {', '.join(invalid_capabilities)}", registry_path)

            skill_profiles = item.get("resource_profiles", [])
            if "resource_profiles" in item:
                if not isinstance(skill_profiles, list) or any(not isinstance(value, str) or not value for value in skill_profiles):
                    add("error", "registry-skill-resource-profiles", name, "resource_profiles must be an array of profile IDs", registry_path)
                    skill_profiles = []
                unresolved_profiles = sorted(set(skill_profiles) - set(profile_paths))
                if unresolved_profiles:
                    add("error", "registry-skill-resource-profile-missing", name, f"undefined resource profiles: {', '.join(unresolved_profiles)}", registry_path)

            legacy = string_list(item, "legacy_names", name)
            for legacy_name in legacy:
                legacy_owners[legacy_name].append(name)
                if not NAME_RE.fullmatch(legacy_name):
                    add("error", "registry-legacy-name-invalid", name, f"legacy name must be lowercase hyphen-case: {legacy_name}", registry_path)
                if legacy_name in registry_name_set:
                    add("error", "registry-active-legacy", name, f"legacy name is also active: {legacy_name}", registry_path)
        for legacy_name, owners in legacy_owners.items():
            if len(owners) > 1:
                add("error", "registry-legacy-collision", owners[0], f"legacy name '{legacy_name}' maps to: {', '.join(owners)}", registry_path)

        def report_cycles(graph: dict[str, list[str]], code: str, label: str) -> None:
            visiting: set[str] = set()
            visited: set[str] = set()

            def visit(node: str, trail: list[str]) -> None:
                if node in visiting:
                    cycle_start = trail.index(node) if node in trail else 0
                    cycle = trail[cycle_start:] + [node]
                    add("error", code, node, f"{label} cycle: {' -> '.join(cycle)}", registry_path)
                    return
                if node in visited:
                    return
                visiting.add(node)
                for target in graph.get(node, []):
                    if target in graph:
                        visit(target, trail + [node])
                visiting.remove(node)
                visited.add(node)

            for node in sorted(graph):
                visit(node, [])

        report_cycles(relation_graphs["requires"], "registry-requires-cycle", "hard requirement")
        report_cycles(relation_graphs["routes_to"], "registry-route-cycle", "routing")

        bundles = registry.get("bundles")
        bundle_graph: dict[str, list[str]] = {}
        bundle_skills: dict[str, list[str]] = {}
        if not isinstance(bundles, dict) or not bundles:
            add("error", "registry-bundles", "suite", "bundles must be a non-empty object", registry_path)
            bundles = {}
        bundle_names = set(bundles)
        for bundle_name, bundle in bundles.items():
            if not NAME_RE.fullmatch(str(bundle_name)):
                add("error", "registry-bundle-name", "suite", f"invalid bundle name: {bundle_name}", registry_path)
            if not isinstance(bundle, dict):
                add("error", "registry-bundle", str(bundle_name), "bundle definition must be an object", registry_path)
                continue
            missing_bundle_fields = sorted({"description", "includes", "skills"} - set(bundle))
            unknown_bundle_fields = sorted(set(bundle) - {"description", "includes", "skills"})
            if missing_bundle_fields:
                add("error", "registry-bundle-fields", str(bundle_name), f"missing bundle fields: {', '.join(missing_bundle_fields)}", registry_path)
            if unknown_bundle_fields:
                add("error", "registry-bundle-fields", str(bundle_name), f"unsupported bundle fields: {', '.join(unknown_bundle_fields)}", registry_path)
            if not isinstance(bundle.get("description"), str) or not bundle.get("description", "").strip():
                add("error", "registry-bundle-description", str(bundle_name), "bundle description must be a non-empty string", registry_path)
            includes = string_list(bundle, "includes", str(bundle_name))
            selected_skills = string_list(bundle, "skills", str(bundle_name))
            bundle_graph[str(bundle_name)] = includes
            bundle_skills[str(bundle_name)] = selected_skills
            unresolved_bundles = sorted(set(includes) - bundle_names)
            if unresolved_bundles:
                add("error", "registry-bundle-include-missing", str(bundle_name), f"undefined included bundles: {', '.join(unresolved_bundles)}", registry_path)
            unresolved_skills = sorted(set(selected_skills) - registry_name_set)
            if unresolved_skills:
                add("error", "registry-bundle-skill-missing", str(bundle_name), f"undefined bundled skills: {', '.join(unresolved_skills)}", registry_path)
            if bundle_name in includes:
                add("error", "registry-bundle-self-include", str(bundle_name), "bundle includes itself", registry_path)
            if not includes and not selected_skills:
                add("error", "registry-bundle-empty", str(bundle_name), "bundle must include a bundle or skill", registry_path)

        report_cycles(bundle_graph, "registry-bundle-cycle", "bundle inclusion")

        covered_skills: set[str] = set()
        for values in bundle_skills.values():
            covered_skills.update(values)
        uncovered = sorted(registry_name_set - covered_skills)
        if uncovered:
            add("warning", "registry-bundle-uncovered", "suite", f"skills are not directly named by any bundle: {', '.join(uncovered)}", registry_path)

    severity_order = {"error": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda item: (severity_order.get(item["severity"], 9), item["skill"], item["code"]))
    counts = {severity: sum(item["severity"] == severity for item in findings) for severity in ("error", "warning", "info")}
    report = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "skills_root": str(root),
        "registry": str(registry_path) if registry_path.is_file() else None,
        "skill_count": len(records),
        "summary": counts,
        "skills": records,
        "findings": findings,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "skill_count": len(records), **counts}))
    if counts["error"] or (args.fail_on_warning and counts["warning"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
