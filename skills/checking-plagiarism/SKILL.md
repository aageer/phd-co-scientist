---
name: checking-plagiarism
description: Use when a hypothesis or manuscript might reuse methods or prose from the SOTA catalog or source papers
---

# Checking Plagiarism

## Overview

Gupta & Pruthi 2025 measured up to ~24% plagiarism in AI-written papers. We penalize n-gram overlap and derivative methods.

## Instructions

1. Build a corpus: SOTA catalog text + any PDFs you actually used.
2. 8-gram Jaccard. Flag > 0.15 for prose; method-level copies fail even if wording changed.
3. Idea-level: reflection agent applies prompt penalties instead of a single number (paper §2.1.1).
4. Quoting with a citation is allowed. Silent paraphrase of a method is not.
5. λ_plag = 0.5 on manuscripts so discussion of prior work remains possible.

```python
from swarm.reliability import plagiarism_score
from swarm.literature import corpus_for_plagiarism, load_catalog
plagiarism_score(text, corpus_for_plagiarism(load_catalog()))
```

## Examples

Fail: Agent_H's eight phases copied in order with new names.
OK: "We adopt pairwise tournaments (Gottweis 2026; Herbrich 2006) and change the routing rule."

## Performance Notes

Run on hypotheses *and* papers. Cheap.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Related Work lights up | Expected shared citations; inspect methods/results instead. |
