#!/usr/bin/env python3
"""Validate a run-manifest JSON file with optional contract and file checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlparse


ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
TOP_REQUIRED = {
    "schema_version",
    "artifact_type",
    "contract_id",
    "run_id",
    "status",
    "started_at",
    "inputs",
    "external_sources",
    "environment",
    "steps",
    "artifacts",
    "quality",
    "deviations",
    "extensions",
}
TOP_ALLOWED = TOP_REQUIRED | {"ended_at", "resources", "strict"}
LOCATOR_KINDS = {"file", "collection", "remote", "physical"}


class Problems:
    def __init__(self) -> None:
        self.items: list[str] = []

    def add(self, path: str, message: str) -> None:
        self.items.append(f"{path}: {message}")


def check_object(
    value: Any,
    path: str,
    required: Iterable[str],
    allowed: Iterable[str],
    problems: Problems,
) -> bool:
    if not isinstance(value, dict):
        problems.add(path, "must be an object")
        return False
    required_set = set(required)
    allowed_set = set(allowed)
    for key in sorted(required_set - value.keys()):
        problems.add(path, f"missing required key {key!r}")
    for key in sorted(value.keys() - allowed_set):
        problems.add(f"{path}.{key}", "unknown key; use top-level 'extensions' for extensions")
    return True


def check_list(value: Any, path: str, problems: Problems) -> bool:
    if not isinstance(value, list):
        problems.add(path, "must be an array")
        return False
    return True


def check_text(value: Any, path: str, problems: Problems) -> None:
    if not isinstance(value, str) or not value.strip():
        problems.add(path, "must be a non-empty string")


def check_id(value: Any, path: str, problems: Problems) -> None:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        problems.add(path, "must match ^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


def check_enum(value: Any, path: str, choices: set[str], problems: Problems) -> None:
    if value not in choices:
        problems.add(path, f"must be one of {sorted(choices)}")


def check_sha(value: Any, path: str, problems: Problems) -> None:
    if not isinstance(value, str) or not SHA_RE.fullmatch(value):
        problems.add(path, "must be a lowercase 64-character SHA-256")


def parse_timestamp(value: Any, path: str, problems: Problems) -> datetime | None:
    if not isinstance(value, str):
        problems.add(path, "must be an RFC 3339 UTC timestamp")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        problems.add(path, "must be an RFC 3339 UTC timestamp")
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        problems.add(path, "must include UTC offset Z or +00:00")
        return None
    return parsed


def check_nonnegative_int(value: Any, path: str, problems: Problems) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        problems.add(path, "must be a non-negative integer")


def check_unique_ids(items: list[Any], key: str, path: str, problems: Problems) -> None:
    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict) or not isinstance(item.get(key), str):
            continue
        value = item[key]
        if value in seen:
            problems.add(f"{path}[{index}].{key}", f"duplicate ID {value!r}")
        seen.add(value)


def check_id_array(value: Any, path: str, problems: Problems) -> None:
    if not check_list(value, path, problems):
        return
    seen: set[str] = set()
    for index, item in enumerate(value):
        check_id(item, f"{path}[{index}]", problems)
        if isinstance(item, str) and item in seen:
            problems.add(f"{path}[{index}]", f"duplicate ID {item!r}")
        elif isinstance(item, str):
            seen.add(item)


def validate_inputs(value: Any, schema_version: Any, problems: Problems) -> list[dict[str, Any]]:
    path = "$.inputs"
    if not check_list(value, path, problems):
        return []
    required = {"input_id", "contract_input_id", "uri"}
    if schema_version == "1.1.0":
        required.add("locator_kind")
    allowed = required | {"locator_kind", "media_type", "size_bytes", "sha256"}
    valid_items: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, required, allowed, problems):
            continue
        valid_items.append(item)
        check_id(item.get("input_id"), f"{item_path}.input_id", problems)
        check_id(item.get("contract_input_id"), f"{item_path}.contract_input_id", problems)
        if "locator_kind" in item:
            check_enum(item["locator_kind"], f"{item_path}.locator_kind", LOCATOR_KINDS, problems)
        check_text(item.get("uri"), f"{item_path}.uri", problems)
        if "media_type" in item:
            check_text(item["media_type"], f"{item_path}.media_type", problems)
        if "size_bytes" in item:
            check_nonnegative_int(item["size_bytes"], f"{item_path}.size_bytes", problems)
        if "sha256" in item:
            check_sha(item["sha256"], f"{item_path}.sha256", problems)
    check_unique_ids(value, "input_id", path, problems)
    return valid_items


def validate_resources(value: Any, schema_version: Any, problems: Problems) -> list[dict[str, Any]]:
    path = "$.resources"
    if value is None and schema_version != "1.1.0":
        return []
    if not check_list(value, path, problems):
        return []
    required = {"resource_id", "kind", "name"}
    allowed = required | {
        "version",
        "identifier",
        "uri",
        "lot",
        "serial_number",
        "sha256",
        "details",
    }
    kinds = {
        "protocol",
        "instrument",
        "reagent",
        "calibration",
        "model",
        "reference-standard",
        "other",
    }
    valid_items: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, required, allowed, problems):
            continue
        valid_items.append(item)
        check_id(item.get("resource_id"), f"{item_path}.resource_id", problems)
        check_enum(item.get("kind"), f"{item_path}.kind", kinds, problems)
        check_text(item.get("name"), f"{item_path}.name", problems)
        for key in ("version", "identifier", "uri", "lot", "serial_number"):
            if key in item:
                check_text(item[key], f"{item_path}.{key}", problems)
        if "sha256" in item:
            check_sha(item["sha256"], f"{item_path}.sha256", problems)
        if "details" in item and not isinstance(item["details"], dict):
            problems.add(f"{item_path}.details", "must be an object")
    check_unique_ids(value, "resource_id", path, problems)
    return valid_items


def validate_sources(value: Any, problems: Problems) -> list[dict[str, Any]]:
    path = "$.external_sources"
    if not check_list(value, path, problems):
        return []
    required = {"source_id", "kind", "name", "resource", "retrieved_at", "mutable"}
    allowed = required | {"version", "cache_artifact_id"}
    kinds = {"database", "api", "literature", "reference", "other"}
    valid_items: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, required, allowed, problems):
            continue
        valid_items.append(item)
        check_id(item.get("source_id"), f"{item_path}.source_id", problems)
        check_enum(item.get("kind"), f"{item_path}.kind", kinds, problems)
        check_text(item.get("name"), f"{item_path}.name", problems)
        check_text(item.get("resource"), f"{item_path}.resource", problems)
        parse_timestamp(item.get("retrieved_at"), f"{item_path}.retrieved_at", problems)
        if not isinstance(item.get("mutable"), bool):
            problems.add(f"{item_path}.mutable", "must be a boolean")
        if "version" in item:
            check_text(item["version"], f"{item_path}.version", problems)
        if "cache_artifact_id" in item:
            check_id(item["cache_artifact_id"], f"{item_path}.cache_artifact_id", problems)
    check_unique_ids(value, "source_id", path, problems)
    return valid_items


def validate_environment(value: Any, problems: Problems) -> None:
    path = "$.environment"
    keys = {"runtimes", "packages"}
    if not check_object(value, path, keys, keys, problems):
        return
    for collection in ("runtimes", "packages"):
        items = value.get(collection)
        item_path = f"{path}.{collection}"
        if not check_list(items, item_path, problems):
            continue
        component_keys = {"name", "version"}
        seen: set[str] = set()
        for index, item in enumerate(items):
            current = f"{item_path}[{index}]"
            if not check_object(item, current, component_keys, component_keys, problems):
                continue
            check_text(item.get("name"), f"{current}.name", problems)
            check_text(item.get("version"), f"{current}.version", problems)
            name = item.get("name")
            if isinstance(name, str) and name.casefold() in seen:
                problems.add(f"{current}.name", f"duplicate component {name!r}")
            elif isinstance(name, str):
                seen.add(name.casefold())


def validate_steps(value: Any, schema_version: Any, problems: Problems) -> list[dict[str, Any]]:
    path = "$.steps"
    if not check_list(value, path, problems):
        return []
    required = {
        "execution_id",
        "step_id",
        "implementation",
        "invocation",
        "parameters",
        "rationale",
        "status",
        "artifact_ids",
        "stochastic",
    }
    lineage_keys = {"input_ids", "upstream_artifact_ids", "resource_ids"}
    if schema_version == "1.1.0":
        required |= lineage_keys
    allowed = required | lineage_keys | {"random_seed"}
    implementation_required = {"kind", "ref"}
    implementation_allowed = implementation_required | {"version"}
    kinds = {"script", "notebook", "workflow", "command", "tool", "manual"}
    statuses = {"completed", "failed", "skipped"}
    valid_items: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, required, allowed, problems):
            continue
        valid_items.append(item)
        check_id(item.get("execution_id"), f"{item_path}.execution_id", problems)
        check_id(item.get("step_id"), f"{item_path}.step_id", problems)
        implementation = item.get("implementation")
        implementation_path = f"{item_path}.implementation"
        if check_object(
            implementation,
            implementation_path,
            implementation_required,
            implementation_allowed,
            problems,
        ):
            check_enum(implementation.get("kind"), f"{implementation_path}.kind", kinds, problems)
            check_text(implementation.get("ref"), f"{implementation_path}.ref", problems)
            if "version" in implementation:
                check_text(implementation["version"], f"{implementation_path}.version", problems)
        check_text(item.get("invocation"), f"{item_path}.invocation", problems)
        if not isinstance(item.get("parameters"), dict):
            problems.add(f"{item_path}.parameters", "must be an object")
        check_text(item.get("rationale"), f"{item_path}.rationale", problems)
        check_enum(item.get("status"), f"{item_path}.status", statuses, problems)
        for key in sorted(lineage_keys):
            if key in item:
                check_id_array(item[key], f"{item_path}.{key}", problems)
        check_id_array(item.get("artifact_ids"), f"{item_path}.artifact_ids", problems)
        if not isinstance(item.get("stochastic"), bool):
            problems.add(f"{item_path}.stochastic", "must be a boolean")
        if "random_seed" in item:
            check_nonnegative_int(item["random_seed"], f"{item_path}.random_seed", problems)
    check_unique_ids(value, "execution_id", path, problems)
    return valid_items


def validate_artifacts(value: Any, schema_version: Any, problems: Problems) -> list[dict[str, Any]]:
    path = "$.artifacts"
    if not check_list(value, path, problems):
        return []
    required = {"artifact_id", "kind", "status"}
    if schema_version == "1.1.0":
        required.add("locator_kind")
    allowed = required | {"output_id", "locator_kind", "uri", "media_type", "size_bytes", "sha256"}
    kinds = {"table", "figure", "model", "data", "report", "log", "cache", "lockfile", "reference", "other"}
    statuses = {"produced", "empty", "missing", "failed"}
    valid_items: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, required, allowed, problems):
            continue
        valid_items.append(item)
        check_id(item.get("artifact_id"), f"{item_path}.artifact_id", problems)
        if "output_id" in item:
            check_id(item["output_id"], f"{item_path}.output_id", problems)
        check_enum(item.get("kind"), f"{item_path}.kind", kinds, problems)
        check_enum(item.get("status"), f"{item_path}.status", statuses, problems)
        if "locator_kind" in item:
            check_enum(item["locator_kind"], f"{item_path}.locator_kind", LOCATOR_KINDS, problems)
        if item.get("status") in {"produced", "empty"} and "uri" not in item:
            problems.add(f"{item_path}.uri", "is required for produced or empty artifacts")
        if "uri" in item:
            check_text(item["uri"], f"{item_path}.uri", problems)
        if "media_type" in item:
            check_text(item["media_type"], f"{item_path}.media_type", problems)
        if "size_bytes" in item:
            check_nonnegative_int(item["size_bytes"], f"{item_path}.size_bytes", problems)
            if item.get("status") == "empty" and item["size_bytes"] != 0:
                problems.add(f"{item_path}.size_bytes", "must be 0 when status is 'empty'")
            if item.get("status") == "produced" and item["size_bytes"] == 0:
                problems.add(f"{item_path}.size_bytes", "must be greater than 0 when status is 'produced'")
        if "sha256" in item:
            check_sha(item["sha256"], f"{item_path}.sha256", problems)
    check_unique_ids(value, "artifact_id", path, problems)
    return valid_items


def validate_performance_status(value: Any, path: str, problems: Problems) -> None:
    required = {"status"}
    allowed = required | {"reason"}
    if not check_object(value, path, required, allowed, problems):
        return
    check_enum(value.get("status"), f"{path}.status", {"performed", "not_performed", "not_applicable"}, problems)
    if value.get("status") in {"not_performed", "not_applicable"} and "reason" not in value:
        problems.add(f"{path}.reason", "is required for this status")
    if "reason" in value:
        check_text(value["reason"], f"{path}.reason", problems)


def validate_quality(value: Any, problems: Problems) -> list[dict[str, Any]]:
    path = "$.quality"
    required = {"input_qc", "statistical_assumptions", "checks"}
    if not check_object(value, path, required, required, problems):
        return []
    validate_performance_status(value.get("input_qc"), f"{path}.input_qc", problems)
    validate_performance_status(value.get("statistical_assumptions"), f"{path}.statistical_assumptions", problems)
    checks = value.get("checks")
    if not check_list(checks, f"{path}.checks", problems):
        return []
    required_check = {"check_id", "category", "status", "summary", "artifact_ids"}
    allowed_check = required_check | {"contract_check_id"}
    statuses = {"pass", "warn", "fail", "not_applicable"}
    valid_items: list[dict[str, Any]] = []
    for index, item in enumerate(checks):
        item_path = f"{path}.checks[{index}]"
        if not check_object(item, item_path, required_check, allowed_check, problems):
            continue
        valid_items.append(item)
        check_id(item.get("check_id"), f"{item_path}.check_id", problems)
        if "contract_check_id" in item:
            check_id(item["contract_check_id"], f"{item_path}.contract_check_id", problems)
        check_id(item.get("category"), f"{item_path}.category", problems)
        check_enum(item.get("status"), f"{item_path}.status", statuses, problems)
        check_text(item.get("summary"), f"{item_path}.summary", problems)
        check_id_array(item.get("artifact_ids"), f"{item_path}.artifact_ids", problems)
    check_unique_ids(checks, "check_id", f"{path}.checks", problems)
    return valid_items


def validate_deviations(value: Any, problems: Problems) -> list[dict[str, Any]]:
    path = "$.deviations"
    if not check_list(value, path, problems):
        return []
    keys = {"deviation_id", "target_type", "target_id", "reason", "impact"}
    target_types = {"input", "source", "resource", "step", "artifact", "output", "parameter", "other"}
    valid_items: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, keys, keys, problems):
            continue
        valid_items.append(item)
        check_id(item.get("deviation_id"), f"{item_path}.deviation_id", problems)
        check_enum(item.get("target_type"), f"{item_path}.target_type", target_types, problems)
        check_id(item.get("target_id"), f"{item_path}.target_id", problems)
        check_text(item.get("reason"), f"{item_path}.reason", problems)
        check_text(item.get("impact"), f"{item_path}.impact", problems)
    check_unique_ids(value, "deviation_id", path, problems)
    return valid_items


def validate_strict_block(value: Any, problems: Problems) -> dict[str, Any] | None:
    path = "$.strict"
    required = {"lockfiles", "references"}
    allowed = required | {"code_revision", "pipeline", "procedure", "container"}
    if not check_object(value, path, required, allowed, problems):
        return None
    if not any(key in value for key in ("code_revision", "pipeline", "procedure")):
        problems.add(path, "must contain 'code_revision', 'pipeline', or 'procedure'")

    if "code_revision" in value:
        revision = value["code_revision"]
        revision_path = f"{path}.code_revision"
        keys = {"repository", "commit", "dirty"}
        if check_object(revision, revision_path, keys, keys, problems):
            check_text(revision.get("repository"), f"{revision_path}.repository", problems)
            check_text(revision.get("commit"), f"{revision_path}.commit", problems)
            if not isinstance(revision.get("dirty"), bool):
                problems.add(f"{revision_path}.dirty", "must be a boolean")

    if "pipeline" in value:
        pipeline = value["pipeline"]
        pipeline_path = f"{path}.pipeline"
        keys = {"name", "version", "definition_sha256"}
        if check_object(pipeline, pipeline_path, keys, keys, problems):
            check_text(pipeline.get("name"), f"{pipeline_path}.name", problems)
            check_text(pipeline.get("version"), f"{pipeline_path}.version", problems)
            check_sha(pipeline.get("definition_sha256"), f"{pipeline_path}.definition_sha256", problems)

    if "procedure" in value:
        procedure = value["procedure"]
        procedure_path = f"{path}.procedure"
        required_procedure = {"name", "version", "ref", "definition_sha256"}
        allowed_procedure = required_procedure | {"resource_id"}
        if check_object(
            procedure,
            procedure_path,
            required_procedure,
            allowed_procedure,
            problems,
        ):
            check_text(procedure.get("name"), f"{procedure_path}.name", problems)
            check_text(procedure.get("version"), f"{procedure_path}.version", problems)
            check_text(procedure.get("ref"), f"{procedure_path}.ref", problems)
            check_sha(procedure.get("definition_sha256"), f"{procedure_path}.definition_sha256", problems)
            if "resource_id" in procedure:
                check_id(procedure["resource_id"], f"{procedure_path}.resource_id", problems)

    lockfiles = value.get("lockfiles")
    if check_list(lockfiles, f"{path}.lockfiles", problems):
        keys = {"uri", "sha256"}
        for index, item in enumerate(lockfiles):
            item_path = f"{path}.lockfiles[{index}]"
            if not check_object(item, item_path, keys, keys, problems):
                continue
            check_text(item.get("uri"), f"{item_path}.uri", problems)
            check_sha(item.get("sha256"), f"{item_path}.sha256", problems)

    if "container" in value:
        container = value["container"]
        container_path = f"{path}.container"
        keys = {"engine", "image", "digest"}
        if check_object(container, container_path, keys, keys, problems):
            check_enum(container.get("engine"), f"{container_path}.engine", {"docker", "apptainer", "other"}, problems)
            check_text(container.get("image"), f"{container_path}.image", problems)
            digest = container.get("digest")
            if not isinstance(digest, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
                problems.add(f"{container_path}.digest", "must be 'sha256:' followed by 64 lowercase hex characters")

    references = value.get("references")
    if check_list(references, f"{path}.references", problems):
        keys = {"reference_id", "name", "release", "uri", "sha256"}
        for index, item in enumerate(references):
            item_path = f"{path}.references[{index}]"
            if not check_object(item, item_path, keys, keys, problems):
                continue
            check_id(item.get("reference_id"), f"{item_path}.reference_id", problems)
            check_text(item.get("name"), f"{item_path}.name", problems)
            check_text(item.get("release"), f"{item_path}.release", problems)
            check_text(item.get("uri"), f"{item_path}.uri", problems)
            check_sha(item.get("sha256"), f"{item_path}.sha256", problems)
        check_unique_ids(references, "reference_id", f"{path}.references", problems)
    return value


def has_deviation(deviations: list[dict[str, Any]], target_type: str, *target_ids: str) -> bool:
    return any(
        item.get("target_type") == target_type and item.get("target_id") in target_ids
        for item in deviations
    )


def validate_references(
    inputs: list[dict[str, Any]],
    steps: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    resources: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    checks: list[dict[str, Any]],
    strict_block: dict[str, Any] | None,
    problems: Problems,
) -> None:
    input_ids = {item.get("input_id") for item in inputs}
    resource_ids = {item.get("resource_id") for item in resources}
    artifact_ids = {item.get("artifact_id") for item in artifacts}
    for index, step in enumerate(steps):
        for input_id in step.get("input_ids", []):
            if input_id not in input_ids:
                problems.add(f"$.steps[{index}].input_ids", f"unknown input ID {input_id!r}")
        for artifact_id in step.get("upstream_artifact_ids", []):
            if artifact_id not in artifact_ids:
                problems.add(
                    f"$.steps[{index}].upstream_artifact_ids",
                    f"unknown artifact ID {artifact_id!r}",
                )
        for resource_id in step.get("resource_ids", []):
            if resource_id not in resource_ids:
                problems.add(f"$.steps[{index}].resource_ids", f"unknown resource ID {resource_id!r}")
        for artifact_id in step.get("artifact_ids", []):
            if artifact_id not in artifact_ids:
                problems.add(f"$.steps[{index}].artifact_ids", f"unknown artifact ID {artifact_id!r}")
    for index, source in enumerate(sources):
        cache_id = source.get("cache_artifact_id")
        if cache_id is not None and cache_id not in artifact_ids:
            problems.add(f"$.external_sources[{index}].cache_artifact_id", f"unknown artifact ID {cache_id!r}")
    for index, check in enumerate(checks):
        for artifact_id in check.get("artifact_ids", []):
            if artifact_id not in artifact_ids:
                problems.add(f"$.quality.checks[{index}].artifact_ids", f"unknown artifact ID {artifact_id!r}")
    if isinstance(strict_block, dict):
        procedure = strict_block.get("procedure")
        if isinstance(procedure, dict) and procedure.get("resource_id") not in {None, *resource_ids}:
            problems.add("$.strict.procedure.resource_id", "must reference a declared resource_id")


def major_version(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    return value.split(".", 1)[0]


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate_against_contract(
    data: dict[str, Any],
    contract: Any,
    deviations: list[dict[str, Any]],
    problems: Problems,
) -> tuple[bool, dict[str, Any]]:
    if not isinstance(contract, dict):
        problems.add("contract", "must be a JSON object")
        return False, {}
    if contract.get("artifact_type") != "analysis_contract":
        problems.add("contract.artifact_type", "must equal 'analysis_contract'")
    if data.get("contract_id") != contract.get("contract_id"):
        problems.add("$.contract_id", "does not match the linked analysis contract")
    if major_version(data.get("schema_version")) != major_version(contract.get("schema_version")):
        problems.add("$.schema_version", "major version does not match the linked contract")

    contract_inputs = {
        item.get("input_id"): item
        for item in as_list(contract.get("inputs"))
        if isinstance(item, dict) and isinstance(item.get("input_id"), str)
    }
    mapped_inputs: dict[str, list[dict[str, Any]]] = {}
    for index, item in enumerate(as_list(data.get("inputs"))):
        if not isinstance(item, dict):
            continue
        logical_id = item.get("contract_input_id")
        mapped_inputs.setdefault(logical_id, []).append(item)
        if logical_id not in contract_inputs and not has_deviation(
            deviations, "input", item.get("input_id", ""), str(logical_id)
        ):
            problems.add(f"$.inputs[{index}].contract_input_id", "is not declared by the contract and has no deviation")
    for input_id, specification in contract_inputs.items():
        if specification.get("required") is True and not mapped_inputs.get(input_id):
            problems.add("$.inputs", f"missing concrete input for required contract input {input_id!r}")

    planned_steps = {
        item.get("step_id")
        for item in as_list(contract.get("steps"))
        if isinstance(item, dict) and isinstance(item.get("step_id"), str)
    }
    for index, item in enumerate(as_list(data.get("steps"))):
        if not isinstance(item, dict):
            continue
        if item.get("step_id") not in planned_steps and not has_deviation(
            deviations, "step", item.get("execution_id", ""), item.get("step_id", "")
        ):
            problems.add(f"$.steps[{index}].step_id", "is not declared by the contract and has no deviation")

    required_outputs = {
        item.get("output_id")
        for item in as_list(contract.get("required_outputs"))
        if isinstance(item, dict) and isinstance(item.get("output_id"), str)
    }
    artifact_outputs: dict[str, list[dict[str, Any]]] = {}
    for index, item in enumerate(as_list(data.get("artifacts"))):
        if not isinstance(item, dict) or "output_id" not in item:
            continue
        output_id = item.get("output_id")
        artifact_outputs.setdefault(output_id, []).append(item)
        if output_id not in required_outputs and not has_deviation(
            deviations, "output", str(output_id), item.get("artifact_id", "")
        ):
            problems.add(f"$.artifacts[{index}].output_id", "is not declared by the contract and has no deviation")
    if data.get("status") in {"completed", "partial", "failed"}:
        for output_id in sorted(required_outputs):
            if not artifact_outputs.get(output_id):
                problems.add("$.artifacts", f"missing explicit artifact record for required output {output_id!r}")
            elif data.get("status") == "completed" and not any(
                artifact.get("status") == "produced" for artifact in artifact_outputs[output_id]
            ):
                problems.add("$.artifacts", f"completed run has no produced artifact for required output {output_id!r}")

    assurance = contract.get("profile", {}).get("assurance") if isinstance(contract.get("profile"), dict) else None
    strict_policy = contract.get("strict_policy") if isinstance(contract.get("strict_policy"), dict) else {}
    return assurance == "strict", strict_policy


def validate_strict_requirements(
    inputs: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    steps: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    strict_block: dict[str, Any] | None,
    strict_policy: dict[str, Any],
    problems: Problems,
) -> None:
    for index, item in enumerate(inputs):
        if item.get("locator_kind", "file") == "file" and "sha256" not in item:
            problems.add(f"$.inputs[{index}].sha256", "is required in strict mode")
    artifact_by_id = {item.get("artifact_id"): item for item in artifacts}
    for index, item in enumerate(artifacts):
        if (
            item.get("locator_kind", "file") == "file"
            and item.get("status") in {"produced", "empty"}
            and "sha256" not in item
        ):
            problems.add(f"$.artifacts[{index}].sha256", "is required for produced or empty artifacts in strict mode")
    for index, item in enumerate(sources):
        cache_id = item.get("cache_artifact_id")
        if item.get("mutable") is True and cache_id is None:
            problems.add(f"$.external_sources[{index}].cache_artifact_id", "is required for mutable sources in strict mode")
        if "version" not in item and cache_id is None:
            problems.add(f"$.external_sources[{index}]", "must record a fixed version or cached artifact in strict mode")
        if cache_id is not None:
            cache = artifact_by_id.get(cache_id)
            if cache is not None and (cache.get("status") != "produced" or "sha256" not in cache):
                problems.add(f"$.external_sources[{index}].cache_artifact_id", "must reference a produced, hashed artifact")
    for index, item in enumerate(steps):
        if item.get("stochastic") is True and "random_seed" not in item:
            problems.add(f"$.steps[{index}].random_seed", "is required for stochastic execution in strict mode")
    if strict_block is None:
        problems.add("$.strict", "is required in strict mode")
        return
    revision = strict_block.get("code_revision")
    if (
        isinstance(revision, dict)
        and revision.get("dirty") is True
        and "pipeline" not in strict_block
        and "procedure" not in strict_block
    ):
        problems.add(
            "$.strict.code_revision.dirty",
            "cannot be true without an immutable pipeline or procedure definition in strict mode",
        )
    software_provenance = "code_revision" in strict_block or "pipeline" in strict_block
    if strict_policy.get("require_lockfile", software_provenance) and not strict_block.get("lockfiles"):
        problems.add("$.strict.lockfiles", "must contain at least one lockfile in strict mode")
    if strict_policy.get("require_container", False) and "container" not in strict_block:
        problems.add("$.strict.container", "is required by the analysis contract")
    if strict_policy.get("require_fixed_references", False):
        reference_names = {
            item.get("name")
            for item in as_list(strict_block.get("references"))
            if isinstance(item, dict)
        }
        for index, source in enumerate(sources):
            if source.get("kind") == "reference" and source.get("name") not in reference_names:
                problems.add(f"$.external_sources[{index}]", "reference is not frozen in $.strict.references")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def local_path(uri: Any, root: Path) -> Path | None:
    if not isinstance(uri, str):
        return None
    parsed = urlparse(uri)
    if parsed.scheme not in {"", "file"}:
        return None
    candidate = Path(unquote(parsed.path if parsed.scheme == "file" else uri))
    return candidate if candidate.is_absolute() else root / candidate


def check_file_record(record: dict[str, Any], path: str, root: Path, problems: Problems) -> None:
    if record.get("locator_kind", "file") != "file":
        return
    file_path = local_path(record.get("uri"), root)
    if file_path is None:
        return
    if not file_path.is_file():
        problems.add(f"{path}.uri", f"local file does not exist: {file_path}")
        return
    size = file_path.stat().st_size
    if "size_bytes" in record and record["size_bytes"] != size:
        problems.add(f"{path}.size_bytes", f"recorded {record['size_bytes']}, observed {size}")
    if record.get("status") == "empty" and size != 0:
        problems.add(f"{path}.status", f"marked empty but observed {size} bytes")
    if record.get("status") == "produced" and size == 0:
        problems.add(f"{path}.status", "marked produced but file is empty")
    if "sha256" in record:
        observed = sha256_file(file_path)
        if observed != record["sha256"]:
            problems.add(f"{path}.sha256", f"checksum mismatch; observed {observed}")


def check_local_files(data: dict[str, Any], root: Path, problems: Problems) -> None:
    for index, item in enumerate(as_list(data.get("inputs"))):
        if isinstance(item, dict):
            check_file_record(item, f"$.inputs[{index}]", root, problems)
    for index, item in enumerate(as_list(data.get("artifacts"))):
        if isinstance(item, dict) and item.get("status") in {"produced", "empty"}:
            check_file_record(item, f"$.artifacts[{index}]", root, problems)
    strict = data.get("strict")
    if isinstance(strict, dict):
        for collection in ("lockfiles", "references"):
            for index, item in enumerate(as_list(strict.get(collection))):
                if isinstance(item, dict):
                    check_file_record(item, f"$.strict.{collection}[{index}]", root, problems)


def validate(
    data: Any,
    contract: Any | None = None,
    force_strict: bool = False,
    check_files: bool = False,
    root: Path | None = None,
) -> list[str]:
    problems = Problems()
    if not check_object(data, "$", TOP_REQUIRED, TOP_ALLOWED, problems):
        return problems.items
    schema_version = data.get("schema_version")
    if schema_version not in {"1.0.0", "1.1.0"}:
        problems.add("$.schema_version", "must equal '1.0.0' or '1.1.0'")
    if data.get("artifact_type") != "run_manifest":
        problems.add("$.artifact_type", "must equal 'run_manifest'")
    check_id(data.get("contract_id"), "$.contract_id", problems)
    check_id(data.get("run_id"), "$.run_id", problems)
    check_enum(data.get("status"), "$.status", {"running", "completed", "partial", "failed"}, problems)
    started = parse_timestamp(data.get("started_at"), "$.started_at", problems)
    ended = parse_timestamp(data.get("ended_at"), "$.ended_at", problems) if "ended_at" in data else None
    if data.get("status") in {"completed", "partial", "failed"} and "ended_at" not in data:
        problems.add("$.ended_at", "is required when the run is no longer running")
    if started is not None and ended is not None and ended < started:
        problems.add("$.ended_at", "must not precede started_at")

    inputs = validate_inputs(data.get("inputs"), schema_version, problems)
    sources = validate_sources(data.get("external_sources"), problems)
    if schema_version == "1.1.0" and "resources" not in data:
        problems.add("$.resources", "is required in schema 1.1.0")
    resources = validate_resources(data.get("resources"), schema_version, problems)
    validate_environment(data.get("environment"), problems)
    steps = validate_steps(data.get("steps"), schema_version, problems)
    artifacts = validate_artifacts(data.get("artifacts"), schema_version, problems)
    checks = validate_quality(data.get("quality"), problems)
    deviations = validate_deviations(data.get("deviations"), problems)
    if not isinstance(data.get("extensions"), dict):
        problems.add("$.extensions", "must be an object")
    strict_block = validate_strict_block(data["strict"], problems) if "strict" in data else None
    validate_references(inputs, steps, sources, resources, artifacts, checks, strict_block, problems)

    contract_strict = False
    strict_policy: dict[str, Any] = {}
    if contract is not None:
        contract_strict, strict_policy = validate_against_contract(data, contract, deviations, problems)
    if force_strict or contract_strict:
        validate_strict_requirements(inputs, sources, steps, artifacts, strict_block, strict_policy, problems)
    if check_files:
        check_local_files(data, (root or Path.cwd()).resolve(), problems)
    return problems.items


def load_json(path: Path, label: str) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label} {path}: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Path to run-manifest.json")
    parser.add_argument("--contract", type=Path, help="Optional analysis-contract.json")
    parser.add_argument("--strict", action="store_true", help="Enforce strict-mode requirements")
    parser.add_argument("--check-files", action="store_true", help="Verify local paths, sizes, and recorded hashes")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root for relative file paths (default: current directory)")
    args = parser.parse_args()

    try:
        data = load_json(args.manifest, "manifest")
        contract = load_json(args.contract, "contract") if args.contract else None
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate(data, contract, args.strict, args.check_files, args.root)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(f"INVALID run_manifest ({len(errors)} error(s))", file=sys.stderr)
        return 1

    print(f"VALID run_manifest: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
