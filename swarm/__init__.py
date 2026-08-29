"""PhD Co-Scientist swarm: ideation, experiment, paper, SOTA."""

__version__ = "1.0.0"

from swarm.models import (
    Autonomy,
    ExperimentResult,
    Hypothesis,
    Manuscript,
    ResearchDirective,
    SkillRating,
    SotaEntry,
)
from swarm.factory import AgentFactory
from swarm.solve import solve

__all__ = [
    "Autonomy",
    "ExperimentResult",
    "Hypothesis",
    "Manuscript",
    "ResearchDirective",
    "SkillRating",
    "SotaEntry",
    "AgentFactory",
    "solve",
    "__version__",
]
