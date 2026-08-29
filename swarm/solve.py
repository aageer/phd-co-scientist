"""Top-level Co-Scientist solve loop (paper diagram: solve.py)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
import time

from swarm.config import load_settings
from swarm.experiment import evolutionary_search
from swarm.ideation import default_directive, evolve
from swarm.models import Hypothesis, ResearchDirective
from swarm.paper import score_manuscript, write_manuscript
from swarm.ranking import rank_population


@dataclass
class SolveReport:
    directive: dict
    top_hypothesis: dict
    population: list[dict]
    experiment_best: dict
    manuscript_score: float
    manuscript_path: str
    run_dir: str


def solve(
    goal: str,
    *,
    domain: str = "cs",
    generations: int | None = None,
    population: int | None = None,
    run_dir: str | Path | None = None,
    seed: int = 7,
) -> SolveReport:
    settings = load_settings()
    directive = default_directive(goal, domain=domain)
    if generations:
        directive.max_generations = generations
    if population:
        directive.population = population
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out = Path(run_dir or settings.runs_dir) / stamp
    out.mkdir(parents=True, exist_ok=True)

    pop = evolve(directive, generations=directive.max_generations)
    ranked = rank_population(pop)
    top: Hypothesis = ranked[0]

    results = evolutionary_search(top, out / "experiment")
    best = max(results, key=lambda r: r.score)
    manuscript = write_manuscript(directive, top, results)
    paper_path = out / "paper.md"
    paper_path.write_text(manuscript.render())

    report = SolveReport(
        directive=asdict(directive) | {"domain": directive.domain.value, "autonomy": directive.autonomy.value},
        top_hypothesis=top.to_dict(),
        population=[h.to_dict() for h in ranked],
        experiment_best={
            "score": best.score,
            "metrics": best.metrics,
            "logs_path": best.logs_path,
            "exit_code": best.exit_code,
        },
        manuscript_score=score_manuscript(manuscript),
        manuscript_path=str(paper_path),
        run_dir=str(out),
    )
    (out / "report.json").write_text(json.dumps(asdict(report), indent=2, default=str))
    return report


def solve_from_directive(directive: ResearchDirective, run_dir: Path) -> SolveReport:
    return solve(
        directive.goal,
        domain=directive.domain.value,
        generations=directive.max_generations,
        population=directive.population,
        run_dir=run_dir,
    )
