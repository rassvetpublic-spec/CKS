#!/usr/bin/env python3
"""Совместимый движок связей CKS.

Сохраняет старый интерфейс RelationEngine, но использует реальный рабочий граф
из cks_knowledge_graph_runtime.py. Новые компоненты должны обращаться к
KnowledgeGraph напрямую.
"""
from __future__ import annotations

from cks_knowledge_graph_runtime import KnowledgeGraph


class RelationEngine:
    def __init__(self):
        self.graph = KnowledgeGraph()

    @property
    def relations(self):
        return self.graph.edges

    def add_relation(self, source, target, relation):
        # Старый интерфейс не передавал сведения об узлах, поэтому совместимый
        # слой создаёт технические узлы unknown. Основной runtime так не делает.
        if source not in self.graph.nodes:
            self.graph.add_node(str(source), "unknown")
        if target not in self.graph.nodes:
            self.graph.add_node(str(target), "unknown")
        self.graph.add_edge(str(source), str(target), str(relation))
        return True

    def find(self, relation=None):
        if relation is None:
            return list(self.graph.edges)
        return [item for item in self.graph.edges if item["relation"] == relation]
