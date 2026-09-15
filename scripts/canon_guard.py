"""CKS canon protection skeleton."""


def can_promote_to_canon(record):
    return bool(record.get("evidence")) and record.get("status") == "accepted"


if __name__ == "__main__":
    print("CKS canon guard ready")
