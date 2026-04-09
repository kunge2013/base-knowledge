---
title: LLM Wiki
date: 2026-04-09
last_updated: 2026-04-09
tags: [concept, knowledge-management, patterns]
sources: [["wiki/sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file.md", "Karpathy's LLM Wiki"]]
---

# LLM Wiki

**LLM Wiki** is a pattern for building personal knowledge bases where an LLM incrementally maintains a persistent, structured wiki of synthesized knowledge instead of just retrieving raw chunks at query time.

## Core Idea

Instead of:
- User adds documents → system chunks and embeds → at query time retrieve relevant chunks → LLM synthesizes answer from scratch *every time*

LLM Wiki does:
- User adds documents → LLM reads document → extracts and integrates information into wiki by creating/updating multiple interlinked pages → updates index and log → at query time answer from already-synthesized knowledge

The wiki is a **persistent, compounding artifact** that gets richer with every source added. Cross-references are already in place, contradictions already flagged.

## Key Contrast with RAG

| Aspect | Traditional RAG | LLM Wiki |
|--------|-----------------|----------|
| Synthesis | Done at query time, every query | Done at ingest time, once |
| Knowledge | Doesn't accumulate | Compounds over time |
| Cross-references | Not pre-computed | Maintained by LLM |
| Contradiction handling | Handled on-the-fly | Flagged when new info arrives |
| Maintenance | None (stateless) | LLM does it automatically |

## Three-Layer Architecture

1. **Raw sources** - Original documents in `raw/`, immutable.
2. **Wiki** - LLM-maintained markdown in `wiki/`, structured into sources, concepts, entities, queries.
3. **Schema** - Instructions like `CLAUDE.md` telling LLM the conventions and workflows.

## Key Operations

- **Ingest** - Add a new source, integrate into wiki across multiple pages
- **Query** - Answer question from wiki, save valuable answers back to wiki
- **Lint** - Periodic health check to find contradictions, orphans, and missing pages

## Author

Pattern originally described by [[entities/andrej-karpathy|Andrej Karpathy]].

## See Also

- [[sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file|Karpathy's LLM Wiki - Idea File Summary]]
- [[concepts/vannevar-bush-memex|Vannevar Bush's Memex]]
- [[concepts/knowledge-accumulation|Knowledge Accumulation]]
