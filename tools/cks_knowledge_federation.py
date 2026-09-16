#!/usr/bin/env python3
"""Федерация знаний нескольких проектов CKS.

Multi-project Knowledge Federation (федерация знаний нескольких проектов)
объединяет только производные индексы и ссылки. Canon каждого проекта остаётся
независимым и не переносится автоматически между проектами.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from cks_knowledge_graph_runtime import KnowledgeGraph, GraphError


class FederationError(ValueError):
    pass


class KnowledgeFederation:
    def __init__(self) -> None:
        self.projects: dict[str, dict[str, Any]] = {}
        self.graph = KnowledgeGraph()
        self.cross_project_edges: list[dict[str, Any]] = []

    @staticmethod
    def namespace(project_id: str, object_id: str) -> str:
        return f"{project_id}::{object_id}"

    def add_project(self, project: dict[str, Any]) -> None:
        project_id = str(project.get("project_id") or "").strip()
        if not project_id:
            raise FederationError("Проект должен иметь project_id")
        if project_id in self.projects:
            raise FederationError(f"Проект уже добавлен: {project_id}")

        self.projects[project_id] = {
            "project_id": project_id,
            "source": project.get("source"),
            "version": project.get("version"),
            "canon_owner": project.get("canon_owner") or project_id,
        }

        for node in project.get("nodes", []):
            if not isinstance(node, dict) or not node.get("id"):
                continue
            namespaced = self.namespace(project_id, str(node["id"]))
            self.graph.add_node(
                namespaced,
                str(node.get("type") or "unknown"),
                project=project_id,
                lifecycle=node.get("lifecycle"),
                metadata={
                    "local_id": str(node["id"]),
                    "source": node.get("source"),
                    "version": node.get("version"),
                },
            )

        for edge in project.get("edges", []):
            if not isinstance(edge, dict):
                continue
            source = self.namespace(project_id, str(edge.get("source") or ""))
            target = self.namespace(project_id, str(edge.get("target") or ""))
            if source.endswith("::") or target.endswith("::"):
                continue
            self.graph.add_edge(
                source,
                target,
                str(edge.get("relation") or "depends_on"),
                evidence=list(edge.get("evidence") or []),
                metadata={"project": project_id},
            )

    def add_cross_project_relation(
        self,
        source_project: str,
        source_id: str,
        target_project: str,
        target_id: str,
        relation: str,
        *,
        evidence: list[str] | None = None,
    ) -> dict[str, Any]:
        if source_project == target_project:
            raise FederationError("Для связи внутри проекта используйте его локальный граф")
        source = self.namespace(source_project, source_id)
        target = self.namespace(target_project, target_id)
        edge = self.graph.add_edge(
            source,
            target,
            relation,
            evidence=evidence,
            metadata={"cross_project": True},
        )
        self.cross_project_edges.append(edge)
        return edge

    def validate(self) -> dict[str, Any]:
        graph_result = self.graph.validate()
        ownership_conflicts: list[dict[str, str]] = []
        for edge in self.cross_project_edges:
            source_project = self.graph.nodes[edge["source"]].get("project")
            target_project = self.graph.nodes[edge["target"]].get("project")
            if source_project == target_project:
                ownership_conflicts.append({"source": edge["source"], "target": edge["target"]})
        status = "FAIL" if graph_result["status"] == "FAIL" or ownership_conflicts else graph_result["status"]
        return {
            "status": status,
            "projects": len(self.projects),
            "cross_project_edges": len(self.cross_project_edges),
            "ownership_conflicts": ownership_conflicts,
            "graph": graph_result,
        }

    def export_index(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "derived_federation_index": True,
            "projects": list(self.projects.values()),
            "graph": self.graph.to_dict(),
            "cross_project_edges": self.cross_project_edges,
            "rule": "Индекс федерации не является SSOT и не объединяет Canon проектов.",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: федерация знаний нескольких проектов")
    parser.add_argument("manifests", nargs="+", help="JSON-манифесты проектов")
    parser.add_argument("--output", required=True, help="JSON-файл производного индекса")
    args = parser.parse_args()

    federation = KnowledgeFederation()
    try:
        for manifest in args.manifests:
            payload = json.loads(Path(manifest).read_text(encoding="utf-8"))
            federation.add_project(payload)
    except (FederationError, GraphError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 1

    result = federation.validate()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(federation.export_index(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
