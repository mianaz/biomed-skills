#!/usr/bin/env python3
"""Perform deterministic cross-artifact checks on an AI-scientist run bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILLS_DIR = SKILL_DIR.parent
REFERENCE_DIR = SKILL_DIR / "references"
BAD_ARTIFACT_STATES = {"empty", "missing", "failed"}
P_VALUE_RE = re.compile(r"(^|[_-])(adjusted[_-]?)?p([_-]?value)?$", re.I)
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


def reject_json_constant(constant: str) -> None:
    raise ValueError(f"non-finite JSON number {constant}")


def load_json(path: Path, label: str, errors: list[str]) -> dict[str, Any]:
    if not path.exists():
        errors.append(f"{label} is missing: {path}")
        return {}
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=reject_json_constant,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"{label} is not readable JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{label} must contain a JSON object")
        return {}
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_path(path: Path) -> str:
    if path.is_file():
        return sha256_file(path)
    digest = hashlib.sha256()
    for child in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(child.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        with child.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def local_locator_state(
    uri: str, locator_kind: str, artifact_root: Path
) -> tuple[Path | None, bool, str]:
    if locator_kind in {"remote", "physical"}:
        return None, bool(uri), f"{locator_kind} locator is recorded"
    if is_external(uri):
        return None, bool(uri), "remote locator is recorded"
    path = Path(uri)
    if not path.is_absolute():
        path = artifact_root / path
    if locator_kind == "collection":
        exists = path.is_dir() or path.is_file()
        nonempty = exists and (
            path.stat().st_size > 0
            if path.is_file()
            else any(path.iterdir())
        )
    else:
        exists = path.is_file()
        nonempty = exists and path.stat().st_size > 0
    return path, nonempty, f"local {locator_kind or 'file'} locator"


def is_external(uri: str) -> bool:
    parsed = urlparse(uri)
    return parsed.scheme not in {"", "file"}


def major(version: object) -> str:
    return str(version or "").split(".", 1)[0]


def item_ids(items: object, field: str) -> set[str]:
    if not isinstance(items, list):
        return set()
    return {
        str(item[field])
        for item in items
        if isinstance(item, dict) and item.get(field) is not None
    }


def duplicate_ids(items: object, field: str) -> list[str]:
    if not isinstance(items, list):
        return []
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        if not isinstance(item, dict) or item.get(field) is None:
            continue
        value = str(item[field])
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def json_equal(left: object, right: object) -> bool:
    return json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(
        right, sort_keys=True, separators=(",", ":")
    )


def json_type_matches(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def resolve_pointer(root: dict[str, Any], pointer: str) -> object:
    if not pointer.startswith("#/"):
        raise ValueError(f"only local schema references are supported: {pointer}")
    value: object = root
    for raw_part in pointer[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or part not in value:
            raise ValueError(f"unresolved schema reference: {pointer}")
        value = value[part]
    return value


def validate_schema(
    value: object,
    schema: object,
    *,
    root: dict[str, Any] | None = None,
    path: str = "$",
) -> list[str]:
    """Validate the JSON Schema features used by this suite, without dependencies."""
    if schema is True:
        return []
    if schema is False:
        return [f"{path}: value is forbidden by schema"]
    if not isinstance(schema, dict):
        return [f"{path}: invalid schema node"]
    if root is None:
        root = schema
    errors: list[str] = []

    if "$ref" in schema:
        try:
            target = resolve_pointer(root, str(schema["$ref"]))
        except ValueError as exc:
            return [f"{path}: {exc}"]
        errors.extend(validate_schema(value, target, root=root, path=path))
        schema = {key: item for key, item in schema.items() if key != "$ref"}

    if "const" in schema and not json_equal(value, schema["const"]):
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and not any(json_equal(value, item) for item in schema["enum"]):
        errors.append(f"{path}: value is not in the allowed enumeration")

    expected_type = schema.get("type")
    if expected_type is not None:
        expected_types = [expected_type] if isinstance(expected_type, str) else expected_type
        if not isinstance(expected_types, list) or not any(
            isinstance(item, str) and json_type_matches(value, item)
            for item in expected_types
        ):
            errors.append(f"{path}: expected type {expected_type!r}")
            return errors

    for subschema in schema.get("allOf", []) or []:
        errors.extend(validate_schema(value, subschema, root=root, path=path))
    if "anyOf" in schema:
        branches = [
            validate_schema(value, subschema, root=root, path=path)
            for subschema in schema.get("anyOf", [])
        ]
        if not any(not branch_errors for branch_errors in branches):
            errors.append(f"{path}: no anyOf branch matched")
    if "oneOf" in schema:
        matched = sum(
            not validate_schema(value, subschema, root=root, path=path)
            for subschema in schema.get("oneOf", [])
        )
        if matched != 1:
            errors.append(f"{path}: expected exactly one matching oneOf branch, observed {matched}")
    if "not" in schema and not validate_schema(value, schema["not"], root=root, path=path):
        errors.append(f"{path}: value matched a forbidden schema")
    if "if" in schema and not validate_schema(value, schema["if"], root=root, path=path):
        if "then" in schema:
            errors.extend(validate_schema(value, schema["then"], root=root, path=path))
    elif "else" in schema:
        errors.extend(validate_schema(value, schema["else"], root=root, path=path))

    if isinstance(value, dict):
        required = schema.get("required", []) or []
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing required property {key!r}")
        properties = schema.get("properties", {}) or {}
        if isinstance(properties, dict):
            for key, subschema in properties.items():
                if key in value:
                    errors.extend(
                        validate_schema(
                            value[key],
                            subschema,
                            root=root,
                            path=f"{path}.{key}",
                        )
                    )
            extras = sorted(set(value) - set(properties))
            additional = schema.get("additionalProperties", True)
            if additional is False:
                for key in extras:
                    errors.append(f"{path}: additional property {key!r} is not allowed")
            elif isinstance(additional, dict):
                for key in extras:
                    errors.extend(
                        validate_schema(
                            value[key],
                            additional,
                            root=root,
                            path=f"{path}.{key}",
                        )
                    )
        if "propertyNames" in schema:
            for key in value:
                errors.extend(
                    validate_schema(
                        key,
                        schema["propertyNames"],
                        root=root,
                        path=f"{path}.<property-name>",
                    )
                )
        minimum_properties = schema.get("minProperties")
        if isinstance(minimum_properties, int) and len(value) < minimum_properties:
            errors.append(f"{path}: fewer than {minimum_properties} properties")
        maximum_properties = schema.get("maxProperties")
        if isinstance(maximum_properties, int) and len(value) > maximum_properties:
            errors.append(f"{path}: more than {maximum_properties} properties")

    if isinstance(value, list):
        minimum_items = schema.get("minItems")
        maximum_items = schema.get("maxItems")
        if isinstance(minimum_items, int) and len(value) < minimum_items:
            errors.append(f"{path}: fewer than {minimum_items} items")
        if isinstance(maximum_items, int) and len(value) > maximum_items:
            errors.append(f"{path}: more than {maximum_items} items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value]
            if len(encoded) != len(set(encoded)):
                errors.append(f"{path}: array items are not unique")
        if "items" in schema:
            for index, item in enumerate(value):
                errors.extend(
                    validate_schema(
                        item,
                        schema["items"],
                        root=root,
                        path=f"{path}[{index}]",
                    )
                )

    if isinstance(value, str):
        minimum_length = schema.get("minLength")
        maximum_length = schema.get("maxLength")
        if isinstance(minimum_length, int) and len(value) < minimum_length:
            errors.append(f"{path}: string is shorter than {minimum_length}")
        if isinstance(maximum_length, int) and len(value) > maximum_length:
            errors.append(f"{path}: string is longer than {maximum_length}")
        if "pattern" in schema:
            try:
                if re.search(str(schema["pattern"]), value) is None:
                    errors.append(f"{path}: string does not match required pattern")
            except re.error as exc:
                errors.append(f"{path}: invalid schema pattern: {exc}")
        if schema.get("format") == "date-time":
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    raise ValueError("timezone is required")
            except ValueError:
                errors.append(f"{path}: invalid date-time")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value is below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value is above maximum {schema['maximum']}")
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errors.append(f"{path}: value must exceed {schema['exclusiveMinimum']}")
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            errors.append(f"{path}: value must be below {schema['exclusiveMaximum']}")

    return errors


def summarized(errors: list[str], limit: int = 12) -> str:
    shown = errors[:limit]
    text = "; ".join(shown)
    if len(errors) > limit:
        text += f"; ... {len(errors) - limit} additional error(s)"
    return text


def safe_id(value: object, fallback: str) -> str:
    return str(value) if isinstance(value, str) and ID_RE.fullmatch(value) else fallback


def declared_extension_ids(contract: dict[str, Any], plural: str, field: str) -> set[str]:
    candidates: list[object] = [contract.get(plural)]
    design = contract.get("design")
    if isinstance(design, dict):
        candidates.append(design.get(plural))
    extensions = contract.get("extensions")
    if isinstance(extensions, dict):
        candidates.append(extensions.get(plural))
        design = extensions.get("design")
        if isinstance(design, dict):
            candidates.append(design.get(plural))
    found: set[str] = set()
    for candidate in candidates:
        found.update(item_ids(candidate, field))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, help="Directory containing the run bundle")
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--root", type=Path, help="Project root for relative input and artifact paths")
    parser.add_argument("--fail-on-warning", action="store_true")
    parser.add_argument("--verifier-metadata", type=Path, help="JSON object describing the verifier")
    parser.add_argument("--verifier-id")
    parser.add_argument("--verifier-kind", choices=["agent", "script", "human", "hybrid"])
    independence = parser.add_mutually_exclusive_group()
    independence.add_argument(
        "--independent-of-executor",
        action="store_true",
        dest="independent_of_executor",
        help="Explicitly assert that verifier and executor are independent",
    )
    independence.add_argument(
        "--not-independent-of-executor",
        action="store_false",
        dest="independent_of_executor",
        help="Explicitly record that verifier and executor are not independent",
    )
    parser.set_defaults(independent_of_executor=None)
    parser.add_argument("--context-isolated", action="store_true")
    parser.add_argument(
        "--rerun-record",
        type=Path,
        help="JSON rerun comparison record for numeric-tolerance verification",
    )
    parser.add_argument(
        "--domain-profile",
        action="append",
        default=[],
        help="Registered profile ID or path to a domain check profile; repeatable",
    )
    args = parser.parse_args()

    bundle = (args.bundle or Path(".ai-scientist/current")).resolve()
    contract_path = (args.contract or bundle / "analysis-contract.json").resolve()
    manifest_path = (args.manifest or bundle / "run-manifest.json").resolve()
    evidence_path = (args.evidence or bundle / "evidence-index.json").resolve()
    output_path = (args.output or bundle / "verification-report.json").resolve()
    artifact_root = (args.root or Path.cwd()).resolve()

    load_errors: list[str] = []
    contract = load_json(contract_path, "analysis contract", load_errors)
    manifest = load_json(manifest_path, "run manifest", load_errors)
    evidence = load_json(evidence_path, "evidence index", load_errors)
    checks: list[dict[str, Any]] = []
    used_check_ids: set[str] = set()

    def add(
        check_id: str,
        category: str,
        status: str,
        message: str,
        *,
        severity: str = "error",
        method: str = "deterministic",
        targets: list[dict[str, str]] | None = None,
        remediation: str | None = None,
        contract_check_id: str | None = None,
        supporting_refs: list[str] | None = None,
    ) -> dict[str, Any]:
        base = check_id
        number = 2
        while check_id in used_check_ids:
            check_id = f"{base}-{number}"
            number += 1
        used_check_ids.add(check_id)
        item: dict[str, Any] = {
            "check_id": check_id,
            "category": category,
            "method": method,
            "severity": severity,
            "status": status,
            "targets": targets or [],
            "message": message,
            "supporting_refs": supporting_refs or [],
        }
        if remediation:
            item["remediation"] = remediation
        if contract_check_id:
            item["contract_check_id"] = contract_check_id
        checks.append(item)
        return item

    for number, message in enumerate(load_errors, 1):
        add(
            f"bundle-load-{number}",
            "schema",
            "fail",
            message,
            remediation="Restore a valid JSON artifact at the recorded path.",
        )

    schema_paths = {
        "contract": SKILLS_DIR
        / "plan-biomedical-analysis"
        / "references"
        / "analysis-contract.schema.json",
        "manifest": SKILLS_DIR
        / "ensure-biomedical-reproducibility"
        / "references"
        / "run-manifest.schema.json",
        "evidence": REFERENCE_DIR / "evidence-index.schema.json",
        "report": REFERENCE_DIR / "verification-report.schema.json",
        "domain_profile": REFERENCE_DIR / "domain-check-profile.schema.json",
        "rerun": REFERENCE_DIR / "rerun-record.schema.json",
    }
    schemas: dict[str, dict[str, Any]] = {}
    for label, path in schema_paths.items():
        schema_load_errors: list[str] = []
        schemas[label] = load_json(path, f"{label} schema", schema_load_errors)
        for number, message in enumerate(schema_load_errors, 1):
            add(f"schema-definition-{label}-{number}", "schema", "fail", message)

    for label, document in (
        ("contract", contract),
        ("manifest", manifest),
        ("evidence", evidence),
    ):
        errors = validate_schema(document, schemas.get(label, {}))
        add(
            f"schema-{label}",
            "schema",
            "pass" if not errors else "fail",
            f"{label} conforms to its complete structural schema"
            if not errors
            else summarized(errors),
            remediation="Correct every reported schema violation before interpreting the run."
            if errors
            else None,
        )

    contract_id = contract.get("contract_id")
    run_id = manifest.get("run_id")
    ids_match = (
        bool(contract_id)
        and manifest.get("contract_id") == contract_id
        and evidence.get("contract_id") == contract_id
    )
    run_ids_match = bool(run_id) and evidence.get("run_id") == run_id
    versions = {major(doc.get("schema_version")) for doc in (contract, manifest, evidence) if doc}
    add(
        "identity-contract",
        "schema",
        "pass" if ids_match else "fail",
        "Contract IDs agree" if ids_match else "Contract IDs do not agree across artifacts",
    )
    add(
        "identity-run",
        "schema",
        "pass" if run_ids_match else "fail",
        "Run IDs agree" if run_ids_match else "Run IDs do not agree across run artifacts",
    )
    add(
        "identity-schema-major",
        "schema",
        "pass" if len(versions) <= 1 else "fail",
        "Schema major versions agree"
        if len(versions) <= 1
        else f"Schema major versions differ: {sorted(versions)}",
    )

    contract_inputs = contract.get("inputs", []) if isinstance(contract.get("inputs"), list) else []
    questions_list = contract.get("questions", []) if isinstance(contract.get("questions"), list) else []
    contract_steps_list = contract.get("steps", []) if isinstance(contract.get("steps"), list) else []
    contract_outputs = (
        contract.get("required_outputs", [])
        if isinstance(contract.get("required_outputs"), list)
        else []
    )
    validations = contract.get("validation", []) if isinstance(contract.get("validation"), list) else []
    design = contract.get("design") if isinstance(contract.get("design"), dict) else {}
    units_list = design.get("units", []) if isinstance(design.get("units"), list) else []
    outcomes_list = (
        design.get("outcomes", []) if isinstance(design.get("outcomes"), list) else []
    )
    analysis_sets_list = (
        design.get("analysis_sets", [])
        if isinstance(design.get("analysis_sets"), list)
        else []
    )
    factors_list = design.get("factors", []) if isinstance(design.get("factors"), list) else []
    contrasts_list = design.get("contrasts", []) if isinstance(design.get("contrasts"), list) else []

    manifest_inputs = manifest.get("inputs", []) if isinstance(manifest.get("inputs"), list) else []
    executions = manifest.get("steps", []) if isinstance(manifest.get("steps"), list) else []
    artifacts = manifest.get("artifacts", []) if isinstance(manifest.get("artifacts"), list) else []
    external_source_list = (
        manifest.get("external_sources", [])
        if isinstance(manifest.get("external_sources"), list)
        else []
    )
    resources = (
        manifest.get("resources", [])
        if isinstance(manifest.get("resources"), list)
        else []
    )
    deviations = manifest.get("deviations", []) if isinstance(manifest.get("deviations"), list) else []
    quality = manifest.get("quality", {}) if isinstance(manifest.get("quality"), dict) else {}
    quality_checks = quality.get("checks", []) if isinstance(quality.get("checks"), list) else []

    claims = evidence.get("claims", []) if isinstance(evidence.get("claims"), list) else []
    evidence_items = (
        evidence.get("evidence_items", [])
        if isinstance(evidence.get("evidence_items"), list)
        else []
    )

    identifier_collections = [
        ("contract questions", questions_list, "question_id"),
        ("contract inputs", contract_inputs, "input_id"),
        ("contract steps", contract_steps_list, "step_id"),
        ("contract outputs", contract_outputs, "output_id"),
        ("contract validations", validations, "check_id"),
        ("design units", units_list, "unit_id"),
        ("design outcomes", outcomes_list, "outcome_id"),
        ("design analysis sets", analysis_sets_list, "analysis_set_id"),
        ("design factors", factors_list, "factor_id"),
        ("design contrasts", contrasts_list, "contrast_id"),
        ("manifest inputs", manifest_inputs, "input_id"),
        ("manifest sources", external_source_list, "source_id"),
        ("manifest resources", resources, "resource_id"),
        ("manifest executions", executions, "execution_id"),
        ("manifest artifacts", artifacts, "artifact_id"),
        ("manifest deviations", deviations, "deviation_id"),
        ("manifest quality checks", quality_checks, "check_id"),
        ("evidence claims", claims, "claim_id"),
        ("evidence items", evidence_items, "evidence_id"),
    ]
    duplicate_messages = [
        f"{label}: {', '.join(duplicates)}"
        for label, items, field in identifier_collections
        if (duplicates := duplicate_ids(items, field))
    ]
    contract_quality_duplicates = duplicate_ids(
        [
            {"contract_check_id": item.get("contract_check_id")}
            for item in quality_checks
            if isinstance(item, dict) and item.get("contract_check_id")
        ],
        "contract_check_id",
    )
    if contract_quality_duplicates:
        duplicate_messages.append(
            "manifest contract-check mappings: " + ", ".join(contract_quality_duplicates)
        )
    add(
        "identifier-uniqueness",
        "schema",
        "pass" if not duplicate_messages else "fail",
        "All semantic identifiers are unique"
        if not duplicate_messages
        else "; ".join(duplicate_messages),
        remediation="Assign one unique identifier to each semantic object."
        if duplicate_messages
        else None,
    )

    unit_ids = item_ids(units_list, "unit_id")
    design_reference_errors: list[str] = []
    for unit in units_list:
        if (
            isinstance(unit, dict)
            and unit.get("parent_unit_id")
            and str(unit["parent_unit_id"]) not in unit_ids
        ):
            design_reference_errors.append(
                f"unit {unit.get('unit_id')} has unknown parent {unit.get('parent_unit_id')}"
            )
    for outcome in outcomes_list:
        if (
            isinstance(outcome, dict)
            and outcome.get("unit_id")
            and str(outcome["unit_id"]) not in unit_ids
        ):
            design_reference_errors.append(
                f"outcome {outcome.get('outcome_id')} has unknown unit {outcome.get('unit_id')}"
            )
    for analysis_set in analysis_sets_list:
        if (
            isinstance(analysis_set, dict)
            and analysis_set.get("unit_id")
            and str(analysis_set["unit_id"]) not in unit_ids
        ):
            design_reference_errors.append(
                "analysis set "
                f"{analysis_set.get('analysis_set_id')} has unknown unit "
                f"{analysis_set.get('unit_id')}"
            )
    add(
        "design-unit-refs",
        "design",
        "pass" if not design_reference_errors else "fail",
        "All outcomes, analysis sets, and nested units resolve"
        if not design_reference_errors
        else summarized(design_reference_errors),
    )

    contract_input_ids = item_ids(contract_inputs, "input_id")
    required_inputs = {
        str(item.get("input_id"))
        for item in contract_inputs
        if isinstance(item, dict)
        and item.get("required", True)
        and item.get("input_id")
    }
    supplied_inputs = {
        str(item.get("contract_input_id"))
        for item in manifest_inputs
        if isinstance(item, dict) and item.get("contract_input_id")
    }
    missing_inputs = sorted(required_inputs - supplied_inputs)
    unknown_input_refs = sorted(supplied_inputs - contract_input_ids)
    add(
        "contract-required-inputs",
        "input",
        "pass" if not missing_inputs else "fail",
        "All required contract inputs are represented"
        if not missing_inputs
        else f"Required inputs absent from manifest: {', '.join(missing_inputs)}",
    )
    add(
        "manifest-input-contract-refs",
        "input",
        "pass" if not unknown_input_refs else "fail",
        "All manifest inputs resolve to contract inputs"
        if not unknown_input_refs
        else f"Manifest inputs reference unknown contract inputs: {', '.join(unknown_input_refs)}",
    )
    for index, item in enumerate(manifest_inputs, 1):
        if not isinstance(item, dict):
            continue
        input_id = str(item.get("input_id", f"unknown-{index}"))
        uri = str(item.get("uri", ""))
        locator_kind = str(item.get("locator_kind", "file"))
        if not uri:
            add(
                f"input-file-{input_id}",
                "input",
                "warn",
                f"Input {input_id} has no locator",
                severity="warning",
                targets=[{"type": "input", "id": safe_id(input_id, "unknown-input")}],
            )
            continue
        path, nonempty, locator_description = local_locator_state(
            uri, locator_kind, artifact_root
        )
        add(
            f"input-file-{input_id}",
            "input",
            "pass" if nonempty else "fail",
            f"Input {input_id} {locator_description}"
            if nonempty
            else f"Input {input_id} is missing or empty at {path}",
            targets=[{"type": "input", "id": safe_id(input_id, "unknown-input")}],
        )
        expected_hash = item.get("sha256")
        if nonempty and expected_hash and path is not None:
            matches = sha256_path(path) == expected_hash
            add(
                f"input-hash-{input_id}",
                "reproducibility",
                "pass" if matches else "fail",
                f"Input {input_id} SHA-256 matches"
                if matches
                else f"Input {input_id} SHA-256 mismatch",
                targets=[{"type": "input", "id": safe_id(input_id, "unknown-input")}],
            )

    contract_step_ids = item_ids(contract_steps_list, "step_id")
    represented_step_ids = item_ids(executions, "step_id")
    execution_ids = item_ids(executions, "execution_id")
    deviation_step_ids = {
        str(item.get("target_id"))
        for item in deviations
        if isinstance(item, dict)
        and item.get("target_type") == "step"
        and item.get("target_id")
    }
    unplanned = sorted(
        represented_step_ids - contract_step_ids - deviation_step_ids
    )
    missing_planned_steps = sorted(contract_step_ids - represented_step_ids)
    add(
        "contract-step-resolution",
        "design",
        "pass" if not unplanned else "fail",
        "All executions resolve to planned steps or deviations"
        if not unplanned
        else f"Unplanned steps without deviations: {', '.join(unplanned)}",
    )
    add(
        "contract-step-coverage",
        "design",
        "pass" if not missing_planned_steps else "fail",
        "Every planned step has an execution record"
        if not missing_planned_steps
        else f"Planned steps absent from the manifest: {', '.join(missing_planned_steps)}",
        remediation="Record a completed, failed, or skipped execution for every planned step."
        if missing_planned_steps
        else None,
    )

    artifact_by_id = {
        str(item.get("artifact_id")): item
        for item in artifacts
        if isinstance(item, dict) and item.get("artifact_id")
    }
    manifest_input_ids = item_ids(manifest_inputs, "input_id")
    resource_ids = item_ids(resources, "resource_id")
    dangling_step_artifacts: list[str] = []
    dangling_step_inputs: list[str] = []
    dangling_step_resources: list[str] = []
    for execution in executions:
        if not isinstance(execution, dict):
            continue
        for artifact_id in execution.get("artifact_ids", []) or []:
            if str(artifact_id) not in artifact_by_id:
                dangling_step_artifacts.append(f"{execution.get('execution_id')}->{artifact_id}")
        for artifact_id in execution.get("upstream_artifact_ids", []) or []:
            if str(artifact_id) not in artifact_by_id:
                dangling_step_artifacts.append(
                    f"{execution.get('execution_id')} upstream->{artifact_id}"
                )
        for input_id in execution.get("input_ids", []) or []:
            if str(input_id) not in manifest_input_ids:
                dangling_step_inputs.append(
                    f"{execution.get('execution_id')}->{input_id}"
                )
        for resource_id in execution.get("resource_ids", []) or []:
            if str(resource_id) not in resource_ids:
                dangling_step_resources.append(
                    f"{execution.get('execution_id')}->{resource_id}"
                )
    add(
        "manifest-step-artifacts",
        "artifact",
        "pass" if not dangling_step_artifacts else "fail",
        "All step artifact references resolve"
        if not dangling_step_artifacts
        else f"Unresolved step artifacts: {', '.join(dangling_step_artifacts)}",
    )
    add(
        "manifest-step-inputs",
        "input",
        "pass" if not dangling_step_inputs else "fail",
        "All step input references resolve"
        if not dangling_step_inputs
        else f"Unresolved step inputs: {', '.join(dangling_step_inputs)}",
    )
    add(
        "manifest-step-resources",
        "reproducibility",
        "pass" if not dangling_step_resources else "fail",
        "All step resource references resolve"
        if not dangling_step_resources
        else f"Unresolved step resources: {', '.join(dangling_step_resources)}",
    )

    required_output_ids = item_ids(contract_outputs, "output_id")
    produced_output_ids = {
        str(item.get("output_id"))
        for item in artifacts
        if isinstance(item, dict) and item.get("output_id")
    }
    missing_outputs = sorted(required_output_ids - produced_output_ids)
    unknown_output_refs = sorted(produced_output_ids - required_output_ids)
    add(
        "contract-required-outputs",
        "artifact",
        "pass" if not missing_outputs else "fail",
        "All required outputs have manifest records"
        if not missing_outputs
        else f"Required outputs absent from manifest: {', '.join(missing_outputs)}",
    )
    add(
        "manifest-output-contract-refs",
        "artifact",
        "pass" if not unknown_output_refs else "fail",
        "All output-linked artifacts resolve to contract outputs"
        if not unknown_output_refs
        else f"Artifacts reference unknown output IDs: {', '.join(unknown_output_refs)}",
    )

    bad_artifact_ids: set[str] = set()
    for artifact_id, artifact in artifact_by_id.items():
        status = str(artifact.get("status", "missing"))
        uri = str(artifact.get("uri", ""))
        locator_kind = str(artifact.get("locator_kind", "file"))
        if status in BAD_ARTIFACT_STATES:
            bad_artifact_ids.add(artifact_id)
            add(
                f"artifact-state-{artifact_id}",
                "artifact",
                "fail",
                f"Artifact {artifact_id} is marked {status}",
                targets=[{"type": "artifact", "id": safe_id(artifact_id, "unknown-artifact")}],
            )
            continue
        if not uri:
            add(
                f"artifact-file-{artifact_id}",
                "artifact",
                "warn",
                f"Artifact {artifact_id} has no locator",
                severity="warning",
                targets=[{"type": "artifact", "id": safe_id(artifact_id, "unknown-artifact")}],
            )
            continue
        path, nonempty, locator_description = local_locator_state(
            uri, locator_kind, artifact_root
        )
        if not nonempty:
            bad_artifact_ids.add(artifact_id)
        add(
            f"artifact-file-{artifact_id}",
            "artifact",
            "pass" if nonempty else "fail",
            f"Artifact {artifact_id} {locator_description}"
            if nonempty
            else f"Artifact {artifact_id} is missing or empty at {path}",
            targets=[{"type": "artifact", "id": safe_id(artifact_id, "unknown-artifact")}],
        )
        expected_hash = artifact.get("sha256")
        if nonempty and expected_hash and path is not None:
            matches = sha256_path(path) == expected_hash
            if not matches:
                bad_artifact_ids.add(artifact_id)
            add(
                f"artifact-hash-{artifact_id}",
                "reproducibility",
                "pass" if matches else "fail",
                f"Artifact {artifact_id} SHA-256 matches"
                if matches
                else f"Artifact {artifact_id} SHA-256 mismatch",
                targets=[{"type": "artifact", "id": safe_id(artifact_id, "unknown-artifact")}],
            )

    source_ids = item_ids(external_source_list, "source_id")
    cache_ref_errors: list[str] = []
    for source in external_source_list:
        if not isinstance(source, dict) or not source.get("cache_artifact_id"):
            continue
        source_id = str(source.get("source_id", "unknown"))
        cache_id = str(source["cache_artifact_id"])
        if cache_id not in artifact_by_id:
            cache_ref_errors.append(f"{source_id}->{cache_id} is unresolved")
    add(
        "manifest-source-cache-refs",
        "reproducibility",
        "pass" if not cache_ref_errors else "fail",
        "All source cache references resolve"
        if not cache_ref_errors
        else "; ".join(cache_ref_errors),
    )

    deviation_targets = {
        "input": manifest_input_ids | contract_input_ids,
        "source": source_ids,
        "resource": resource_ids,
        "step": contract_step_ids | represented_step_ids,
        "artifact": set(artifact_by_id),
        "output": required_output_ids,
    }
    deviation_ref_errors: list[str] = []
    for deviation in deviations:
        if not isinstance(deviation, dict):
            continue
        target_type = str(deviation.get("target_type", ""))
        target_id = str(deviation.get("target_id", ""))
        if target_type in deviation_targets and target_id not in deviation_targets[target_type]:
            deviation_ref_errors.append(
                f"{deviation.get('deviation_id')}: unknown {target_type} {target_id}"
            )
    add(
        "manifest-deviation-refs",
        "schema",
        "pass" if not deviation_ref_errors else "fail",
        "All typed deviation targets resolve"
        if not deviation_ref_errors
        else summarized(deviation_ref_errors),
    )

    contract_question_ids = item_ids(questions_list, "question_id")
    claimed_question_ids = item_ids(claims, "question_id")
    missing_questions = sorted(contract_question_ids - claimed_question_ids)
    unknown_questions = sorted(claimed_question_ids - contract_question_ids)
    add(
        "contract-question-coverage",
        "evidence",
        "pass" if not missing_questions else "fail",
        "Every planned question has a recorded claim verdict"
        if not missing_questions
        else f"Planned questions without claims: {', '.join(missing_questions)}",
        remediation="Record a bounded verdict, including inconclusive or technical failure, for each question."
        if missing_questions
        else None,
    )
    add(
        "evidence-question-refs",
        "evidence",
        "pass" if not unknown_questions else "fail",
        "All claim question references resolve"
        if not unknown_questions
        else f"Claims reference unknown questions: {', '.join(unknown_questions)}",
    )

    contrast_ids = item_ids(contrasts_list, "contrast_id")
    outcome_ids = declared_extension_ids(contract, "outcomes", "outcome_id")
    analysis_set_ids = declared_extension_ids(contract, "analysis_sets", "analysis_set_id")
    evidence_by_id = {
        str(item.get("evidence_id")): item
        for item in evidence_items
        if isinstance(item, dict) and item.get("evidence_id")
    }
    used_evidence: set[str] = set()
    evidence_errors: list[str] = []
    for claim in claims:
        if not isinstance(claim, dict):
            evidence_errors.append("non-object claim")
            continue
        claim_id = str(claim.get("claim_id", "unknown"))
        claim_evidence = [str(item) for item in claim.get("evidence_ids", []) or []]
        if not claim_evidence:
            evidence_errors.append(f"{claim_id}: no evidence")
        for evidence_id in claim_evidence:
            used_evidence.add(evidence_id)
            if evidence_id not in evidence_by_id:
                evidence_errors.append(f"{claim_id}: unknown evidence {evidence_id}")
        if claim.get("verdict") == "supported":
            for evidence_id in claim_evidence:
                item = evidence_by_id.get(evidence_id, {})
                source = item.get("source", {}) if isinstance(item, dict) else {}
                if source.get("type") == "artifact" and str(source.get("id")) in bad_artifact_ids:
                    evidence_errors.append(
                        f"{claim_id}: supported by bad artifact {source.get('id')}"
                    )

    for evidence_id, item in evidence_by_id.items():
        source = item.get("source", {}) if isinstance(item.get("source"), dict) else {}
        source_id = str(source.get("id", ""))
        if source.get("type") == "artifact" and source_id not in artifact_by_id:
            evidence_errors.append(f"{evidence_id}: unknown artifact source {source_id}")
        if source.get("type") == "external_source" and source_id not in source_ids:
            evidence_errors.append(f"{evidence_id}: unknown external source {source_id}")
        if source.get("type") == "resource" and source_id not in resource_ids:
            evidence_errors.append(f"{evidence_id}: unknown resource source {source_id}")
        if item.get("execution_id") and str(item.get("execution_id")) not in execution_ids:
            evidence_errors.append(
                f"{evidence_id}: unknown execution {item.get('execution_id')}"
            )
        context = item.get("data_context", {}) if isinstance(item.get("data_context"), dict) else {}
        if context.get("contrast_id") and str(context.get("contrast_id")) not in contrast_ids:
            evidence_errors.append(
                f"{evidence_id}: unknown contrast {context.get('contrast_id')}"
            )
        if outcome_ids and context.get("outcome_id") and str(context.get("outcome_id")) not in outcome_ids:
            evidence_errors.append(
                f"{evidence_id}: unknown outcome {context.get('outcome_id')}"
            )
        if (
            analysis_set_ids
            and context.get("analysis_set_id")
            and str(context.get("analysis_set_id")) not in analysis_set_ids
        ):
            evidence_errors.append(
                f"{evidence_id}: unknown analysis set {context.get('analysis_set_id')}"
            )
        if (
            context.get("unit_set_artifact_id")
            and str(context.get("unit_set_artifact_id")) not in artifact_by_id
        ):
            evidence_errors.append(
                f"{evidence_id}: unknown unit-set artifact {context.get('unit_set_artifact_id')}"
            )
        for statistic in item.get("statistics", []) or []:
            if not isinstance(statistic, dict):
                continue
            name = str(statistic.get("name", ""))
            value = statistic.get("value")
            if P_VALUE_RE.search(name) and (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not 0 <= value <= 1
            ):
                evidence_errors.append(f"{evidence_id}: {name} outside [0,1]")
            for field in ("p_value", "adjusted_p_value"):
                if field in statistic:
                    probability = statistic[field]
                    if (
                        not isinstance(probability, (int, float))
                        or isinstance(probability, bool)
                        or not 0 <= probability <= 1
                    ):
                        evidence_errors.append(f"{evidence_id}: {field} outside [0,1]")
            interval = statistic.get("interval")
            if isinstance(interval, dict):
                lower = interval.get("lower")
                upper = interval.get("upper")
                level = interval.get("level")
                if (
                    not isinstance(lower, (int, float))
                    or isinstance(lower, bool)
                    or not isinstance(upper, (int, float))
                    or isinstance(upper, bool)
                    or lower > upper
                ):
                    evidence_errors.append(f"{evidence_id}: invalid interval bounds")
                if (
                    not isinstance(level, (int, float))
                    or isinstance(level, bool)
                    or not 0 < level < 1
                ):
                    evidence_errors.append(f"{evidence_id}: interval level outside (0,1)")
            if "n" in statistic and (
                not isinstance(statistic["n"], int)
                or isinstance(statistic["n"], bool)
                or statistic["n"] < 0
            ):
                evidence_errors.append(f"{evidence_id}: invalid n")
            has_basis = "count_basis" in statistic
            has_denominator = "denominator" in statistic
            if has_basis != has_denominator:
                evidence_errors.append(
                    f"{evidence_id}: count_basis and denominator must be recorded together"
                )
    unused = sorted(set(evidence_by_id) - used_evidence)
    if unused:
        evidence_errors.append(f"unused evidence items: {', '.join(unused)}")
    add(
        "evidence-resolution",
        "evidence",
        "pass" if not evidence_errors else "fail",
        "All claims, contexts, statistics, and evidence references resolve"
        if not evidence_errors
        else summarized(evidence_errors),
    )

    validation_ids = item_ids(validations, "check_id")
    quality_ref_errors: list[str] = []
    quality_by_contract: dict[str, dict[str, Any]] = {}
    quality_by_id: dict[str, dict[str, Any]] = {}
    for item in quality_checks:
        if not isinstance(item, dict):
            continue
        quality_id = str(item.get("check_id", ""))
        if quality_id:
            quality_by_id[quality_id] = item
        contract_check_id = item.get("contract_check_id")
        if contract_check_id:
            key = str(contract_check_id)
            quality_by_contract[key] = item
            if key not in validation_ids:
                quality_ref_errors.append(
                    f"{quality_id}: unknown contract_check_id {contract_check_id}"
                )
        elif quality_id in validation_ids:
            quality_by_contract[quality_id] = item
        for artifact_id in item.get("artifact_ids", []) or []:
            if str(artifact_id) not in artifact_by_id:
                quality_ref_errors.append(
                    f"{quality_id}: unknown artifact {artifact_id}"
                )
    add(
        "manifest-quality-refs",
        "schema",
        "pass" if not quality_ref_errors else "fail",
        "All quality-check references resolve"
        if not quality_ref_errors
        else summarized(quality_ref_errors),
    )

    def status_for_severity(raw_status: str, severity: str) -> str:
        normalized = {"warning": "warn", "error": "fail"}.get(raw_status, raw_status)
        if normalized in {"pass", "not_applicable"}:
            return normalized
        if normalized not in {"warn", "fail"}:
            normalized = "warn"
        return "fail" if severity == "error" else "warn"

    for item in validations:
        if not isinstance(item, dict) or not item.get("check_id"):
            continue
        check_id = str(item["check_id"])
        severity = str(item.get("severity", "error"))
        recorded = quality_by_contract.get(check_id)
        criterion = str(item.get("criterion", ""))
        if recorded:
            add(
                f"planned-{check_id}",
                str(recorded.get("category", "other")),
                status_for_severity(str(recorded.get("status", "warn")), severity),
                str(recorded.get("summary") or f"Recorded validation result for {check_id}"),
                severity=severity,
                method="review",
                contract_check_id=check_id,
                targets=[{"type": "contract_check", "id": safe_id(check_id, "unknown-check")}],
            )
            continue
        normalized_criterion = criterion.lower().replace("‑", "-")
        output_presence_check = "exist" in normalized_criterion and (
            "non-empty" in normalized_criterion or "nonempty" in normalized_criterion
        )
        if output_presence_check:
            bad_required_output = any(
                str(artifact.get("output_id")) in required_output_ids
                and artifact_id in bad_artifact_ids
                for artifact_id, artifact in artifact_by_id.items()
            )
            passing = not missing_outputs and not bad_required_output
            add(
                f"planned-{check_id}",
                "artifact",
                "pass" if passing else ("fail" if severity == "error" else "warn"),
                f"Deterministic output-presence check: {criterion}",
                severity=severity,
                remediation=None
                if passing
                else "Produce every required output as a nonempty artifact.",
                contract_check_id=check_id,
                targets=[{"type": "contract_check", "id": safe_id(check_id, "unknown-check")}],
            )
            continue
        add(
            f"planned-{check_id}",
            "other",
            "fail" if severity == "error" else "warn",
            f"Planned validation '{check_id}' has no recorded result: {criterion}",
            severity=severity,
            method="review",
            remediation="Execute the specified validation and record its result with contract_check_id.",
            contract_check_id=check_id,
            targets=[{"type": "contract_check", "id": safe_id(check_id, "unknown-check")}],
        )

    registry_errors: list[str] = []
    registry = load_json(
        REFERENCE_DIR / "domain-check-profiles.json",
        "domain profile registry",
        registry_errors,
    )
    for number, message in enumerate(registry_errors, 1):
        add(f"domain-registry-{number}", "schema", "fail", message)
    registered_profiles: dict[str, Path] = {
        str(item.get("profile_id")): (REFERENCE_DIR / str(item.get("path"))).resolve()
        for item in registry.get("profiles", [])
        if isinstance(item, dict) and item.get("profile_id") and item.get("path")
    }
    suite_registry_path = SKILLS_DIR.parent / "suite.json"
    if suite_registry_path.is_file():
        suite_registry_errors: list[str] = []
        suite_registry = load_json(
            suite_registry_path, "suite registry", suite_registry_errors
        )
        for number, message in enumerate(suite_registry_errors, 1):
            add(f"suite-registry-{number}", "schema", "fail", message)
        suite_profiles = suite_registry.get("resource_profiles", {})
        if isinstance(suite_profiles, dict):
            for profile_id, relative_path in suite_profiles.items():
                if isinstance(relative_path, str) and relative_path:
                    registered_profiles[str(profile_id)] = (
                        suite_registry_path.parent / relative_path
                    ).resolve()
    extension_key_profiles: dict[str, Path] = {}
    for profile_path in registered_profiles.values():
        if not profile_path.is_file():
            continue
        try:
            profile_header = json.loads(profile_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        contract_extension = (
            profile_header.get("contract_extension")
            if isinstance(profile_header, dict)
            and isinstance(profile_header.get("contract_extension"), dict)
            else {}
        )
        extension_key = contract_extension.get("key")
        if isinstance(extension_key, str) and extension_key:
            extension_key_profiles[extension_key] = profile_path
    requested_profiles = list(args.domain_profile)
    extensions = contract.get("extensions")
    profile_payloads: dict[str, Any] = {}
    if isinstance(extensions, dict):
        configured_profiles = extensions.get("profiles")
        if isinstance(configured_profiles, dict):
            profile_payloads = configured_profiles
            requested_profiles.extend(str(item) for item in configured_profiles)
        verification_extension = extensions.get("verification")
        if isinstance(verification_extension, dict):
            configured = verification_extension.get("domain_profiles", [])
            if isinstance(configured, list):
                requested_profiles.extend(str(item) for item in configured)
    requested_profiles = list(dict.fromkeys(requested_profiles))
    loaded_profile_ids: list[str] = []
    loaded_categories: list[str] = []
    for requested in requested_profiles:
        candidate = Path(requested)
        if candidate.exists():
            profile_path = candidate.resolve()
        elif requested in registered_profiles:
            profile_path = registered_profiles[requested]
        elif requested in extension_key_profiles:
            profile_path = extension_key_profiles[requested]
        else:
            add(
                f"domain-profile-{safe_id(requested, 'unknown')}",
                "schema",
                "fail",
                f"Domain profile is neither registered nor a readable path: {requested}",
            )
            continue
        profile_load_errors: list[str] = []
        profile = load_json(profile_path, f"domain profile {requested}", profile_load_errors)
        profile_schema_errors = validate_schema(profile, schemas.get("domain_profile", {}))
        combined_errors = profile_load_errors + profile_schema_errors
        profile_id = safe_id(profile.get("profile_id"), safe_id(requested, "unknown-profile"))
        add(
            f"schema-domain-profile-{profile_id}",
            "schema",
            "pass" if not combined_errors else "fail",
            f"Domain profile {profile_id} conforms to its schema"
            if not combined_errors
            else summarized(combined_errors),
        )
        if combined_errors:
            continue
        explicit_category_ids = item_ids(profile.get("categories", []), "category_id")
        check_duplicates = duplicate_ids(profile.get("checks", []), "check_id")
        category_duplicates = duplicate_ids(profile.get("categories", []), "category_id")
        verification_metadata = (
            profile.get("verification")
            if isinstance(profile.get("verification"), dict)
            else {}
        )
        required_category_ids = {
            str(item)
            for item in verification_metadata.get("required_categories", [])
            if isinstance(item, str)
        }
        category_ids = explicit_category_ids or required_category_ids
        unknown_categories = sorted(
            {
                str(item.get("category"))
                for item in profile.get("checks", [])
                if isinstance(item, dict) and item.get("category")
            }
            - category_ids
        )
        semantic_errors: list[str] = []
        if check_duplicates:
            semantic_errors.append("duplicate checks: " + ", ".join(check_duplicates))
        if category_duplicates:
            semantic_errors.append("duplicate categories: " + ", ".join(category_duplicates))
        if unknown_categories:
            semantic_errors.append(
                "checks use undeclared categories: " + ", ".join(unknown_categories)
            )
        missing_required_categories = sorted(required_category_ids - category_ids)
        if missing_required_categories:
            semantic_errors.append(
                "required categories are undeclared: "
                + ", ".join(missing_required_categories)
            )
        reference_fields = {
            "contract extension schema": (
                profile.get("contract_extension", {}).get("schema")
                if isinstance(profile.get("contract_extension"), dict)
                else None
            ),
            "verification catalog": verification_metadata.get("catalog"),
        }
        resolved_profile_references: dict[str, Path] = {}
        for label, relative_reference in reference_fields.items():
            if not isinstance(relative_reference, str) or not relative_reference:
                semantic_errors.append(f"{label} is not declared")
                continue
            reference_path = Path(relative_reference)
            if reference_path.is_absolute():
                semantic_errors.append(f"{label} must use a relative path")
                continue
            resolved = (profile_path.parent / reference_path).resolve()
            if not resolved.is_file():
                semantic_errors.append(f"{label} is missing at {resolved}")
                continue
            resolved_profile_references[label] = resolved
        contract_extension = (
            profile.get("contract_extension")
            if isinstance(profile.get("contract_extension"), dict)
            else {}
        )
        extension_key = str(contract_extension.get("key", ""))
        if extension_key in profile_payloads and "contract extension schema" in resolved_profile_references:
            extension_schema_errors: list[str] = []
            extension_schema = load_json(
                resolved_profile_references["contract extension schema"],
                f"{profile_id} contract extension schema",
                extension_schema_errors,
            )
            extension_schema_errors.extend(
                validate_schema(profile_payloads[extension_key], extension_schema)
            )
            if extension_schema_errors:
                semantic_errors.append(
                    "contract extension is invalid: "
                    + summarized(extension_schema_errors)
                )
        add(
            f"domain-profile-integrity-{profile_id}",
            "schema",
            "pass" if not semantic_errors else "fail",
            f"Domain profile {profile_id} identifiers and categories resolve"
            if not semantic_errors
            else "; ".join(semantic_errors),
        )
        if semantic_errors:
            continue
        loaded_profile_ids.append(profile_id)
        loaded_categories.extend(sorted(category_ids))
        profile_checks = (
            profile.get("checks", []) if isinstance(profile.get("checks"), list) else []
        )
        for profile_check in profile_checks:
            if not isinstance(profile_check, dict):
                continue
            domain_check_id = str(profile_check["check_id"])
            severity = str(profile_check["severity"])
            recorded = quality_by_contract.get(domain_check_id) or quality_by_id.get(
                domain_check_id
            )
            if recorded:
                status = status_for_severity(str(recorded.get("status", "warn")), severity)
                message = str(
                    recorded.get("summary")
                    or f"Recorded domain validation result for {domain_check_id}"
                )
            else:
                status = "fail" if severity == "error" else "warn"
                message = (
                    f"Active domain check '{domain_check_id}' has no recorded result: "
                    f"{profile_check['criterion']}"
                )
            add(
                f"profile-{profile_id}-{domain_check_id}",
                str(profile_check["category"]),
                status,
                message,
                severity=severity,
                method="review",
                remediation=None
                if recorded
                else "Execute the domain check and record it in manifest quality checks.",
                supporting_refs=[
                    str(resolved_profile_references["verification catalog"])
                ]
                if "verification catalog" in resolved_profile_references
                else [],
            )
        if not profile_checks:
            for category_id in sorted(required_category_ids):
                recorded_category_checks = [
                    item
                    for item in quality_checks
                    if isinstance(item, dict)
                    and str(item.get("category", "")) == category_id
                ]
                if not recorded_category_checks:
                    status = "fail"
                    message = (
                        f"Active domain profile {profile_id} has no recorded check "
                        f"in required category {category_id}"
                    )
                else:
                    recorded_statuses = {
                        str(item.get("status", "warn"))
                        for item in recorded_category_checks
                    }
                    if "fail" in recorded_statuses:
                        status = "fail"
                    elif "warn" in recorded_statuses:
                        status = "warn"
                    elif "pass" in recorded_statuses:
                        status = "pass"
                    else:
                        status = "not_applicable"
                    message = (
                        f"Required domain category {category_id} has "
                        f"{len(recorded_category_checks)} recorded check(s)"
                    )
                add(
                    f"profile-{profile_id}-category-{category_id}",
                    category_id,
                    status,
                    message,
                    severity="error",
                    method="review",
                    remediation=None
                    if recorded_category_checks
                    else "Execute and record at least one check in this required domain category.",
                    supporting_refs=[
                        str(resolved_profile_references["verification catalog"])
                    ]
                    if "verification catalog" in resolved_profile_references
                    else [],
                )

    assurance = (
        str((contract.get("profile") or {}).get("assurance", "standard"))
        if isinstance(contract.get("profile"), dict)
        else "standard"
    )
    policy = contract.get("strict_policy", {}) if isinstance(contract.get("strict_policy"), dict) else {}
    strict_block = manifest.get("strict", {}) if isinstance(manifest.get("strict"), dict) else {}
    strict_errors: list[str] = []
    if assurance == "strict":
        for item in manifest_inputs:
            if isinstance(item, dict) and not item.get("sha256"):
                strict_errors.append(f"input {item.get('input_id')} lacks sha256")
        for artifact_id, item in artifact_by_id.items():
            if item.get("status") == "produced" and not item.get("sha256"):
                strict_errors.append(f"artifact {artifact_id} lacks sha256")
        environment = manifest.get("environment", {}) if isinstance(manifest.get("environment"), dict) else {}
        for component_type in ("runtimes", "packages"):
            for component in environment.get(component_type, []) or []:
                if not isinstance(component, dict):
                    continue
                version = str(component.get("version", ""))
                if not version or re.search(
                    r"(^|[._-])x($|[._-])|\*|\b(latest|unknown|unspecified)\b",
                    version,
                    re.I,
                ):
                    strict_errors.append(
                        f"{component_type[:-1]} {component.get('name')} lacks exact version"
                    )
        for source in external_source_list:
            if not isinstance(source, dict):
                continue
            if source.get("mutable") and not (
                source.get("version") or source.get("cache_artifact_id")
            ):
                strict_errors.append(
                    f"mutable source {source.get('source_id')} is not fixed or cached"
                )
        for execution in executions:
            if (
                isinstance(execution, dict)
                and execution.get("stochastic")
                and execution.get("random_seed") is None
            ):
                strict_errors.append(
                    f"stochastic execution {execution.get('execution_id')} lacks seed"
                )
        if policy.get("require_lockfile") and not strict_block.get("lockfiles"):
            strict_errors.append("required lockfile is absent")
        if policy.get("require_container") and not strict_block.get("container"):
            strict_errors.append("required container is absent")
        if policy.get("require_fixed_references") and not strict_block.get("references"):
            strict_errors.append("fixed references are absent")
        procedure = (
            strict_block.get("procedure")
            if isinstance(strict_block.get("procedure"), dict)
            else {}
        )
        if (
            procedure.get("resource_id")
            and str(procedure["resource_id"]) not in resource_ids
        ):
            strict_errors.append(
                f"procedure references unknown resource {procedure['resource_id']}"
            )
        if policy.get("require_cached_sources"):
            for source in external_source_list:
                if not isinstance(source, dict):
                    continue
                source_id = str(source.get("source_id", "unknown"))
                cache_id = source.get("cache_artifact_id")
                if not cache_id:
                    strict_errors.append(f"source {source_id} lacks required cached artifact")
                    continue
                cache = artifact_by_id.get(str(cache_id))
                if not cache:
                    strict_errors.append(
                        f"source {source_id} cache artifact {cache_id} is unresolved"
                    )
                elif (
                    cache.get("kind") != "cache"
                    or cache.get("status") != "produced"
                    or str(cache_id) in bad_artifact_ids
                ):
                    strict_errors.append(
                        f"source {source_id} cache artifact {cache_id} is not a valid produced cache"
                    )
        add(
            "strict-policy",
            "reproducibility",
            "pass" if not strict_errors else "fail",
            "Strict assurance requirements are represented"
            if not strict_errors
            else summarized(strict_errors),
        )

    rerun_required = assurance == "strict" and bool(policy.get("require_rerun"))
    rerun_record: dict[str, Any] = {}
    rerun_errors: list[str] = []
    rerun_path = args.rerun_record.resolve() if args.rerun_record else None
    if rerun_path:
        rerun_record = load_json(rerun_path, "rerun record", rerun_errors)
        rerun_errors.extend(validate_schema(rerun_record, schemas.get("rerun", {})))
        if rerun_record.get("contract_id") != contract_id:
            rerun_errors.append("rerun record contract_id does not match")
        if rerun_record.get("run_id") != run_id:
            rerun_errors.append("rerun record run_id does not match")
        comparison_duplicates = duplicate_ids(
            rerun_record.get("comparisons", []), "comparison_id"
        )
        if comparison_duplicates:
            rerun_errors.append(
                "duplicate rerun comparison IDs: " + ", ".join(comparison_duplicates)
            )
        tolerance_used = rerun_record.get("tolerance_used")
        contract_tolerance = policy.get("numeric_tolerance") if rerun_required else tolerance_used
        if (
            rerun_required
            and isinstance(tolerance_used, (int, float))
            and not isinstance(tolerance_used, bool)
            and isinstance(contract_tolerance, (int, float))
            and tolerance_used > contract_tolerance
        ):
            rerun_errors.append(
                f"rerun tolerance {tolerance_used} exceeds contract tolerance {contract_tolerance}"
            )
        for comparison in rerun_record.get("comparisons", []) or []:
            if not isinstance(comparison, dict):
                continue
            comparison_id = str(comparison.get("comparison_id", "unknown"))
            baseline_id = str(comparison.get("baseline_artifact_id", ""))
            if baseline_id not in artifact_by_id:
                rerun_errors.append(
                    f"{comparison_id}: unknown baseline artifact {baseline_id}"
                )
            observed = comparison.get("observed_difference")
            tolerance = contract_tolerance
            if (
                isinstance(observed, (int, float))
                and not isinstance(observed, bool)
                and isinstance(tolerance, (int, float))
                and observed > tolerance
            ):
                rerun_errors.append(
                    f"{comparison_id}: observed difference {observed} exceeds tolerance {tolerance}"
                )
        add(
            "schema-rerun-record",
            "reproducibility",
            "pass" if not rerun_errors else "fail",
            "Rerun record is valid and all numeric comparisons are within tolerance"
            if not rerun_errors
            else summarized(rerun_errors),
        )
    elif rerun_required:
        rerun_errors.append("strict policy requires a rerun record")
        add(
            "schema-rerun-record",
            "reproducibility",
            "fail",
            rerun_errors[0],
            remediation="Run the analysis independently, record numeric comparisons, and pass --rerun-record.",
        )

    metadata_errors: list[str] = []
    verifier_id = "verify-bundle-py"
    verifier_kind = "script"
    independent_of_executor = False
    independence_assertion = "not_asserted"
    if args.verifier_metadata:
        metadata = load_json(
            args.verifier_metadata.resolve(), "verifier metadata", metadata_errors
        )
        allowed = {"verifier_id", "kind", "independent_of_executor"}
        unknown = sorted(set(metadata) - allowed)
        if unknown:
            metadata_errors.append(
                "verifier metadata has unknown fields: " + ", ".join(unknown)
            )
        if not isinstance(metadata.get("verifier_id"), str) or not ID_RE.fullmatch(
            str(metadata.get("verifier_id", ""))
        ):
            metadata_errors.append("verifier metadata requires a valid verifier_id")
        if metadata.get("kind") not in {"agent", "script", "human", "hybrid"}:
            metadata_errors.append("verifier metadata requires a valid kind")
        if not isinstance(metadata.get("independent_of_executor"), bool):
            metadata_errors.append(
                "verifier metadata requires boolean independent_of_executor"
            )
        if not metadata_errors:
            verifier_id = str(metadata["verifier_id"])
            verifier_kind = str(metadata["kind"])
            independent_of_executor = bool(metadata["independent_of_executor"])
            independence_assertion = "metadata_file"
        add(
            "verifier-metadata",
            "reproducibility",
            "pass" if not metadata_errors else "fail",
            "Verifier metadata is explicit and valid"
            if not metadata_errors
            else summarized(metadata_errors),
        )
    if args.verifier_id:
        verifier_id = args.verifier_id
    if args.verifier_kind:
        verifier_kind = args.verifier_kind
    if args.independent_of_executor is not None:
        independent_of_executor = bool(args.independent_of_executor)
        independence_assertion = "cli"
    if assurance == "strict" and not independent_of_executor:
        add(
            "verifier-independence",
            "reproducibility",
            "warn",
            "Strict review was not asserted independent of the executor",
            severity="warning",
            remediation="Use an isolated verifier and explicitly record independence via CLI or metadata.",
        )

    rerun_comparisons = (
        rerun_record.get("comparisons", [])
        if isinstance(rerun_record.get("comparisons"), list)
        else []
    )
    observed_differences = [
        float(item["observed_difference"])
        for item in rerun_comparisons
        if isinstance(item, dict)
        and isinstance(item.get("observed_difference"), (int, float))
        and not isinstance(item.get("observed_difference"), bool)
    ]
    if not rerun_required:
        rerun_status = "not_required" if not rerun_path else ("fail" if rerun_errors else "pass")
    else:
        rerun_status = "missing" if not rerun_path else ("fail" if rerun_errors else "pass")
    rerun_summary: dict[str, Any] = {
        "required": rerun_required,
        "record_supplied": bool(rerun_path),
        "status": rerun_status,
        "comparison_count": len(rerun_comparisons),
    }
    if isinstance(policy.get("numeric_tolerance"), (int, float)):
        rerun_summary["contract_tolerance"] = policy["numeric_tolerance"]
    if observed_differences:
        rerun_summary["maximum_observed_difference"] = max(observed_differences)
    if rerun_path:
        rerun_summary["record_path"] = str(rerun_path)

    report_schema_check = add(
        "schema-report",
        "schema",
        "pass",
        "Generated verification report conforms to its structural schema",
    )

    def build_report() -> dict[str, Any]:
        statuses = [item["status"] for item in checks]
        if "fail" in statuses:
            overall = "fail"
        elif "warn" in statuses:
            overall = "pass_with_warnings"
        else:
            overall = "pass"
        counts = {
            status: statuses.count(status)
            for status in ("pass", "warn", "fail", "not_applicable")
        }
        report: dict[str, Any] = {
            "schema_version": "1.1.0",
            "artifact_type": "verification_report",
            "report_id": f"vr-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
            "contract_id": safe_id(contract_id, "unknown-contract"),
            "run_id": safe_id(run_id, "unknown-run"),
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "verifier": {
                "verifier_id": safe_id(verifier_id, "invalid-verifier-id"),
                "kind": verifier_kind
                if verifier_kind in {"agent", "script", "human", "hybrid"}
                else "script",
                "independent_of_executor": independent_of_executor,
                "independence_assertion": independence_assertion,
            },
            "overall_status": overall,
            "summary": (
                f"Deterministic verification: {counts['pass']} pass, "
                f"{counts['warn']} warning, {counts['fail']} fail."
            ),
            "checks": checks,
            "extensions": {
                "domain_profiles": loaded_profile_ids,
                "domain_categories": sorted(set(loaded_categories)),
            },
        }
        if assurance == "strict" or rerun_path:
            report["strict"] = {
                "context_isolated": bool(args.context_isolated),
                "verifier_tools": [
                    {
                        "name": "verify_bundle.py",
                        "version": "1.1.0",
                    }
                ],
                "rerun": rerun_summary,
            }
        return report

    report = build_report()
    report_errors = validate_schema(report, schemas.get("report", {}))
    if report_errors:
        report_schema_check["status"] = "fail"
        report_schema_check["message"] = summarized(report_errors)
        report_schema_check["remediation"] = (
            "Repair the report generator before relying on this verification artifact."
        )
        report = build_report()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    counts = {
        status: sum(item["status"] == status for item in checks)
        for status in ("pass", "warn", "fail", "not_applicable")
    }
    print(
        json.dumps(
            {
                "output": str(output_path),
                "overall_status": report["overall_status"],
                "counts": counts,
            }
        )
    )
    if report["overall_status"] == "fail" or (
        args.fail_on_warning and report["overall_status"] == "pass_with_warnings"
    ):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
