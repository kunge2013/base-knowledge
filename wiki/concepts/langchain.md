---
title: LangChain
date: 2026-04-09
last_updated: 2026-04-09
tags: [framework, llm, python]
sources: [["wiki/sources/agentic-design-patterns-chapter-1-prompt-chaining", "Agentic Design Patterns - Chapter 1 - Prompt Chaining"]]
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

## 相关概念

- [[concepts/prompt-chaining|提示词链]]
- [[concepts/pipeline-pattern|管道模式]]
- [[concepts/agentic-design-patterns|智能体设计模式]]

## 参考文献

- [[sources/agentic-design-patterns-chapter-1-prompt-chaining|Agentic Design Patterns - Chapter 1 - Prompt Chaining]]
- https://python.langchain.com/
