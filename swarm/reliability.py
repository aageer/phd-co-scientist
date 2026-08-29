"""Hallucination clipping and plagiarism scoring (paper §2.1).

S_score(P) = λ_review S_reviewer − λ_plag S_plag − λ_hall S_hall
Default λ = (1.0, 0.5, 1.0). Hallucination is hard-verified against E_log.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

CLAIM_RE = re.compile(
    r"(?:(?:accuracy|score|f1|auc|elo|mu|sigma|win.?rate|improvement|delta)\s*(?:of|=|:)?\s*)"
    r"([-+]?\d+(?:\.\d+)?(?:%)?)",
    flags=re.I,
)
NUMBER_RE = re.compile(r"[-+]?\d+(?:\.\d+)?")


@dataclass
class ClipResult:
    text: str
    hallucination_score: float
    clipped: list[str]
    verified: list[str]


def extract_numbers(text: str) -> set[str]:
    return {m.group(0) for m in NUMBER_RE.finditer(text or "")}


def hallucination_score(manuscript: str, execution_log: str) -> ClipResult:
    """Fraction of numeric claims that cannot be found in the log."""
    if not (execution_log or "").strip():
        return ClipResult(manuscript, 1.0, ["NO_EXECUTION_LOG"], [])

    log_nums = extract_numbers(execution_log)
    clipped: list[str] = []
    verified: list[str] = []
    rewritten = manuscript

    for match in CLAIM_RE.finditer(manuscript):
        raw = match.group(1).rstrip("%")
        # Accept the number or a close rounding present in the log.
        ok = raw in log_nums or any(_near(raw, n) for n in log_nums)
        if ok:
            verified.append(match.group(0))
        else:
            clipped.append(match.group(0))
            rewritten = rewritten.replace(match.group(0), f"[UNVERIFIED:{match.group(0)}]", 1)

    n = max(len(clipped) + len(verified), 1)
    score = len(clipped) / n
    return ClipResult(rewritten, score, clipped, verified)


def _near(a: str, b: str, tol: float = 1e-6) -> bool:
    try:
        return abs(float(a) - float(b)) <= tol
    except ValueError:
        return a == b


def ngrams(text: str, n: int = 8) -> set[tuple[str, ...]]:
    tokens = re.findall(r"[a-z0-9]+", (text or "").lower())
    if len(tokens) < n:
        return set()
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def plagiarism_score(text: str, corpus: Iterable[str], n: int = 8) -> float:
    """Max Jaccard overlap of n-grams against any corpus document."""
    src = ngrams(text, n)
    if not src:
        return 0.0
    worst = 0.0
    for doc in corpus:
        other = ngrams(doc, n)
        if not other:
            continue
        inter = len(src & other)
        union = len(src | other)
        if union:
            worst = max(worst, inter / union)
    return worst


def joint_score(
    reviewer: float,
    plagiarism: float,
    hallucination: float,
    lam_review: float = 1.0,
    lam_plag: float = 0.5,
    lam_hall: float = 1.0,
) -> float:
    return lam_review * reviewer - lam_plag * plagiarism - lam_hall * hallucination
