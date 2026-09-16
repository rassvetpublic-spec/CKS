#!/usr/bin/env python3
"""Рабочий граф знаний CKS.

Техническое имя Knowledge Graph Runtime означает исполняемый слой графа.
Граф является производным индексом связей и не заменяет источники истины CKS.
Модуль не принимает архитектурных решений и не изменяет Canon автоматически.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from collections import deque
from pathlib import Path
from typing import Any, Iterable

DEFAULT_RELATIONS = {
    "supports",
    "contradicts",
    "implements",
    "supersedes",
    "depends_on",
    "derived_from",
    "validates",
    "evidenced_by",
    "decided_by",
    "implemented_by",
    "reviewed_by",
    "conflicts_with",
}


class GraphError(ValueError):
    """Ошибка целостности производного графа."""


class KnowledgeGraph:
    """Граф объектов CKS с JSON-хранилищем и проверкой ссылок."""

    def __init__(self, storage_path: str | Path | None = None, *, allowed_relations: Iterable[str] | None = None):
        self.storage_path = Path(storage_path) if storage_path else None
        self.allowed_relations = set(allowed_relations or DEFAULT_RELATIONS)
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: list[dict[str, Any]] = []
        if self.storage_path and self.storage_path.exists():
            self.load()

    def add_node(
        self,
        node_id: str,
        node_type: str,
        *,
        project: str | None = None,
        lifecycle: str | None = None,
        metadata: dict[str, Any] | None = None,
        replace: bool = False,
    ) -> dict[str, Any]:
        if not node_id or not node_type:
            raise GraphError("Узел должен иметь id и type")
        if node_id in self.nodes and not replace:
            raise GraphError(f"Узел уже существует: {node_id}")
        node = {
            "id": node_id,
            "type": node_type,
            "project": project,
            "lifecycle": lifecycle,
            "metadata": metadata or {},
        }
        self.nodes[node_id] = node
        return node

    def upsert_node(self, node: dict[str, Any]) -> dict[str, Any]:
        return self.add_node(
            str(node["id"]),
            str(node.get("type", "unknown")),
            project=node.get("project"),
            lifecycle=node.get("lifecycle"),
            metadata=dict(node.get("metadata") or {}),
            replace=True,
        )

    def add_edge(
        self,
        source: str,
        target: str,
        relation: str,
        *,
        evidence: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if source not in self.nodes:
            raise GraphError(f"Не найден исходный узел: {source}")
        if target not in self.nodes:
            raise GraphError(f"Не найден целевой узел: {target}")
        if relation not in self.allowed_relations:
            raise GraphError(f"Недопустимый тип связи: {relation}")
        edge = {
            "source": source,
            "target": target,
            "relation": relation,
            "evidence": list(evidence or []),
            "metadata": metadata or {},
        }
        if edge not in self.edges:
            self.edges.append(edge)
        return edge

    def remove_node(self, node_id: str, *, cascade: bool = False) -> None:
        if node_id not in self.nodes:
            return
        attached = [e for e in self.edges if e["source"] == node_id or e["target"] == node_id]
        if attached and not cascade:
            raise GraphError(f"Узел {node_id} имеет связи; требуется cascade=True")
        self.edges = [e for e in self.edges if e not in attached]
        del self.nodes[node_id]

    def outgoing(self, node_id: str, relation: str | None = None) -> list[dict[str, Any]]:
        return [e for e in self.edges if e["source"] == node_id and (relation is None or e["relation"] == relation)]

    def incoming(self, node_id: str, relation: str | None = None) -> list[dict[str, Any]]:
        return [e for e in self.edges if e["target"] == node_id and (relation is None or e["relation"] == relation)]

    def dependencies(self, node_id: str, *, transitive: bool = False) -> list[str]:
        if node_id not in self.nodes:
            raise GraphError(f"Не найден узел: {node_id}")
        direct = [e["target"] for e in self.outgoing(node_id, "depends_on")]
        if not transitive:
            return direct
        seen: set[str] = set()
        queue = deque(direct)
        while queue:
            current = queue.popleft()
            if current in seen:
                continue
            seen.add(current)
            queue.extend(e["target"] for e in self.outgoing(current, "depends_on") if e["target"] not in seen)
        return sorted(seen)

    def validate(self) -> dict[str, Any]:
        broken = [e for e in self.edges if e["source"] not in self.nodes or e["target"] not in self.nodes]
        invalid_relations = [e for e in self.edges if e.get("relation") not in self.allowed_relations]
        orphan_nodes = [
            node_id
            for node_id in self.nodes
            if not any(e["source"] == node_id or e["target"] == node_id for e in self.edges)
        ]
        return {
            "status": "FAIL" if broken or invalid_relations else ("WARN" if orphan_nodes else "PASS"),
            "broken_edges": broken,
            "invalid_relations": invalid_relations,
            "orphan_nodes": sorted(orphan_nodes),
            "nodes": len(self.nodes),
            "edges": len(self.edges),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "derived_index": True,
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "KnowledgeGraph":
        graph = cls()
        for node in payload.get("nodes", []):
            graph.upsert_node(node)
        for edge in payload.get("edges", []):
            graph.add_edge(
                str(edge["source"]),
                str(edge["target"]),
                str(edge["relation"]),
                evidence=list(edge.get("evidence") or []),
                metadata=dict(edge.get("metadata") or {}),
            )
        return graph

    def save(self, path: str | Path | None = None) -> Path:
        target = Path(path) if path else self.storage_path
        if target is None:
            raise GraphError("Не указан путь хранилища")
        target.parent.mkdir(parents=True, exist_ok=True)
        data = json.dumps(self.to_dict(), ensure_ascii=False, indent=2) + "\n"
        fd, temp_name = tempfile.mkstemp(prefix=target.name + ".", dir=str(target.parent), text=True)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, target)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
        self.storage_path = target
        return target

    def load(self, path: str | Path | None = None) -> None:
        source = Path(path) if path else self.storage_path
        if source is None or not source.exists():
            raise GraphError("Файл графа не найден")
        payload = json.loads(source.read_text(encoding="utf-8"))
        loaded = self.from_dict(payload)
        self.nodes = loaded.nodes
        self.edges = loaded.edges
        self.storage_path = source


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: рабочий граф знаний")
    parser.add_argument("--graph", required=True, help="JSON-файл производного графа")
    parser.add_argument("--validate", action="store_true", help="Проверить целостность графа")
    args = parser.parse_args()
    graph = KnowledgeGraph(args.graph)
    result = graph.validate() if args.validate else graph.to_dict()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result.get("status") == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
