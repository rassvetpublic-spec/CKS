"""CKS v1.7 Graph Validator.
Validates structural graph quality without making decisions.
"""


def validate_graph(nodes, edges):
    issues = []
    node_ids = {n.get('id') for n in nodes}
    for edge in edges:
        if edge.get('source') not in node_ids or edge.get('target') not in node_ids:
            issues.append('broken_edge_reference')
    return issues
