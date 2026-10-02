#!/usr/bin/env python3
"""Capture hashed input/artifact records and local runtime versions as JSON."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import mimetypes
import platform
import re
import sys
from pathlib import Path
from typing import Any


ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
ARTIFACT_KINDS = {
    "table",
    "figure",
    "model",
    "data",
    "report",
    "log",
    "cache",
    "lockfile",
    "reference",
    "other",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_id(value: str, label: str) -> None:
    if not ID_RE.fullmatch(value):
        raise ValueError(f"{label} {value!r} is not a valid artifact ID")


def resolve_file(raw_path: str, root: Path) -> Path:
    candidate = Path(raw_path).expanduser()
    candidate = candidate if candidate.is_absolute() else root / candidate
    candidate = candidate.resolve()
    if not candidate.is_file():
        raise ValueError(f"file does not exist: {candidate}")
    return candidate


def portable_uri(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def media_type(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(path.name)
    return guessed or "application/octet-stream"


def file_facts(path: Path, root: Path) -> dict[str, Any]:
    return {
        "locator_kind": "file",
        "uri": portable_uri(path, root),
        "media_type": media_type(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def reject_duplicate_ids(items: list[dict[str, Any]], key: str) -> None:
    seen: set[str] = set()
    for item in items:
        value = item[key]
        if value in seen:
            raise ValueError(f"duplicate {key}: {value!r}")
        seen.add(value)


def build_fragment(args: argparse.Namespace) -> dict[str, Any]:
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"root is not a directory: {root}")

    inputs: list[dict[str, Any]] = []
    for input_id, contract_input_id, raw_path in args.input or []:
        validate_id(input_id, "input_id")
        validate_id(contract_input_id, "contract_input_id")
        path = resolve_file(raw_path, root)
        inputs.append(
            {
                "input_id": input_id,
                "contract_input_id": contract_input_id,
                **file_facts(path, root),
            }
        )

    artifacts: list[dict[str, Any]] = []
    for artifact_id, output_id, kind, raw_path in args.artifact or []:
        validate_id(artifact_id, "artifact_id")
        if output_id != "-":
            validate_id(output_id, "output_id")
        if kind not in ARTIFACT_KINDS:
            raise ValueError(f"artifact kind {kind!r} must be one of {sorted(ARTIFACT_KINDS)}")
        path = resolve_file(raw_path, root)
        facts = file_facts(path, root)
        item: dict[str, Any] = {
            "artifact_id": artifact_id,
            "kind": kind,
            "status": "produced" if facts["size_bytes"] > 0 else "empty",
            **facts,
        }
        if output_id != "-":
            item["output_id"] = output_id
        artifacts.append(item)

    reject_duplicate_ids(inputs, "input_id")
    reject_duplicate_ids(artifacts, "artifact_id")
    inputs.sort(key=lambda item: item["input_id"])
    artifacts.sort(key=lambda item: item["artifact_id"])

    runtimes = [{"name": "Python", "version": platform.python_version()}]
    for name, version in args.runtime or []:
        if not name.strip() or not version.strip():
            raise ValueError("runtime name and version must be non-empty")
        runtimes.append({"name": name, "version": version})
    runtime_names = [item["name"].casefold() for item in runtimes]
    if len(runtime_names) != len(set(runtime_names)):
        raise ValueError("duplicate runtime name")
    runtimes.sort(key=lambda item: item["name"].casefold())

    packages: list[dict[str, str]] = []
    for name in sorted(set(args.package or []), key=str.casefold):
        try:
            version = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError as exc:
            raise ValueError(f"installed package not found: {name}") from exc
        packages.append({"name": name, "version": version})

    return {
        "inputs": inputs,
        "environment": {"runtimes": runtimes, "packages": packages},
        "artifacts": artifacts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root used to resolve and relativize paths")
    parser.add_argument(
        "--input",
        nargs=3,
        action="append",
        metavar=("INPUT_ID", "CONTRACT_INPUT_ID", "PATH"),
        help="Capture an input; repeat as needed",
    )
    parser.add_argument(
        "--artifact",
        nargs=4,
        action="append",
        metavar=("ARTIFACT_ID", "OUTPUT_ID_OR_DASH", "KIND", "PATH"),
        help="Capture an artifact; use '-' when it has no contract output ID",
    )
    parser.add_argument("--runtime", nargs=2, action="append", metavar=("NAME", "VERSION"))
    parser.add_argument("--package", action="append", help="Capture an installed Python distribution version")
    parser.add_argument("--output", type=Path, help="Write JSON here instead of stdout")
    args = parser.parse_args()

    try:
        fragment = build_fragment(args)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(fragment, indent=2, sort_keys=True) + "\n"
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: cannot write {args.output}: {exc}", file=sys.stderr)
            return 2
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
