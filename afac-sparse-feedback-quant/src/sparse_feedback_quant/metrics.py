from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Mapping, Sequence

from .correlation import daily_returns


@dataclass(frozen=True)
class PnlMetrics:
    name: str
    observations: int
    total_pnl: float
    mean_daily_pnl: float
    volatility: float
    sharpe_like: float
    max_drawdown: float
    hit_rate: float


def compute_pnl_metrics(name: str, cumulative_pnl: Sequence[float]) -> PnlMetrics:
    if len(cumulative_pnl) < 3:
        raise ValueError("each PnL series must contain at least three cumulative observations")

    values = [float(v) for v in cumulative_pnl]
    returns = daily_returns(values)
    mean_ret = sum(returns) / len(returns)
    variance = sum((ret - mean_ret) ** 2 for ret in returns) / len(returns)
    volatility = sqrt(variance)
    sharpe_like = mean_ret / volatility if volatility else 0.0
    hit_rate = sum(1 for ret in returns if ret > 0) / len(returns)
    return PnlMetrics(
        name=name,
        observations=len(values),
        total_pnl=values[-1] - values[0],
        mean_daily_pnl=mean_ret,
        volatility=volatility,
        sharpe_like=sharpe_like,
        max_drawdown=_max_drawdown(values),
        hit_rate=hit_rate,
    )


def compute_metrics_table(cumulative_pnls: Mapping[str, Sequence[float]]) -> dict[str, PnlMetrics]:
    return {name: compute_pnl_metrics(name, values) for name, values in cumulative_pnls.items()}


def metrics_to_dict(metrics: PnlMetrics) -> dict[str, object]:
    return {
        "name": metrics.name,
        "observations": metrics.observations,
        "total_pnl": metrics.total_pnl,
        "mean_daily_pnl": metrics.mean_daily_pnl,
        "volatility": metrics.volatility,
        "sharpe_like": metrics.sharpe_like,
        "max_drawdown": metrics.max_drawdown,
        "hit_rate": metrics.hit_rate,
    }


def _max_drawdown(values: Sequence[float]) -> float:
    peak = float(values[0])
    worst = 0.0
    for value in values:
        current = float(value)
        peak = max(peak, current)
        worst = min(worst, current - peak)
    return worst
