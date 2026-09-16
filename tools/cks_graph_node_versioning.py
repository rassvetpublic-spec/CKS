#!/usr/bin/env python3
"""Жизненный цикл и версионирование узлов рабочего графа CKS.

Модуль НЕ создаёт второй графовый движок. Он работает поверх существующего
``KnowledgeGraph`` и хранит служебную историю внутри metadata узла, поэтому
история переживает обычный save/load существующего графа.

Назначение:
- Graph Object Lifecycle — применять существующие правила жизненного цикла
  знаний к узлам графа;
- Node Versioning — хранить номер версии узла и историю изменений;
- не позволять обходить защиту Canon через графовый слой.
"""
from __future__ import annotations

import copy
from typing import Any

from cks_knowledge_graph_runtime import GraphError, KnowledgeGraph
from cks_knowledge_state_machine import validate_transition

META_KEY = "_cks_node_versioning"


def _state(node: dict[str, Any]) -> dict[str, Any]:
    metadata = node.setdefault("metadata", {})
    state = metadata.setdefault(
        META_KEY,
        {
            "version": 1,
            "history": [],
        },
    )
    state.setdefault("version", 1)
    state.setdefault("history", [])
    return state


def initialize_node(
    graph: KnowledgeGraph,
    node_id: str,
    node_type: str,
    *,
    project: str | None = None,
    lifecycle: str = "raw",
    metadata: dict[str, Any] | None = None,
    changed_by: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    node = graph.add_node(
        node_id,
        node_type,
        project=project,
        lifecycle=lifecycle,
        metadata=copy.deepcopy(metadata or {}),
    )
    state = _state(node)
    event: dict[str, Any] = {
        "event": "created",
        "version": 1,
        "lifecycle": lifecycle,
    }
    if changed_by:
        event["changed_by"] = changed_by
    if timestamp:
        event["timestamp"] = timestamp
    state["history"].append(event)
    return node


def node_version(graph: KnowledgeGraph, node_id: str) -> int:
    if node_id not in graph.nodes:
        raise GraphError(f"Узел не найден: {node_id}")
    return int(_state(graph.nodes[node_id])["version"])


def node_history(graph: KnowledgeGraph, node_id: str) -> list[dict[str, Any]]:
    if node_id not in graph.nodes:
        raise GraphError(f"Узел не найден: {node_id}")
    return copy.deepcopy(_state(graph.nodes[node_id])["history"])


def update_node(
    graph: KnowledgeGraph,
    node_id: str,
    *,
    node_type: str | None = None,
    project: str | None = None,
    lifecycle: str | None = None,
    metadata_patch: dict[str, Any] | None = None,
    reason: str,
    changed_by: str | None = None,
    timestamp: str | None = None,
    evidence_count: int = 0,
    decision_ref: str | None = None,
) -> dict[str, Any]:
    if node_id not in graph.nodes:
        raise GraphError(f"Узел не найден: {node_id}")
    if not str(reason or "").strip():
        raise GraphError("Изменение узла требует reason")

    node = graph.nodes[node_id]
    before = copy.deepcopy(node)

    if lifecycle is not None and lifecycle != node.get("lifecycle"):
        check = validate_transition(
            node.get("lifecycle") or "raw",
            lifecycle,
            reason=reason,
            evidence_count=evidence_count,
            decision_ref=decision_ref,
        )
        if check["status"] != "PASS":
            raise GraphError("; ".join(check.get("errors") or ["недопустимый переход жизненного цикла"]))
        node["lifecycle"] = lifecycle

    if node_type is not None:
        node["type"] = node_type
    if project is not None:
        node["project"] = project
    if metadata_patch:
        metadata = node.setdefault("metadata", {})
        for key, value in metadata_patch.items():
            if key == META_KEY:
                raise GraphError(f"Служебное поле {META_KEY} нельзя изменять через metadata_patch")
            metadata[key] = copy.deepcopy(value)

    comparable_before = copy.deepcopy(before)
    comparable_after = copy.deepcopy(node)
    comparable_before.get("metadata", {}).pop(META_KEY, None)
    comparable_after.get("metadata", {}).pop(META_KEY, None)
    if comparable_before == comparable_after:
        return node

    state = _state(node)
    state["version"] = int(state.get("version", 1)) + 1
    event: dict[str, Any] = {
        "event": "updated",
        "version": state["version"],
        "reason": reason,
        "before": comparable_before,
        "after": comparable_after,
    }
    if changed_by:
        event["changed_by"] = changed_by
    if timestamp:
        event["timestamp"] = timestamp
    state["history"].append(event)
    return node


def transition_node(
    graph: KnowledgeGraph,
    node_id: str,
    target: str,
    *,
    reason: str,
    changed_by: str | None = None,
    timestamp: str | None = None,
    evidence_count: int = 0,
    decision_ref: str | None = None,
) -> dict[str, Any]:
    return update_node(
        graph,
        node_id,
        lifecycle=target,
        reason=reason,
        changed_by=changed_by,
        timestamp=timestamp,
        evidence_count=evidence_count,
        decision_ref=decision_ref,
    )
