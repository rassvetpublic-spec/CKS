#!/usr/bin/env python3
"""Совместимый валидатор графа CKS v1.7.

Сохраняет исторический интерфейс ``validate_graph(nodes, edges)`` и проверяет
его через текущий ``KnowledgeGraph``. Модуль не является отдельным графовым
движком и не принимает Decision/Canon.
"""
from __future__ import annotations

from typing import Any

from cks_knowledge_graph_runtime import GraphError, KnowledgeGraph


def validate_graph_report(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, Any]:
    """Вернуть подробный диагностический отчёт совместимости v1.7."""
    graph = KnowledgeGraph()
    issues: list[str] = []

    for raw in nodes:
        node_id = str(raw.get("id") or "").strip()
        node_type = str(raw.get("type") or "unknown").strip() or "unknown"
        if not node_id:
            issues.append("invalid_node")
            continue
        try:
            graph.add_node(
                node_id,
                node_type,
                project=raw.get("project"),
                lifecycle=raw.get("lifecycle"),
                metadata=dict(raw.get("metadata") or {}),
            )
        except GraphError:
            issues.append("duplicate_node_id")

    for raw in edges:
        source = str(raw.get("source") or "").strip()
        target = str(raw.get("target") or "").strip()
        relation = str(raw.get("relation") or raw.get("type") or "").strip()
        if not source or not target or source not in graph.nodes or target not in graph.nodes:
            issues.append("broken_edge_reference")
            continue
        if not relation:
            issues.append("invalid_relation")
            continue
        try:
            graph.add_edge(
                source,
                target,
                relation,
                evidence=list(raw.get("evidence") or []),
                metadata=dict(raw.get("metadata") or {}),
            )
        except GraphError:
            issues.append("invalid_relation")

    runtime_report = graph.validate()
    if runtime_report.get("invalid_relations"):
        issues.append("invalid_relation")
    if runtime_report.get("duplicate_edge_ids"):
        issues.append("duplicate_edge_id")
    if runtime_report.get("invalid_edge_versions"):
        issues.append("invalid_edge_version")

    deduplicated = list(dict.fromkeys(issues))
    return {
        "status": "FAIL" if deduplicated else ("WARN" if runtime_report.get("orphan_nodes") else "PASS"),
        "issues": deduplicated,
        "runtime": runtime_report,
        "authority": "validation_only",
    }


def validate_graph(nodes, edges):
    """Исторический интерфейс: вернуть только список кодов проблем."""
    return validate_graph_report(list(nodes), list(edges))["issues"]
