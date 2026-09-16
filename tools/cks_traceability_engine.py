#!/usr/bin/env python3
"""Движок происхождения знаний CKS.

Traceability Engine (движок трассируемости) автоматически строит производные
цепочки происхождения из объектов, доказательств, решений, изменений и проверок.
Он не создаёт решения и не повышает материалы до Canon.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from cks_knowledge_graph_runtime import KnowledgeGraph

FIELD_RELATIONS = {
    "origin": "derived_from",
    "evidence": "evidenced_by",
    "decision": "decided_by",
    "decisions": "decided_by",
    "changes": "implemented_by",
    "reviews": "reviewed_by",
}


class TraceabilityEngine:
    def __init__(self) -> None:
        self.graph = KnowledgeGraph()
        self.records: dict[str, dict[str, Any]] = {}
        self.broken_references: list[dict[str, str]] = []

    @staticmethod
    def _refs(value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value] if value else []
        if isinstance(value, dict):
            for key in ("id", "reference", "target", "object_id"):
                if value.get(key):
                    return [str(value[key])]
            return []
        if isinstance(value, list):
            result: list[str] = []
            for item in value:
                result.extend(TraceabilityEngine._refs(item))
            return result
        return []

    def ingest(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        self.records = {}
        self.graph = KnowledgeGraph()
        self.broken_references = []

        for record in records:
            record_id = str(record.get("id") or record.get("object_id") or "").strip()
            if not record_id:
                continue
            normalized = dict(record)
            normalized["id"] = record_id
            self.records[record_id] = normalized
            self.graph.add_node(
                record_id,
                str(record.get("type") or "unknown"),
                project=record.get("project"),
                lifecycle=record.get("lifecycle") or record.get("status"),
                metadata={"source": record.get("source")},
            )

        for record_id, record in self.records.items():
            for field, relation in FIELD_RELATIONS.items():
                for target in self._refs(record.get(field)):
                    self._link(record_id, target, relation, field)
            for relation_item in record.get("relations", []) if isinstance(record.get("relations"), list) else []:
                if not isinstance(relation_item, dict):
                    continue
                target = str(relation_item.get("target") or relation_item.get("object_id") or "").strip()
                relation = str(relation_item.get("type") or relation_item.get("relation") or "").strip()
                if target and relation:
                    self._link(record_id, target, relation, "relations")

        validation = self.graph.validate()
        status = "FAIL" if self.broken_references or validation["status"] == "FAIL" else validation["status"]
        return {
            "status": status,
            "records": len(self.records),
            "edges": len(self.graph.edges),
            "broken_references": self.broken_references,
            "graph_validation": validation,
        }

    def _link(self, source: str, target: str, relation: str, field: str) -> None:
        if target not in self.records:
            self.broken_references.append(
                {"source": source, "target": target, "relation": relation, "field": field}
            )
            return
        self.graph.add_edge(source, target, relation)

    def chain(self, object_id: str) -> dict[str, Any]:
        if object_id not in self.records:
            return {"status": "FAIL", "object_id": object_id, "reason": "объект не найден"}
        outgoing = self.graph.outgoing(object_id)
        incoming = self.graph.incoming(object_id)
        return {
            "status": "PASS",
            "object_id": object_id,
            "outgoing": outgoing,
            "incoming": incoming,
            "broken_references": [x for x in self.broken_references if x["source"] == object_id],
        }

    def export(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "derived_traceability": True,
            "graph": self.graph.to_dict(),
            "broken_references": self.broken_references,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: построение цепочек происхождения")
    parser.add_argument("input", help="JSON-массив записей CKS")
    parser.add_argument("--output", help="Куда сохранить производный граф")
    parser.add_argument("--object", dest="object_id", help="Показать цепочку одного объекта")
    args = parser.parse_args()

    records = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise SystemExit("Вход должен быть JSON-массивом")
    engine = TraceabilityEngine()
    result = engine.ingest(records)
    payload = engine.chain(args.object_id) if args.object_id else engine.export()
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": result, "payload": payload}, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
