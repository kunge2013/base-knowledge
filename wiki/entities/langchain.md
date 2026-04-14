---
title: LangChain
date: 2026-04-09
last_updated: 2026-04-14
tags: [company, open-source, llm-framework]
sources: [["wiki/sources/agentic-design-patterns-chapter-1-prompt-chaining", "Agentic Design Patterns - Chapter 1 - Prompt Chaining"], ["wiki/sources/agentic-design-patterns-chapter-2-routing", "Agentic Design Patterns - Chapter 2 - Routing"], ["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# LangChain

LangChain 是一家构建大语言模型开发框架的公司，同时也是其开源框架的名称。

## 概述

LangChain 公司开发并维护着最流行的开源 LLM 应用开发框架 LangChain，以及相关项目如 LangGraph。

## 主要产品

- **LangChain**：核心框架，提供 LCEL 表达式语言用于构建 LLM 工作流，包含 `RunnableBranch` 支持条件路由
- **LangGraph**：用于构建有状态、循环智能体的扩展框架，特别适合复杂路由场景
- **LangServe**：将 LangChain 应用部署为 API 服务
- **`create_agent`**: 生产就绪的 Agent API，基于 LangGraph 构建，支持静态/动态模型选择、静态/动态工具、结构化输出、中间件扩展等

## 相关链接

- 框架页面：[[concepts/langchain|LangChain - 概念页面]]
- 相关框架：[[entities/langgraph|LangGraph]]

## 参考文献

- [[sources/agentic-design-patterns-chapter-1-prompt-chaining|Agentic Design Patterns - Chapter 1 - Prompt Chaining]]
- [[sources/agentic-design-patterns-chapter-2-routing|Agentic Design Patterns - Chapter 2 - Routing]]
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
