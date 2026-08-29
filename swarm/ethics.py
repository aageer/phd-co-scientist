"""Two-layer research-safety gate (Schmidgall et al. 2026 §2.2).

Layer 1: refuse the top-level directive if it is dual-use / restricted.
Layer 2: binary ethics check on each hypothesis with textual feedback.
Fail closed on match; never invent a workaround.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from swarm.models import Hypothesis, ResearchDirective

_RESTRICTED = (
    r"\b(bioweapon|pathogen enhanc|gain.of.function|reverse genetics of (ebola|smallpox|1918))\b",
    r"\b(nerve agent|sarin|vx |ricin|weaponize)\b",
    r"\b(child sexual|csam|cse)\b",
    r"\b(build (an )?exploit|zero.day|ransomware|keylogger)\b",
    r"\b(undetectable phishing kit|carding|fake id factory)\b",
)

_REVIEW_FLAGS = (
    ("human subjects without irb", "Requires IRB / ethics board before any human data work."),
    ("clinical deployment", "Do not ship medical advice systems. Keep to benchmarked research."),
    ("dual-use chemistry", "Refuse synthesis routes for restricted precursors."),
    ("surveillance at scale", "Do not design covert monitoring of people."),
)


@dataclass
class EthicsVerdict:
    ok: bool
    reason: str
    layer: int


def _matches(text: str) -> str | None:
    blob = text.lower()
    for pattern in _RESTRICTED:
        if re.search(pattern, blob, flags=re.I):
            return pattern
    return None


def screen_directive(directive: ResearchDirective) -> EthicsVerdict:
    blob = " ".join([directive.goal, *directive.constraints, *directive.forbidden])
    hit = _matches(blob)
    if hit:
        return EthicsVerdict(False, f"Directive matches restricted category ({hit}). Stop.", 1)
    return EthicsVerdict(True, "Directive passed layer-1 screen.", 1)


def screen_hypothesis(hypothesis: Hypothesis, directive: ResearchDirective | None = None) -> EthicsVerdict:
    blob = " ".join(
        [
            hypothesis.title,
            hypothesis.statement,
            hypothesis.method,
            hypothesis.safety_notes,
            *(directive.forbidden if directive else []),
        ]
    )
    hit = _matches(blob)
    if hit:
        hypothesis.ethics_ok = False
        hypothesis.ethics_feedback = f"Hypothesis matches restricted category ({hit})."
        return EthicsVerdict(False, hypothesis.ethics_feedback, 2)

    notes = []
    low = blob.lower()
    for needle, msg in _REVIEW_FLAGS:
        if needle in low:
            notes.append(msg)
    hypothesis.ethics_ok = True
    hypothesis.ethics_feedback = " ".join(notes) if notes else "Ethics-proofed."
    return EthicsVerdict(True, hypothesis.ethics_feedback, 2)
