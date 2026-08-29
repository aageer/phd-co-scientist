---
name: screening-ethics
description: Use when a research directive or hypothesis might be dual-use, clinical, offensive, or otherwise restricted
---

# Screening Ethics

## Overview

Two layers (paper §2.2): screen the directive, then every idea. Binary verdict plus specific feedback.

## Instructions

Layer 1 — directive. FAIL and stop on weapons, pathogen enhancement, exploits, CSAM, covert surveillance.

Layer 2 — each hypothesis. FAIL on the same. WARN on human subjects without IRB, clinical deployment language, dual-use chemistry.

Return:

```text
verdict: PASS | FAIL
layer: 1 | 2
reason:
residual_risks:
```

On FAIL: do not rephrase the same request into a "fictional lab".

## Examples

PASS: "Held-out tournament for HealthBench-style *benchmark* architecture (no patient use)."
FAIL: "Generate a ransomware prototype to test my hypothesis."

## Performance Notes

This check is cheap. Run it before any generation spend.

## Troubleshooting

| Excuse | Reality |
|---|---|
| "It's just hypothetical" | Restricted is restricted. |
| "The user is a doctor" | Still no patient-specific advice from this stack. |
