---
title: "Source Summary: Karpathy's LLM Wiki Idea File"
created: 2026-04-08
updated: 2026-04-08
source: raw/articles/Karpathy's LLM Wiki The Complete Guide to His Idea File.md
depth: 300
articles_created: [idea-files.md, wiki-vs-rag.md, three-layer-architecture.md, llm-wiki-operations.md]
tags: [karpathy, llm-wiki, knowledge-management, idea-files]
---

# Karpathy's LLM Wiki Idea File - Summary

This article provides a comprehensive analysis of Andrej Karpathy's "idea file" for building LLM-maintained wikis, a shift from traditional code sharing to pattern sharing in the AI agent era.

## The Core Insight

Karpathy introduces the concept of **idea files**—structured descriptions of patterns and architectures designed to be interpreted by LLM agents rather than shared as executable code. In an era where everyone has access to LLM agents (Claude Code, OpenAI Codex, Cursor), sharing the *idea* is more portable and valuable than sharing the *implementation* because the agent can adapt the pattern to the user's specific environment and configuration.

## Key Concept: Wiki vs RAG

The fundamental shift is moving from RAG (Retrieval-Augmented Generation) to a **persistent wiki** approach:

```
RAG Flow:
Sources → Upload → Query time retrieval → Answer

LLM Wiki Flow:
Sources → Ingest → Wiki compilation → Query → Answer
           ↓
        Persistent (cross-references accumulated)
```

**RAG problems:**
- LLM re-discovers knowledge for every question
- No knowledge accumulation between queries
- Contradictions may go unnoticed

**Wiki solutions:**
- Knowledge compiled once and maintained
- Pre-built cross-references
- Contradictions flagged during ingestion
- Compound growth with each source

## Three-Layer Architecture

```
raw/              # Immutable source documents (append-only)
  articles/       # Blog posts, news
  papers/         # Academic papers
  repos/          # Code documentation
  data/           # Datasets, benchmarks
  assets/         # Downloaded images

wiki/             # LLM-generated, interconnected markdown
  index.md        # Table of contents
  log.md          # Activity timeline
  overview.md     # High-level synthesis
  concepts/       # Concept pages (attention, scaling laws)
  entities/       # Entity pages (OpenAI, Anthropic)
  sources/        # Source summaries
  comparisons/    # Comparative analyses

CLAUDE.md        # Schema: rules, formats, workflows
```

**Layer 1: raw/** - The source of truth. LLM reads only, never writes.
**Layer 2: wiki/** - LLM's domain. Creates, updates, maintains all content.
**Layer 3: Schema** - The contract. Defines structure, frontmatter, workflows.

## Core Operations

### Ingest
When you add a source:
1. LLM reads the source
2. Discusses key points with you
3. Creates/updates summary page
4. Updates index.md
5. Updates related concept and entity pages
6. Appends entry to log.md

Single ingestion can ripple through 10-15 wiki pages.

### Query
When you ask questions:
1. LLM reads index.md to find relevant pages
2. Reads those pages
3. Synthesizes answer with [[wiki-links]] references
4. Suggests archiving valuable answers as new pages

### Lint
Periodic health checks:
- Identify contradictions between pages
- Find orphaned pages (no inbound links)
- Suggest missing pages for mentioned concepts
- Flag outdated information superseded by new sources
- Recommend new research areas

## Tool Stack

| Tool | Role | Essential? |
|------|------|------------|
| **Obsidian** | Wiki viewer/browser | Recommended |
| **qmd** | Local markdown search (BM25 + vector + LLM rerank) | Optional |
| **Obsidian Web Clipper** | Capture web articles as markdown | Recommended |
| **Git** | Version control for wiki | Recommended |
| **LLM Agent** | Wiki maintainer (Claude Code, Codex) | Essential |

## Historical Context

The concept connects to **Vannevar Bush's Memex (1945)**—a vision of personalized, associative knowledge where document links matter as much as the documents themselves. Bush's unsolved problem: *who maintains?* LLM Wiki solves this—the agent doesn't get bored, doesn't forget updates, and can process 15 files at once.

## What This Source Covers

- Idea files as a new open source format for AI agents
- Comparison between RAG and persistent wiki approaches
- Three-layer architecture (raw, wiki, schema)
- Core operations: ingest, query, lint
- Index.md as RAG replacement for medium-scale wikis
- Tool recommendations (qmd, Obsidian, Git)
- Implementation guide with step-by-step setup
- Use cases: personal knowledge management, research, reading, enterprise
- Historical connection to Memex and associative computing
- Community extensions and patterns

## Wiki Articles From This Source

- [Idea Files](idea-files.md) - Pattern sharing vs code sharing in the AI agent era
- [Wiki vs RAG](wiki-vs-rag.md) - Persistent compilation vs query-time retrieval
- [Three-Layer Architecture](three-layer-architecture.md) - raw/, wiki/, and schema layers
- [LLM Wiki Operations](llm-wiki-operations.md) - Ingest, query, and lint workflows
