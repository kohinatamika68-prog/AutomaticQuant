from sparse_feedback_quant.experiment import Experiment, SparseFeedbackState, validate_experiment_payload
from sparse_feedback_quant.memory import build_research_note


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
    assert "mechanism-level lessons" in note


def test_validate_experiment_payload_catches_bad_rows():
    errors = validate_experiment_payload(
        {
            "experiments": [
                {"experiment_id": "x", "candidate_family": "quality", "state": "accepted"},
                {"experiment_id": "x", "candidate_family": "", "state": "unknown", "score": "bad"},
            ]
        }
    )
    assert any("duplicates" in error for error in errors)
    assert any("unsupported" in error for error in errors)
    assert any("score" in error for error in errors)
