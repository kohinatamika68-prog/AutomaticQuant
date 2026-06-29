from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Mapping, Sequence


@dataclass(frozen=True)
class CorrelationPair:
    left: str
    right: str
    correlation: float
    severity: str


@dataclass(frozen=True)
class CorrelationCluster:
    members: tuple[str, ...]
    representative: str
    review: tuple[str, ...]


@dataclass(frozen=True)
class CorrelationReport:
    matrix: dict[str, dict[str, float]]
    pairs: tuple[CorrelationPair, ...]
    clusters: tuple[CorrelationCluster, ...]


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
    if len(names) < 2:
        raise ValueError("at least two PnL series are required")

    returns = {name: daily_returns(values) for name, values in cumulative_pnls.items()}
    lengths = {len(values) for values in returns.values()}
    if len(lengths) != 1:
        raise ValueError("all PnL series must have the same number of observations")
    if next(iter(lengths)) < 2:
        raise ValueError("each PnL series must contain at least three cumulative observations")

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
                pairs.append(CorrelationPair(left, right, corr, _severity(abs(corr))))
    pairs.sort(key=lambda p: abs(p.correlation), reverse=True)
    return pairs


def analyze_correlations(
    cumulative_pnls: Mapping[str, Sequence[float]],
    threshold: float = 0.70,
    scores: Mapping[str, float] | None = None,
) -> CorrelationReport:
    """Build a matrix, high-correlation pairs, and connected clusters."""
    matrix = correlation_matrix(cumulative_pnls)
    pairs = tuple(high_correlation_pairs(cumulative_pnls, threshold=threshold))
    clusters = tuple(_build_clusters(pairs, list(cumulative_pnls), scores=scores))
    return CorrelationReport(matrix=matrix, pairs=pairs, clusters=clusters)


def report_to_dict(report: CorrelationReport) -> dict[str, object]:
    return {
        "matrix": report.matrix,
        "pairs": [
            {
                "left": pair.left,
                "right": pair.right,
                "correlation": pair.correlation,
                "severity": pair.severity,
            }
            for pair in report.pairs
        ],
        "clusters": [
            {
                "members": list(cluster.members),
                "representative": cluster.representative,
                "review": list(cluster.review),
            }
            for cluster in report.clusters
        ],
    }


def _severity(abs_corr: float) -> str:
    if abs_corr >= 0.90:
        return "critical"
    if abs_corr >= 0.80:
        return "high"
    return "medium"


def _build_clusters(
    pairs: Sequence[CorrelationPair],
    names: Sequence[str],
    scores: Mapping[str, float] | None = None,
) -> list[CorrelationCluster]:
    parent = {name: name for name in names}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        root_a = find(a)
        root_b = find(b)
        if root_a != root_b:
            parent[root_b] = root_a

    for pair in pairs:
        union(pair.left, pair.right)

    groups: dict[str, list[str]] = {}
    for name in names:
        groups.setdefault(find(name), []).append(name)

    clusters: list[CorrelationCluster] = []
    for members in groups.values():
        if len(members) < 2:
            continue
        ordered = tuple(sorted(members))
        representative = _choose_representative(ordered, scores=scores)
        review = tuple(name for name in ordered if name != representative)
        clusters.append(CorrelationCluster(ordered, representative, review))

    clusters.sort(key=lambda c: (-len(c.members), c.representative))
    return clusters


def _choose_representative(members: Sequence[str], scores: Mapping[str, float] | None) -> str:
    if scores:
        return max(members, key=lambda name: (scores.get(name, float("-inf")), name))
    return sorted(members)[0]
