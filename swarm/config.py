from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    xai_api_key: str = ""
    xai_base_url: str = "https://api.x.ai/v1"
    xai_model: str = "grok-4-1-fast-reasoning"
    openai_api_key: str = ""
    openai_base_url: str = ""
    openai_model: str = "gpt-5.6"
    runs_dir: str = "runs"
    population: int = 8
    generations: int = 6
    kappa: float = 1.0
    crossover_p: float = 0.7
    temperature: float = 1.6
    score_decay: float = 0.97
    timeout_s: int = 20

    @property
    def has_llm(self) -> bool:
        return bool(self.xai_api_key or self.openai_api_key)


def load_settings() -> Settings:
    return Settings(
        xai_api_key=os.environ.get("XAI_API_KEY", ""),
        xai_base_url=os.environ.get("XAI_BASE_URL", "https://api.x.ai/v1"),
        xai_model=os.environ.get("XAI_MODEL", "grok-4-1-fast-reasoning"),
        openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
        openai_base_url=os.environ.get("OPENAI_BASE_URL", ""),
        openai_model=os.environ.get("OPENAI_MODEL", "gpt-5.6"),
        runs_dir=os.environ.get("COSCI_RUNS_DIR", "runs"),
        population=int(os.environ.get("COSCI_POPULATION", "8")),
        generations=int(os.environ.get("COSCI_GENERATIONS", "6")),
        kappa=float(os.environ.get("COSCI_KAPPA", "1.0")),
    )
