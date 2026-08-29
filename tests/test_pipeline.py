from pathlib import Path

from swarm.experiment import evolutionary_search, write_program, run_program
from swarm.ideation import default_directive, evolve
from swarm.literature import load_catalog
from swarm.models import Hypothesis
from swarm.paper import write_manuscript
from swarm.solve import solve


def test_catalog_loads():
    entries = load_catalog()
    assert len(entries) >= 15
    assert any(e.arxiv == "2608.26701" for e in entries)


def test_ideation_returns_ethics_ok_population():
    pop = evolve(default_directive("Find a better tournament scaffold"), generations=3)
    assert len(pop) >= 4
    assert any(h.ethics_ok for h in pop)


def test_experiment_emits_metrics(tmp_path: Path):
    path = write_program(tmp_path)
    result = run_program(path, ["1.0", "32", "6"])
    assert result.exit_code == 0
    assert "score" in result.metrics
    assert Path(result.logs_path).exists()


def test_paper_refuses_without_logs():
    d = default_directive("x")
    h = Hypothesis(title="t", statement="s")
    try:
        write_manuscript(d, h, [])
        raise AssertionError("should have refused")
    except RuntimeError as exc:
        assert "logs" in str(exc).lower()


def test_end_to_end_solve(tmp_path: Path):
    report = solve(
        "Discover a length-calibrated tournament agent on a held-out proxy",
        generations=2,
        population=6,
        run_dir=tmp_path,
    )
    assert Path(report.manuscript_path).exists()
    assert report.experiment_best["exit_code"] == 0
    assert "score" in report.experiment_best["metrics"]


def test_evolutionary_search_runs(tmp_path: Path):
    h = Hypothesis(title="proxy", statement="search kappa")
    results = evolutionary_search(h, tmp_path, generations=3)
    assert len(results) == 3
    assert max(r.score for r in results) > 0
