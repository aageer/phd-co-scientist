---
name: generating-hypotheses
description: Use when creating the initial hypothesis pool for a research directive, before critique or ranking
---

# Generating Hypotheses

## Overview

High temperature, low complexity. Novelty comes from the search process, not from ornate prose.

## Instructions

1. Ground each idea with its own mini literature pass.
2. Sample at τ ≈ 1.6. Prompt for **simplicity** (Schmidgall 2026).
3. Each hypothesis is a record: title, statement, method, metric, citations, safety notes, constraints.
4. Target pop=8. Cover more than one basin (use the proximity agent).
5. Immediately send every item through `screening-ethics` then `critiquing-hypotheses`.

Schema:

```text
title:
statement:  # one paragraph, testable
method:     # files, data slice, timeout
metric:     # held-out, machine-checkable
citations:  # 2–5 primary
safety:
```

## Examples

Good: "UCB parent selection (κ=1) raises unique high-μ hypotheses vs greedy Elo at fixed pairwise budget."
Bad: "A revolutionary AGI scientist will transform knowledge."

## Performance Notes

Generate in parallel. Do not wait to batch ethics — run it per item.

## Troubleshooting

| Excuse | Reality |
|---|---|
| "Need a grand theory first" | Start with a one-week test. |
| "More complexity looks novel" | Complexity is a plagiarism hide. |
