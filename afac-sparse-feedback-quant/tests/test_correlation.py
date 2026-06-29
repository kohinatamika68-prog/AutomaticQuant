from afac_sparse_quant.correlation import daily_returns, high_correlation_pairs


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
