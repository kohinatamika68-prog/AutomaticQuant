"""Sparse Feedback Quant public toolkit."""

from .correlation import (
    CorrelationCluster,
    CorrelationPair,
    CorrelationReport,
    analyze_correlations,
    daily_returns,
    high_correlation_pairs,
    report_to_dict,
)
from .experiment import Experiment, SparseFeedbackState, summarize_experiments, validate_experiment_payload
from .factor import FactorCandidate
from .memory import build_research_note
from .metrics import PnlMetrics, compute_metrics_table, compute_pnl_metrics, metrics_to_dict
from .selection import SelectionReport, select_candidates, selection_to_dict

__all__ = [
    "CorrelationPair",
    "CorrelationCluster",
    "CorrelationReport",
    "Experiment",
    "FactorCandidate",
    "PnlMetrics",
    "SelectionReport",
    "SparseFeedbackState",
    "analyze_correlations",
    "build_research_note",
    "compute_metrics_table",
    "compute_pnl_metrics",
    "daily_returns",
    "high_correlation_pairs",
    "metrics_to_dict",
    "report_to_dict",
    "select_candidates",
    "selection_to_dict",
    "summarize_experiments",
    "validate_experiment_payload",
]
