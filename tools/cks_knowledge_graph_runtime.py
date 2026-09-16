#!/usr/bin/env python3
"""Рабочий граф знаний CKS.

Knowledge Graph Runtime (рабочий граф знаний) является производным индексом
связей и не заменяет SSOT (единый источник истины), Decision (решение) или
Canon (канон).

Модуль поддерживает:
- узлы, связи и зависимости;
- versioned Relation History (версионируемую историю связей);
- миграцию формата графового хранилища;
- контрольные снимки и восстановление графа с SHA-256;
- атомарную запись JSON-хранилища.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import tempfile
from collections import deque
from pathlib import Path
from typing import Any, Iterable

CURRENT_GRAPH_SCHEMA_VERSION = "2.0"
RECOVERY_SNAPSHOT_VERSION = "1.0"

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
    """Ошибка целостности или формата производного графа."""


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _edge_id(source: str, target: str, relation: str) -> str:
    raw = f"{source}\0{relation}\0{target}".encode("utf-8")
    return "REL-" + hashlib.sha256(raw).hexdigest()[:24]


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent), text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


class KnowledgeGraph:
    """Граф объектов CKS с JSON-хранилищем, историей связей и recovery."""

    def __init__(self, storage_path: str | Path | None = None, *, allowed_relations: Iterable[str] | None = None):
        self.storage_path = Path(storage_path) if storage_path else None
        self.allowed_relations = set(allowed_relations or DEFAULT_RELATIONS)
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: list[dict[str, Any]] = []
        self.relation_history: list[dict[str, Any]] = []
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
            "metadata": copy.deepcopy(metadata or {}),
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

    @staticmethod
    def _relation_event(
        edge: dict[str, Any],
        event: str,
        *,
        reason: str | None = None,
        changed_by: str | None = None,
        timestamp: str | None = None,
        changes: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        item: dict[str, Any] = {
            "edge_id": edge["id"],
            "event": event,
            "version": edge["version"],
            "source": edge["source"],
            "target": edge["target"],
            "relation": edge["relation"],
        }
        if reason:
            item["reason"] = reason
        if changed_by:
            item["changed_by"] = changed_by
        if timestamp:
            item["timestamp"] = timestamp
        if changes:
            item["changes"] = copy.deepcopy(changes)
        return item

    def _edge_by_id(self, edge_id: str) -> dict[str, Any] | None:
        return next((edge for edge in self.edges if edge.get("id") == edge_id), None)

    def add_edge(
        self,
        source: str,
        target: str,
        relation: str,
        *,
        evidence: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        reason: str | None = None,
        changed_by: str | None = None,
        timestamp: str | None = None,
        edge_id: str | None = None,
        version: int = 1,
        history: list[dict[str, Any]] | None = None,
        record_history: bool = True,
    ) -> dict[str, Any]:
        if source not in self.nodes:
            raise GraphError(f"Не найден исходный узел: {source}")
        if target not in self.nodes:
            raise GraphError(f"Не найден целевой узел: {target}")
        if relation not in self.allowed_relations:
            raise GraphError(f"Недопустимый тип связи: {relation}")

        relation_id = edge_id or _edge_id(source, target, relation)
        existing = self._edge_by_id(relation_id)
        if existing is not None:
            return existing

        edge = {
            "id": relation_id,
            "version": int(version),
            "source": source,
            "target": target,
            "relation": relation,
            "evidence": list(evidence or []),
            "metadata": copy.deepcopy(metadata or {}),
            "history": copy.deepcopy(history or []),
        }
        if record_history:
            event = self._relation_event(
                edge,
                "created",
                reason=reason,
                changed_by=changed_by,
                timestamp=timestamp,
            )
            edge["history"].append(copy.deepcopy(event))
            self.relation_history.append(event)
        self.edges.append(edge)
        return edge

    def update_edge(
        self,
        edge_id: str,
        *,
        evidence: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        reason: str,
        changed_by: str | None = None,
        timestamp: str | None = None,
    ) -> dict[str, Any]:
        edge = self._edge_by_id(edge_id)
        if edge is None:
            raise GraphError(f"Связь не найдена: {edge_id}")
        if not reason:
            raise GraphError("Изменение связи требует reason")

        changes: dict[str, Any] = {}
        if evidence is not None and list(evidence) != edge.get("evidence", []):
            changes["evidence"] = {"before": copy.deepcopy(edge.get("evidence", [])), "after": list(evidence)}
            edge["evidence"] = list(evidence)
        if metadata is not None and dict(metadata) != edge.get("metadata", {}):
            changes["metadata"] = {"before": copy.deepcopy(edge.get("metadata", {})), "after": copy.deepcopy(dict(metadata))}
            edge["metadata"] = copy.deepcopy(dict(metadata))
        if not changes:
            return edge

        edge["version"] = int(edge.get("version", 1)) + 1
        event = self._relation_event(
            edge,
            "updated",
            reason=reason,
            changed_by=changed_by,
            timestamp=timestamp,
            changes=changes,
        )
        edge.setdefault("history", []).append(copy.deepcopy(event))
        self.relation_history.append(event)
        return edge

    def remove_edge(
        self,
        edge_id: str,
        *,
        reason: str,
        changed_by: str | None = None,
        timestamp: str | None = None,
    ) -> None:
        edge = self._edge_by_id(edge_id)
        if edge is None:
            return
        if not reason:
            raise GraphError("Удаление связи требует reason")
        edge["version"] = int(edge.get("version", 1)) + 1
        event = self._relation_event(
            edge,
            "removed",
            reason=reason,
            changed_by=changed_by,
            timestamp=timestamp,
        )
        self.relation_history.append(event)
        self.edges = [item for item in self.edges if item.get("id") != edge_id]

    def relation_history_for(self, edge_id: str) -> list[dict[str, Any]]:
        return [copy.deepcopy(item) for item in self.relation_history if item.get("edge_id") == edge_id]

    def remove_node(self, node_id: str, *, cascade: bool = False) -> None:
        if node_id not in self.nodes:
            return
        attached = [e for e in self.edges if e["source"] == node_id or e["target"] == node_id]
        if attached and not cascade:
            raise GraphError(f"Узел {node_id} имеет связи; требуется cascade=True")
        if cascade:
            for edge in list(attached):
                self.remove_edge(edge["id"], reason=f"каскадное удаление узла {node_id}")
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
            if current in seen or current == node_id:
                continue
            seen.add(current)
            queue.extend(e["target"] for e in self.outgoing(current, "depends_on") if e["target"] not in seen)
        return sorted(seen)

    def validate(self) -> dict[str, Any]:
        broken = [e for e in self.edges if e["source"] not in self.nodes or e["target"] not in self.nodes]
        invalid_relations = [e for e in self.edges if e.get("relation") not in self.allowed_relations]
        ids = [str(e.get("id") or "") for e in self.edges]
        duplicate_edge_ids = sorted({edge_id for edge_id in ids if edge_id and ids.count(edge_id) > 1})
        invalid_versions = [e.get("id") for e in self.edges if not isinstance(e.get("version"), int) or e.get("version", 0) < 1]
        orphan_nodes = [
            node_id
            for node_id in self.nodes
            if not any(e["source"] == node_id or e["target"] == node_id for e in self.edges)
        ]
        failures = bool(broken or invalid_relations or duplicate_edge_ids or invalid_versions)
        return {
            "status": "FAIL" if failures else ("WARN" if orphan_nodes else "PASS"),
            "broken_edges": broken,
            "invalid_relations": invalid_relations,
            "duplicate_edge_ids": duplicate_edge_ids,
            "invalid_edge_versions": invalid_versions,
            "orphan_nodes": sorted(orphan_nodes),
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "relation_history_events": len(self.relation_history),
        }

    @classmethod
    def migrate_payload(cls, payload: dict[str, Any]) -> dict[str, Any]:
        """Мигрировать JSON графа к текущей версии без изменения входных данных."""
        source = copy.deepcopy(payload)
        version = str(source.get("schema_version") or "1.0")
        if version not in {"1.0", CURRENT_GRAPH_SCHEMA_VERSION}:
            raise GraphError(f"Неподдерживаемая schema_version графа: {version}")

        nodes = copy.deepcopy(source.get("nodes") or [])
        raw_edges = copy.deepcopy(source.get("edges") or [])
        relation_history = copy.deepcopy(source.get("relation_history") or [])
        migrated_edges: list[dict[str, Any]] = []

        for raw in raw_edges:
            source_id = str(raw.get("source") or "")
            target_id = str(raw.get("target") or "")
            relation = str(raw.get("relation") or "")
            if not source_id or not target_id or not relation:
                raise GraphError("Связь графа должна иметь source, target и relation")
            edge = {
                "id": str(raw.get("id") or _edge_id(source_id, target_id, relation)),
                "version": int(raw.get("version") or 1),
                "source": source_id,
                "target": target_id,
                "relation": relation,
                "evidence": list(raw.get("evidence") or []),
                "metadata": copy.deepcopy(raw.get("metadata") or {}),
                "history": copy.deepcopy(raw.get("history") or []),
            }
            if version == "1.0" and not edge["history"]:
                event = cls._relation_event(edge, "migrated", reason="миграция graph schema 1.0 → 2.0")
                edge["history"].append(copy.deepcopy(event))
                relation_history.append(event)
            migrated_edges.append(edge)

        return {
            "schema_version": CURRENT_GRAPH_SCHEMA_VERSION,
            "derived_index": bool(source.get("derived_index", True)),
            "nodes": nodes,
            "edges": migrated_edges,
            "relation_history": relation_history,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": CURRENT_GRAPH_SCHEMA_VERSION,
            "derived_index": True,
            "nodes": [copy.deepcopy(self.nodes[key]) for key in sorted(self.nodes)],
            "edges": copy.deepcopy(sorted(self.edges, key=lambda item: str(item.get("id") or ""))),
            "relation_history": copy.deepcopy(self.relation_history),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "KnowledgeGraph":
        migrated = cls.migrate_payload(payload)
        graph = cls()
        for node in migrated.get("nodes", []):
            graph.upsert_node(node)
        for edge in migrated.get("edges", []):
            graph.add_edge(
                str(edge["source"]),
                str(edge["target"]),
                str(edge["relation"]),
                evidence=list(edge.get("evidence") or []),
                metadata=dict(edge.get("metadata") or {}),
                edge_id=str(edge["id"]),
                version=int(edge.get("version") or 1),
                history=list(edge.get("history") or []),
                record_history=False,
            )
        graph.relation_history = copy.deepcopy(migrated.get("relation_history") or [])
        return graph

    def create_recovery_snapshot(self, *, label: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "snapshot_version": RECOVERY_SNAPSHOT_VERSION,
            "kind": "cks_graph_recovery_snapshot",
            "graph": self.to_dict(),
        }
        if label:
            payload["label"] = str(label)
        return {**payload, "sha256": _digest(payload), "authority": "recovery_artifact_only"}

    @classmethod
    def verify_recovery_snapshot(cls, snapshot: dict[str, Any]) -> dict[str, Any]:
        errors: list[str] = []
        if snapshot.get("kind") != "cks_graph_recovery_snapshot":
            errors.append("неверный kind снимка графа")
        if snapshot.get("snapshot_version") != RECOVERY_SNAPSHOT_VERSION:
            errors.append("неподдерживаемая версия снимка графа")
        expected = str(snapshot.get("sha256") or "")
        payload = {key: copy.deepcopy(value) for key, value in snapshot.items() if key not in {"sha256", "authority"}}
        if not expected or _digest(payload) != expected:
            errors.append("SHA-256 снимка графа не совпадает")
        if not errors:
            try:
                graph = cls.from_dict(snapshot.get("graph") or {})
                validation = graph.validate()
                if validation["status"] == "FAIL":
                    errors.append("содержимое снимка не прошло проверку графа")
            except (GraphError, TypeError, ValueError) as exc:
                errors.append(f"снимок графа не восстанавливается: {exc}")
        return {"status": "FAIL" if errors else "PASS", "errors": errors, "authority": "verification_only"}

    @classmethod
    def recover_snapshot(cls, snapshot: dict[str, Any]) -> "KnowledgeGraph":
        verification = cls.verify_recovery_snapshot(snapshot)
        if verification["status"] != "PASS":
            raise GraphError("; ".join(verification["errors"]))
        return cls.from_dict(copy.deepcopy(snapshot["graph"]))

    def save_snapshot(self, path: str | Path, *, label: str | None = None) -> Path:
        target = Path(path)
        text = json.dumps(self.create_recovery_snapshot(label=label), ensure_ascii=False, indent=2) + "\n"
        _atomic_write(target, text)
        return target

    @classmethod
    def load_snapshot(cls, path: str | Path) -> "KnowledgeGraph":
        source = Path(path)
        if not source.exists():
            raise GraphError("Файл recovery snapshot не найден")
        payload = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise GraphError("Recovery snapshot должен быть JSON-объектом")
        return cls.recover_snapshot(payload)

    def save(self, path: str | Path | None = None) -> Path:
        target = Path(path) if path else self.storage_path
        if target is None:
            raise GraphError("Не указан путь хранилища")
        _atomic_write(target, json.dumps(self.to_dict(), ensure_ascii=False, indent=2) + "\n")
        self.storage_path = target
        return target

    def load(self, path: str | Path | None = None) -> None:
        source = Path(path) if path else self.storage_path
        if source is None or not source.exists():
            raise GraphError("Файл графа не найден")
        payload = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise GraphError("Файл графа должен быть JSON-объектом")
        loaded = self.from_dict(payload)
        validation = loaded.validate()
        if validation["status"] == "FAIL":
            raise GraphError(f"Граф не прошёл проверку: {validation}")
        self.nodes = loaded.nodes
        self.edges = loaded.edges
        self.relation_history = loaded.relation_history
        self.storage_path = source


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: рабочий граф знаний")
    parser.add_argument("--graph", required=True, help="JSON-файл производного графа")
    parser.add_argument("--validate", action="store_true", help="Проверить целостность графа")
    parser.add_argument("--migrate", action="store_true", help="Мигрировать файл графа к текущей schema_version")
    parser.add_argument("--snapshot", help="Записать recovery snapshot в указанный JSON-файл")
    args = parser.parse_args()

    graph = KnowledgeGraph(args.graph)
    if args.migrate:
        graph.save(args.graph)
    if args.snapshot:
        graph.save_snapshot(args.snapshot, label="cli")
    result = graph.validate() if args.validate else graph.to_dict()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result.get("status") == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
