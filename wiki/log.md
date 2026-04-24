---
title: Change Log
date: 2026-04-09
last_updated: 2026-04-14
tags: [meta]
sources: []
---

# Change Log

This is an append-only chronological log of all changes to the wiki.

## [2026-04-09] initialize | Wiki setup

- Created directory structure for three-layer architecture
- Created CLAUDE.md schema with workflow definitions
- Created initial overview, index, and log pages
- Ready for first source ingest

## [2026-04-09] ingest | LLM Wiki by Andrej Karpathy

- Created: 1 source summary
- Created: 6 concepts (LLM Wiki, RAG, Memex, Knowledge Accumulation, PKM, ML Research)
- Created: 1 entity (Andrej Karpathy)
- Updated: index.md
- Raw source: `raw/articles/llm-wiki.md`

## [2026-04-09] ingest | Agentic Design Patterns - Chapter 1 - Prompt Chaining

- Created: 1 source summary
- Created: 8 concepts (Prompt Chaining, Context Engineering, Agentic Design Patterns, Pipeline Pattern, Prompt Engineering, LangChain, LangGraph, Crew AI)
- Created: 5 entities (LangChain, LangGraph, Crew AI, Google, OpenAI)
- Updated: index.md
- Raw source: `raw/books/agentic-design-patterns-智能体设计模式/Chapter 1_ Prompt Chaining.md`

## [2026-04-09] ingest | Agentic Design Patterns - Chapter 2 - Routing

- Created: 1 source summary
- Created: 5 concepts (Routing, Embeddings, Google ADK, Multi-Agent Systems, Conditional Logic)
- Created: 2 entities (Gemini, Marco Fago)
- Updated: 6 existing pages (agentic-design-patterns, google, langchain, langgraph, langgraph-concept, index)
- Raw source: `raw/books/agentic-design-patterns-智能体设计模式/Chapter 2_ Routing.md`

## [2026-04-09] lint | Wiki health check

- Created: 1 missing concept (AI Agents - AI 智能体)
- Fixed: added missing cross-references between related pages
- Fixed: added inbound link to Marco Fago entity page
- Checked: no contradictions, no broken links
- All pages up to date

## [2026-04-09] query | What is Prompt Chaining

- Created: saved query answer to wiki/queries/what-is-prompt-chaining.md
- Updated: index.md added the query page
- Summary: Explainer answer based on existing wiki content

## [2026-04-09] ingest | Karpathy's LLM Wiki - The Complete Guide to His Idea File

- Updated: 1 source summary (replaced original with full article summary)
- Created: 3 concepts (Three-Layer Architecture, Idea File, qmd)
- Updated: 3 existing concepts (LLM Wiki, RAG, Andrej Karpathy)
- Created: 1 entity (Antigravity.codes)
- Updated: 1 existing entity (Andrej Karpathy)
- Updated: index.md
- Raw source: `raw/articles/llm/Karpathy's LLM Wiki The Complete Guide to His Idea File.md`

## [2026-04-14] ingest | Arthas - 1. Arthas接入 + LangChain - 1. Agents

- Created: 2 source summaries (arthas-1-arthas-ji-ru, langchain-1-agents)
- Created: 15 concepts (Arthas, Model Context Protocol (MCP), ReAct Pattern, Static Model Selection, Dynamic Model Selection, Static Tools, Dynamic Tools, Structured Output, ToolStrategy, ProviderStrategy, Agent Middleware, Agent Memory, Custom Agent State)
- Created: 1 entity (Alibaba)
- Updated: 5 existing pages (ai-agents, langchain, langgraph, langchain-entity, langgraph-entity)
- Updated: index.md
- Raw sources:
  - `raw/articles/arthas/1. arthas接入.md`
  - `raw/articles/llm/langchain/1.Agents.md`

## [2026-04-23] coding | Deep Agents Quickstart - Chapter 2 Code Implementation

- Created: coding directory structure for deepagent-langchain
- Created: 6 code files (llm_config.py, 01_search_tool.py, 02_create_agent.py, 03_invoke_agent.py, README.md, Chapter_2_Quickstart_SUMMARY.md)
- Created: requirements.txt and .env.example
- Raw source: `raw/articles/llm/deepagent-langchain/2.Quickstart.md`
- Code location: `coding/langchain/deepagent-langchain/Chapter_2_Quickstart/`

## [2026-04-23] coding | Deep Agents Customize - Chapter 3 Code Implementation

- Created: coding directory structure for deepagent-langchain Chapter 3
- Created: 12 code files:
  - llm_config.py, requirements.txt, .env.example
  - 01_model_configuration.py (模型配置)
  - 02_custom_tools.py (自定义工具)
  - 03_system_prompt.py (系统提示设计)
  - 04_middleware.py (自定义中间件)
  - 05_subagents.py (子代理配置)
  - 06_human_in_the_loop.py (人工审批)
  - 07_skills.py (技能配置)
  - 08_memory.py (记忆文件)
  - 09_structured_output.py (结构化输出)
  - README.md, Chapter_3_Customize_SUMMARY.md
- Raw source: `raw/articles/llm/deepagent-langchain/3.Customize Deep Agents.md`
- Code location: `coding/langchain/deepagent-langchain/Chapter_3_Customize/`

