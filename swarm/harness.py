"""CLI + Agent_H-style inference harness (paper diagram: harness.py).

The 8-phase pipeline is a CS architecture, not a clinician. It must not be
used to give medical advice. Default task is research-question answering
with tournament selection over candidate outlines.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from swarm.factory import AgentFactory
from swarm.literature import filter_entries, load_catalog, render_markdown
from swarm.models import Domain
from swarm.solve import solve


PHASES = [
    "1. triage",
    "2. decompose",
    "3. parallel candidates",
    "4. tournament + 3-judge vote",
    "5. critique-and-refine",
    "6. metacognitive verification",
    "7. citation audit",
    "8. length optimization",
]


def agent_h_plan(query: str, n_candidates: int = 32, personas: int = 6) -> dict:
    complexity = "hard" if len(query) > 120 or "ablation" in query.lower() else "medium"
    calls = n_candidates + int(n_candidates**0.5) + 3 + 6
    return {
        "query": query,
        "phases": PHASES,
        "tier": complexity,
        "n_candidates": n_candidates,
        "personas": personas,
        "est_llm_calls": calls,
        "length_pivot": 2000,
        "warning": "Research harness only. Not a medical device. Not clinical advice.",
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cosci", description="PhD Co-Scientist swarm")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sota", help="Print the curated SOTA catalog")
    s.add_argument("--lab", default=None)
    s.add_argument("--domain", default=None)
    s.add_argument("--tag", default=None)
    s.add_argument("--year-min", type=int, default=None)
    s.add_argument("--query", default=None)

    r = sub.add_parser("run", help="Full ideation → experiment → paper loop")
    r.add_argument("goal", help="Research directive")
    r.add_argument("--domain", default="cs", choices=[d.value for d in Domain])
    r.add_argument("--generations", type=int, default=None)
    r.add_argument("--population", type=int, default=None)
    r.add_argument("--run-dir", default=None)

    i = sub.add_parser("ideate", help="Hypothesis tournament only")
    i.add_argument("goal")
    i.add_argument("--domain", default="cs")
    i.add_argument("--generations", type=int, default=4)
    i.add_argument("--population", type=int, default=8)

    sub.add_parser("agents", help="List coalition")

    d = sub.add_parser("discover", help="Print an Agent_H-style architecture plan")
    d.add_argument("query")
    d.add_argument("--candidates", type=int, default=32)
    d.add_argument("--personas", type=int, default=6)

    sw = sub.add_parser("swarm", help="Fan-out plan for N Grok workers (prints briefs)")
    sw.add_argument("topic")
    sw.add_argument("-n", type=int, default=6)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "sota":
        entries = filter_entries(
            load_catalog(),
            lab=args.lab,
            domain=args.domain,
            tag=args.tag,
            year_min=args.year_min,
            query=args.query,
        )
        sys.stdout.write(render_markdown(entries))
        return 0
    if args.cmd == "agents":
        for spec in AgentFactory().coalition():
            print(f"{spec.name:12} {spec.phase:16} {spec.skill}")
        return 0
    if args.cmd == "discover":
        print(json.dumps(agent_h_plan(args.query, args.candidates, args.personas), indent=2))
        return 0
    if args.cmd == "swarm":
        labs = ["gdm", "stanford", "sakana", "futurehouse", "openai-eval", "cs-agents"]
        briefs = []
        for i in range(args.n):
            briefs.append(
                {
                    "worker": i + 1,
                    "slice": labs[i % len(labs)],
                    "topic": args.topic,
                    "done": "Return PASS/ISSUES/BLOCKED plus citations.",
                    "model": "grok-4.6-fast",
                }
            )
        print(json.dumps(briefs, indent=2))
        return 0
    if args.cmd == "ideate":
        from swarm.ideation import default_directive, evolve
        from swarm.ranking import rank_population

        pop = evolve(
            default_directive(args.goal, args.domain),
            generations=args.generations,
        )
        for i, h in enumerate(rank_population(pop)[:8], 1):
            print(f"{i}. {h.title}  μ={h.rating.mu:.2f} σ={h.rating.sigma:.2f} ethics={h.ethics_ok}")
        return 0
    if args.cmd == "run":
        report = solve(
            args.goal,
            domain=args.domain,
            generations=args.generations,
            population=args.population,
            run_dir=args.run_dir,
        )
        print(json.dumps(
            {
                "run_dir": report.run_dir,
                "top": report.top_hypothesis["title"],
                "experiment_score": report.experiment_best["score"],
                "manuscript_score": report.manuscript_score,
                "paper": report.manuscript_path,
            },
            indent=2,
        ))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
