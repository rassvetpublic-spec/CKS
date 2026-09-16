#!/usr/bin/env python3
"""Аналитика знаний CKS.

Knowledge Intelligence (аналитика знаний) строит предложения скрытых связей,
кластеров, анализирует превращение материала в знание, формирует карту
развития проекта и диагностирует качество объектов.

Все результаты являются рекомендациями и производными представлениями.
Модуль не принимает Decision (решение) и не изменяет Canon (канон).
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

from cks_knowledge_runtime import KnowledgeRuntime, STATUS_ORDER, STATUS_RU


KNOWLEDGE_STATUSES = {"knowledge", "canonical", "evolving", "disputed", "superseded", "archived"}
EARLY_STATUSES = {"raw", "captured", "normalized", "deduplicated", "clustered", "researched", "understood", "connected", "validated"}


def _set(record: dict[str, Any], field: str) -> set[str]:
    value = record.get(field) or []
    if isinstance(value, str):
        value = [value]
    return {str(item).strip().lower() for item in value if str(item).strip()}


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 0.0
    union = left | right
    return len(left & right) / len(union) if union else 0.0


class KnowledgeIntelligence:
    def __init__(self, runtime: KnowledgeRuntime) -> None:
        self.runtime = runtime

    def hidden_links(self, *, threshold: float = 0.34) -> list[dict[str, Any]]:
        """Предложить потенциальные связи по общим кластерам и тегам."""
        ids = sorted(self.runtime.records)
        existing: set[tuple[str, str]] = set()
        for source_id, record in self.runtime.records.items():
            for target, _relation in self.runtime.relation_targets(record):
                existing.add(tuple(sorted((source_id, target))))

        suggestions: list[dict[str, Any]] = []
        for pos, left_id in enumerate(ids):
            left = self.runtime.records[left_id]
            for right_id in ids[pos + 1 :]:
                if (left_id, right_id) in existing or (right_id, left_id) in existing:
                    continue
                right = self.runtime.records[right_id]
                shared_clusters = sorted(_set(left, "clusters") & _set(right, "clusters"))
                shared_tags = sorted(_set(left, "tags") & _set(right, "tags"))
                cluster_score = _jaccard(_set(left, "clusters"), _set(right, "clusters"))
                tag_score = _jaccard(_set(left, "tags"), _set(right, "tags"))
                type_bonus = 0.05 if left.get("type") == right.get("type") else 0.0
                score = min(1.0, 0.55 * cluster_score + 0.4 * tag_score + type_bonus)
                if score < threshold:
                    continue
                reasons: list[str] = []
                if shared_clusters:
                    reasons.append("общие кластеры: " + ", ".join(shared_clusters))
                if shared_tags:
                    reasons.append("общие теги: " + ", ".join(shared_tags))
                if left.get("type") == right.get("type"):
                    reasons.append("одинаковый тип объекта")
                suggestions.append(
                    {
                        "source": left_id,
                        "target": right_id,
                        "score": round(score, 3),
                        "reason": reasons,
                        "authority": "suggestion_only",
                    }
                )
        return sorted(suggestions, key=lambda item: (-item["score"], item["source"], item["target"]))

    def cluster_suggestions(self, *, min_shared_tags: int = 2) -> list[dict[str, Any]]:
        """Выделить компоненты объектов с устойчивым совпадением тегов."""
        ids = sorted(self.runtime.records)
        adjacency: dict[str, set[str]] = {object_id: set() for object_id in ids}
        for pos, left_id in enumerate(ids):
            left_tags = _set(self.runtime.records[left_id], "tags")
            for right_id in ids[pos + 1 :]:
                shared = left_tags & _set(self.runtime.records[right_id], "tags")
                if len(shared) >= min_shared_tags:
                    adjacency[left_id].add(right_id)
                    adjacency[right_id].add(left_id)

        seen: set[str] = set()
        result: list[dict[str, Any]] = []
        number = 1
        for object_id in ids:
            if object_id in seen or not adjacency[object_id]:
                continue
            component: list[str] = []
            queue = deque([object_id])
            while queue:
                current = queue.popleft()
                if current in seen:
                    continue
                seen.add(current)
                component.append(current)
                queue.extend(sorted(adjacency[current] - seen))
            tags_counter: dict[str, int] = defaultdict(int)
            for member in component:
                for tag in _set(self.runtime.records[member], "tags"):
                    tags_counter[tag] += 1
            common = sorted(tag for tag, count in tags_counter.items() if count >= 2)
            result.append(
                {
                    "suggested_cluster": f"AUTO-CLUSTER-{number:03d}",
                    "objects": sorted(component),
                    "shared_tags": common,
                    "authority": "suggestion_only",
                }
            )
            number += 1
        return result

    @staticmethod
    def _history_statuses(record: dict[str, Any]) -> list[str]:
        statuses: list[str] = []
        for item in record.get("history", []):
            if isinstance(item, dict) and item.get("status"):
                statuses.append(str(item["status"]))
        return statuses

    def became_knowledge(self) -> list[dict[str, Any]]:
        """Показать, какие объекты прошли путь от ранних состояний к знанию."""
        result: list[dict[str, Any]] = []
        for object_id, record in sorted(self.runtime.records.items()):
            current = str(record.get("status"))
            history_statuses = self._history_statuses(record)
            reached_knowledge = current in KNOWLEDGE_STATUSES
            had_early_stage = any(status in EARLY_STATUSES for status in history_statuses)
            if reached_knowledge:
                result.append(
                    {
                        "id": object_id,
                        "title": record.get("title"),
                        "current_status": current,
                        "current_status_ru": STATUS_RU.get(current, current),
                        "had_early_stage": had_early_stage,
                        "status_path": history_statuses + ([current] if not history_statuses or history_statuses[-1] != current else []),
                        "evidence_count": len(record.get("evidence", [])),
                        "relation_count": len(record.get("relations", [])),
                        "clusters": record.get("clusters", []),
                    }
                )
        return result

    def project_evolution_map(self) -> dict[str, Any]:
        """Собрать карту развития проекта как проекции знаний."""
        projects: dict[str, dict[str, Any]] = {}
        for object_id, record in sorted(self.runtime.records.items()):
            for project in record.get("projects", []):
                state = projects.setdefault(
                    project,
                    {
                        "objects": [],
                        "status_counts": defaultdict(int),
                        "clusters": defaultdict(int),
                        "events": [],
                    },
                )
                state["objects"].append(object_id)
                state["status_counts"][record["status"]] += 1
                for cluster in record.get("clusters", []):
                    state["clusters"][cluster] += 1
                for event in record.get("history", []):
                    if isinstance(event, dict):
                        state["events"].append(
                            {
                                "object_id": object_id,
                                "timestamp": event.get("timestamp"),
                                "status": event.get("status"),
                                "reason": event.get("reason"),
                            }
                        )

        normalized: dict[str, Any] = {}
        for project, state in sorted(projects.items()):
            status_counts = dict(sorted(state["status_counts"].items(), key=lambda item: STATUS_ORDER.index(item[0]) if item[0] in STATUS_ORDER else 999))
            events = sorted(state["events"], key=lambda item: (str(item.get("timestamp") or ""), item["object_id"]))
            normalized[project] = {
                "objects": sorted(state["objects"]),
                "status_counts": status_counts,
                "clusters": dict(sorted(state["clusters"].items(), key=lambda item: (-item[1], item[0]))),
                "events": events,
            }
        return {"authority": "derived_view_only", "projects": normalized}

    def quality_audit(self) -> dict[str, Any]:
        """Диагностировать качество знаний без автоматического принятия решений."""
        objects: list[dict[str, Any]] = []
        for object_id, record in sorted(self.runtime.records.items()):
            warnings: list[str] = []
            completeness_fields = ["title", "type", "status", "owner", "lifecycle"]
            completeness = sum(bool(record.get(field)) for field in completeness_fields) / len(completeness_fields)
            evidence_score = min(1.0, len(record.get("evidence", [])) / 2)
            connectivity_score = min(1.0, len(record.get("relations", [])) / 3)
            classification_score = min(1.0, (len(record.get("clusters", [])) + len(record.get("tags", []))) / 4)
            history_score = min(1.0, len(record.get("history", [])) / 2)
            total = round(
                100
                * (
                    0.25 * completeness
                    + 0.25 * evidence_score
                    + 0.2 * connectivity_score
                    + 0.15 * classification_score
                    + 0.15 * history_score
                ),
                1,
            )
            if not record.get("clusters"):
                warnings.append("нет кластера")
            if not record.get("tags"):
                warnings.append("нет тегов")
            if record.get("status") in {"validated", "knowledge", "canonical", "evolving"} and not record.get("evidence"):
                warnings.append("зрелый объект без доказательств")
            if record.get("status") == "canonical" and not record.get("history"):
                warnings.append("канонический объект без истории")
            if not record.get("relations"):
                warnings.append("изолированный объект")
            objects.append(
                {
                    "id": object_id,
                    "score": total,
                    "warnings": warnings,
                    "authority": "diagnostic_only",
                }
            )

        average = round(sum(item["score"] for item in objects) / len(objects), 1) if objects else 0.0
        return {
            "status": "WARN" if any(item["warnings"] for item in objects) else "PASS",
            "average_score": average,
            "objects": objects,
            "authority": "diagnostic_only",
        }

    def full_report(self, *, link_threshold: float = 0.34) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "kind": "cks_knowledge_intelligence",
            "authority": "analysis_and_suggestions_only",
            "скрытые_связи": self.hidden_links(threshold=link_threshold),
            "новые_кластеры": self.cluster_suggestions(),
            "что_стало_знанием": self.became_knowledge(),
            "карта_развития_проекта": self.project_evolution_map(),
            "самоаудит_качества": self.quality_audit(),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: аналитика знаний")
    parser.add_argument("input", help="JSON-массив объектов CKS")
    parser.add_argument("--output", help="Куда записать аналитический отчёт JSON")
    parser.add_argument("--link-threshold", type=float, default=0.34, help="Порог предложения скрытой связи 0..1")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise SystemExit("Вход должен быть JSON-массивом объектов")
    runtime = KnowledgeRuntime()
    validation = runtime.ingest(payload)
    intelligence = KnowledgeIntelligence(runtime)
    report = intelligence.full_report(link_threshold=args.link_threshold)
    result = {"validation": validation, "report": report}
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    print(text, end="")
    return 1 if validation["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
