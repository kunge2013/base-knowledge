---
title: Overview
date: 2026-04-09
last_updated: 2026-04-14
tags: [meta]
sources: []
---

# Overview

This is a personal LLM Wiki following Andrej Karpathy's LLM Wiki pattern. It's a persistent, compounding knowledge base maintained by Claude Code.

## Purpose

This wiki accumulates knowledge on:
- Machine learning research
- AI agent design patterns
- Java diagnostics and debugging tools
- Competitive analysis
- Book notes
- General learning

## Contents

Currently the wiki includes:
- **Agentic Design Patterns**: Book notes on foundational AI agent patterns:
  - [[concepts/prompt-chaining|Prompt Chaining]] - Sequential decomposition of complex tasks
  - [[concepts/routing|Routing]] - Dynamic conditional logic for adaptive agent behavior
  - [[concepts/context-engineering|Context Engineering]] - Systematic construction of complete information environments
  - Coverage of major frameworks: [[concepts/langchain|LangChain]], [[concepts/langgraph|LangGraph]], [[concepts/google-adk|Google ADK]], [[concepts/crew-ai|Crew AI]]
- **LangChain Agents**: Detailed documentation of LangChain Agent implementation:
  - [[concepts/react-pattern|ReAct Pattern]] - Reasoning + Acting 迭代执行模式
  - [[concepts/static-model-selection|Static Model Selection]] / [[concepts/dynamic-model-selection|Dynamic Model Selection]] - 模型选择策略
  - [[concepts/static-tools|Static Tools]] / [[concepts/dynamic-tools|Dynamic Tools]] - 工具管理方式
  - [[concepts/structured-output|Structured Output]] - 结构化输出，两种策略 [[providerstrategy|ProviderStrategy]] / [[toolstrategy|ToolStrategy]]
  - [[concepts/agent-middleware|Agent Middleware]] - 可扩展中间件机制
  - [[concepts/agent-memory|Agent Memory]] / [[concepts/custom-agent-state|Custom Agent State]] - 记忆和状态管理
- **Java Diagnostics**:
  - [[concepts/arthas|Arthas]] - Alibaba 开源 Java 诊断调试工具
  - [[concepts/model-context-protocol-mcp|Model Context Protocol (MCP)]] - AI 客户端与外部工具通信协议
- **LLM Wiki methodology**: Complete documentation of Andrej Karpathy's LLM Wiki pattern:
  - [[concepts/llm-wiki|LLM Wiki]] - Core pattern overview and comparison with traditional RAG
  - [[concepts/three-layer-architecture|Three-Layer Architecture - 三层架构]] - The three-layer separation (raw/ + wiki/ + Schema)
  - [[concepts/idea-file|Idea File - 想法文件]] - The idea sharing concept for the AI agent era
  - [[concepts/qmd|qmd - Quick Markdown Search]] - Local hybrid markdown search engine
  - [[concepts/retrieval-augmented-generation-rag|Retrieval-Augmented Generation (RAG)]] - Traditional approach comparison

## How It Works

Unlike RAG where knowledge is re-synthesized from scratch on every query, this wiki is incrementally maintained by an LLM. When new sources are added, the LLM:
1. Reads the source
2. Extracts key information
3. Updates/creates pages across the wiki
4. Maintains cross-references
5. Flags contradictions

The knowledge is already synthesized and interlinked - it compounds over time.

## Structure

- [[index|Index]] - complete catalog of all pages
- [[log|Log]] - chronological change log
- [sources/](sources/) - summaries of raw sources
- [concepts/](concepts/) - concept and topic pages
- [entities/](entities/) - entity pages (authors, companies, products)
- [queries/](queries/) - saved query responses and analyses

## Getting Started

To add a new source: place it in `raw/` and ask Claude to ingest it.

To query the wiki: ask a question, and Claude will search relevant pages and synthesize an answer. Valuable answers get saved as new wiki pages.
