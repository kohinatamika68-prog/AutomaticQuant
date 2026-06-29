from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Mapping, Sequence


@dataclass(frozen=True)
class CorrelationPair:
    left: str
    right: str
    correlation: float


def daily_returns(cumulative_pnl: Sequence[float]) -> list[float]:
    """Convert cumulative PnL into daily PnL deltas."""
    return [float(cumulative_pnl[i + 1]) - float(cumulative_pnl[i]) for i in range(len(cumulative_pnl) - 1)]


def pearson(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y):
        raise ValueError("series must have the same length")
    if len(x) < 2:
        raise ValueError("series must contain at least two observations")

    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    dx = [v - mean_x for v in x]
    dy = [v - mean_y for v in y]
    denom = sqrt(sum(v * v for v in dx) * sum(v * v for v in dy))
    if denom == 0:
        return 0.0
    return sum(a * b for a, b in zip(dx, dy)) / denom


def correlation_matrix(cumulative_pnls: Mapping[str, Sequence[float]]) -> dict[str, dict[str, float]]:
    """Compute daily-return correlations for cumulative PnL series."""
    names = list(cumulative_pnls)
    returns = {name: daily_returns(values) for name, values in cumulative_pnls.items()}
    matrix: dict[str, dict[str, float]] = {name: {} for name in names}

    for left in names:
        for right in names:
            matrix[left][right] = 1.0 if left == right else pearson(returns[left], returns[right])
    return matrix


def high_correlation_pairs(
    cumulative_pnls: Mapping[str, Sequence[float]],
    threshold: float = 0.70,
) -> list[CorrelationPair]:
    """Return strategy pairs whose absolute daily-return correlation is high."""
    matrix = correlation_matrix(cumulative_pnls)
    names = list(cumulative_pnls)
    pairs: list[CorrelationPair] = []
    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            corr = matrix[left][right]
            if abs(corr) >= threshold:
                pairs.append(CorrelationPair(left, right, corr))
    pairs.sort(key=lambda p: abs(p.correlation), reverse=True)
    return pairs
