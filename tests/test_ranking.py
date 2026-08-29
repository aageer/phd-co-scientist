from swarm.models import Hypothesis, SkillRating
from swarm.ranking import run_tournament, ucb, update_pair


def test_trueskill_winner_mu_rises():
    w, l = SkillRating(), SkillRating()
    nw, nl = update_pair(w, l)
    assert nw.mu > w.mu
    assert nl.mu < l.mu
    assert nw.sigma < w.sigma


def test_ucb_prefers_uncertain_equal_mu():
    a = Hypothesis(title="a", statement="a")
    b = Hypothesis(title="b", statement="b")
    a.rating = SkillRating(mu=25, sigma=1)
    b.rating = SkillRating(mu=25, sigma=8)
    assert ucb(b) > ucb(a)


def test_tournament_ranks_testable_ideas():
    weak = Hypothesis(title="Vague vibe", statement="Something something science")
    strong = Hypothesis(
        title="Held-out metric",
        statement="Evaluate a novel ablation on a held-out benchmark and log the score",
        method="Run evaluate.py and write metrics.json",
        citations=["arXiv:2608.26701"],
        review={"overall": 0.9},
    )
    ranked = run_tournament([weak, strong], rounds=12)
    assert ranked[0].title == strong.title
