---
title: LLM Wiki Operations
created: 2026-04-08
updated: 2026-04-08
sources: [raw/articles/Karpathy's LLM Wiki The Complete Guide to His Idea File.md]
related: [three-layer-architecture.md](three-layer-architecture.md), [wiki-vs-rag.md](wiki-vs-rag.md)
tags: [operations, llm-wiki, karpathy, knowledge-management, ingest-query-lint]
---

# LLM Wiki Operations

Karpathy defines three core operations for maintaining LLM Wiki: ingest, query, and lint. Each has clear trigger, process, and output.

## Operation 1: Ingest

**Trigger:** You place new source into raw/ and ask LLM to process it.

**Process:**
1. LLM reads source
2. Discusses key points with you
3. Writes summary page in wiki/sources/
4. Updates wiki/index.md
5. Updates related entity and concept pages throughout wiki
6. Appends entry to wiki/log.md

**Impact:** Single ingestion can cascade through 10-15 wiki pages.

**Example cascade:**
- Ingest paper on new transformer variant
- Creates summary page for that paper
- Updates "attention mechanism" concept page with new variant
- Updates "Scaling Laws" page if paper includes new benchmarks
- Updates entity page for authors' institution
- Updates comparison page if paper benchmarks known models
- Adds links from existing pages that reference new content
- Updates index.md with new page
- Logs import in activity log

**Human interaction style:** "I prefer importing one source at a time and staying engaged—I'll read the summary, check updates, guide the LLM to focus on what's important. But you can also batch import multiple sources without supervision."

## Operation 2: Query

**Trigger:** You ask questions about wiki content.

**Process:**
1. LLM searches wiki/index.md for relevant pages
2. Reads those pages
3. Synthesizes answer with [[wiki-links]] references
4. Output can be: markdown page, comparison table, slides (Marp), charts (matplotlib), diagrams (canvas)

**Key insight:** "Excellent answers can be archived back into the wiki as new pages."

**Compound effect:** Sources ingest into wiki, queries generate insights, best insights archive back into wiki pages. Wiki grows from external sources AND your own exploration.

**Example with archiving:**
```
> Compare MoE routing strategies across all sources.
> Which has best efficiency/quality tradeoff?

# LLM reads wiki/concepts/mixture-of-experts.md,
# wiki/sources/summary-moe-*.md, generates analysis

[LLM generates detailed comparison table]

> Excellent. Archive as wiki page.

# LLM creates query page wiki/comparisons/moe-routing-strategies.md
# Updates index.md, adds links from related pages
```

## Operation 3: Lint

**Trigger:** You ask LLM to perform health check (weekly recommended).

**Process:**
1. Scans all wiki pages
2. Identifies contradictions between pages
3. Finds orphaned pages (no inbound links)
4. Finds concepts mentioned but lacking dedicated pages
5. Identifies outdated information superseded by new sources
6. Suggests new questions to research
7. Recommends new sources to seek

**Purpose:** Keeps wiki healthy as it grows.

**Example output:**
```
Health Report (2026-04-04):

Contradictions (2):
- concepts/dense-vs-sparse.md claims dense > sparse below 10B,
  but sources/summary-moe-efficiency.md shows opposite results.
  Recommendation: Update and add nuance.
- entities/openai.md claims GPT-5 has 200B parameters,
  but sources/summary-gpt5-leak.md shows 300B parameters.

Orphaned Pages (3):
- concepts/tokenization.md (no incoming links)
- sources/summary-old-bert-paper.md (no references)
- comparisons/old-gpu-benchmark.md (outdated)

Missing Pages (4):
- "RLHF" mentioned 12 times, no concept page
- "Constitutional AI" mentioned 8 times, no page
- "KV Cache" referenced in 5 sources, no page
- "Speculative Decoding" mentioned 3 times, no page

Suggested Investigations:
- No sources on inference optimizations since 2025
- Meta AI entity page sparse (only 1 source)
- "Scaling Laws" page not updated in 3 weeks
```

## Index.md as RAG Replacement

For medium-scale wikis (~100 sources, ~hundreds of pages), index.md replaces vector-based RAG:

- LLM reads index.md (few thousand tokens)
- Identifies relevant pages by scanning descriptions
- Reads those pages directly
- No vector database or embedding infrastructure needed

Works "surprisingly well at medium scale" and avoids need for complex RAG infrastructure.

## Related Concepts

- [Three-Layer Architecture](three-layer-architecture.md) - Operations operate on wiki/ and raw/ layers
- [Wiki vs RAG](wiki-vs-rag.md) - Query operation demonstrates wiki advantage over RAG

## Sources

- raw/articles/Karpathy's LLM Wiki The Complete Guide to His Idea File.md - Defined three operations (ingest, query, lint), described workflows, explained index.md as RAG replacement
