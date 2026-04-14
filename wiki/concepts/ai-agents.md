---
title: AI Agents - AI 智能体
date: 2026-04-09
last_updated: 2026-04-14
tags: [concept, ai, agentic-design]
sources: [["wiki/sources/agentic-design-patterns-chapter-1-prompt-chaining", "Agentic Design Patterns - Chapter 1 - Prompt Chaining"], ["wiki/sources/agentic-design-patterns-chapter-2-routing", "Agentic Design Patterns - Chapter 2 - Routing"], ["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# AI Agents（AI 智能体）

**AI 智能体**是能够感知环境、进行推理决策并自主执行行动以实现目标的人工智能系统。在大语言模型语境中，AI 智能体是指基于 LLM 构建的能够自主完成多步任务的系统。

## 核心特征

- **感知**：接收并理解用户输入和环境状态
- **推理**：基于当前状态和目标进行推理
- **决策**：选择下一步行动（调用工具、路由到子智能体等）
- **行动**：执行决策，产生输出
- **自主性**：能够在没有人干预的情况下完成多步任务

## 基础设计模式

### 顺序模式
- **[[concepts/prompt-chaining|提示词链]]** - 将复杂任务分解为顺序执行的步骤链

### 控制流模式
- **[[concepts/routing|路由]]** - 根据条件动态选择执行路径
- **[[concepts/conditional-logic|条件逻辑]]** - 基于条件选择不同分支

## 架构模式

- **[[concepts/multi-agent-systems|多智能体系统]]** - 多个专门智能体协作完成任务
- 协调器-专家架构：中央协调器路由任务给专家智能体

## 关键能力

智能体系统通过组合基础设计模式获得更高级的能力：
- **多步推理**：通过提示词链逐步推理
- **工具使用**：路由模式选择正确工具调用
- **状态维护**：在多轮交互中保持上下文
- **自适应行为**：根据输入动态改变执行路径

## 框架支持

- [[concepts/langchain|LangChain]] - 基础链和组件
- [[concepts/langgraph|LangGraph]] - 基于图的有状态智能体
- [[concepts/google-adk|Google ADK]] - Google 智能体开发工具包
- [[concepts/crew-ai|Crew AI]] - 多智能体协作框架

## 相关概念

- [[concepts/agentic-design-patterns|智能体设计模式]] - 可复用的智能体设计模式集合
- [[concepts/prompt-chaining|提示词链]]
- [[concepts/routing|路由]]

## 执行模式

### ReAct 模式

**ReAct**（Reasoning + Acting）是最常见的迭代执行模式：Agent 在推理（Reasoning）和行动（Acting）之间交替，逐步解决问题。

1. 推理：分析当前状态，决定下一步做什么
2. 行动：调用工具获取信息
3. 观察：获取工具执行结果
4. 重复：继续直到问题解决

ReAct 模式让 LLM 能够在获取新信息后修正推理方向，比一次性解决更可靠。

## 核心组件

在 LangChain 实现中，Agent 通常包含：

- **Model** - 推理引擎，支持静态和动态选择
- **Tools** - 可调用的外部工具，支持静态和动态管理
- **System Prompt** - 定义 Agent 的行为方式
- **Memory/State** - 维护对话状态和记忆

## 参考文献

- [[sources/agentic-design-patterns-chapter-1-prompt-chaining|Agentic Design Patterns - Chapter 1 - Prompt Chaining]]
- [[sources/agentic-design-patterns-chapter-2-routing|Agentic Design Patterns - Chapter 2 - Routing]]
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
