# Architecture

Implementation of Schmidgall et al., *Accelerating Scientific Research with Gemini in the Real-World*, arXiv:2608.26701 (2026), adapted for a **local Grok / Cursor Co-Scientist** a CS PhD can run.

## Stages

```text
directive
   │
   ▼
ethics (layer 1)
   │
   ▼
ideation ── literature ── generation (τ=1.6)
   │
   ├─ ethics (layer 2)
   ├─ reflection (novelty / plausibility / testability)
   ├─ ranking (TrueSkill pairwise + UCB, κ=1.0)
   ├─ proximity (dedup basins)
   └─ evolution (p_c=0.7 / p_m=0.3, G≈6–10)
   │
   ▼
top hypothesis → research plan
   │
   ▼
experimentation
   scaffold (slice, short timeout)
   transition (remove hacks)
   full-scale (held-out)
   parallel solvers, γ=0.97 decay
   execution.log  ──reward──►  ideation
   │
   ▼
paper (only if logs exist)
   scaffold sections
   evolutionary edits
   S = λ_r S_rev − λ_p S_plag − λ_h S_hall
   λ = (1.0, 0.5, 1.0)
   hallucination clipping against E_log
   plagiarism n-grams
```

## Paper diagram files

| File | Role |
|---|---|
| `solve.py` | Full loop |
| `factory.py` | Coalition specs |
| `agents.py` | Personas |
| `harness.py` | CLI + Agent_H-style plan |
| `readme.txt` | Experiment contract |

Python package lives in `swarm/`. The four root files re-export so the tree matches Figure 1.

## Autonomy (Figure 1g)

1. Human-driven research
2. Materials / human-executed protocols
3. Biology / collaborative
4. Health-agent **architecture** development (CS, autonomous)
5. Autonomous paper writing (integrity modules on)
6. Fully autonomous research (not claimed here)

This repo defaults to **(4)**: CS in-silico, logs required, no wet-lab, no clinic.

## Agent_H (what to steal, not copy)

Eight phases, 40–80 calls, 28–48 candidates, 3-judge final, 2000-char pivot. Your job is a **Pareto** improvement (quality vs calls) on a **held-out** split.

## Integrity

Chen 2025: fabrication 80–100% when fitness is an LLM reviewer.
Gupta & Pruthi 2025: plagiarism up to ~24% in AI papers.

This stack treats those as the default failure mode.
