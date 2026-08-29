---
name: running-grok-swarm
description: Use when the user asks to swarm, fan out Grok workers, race labs, or cover SOTA slices in parallel
---

# Running Grok Swarm

## Overview

Fan out N Grok workers, drain them, return one report. Parent does not paste raw dumps.

## Instructions

1. **Frame.** Done predicate + artifact. Shape: partition, race, or mixed. Declare first-pass / rank-all / best-of.
2. **N.** User value or one worker per lab/slice. N is workers, not concurrency.
3. **Fan out.** One message, N `generalPurpose` subagents, `run_in_background: true`, model `cursor-grok-4.6-high-fast` (or the user's Grok id). Isolated briefs.
4. **Each brief** includes goal, slice, citations required, PASS/ISSUES/BLOCKED.
5. **Aggregate.** Table + one-line issues + dropouts. Apply the race rule.
6. **Report.** One memo the PhD can file.

```bash
python -m swarm swarm "inference-time scaling SOTA" -n 6
```

Default slices: gdm, stanford, sakana, futurehouse, openai-eval, cs-agents.

## Examples

Race: 4 workers, same "beat Agent_H cheaply" brief, best-of by held-out proxy score.
Coverage: 6 workers, one lab each, merge into `docs/SOTA.md`.

## Performance Notes

If a worker drops, proceed with N-1 and say so. Do not respawn forever.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Workers overlap | You wrote the same brief 6 times. Partition. |
| Novel claims without ids | Mark ISSUES. Parent verifies. |
