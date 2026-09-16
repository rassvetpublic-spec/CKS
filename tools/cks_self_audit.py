#!/usr/bin/env python3
"""Система самопроверки архитектуры CKS.

CKS Self Audit System (система самопроверки CKS) диагностирует структуру,
управляющий слой, рабочий Runtime и исторические compatibility-слои. Она не
изменяет файлы, не принимает решения и не создаёт Canon.
"""
from __future__ import annotations

import argparse
import json
import py_compile
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Finding:
    level: str
    code: str
    path: str
    message: str


REQUIRED_PATHS = (
    "README.md",
    "ARCHITECTURE.md",
    "core/CKS_CHANGE_RULES.md",
    "control/system-state.yaml",
    "control/ssot-registry.yaml",
    "control/traceability-model.yaml",
    "control/lifecycle-state-model.yaml",
    "control/automation-governance.yaml",
    "docs/ADR-007_Двуязычная_модель_документации_CKS.md",
    "docs/ГЛОССАРИЙ.md",
    "decisions/ADR-0002-knowledge-centric-runtime.md",
    "docs/CKS_KNOWLEDGE_RUNTIME_AND_INTELLIGENCE_RU.md",
    "schemas/cks-knowledge-object.schema.json",
    "schemas/cks-knowledge-view.schema.json",
    "obsidian/README.md",
    "obsidian/Шаблон_объекта_знания.md",
    "tools/cks_knowledge_graph_runtime.py",
    "tools/cks_traceability_engine.py",
    "tools/cks_knowledge_federation.py",
    "tools/cks_governance_runner.py",
    "tools/cks_knowledge_runtime.py",
    "tools/cks_knowledge_intelligence.py",
    "tools/cks_compatibility_audit.py",
)

RUNTIME_MODULES = (
    "tools/cks_knowledge_graph_runtime.py",
    "tools/cks_traceability_engine.py",
    "tools/cks_knowledge_federation.py",
    "tools/cks_runtime_pipeline.py",
    "tools/cks_governance_runner.py",
    "tools/cks_knowledge_runtime.py",
    "tools/cks_knowledge_intelligence.py",
    "tools/cks_compatibility_audit.py",
    "tools/cks_v1_6_intelligence_runtime.py",
    "tools/cks_canon_conflict_detector.py",
    "tools/cks_knowledge_health_score.py",
    "tools/cks_v1_7_graph_validator.py",
    "tools/cks_v1_7_orphan_node_detector.py",
    "tools/cks_v1_7_relation_engine.py",
    "tools/cks_v1_4_metrics_calculator.py",
    "tools/cks_v1_4_graph_builder.py",
    "tools/cks_v1_4_review_gate_runner.py",
    "tools/cks_v1_4_migration_adapter.py",
    "tools/cks_v1_4_dashboard_runtime.py",
)


class SelfAudit:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.findings: list[Finding] = []

    def add(self, level: str, code: str, path: str, message: str) -> None:
        self.findings.append(Finding(level, code, path, message))

    def check_required_paths(self) -> None:
        for rel in REQUIRED_PATHS:
            if not (self.root / rel).exists():
                self.add("FAIL", "REQUIRED_PATH_MISSING", rel, "Обязательный элемент CKS отсутствует")

    def check_system_state(self) -> None:
        rel = "control/system-state.yaml"
        path = self.root / rel
        if not path.exists():
            return
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in (
            "current_version:",
            "core: frozen",
            "experiments: isolated",
            "proposal_is_not_decision: true",
            "experiment_is_not_canon: true",
        ):
            if marker not in text:
                self.add("FAIL", "SYSTEM_STATE_CONTRACT", rel, f"Нет обязательного признака: {marker}")

    def check_ssot_registry(self) -> None:
        rel = "control/ssot-registry.yaml"
        path = self.root / rel
        if not path.exists():
            return
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in (
            "architecture:",
            "schemas:",
            "decisions:",
            "knowledge:",
            "evidence:",
            "runtime:",
            "path: tools/",
            "runtime_rules:",
            "path: engine/",
            "obsidian_views:",
            "authority: derived_view_only",
        ):
            if marker not in text:
                self.add("FAIL", "SSOT_REGISTRY_CONTRACT", rel, f"Нет обязательного признака SSOT: {marker}")
        if not (self.root / "tools").is_dir():
            self.add("FAIL", "SSOT_RUNTIME_PATH", "tools/", "Реестр указывает runtime в tools/, но каталог отсутствует")
        if not (self.root / "engine").is_dir():
            self.add("FAIL", "SSOT_RUNTIME_RULES_PATH", "engine/", "Реестр указывает runtime_rules в engine/, но каталог отсутствует")
        if not (self.root / "obsidian").is_dir():
            self.add("FAIL", "SSOT_OBSIDIAN_PATH", "obsidian/", "Реестр указывает Obsidian-представления, но каталог отсутствует")

    def check_language_policy(self) -> None:
        rel = "docs/ADR-007_Двуязычная_модель_документации_CKS.md"
        path = self.root / rel
        if not path.exists():
            return
        text = path.read_text(encoding="utf-8", errors="replace")
        if "Русский язык является основным языком описания архитектуры" not in text:
            self.add("FAIL", "LANGUAGE_POLICY_MISSING", rel, "Не подтверждено правило русского архитектурного слоя")
        if "docs/ГЛОССАРИЙ.md" not in text:
            self.add("WARN", "GLOSSARY_REFERENCE_MISSING", rel, "Не найдена ссылка на единый глоссарий")

    def check_knowledge_model_contract(self) -> None:
        rel = "schemas/cks-knowledge-object.schema.json"
        path = self.root / rel
        if not path.exists():
            return
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self.add("FAIL", "KNOWLEDGE_SCHEMA_JSON", rel, f"Схема не является корректным JSON: {exc}")
            return
        properties = schema.get("properties") or {}
        for field in ("clusters", "tags", "projects", "relations", "history", "signals", "obsidian"):
            if field not in properties:
                self.add("FAIL", "KNOWLEDGE_SCHEMA_FIELD", rel, f"Нет поля модели знаний: {field}")
        statuses = set(((properties.get("status") or {}).get("enum") or []))
        for status in ("raw", "clustered", "validated", "knowledge", "canonical", "evolving", "archived"):
            if status not in statuses:
                self.add("FAIL", "KNOWLEDGE_STATUS_MISSING", rel, f"Нет статуса развития знания: {status}")

    def check_python_syntax(self) -> None:
        for rel in RUNTIME_MODULES:
            path = self.root / rel
            if not path.exists():
                continue
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                self.add("FAIL", "PYTHON_SYNTAX", rel, str(exc))

    def check_runtime_contract(self) -> None:
        tools = self.root / "tools"
        sys.path.insert(0, str(tools))
        try:
            from cks_knowledge_graph_runtime import GraphError, KnowledgeGraph
            from cks_traceability_engine import TraceabilityEngine
            from cks_knowledge_runtime import KnowledgeRuntime
            from cks_knowledge_intelligence import KnowledgeIntelligence

            graph = KnowledgeGraph()
            graph.add_node("CKS-EVD-9001", "evidence")
            graph.add_node("CKS-KNW-9001", "knowledge")
            graph.add_node("CKS-DEC-9001", "decision")
            graph.add_edge("CKS-KNW-9001", "CKS-EVD-9001", "evidenced_by")
            graph.add_edge("CKS-KNW-9001", "CKS-DEC-9001", "decided_by")
            if graph.validate()["status"] == "FAIL":
                self.add("FAIL", "GRAPH_RUNTIME", "tools/cks_knowledge_graph_runtime.py", "Рабочий граф не прошёл внутреннюю проверку")
            try:
                graph.add_edge("CKS-KNW-9001", "CKS-MISSING-1", "depends_on")
                self.add("FAIL", "GRAPH_BROKEN_REF_ACCEPTED", "tools/cks_knowledge_graph_runtime.py", "Граф принял ссылку на отсутствующий узел")
            except GraphError:
                pass

            trace = TraceabilityEngine()
            trace_result = trace.ingest([
                {"id": "CKS-EVD-9001", "type": "evidence"},
                {"id": "CKS-DEC-9001", "type": "decision"},
                {"id": "CKS-KNW-9001", "type": "knowledge", "evidence": ["CKS-EVD-9001"], "decision": "CKS-DEC-9001"},
            ])
            if trace_result["status"] == "FAIL" or trace_result["edges"] != 2:
                self.add("FAIL", "TRACE_RUNTIME", "tools/cks_traceability_engine.py", "Цепочка происхождения строится некорректно")

            knowledge = KnowledgeRuntime()
            validation = knowledge.ingest([
                {
                    "id": "CKS-KNW-9201", "type": "knowledge", "status": "knowledge", "owner": "CKS", "lifecycle": "knowledge",
                    "clusters": ["архитектура"], "tags": ["cks", "runtime"], "projects": ["CKS"], "relations": [],
                    "evidence": ["CKS-EVD-9001"], "history": [{"status": "validated"}],
                },
                {
                    "id": "CKS-KNW-9202", "type": "knowledge", "status": "evolving", "owner": "CKS", "lifecycle": "knowledge",
                    "clusters": ["архитектура"], "tags": ["cks", "runtime"], "projects": ["CKS"], "relations": [],
                    "evidence": ["CKS-EVD-9001"], "history": [{"status": "clustered"}],
                },
            ])
            if validation["status"] != "PASS":
                self.add("FAIL", "KNOWLEDGE_RUNTIME", "tools/cks_knowledge_runtime.py", "Рабочий контур знаний не принял эталонные объекты")
            if "архитектура" not in knowledge.dynamic_views().get("по_кластерам", {}):
                self.add("FAIL", "KNOWLEDGE_VIEWS", "tools/cks_knowledge_runtime.py", "Не построено кластерное представление")
            intelligence = KnowledgeIntelligence(knowledge)
            if not intelligence.hidden_links(threshold=0.3):
                self.add("FAIL", "KNOWLEDGE_INTELLIGENCE_LINKS", "tools/cks_knowledge_intelligence.py", "Не найден ожидаемый кандидат скрытой связи")
            if intelligence.quality_audit().get("authority") != "diagnostic_only":
                self.add("FAIL", "KNOWLEDGE_INTELLIGENCE_AUTHORITY", "tools/cks_knowledge_intelligence.py", "Самоаудит знаний должен оставаться диагностическим")
        except Exception as exc:
            self.add("FAIL", "RUNTIME_IMPORT_OR_EXECUTION", "tools", f"Ошибка рабочего контура: {exc}")
        finally:
            if sys.path and sys.path[0] == str(tools):
                sys.path.pop(0)

    def check_compatibility_layers(self) -> None:
        """Проверить, что исторические интерфейсы не деградировали в заглушки."""
        tools = self.root / "tools"
        sys.path.insert(0, str(tools))
        try:
            from cks_compatibility_audit import run_compatibility_audit

            result = run_compatibility_audit()
            if result.get("status") != "PASS":
                failed = ", ".join(result.get("failed_checks") or []) or "неизвестная ошибка"
                self.add(
                    "FAIL",
                    "COMPATIBILITY_LAYER_INTEGRITY",
                    "tools/cks_compatibility_audit.py",
                    f"Compatibility-слои не прошли содержательную проверку: {failed}",
                )
        except Exception as exc:
            self.add(
                "FAIL",
                "COMPATIBILITY_LAYER_EXECUTION",
                "tools/cks_compatibility_audit.py",
                f"Ошибка проверки compatibility-слоёв: {exc}",
            )
        finally:
            if sys.path and sys.path[0] == str(tools):
                sys.path.pop(0)

    def run(self) -> dict[str, object]:
        self.check_required_paths()
        self.check_system_state()
        self.check_ssot_registry()
        self.check_language_policy()
        self.check_knowledge_model_contract()
        self.check_python_syntax()
        self.check_runtime_contract()
        self.check_compatibility_layers()
        failures = sum(1 for x in self.findings if x.level == "FAIL")
        warnings = sum(1 for x in self.findings if x.level == "WARN")
        return {
            "schema_version": "1.3",
            "kind": "cks_self_audit",
            "status": "FAIL" if failures else ("WARN" if warnings else "PASS"),
            "summary": {"fail": failures, "warn": warnings},
            "findings": [asdict(x) for x in self.findings],
            "authority": "diagnostic_only",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: самопроверка архитектуры, Runtime и compatibility-слоёв")
    parser.add_argument("--root", default=".")
    parser.add_argument("--report")
    args = parser.parse_args()
    result = SelfAudit(args.root).run()
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        report = Path(args.report)
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
