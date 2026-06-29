"""Compatibility package for Sparse Feedback Quant."""

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

__all__ = [
    "CorrelationPair",
    "CorrelationCluster",
    "CorrelationReport",
    "Experiment",
    "FactorCandidate",
    "SparseFeedbackState",
    "analyze_correlations",
    "build_research_note",
    "daily_returns",
    "high_correlation_pairs",
    "report_to_dict",
    "summarize_experiments",
    "validate_experiment_payload",
]
