# Architecture

AFAC Sparse Feedback Quant is organized around a public research loop:

```text
candidate proposal
  -> sparse or delayed evaluation
  -> public outcome normalization
  -> diversity and correlation checks
  -> sanitized research note
  -> human review before playbook update
```

## Components

### Experiment State

`Experiment` stores only public-safe metadata:

- experiment id
- factor family
- sparse feedback state
- public score
- turnover band
- diversity band
- failure reason

It does not store private formulas, exact tuning, prompts, seeds, or platform
responses.

### Factor Candidate

`FactorCandidate` describes a candidate at mechanism level:

- family
- cadence
- expected turnover
- feedback channel
- risk notes

This keeps the public project useful without leaking recipe-level details.

### Correlation Guard

The correlation guard converts cumulative PnL into daily deltas before
computing Pearson correlation. This avoids the common mistake of comparing
cumulative curves, which can overstate similarity for unrelated profitable
series.

### Research Memory

`build_research_note` turns experiment records into a Markdown summary. The
generated note is intentionally review-first: it should be inspected before it
is copied into a public playbook.
