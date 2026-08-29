Co-Scientist experiment contract (Figure 1 files)

solve.py     Full loop or the program under test. Must print one JSON metrics object.
factory.py   Agent coalition.
agents.py    Personas / prompts.
harness.py   CLI and inference-time plan.
execution.log  Created at runtime. Paper writing is illegal without it.

Default proxy metric (offline):
  score in [0,1], calls:int, kappa, n_candidates, personas, length_pivot=2000

Replace the proxy with a real held-out benchmark before claiming SOTA.
