"""CKS v1.4 Metrics Calculator prototype.

Calculates diagnostic scores only. It does not create Canon or Decisions.
"""

from dataclasses import dataclass


@dataclass
class KnowledgeMetrics:
    completeness: int
    evidence: int
    freshness: int
    consistency: int

    @property
    def health_score(self) -> int:
        return round((self.completeness + self.evidence + self.freshness + self.consistency) / 4)


def calculate_health(metrics: KnowledgeMetrics) -> dict:
    return {
        "health_score": metrics.health_score,
        "evidence_score": metrics.evidence,
        "freshness_score": metrics.freshness,
        "consistency_score": metrics.consistency,
    }
