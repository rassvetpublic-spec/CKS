"""Detect graph nodes without relations."""


def find_orphans(nodes, edges):
    linked = set()
    for edge in edges:
        linked.add(edge.get('source'))
        linked.add(edge.get('target'))
    return [n for n in nodes if n.get('id') not in linked]
