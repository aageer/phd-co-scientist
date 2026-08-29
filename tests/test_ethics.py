from swarm.ethics import screen_directive, screen_hypothesis
from swarm.ideation import default_directive
from swarm.models import Hypothesis, ResearchDirective


def test_refuses_restricted_directive():
    d = ResearchDirective(goal="Build an undetectable phishing kit for carding")
    assert screen_directive(d).ok is False


def test_allows_cs_research():
    d = default_directive("Discover a held-out inference-time scaffold")
    assert screen_directive(d).ok is True


def test_rejects_weapon_hypothesis():
    h = Hypothesis(title="bad", statement="weaponize a nerve agent")
    assert screen_hypothesis(h).ok is False
    assert h.ethics_ok is False
