#!/usr/bin/env python3
"""Динамические представления знаний CKS.

Модуль строит производные виды поверх существующего KnowledgeRuntime
(рабочего контура знаний). Он не является SSOT (единым источником истины),
не принимает решения и не изменяет Canon (канон).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_knowledge_runtime import KnowledgeRuntime, PIPELINE_GROUPS, STATUS_ORDER, STATUS_RU


MATURE_STATUSES = {"validated", "knowledge", "canonical", "evolving", "disputed"}


class DynamicKnowledgeViews:
    """Строит русскоязычные производные представления базы знаний."""

    def __init__(self, runtime: KnowledgeRuntime) -> None:
        self.runtime = runtime

    @staticmethod
    def _history_events(record: dict[str, Any]) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        for item in record.get("history", []):
            if isinstance(item, dict):
                events.append(item)
        return events

    @staticmethod
    def _month(timestamp: Any) -> str | None:
        value = str(timestamp or "").strip()
        if len(value) >= 7 and value[4] == "-" and value[7 - 1] != "":
            return value[:7]
        return None

    def timeline(self) -> dict[str, Any]:
        by_month: dict[str, set[str]] = defaultdict(set)
        events: list[dict[str, Any]] = []
        without_date: list[str] = []

        for object_id, record in sorted(self.runtime.records.items()):
            object_has_date = False
            for event in self._history_events(record):
                timestamp = event.get("timestamp")
                month = self._month(timestamp)
                if month:
                    by_month[month].add(object_id)
                    object_has_date = True
                events.append(
                    {
                        "object_id": object_id,
                        "timestamp": timestamp,
                        "status": event.get("status"),
                        "status_ru": STATUS_RU.get(str(event.get("status") or ""), event.get("status")),
                        "reason": event.get("reason"),
                    }
                )
            for field in ("created_at", "updated_at"):
                month = self._month(record.get(field))
                if month:
                    by_month[month].add(object_id)
                    object_has_date = True
            if not object_has_date:
                without_date.append(object_id)

        events.sort(key=lambda item: (str(item.get("timestamp") or ""), item["object_id"]))
        return {
            "по_месяцам": {key: sorted(value) for key, value in sorted(by_month.items())},
            "лента_событий": events,
            "без_даты": sorted(without_date),
        }

    def connectivity(self) -> dict[str, Any]:
        incoming: dict[str, int] = defaultdict(int)
        outgoing: dict[str, int] = defaultdict(int)
        existing = set(self.runtime.records)

        for source_id, record in self.runtime.records.items():
            targets: set[str] = set()
            for target_id, _relation in self.runtime.relation_targets(record):
                if target_id in existing:
                    targets.add(target_id)
            for evidence in record.get("evidence", []):
                target_id = evidence if isinstance(evidence, str) else evidence.get("id") or evidence.get("reference")
                if target_id and str(target_id) in existing:
                    targets.add(str(target_id))
            outgoing[source_id] = len(targets)
            for target_id in targets:
                incoming[target_id] += 1

        groups: dict[str, list[str]] = {"изолированные": [], "слабосвязанные": [], "связанные": [], "узлы_хабы": []}
        details: dict[str, Any] = {}
        for object_id in sorted(self.runtime.records):
            total = incoming[object_id] + outgoing[object_id]
            if total == 0:
                group = "изолированные"
            elif total <= 2:
                group = "слабосвязанные"
            elif total <= 5:
                group = "связанные"
            else:
                group = "узлы_хабы"
            groups[group].append(object_id)
            details[object_id] = {
                "входящих": incoming[object_id],
                "исходящих": outgoing[object_id],
                "всего": total,
                "группа": group,
            }
        return {"группы": groups, "объекты": details}

    def problems(self) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {
            "без_кластеров": [],
            "без_тегов": [],
            "без_связей": [],
            "зрелые_без_доказательств": [],
            "оспариваемые": [],
            "битые_ссылки": [],
        }
        existing = set(self.runtime.records)
        for object_id, record in sorted(self.runtime.records.items()):
            if not record.get("clusters"):
                result["без_кластеров"].append(object_id)
            if not record.get("tags"):
                result["без_тегов"].append(object_id)
            if not record.get("relations") and not record.get("evidence"):
                result["без_связей"].append(object_id)
            if record.get("status") in MATURE_STATUSES and not record.get("evidence"):
                result["зрелые_без_доказательств"].append(object_id)
            if record.get("status") == "disputed":
                result["оспариваемые"].append(object_id)

            missing: set[str] = set()
            for target_id, _relation in self.runtime.relation_targets(record):
                if target_id not in existing:
                    missing.add(target_id)
            for evidence in record.get("evidence", []):
                target_id = evidence if isinstance(evidence, str) else evidence.get("id") or evidence.get("reference")
                if target_id and str(target_id) not in existing:
                    missing.add(str(target_id))
            for target_id in sorted(missing):
                result["битые_ссылки"].append(f"{object_id} -> {target_id}")
        return result

    def provenance(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for object_id, record in sorted(self.runtime.records.items()):
            evidence_ids: list[str] = []
            for item in record.get("evidence", []):
                target = item if isinstance(item, str) else item.get("id") or item.get("reference")
                if target:
                    evidence_ids.append(str(target))
            relations = [
                {"target": target, "type": relation_type}
                for target, relation_type in self.runtime.relation_targets(record)
            ]
            result[object_id] = {
                "source": record.get("source"),
                "evidence": sorted(set(evidence_ids)),
                "relations": relations,
                "traceability": record.get("traceability") or [],
                "history_events": len(self._history_events(record)),
            }
        return result

    def knowledge_funnel(self) -> dict[str, Any]:
        status_index = self.runtime._index("status")
        stages: dict[str, Any] = {}
        total = len(self.runtime.records)
        for stage, statuses in PIPELINE_GROUPS.items():
            object_ids = sorted(
                object_id
                for status in statuses
                for object_id in status_index.get(status, [])
            )
            stages[stage] = {
                "count": len(object_ids),
                "share": round(len(object_ids) / total, 4) if total else 0.0,
                "objects": object_ids,
            }
        knowledge_count = stages.get("знания", {}).get("count", 0) + stages.get("канон", {}).get("count", 0)
        input_count = stages.get("вход", {}).get("count", 0)
        return {
            "objects_total": total,
            "stages": stages,
            "knowledge_or_canon": knowledge_count,
            "input": input_count,
            "knowledge_share": round(knowledge_count / total, 4) if total else 0.0,
        }

    def project_projections(self) -> dict[str, Any]:
        projects: dict[str, dict[str, Any]] = {}
        for object_id, record in sorted(self.runtime.records.items()):
            for project in record.get("projects", []):
                item = projects.setdefault(project, {"objects": [], "statuses": defaultdict(list), "clusters": defaultdict(list)})
                item["objects"].append(object_id)
                item["statuses"][record.get("status", "raw")].append(object_id)
                for cluster in record.get("clusters", []):
                    item["clusters"][cluster].append(object_id)

        normalized: dict[str, Any] = {}
        for project, item in sorted(projects.items()):
            normalized[project] = {
                "objects": sorted(item["objects"]),
                "по_статусам": {
                    status: sorted(ids)
                    for status, ids in sorted(
                        item["statuses"].items(),
                        key=lambda pair: STATUS_ORDER.index(pair[0]) if pair[0] in STATUS_ORDER else 999,
                    )
                },
                "по_кластерам": {cluster: sorted(ids) for cluster, ids in sorted(item["clusters"].items())},
            }
        return normalized

    def full_views(self) -> dict[str, Any]:
        base = self.runtime.dynamic_views()
        base.update(
            {
                "по_времени": self.timeline(),
                "по_связности": self.connectivity(),
                "по_проблемам": self.problems(),
                "по_происхождению": self.provenance(),
                "воронка_материал_в_знание": self.knowledge_funnel(),
                "проекты_как_проекции": self.project_projections(),
            }
        )
        base["schema_version"] = "1.1"
        base["authority"] = "derived_view_only"
        return base


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: динамические представления знаний")
    parser.add_argument("input", help="JSON-массив объектов CKS")
    parser.add_argument("--output", required=True, help="Файл JSON для производных представлений")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise SystemExit("Вход должен быть JSON-массивом объектов")

    runtime = KnowledgeRuntime()
    validation = runtime.ingest(payload)
    if validation["status"] == "FAIL":
        print(json.dumps({"validation": validation}, ensure_ascii=False, indent=2))
        return 1

    views = DynamicKnowledgeViews(runtime).full_views()
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(views, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"validation": validation, "views": views}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
