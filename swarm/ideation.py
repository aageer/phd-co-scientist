"""Evolutionary ideation: generate → ethics → critique → tournament → evolve."""

from __future__ import annotations

from dataclasses import replace
import random
import re

from swarm.ethics import screen_directive, screen_hypothesis
from swarm.literature import corpus_for_plagiarism, load_catalog
from swarm.models import Domain, Hypothesis, ResearchDirective
from swarm.ranking import run_tournament, select_parents, ucb
from swarm.reliability import plagiarism_score


SEED_TEMPLATES = [
    (
        "Held-out tournament scaffold",
        "A {domain} agent that allocates test-time compute with multi-axis triage, "
        "diverse candidate generation, and a TrueSkill tournament will beat a single-pass "
        "backbone on a held-out benchmark without seeing rubric text during search.",
        "Implement a harness with triage, N candidates, pairwise elimination, and length cap. "
        "Tune on a tiny proxy; report on a frozen held-out split.",
    ),
    (
        "Log-grounded paper loop",
        "Joint-optimizing reviewer score minus plagiarism and hallucination penalties, "
        "with hard clipping against execution logs, will reduce fabricated metrics versus "
        "reviewer-only evolutionary paper writing.",
        "Generate programs that emit JSON metrics. Reject any manuscript number absent from logs.",
    ),
    (
        "UCB idea explorer",
        "Selecting ideation parents by UCB(μ+κσ) rather than greedy μ will discover more "
        "diverse high-quality hypotheses in G generations at fixed pairwise budget.",
        "Run two ideation seeds (UCB vs greedy) on the same directive and compare unique clusters.",
    ),
    (
        "Persona-diverse candidates",
        "Sampling candidates from several specialist personas at mixed temperatures "
        "will raise tournament quality more than the same call budget at one temperature.",
        "Ablate persona count vs temperature schedule on a proxy task.",
    ),
    (
        "Proximity-aware mutation",
        "Clustering near-duplicate hypotheses before crossover will prevent the population "
        "from collapsing to a single reworded idea.",
        "Embed titles; reject offspring within a similarity threshold of an existing parent.",
    ),
    (
        "Cost-aware inference scaling",
        "An adaptive compute tier (cheap refuse / medium draft / expensive tournament) "
        "will match full-tournament quality on hard items at lower mean LLM-call cost.",
        "Route by a cheap complexity classifier; report quality vs mean calls.",
    ),
    (
        "Verifier-first ranking",
        "A small deterministic verifier (unit tests, schema, citation presence) as a hard "
        "filter before LLM judging will cut reward hacking in architecture search.",
        "Fail closed on schema/log errors; only then run pairwise LLM or heuristic judges.",
    ),
    (
        "Length-calibrated answers",
        "Optimizing a length-adjusted score around a 2k-character pivot will beat raw-score "
        "maximizers that win by verbosity.",
        "Add a compression pass that must preserve verifier-checked facts.",
    ),
]


def _critique(h: Hypothesis) -> dict:
    text = f"{h.title} {h.statement} {h.method}".lower()
    novelty = 0.7 + 0.1 * ("held-out" in text or "novel" in text)
    plausibility = 0.6 + 0.2 * ("benchmark" in text or "metric" in text)
    testability = 0.5 + 0.3 * ("ablation" in text or "log" in text or "evaluate" in text)
    simplicity = 0.8 if len(h.statement.split()) < 90 else 0.4
    overall = min(1.0, (novelty + plausibility + testability + simplicity) / 4.0)
    return {
        "novelty": round(min(novelty, 1.0), 3),
        "plausibility": round(min(plausibility, 1.0), 3),
        "testability": round(min(testability, 1.0), 3),
        "simplicity": round(simplicity, 3),
        "overall": round(overall, 3),
    }


def seed_population(directive: ResearchDirective, rng: random.Random) -> list[Hypothesis]:
    catalog = load_catalog()
    cites = [e.cite() for e in catalog[:6]]
    pop: list[Hypothesis] = []
    templates = SEED_TEMPLATES[:]
    rng.shuffle(templates)
    for title, stmt, method in templates[: directive.population]:
        h = Hypothesis(
            title=f"{title}: {directive.domain.value}",
            statement=stmt.format(domain=directive.domain.value) + f" Goal: {directive.goal}",
            rationale=f"Grounded in {', '.join(cites[:3])}.",
            method=method + " Constraints: " + "; ".join(directive.constraints),
            constraints=list(directive.constraints),
            citations=cites[:5],
            safety_notes="CS in-silico only. No clinical deployment. No exploit development.",
        )
        screen_hypothesis(h, directive)
        h.review = _critique(h)
        h.plagiarism_score = plagiarism_score(h.statement, [e.architecture for e in catalog])
        pop.append(h)
    return pop


def _crossover(a: Hypothesis, b: Hypothesis, gen: int) -> Hypothesis:
    child = Hypothesis(
        title=f"Hybrid: {a.title.split(':')[0]} × {b.title.split(':')[0]}",
        statement=a.statement.split(" Goal:")[0] + " Combined with " + b.statement.split(" Goal:")[0],
        rationale=f"Crossover of {a.id} and {b.id}.",
        method=a.method + " | " + b.method,
        constraints=sorted(set(a.constraints + b.constraints)),
        citations=list(dict.fromkeys(a.citations + b.citations))[:8],
        safety_notes=a.safety_notes,
        generation=gen,
        parent_ids=[a.id, b.id],
    )
    return child


def _mutate(parent: Hypothesis, gen: int) -> Hypothesis:
    extra = " Mutation repairs review: add an explicit held-out split and JSON logs."
    child = replace(
        parent,
        id=__import__("uuid").uuid4().hex[:12],
        title=re.sub(r"^Hybrid: ", "", parent.title) + " (refined)",
        statement=parent.statement + extra,
        method=parent.method + " Log metrics={'score': float, 'calls': int}.",
        generation=gen,
        parent_ids=[parent.id],
        rating=parent.rating.__class__(),  # reset uncertainty for offspring
    )
    return child


def evolve(
    directive: ResearchDirective,
    *,
    rng: random.Random | None = None,
    generations: int | None = None,
    crossover_p: float = 0.7,
) -> list[Hypothesis]:
    gate = screen_directive(directive)
    if not gate.ok:
        raise PermissionError(gate.reason)
    rng = rng or random.Random(7)
    gens = generations or directive.max_generations
    pop = seed_population(directive, rng)
    catalog_text = [e.architecture for e in load_catalog()]
    history = [rank_snapshot(pop)]
    for g in range(1, gens + 1):
        run_tournament(pop, rounds=max(8, len(pop)), rng=rng)
        parents = select_parents(pop, k=2, rng=rng)
        if len(parents) == 2 and rng.random() < crossover_p:
            child = _crossover(parents[0], parents[1], g)
        elif parents:
            child = _mutate(parents[0], g)
        else:
            break
        screen_hypothesis(child, directive)
        child.review = _critique(child)
        child.plagiarism_score = plagiarism_score(child.statement, catalog_text)
        pop.append(child)
        # Keep a bounded population: top UCB plus a few newcomers.
        pop = sorted(pop, key=lambda h: (h.ethics_ok, ucb(h), h.generation), reverse=True)[
            : max(directive.population, 8)
        ]
        history.append(rank_snapshot(pop))
    run_tournament(pop, rounds=len(pop) * 2, rng=rng)
    return pop


def rank_snapshot(pop: list[Hypothesis]) -> list[dict]:
    return [
        {
            "id": h.id,
            "title": h.title,
            "mu": round(h.rating.mu, 3),
            "sigma": round(h.rating.sigma, 3),
            "ucb": round(ucb(h), 3),
            "ethics_ok": h.ethics_ok,
            "plagiarism": round(h.plagiarism_score, 3),
        }
        for h in pop
    ]


def default_directive(goal: str, domain: str = "cs") -> ResearchDirective:
    return ResearchDirective(
        goal=goal,
        constraints=[
            "In-silico CS only",
            "Held-out evaluation",
            "No clinical deployment",
            "Every metric must appear in execution logs",
        ],
        domain=Domain(domain),
        success_metric="held-out length-adjusted score and verified log claims",
    )
