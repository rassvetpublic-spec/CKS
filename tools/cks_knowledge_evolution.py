#!/usr/bin/env python3
"""Эволюция, миграция и восстановление объектов знаний CKS.

Модуль работает только с копиями данных и не меняет SSOT, Decision (решение)
или Canon (канон) автоматически. Он предоставляет проверяемые операции:
- нормализация и миграция старых объектов к текущей модели runtime;
- управляемый переход состояния через действующую машину состояний;
- детерминированные snapshot (снимки) с SHA-256;
- сравнение наборов объектов;
- проверка и восстановление snapshot с повторной валидацией runtime.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from cks_knowledge_runtime import KnowledgeRuntime
from cks_knowledge_state_machine import canonical_status, validate_record_transition

SNAPSHOT_SCHEMA_VERSION = "1.0"


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest_payload(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _evidence_ref(item: Any) -> str | None:
    if isinstance(item, str):
        value = item.strip()
        return value or None
    if isinstance(item, dict):
        value = str(item.get("id") or item.get("reference") or item.get("target") or "").strip()
        return value or None
    return None


def _field_diff(old: dict[str, Any], new: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for field in sorted(set(old) | set(new)):
        before = old.get(field)
        after = new.get(field)
        if before != after:
            result.append({"field": field, "before": copy.deepcopy(before), "after": copy.deepcopy(after)})
    return result


class KnowledgeEvolutionError(ValueError):
    """Ошибка миграции, эволюции или восстановления знания."""


class KnowledgeEvolution:
    """Безопасные операции жизненного цикла поверх KnowledgeRuntime."""

    @staticmethod
    def migrate_record(record: dict[str, Any]) -> dict[str, Any]:
        """Нормализовать старую запись без изменения входного объекта.

        Совместимые старые статусы draft/review/active переводятся в их
        канонические runtime-статусы. Сам переход не означает принятие в Canon.
        """
        source = copy.deepcopy(record)
        migrated = KnowledgeRuntime.normalize(source)
        previous_status = migrated.get("status")
        migrated["status"] = canonical_status(previous_status)

        # Нормализатор уже переносит старые confidence/intuition в signals.
        # После переноса удаляем дублирующие верхнеуровневые поля, чтобы
        # повторная миграция давала тот же результат.
        if "confidence" in migrated:
            migrated.pop("confidence", None)
        if "intuition" in migrated:
            migrated.pop("intuition", None)

        errors = KnowledgeRuntime.validate(migrated)
        changes = _field_diff(source, migrated)
        return {
            "status": "FAIL" if errors else "PASS",
            "record": migrated,
            "errors": errors,
            "changes": changes,
            "legacy_status_mapped": str(previous_status) != str(migrated.get("status")),
            "authority": "migration_only",
        }

    @classmethod
    def migrate_records(cls, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
        migrated: list[dict[str, Any]] = []
        errors: dict[str, list[str]] = {}
        changes: dict[str, list[dict[str, Any]]] = {}

        for raw in records:
            result = cls.migrate_record(raw)
            record = result["record"]
            object_id = str(record.get("id") or "<missing-id>")
            migrated.append(record)
            if result["errors"]:
                errors[object_id] = list(result["errors"])
            if result["changes"]:
                changes[object_id] = result["changes"]

        runtime = KnowledgeRuntime()
        validation = runtime.ingest(migrated)
        for object_id, object_errors in validation["errors"].items():
            errors.setdefault(object_id, []).extend(
                item for item in object_errors if item not in errors.get(object_id, [])
            )

        return {
            "status": "FAIL" if errors else "PASS",
            "records": [copy.deepcopy(runtime.records[key]) for key in sorted(runtime.records)],
            "errors": errors,
            "changes": changes,
            "authority": "migration_only",
        }

    @staticmethod
    def evolve_record(
        record: dict[str, Any],
        target_status: str,
        *,
        reason: str | None = None,
        changed_by: str = "unknown",
        timestamp: str | None = None,
        new_version: str | int | None = None,
    ) -> dict[str, Any]:
        """Создать новую версию записи после разрешённого перехода состояния."""
        source = KnowledgeRuntime.normalize(copy.deepcopy(record))
        source["status"] = canonical_status(source.get("status"))
        validation = validate_record_transition(source, target_status, reason=reason)
        if validation["status"] != "PASS":
            return {
                "status": "FAIL",
                "record": source,
                "validation": validation,
                "authority": "validated_transition_only",
            }

        target = canonical_status(target_status)
        evolved = copy.deepcopy(source)
        previous_status = evolved["status"]
        previous_version = evolved.get("version", "1")
        evolved["status"] = target
        if new_version is not None:
            evolved["version"] = new_version

        event: dict[str, Any] = {
            "status": target,
            "from_status": previous_status,
            "changed_by": str(changed_by or "unknown"),
        }
        if reason:
            event["reason"] = reason
        if timestamp:
            event["timestamp"] = timestamp
        if new_version is not None:
            event["from_version"] = previous_version
            event["version"] = new_version

        evolved.setdefault("history", [])
        evolved["history"] = copy.deepcopy(evolved["history"])
        evolved["history"].append(event)

        errors = KnowledgeRuntime.validate(evolved)
        return {
            "status": "FAIL" if errors else "PASS",
            "record": evolved,
            "validation": validation,
            "errors": errors,
            "authority": "validated_transition_only",
        }

    @staticmethod
    def create_snapshot(runtime: KnowledgeRuntime, *, label: str | None = None) -> dict[str, Any]:
        """Создать детерминированный снимок текущего runtime."""
        records = [copy.deepcopy(runtime.records[key]) for key in sorted(runtime.records)]
        payload: dict[str, Any] = {
            "schema_version": SNAPSHOT_SCHEMA_VERSION,
            "kind": "cks_knowledge_snapshot",
            "records": records,
        }
        if label:
            payload["label"] = str(label)
        digest = _digest_payload(payload)
        return {
            **payload,
            "sha256": digest,
            "authority": "recovery_artifact_only",
        }

    @staticmethod
    def verify_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
        errors: list[str] = []
        if snapshot.get("kind") != "cks_knowledge_snapshot":
            errors.append("неверный kind snapshot")
        if snapshot.get("schema_version") != SNAPSHOT_SCHEMA_VERSION:
            errors.append("неподдерживаемая schema_version snapshot")
        if not isinstance(snapshot.get("records"), list):
            errors.append("records snapshot должен быть списком")

        expected = str(snapshot.get("sha256") or "").strip()
        if not expected:
            errors.append("нет sha256 snapshot")
        else:
            payload = {
                key: copy.deepcopy(value)
                for key, value in snapshot.items()
                if key not in {"sha256", "authority"}
            }
            actual = _digest_payload(payload)
            if actual != expected:
                errors.append("sha256 snapshot не совпадает с содержимым")

        return {
            "status": "FAIL" if errors else "PASS",
            "errors": errors,
            "authority": "verification_only",
        }

    @classmethod
    def recover_snapshot(cls, snapshot: dict[str, Any]) -> dict[str, Any]:
        """Проверить снимок и восстановить новый изолированный runtime."""
        verification = cls.verify_snapshot(snapshot)
        if verification["status"] != "PASS":
            return {
                "status": "FAIL",
                "verification": verification,
                "runtime": None,
                "errors": list(verification["errors"]),
                "authority": "recovery_only",
            }

        runtime = KnowledgeRuntime()
        validation = runtime.ingest(copy.deepcopy(snapshot["records"]))
        if validation["status"] != "PASS":
            return {
                "status": "FAIL",
                "verification": verification,
                "runtime": None,
                "errors": validation["errors"],
                "authority": "recovery_only",
            }

        return {
            "status": "PASS",
            "verification": verification,
            "runtime": runtime,
            "records": [copy.deepcopy(runtime.records[key]) for key in sorted(runtime.records)],
            "errors": {},
            "authority": "recovery_only",
        }

    @staticmethod
    def compare_record_sets(
        old_records: Iterable[dict[str, Any]],
        new_records: Iterable[dict[str, Any]],
    ) -> dict[str, Any]:
        """Сравнить два набора знаний по стабильным id."""
        old_map = {str(item.get("id")): copy.deepcopy(item) for item in old_records}
        new_map = {str(item.get("id")): copy.deepcopy(item) for item in new_records}
        old_ids = set(old_map)
        new_ids = set(new_map)

        added = sorted(new_ids - old_ids)
        removed = sorted(old_ids - new_ids)
        changed: list[dict[str, Any]] = []
        for object_id in sorted(old_ids & new_ids):
            fields = _field_diff(old_map[object_id], new_map[object_id])
            if fields:
                changed.append({"id": object_id, "fields": fields})

        return {
            "status": "CHANGED" if added or removed or changed else "UNCHANGED",
            "added": added,
            "removed": removed,
            "changed": changed,
            "authority": "diff_only",
        }

    @staticmethod
    def evidence_references(record: dict[str, Any]) -> list[str]:
        """Нормализовать явные evidence-ссылки для проверок миграции/восстановления."""
        refs = {_evidence_ref(item) for item in record.get("evidence", [])}
        return sorted(ref for ref in refs if ref)


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: миграция и восстановление знаний")
    sub = parser.add_subparsers(dest="command", required=True)

    migrate = sub.add_parser("migrate", help="Нормализовать JSON-массив объектов")
    migrate.add_argument("input")
    migrate.add_argument("--output")

    verify = sub.add_parser("verify-snapshot", help="Проверить snapshot JSON")
    verify.add_argument("input")

    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))

    if args.command == "migrate":
        if not isinstance(payload, list):
            raise SystemExit("Вход migrate должен быть JSON-массивом")
        result = KnowledgeEvolution.migrate_records(payload)
        text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            target = Path(args.output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        print(text, end="")
        return 1 if result["status"] == "FAIL" else 0

    if not isinstance(payload, dict):
        raise SystemExit("Snapshot должен быть JSON-объектом")
    result = KnowledgeEvolution.verify_snapshot(payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
