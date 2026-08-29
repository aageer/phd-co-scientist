---
name: co-scientist
description: Run the full ideation → experiment → paper Co-Scientist loop
---

Read `running-co-scientist`. Restate the user's directive and constraints. Ethics screen. Then:

```bash
python -m swarm run "$DIRECTIVE" --domain cs
```

Return ranked hypotheses, best metrics, `paper.md` path, and residual risks.
