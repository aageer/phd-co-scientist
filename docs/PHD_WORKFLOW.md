# PhD workflow

A practical cadence for using this Co-Scientist during a CS PhD.

## First day

1. Install the Cursor plugin (this repo root).
2. `python -m pytest tests`
3. `python -m swarm sota --domain cs`
4. Write your real directive in one paragraph + constraints + a held-out metric.
5. `/co-scientist` or `python -m swarm run "..."`.

## Weekly (`/phd-weekly`)

- 30 minutes: SOTA delta (one Grok swarm if a big week).
- One experiment mutation or one ideation generation — not a new paper.
- File `runs/<date>/` with logs.
- Half-page note: verified number, failed idea, next metric.

## When to swarm

Use `/swarm` when the work **partitions**:

- 6 labs × SOTA
- 4 races of the same architecture idea
- Ablation matrix (routing, judge, length, verifier)

Do not swarm a single bug.

## Promotion bar (idea → chapter)

An idea may enter a thesis chapter only if:

1. Ethics PASS
2. Held-out metric exists and was not used for search
3. `execution.log` contains every number you will write
4. Related work cites primary papers
5. A human (you) can re-run `solve.py`

## What this will not do

- Replace your advisor
- Run a CVD furnace
- Give medical advice
- Guarantee a conference accept

It will keep you from the two failure modes that killed first-wave AI Scientists: **fake tables** and **copied methods**.
