"""Agent factory — maps paper roles onto runnable worker specs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from swarm.models import Domain


@dataclass
class AgentSpec:
    name: str
    role: str
    skill: str
    temperature: float
    system: str
    phase: str
    tags: list[str] = field(default_factory=list)


class AgentFactory:
    """Creates the coalition from Gottweis/Schmidgall plus CS extras."""

    def __init__(self, domain: Domain = Domain.CS):
        self.domain = domain

    def coalition(self) -> list[AgentSpec]:
        specs = [
            AgentSpec(
                "supervisor",
                "Adaptive planner",
                "running-co-scientist",
                0.2,
                "Break the research goal into parallel agent tasks. Never skip ethics or logs.",
                "all",
            ),
            AgentSpec(
                "generation",
                "Hypothesis proposer",
                "generating-hypotheses",
                1.6,
                "Propose simple, testable, novel hypotheses grounded in cited papers. Prefer simplicity.",
                "ideation",
            ),
            AgentSpec(
                "literature",
                "Literature scout",
                "searching-literature",
                0.3,
                "Retrieve primary papers. Quote claims. Refuse abstract-only citations.",
                "ideation",
            ),
            AgentSpec(
                "ethics",
                "Safety screen",
                "screening-ethics",
                0.0,
                "Binary harm check. If dual-use, refuse. Feedback must be specific.",
                "ideation",
            ),
            AgentSpec(
                "reflection",
                "Virtual peer reviewer",
                "critiquing-hypotheses",
                0.2,
                "Score novelty, plausibility, testability. Flag derivative methods and fake equipment.",
                "ideation",
            ),
            AgentSpec(
                "ranking",
                "Tournament judge",
                "ranking-hypotheses",
                0.1,
                "Pairwise debate. Update TrueSkill. Do not collapse to a single scalar without games.",
                "ideation",
            ),
            AgentSpec(
                "evolution",
                "Crossover / mutation",
                "evolving-hypotheses",
                0.8,
                "Crossover complementary parents (p=0.7) or mutate using review feedback (p=0.3).",
                "ideation",
            ),
            AgentSpec(
                "proximity",
                "Diversity cluster",
                "generating-hypotheses",
                0.2,
                "Cluster near-duplicates so the tournament explores more than one basin.",
                "ideation",
            ),
            AgentSpec(
                "meta-review",
                "Debate synthesizer",
                "running-co-scientist",
                0.3,
                "Turn tournament traces into a research plan and system lessons.",
                "ideation",
            ),
            AgentSpec(
                "experiment",
                "Evolutionary coder",
                "executing-experiments",
                0.4,
                "Scaffold on a slice, then full-scale. Log every metric. Score decay 0.97.",
                "experimentation",
            ),
            AgentSpec(
                "paper",
                "Manuscript solver",
                "writing-papers",
                0.4,
                "Section scaffold then evolutionary edits. Joint-opt review − plagiarism − hallucination.",
                "paper",
            ),
            AgentSpec(
                "reliability",
                "Log verifier",
                "clipping-hallucinations",
                0.0,
                "Hard-verify every number against E_log. Abort paper if logs are empty.",
                "paper",
            ),
        ]
        if self.domain == Domain.CS:
            specs.append(
                AgentSpec(
                    "architect",
                    "Inference-time architecture searcher",
                    "discovering-agent-architectures",
                    0.7,
                    "Search scaffolds like Agent_H. Held-out eval only. Length-calibrate.",
                    "experimentation",
                    tags=["cs"],
                )
            )
        return specs

    def by_phase(self, phase: str) -> list[AgentSpec]:
        return [s for s in self.coalition() if s.phase in {phase, "all"}]


def worker_banner(spec: AgentSpec) -> str:
    return f"[{spec.name}/{spec.role}] skill={spec.skill} T={spec.temperature}"
