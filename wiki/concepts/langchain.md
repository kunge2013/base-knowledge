---
title: LangChain
date: 2026-04-09
last_updated: 2026-04-14
tags: [framework, llm, python]
sources: [["wiki/sources/agentic-design-patterns-chapter-1-prompt-chaining", "Agentic Design Patterns - Chapter 1 - Prompt Chaining"], ["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# LangChain

**LangChain**是一个用于构建基于大语言模型应用的开源框架，它提供了核心抽象和工具来编排 LLM 工作流。

## 核心特性

- **LCEL（LangChain Expression Language）**：一种表达式语言，用于优雅地组合不同组件，构建复杂的处理链
- **丰富的组件集成**：支持多种 LLM 提供商、向量数据库、工具等
- **内置链和代理**：提供常用工作流的现成实现

## 在提示词链中的应用

LangChain 原生支持线性提示词链的构建。例如，使用 LCEL 可以非常简洁地定义两步处理链：

```python
extraction_chain = prompt_extract | llm | StrOutputParser()
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform
    | llm
    | StrOutputParser()
)
```

管道（|）语法清晰表达了数据流动方向。

## 相关项目

- **[[concepts/langgraph|LangGraph]]**：由 LangChain 团队开发，扩展支持状态化和循环计算，适合实现更复杂的智能体行为
- **LangChain Agents**: `create_agent` API 提供生产就绪的 Agent 运行时，基于 LangGraph 构建

## Agent 特性

LangChain `create_agent` 提供完整的 Agent 运行时支持：

- **模型选择**: 支持[[static-model-selection|静态模型选择]]和[[dynamic-model-selection|动态模型选择]]
- **工具管理**: 支持[[static-tools|静态工具]]和[[dynamic-tools|动态工具]]（基于状态/权限过滤）
- **错误处理**: 可自定义工具执行错误处理
- **结构化输出**: 支持两种策略[[providerstrategy|ProviderStrategy]]和[[toolstrategy|ToolStrategy]]
- **记忆和状态**: 支持[[agent-memory|Agent Memory]]和[[custom-agent-state|Custom Agent State]]
- **可扩展性**: 通过[[agent-middleware|Agent Middleware]]在各个执行阶段插入自定义逻辑
- **ReAct 执行**: 默认遵循[[react-pattern|ReAct]]模式迭代执行

## 相关概念

- [[concepts/prompt-chaining|提示词链]]
- [[concepts/pipeline-pattern|管道模式]]
- [[concepts/agentic-design-patterns|智能体设计模式]]
- [[concepts/ai-agents|AI Agents - AI 智能体]]

## 参考文献

- [[sources/agentic-design-patterns-chapter-1-prompt-chaining|Agentic Design Patterns - Chapter 1 - Prompt Chaining]]
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
- https://python.langchain.com/
