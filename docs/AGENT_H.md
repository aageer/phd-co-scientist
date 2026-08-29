# Agent_H reference (CS track)

Source: Schmidgall et al. 2026, arXiv:2608.26701 §3.3 / Figure 6.

Discovered **autonomously** by Co-Scientist for medical *response generation* as a **benchmarked architecture**. This repo treats it as a CS object: an inference-time scaffold.

## Pipeline

1. **Triage** — specialty, audience, intent, complexity, adversarial risk, context gaps → compute tier
2. **Decompose** — multi-part queries into typed sub-questions
3. **Parallel candidates** — 28–48 samples, ~6 personas, τ ∈ [0.5, 0.95]
4. **Tournament** — single elimination + 3-judge majority on finalists
5. **Critique loop** — up to 5 auditor/editor cycles
6. **Metacognition** — did we answer every sub-question / gap?
7. **Citation audit** — named guidelines / dosages / stats
8. **Length optimize** — ~2000-character pivot

Cost: ~40–80 LLM calls/query.

## Numbers to beat (do not peek at rubrics)

HealthBench Hard and Professional, two judges, 8 runs, length-adjusted.

From Table 2 (Gemini 3.5 Flash judge, length-adj):

| System | Hard | Professional |
|---|---|---|
| Agent_H | 0.377 | 0.643 |
| GPT-5 | 0.334 | 0.485 |
| GPT-5.6 Sol | 0.293 | 0.614 |
| Fable 5 | 0.300 | 0.581 |
| Opus 5 | 0.281 | 0.572 |
| Gemini 3.1 Pro | 0.148 | 0.467 |

Physician blinded eval: modest harm reduction vs Gemini 3.1 Pro; preference mixed vs autorater. Do not overclaim.

## PhD moves

- Keep the tournament; replace the 28–48 spray with a verifier-first filter.
- Learn a cheap complexity router (adaptive tier is the real invention).
- Optimize the **Pareto** of length-adj score vs calls.
- Never deploy as a clinician.
