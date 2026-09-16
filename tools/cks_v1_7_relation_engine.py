"""CKS v1.7 Relation Engine foundation."""

class RelationEngine:
    def __init__(self):
        self.relations = []

    def add_relation(self, source, target, relation):
        self.relations.append({
            "source": source,
            "target": target,
            "relation": relation,
        })
        return True

    def find(self, relation=None):
        if relation is None:
            return self.relations
        return [r for r in self.relations if r["relation"] == relation]
