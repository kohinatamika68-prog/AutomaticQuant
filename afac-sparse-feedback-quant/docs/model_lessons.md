# Model Lessons For Sparse Feedback Research

These lessons are intentionally abstract. They capture model behavior patterns
without revealing high-score configurations.

## Lessons

1. Optimize the research loop, not only the candidate generator.

   In sparse feedback settings, better state tracking and failure attribution
   can matter more than generating more candidates.

2. Treat delayed feedback as a system design constraint.

   A candidate should move through explicit states such as `running`,
   `partial`, `needs_review`, `accepted`, or `rejected`. Blind retries hide
   useful error signals.

3. Separate score improvement from diversity improvement.

   A stronger local score can still be redundant at the portfolio level.
   Diversity checks should be part of the acceptance gate.

4. Use mechanism families, not private formulas, as public labels.

   Publishing "quality with slow cadence" is useful; publishing exact private
   feature recipes is not.

5. Convert experiments into reviewable notes.

   The public artifact should be a general lesson after human review, not a raw
   transcript of model behavior.

## Red Lines

Do not publish exact:

- model architecture decisions;
- hyperparameter grids;
- prompt chains;
- leaderboard-specific heuristics;
- factor formulas;
- private thresholds.
