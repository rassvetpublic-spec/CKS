#!/usr/bin/env python3
"""Dependency-free JSON Schema subset validator used by CKS CI.

Supports the keywords currently used by CKS schemas: type, const, required,
properties, enum, pattern, items, oneOf, uniqueItems, minimum, maximum and
additionalProperties=false.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def validate_instance(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []

    if "oneOf" in schema:
        matches = 0
        candidate_errors: list[list[str]] = []
        for candidate in schema["oneOf"]:
            current = validate_instance(value, candidate, path)
            candidate_errors.append(current)
            if not current:
                matches += 1
        if matches != 1:
            errors.append(f"{path}: oneOf matched {matches} schemas, expected exactly 1")
        return errors

    expected = schema.get("type")
    if expected is not None:
        expected_types = expected if isinstance(expected, list) else [expected]
        if not any(_type_matches(value, item) for item in expected_types):
            errors.append(f"{path}: expected type {expected_types}, got {type(value).__name__}")
            return errors

    if "const" in schema and (value != schema["const"] or (isinstance(value, bool) != isinstance(schema["const"], bool))):
        errors.append(f"{path}: value {value!r} does not match const {schema['const']!r}")

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} is not in enum")

    if isinstance(value, str) and schema.get("pattern"):
        if re.search(str(schema["pattern"]), value) is None:
            errors.append(f"{path}: string does not match pattern {schema['pattern']!r}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value above maximum {schema['maximum']}")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required if isinstance(required, list) else []:
            if key not in value:
                errors.append(f"{path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, child in properties.items():
                if key in value and isinstance(child, dict):
                    errors.extend(validate_instance(value[key], child, f"{path}.{key}"))
            if schema.get("additionalProperties") is False:
                for key in value:
                    if key not in properties:
                        errors.append(f"{path}: additional property {key!r} is not allowed")

    if isinstance(value, list):
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                errors.append(f"{path}: array items must be unique")
        items = schema.get("items")
        if isinstance(items, dict):
            for index, item in enumerate(value):
                errors.extend(validate_instance(item, items, f"{path}[{index}]"))

    return errors


def validate_file(schema_path: Path, instance_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        return [f"{schema_path}: schema root must be an object"]
    instance = json.loads(instance_path.read_text(encoding="utf-8"))
    return validate_instance(instance, schema)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate JSON instances against the CKS JSON Schema subset")
    parser.add_argument("--schema", required=True)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    schema_path = Path(args.schema)
    failures = 0
    for raw in args.files:
        path = Path(raw)
        try:
            errors = validate_file(schema_path, path)
        except Exception as exc:
            errors = [f"{path}: {exc.__class__.__name__}: {exc}"]
        if errors:
            failures += 1
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
