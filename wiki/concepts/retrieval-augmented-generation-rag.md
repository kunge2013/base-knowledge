---
title: Retrieval-Augmented Generation (RAG)
date: 2026-04-09
last_updated: 2026-04-09
tags: [concept, llm, information-retrieval]
sources: [["wiki/sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file.md", "Karpathy's LLM Wiki"]]
---

# Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) is the dominant approach today for using LLMs with custom document collections.

## How RAG Works

1. User uploads a collection of documents
2. System chunks documents, creates embeddings, stores in a vector database
3. At query time: retrieve relevant chunks based on embedding similarity
4. LLM synthesizes answer from the retrieved chunks *every time* the question is asked

## Karpathy's Critique of RAG

In the LLM Wiki pattern, RAG is the baseline to improve upon because:
- The LLM rediscovers and re-synthesizes knowledge from scratch on every question
- No accumulation of knowledge over time
- A subtle question requiring synthesis from 5 documents requires finding and piecing everything together every time

## Contrast with LLM Wiki

See [[concepts/llm-wiki|LLM Wiki]] does the synthesis once at ingest time, and maintains it incrementally.

## See Also

- [[concepts/llm-wiki|LLM Wiki]]
- [[wiki/sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file|Karpathy's LLM Wiki - Idea File Summary]]
