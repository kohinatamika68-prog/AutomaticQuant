from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .correlation import analyze_correlations
from .metrics import PnlMetrics, compute_metrics_table, metrics_to_dict


@dataclass(frozen=True)
class SelectionReport:
    selected: tuple[str, ...]
    review: tuple[str, ...]
    metrics: dict[str, PnlMetrics]
    reasons: dict[str, str]


def select_candidates(
    cumulative_pnls: Mapping[str, Sequence[float]],
    threshold: float = 0.70,
    top: int | None = None,
) -> SelectionReport:
    """Select candidates by score while avoiding high-correlation duplicates."""
    metrics = compute_metrics_table(cumulative_pnls)
    scores = {name: _selection_score(row) for name, row in metrics.items()}
    corr = analyze_correlations(cumulative_pnls, threshold=threshold, scores=scores)

    selected: set[str] = set()
    review: set[str] = set()
    reasons: dict[str, str] = {}

    clustered = set()
    for cluster in corr.clusters:
        clustered.update(cluster.members)
        selected.add(cluster.representative)
        reasons[cluster.representative] = "cluster representative with strongest selection score"
        for name in cluster.review:
            review.add(name)
            reasons[name] = f"highly correlated with representative {cluster.representative}"

    for name in metrics:
        if name not in clustered:
            selected.add(name)
            reasons[name] = "independent candidate"

    ordered_selected = sorted(selected, key=lambda name: scores[name], reverse=True)
    if top is not None:
        kept = tuple(ordered_selected[:top])
        overflow = ordered_selected[top:]
        for name in overflow:
            review.add(name)
            reasons[name] = "below top selection cutoff"
    else:
        kept = tuple(ordered_selected)

    ordered_review = tuple(sorted(review - set(kept), key=lambda name: scores[name], reverse=True))
    return SelectionReport(selected=kept, review=ordered_review, metrics=metrics, reasons=reasons)


def selection_to_dict(report: SelectionReport) -> dict[str, object]:
    return {
        "selected": list(report.selected),
        "review": list(report.review),
        "metrics": {name: metrics_to_dict(row) for name, row in report.metrics.items()},
        "reasons": report.reasons,
    }


def _selection_score(metrics: PnlMetrics) -> float:
    drawdown_penalty = abs(metrics.max_drawdown) * 0.05
    return metrics.sharpe_like + metrics.hit_rate * 0.25 + metrics.total_pnl * 0.01 - drawdown_penalty
