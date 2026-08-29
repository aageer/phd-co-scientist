"""Manuscript scaffold + joint-opt integrity (review − plag − hall)."""

from __future__ import annotations

from swarm.literature import corpus_for_plagiarism, load_catalog
from swarm.models import ExperimentResult, Hypothesis, Manuscript, ResearchDirective
from swarm.reliability import hallucination_score, joint_score, plagiarism_score


def _reviewer(text: str) -> float:
    checks = [
        "abstract" in text.lower(),
        "held-out" in text.lower() or "held out" in text.lower(),
        "limitation" in text.lower(),
        "log" in text.lower(),
        len(text) > 400,
    ]
    return sum(checks) / len(checks)


def write_manuscript(
    directive: ResearchDirective,
    hypothesis: Hypothesis,
    results: list[ExperimentResult],
) -> Manuscript:
    if not results or all(r.exit_code != 0 for r in results):
        raise RuntimeError("No valid execution logs; refusing to write a paper.")

    best = max(results, key=lambda r: r.score)
    catalog = load_catalog()
    related = "\n".join(f"- {e.cite()}: {e.results}" for e in catalog[:8])
    metrics = best.metrics or {}
    log = (best.stdout or "") + "\n" + Path_read(best.logs_path)

    results_text = (
        f"Best scaffold score={metrics.get('score', best.score)} "
        f"calls={metrics.get('calls', 'n/a')} kappa={metrics.get('kappa', 'n/a')} "
        f"n_candidates={metrics.get('n_candidates', 'n/a')} "
        f"personas={metrics.get('personas', 'n/a')}. "
        f"Successful runs: {sum(1 for r in results if r.exit_code == 0)}/{len(results)}."
    )

    ms = Manuscript(
        title=f"Co-Scientist run: {hypothesis.title}",
        abstract=(
            f"We test the hypothesis that {hypothesis.statement.split(' Goal:')[0].strip()} "
            f"The execution-grounded loop logs every metric. Best verified score is "
            f"{metrics.get('score', best.score)} at {metrics.get('calls', '?')} calls."
        ),
        introduction=(
            f"Directive: {directive.goal}. Autonomy={directive.autonomy.value}. "
            "We follow Schmidgall et al. 2026 (arXiv:2608.26701): ideation tournament, "
            "evolutionary programs, then integrity-checked writing."
        ),
        related_work=related,
        methods=(
            f"Hypothesis method: {hypothesis.method}\n"
            "Ranking: TrueSkill + UCB. Ethics: two-layer screen. "
            "Programs emit JSON metrics. Papers cannot start without logs."
        ),
        results=results_text,
        discussion=(
            "Limitations: the default experiment is a deterministic proxy so the loop "
            "is testable without paid APIs. Replace solve.py with a real benchmark to "
            "claim SOTA. Do not treat this manuscript as a conference submission."
        ),
    )
    rendered = ms.render()
    ms.plagiarism_score = plagiarism_score(rendered, corpus_for_plagiarism(catalog))
    clip = hallucination_score(rendered, log)
    ms.hallucination_score = clip.hallucination_score
    ms.clipped_claims = clip.clipped
    ms.reviewer_score = _reviewer(rendered)
    if clip.clipped:
        ms.discussion += "\n\nClipped unverified claims: " + "; ".join(clip.clipped)
    return ms


def Path_read(path: str) -> str:
    from pathlib import Path

    p = Path(path)
    return p.read_text() if path and p.exists() else ""


def score_manuscript(ms: Manuscript) -> float:
    return joint_score(ms.reviewer_score, ms.plagiarism_score, ms.hallucination_score)
