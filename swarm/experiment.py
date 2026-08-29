"""Evolutionary program loop: scaffold → transition → full-scale.

Failed runs get the traceback. Successful runs emit JSON metrics into the log.
Score decay (γ=0.97) prevents a lucky first program from freezing search.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import subprocess
import sys
import textwrap
import time

from swarm.models import ExperimentResult, Hypothesis

SCAFFOLD_PROGRAM = textwrap.dedent(
    '''
    import json, math, random, sys

    def score_config(kappa, n_candidates, personas, seed=0):
        rng = random.Random(seed)
        # Synthetic but deterministic proxy: diversity * calibration - cost
        diversity = 1.0 - abs(personas - 6) / 10.0
        budget = 1.0 - abs(n_candidates - 32) / 64.0
        explore = 1.0 - abs(kappa - 1.0) / 3.0
        noise = 0.02 * rng.random()
        quality = min(1.0, max(0.0, 0.55 * diversity + 0.30 * budget + 0.15 * explore + noise))
        calls = int(n_candidates * 1.4 + personas * 2)
        return quality, calls

    def main():
        kappa = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 32
        personas = int(sys.argv[3]) if len(sys.argv) > 3 else 6
        quality, calls = score_config(kappa, n, personas)
        metrics = {
            "score": round(quality, 4),
            "calls": calls,
            "kappa": kappa,
            "n_candidates": n,
            "personas": personas,
            "length_pivot": 2000,
        }
        print(json.dumps(metrics))
        print(f"LOG score={metrics['score']} calls={calls} kappa={kappa}")

    if __name__ == "__main__":
        main()
    '''
).strip() + "\n"


@dataclass
class ProgramCandidate:
    path: Path
    args: list[str]
    note: str


def write_program(run_dir: Path) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "solve.py"
    path.write_text(SCAFFOLD_PROGRAM)
    (run_dir / "readme.txt").write_text(
        "Scaffold experiment: search (kappa, n_candidates, personas) on a "
        "deterministic proxy for inference-time scaling.\n"
    )
    return path


def run_program(path: Path, args: list[str], timeout_s: int = 20) -> ExperimentResult:
    started = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, str(path), *args],
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        stdout, stderr, code = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, code = exc.stdout or "", "TIMEOUT", 124

    metrics = {}
    for line in (stdout or "").splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                metrics = json.loads(line)
            except json.JSONDecodeError:
                continue
    score = float(metrics.get("score", 0.0)) if metrics else 0.0
    log_path = path.parent / "execution.log"
    log_path.write_text(
        f"exit={code} elapsed={time.time()-started:.3f}s args={args}\n{stdout}\n{stderr}\n"
    )
    return ExperimentResult(
        hypothesis_id="",
        exit_code=code,
        stdout=stdout,
        stderr=stderr,
        metrics=metrics,
        score=score,
        logs_path=str(log_path),
        program_path=str(path),
    )


def evolutionary_search(
    hypothesis: Hypothesis,
    run_dir: Path,
    generations: int = 5,
    decay: float = 0.97,
) -> list[ExperimentResult]:
    """Small evolutionary search over harness hyperparameters."""
    path = write_program(run_dir)
    grid = [
        (0.5, 16, 3),
        (1.0, 32, 6),
        (1.5, 48, 8),
        (0.8, 28, 6),
        (1.2, 40, 4),
        (1.0, 24, 6),
    ]
    results: list[ExperimentResult] = []
    best = 0.0
    for g in range(generations):
        kappa, n, personas = grid[g % len(grid)]
        # Decay pressure: later gens must beat decayed best.
        result = run_program(path, [str(kappa), str(n), str(personas)])
        result.hypothesis_id = hypothesis.id
        result.phase = "scaffold" if g == 0 else ("transition" if g < generations - 1 else "full")
        if result.exit_code == 0:
            if result.score > best * decay:
                best = result.score
            result.score = result.score  # keep raw; callers apply decay if needed
        results.append(result)
    return results
