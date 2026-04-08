---
title: Wiki vs RAG
created: 2026-04-08
updated: 2026-04-08
sources: [raw/articles/Karpathy's LLM Wiki The Complete Guide to His Idea File.md]
related: [idea-files.md](idea-files.md), [three-layer-architecture.md](three-layer-architecture.md)
tags: [rag, knowledge-management, llm-wiki, karpathy, persistent-knowledge]
---

# Wiki vs RAG

The fundamental shift in LLM knowledge management: moving from query-time retrieval (RAG) to persistent wiki compilation.

## The RAG Problem

**How RAG works:**
- Upload files to system
- Query triggers retrieval of relevant chunks
- LLM synthesizes answer from chunks
- Each query re-discovers knowledge from scratch

**Problems identified:**
- No knowledge accumulation between queries
- Tomorrow's same question = same work
- Cross-references must be rebuilt each time
- Contradictions may go unnoticed
- System is a black box—no persistent knowledge structure

**Tools using RAG:**
- Google NotebookLM
- ChatGPT file uploads
- Most enterprise AI tools

## The Wiki Solution

**How LLM Wiki works:**
- LLM maintains persistent markdown wiki
- Sources compile into interconnected pages
- Cross-references pre-built and maintained
- Contradictions flagged during ingestion
- Knowledge compounds over time

**Key principle:** "The wiki only needs to be compiled once, then kept up to date, without re-deriving for every query."

```
When you add new source:
LLM doesn't just index it—it INTEGRATES it:
- Updates entity pages with new info
- Revises topic summaries
- Flags contradictions with existing claims
- Strengthens or questions evolving synthesis
- Adds links from existing pages
```

## Comparison

| Aspect | RAG | LLM Wiki |
|--------|-----|----------|
| **Knowledge processing** | Query time (every question) | Ingest time (per source once) |
| **Cross-references** | Discovered per query | Pre-built and maintained |
| **Contradictions** | May go unnoticed | Flagged during ingestion |
| **Knowledge accumulation** | None—each query starts from zero | Compounds with each source/query |
| **Output format** | Chat reply (ephemeral) | Persistent markdown files |
| **Maintained by** | System (black box) | LLM (transparent, editable) |
| **Human role** | Upload and query | Curate, explore, question |
| **Example tools** | NotebookLM, ChatGPT | Karpathy's LLM Wiki |

## The Compound Effect

Wiki is "a persistent, compound product." Cross-references exist. Contradictions are flagged. Synthesis reflects everything you've read. Each source added, each question asked, makes wiki richer.

## Human-AI Collaboration

**Workflow:**
- You: Find sources, explore, ask right questions
- LLM: All heavy lifting—summarizing, cross-referencing, filing, documenting

**Daily setup:** Open LLM agent in one window, Obsidian in another. LLM edits based on conversation. You browse results in real-time—clicking links, checking relationships, reading updated pages.

**Metaphor:** "Obsidian is the IDE; LLM is the programmer; Wiki is the codebase."

## Related Concepts

- [Idea Files](idea-files.md) - Pattern sharing that enables wiki approach
- [Three-Layer Architecture](three-layer-architecture.md) - Wiki layer in architecture

## Sources

- raw/articles/Karpathy's LLM Wiki The Complete Guide to His Idea File.md - Compared RAG vs wiki approaches, identified RAG problems, explained compound knowledge effect
