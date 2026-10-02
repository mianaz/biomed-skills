#!/usr/bin/env python3
"""Validate an analysis-contract JSON file using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
TOP_REQUIRED = {
    "schema_version",
    "artifact_type",
    "contract_id",
    "profile",
    "objective",
    "questions",
    "inputs",
    "design",
    "steps",
    "required_outputs",
    "validation",
    "constraints",
    "audiences",
    "extensions",
}
TOP_ALLOWED = TOP_REQUIRED | {"governance", "strict_policy"}


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
        problems.add(f"{path}.{key}", "unknown key; put extensions under top-level 'extensions'")
    return True


def check_list(value: Any, path: str, problems: Problems, *, nonempty: bool = False) -> bool:
    if not isinstance(value, list):
        problems.add(path, "must be an array")
        return False
    if nonempty and not value:
        problems.add(path, "must contain at least one item")
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


def check_unique_ids(items: list[Any], key: str, path: str, problems: Problems) -> None:
    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict) or key not in item:
            continue
        value = item[key]
        if isinstance(value, str) and value in seen:
            problems.add(f"{path}[{index}].{key}", f"duplicate ID {value!r}")
        elif isinstance(value, str):
            seen.add(value)


def validate_profile(value: Any, problems: Problems) -> str | None:
    path = "$.profile"
    keys = {"analysis_mode", "assurance", "autonomy"}
    if not check_object(value, path, keys, keys, problems):
        return None
    check_enum(value.get("analysis_mode"), f"{path}.analysis_mode", {"exploratory", "confirmatory"}, problems)
    check_enum(value.get("assurance"), f"{path}.assurance", {"basic", "standard", "strict"}, problems)
    check_enum(
        value.get("autonomy"),
        f"{path}.autonomy",
        {"autonomous", "collaborative", "approval_required"},
        problems,
    )
    return value.get("assurance") if isinstance(value.get("assurance"), str) else None


def validate_questions(value: Any, problems: Problems) -> None:
    path = "$.questions"
    if not check_list(value, path, problems, nonempty=True):
        return
    keys = {"question_id", "text"}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, keys, keys, problems):
            continue
        check_id(item.get("question_id"), f"{item_path}.question_id", problems)
        check_text(item.get("text"), f"{item_path}.text", problems)
    check_unique_ids(value, "question_id", path, problems)


def validate_inputs(value: Any, problems: Problems) -> None:
    path = "$.inputs"
    if not check_list(value, path, problems):
        return
    keys = {"input_id", "role", "required", "description"}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, keys, keys, problems):
            continue
        check_id(item.get("input_id"), f"{item_path}.input_id", problems)
        check_id(item.get("role"), f"{item_path}.role", problems)
        if not isinstance(item.get("required"), bool):
            problems.add(f"{item_path}.required", "must be a boolean")
        check_text(item.get("description"), f"{item_path}.description", problems)
    check_unique_ids(value, "input_id", path, problems)


def validate_design(value: Any, schema_version: Any, problems: Problems) -> None:
    path = "$.design"
    required = {"study_type", "analysis_unit", "factors", "contrasts", "covariates"}
    general_fields = {"units", "outcomes", "analysis_sets"}
    if schema_version == "1.1.0":
        required |= general_fields
    if not check_object(value, path, required, required | general_fields, problems):
        return
    check_text(value.get("study_type"), f"{path}.study_type", problems)
    check_text(value.get("analysis_unit"), f"{path}.analysis_unit", problems)

    units = value.get("units")
    unit_ids: set[str] = set()
    parent_by_id: dict[str, str] = {}
    if "units" in value and check_list(units, f"{path}.units", problems, nonempty=True):
        unit_required = {"unit_id", "description"}
        unit_allowed = unit_required | {"parent_unit_id"}
        for index, item in enumerate(units):
            item_path = f"{path}.units[{index}]"
            if not check_object(item, item_path, unit_required, unit_allowed, problems):
                continue
            check_id(item.get("unit_id"), f"{item_path}.unit_id", problems)
            check_text(item.get("description"), f"{item_path}.description", problems)
            if "parent_unit_id" in item:
                check_id(item["parent_unit_id"], f"{item_path}.parent_unit_id", problems)
            if isinstance(item.get("unit_id"), str):
                unit_ids.add(item["unit_id"])
                if isinstance(item.get("parent_unit_id"), str):
                    parent_by_id[item["unit_id"]] = item["parent_unit_id"]
        check_unique_ids(units, "unit_id", f"{path}.units", problems)
        for unit_id, parent_id in parent_by_id.items():
            if parent_id not in unit_ids:
                problems.add(f"{path}.units", f"unit {unit_id!r} has unknown parent {parent_id!r}")
            if parent_id == unit_id:
                problems.add(f"{path}.units", f"unit {unit_id!r} cannot be its own parent")
        for unit_id in unit_ids:
            seen: set[str] = set()
            current = unit_id
            while current in parent_by_id:
                if current in seen:
                    problems.add(f"{path}.units", f"parent hierarchy contains a cycle involving {current!r}")
                    break
                seen.add(current)
                current = parent_by_id[current]
        if schema_version == "1.1.0" and value.get("analysis_unit") not in unit_ids:
            problems.add(f"{path}.analysis_unit", "must equal a declared unit_id in schema 1.1.0")

    outcomes = value.get("outcomes")
    if "outcomes" in value and check_list(outcomes, f"{path}.outcomes", problems):
        outcome_required = {"outcome_id", "role", "definition"}
        outcome_allowed = outcome_required | {"unit_id"}
        roles = {"primary", "secondary", "exploratory", "safety", "other"}
        for index, item in enumerate(outcomes):
            item_path = f"{path}.outcomes[{index}]"
            if not check_object(item, item_path, outcome_required, outcome_allowed, problems):
                continue
            check_id(item.get("outcome_id"), f"{item_path}.outcome_id", problems)
            check_enum(item.get("role"), f"{item_path}.role", roles, problems)
            check_text(item.get("definition"), f"{item_path}.definition", problems)
            if "unit_id" in item:
                check_id(item["unit_id"], f"{item_path}.unit_id", problems)
                if unit_ids and item["unit_id"] not in unit_ids:
                    problems.add(f"{item_path}.unit_id", "must reference a declared unit_id")
        check_unique_ids(outcomes, "outcome_id", f"{path}.outcomes", problems)

    analysis_sets = value.get("analysis_sets")
    if "analysis_sets" in value and check_list(
        analysis_sets, f"{path}.analysis_sets", problems, nonempty=True
    ):
        set_keys = {"analysis_set_id", "unit_id", "definition"}
        for index, item in enumerate(analysis_sets):
            item_path = f"{path}.analysis_sets[{index}]"
            if not check_object(item, item_path, set_keys, set_keys, problems):
                continue
            check_id(item.get("analysis_set_id"), f"{item_path}.analysis_set_id", problems)
            check_id(item.get("unit_id"), f"{item_path}.unit_id", problems)
            check_text(item.get("definition"), f"{item_path}.definition", problems)
            if unit_ids and item.get("unit_id") not in unit_ids:
                problems.add(f"{item_path}.unit_id", "must reference a declared unit_id")
        check_unique_ids(analysis_sets, "analysis_set_id", f"{path}.analysis_sets", problems)

    factors = value.get("factors")
    if check_list(factors, f"{path}.factors", problems):
        factor_keys = {"factor_id", "levels"}
        for index, item in enumerate(factors):
            item_path = f"{path}.factors[{index}]"
            if not check_object(item, item_path, factor_keys, factor_keys, problems):
                continue
            check_id(item.get("factor_id"), f"{item_path}.factor_id", problems)
            levels = item.get("levels")
            if check_list(levels, f"{item_path}.levels", problems, nonempty=True):
                for level_index, level in enumerate(levels):
                    check_text(level, f"{item_path}.levels[{level_index}]", problems)
                if all(isinstance(level, str) for level in levels) and len(levels) != len(set(levels)):
                    problems.add(f"{item_path}.levels", "must not contain duplicate levels")
        check_unique_ids(factors, "factor_id", f"{path}.factors", problems)

    contrasts = value.get("contrasts")
    if check_list(contrasts, f"{path}.contrasts", problems):
        contrast_keys = {"contrast_id", "definition"}
        for index, item in enumerate(contrasts):
            item_path = f"{path}.contrasts[{index}]"
            if not check_object(item, item_path, contrast_keys, contrast_keys, problems):
                continue
            check_id(item.get("contrast_id"), f"{item_path}.contrast_id", problems)
            check_text(item.get("definition"), f"{item_path}.definition", problems)
        check_unique_ids(contrasts, "contrast_id", f"{path}.contrasts", problems)

    covariates = value.get("covariates")
    if check_list(covariates, f"{path}.covariates", problems):
        for index, covariate in enumerate(covariates):
            check_text(covariate, f"{path}.covariates[{index}]", problems)
        if all(isinstance(covariate, str) for covariate in covariates) and len(covariates) != len(set(covariates)):
            problems.add(f"{path}.covariates", "must not contain duplicates")


def validate_steps(value: Any, problems: Problems) -> None:
    path = "$.steps"
    if not check_list(value, path, problems, nonempty=True):
        return
    required = {"step_id", "purpose"}
    allowed = required | {"method", "selection_rule"}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, required, allowed, problems):
            continue
        check_id(item.get("step_id"), f"{item_path}.step_id", problems)
        check_text(item.get("purpose"), f"{item_path}.purpose", problems)
        if "method" not in item and "selection_rule" not in item:
            problems.add(item_path, "must contain 'method' or 'selection_rule'")
        for key in ("method", "selection_rule"):
            if key in item:
                check_text(item[key], f"{item_path}.{key}", problems)
    check_unique_ids(value, "step_id", path, problems)


def validate_outputs(value: Any, problems: Problems) -> None:
    path = "$.required_outputs"
    if not check_list(value, path, problems, nonempty=True):
        return
    keys = {"output_id", "kind", "description"}
    kinds = {"table", "figure", "model", "data", "report", "other"}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, keys, keys, problems):
            continue
        check_id(item.get("output_id"), f"{item_path}.output_id", problems)
        check_enum(item.get("kind"), f"{item_path}.kind", kinds, problems)
        check_text(item.get("description"), f"{item_path}.description", problems)
    check_unique_ids(value, "output_id", path, problems)


def validate_validation(value: Any, problems: Problems) -> None:
    path = "$.validation"
    if not check_list(value, path, problems, nonempty=True):
        return
    keys = {"check_id", "criterion", "severity"}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, keys, keys, problems):
            continue
        check_id(item.get("check_id"), f"{item_path}.check_id", problems)
        check_text(item.get("criterion"), f"{item_path}.criterion", problems)
        check_enum(item.get("severity"), f"{item_path}.severity", {"error", "warning"}, problems)
    check_unique_ids(value, "check_id", path, problems)


def validate_constraints(value: Any, problems: Problems) -> None:
    path = "$.constraints"
    if not check_list(value, path, problems):
        return
    keys = {"constraint_id", "kind", "text"}
    kinds = {"data", "compute", "time", "policy", "user", "other"}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_object(item, item_path, keys, keys, problems):
            continue
        check_id(item.get("constraint_id"), f"{item_path}.constraint_id", problems)
        check_enum(item.get("kind"), f"{item_path}.kind", kinds, problems)
        check_text(item.get("text"), f"{item_path}.text", problems)
    check_unique_ids(value, "constraint_id", path, problems)


def validate_strict_policy(value: Any, problems: Problems) -> None:
    path = "$.strict_policy"
    boolean_keys = {
        "require_lockfile",
        "require_container",
        "require_fixed_references",
        "require_cached_sources",
        "require_rerun",
    }
    keys = boolean_keys | {"numeric_tolerance"}
    if not check_object(value, path, keys, keys, problems):
        return
    for key in sorted(boolean_keys):
        if not isinstance(value.get(key), bool):
            problems.add(f"{path}.{key}", "must be a boolean")
    tolerance = value.get("numeric_tolerance")
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)) or tolerance < 0:
        problems.add(f"{path}.numeric_tolerance", "must be a non-negative number")


def validate_governance(value: Any, problems: Problems) -> None:
    path = "$.governance"
    risk_fields = {"human_subjects", "animals", "sensitive_data", "hazardous_materials"}
    keys = risk_fields | {"approvals", "restrictions"}
    if not check_object(value, path, keys, keys, problems):
        return
    for key in sorted(risk_fields):
        check_enum(
            value.get(key),
            f"{path}.{key}",
            {"yes", "no", "unknown", "not_applicable"},
            problems,
        )
    for key in ("approvals", "restrictions"):
        items = value.get(key)
        if not check_list(items, f"{path}.{key}", problems):
            continue
        for index, item in enumerate(items):
            check_text(item, f"{path}.{key}[{index}]", problems)
        if all(isinstance(item, str) for item in items) and len(items) != len(set(items)):
            problems.add(f"{path}.{key}", "must not contain duplicates")


def validate_extensions(value: Any, schema_version: Any, problems: Problems) -> None:
    path = "$.extensions"
    if not isinstance(value, dict):
        problems.add(path, "must be an object")
        return
    if schema_version == "1.1.0" and "profiles" not in value:
        problems.add(f"{path}.profiles", "is required in schema 1.1.0")
    if "profiles" not in value:
        return
    profiles = value["profiles"]
    if not isinstance(profiles, dict):
        problems.add(f"{path}.profiles", "must be an object keyed by profile ID")
        return
    for name, configuration in profiles.items():
        check_id(name, f"{path}.profiles.{name}", problems)
        if not isinstance(configuration, dict):
            problems.add(f"{path}.profiles.{name}", "must be an object")


def validate(data: Any) -> list[str]:
    problems = Problems()
    if not check_object(data, "$", TOP_REQUIRED, TOP_ALLOWED, problems):
        return problems.items

    schema_version = data.get("schema_version")
    if schema_version not in {"1.0.0", "1.1.0"}:
        problems.add("$.schema_version", "must equal '1.0.0' or '1.1.0'")
    if data.get("artifact_type") != "analysis_contract":
        problems.add("$.artifact_type", "must equal 'analysis_contract'")
    check_id(data.get("contract_id"), "$.contract_id", problems)
    assurance = validate_profile(data.get("profile"), problems)
    check_text(data.get("objective"), "$.objective", problems)
    validate_questions(data.get("questions"), problems)
    validate_inputs(data.get("inputs"), problems)
    validate_design(data.get("design"), schema_version, problems)
    validate_steps(data.get("steps"), problems)
    validate_outputs(data.get("required_outputs"), problems)
    validate_validation(data.get("validation"), problems)
    validate_constraints(data.get("constraints"), problems)

    audiences = data.get("audiences")
    if check_list(audiences, "$.audiences", problems, nonempty=True):
        for index, audience in enumerate(audiences):
            check_id(audience, f"$.audiences[{index}]", problems)
        if all(isinstance(audience, str) for audience in audiences) and len(audiences) != len(set(audiences)):
            problems.add("$.audiences", "must not contain duplicates")

    if schema_version == "1.1.0" and "governance" not in data:
        problems.add("$.governance", "is required in schema 1.1.0")
    if "governance" in data:
        validate_governance(data["governance"], problems)
    validate_extensions(data.get("extensions"), schema_version, problems)
    if assurance == "strict" and "strict_policy" not in data:
        problems.add("$.strict_policy", "is required when profile.assurance is 'strict'")
    if "strict_policy" in data:
        validate_strict_policy(data["strict_policy"], problems)
    return problems.items


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path, help="Path to analysis-contract.json")
    args = parser.parse_args()

    try:
        with args.contract.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read {args.contract}: {exc}", file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(f"INVALID analysis_contract ({len(errors)} error(s))", file=sys.stderr)
        return 1

    print(f"VALID analysis_contract: {args.contract}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
