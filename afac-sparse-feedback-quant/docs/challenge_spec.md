# Open Challenge Spec

This project can host an open challenge named:

**Sparse Feedback Automation Meets Quantitative Factor Mining**

## Task

Build an agent that proposes sanitized factor candidates, evaluates sparse
feedback, avoids redundant candidates, and writes reviewable research notes.

## Public Inputs

- Synthetic candidate metadata.
- Synthetic cumulative PnL series.
- Delayed outcome records.
- Public failure labels.

## Public Outputs

- Candidate state transitions.
- High-correlation warnings.
- Failure taxonomy summary.
- Sanitized Markdown research note.

## Scoring Ideas

- Feedback efficiency: useful decisions per trial.
- Diversity: fewer high-correlation accepted candidates.
- Robustness: graceful handling of missing or partial feedback.
- Memory quality: concise lessons that do not expose private recipes.

## Non-Goals

- Replicating high-score configurations from private competitions.
- Publishing private alpha expressions.
- Measuring real trading performance.
- Encouraging platform-specific rule circumvention.
