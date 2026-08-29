---
name: running-co-scientist
description: Use when the user starts a research project, asks to run the Co-Scientist, or wants ideation through paper in one loop
---

# Running Co-Scientist

## Overview

Three stages, in order: ideation → experimentation → paper. Paper is forbidden without execution logs.

## When to Use

- "Be my co-scientist", "run the loop", "help my PhD"
- A new research directive with constraints
- After a SOTA survey, when it is time to pick and test one idea

Do not use for a literature-only question (`surveying-sota`) or a one-off code bug.

## Instructions

1. Restate the **directive**, **constraints**, **domain**, **autonomy**, and **success metric**.
2. Read `screening-ethics`. Layer-1 screen the directive. Stop on FAIL.
3. Read `surveying-sota` and ground 3–8 primary papers.
4. Ideation (`generating-hypotheses` → `critiquing-hypotheses` → `ranking-hypotheses` → `evolving-hypotheses`). Default G=6, pop=8, κ=1.0, p_crossover=0.7.
5. Take the top UCB hypothesis. Build a research plan (`planning-experiments`).
6. Execute (`executing-experiments`): scaffold on a slice, then full scale. Verbose logs.
7. Only then `writing-papers` + `clipping-hallucinations` + `checking-plagiarism`.
8. Return: ranked hypotheses, best program + metrics, manuscript path, residual risks.

Local runner:

```bash
python -m swarm run "Your directive" --domain cs --generations 6
```

## Examples

User: "Build me a co-scientist for inference-time scaling."
You: ethics PASS → SOTA table → tournament → `runs/<stamp>/paper.md` with log-verified numbers.

## Performance Notes

- Parallelize literature and generation. Serialize ethics and paper-start.
- Offline mode (no API key) still runs the full loop on the proxy experiment.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Want a paper first | Refuse. Run experiments. |
| Population collapsed to one idea | Use proximity clustering; raise temperature on generation only. |
| Directive is wet-lab | Drop autonomy to human-executed; output a protocol, not a claim of synthesis. |
