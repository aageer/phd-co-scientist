---
name: clipping-hallucinations
description: Use when a draft contains numbers, metrics, or empirical claims that must be checked against execution logs
---

# Clipping Hallucinations

## Overview

Hard verification against E_log. Soft penalties are not enough (paper §2.1.2).

## Instructions

1. Parse quantitative claims (scores, counts, percentages, call budgets).
2. Match each to a log token (exact or rounding).
3. Rewrite misses with the logged value, or mark `[UNVERIFIED]`.
4. If there is no log, HALT paper writing.
5. Encourage verbose logging upstream so this module has evidence.

```python
from swarm.reliability import hallucination_score
clip = hallucination_score(manuscript, Path("execution.log").read_text())
```

## Examples

Paper: "accuracy of 99.7". Log: `score=0.42`. → clip 99.7, keep 0.42 if present.

## Performance Notes

Deterministic and cheap. Run after every draft mutation.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Everything clipped | Logs are too terse. Change solve.py to print JSON. |
| Model "remembers" a paper number | That is not E_log. Clip it. |
