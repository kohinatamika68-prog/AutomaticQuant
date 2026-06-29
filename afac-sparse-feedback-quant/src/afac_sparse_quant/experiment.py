from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class SparseFeedbackState(str, Enum):
    PROPOSED = "proposed"
    RUNNING = "running"
    PARTIAL = "partial"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"


@dataclass(frozen=True)
class Experiment:
    """Public experiment record with sanitized metadata."""

    experiment_id: str
    candidate_family: str
    state: SparseFeedbackState
    score: float | None = None
    turnover_band: str | None = None
    diversity_band: str | None = None
    failure_reason: str | None = None

    @classmethod
    def from_dict(cls, item: dict) -> "Experiment":
        return cls(
            experiment_id=str(item["experiment_id"]),
            candidate_family=str(item["candidate_family"]),
            state=SparseFeedbackState(str(item["state"])),
            score=item.get("score"),
            turnover_band=item.get("turnover_band"),
            diversity_band=item.get("diversity_band"),
            failure_reason=item.get("failure_reason"),
        )


def summarize_experiments(experiments: Iterable[Experiment]) -> dict[str, object]:
    rows = list(experiments)
    by_state: dict[str, int] = {}
    by_family: dict[str, int] = {}
    failures: dict[str, int] = {}
    scored = [row.score for row in rows if row.score is not None]

    for row in rows:
        by_state[row.state.value] = by_state.get(row.state.value, 0) + 1
        by_family[row.candidate_family] = by_family.get(row.candidate_family, 0) + 1
        if row.failure_reason:
            failures[row.failure_reason] = failures.get(row.failure_reason, 0) + 1

    return {
        "total": len(rows),
        "by_state": by_state,
        "by_family": by_family,
        "failures": failures,
        "average_score": sum(scored) / len(scored) if scored else None,
    }
