#!/usr/bin/env python3
"""Совместимый поиск несвязанных узлов CKS v1.7.

Исторический интерфейс сохраняется, но связность вычисляется через текущий
``KnowledgeGraph``. Битые связи не считаются доказательством связности узла.
"""
from __future__ import annotations

from typing import Any

from cks_knowledge_graph_runtime import DEFAULT_RELATIONS, GraphError, KnowledgeGraph


def find_orphans(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    relation_names = {
        str(edge.get("relation") or edge.get("type") or "").strip()
        for edge in edges
        if str(edge.get("relation") or edge.get("type") or "").strip()
    }
    graph = KnowledgeGraph(allowed_relations=DEFAULT_RELATIONS | relation_names)
    source_by_id: dict[str, dict[str, Any]] = {}

    for raw in nodes:
        node_id = str(raw.get("id") or "").strip()
        if not node_id or node_id in source_by_id:
            continue
        source_by_id[node_id] = raw
        graph.add_node(
            node_id,
            str(raw.get("type") or "unknown"),
            project=raw.get("project"),
            lifecycle=raw.get("lifecycle"),
            metadata=dict(raw.get("metadata") or {}),
        )

    for raw in edges:
        source = str(raw.get("source") or "").strip()
        target = str(raw.get("target") or "").strip()
        relation = str(raw.get("relation") or raw.get("type") or "").strip()
        if not source or not target or not relation:
            continue
        try:
            graph.add_edge(source, target, relation)
        except GraphError:
            # Битая связь не должна скрывать реальный orphan-узел.
            continue

    orphan_ids = set(graph.validate()["orphan_nodes"])
    return [raw for raw in nodes if str(raw.get("id") or "").strip() in orphan_ids]
