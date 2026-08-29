---
name: discovering-agent-architectures
description: Use when the research goal is to find an inference-time scaffold (Agent_H-like) or beat a backbone on a held-out agent benchmark
---

# Discovering Agent Architectures

## Overview

This is the CS track from Figure 1f: fully autonomous architecture search. HealthBench is an *eval*, not a product.

## Instructions

Search in the Agent_H neighborhood only as a **baseline**, then change one mechanism:

1. Triage + adaptive tier
2. Decomposition
3. Parallel candidates (personas × temperatures)
4. Tournament + ensemble judges
5. Critique loop
6. Metacognitive coverage check
7. Citation / schema audit
8. Length calibration (2k-char pivot in the paper)

Rules:

- Never train on or peek at held-out rubrics.
- Report raw **and** length-adjusted scores.
- Report mean LLM calls.
- Physician or human pref is a different metric; do not collapse it into the autorater.
- No clinical deployment language.

```bash
python -m swarm discover "held-out architecture search for a debate agent"
```

## Examples

Steal: held-out Hard vs Pro, length penalty, 3-judge final.
Change: replace 28–48 samples with a verifier-first filter that spends calls only on hard items.

## Performance Notes

40–80 calls/query is the paper's cost. Your PhD should beat the *Pareto* of quality vs calls, not only the raw score.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Beating raw score with 8k-char answers | You lost length-adj. Compress. |
| "I improved HealthBench" after seeing rubrics | Invalid. Frozen split only. |
