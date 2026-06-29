from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FactorCandidate:
    """Sanitized factor metadata without private formulas or tuning details."""

    name: str
    family: str
    cadence: str
    expected_turnover: str
    feedback_channel: str
    risk_notes: tuple[str, ...] = field(default_factory=tuple)

    def public_description(self) -> str:
        notes = "; ".join(self.risk_notes) if self.risk_notes else "no extra notes"
        return (
            f"{self.name}: family={self.family}, cadence={self.cadence}, "
            f"expected_turnover={self.expected_turnover}, feedback={self.feedback_channel}, "
            f"risk={notes}"
        )
