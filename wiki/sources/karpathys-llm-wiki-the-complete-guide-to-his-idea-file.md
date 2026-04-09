---
title: Karpathy's LLM Wiki - The Complete Guide to His Idea File
date: 2026-04-09
last_updated: 2026-04-09
tags: [source, knowledge-management, llm-wiki, patterns]
sources: [["raw/articles/llm-wiki.md", "LLM Wiki - Andrej Karpathy"]]
---

# Karpathy's LLM Wiki - Idea File Summary

This is the original idea file by Andrej Karpathy that describes the LLM Wiki pattern for building personal knowledge bases with LLMs.

## Core Idea

LLM Wiki is an alternative to RAG for personal knowledge bases:

- **Traditional RAG**: Retrieve raw chunks at query time, re-synthesize from scratch for every question. No accumulation.
- **LLM Wiki**: LLM incrementally builds and maintains a persistent, structured wiki. When adding a new source, the LLM extracts information, updates existing pages, and maintains cross-references. Knowledge is already synthesized when you ask a question.

Key difference: **the wiki is a persistent, compounding artifact** that gets richer with every source added. The LLM does all the bookkeeping automatically.

## Architecture

Three-layer architecture:

1. **Raw sources** - `raw/` directory containing original documents. **Immutable** - LLM never modifies these. This is the source of truth.
2. **Wiki** - `wiki/` directory containing LLM-generated markdown. LLM owns this layer entirely. Creates and updates pages.
3. **Schema** - `CLAUDE.md` (this repo) containing instructions for the LLM on conventions and workflows. Co-evolved over time.

## Key Workflows

### Ingest

When adding a new source:
1. LLM reads the source
2. Discusses key takeaways with user
3. Creates a summary page (this page)
4. Extracts key concepts → creates/updates concept pages
5. Extracts key entities → creates/updates entity pages
6. Updates [[index]]
7. Appends to [[log]]
8. Updates overview if needed

A single source typically touches 5-15 wiki pages. This integration is what makes the wiki valuable.

### Query

When answering a question:
1. LLM reads index to find relevant pages
2. Reads all relevant pages
3. Synthesizes answer with citations
4. If answer is valuable/enduring, saves it as a new wiki page in `queries/`

Good answers compound - they don't disappear into chat history.

### Lint

Periodic health check:
- Look for contradictions between pages
- Flag stale claims superseded by newer sources
- Find orphan pages (no inbound links)
- Identify concepts mentioned without a page
- Add missing cross-references
- Suggest new questions/sources to explore

## Index and Log

- **[[index]]** - Content-oriented catalog of all pages, organized by category. Updated on every ingest. Works well for moderate scale (~100 sources, hundreds of pages) without need for embedding-based search infrastructure.
- **[[log]]** - Append-only chronological record. Entries: `## [YYYY-MM-DD] action | Description`. Easy to parse with simple tools.

## Use Cases

Applies to many contexts:
- [[concepts/personal-knowledge-management|Personal knowledge management]] (goals, health, journaling)
- [[concepts/ml-research|Machine learning research]] (deep dives over time)
- Book notes (characters, themes, plot threads)
- Business/team internal wikis (maintained by LLM from Slack, meetings, docs)
- Competitive analysis, due diligence, trip planning, course notes, hobbies

## Why This Works

- Humans: Curate sources, direct analysis, ask good questions, think about what it means
- LLM: Does all the tedious bookkeeping (summarizing, cross-referencing, updating, maintaining)
- LLMs don't get bored, so maintenance cost is near zero. Wiki stays maintained as it grows.

## Related Concepts

- [[concepts/vannevar-bush-memex|Vannevar Bush's Memex (1945)]] - The original vision of a personal associative knowledge store.

## Original Source

- Raw file: `raw/articles/llm-wiki.md`
- Author: [[entities/andrej-karpathy|Andrej Karpathy]]
