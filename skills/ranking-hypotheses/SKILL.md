---
name: ranking-hypotheses
description: Use when two or more ethics-proofed hypotheses must be compared, Elo/TrueSkill rated, or selected with UCB
---

# Ranking Hypotheses

## Overview

Pairwise games, not a single score. Ratings are Gaussians. UCB picks parents.

## Instructions

1. Play pairwise debates (novelty, testability, safety, simplicity, gap).
2. Update TrueSkill (`swarm.ranking.update_pair`).
3. Parent selection: `UCB(h) = μ + κσ` with κ=1.0 so newcomers play.
4. Fitness may subtract plagiarism. Do not add a raw reviewer score as the only signal.
5. Report μ, σ, UCB, games played.

```bash
python -m swarm ideate "Your directive" --generations 6
```

## Examples

New idea σ=8.3, μ=25 → UCB=33.3 plays before a settled μ=28 σ=2 idea (UCB=30).

## Performance Notes

Rounds ≈ max(8, n). More games beat a fancier judge.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Greedy μ only | You starved exploration. Use UCB. |
| Judge always picks longer text | Add a simplicity criterion. |
