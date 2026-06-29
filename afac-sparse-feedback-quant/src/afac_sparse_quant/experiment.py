from __future__ import annotations

from dataclasses import asdict, dataclass
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

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["state"] = self.state.value
        return data


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


def validate_experiment_payload(payload: dict) -> list[str]:
    """Return human-readable validation errors for an experiment JSON payload."""
    errors: list[str] = []
    rows = payload.get("experiments")
    if not isinstance(rows, list):
        return ["payload must contain an 'experiments' list"]

    seen_ids: set[str] = set()
    for idx, row in enumerate(rows):
        prefix = f"experiments[{idx}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in ("experiment_id", "candidate_family", "state"):
            if key not in row or row[key] in ("", None):
                errors.append(f"{prefix}.{key} is required")
        exp_id = str(row.get("experiment_id", ""))
        if exp_id in seen_ids:
            errors.append(f"{prefix}.experiment_id duplicates '{exp_id}'")
        seen_ids.add(exp_id)
        state = row.get("state")
        if state is not None and str(state) not in {item.value for item in SparseFeedbackState}:
            errors.append(f"{prefix}.state has unsupported value '{state}'")
        score = row.get("score")
        if score is not None and not isinstance(score, int | float):
            errors.append(f"{prefix}.score must be numeric when present")
    return errors
