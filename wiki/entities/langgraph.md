---
title: LangGraph
date: 2026-04-09
last_updated: 2026-04-14
tags: [product, llm-framework, langchain]
sources: [["wiki/sources/agentic-design-patterns-chapter-1-prompt-chaining", "Agentic Design Patterns - Chapter 1 - Prompt Chaining"], ["wiki/sources/agentic-design-patterns-chapter-2-routing", "Agentic Design Patterns - Chapter 2 - Routing"], ["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# LangGraph

LangGraph 是由 LangChain 公司开发的一个开源框架，用于构建有状态的、基于图的大语言模型智能体应用。

## 关系

LangGraph 由 [[entities/langchain|LangChain]] 公司开发，是 LangChain 生态系统的一部分，扩展了基础 LangChain 的能力以支持更复杂的智能体行为。

## 核心能力

- 状态管理
- 循环执行
- **条件分支和路由**：特别适合复杂路由场景，决策可以依赖整个系统的累积状态
- 图结构执行

## 相关链接

- 概念页面：[[concepts/langgraph|LangGraph - 概念页面]]
- LangChain `create_agent` API 底层使用 LangGraph 作为图运行时

## 参考文献

- [[sources/agentic-design-patterns-chapter-1-prompt-chaining|Agentic Design Patterns - Chapter 1 - Prompt Chaining]]
- [[sources/agentic-design-patterns-chapter-2-routing|Agentic Design Patterns - Chapter 2 - Routing]]
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
