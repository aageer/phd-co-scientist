"""Load and query the curated SOTA catalog. Optional live keyword filter."""

from __future__ import annotations

from pathlib import Path
import json
from typing import Iterable

from swarm.models import SotaEntry

CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "sota_catalog.json"


def load_catalog(path: Path | None = None) -> list[SotaEntry]:
    raw = json.loads((path or CATALOG_PATH).read_text())
    return [SotaEntry(**row) for row in raw["entries"]]


def filter_entries(
    entries: Iterable[SotaEntry],
    *,
    lab: str | None = None,
    domain: str | None = None,
    tag: str | None = None,
    year_min: int | None = None,
    query: str | None = None,
) -> list[SotaEntry]:
    q = (query or "").lower()
    out = []
    for e in entries:
        if lab and lab.lower() not in e.lab.lower() and lab.lower() not in e.name.lower():
            continue
        if domain and e.domain != domain:
            continue
        if tag and tag not in e.tags:
            continue
        if year_min and e.year < year_min:
            continue
        blob = " ".join([e.name, e.lab, e.architecture, e.results, " ".join(e.tags)]).lower()
        if q and q not in blob:
            continue
        out.append(e)
    return sorted(out, key=lambda x: (-x.year, x.lab, x.name))


def render_markdown(entries: list[SotaEntry]) -> str:
    lines = [
        "# SOTA catalog",
        "",
        f"{len(entries)} systems. Prefer primary papers. Verify identifiers before you cite.",
        "",
        "| System | Lab | Year | Venue | Steal | Avoid |",
        "|---|---|---|---|---|---|",
    ]
    for e in entries:
        lines.append(
            f"| {e.name} | {e.lab} | {e.year} | {e.venue} | {e.steal} | {e.avoid} |"
        )
    lines.append("")
    for e in entries:
        lines += [
            f"## {e.name}",
            "",
            f"- Cite: `{e.cite()}`",
            f"- Architecture: {e.architecture}",
            f"- Results: {e.results}",
            f"- Autonomy: {e.autonomy}",
            f"- Limitations: {e.limitations}",
            f"- Steal: {e.steal}",
            f"- Avoid: {e.avoid}",
            "",
        ]
    return "\n".join(lines)


def corpus_for_plagiarism(entries: Iterable[SotaEntry]) -> list[str]:
    return [
        " ".join([e.name, e.architecture, e.results, e.steal, e.avoid])
        for e in entries
    ]
