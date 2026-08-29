# PhD Co-Scientist

A Cursor plugin plus a local swarm that implements the execution-grounded Co-Scientist loop from Schmidgall et al., **Accelerating Scientific Research with Gemini in the Real-World** ([arXiv:2608.26701](https://www.alphaxiv.org/pdf/2608.26701) / [alphaXiv](https://www.alphaxiv.org/abs/2608.26701)).

It is built for a **CS PhD**: hypothesis tournaments, Grok swarms, isolated experiments, and papers that are not allowed to exist without logs.

```text
directive → ethics → literature → generate → critique → TrueSkill+UCB
        → evolve → plan → scaffold/full programs → logs
        → manuscript (review − 0.5·plagiarism − 1.0·hallucination)
```

## Why this exists

First-wave AI Scientists optimized an LLM reviewer and fabricated results (Chen 2025; fabrication 80–100% in small audits). Gupta & Pruthi 2025 measured plagiarism up to ~24%. GDM's 2026 extension adds:

- Bayesian idea tournaments (TrueSkill + UCB)
- Evolutionary programs with real execution
- Hallucination clipping against `E_log`
- A two-layer ethics gate
- A CS result: **Agent_H**, an inference-time scaffold that beat six frontier models on length-adjusted HealthBench Hard / Professional

This repo turns that paper into something you can run in Cursor with Grok workers.

## Install (Cursor plugin)

Repo root is a single Cursor plugin (`phd-co-scientist`).

1. Clone this repository.
2. Cursor → Settings → Plugins → add from folder / Git URL.
3. Optional: set `XAI_API_KEY` in Plugins → Configure (live Grok). Offline mode still runs the full loop on a deterministic proxy.

Slash commands: `/co-scientist` `/sota-survey` `/ideate` `/experiment` `/write-paper` `/swarm` `/discover-architecture` `/phd-weekly`

## Install (Python swarm)

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest tests
python3 -m swarm sota --lab DeepMind
python3 -m swarm ideate "Discover a cheaper tournament scaffold" --generations 4
python3 -m swarm run "Discover a length-calibrated tournament agent on a held-out proxy"
python3 -m swarm swarm "co-scientist SOTA" -n 6
```

Artifacts land in `runs/<timestamp>/` (`report.json`, `paper.md`, `experiment/execution.log`).

## What's in the box

| Path | What |
|---|---|
| `skills/` | 15 skills (loop, SOTA, ethics, tournament, paper integrity, Grok swarm, Agent_H search) |
| `agents/` | Supervisor + paper coalition (generation, reflection, ranking, evolution, …) |
| `commands/` | Slash commands |
| `rules/` | Always-on protocol, integrity, safety |
| `hooks/` | Fail-open ethics hints on prompts and shell |
| `swarm/` | TrueSkill, ethics, reliability, ideation, experiment, paper, CLI |
| `data/sota_catalog.json` | Curated GDM / Stanford / Sakana / FutureHouse / eval catalog |
| `docs/` | Architecture, SOTA, PhD cadence, Agent_H, references |

Paper-diagram filenames (`solve.py`, `factory.py`, `agents.py`, `harness.py`, `readme.txt`) sit at repo root and re-export the package.

## SOTA map (start here)

Full write-up: [`docs/SOTA.md`](docs/SOTA.md). Catalog dump: `python -m swarm sota`.

| Lab | System | Steal |
|---|---|---|
| GDM | Co-Scientist (Nature 2026; 2608.26701) | Tournaments, log-grounded papers, adaptive autonomy |
| GDM | AlphaEvolve | Machine-checkable fitness |
| Stanford | Biomni, Virtual Lab, MLAgentBench | Tool-grounded lab agents; research-task specs |
| Sakana | AI Scientist / v2 | Closed code loop — **plus** integrity modules they lacked |
| FutureHouse | Robin, PaperQA2 | Typed search / read / data tools |
| OpenAI | HealthBench Hard/Pro, MLE-bench | Held-out rubrics, length-adjusted scores |
| Ancestry | Coscientist, ChemCrow | Hardware/tools as source of truth |

## Safety

In-silico CS default. No clinical advice. No exploits. No dual-use bio. Ethics hooks fail **open** if they crash, but the Python gate fails **closed** on restricted directives.

## License

MIT. The paper this is inspired by is Google's; this repo is an independent implementation of the *public* architecture for your own research.
