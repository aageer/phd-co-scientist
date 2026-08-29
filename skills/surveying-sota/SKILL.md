---
name: surveying-sota
description: Use when the user asks what is SOTA, which lab to follow, or how GDM, Stanford, Sakana, or FutureHouse systems compare
---

# Surveying SOTA

## Overview

A SOTA survey is a ranked, cited map of systems — not a blog recap. Catalog rows are leads. Primary papers are citations.

## When to Use

- "What's SOTA for co-scientists / agents / HealthBench?"
- Before ideation, so hypotheses are not derivative
- When comparing GDM vs Stanford vs Sakana vs FutureHouse

## Instructions

1. Load `data/sota_catalog.json` (`python -m swarm sota`).
2. Filter by lab / domain / tag. Open the primary PDF or Nature page.
3. For each system record: architecture, validated result, autonomy, limitation, steal, avoid.
4. Separate **oracles** (AlphaFold) from **agents** (Co-Scientist) from **benchmarks** (HealthBench, SWE-bench).
5. End with a steal-stack for *this* PhD, not a generic "AI will change science" paragraph.

Required labs to mention unless the user scoped smaller:

- Google DeepMind: Co-Scientist (Nature 2026, 2502.18864), execution-grounded extension (2608.26701), AlphaEvolve
- Stanford: Biomni (Science 2026), Virtual Lab, MLAgentBench, STORM
- Sakana: AI Scientist / v2
- FutureHouse: Robin, PaperQA2
- Ancestry: Coscientist (Boiko 2023), ChemCrow
- CS evals: SWE-bench, MLE-bench, HealthBench Hard/Pro

## Examples

```bash
python -m swarm sota --lab DeepMind
python -m swarm sota --tag healthbench
python -m swarm sota --domain cs --year-min 2024
```

## Performance Notes

Fan out one Grok worker per lab (`running-grok-swarm`) then merge. Do not paste raw worker dumps.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Only blogs | Demand arXiv/DOI. |
| Mixing AlphaFold into agent SOTA | Move to "oracles you should call". |
| Stale 2023 list | Re-pull catalog + worker slice. |
