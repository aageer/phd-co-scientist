from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any
import time
import uuid


class Autonomy(str, Enum):
    HUMAN_DRIVEN = "human-driven"
    HUMAN_EXECUTED = "human-executed"
    COLLABORATIVE = "collaborative"
    AUTONOMOUS = "autonomous"
    PAPER = "paper-writing"
    FULL = "fully-autonomous"


class Domain(str, Enum):
    CS = "cs"
    BIOLOGY = "biology"
    MATERIALS = "materials"
    GENERAL = "general"


@dataclass
class SkillRating:
    mu: float = 25.0
    sigma: float = 25.0 / 3.0

    @property
    def ucb(self) -> float:
        return self.mu + self.sigma

    def conservative(self) -> float:
        return self.mu - 3.0 * self.sigma


@dataclass
class Hypothesis:
    title: str
    statement: str
    rationale: str = ""
    method: str = ""
    constraints: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
    safety_notes: str = ""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    rating: SkillRating = field(default_factory=SkillRating)
    generation: int = 0
    parent_ids: list[str] = field(default_factory=list)
    ethics_ok: bool = True
    ethics_feedback: str = ""
    review: dict[str, Any] = field(default_factory=dict)
    plagiarism_score: float = 0.0
    created_at: float = field(default_factory=time.time)

    def ucb(self, kappa: float = 1.0) -> float:
        return self.rating.mu + kappa * self.rating.sigma

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data


@dataclass
class ResearchDirective:
    goal: str
    constraints: list[str] = field(default_factory=list)
    domain: Domain = Domain.CS
    autonomy: Autonomy = Autonomy.AUTONOMOUS
    forbidden: list[str] = field(default_factory=list)
    success_metric: str = ""
    max_generations: int = 6
    population: int = 8


@dataclass
class ExperimentResult:
    hypothesis_id: str
    exit_code: int
    stdout: str
    stderr: str
    metrics: dict[str, Any] = field(default_factory=dict)
    score: float = 0.0
    logs_path: str = ""
    phase: str = "scaffold"
    program_path: str = ""


@dataclass
class Manuscript:
    title: str
    abstract: str = ""
    introduction: str = ""
    related_work: str = ""
    methods: str = ""
    results: str = ""
    discussion: str = ""
    reviewer_score: float = 0.0
    plagiarism_score: float = 0.0
    hallucination_score: float = 0.0
    clipped_claims: list[str] = field(default_factory=list)

    def joint_score(self, lam_review: float = 1.0, lam_plag: float = 0.5, lam_hall: float = 1.0) -> float:
        return (
            lam_review * self.reviewer_score
            - lam_plag * self.plagiarism_score
            - lam_hall * self.hallucination_score
        )

    def render(self) -> str:
        parts = [
            f"# {self.title}",
            "",
            "## Abstract",
            self.abstract,
            "",
            "## Introduction",
            self.introduction,
            "",
            "## Related Work",
            self.related_work,
            "",
            "## Methods",
            self.methods,
            "",
            "## Results",
            self.results,
            "",
            "## Discussion",
            self.discussion,
            "",
        ]
        return "\n".join(parts)


@dataclass
class SotaEntry:
    name: str
    lab: str
    year: int
    venue: str
    arxiv: str = ""
    doi: str = ""
    url: str = ""
    architecture: str = ""
    results: str = ""
    autonomy: str = ""
    limitations: str = ""
    steal: str = ""
    avoid: str = ""
    tags: list[str] = field(default_factory=list)
    domain: str = "cs"

    def cite(self) -> str:
        key = self.arxiv or self.doi or self.name
        return f"{self.name} ({self.lab}, {self.year}, {self.venue}; {key})"
