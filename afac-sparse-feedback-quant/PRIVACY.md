# Privacy And Publication Boundary

This project is designed to publish reusable sparse-feedback research patterns
with clear boundaries around private research assets.

## Allowed In This Repository

- Synthetic PnL examples.
- Generic factor families such as value, quality, momentum, sentiment, and
  analyst revision.
- Abstract experiment outcomes such as `accepted`, `rejected`, `timeout`, and
  `needs_review`.
- General lessons such as "use return deltas for correlation checks."
- Public challenge definitions and reproducibility harnesses.

## Not Allowed In This Repository

- Exact high-score model configurations.
- Private model weights, prompts, seeds, hyperparameters, or feature recipes.
- Real factor expressions from competitive or private platforms.
- Account-linked IDs, submission logs, screenshots, API responses, or PnL.
- Any hidden leaderboard strategy, threshold schedule, or tuning workflow.

## Sanitization Rule

Before publishing an observation, convert it from:

```text
specific private artifact -> general mechanism -> reusable public lesson
```

Example:

```text
Do not publish:
  Candidate X with exact formula Y passed after setting private parameter Z.

Publish:
  Candidates that only change smoothing are often still correlated; seek a
  different economic family or data cadence before spending more trials.
```
