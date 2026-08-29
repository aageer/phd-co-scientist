---
name: writing-papers
description: Use when experiments have execution logs and a manuscript must be drafted or refined
---

# Writing Papers

## Overview

Scaffold sections, then evolve edits. Score = S_review − 0.5 S_plag − 1.0 S_hall. Halt if logs are empty.

## Instructions

1. Confirm `execution.log` exists and contains metrics. Else stop.
2. Draft Abstract → Intro → Related Work → Methods → Results → Discussion.
3. Related Work is written from the catalog + PDFs, not from memory.
4. Each evolutionary step may fetch more literature; citations are not frozen at step 0.
5. Run `clipping-hallucinations` then `checking-plagiarism`.
6. Nine-dimension reviewer is allowed only as one term in the joint score.

## Examples

Results sentence: "Best verified score=0.812 (log line 4), calls=44."
Not: "We dramatically outperform GPT-5.6." (unless the log says so)

## Performance Notes

Do not generate a paper to "see how it looks" without logs. That is how 80–100% fabrication happens.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Empty logs | Delete the draft. Re-run experiments. |
| Reviewer loves it, logs disagree | Hallucination term wins. Clip. |
