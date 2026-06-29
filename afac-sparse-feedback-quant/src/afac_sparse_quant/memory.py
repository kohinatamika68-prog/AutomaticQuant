from __future__ import annotations

from .experiment import Experiment, SparseFeedbackState, summarize_experiments


def build_research_note(experiments: list[Experiment]) -> str:
    """Build a sanitized Markdown note from public experiment records."""
    summary = summarize_experiments(experiments)
    lines = [
        "## Sparse Feedback Research Note",
        "",
        f"- Total experiments: {summary['total']}",
        f"- State distribution: {summary['by_state']}",
        f"- Candidate families: {summary['by_family']}",
    ]
    if summary["average_score"] is not None:
        lines.append(f"- Average public score: {summary['average_score']:.4f}")
    if summary["failures"]:
        lines.append(f"- Failure taxonomy: {summary['failures']}")

    accepted = [row for row in experiments if row.state == SparseFeedbackState.ACCEPTED]
    rejected = [row for row in experiments if row.state == SparseFeedbackState.REJECTED]
    review = [row for row in experiments if row.state == SparseFeedbackState.NEEDS_REVIEW]

    lines.extend(["", "### Public Lessons"])
    if accepted:
        families = sorted({row.candidate_family for row in accepted})
        lines.append(f"- Accepted candidates came from these public families: {', '.join(families)}.")
    if rejected:
        reasons = sorted({row.failure_reason or "unspecified" for row in rejected})
        lines.append(f"- Rejections should be grouped by mechanism before another trial: {', '.join(reasons)}.")
    if review:
        lines.append("- Partial or ambiguous feedback should trigger review instead of blind parameter search.")

    lines.append("- Correlation checks should use daily PnL deltas, not cumulative PnL levels.")
    lines.append("- Promote mechanism-level lessons into the playbook after review.")
    return "\n".join(lines) + "\n"
