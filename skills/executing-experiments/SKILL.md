---
name: executing-experiments
description: Use when a research plan exists and programs must be generated, run in isolation, scored, and refined
---

# Executing Experiments

## Overview

Programs are the experiment. Logs are the truth. γ=0.97 score decay fights stagnation.

## Instructions

1. Write `solve.py` that prints one JSON metrics object and human logs.
2. Scaffold on a slice with a short timeout.
3. Spawn parallel variants. Failed runs get the traceback, then reflect.
4. Transition: delete slice hacks. Full-scale: run the real split.
5. Reward: plan adherence, rigor, output quality in [0,1] — plus the real metric.
6. Feed scores back to ideation only as **reward feedback**, not as a license to rewrite history.

```bash
python -m swarm run "directive"
# artifacts: runs/<stamp>/experiment/solve.py experiment/execution.log
```

## Examples

Good log: `{"score": 0.812, "calls": 44, "kappa": 1.0}`
Bad log: "Results were excellent."

## Performance Notes

Isolate subprocesses. Never `eval` model-written shell.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Timeout | Shrink slice; do not fake the metric. |
| Best score frozen | Decay is working; mutate the program. |
