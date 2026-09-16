#!/usr/bin/env python3
"""Аналитика структуры знаний CKS.

Knowledge Intelligence (аналитика знаний) строит предложения скрытых связей
и кластеров, анализирует превращение материала в знание, структуру графа,
слабую связность, явные конфликты и сигналы уверенности/новизны.

Все результаты являются рекомендациями и производными представлениями.
Модуль не принимает Decision (решение), не изменяет Canon (канон) и не
мутирует объекты рабочего контура.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

from cks_knowledge_runtime import KnowledgeRuntime, STATUS_ORDER, STATUS_RU


KNOWLEDGE_STATUSES = {"knowledge", "canonical", "evolving", "disputed", "superseded", "archived"}
EARLY_STATUSES = {
    "raw",
    "captured",
    "normalized",
    "deduplicated",
    "clustered",
    "researched",
    "understood",
    "connected",
    "validated",
}
CONFLICT_RELATIONS = {
    "conflicts_with",
    "contradicts",
    "contradicted_by",
    "disputes",
    "disputed_by",
    "in_conflict_with",
}
SIGNAL_FIELDS = ("confidence", "novelty", "uncertainty", "importance")


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


def _relation_name(value: Any) -> str:
    return str(value or "related_to").strip().lower()


class KnowledgeIntelligence:
    def __init__(self, runtime: KnowledgeRuntime) -> None:
        self.runtime = runtime

    def _graph(self) -> tuple[dict[str, set[str]], list[dict[str, str]], list[dict[str, str]]]:
        """Вернуть ненаправленную проекцию явных связей и битые цели.

        Это производное представление: исходные records не изменяются.
        """
        ids = set(self.runtime.records)
        adjacency: dict[str, set[str]] = {object_id: set() for object_id in ids}
        edges: list[dict[str, str]] = []
        broken: list[dict[str, str]] = []
        seen_edges: set[tuple[str, str, str]] = set()
        seen_broken: set[tuple[str, str, str]] = set()

        for source_id, record in sorted(self.runtime.records.items()):
            for target, relation in self.runtime.relation_targets(record):
                target_id = str(target).strip()
                relation_name = _relation_name(relation)
                if not target_id:
                    continue
                if target_id not in ids:
                    key = (source_id, target_id, relation_name)
                    if key not in seen_broken:
                        broken.append({"source": source_id, "target": target_id, "relation": relation_name})
                        seen_broken.add(key)
                    continue
                edge_key = (source_id, target_id, relation_name)
                if edge_key in seen_edges:
                    continue
                seen_edges.add(edge_key)
                edges.append({"source": source_id, "target": target_id, "relation": relation_name})
                adjacency[source_id].add(target_id)
                adjacency[target_id].add(source_id)

        return adjacency, edges, broken

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

    def structure_analysis(self) -> dict[str, Any]:
        """Оценить структуру явного графа знаний без семантических догадок."""
        adjacency, edges, broken = self._graph()
        ids = sorted(adjacency)
        seen: set[str] = set()
        components: list[list[str]] = []
        for object_id in ids:
            if object_id in seen:
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
            components.append(sorted(component))
        components.sort(key=lambda item: (-len(item), item[0] if item else ""))

        pair_edges = {
            tuple(sorted((edge["source"], edge["target"])))
            for edge in edges
            if edge["source"] != edge["target"]
        }
        node_count = len(ids)
        possible_pairs = node_count * (node_count - 1) / 2
        density = len(pair_edges) / possible_pairs if possible_pairs else 0.0
        clustered_count = sum(bool(self.runtime.records[object_id].get("clusters")) for object_id in ids)
        tagged_count = sum(bool(self.runtime.records[object_id].get("tags")) for object_id in ids)
        isolated = sorted(object_id for object_id in ids if not adjacency[object_id])
        weak = sorted(object_id for object_id in ids if len(adjacency[object_id]) == 1)

        return {
            "nodes": node_count,
            "explicit_relation_edges": len(edges),
            "unique_connected_pairs": len(pair_edges),
            "density": round(density, 4),
            "components_count": len(components),
            "components": components,
            "isolated_nodes": isolated,
            "weakly_connected_nodes": weak,
            "broken_relation_targets": sorted(
                broken,
                key=lambda item: (item["source"], item["target"], item["relation"]),
            ),
            "cluster_coverage": round(clustered_count / node_count, 4) if node_count else 0.0,
            "tag_coverage": round(tagged_count / node_count, 4) if node_count else 0.0,
            "authority": "diagnostic_only",
        }

    def weakly_connected_nodes(self, *, max_degree: int = 1) -> list[dict[str, Any]]:
        """Найти изолированные и слабосвязанные узлы явного графа."""
        if max_degree < 0:
            raise ValueError("max_degree должен быть >= 0")
        adjacency, _edges, broken = self._graph()
        broken_by_source: dict[str, int] = defaultdict(int)
        for item in broken:
            broken_by_source[item["source"]] += 1

        result: list[dict[str, Any]] = []
        for object_id in sorted(adjacency):
            degree = len(adjacency[object_id])
            if degree > max_degree:
                continue
            result.append(
                {
                    "id": object_id,
                    "degree": degree,
                    "status": self.runtime.records[object_id].get("status"),
                    "broken_relation_targets": broken_by_source.get(object_id, 0),
                    "reason": "изолированный узел" if degree == 0 else "слабая связность",
                    "authority": "diagnostic_only",
                }
            )
        return result

    def conflict_signals(self) -> dict[str, Any]:
        """Показать только явно записанные конфликтные признаки.

        Текст объектов не интерпретируется, поэтому ложная семантическая
        классификация конфликта не превращается в системный факт.
        """
        conflicts: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str]] = set()
        ids = set(self.runtime.records)

        for object_id, record in sorted(self.runtime.records.items()):
            if record.get("status") == "disputed":
                key = (object_id, object_id, "status:disputed")
                seen.add(key)
                conflicts.append(
                    {
                        "source": object_id,
                        "target": object_id,
                        "signal": "status:disputed",
                        "target_exists": True,
                    }
                )
            for target, relation in self.runtime.relation_targets(record):
                relation_name = _relation_name(relation)
                if relation_name not in CONFLICT_RELATIONS:
                    continue
                target_id = str(target).strip()
                key = (object_id, target_id, f"relation:{relation_name}")
                if key in seen:
                    continue
                seen.add(key)
                conflicts.append(
                    {
                        "source": object_id,
                        "target": target_id,
                        "signal": f"relation:{relation_name}",
                        "target_exists": target_id in ids,
                    }
                )

        conflicts.sort(key=lambda item: (item["source"], item["target"], item["signal"]))
        return {
            "status": "WARN" if conflicts else "PASS",
            "count": len(conflicts),
            "conflicts": conflicts,
            "method": "explicit_signals_only",
            "authority": "diagnostic_only",
        }

    def signal_diagnostics(self) -> dict[str, Any]:
        """Проверить confidence/novelty/uncertainty/importance как метаданные."""
        objects: list[dict[str, Any]] = []
        values: dict[str, list[float]] = {field: [] for field in SIGNAL_FIELDS}

        for object_id, record in sorted(self.runtime.records.items()):
            signals = record.get("signals") if isinstance(record.get("signals"), dict) else {}
            warnings: list[str] = []
            numeric: dict[str, float] = {}
            for field in SIGNAL_FIELDS:
                value = signals.get(field)
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    numeric[field] = float(value)
                    values[field].append(float(value))

            if not numeric:
                warnings.append("нет числовых сигналов уверенности/новизны/неопределённости/важности")
            confidence = numeric.get("confidence")
            novelty = numeric.get("novelty")
            uncertainty = numeric.get("uncertainty")
            importance = numeric.get("importance")

            if confidence is not None and confidence <= 0.4:
                warnings.append("низкая уверенность")
            if uncertainty is not None and uncertainty >= 0.7:
                warnings.append("высокая неопределённость")
            if importance is not None and importance >= 0.7 and confidence is not None and confidence < 0.5:
                warnings.append("важный объект с низкой уверенностью")
            if novelty is not None and novelty >= 0.7 and not record.get("evidence"):
                warnings.append("высокая новизна без доказательств")
            if record.get("status") == "canonical":
                if confidence is not None and confidence < 0.7:
                    warnings.append("канонический объект с пониженной уверенностью")
                if uncertainty is not None and uncertainty > 0.4:
                    warnings.append("канонический объект с заметной неопределённостью")

            objects.append(
                {
                    "id": object_id,
                    "signals": {field: numeric[field] for field in SIGNAL_FIELDS if field in numeric},
                    "warnings": warnings,
                    "authority": "diagnostic_only",
                }
            )

        averages = {
            field: (round(sum(field_values) / len(field_values), 3) if field_values else None)
            for field, field_values in values.items()
        }
        return {
            "status": "WARN" if any(item["warnings"] for item in objects) else "PASS",
            "averages": averages,
            "objects": objects,
            "authority": "diagnostic_only",
        }

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
                        "status_path": history_statuses
                        + ([current] if not history_statuses or history_statuses[-1] != current else []),
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
            status_counts = dict(
                sorted(
                    state["status_counts"].items(),
                    key=lambda item: STATUS_ORDER.index(item[0]) if item[0] in STATUS_ORDER else 999,
                )
            )
            events = sorted(
                state["events"],
                key=lambda item: (str(item.get("timestamp") or ""), item["object_id"]),
            )
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
            "schema_version": "1.1",
            "kind": "cks_knowledge_intelligence",
            "authority": "analysis_and_suggestions_only",
            "скрытые_связи": self.hidden_links(threshold=link_threshold),
            "новые_кластеры": self.cluster_suggestions(),
            "структура_знаний": self.structure_analysis(),
            "слабосвязанные_узлы": self.weakly_connected_nodes(),
            "конфликтные_сигналы": self.conflict_signals(),
            "сигналы_уверенности_и_новизны": self.signal_diagnostics(),
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
