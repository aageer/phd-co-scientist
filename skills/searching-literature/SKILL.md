---
name: searching-literature
description: Use when grounding a hypothesis or related-work section in primary papers, arXiv IDs, or DOIs
---

# Searching Literature

## Overview

Quote-level grounding. Abstracts are not papers. Catalog rows are not citations.

## Instructions

1. Start from `data/sota_catalog.json` + Semantic Scholar / arXiv / OpenAlex / alphaXiv.
2. Open the PDF. Extract the claim you will rely on, with section or page.
3. Record: authors, year, venue, identifier, one-sentence result, what not to copy.
4. Prefer primary over blog. Prefer Nature/Science/NeurIPS over Twitter threads.
5. For health benchmarks, cite Arora 2025 and Hicks 2026 rather than screenshots.

## Examples

Cite: `Schmidgall et al., 2026, arXiv:2608.26701, §3.3 Agent_H, Table 2`.
Do not cite: "a GDM blog said they beat GPT-5".

## Performance Notes

One worker per lab or per query cluster. Dedup by arXiv id.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Paywalled | Use the arXiv / accepted author PDF. |
| Identifier missing | Do not invent one. Mark `id=unverified`. |
