"""CKS context quality validation placeholder.

Checks that candidate objects contain structured metadata.
"""

REQUIRED_FIELDS = ["id", "source", "status"]


def validate_context_object(obj):
    return all(field in obj for field in REQUIRED_FIELDS)


if __name__ == "__main__":
    print("CKS context quality check ready")
