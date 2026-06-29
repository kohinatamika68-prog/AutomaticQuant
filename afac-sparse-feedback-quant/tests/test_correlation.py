from sparse_feedback_quant.correlation import analyze_correlations, daily_returns, high_correlation_pairs, report_to_dict
from sparse_feedback_quant.metrics import compute_pnl_metrics
from sparse_feedback_quant.selection import select_candidates, selection_to_dict


def test_daily_returns_uses_deltas():
    assert daily_returns([1.0, 1.5, 1.25]) == [0.5, -0.25]


def test_high_correlation_pairs_detects_variants():
    series = {
        "a": [0, 1, 3, 2, 5],
        "b": [0, 2, 6, 4, 10],
        "c": [0, -1, 0, -1, 0],
    }
    pairs = high_correlation_pairs(series, threshold=0.9)
    assert pairs[0].left == "a"
    assert pairs[0].right == "b"
    assert pairs[0].correlation == 1.0
    assert pairs[0].severity == "critical"


def test_analyze_correlations_builds_clusters_and_representative():
    series = {
        "a": [0, 1, 3, 2, 5],
        "b": [0, 2, 6, 4, 10],
        "c": [0, -1, 0, -1, 0],
    }
    report = analyze_correlations(series, threshold=0.9, scores={"a": 0.7, "b": 1.2})
    assert report.clusters[0].representative == "b"
    assert report.clusters[0].review == ("a",)
    data = report_to_dict(report)
    assert data["clusters"][0]["members"] == ["a", "b"]


def test_compute_pnl_metrics_and_select_candidates():
    series = {
        "a": [0, 1, 3, 2, 5],
        "b": [0, 2, 6, 4, 10],
        "c": [0, -1, 0, -1, 0],
    }
    metrics = compute_pnl_metrics("a", series["a"])
    assert metrics.total_pnl == 5.0
    assert metrics.max_drawdown == -1.0

    report = select_candidates(series, threshold=0.9)
    data = selection_to_dict(report)
    assert "b" in data["selected"]
    assert "a" in data["review"]
