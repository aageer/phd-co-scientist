# SOTA for a CS PhD Co-Scientist

Survey date: 2026-08-29. Catalog: `data/sota_catalog.json` (40 systems). Merged from a 4-worker Grok swarm — [GDM](bc-b5014059-8140-5344-95fa-6d4e3d90546a), [Stanford](bc-54b44b09-58c4-53b3-87a4-5763a91a7c12), [Sakana / FutureHouse / OpenAI](bc-91734018-5881-5085-972f-86c7fde13498), [CS agents / evals](bc-781e962c-ced9-592d-ae2c-375d6fbb691d). **Verify identifiers before you cite.**

## How to read this

Three layers people collapse and should not:

1. **Oracles** — AlphaFold 3, GNoME. Call them. They are not research agents.
2. **Agents** — Co-Scientist, Robin, AI Scientist, Biomni, SWE-agent. They *search*.
3. **Benchmarks** — HealthBench, SWE-bench, MLE-bench, MLAgentBench. They *score* agents.

SOTA for *your* PhD is the best **steal-stack**, not the flashiest Nature figure.

## Leaderboard (systems that matter)

| System | Lab | Year | Venue | Autonomy | Why it is SOTA | Fatal flaw |
|---|---|---|---|---|---|---|
| Co-Scientist execution-grounded | GDM + Duke + Columbia | 2026 | arXiv:2608.26701 | Adaptive → fully autonomous on CS | Closed ideation/experiment/paper with integrity modules; Agent_H | Gemini-centric; wet-lab still human |
| Co-Scientist | GDM | 2026 | Nature 655:487 | Supervised hypothesis engine | Elo generate–debate–evolve; AML / fibrosis / AMR | Elo is a proxy, not ground truth |
| ERA | GDM | 2026 | Nature 654:909 | High if scored | Tree search over empirical scientific software | Needs a metric |
| Robin | FutureHouse | 2026 | Nature; 2505.13400 | Semi-autonomous bio | Lit → assay analysis; ripasudil; Deep Research 0 hits | Humans still pipette |
| Biomni | Stanford SNAP | 2026 | Science; 10.1126/science.adz4351 | Tool-using lab copilot | CodeAct + verified env; LAB-Bench ≈ human | Not CS architecture search |
| POPPER | Stanford | 2025 | ICML; 2502.09858 | Validator | Sequential falsification with Type-I control | Does not generate the program |
| Virtual Lab | Stanford Zou | 2025 | Nature | Collaborative PI+agents | Nanobody design with wet-lab binders | Meetings without tests |
| AI Scientist / v2 | Sakana et al. | 2024–26 | 2408.06292; Nature 651:914 | Fully autonomous in-silico ML | Tree search + compute scaling; one workshop accept | Reviewer-only fitness; workshop ≠ main track |
| AlphaEvolve | GDM | 2025 | 2506.13131 | Autonomous with a checker | Programs + honest `evaluate()` | No automatic eval ⇒ out of scope |
| Agent Laboratory | Schmidgall et al. | 2025 | Findings EMNLP; 2501.04227 | Semi-autonomous ML lab | Human idea / agent execution; human score 3.8 vs auto 6.1 | Auto-eval inflates quality |
| Coscientist | CMU (Boiko) | 2023 | Nature | Narrow closed-loop chem | Hardware API as truth | Narrow surface |
| ChemCrow | EPFL | 2024 | Nat Mach Intell | Tool chemist | Force facts through tools | Domain-specific |
| SWE-agent / OpenHands | Princeton / All Hands | 2024–25 | ICLR lineage / OSS | Autonomous coding | Tests as oracle; ACI design | Issue-fix ≠ science |
| AIDE | Weco | 2024 | MLE-bench | Autonomous ML eng | Tree search + real metric | Kaggle ≠ theory |
| PaperQA2 | FutureHouse | 2024 | arXiv:2409.13740 | Lit tool | Quote-level citations | Not an experimenter |
| STORM | Stanford | 2024 | NAACL / 2402.14207 | Writer | Perspective outlines | Not discovery |
| Magentic-One | MSR | 2024 | MSR | Generalist | Orchestrator + specialists | Not science-specialized |
| HealthBench Hard / Pro | OpenAI | 2025–26 | 2505.08775 / 2604.27470 | Benchmark | Rubrics + length penalty; Agent_H's arena | Autorater ≠ physician |
| SWE-bench Pro | community | 2025 | 2509.16941 | Benchmark | Honest 2026 coding metric | Harness > model (2605.23950) |
| TrueSkill + UCB | MSR / bandits | 2006 / 1985 | classic | Algorithm | Idea ranking in Co-Scientist | Needs enough games |

## Google DeepMind — what to steal

**Co-Scientist (Gottweis 2026, Nature).** Supervisor + Generation, Reflection, Ranking, Evolution, Proximity, Meta-review. **Ranking in this paper is Elo** (initial 1200), not TrueSkill. Async tasks. Test-time compute. Validated in drug repurposing, targets, AMR. Product path: Gemini for Science / Hypothesis Generation.

**Execution-grounded extension (Schmidgall 2026, 2608.26701).** This repo's blueprint.

- Ideation: τ=1.6, simplicity, ethics, LLM review, TrueSkill, UCB(h)=μ+κσ, κ=1, p_c=0.7, G=10
- Experiment: scaffold → transition → full; γ=0.97; files `solve.py` `factory.py` `agents.py` `harness.py`
- Paper: joint score λ=(1, 0.5, 1); hard clip vs logs; abort if no logs
- CS result: Agent_H 8-phase inference-time scaler; length-adj SOTA vs GPT-5.6 Sol, Fable 5, Opus 5, GPT-5, Gemini 3.1 Pro / 3.5 Flash

**AlphaEvolve (2506.13131) / FunSearch / ERA (Nature 2026, 2509.06503).** Evolve *programs* only when `evaluate()` is cheap and hard to fake. ERA is tree search (recombination); AlphaEvolve is island EA.

**AlphaFold 3 / GNoME / AlphaGenome / AlphaProteo.** Domain oracles. Do not reimplement with a chat model.

**Avoid:** treating the GDM blog as a methods section; claiming MXene atomic structure from the paper (they say confirmation is pending).

## Stanford — what to steal

**Biomni (Science 2026, 10.1126/science.adz4351).** Leskovec et al. Steal: mine then freeze a verified env; **code as the action**. Avoid: cloning 150 tools.

**Virtual Lab (Nature 2025, 10.1038/s41586-025-09442-9).** Critic as a first-class role; meetings only for interdisciplinary design.

**POPPER (ICML 2025, 2502.09858).** The missing piece in almost every co-scientist: sequential falsification with Type-I control.

**Paper2Agent (2509.06917), CellVoyager, TextGrad, CRISPR-GPT, BioDiscoveryAgent.** Tools-from-papers, condition on the analysis log, optimize the graph, state machines for irreversible actions, knowledge-driven acquisition.

**Peltz microHO (Adv Sci 2025).** Cleanest Stanford-adjacent validation: AI list vs expert list, same organoid assay.

**MLAgentBench / STORM / Co-STORM.** Task-contract shape and lit-review UI — not discovery engines.

Do not clone Biomni or GDM. Compose: verified env + critic/CSO + tournament generation + POPPER.

## Sakana, FutureHouse, OpenAI, Microsoft

**AI Scientist / Nature 2026 (10.1038/s41586-026-10265-5).** Steal the tree and the VLM figure gate. A workshop accept at ~70% accept rate is not “AI does science.”

**Robin (Nature 2026, 2505.13400).** Crow scout + Falcon deep + Finch consensus-of-8 + tournament. Ablate RAG or you get ~44% hallucinated refs. Deep Research is not a substitute (0 hits on the same assay).

**PaperQA2.** Evidence-first full-text RAG. Still the literature engine to wrap, not replace.

**HealthBench (2505.08775) / Professional (2604.27470).** Held-out + length-adjusted + cross-family judge. MedQA is saturated.

**Deep Research / Magentic-One / Claude Science.** Desk research and workbenches. Not discovery. Bound the graph.

## CS agent SOTA (the actual PhD surface)

If your dissertation is "agents that do science / software / evals":

| Question | Current SOTA move |
|---|---|
| Repo-level coding | **SWE-bench Pro / Live**, frozen harness (mini-SWE-agent). Verified is leaky. |
| ML engineering | MLE-bench + AIDE (2502.13138). Ignore unofficial 60%+ rows. |
| ML *research* agents | Outer Co-Scientist loop + inner AIDE/OpenHands + log verification |
| Inference-time scaling | Agent_H as a *failure mode*: beat it on Pareto(score, calls, length) and on humans |
| Idea selection | Gottweis Elo for complete round-robins; **TrueSkill+UCB** for rolling pools |
| Falsification | POPPER sequential tests — not LLM-as-judge |
| Integrity | Joint-opt + log clip + Gupta-style similarity hunt + fail-closed cites |

## Recommended steal-stack for this repo

1. GDM **outer** loop (stages, debate-as-pairwise-ranker, decay, joint score)
2. AlphaEvolve / ERA rule: no evolution without a checker; evolve the **executable architecture**, not the paper
3. PaperQA2 / Falcon rule: quote-level citations; Crow-ablation as a unit test
4. Biomni / Paper2Agent rule: verified tools, code as action
5. POPPER rule: Type-I-controlled falsification after the tournament
6. HealthBench rule: held-out + length pivot + **cross-family** judge + `oracle@N − selected@N`
7. Peltz rule: AI list vs expert list on the same assay (when you claim science)
8. Explicitly reject AI Scientist reviewer-only fitness and SWE-Verified headlines

## Refresh

```bash
python -m swarm sota
python -m swarm sota --lab Stanford
python -m swarm swarm "co-scientist SOTA 2026" -n 6
```

Then merge worker PASS notes into this file. Drop anything without an identifier into a "unverified leads" section.
