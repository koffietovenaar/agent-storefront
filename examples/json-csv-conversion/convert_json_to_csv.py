"""Convert a JSON array to CSV using a small declarative mapping."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


TRANSFORMS = {"identity", "lower", "decimal_2", "boolean", "join_pipe"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def deep_get(record: dict[str, Any], dotted_path: str, default: Any = "") -> Any:
    value: Any = record
    for part in dotted_path.split("."):
        if not isinstance(value, dict) or part not in value:
            return default
        value = value[part]
    return value


def transform(value: Any, name: str) -> str:
    if name not in TRANSFORMS:
        raise ValueError(f"unsupported transform: {name}")
    if name == "lower":
        return str(value).lower()
    if name == "decimal_2":
        return f"{float(value):.2f}"
    if name == "boolean":
        if not isinstance(value, bool):
            raise ValueError("boolean transform requires a JSON boolean")
        return "true" if value else "false"
    if name == "join_pipe":
        if not isinstance(value, list):
            raise ValueError("join_pipe transform requires a JSON array")
        return "|".join(str(item) for item in value)
    return str(value)


def convert(
    input_path: Path,
    mapping_path: Path,
    output_path: Path,
    manifest_path: Path,
) -> dict[str, Any]:
    records = json.loads(input_path.read_text(encoding="utf-8"))
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    if not isinstance(records, list) or not all(
        isinstance(record, dict) for record in records
    ):
        raise ValueError("input must be a JSON array of objects")

    fields = mapping.get("fields")
    if not isinstance(fields, list) or not fields:
        raise ValueError("mapping.fields must be a non-empty array")
    columns = [str(field["column"]) for field in fields]
    if len(columns) != len(set(columns)):
        raise ValueError("mapping columns must be unique")

    rows: list[dict[str, str]] = []
    empty_cells = 0
    for record in records:
        row: dict[str, str] = {}
        for field in fields:
            default = field.get("default", "")
            value = deep_get(record, str(field["path"]), default)
            rendered = transform(value, str(field.get("transform", "identity")))
            row[str(field["column"])] = rendered
            empty_cells += rendered == ""
        rows.append(row)

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    manifest = {
        "format": "koffie-labs-conversion-reconciliation/v1",
        "input_rows": len(records),
        "output_rows": len(rows),
        "mapped_columns": columns,
        "mapped_column_count": len(columns),
        "empty_output_cells": empty_cells,
        "unaccounted_rows": len(records) - len(rows),
        "sha256": {
            "input.json": sha256(input_path),
            "mapping.json": sha256(mapping_path),
            "output.csv": sha256(output_path),
        },
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Convert a JSON array to CSV with deterministic reconciliation."
    )
    result.add_argument("input", type=Path)
    result.add_argument("mapping", type=Path)
    result.add_argument("output", type=Path)
    result.add_argument("--manifest", type=Path, default=Path("reconciliation.json"))
    return result


def main() -> int:
    args = parser().parse_args()
    manifest = convert(args.input, args.mapping, args.output, args.manifest)
    print(
        f"Converted {manifest['input_rows']} rows into "
        f"{manifest['mapped_column_count']} columns; "
        f"{manifest['unaccounted_rows']} unaccounted rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
