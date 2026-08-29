"""Paper-diagram entrypoint. Prefer `python -m swarm`."""

from swarm.solve import solve

if __name__ == "__main__":
    import json
    import sys

    goal = " ".join(sys.argv[1:]) or (
        "Discover an inference-time scaling architecture that beats a single-pass "
        "backbone on a held-out proxy without seeing rubrics during search."
    )
    report = solve(goal)
    print(json.dumps({"run_dir": report.run_dir, "paper": report.manuscript_path, "score": report.manuscript_score}))
