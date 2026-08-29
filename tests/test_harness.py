from swarm.factory import AgentFactory
from swarm.harness import agent_h_plan, main


def test_coalition_has_core_roles():
    names = {s.name for s in AgentFactory().coalition()}
    assert {"supervisor", "generation", "ranking", "ethics", "reliability", "architect"} <= names


def test_agent_h_plan_cost():
    plan = agent_h_plan("Design a held-out ablation for tournament selection", n_candidates=28)
    assert plan["est_llm_calls"] >= 28
    assert plan["length_pivot"] == 2000
    assert "Not a medical device" in plan["warning"]


def test_cli_sota_and_agents(capsys):
    assert main(["agents"]) == 0
    out = capsys.readouterr().out
    assert "supervisor" in out
    assert main(["sota", "--tag", "gdm"]) == 0
    assert "Co-Scientist" in capsys.readouterr().out
