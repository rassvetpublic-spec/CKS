#!/usr/bin/env python3
"""Рабочий контур знаний CKS.

Knowledge Runtime (рабочий контур знаний) нормализует объекты знаний,
строит производные индексы кластеров/тегов/статусов/проектов, формирует
динамические представления и Markdown-проекцию для Obsidian.

Контур не является SSOT (единым источником истины), не принимает решения
и не переводит объект в Canon автоматически.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


STATUS_ORDER = [
    "raw",
    "captured",
    "normalized",
    "deduplicated",
    "clustered",
    "researched",
    "understood",
    "connected",
    "validated",
    "knowledge",
    "canonical",
    "evolving",
    "disputed",
    "superseded",
    "archived",
    "rejected",
]

STATUS_RU = {
    "raw": "сырьё",
    "captured": "захвачено",
    "normalized": "нормализовано",
    "deduplicated": "очищено от дублей",
    "clustered": "сгруппировано",
    "researched": "исследовано",
    "understood": "понято",
    "connected": "связано",
    "validated": "проверено",
    "knowledge": "знание",
    "canonical": "каноническая основа",
    "evolving": "развивается",
    "disputed": "оспаривается",
    "superseded": "заменено",
    "archived": "архив",
    "rejected": "отклонено",
    "draft": "черновик",
    "review": "на проверке",
    "active": "активно",
}

COMPATIBLE_STATUSES = set(STATUS_ORDER) | {"draft", "review", "active"}

TYPE_RU = {
    "knowledge": "знание",
    "evidence": "доказательство",
    "decision": "решение",
    "proposal": "предложение",
    "rule": "правило",
    "process": "процесс",
    "experiment": "эксперимент",
    "idea": "идея",
    "question": "вопрос",
    "hypothesis": "гипотеза",
    "source": "источник",
    "observation": "наблюдение",
    "intuition": "интуиция",
    "cluster": "кластер",
    "project_view": "представление проекта",
}

PIPELINE_GROUPS = {
    "вход": {"raw", "captured"},
    "очистка": {"normalized", "deduplicated"},
    "осмысление": {"clustered", "researched", "understood", "connected", "validated"},
    "знания": {"knowledge", "evolving", "disputed"},
    "канон": {"canonical"},
    "история": {"superseded", "archived", "rejected"},
}


class KnowledgeRuntimeError(ValueError):
    """Ошибка рабочего контура знаний."""


def _unique_strings(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []
    return sorted({str(item).strip() for item in value if str(item).strip()})


def _slug(value: str) -> str:
    result = re.sub(r"[^0-9A-Za-zА-Яа-яЁё._-]+", "_", value.strip())
    return result.strip("_") or "объект"


def _yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


class KnowledgeRuntime:
    """Индексирует объекты знаний без изменения исходных записей."""

    def __init__(self, records: Iterable[dict[str, Any]] | None = None) -> None:
        self.records: dict[str, dict[str, Any]] = {}
        if records is not None:
            self.ingest(records)

    @staticmethod
    def normalize(record: dict[str, Any]) -> dict[str, Any]:
        result = dict(record)
        object_id = str(result.get("id") or "").strip()
        if not object_id:
            raise KnowledgeRuntimeError("Объект знания должен иметь id")
        result["id"] = object_id
        result["title"] = str(result.get("title") or result.get("name") or object_id).strip()
        result["type"] = str(result.get("type") or "knowledge").strip()
        result["status"] = str(result.get("status") or "raw").strip()
        result["owner"] = str(result.get("owner") or "unassigned").strip()
        result["lifecycle"] = str(result.get("lifecycle") or "development").strip()
        result["version"] = result.get("version", "1")
        result["clusters"] = _unique_strings(result.get("clusters"))
        result["tags"] = _unique_strings(result.get("tags"))
        result["projects"] = _unique_strings(result.get("projects") or result.get("project"))
        result["relations"] = list(result.get("relations") or [])
        result["evidence"] = list(result.get("evidence") or [])
        result["history"] = list(result.get("history") or [])
        result["signals"] = dict(result.get("signals") or {})
        if "confidence" in result and "confidence" not in result["signals"]:
            result["signals"]["confidence"] = result.get("confidence")
        if "intuition" in result and "intuition" not in result["signals"]:
            result["signals"]["intuition"] = result.get("intuition")
        result["obsidian"] = dict(result.get("obsidian") or {})
        return result

    @staticmethod
    def validate(record: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        if not str(record.get("id") or "").strip():
            errors.append("нет id")
        if not str(record.get("type") or "").strip():
            errors.append("нет type")
        status = str(record.get("status") or "")
        if status not in COMPATIBLE_STATUSES:
            errors.append(f"неизвестный status: {status}")
        for field in ("clusters", "tags", "projects", "relations", "evidence", "history"):
            if not isinstance(record.get(field), list):
                errors.append(f"{field} должен быть списком")
        signals = record.get("signals") or {}
        if not isinstance(signals, dict):
            errors.append("signals должен быть объектом")
        else:
            for field in ("confidence", "importance", "novelty", "uncertainty"):
                value = signals.get(field)
                if value is not None and (not isinstance(value, (int, float)) or not 0 <= float(value) <= 1):
                    errors.append(f"signals.{field} должен быть числом 0..1")
        return errors

    def ingest(self, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
        self.records = {}
        errors: dict[str, list[str]] = {}
        for raw in records:
            normalized = self.normalize(raw)
            object_errors = self.validate(normalized)
            if normalized["id"] in self.records:
                object_errors.append("дублирующий id")
            if object_errors:
                errors[normalized["id"]] = object_errors
            self.records[normalized["id"]] = normalized
        return {
            "status": "FAIL" if errors else "PASS",
            "objects": len(self.records),
            "errors": errors,
        }

    def _index(self, field: str) -> dict[str, list[str]]:
        index: dict[str, list[str]] = defaultdict(list)
        for object_id, record in self.records.items():
            value = record.get(field)
            values = value if isinstance(value, list) else [value]
            for item in values:
                if item is not None and str(item).strip():
                    index[str(item)].append(object_id)
        return {key: sorted(value) for key, value in sorted(index.items())}

    def dynamic_views(self) -> dict[str, Any]:
        status_index = self._index("status")
        confidence_bands: dict[str, list[str]] = {"низкая": [], "средняя": [], "высокая": [], "не задана": []}
        for object_id, record in self.records.items():
            confidence = (record.get("signals") or {}).get("confidence")
            if confidence is None:
                confidence_bands["не задана"].append(object_id)
            elif float(confidence) < 0.34:
                confidence_bands["низкая"].append(object_id)
            elif float(confidence) < 0.67:
                confidence_bands["средняя"].append(object_id)
            else:
                confidence_bands["высокая"].append(object_id)

        pipeline = {
            group: {
                "count": sum(len(status_index.get(status, [])) for status in statuses),
                "objects": sorted(
                    object_id
                    for status in statuses
                    for object_id in status_index.get(status, [])
                ),
            }
            for group, statuses in PIPELINE_GROUPS.items()
        }
        return {
            "schema_version": "1.0",
            "kind": "cks_dynamic_views",
            "authority": "derived_view_only",
            "objects": len(self.records),
            "по_статусам": status_index,
            "по_типам": self._index("type"),
            "по_кластерам": self._index("clusters"),
            "по_тегам": self._index("tags"),
            "по_проектам": self._index("projects"),
            "по_уверенности": confidence_bands,
            "путь_материал_в_знание": pipeline,
        }

    @staticmethod
    def relation_targets(record: dict[str, Any]) -> list[tuple[str, str]]:
        targets: list[tuple[str, str]] = []
        for relation in record.get("relations", []):
            if isinstance(relation, str):
                if relation.startswith("CKS-"):
                    targets.append((relation, "связано"))
                continue
            if not isinstance(relation, dict):
                continue
            target = str(relation.get("target") or relation.get("object_id") or "").strip()
            relation_type = str(relation.get("type") or relation.get("relation") or "связано").strip()
            if target:
                targets.append((target, relation_type))
        return targets

    def obsidian_markdown(self, record_or_id: str | dict[str, Any]) -> str:
        record = self.records[record_or_id] if isinstance(record_or_id, str) else self.normalize(record_or_id)
        signals = record.get("signals") or {}
        obsidian = record.get("obsidian") or {}
        aliases = _unique_strings(obsidian.get("aliases"))
        cssclasses = _unique_strings(obsidian.get("cssclasses"))
        lines = [
            "---",
            f"id: {_yaml_scalar(record['id'])}",
            f"type: {_yaml_scalar(record['type'])}",
            f"type_ru: {_yaml_scalar(TYPE_RU.get(record['type'], record['type']))}",
            f"status: {_yaml_scalar(record['status'])}",
            f"status_ru: {_yaml_scalar(STATUS_RU.get(record['status'], record['status']))}",
            f"version: {_yaml_scalar(str(record.get('version', '1')))}",
            f"owner: {_yaml_scalar(record.get('owner', 'unassigned'))}",
            "tags: " + json.dumps(record.get("tags", []), ensure_ascii=False),
            "clusters: " + json.dumps(record.get("clusters", []), ensure_ascii=False),
            "projects: " + json.dumps(record.get("projects", []), ensure_ascii=False),
            "aliases: " + json.dumps(aliases, ensure_ascii=False),
            "cssclasses: " + json.dumps(cssclasses, ensure_ascii=False),
        ]
        if signals.get("confidence") is not None:
            lines.append(f"confidence: {float(signals['confidence']):.3f}")
        lines.extend(["---", "", f"# {record['title']}", ""])

        intuition = signals.get("intuition")
        if intuition:
            lines.extend(["## Интуиция", ""])
            items = intuition if isinstance(intuition, list) else [intuition]
            lines.extend(f"- {item}" for item in items)
            lines.append("")

        targets = self.relation_targets(record)
        if targets:
            lines.extend(["## Связи", ""])
            for target, relation_type in targets:
                lines.append(f"- {relation_type}: [[{target}]]")
            lines.append("")

        evidence = record.get("evidence") or []
        if evidence:
            lines.extend(["## Доказательства", ""])
            for item in evidence:
                target = item if isinstance(item, str) else item.get("id") or item.get("reference")
                if target:
                    lines.append(f"- [[{target}]]")
            lines.append("")

        lines.extend([
            "## Состояние знания",
            "",
            f"- Стадия: **{STATUS_RU.get(record['status'], record['status'])}**",
            f"- Кластеры: {', '.join(record.get('clusters', [])) or 'не назначены'}",
            f"- Проекты-проекции: {', '.join(record.get('projects', [])) or 'не назначены'}",
            "",
            "> Это производное представление CKS для Obsidian. Оно не является SSOT и не меняет канон.",
            "",
        ])
        return "\n".join(lines)

    def export_obsidian(self, vault_root: str | Path) -> dict[str, Any]:
        root = Path(vault_root)
        knowledge_dir = root / "Знания"
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        written: list[str] = []
        for object_id, record in sorted(self.records.items()):
            target = knowledge_dir / f"{_slug(object_id)}.md"
            target.write_text(self.obsidian_markdown(record), encoding="utf-8")
            written.append(str(target.relative_to(root)))

        views = self.dynamic_views()
        overview = [
            "# CKS — обзор базы знаний",
            "",
            "> Производное представление для Obsidian. Источники истины остаются в CKS.",
            "",
            "## Путь от материала к знанию",
            "",
        ]
        for stage, payload in views["путь_материал_в_знание"].items():
            overview.append(f"- **{stage}**: {payload['count']}")
        overview.extend(["", "## Объекты", ""])
        for object_id in sorted(self.records):
            overview.append(f"- [[{object_id}]]")
        (root / "CKS_Обзор.md").write_text("\n".join(overview) + "\n", encoding="utf-8")
        written.append("CKS_Обзор.md")
        return {"status": "PASS", "written": written, "objects": len(self.records)}


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: рабочий контур знаний")
    parser.add_argument("input", help="JSON-массив объектов CKS")
    parser.add_argument("--views", help="Куда записать динамические представления JSON")
    parser.add_argument("--obsidian-dir", help="Каталог Obsidian Vault; может быть корнем Git-репозитория")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise SystemExit("Вход должен быть JSON-массивом объектов")
    runtime = KnowledgeRuntime()
    result = runtime.ingest(payload)
    views = runtime.dynamic_views()
    if args.views:
        target = Path(args.views)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(views, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    obsidian_result = runtime.export_obsidian(args.obsidian_dir) if args.obsidian_dir else None
    print(json.dumps({"validation": result, "views": views, "obsidian": obsidian_result}, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
