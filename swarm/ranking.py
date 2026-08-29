"""TrueSkill 1v1 updates and UCB parent selection.

Matches Schmidgall et al. 2026 / Gottweis et al. 2026: each hypothesis is
N(mu, sigma^2); pairwise LLM (or heuristic) outcomes update ratings; UCB
prioritizes uncertain newcomers: UCB(h) = mu + kappa * sigma.
"""

from __future__ import annotations

import math
import random
from typing import Iterable

from swarm.models import Hypothesis, SkillRating

BETA = 25.0 / 6.0
TAU = 25.0 / 300.0
DRAW_PROB = 0.10
DEFAULT_KAPPA = 1.0


def _v_win(t: float, epsilon: float = 0.0) -> float:
    """Gaussian truncation helper for a decisive win (TrueSkill)."""
    from math import erf, exp, sqrt

    denom = math.sqrt(2.0 * math.pi)
    pdf = exp(-0.5 * t * t) / denom
    cdf = 0.5 * (1.0 + erf(t / math.sqrt(2.0)))
    if cdf < 1e-12:
        return t
    return pdf / max(cdf, 1e-12)


def _w_win(t: float) -> float:
    v = _v_win(t)
    return v * (v + t)


def update_pair(winner: SkillRating, loser: SkillRating, beta: float = BETA) -> tuple[SkillRating, SkillRating]:
    """One decisive pairwise update. Returns new (winner, loser) ratings."""
    c2 = 2.0 * beta * beta + winner.sigma**2 + loser.sigma**2
    c = math.sqrt(max(c2, 1e-12))
    t = (winner.mu - loser.mu) / c
    v = _v_win(t)
    w = _w_win(t)

    def apply(skill: SkillRating, sign: float) -> SkillRating:
        sigma2 = skill.sigma**2
        mu = skill.mu + sign * (sigma2 / c) * v
        sigma = math.sqrt(max(sigma2 * (1.0 - (sigma2 / c2) * w) + TAU**2, 1e-6))
        return SkillRating(mu=mu, sigma=sigma)

    return apply(winner, 1.0), apply(loser, -1.0)


def ucb(hypothesis: Hypothesis, kappa: float = DEFAULT_KAPPA) -> float:
    return hypothesis.rating.mu + kappa * hypothesis.rating.sigma


def select_parents(
    population: list[Hypothesis],
    k: int = 2,
    kappa: float = DEFAULT_KAPPA,
    rng: random.Random | None = None,
) -> list[Hypothesis]:
    """Tournament selection with UCB scores (higher is better)."""
    rng = rng or random.Random()
    alive = [h for h in population if h.ethics_ok]
    if not alive:
        return []
    ranked = sorted(alive, key=lambda h: ucb(h, kappa), reverse=True)
    # Soft exploration: sometimes pick from the next tier so ratings move.
    pool = ranked[: max(4, k * 2)]
    return rng.sample(pool, k=min(k, len(pool)))


def rank_population(population: Iterable[Hypothesis], kappa: float = DEFAULT_KAPPA) -> list[Hypothesis]:
    return sorted(population, key=lambda h: (h.ethics_ok, ucb(h, kappa), h.rating.mu), reverse=True)


def pairwise_judge(a: Hypothesis, b: Hypothesis) -> Hypothesis:
    """Heuristic judge used offline (no LLM). Prefer ethics, novelty cues, specificity."""
    def score(h: Hypothesis) -> float:
        text = f"{h.title} {h.statement} {h.method}".lower()
        novelty = sum(w in text for w in ("novel", "unexplored", "first", "unlike", "gap"))
        testable = sum(w in text for w in ("metric", "benchmark", "ablation", "held-out", "log", "evaluate"))
        simple = 1.0 if len(h.statement.split()) < 80 else 0.4
        cites = min(len(h.citations), 5) * 0.15
        ethics = 1.0 if h.ethics_ok else -10.0
        plag = -h.plagiarism_score
        review = float(h.review.get("overall", 0.5))
        return ethics + 0.4 * novelty + 0.5 * testable + 0.3 * simple + cites + plag + review

    return a if score(a) >= score(b) else b


def run_tournament(
    population: list[Hypothesis],
    rounds: int | None = None,
    rng: random.Random | None = None,
    judge=None,
) -> list[Hypothesis]:
    """Round-robin-ish pairwise matches; updates TrueSkill in place."""
    rng = rng or random.Random()
    judge = judge or pairwise_judge
    alive = [h for h in population if h.ethics_ok]
    if len(alive) < 2:
        return rank_population(population)
    n = rounds if rounds is not None else max(len(alive), 8)
    for _ in range(n):
        a, b = rng.sample(alive, 2)
        winner = judge(a, b)
        loser = b if winner is a else a
        wr, lr = update_pair(winner.rating, loser.rating)
        winner.rating = wr
        loser.rating = lr
    return rank_population(population)
