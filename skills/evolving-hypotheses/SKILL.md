---
name: evolving-hypotheses
description: Use when a ranked population exists and the next generation must be produced by crossover or mutation
---

# Evolving Hypotheses

## Overview

p_crossover=0.7 merges complementary parents. p_mutation=0.3 repairs review objections. Reset σ on offspring.

## Instructions

1. Select 2 parents via UCB tournament.
2. Crossover: one mechanism from A, one from B, one shared metric.
3. Mutation: address the reflection agent's top objection; do not only polish prose.
4. Ethics + critique + plagiarism on the child before it enters the pool.
5. Bound population (keep top UCB + a few newcomers). Default G=10 in the paper, G=6 here.

## Examples

Parent A: persona diversity. Parent B: cheap verifier. Child: verifier-gated persona tournament.

## Performance Notes

If similarity(child, parent) is high, mutate again. That is the proximity agent.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Children are reworded parents | Force a mechanism-level edit. |
| Ethics FAIL after crossover | Drop the child. Do not "tone it down". |
