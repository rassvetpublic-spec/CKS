"""CKS v1.3 -> v1.4 migration adapter prototype."""


def migrate_object(obj):
    result = dict(obj)
    result.setdefault("version", "1.4")
    result.setdefault("relations", [])
    result.setdefault("metrics", {})
    return result
