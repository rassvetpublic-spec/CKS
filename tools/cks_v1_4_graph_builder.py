"""CKS v1.4 Knowledge Graph builder prototype.

Graph is an analysis layer and is not a source of truth.
"""


def build_graph(objects):
    nodes = []
    edges = []

    for obj in objects:
        nodes.append({"id": obj.get("id"), "type": obj.get("type")})
        for relation in obj.get("relations", []):
            edges.append(relation)

    return {"nodes": nodes, "edges": edges}
