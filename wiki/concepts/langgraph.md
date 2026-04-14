---
title: LangGraph
date: 2026-04-09
last_updated: 2026-04-14
tags: [framework, llm, agentic-design]
sources: [["wiki/sources/agentic-design-patterns-chapter-1-prompt-chaining", "Agentic Design Patterns - Chapter 1 - Prompt Chaining"], ["wiki/sources/agentic-design-patterns-chapter-2-routing", "Agentic Design Patterns - Chapter 2 - Routing"], ["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# LangGraph

**LangGraph**是由 LangChain 团队开发的框架，扩展了 LangChain 的能力，支持状态化和循环计算，是构建复杂智能体行为的工具。

## 与 LangChain 的关系

- **LangChain**：为线性顺序处理链提供基础抽象，适合简单的提示词链
- **LangGraph**：扩展支持状态管理、循环和条件分支，适合实现更复杂的智能体行为

LangGraph 建立在 LangChain 之上，增加了图状结构执行的能力。

## 核心能力

- **状态管理**：在整个工作流过程中维护状态
- **循环执行**：支持需要迭代修正的任务
- **条件分支**：根据中间结果选择不同执行路径，特别适合复杂路由场景
- **图结构**：将工作流表示为节点和边组成的图

## 使用场景

- 需要循环和条件判断的智能体工作流
- **复杂路由**：决策依赖整个系统累积状态的场景
- 有状态对话系统
- 多步规划和推理
- 复杂智能体架构

## 相关概念

- [[concepts/langchain|LangChain]]
- [[concepts/prompt-chaining|提示词链]]
- [[concepts/routing|路由]]
- [[concepts/agentic-design-patterns|智能体设计模式]]

## LangChain Agents 集成

LangChain `create_agent` API 底层就是使用 LangGraph 构建基于图的 Agent 运行时：

- 图由节点（步骤）和边（连接）组成
- 节点包括模型节点（调用 LLM）和工具节点（执行工具）
- Agent 在图中遍历执行，直到满足停止条件
- 支持流式输出和状态持久化

## 参考文献

- [[sources/agentic-design-patterns-chapter-1-prompt-chaining|Agentic Design Patterns - Chapter 1 - Prompt Chaining]]
- [[sources/agentic-design-patterns-chapter-2-routing|Agentic Design Patterns - Chapter 2 - Routing]]
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
- https://langchain-ai.github.io/langgraph/
