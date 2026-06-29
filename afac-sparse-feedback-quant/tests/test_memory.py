from afac_sparse_quant.experiment import Experiment, SparseFeedbackState
from afac_sparse_quant.memory import build_research_note


def test_research_note_is_sanitized_and_actionable():
    note = build_research_note(
        [
            Experiment("x1", "quality", SparseFeedbackState.ACCEPTED, score=1.0),
            Experiment("x2", "momentum", SparseFeedbackState.REJECTED, score=0.1, failure_reason="turnover"),
        ]
    )
    assert "Sparse Feedback Research Note" in note
    assert "quality" in note
    assert "turnover" in note
    assert "exact recipes" in note
