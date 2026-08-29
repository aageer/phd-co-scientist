---
name: planning-experiments
description: Use when a top-ranked hypothesis must become a research plan with files, slices, timeouts, and metrics
---

# Planning Experiments

## Overview

A plan is a contract: files, data slice, timeout, metric, abort condition.

## Instructions

Write:

```text
phase: scaffold | transition | full
files: solve.py, factory.py, agents.py, harness.py, readme.txt
slice:  # smallest data that can prove the logic
timeout_s:
metric:  # JSON keys the log must contain
abort:   # what failure looks like
held_out: # what you will not touch while searching
```

CS default files match Figure 1 of 2608.26701.

Do not plan a paper section here.

## Examples

Scaffold: 20 proxy seeds, 10s timeout.
Full: held-out 200 items, 20s, metrics `{score, calls, length}`.

## Performance Notes

If the plan needs hardware the user does not have, drop autonomy and emit a human protocol.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Plan is a literature review | You skipped the files/metric. |
| No held-out | You will overfit. Split now. |
