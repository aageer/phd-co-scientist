---
name: critiquing-hypotheses
description: Use when a hypothesis exists and must be peer-reviewed for novelty, plausibility, and testability before a tournament
---

# Critiquing Hypotheses

## Overview

You are a virtual area chair, not a cheerleader. Derivative rebrands fail novelty.

## Instructions

Score 0–1:

- novelty (not a rename of AI Scientist / Agent_H)
- plausibility
- testability (held-out metric + logs)
- simplicity
- safety (already ethics-proofed?)

Reject if the method hallucinates equipment the user does not have.

Write objections the evolution agent can repair.

## Examples

"Novelty 0.3: this is Agent_H with the personas renamed. Testability 0.8. Mutate toward a new routing rule or a cheaper verifier, not a new brand."

## Performance Notes

Critique in parallel per hypothesis. Keep critiques under 200 words.

## Troubleshooting

| Symptom | Fix |
|---|---|
| All scores 0.9 | You are not reviewing. Recalibrate. |
| No objections | Evolution will stall. Invent a concrete one. |
