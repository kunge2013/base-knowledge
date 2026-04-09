---
title: Context Engineering - 上下文工程
date: 2026-04-09
last_updated: 2026-04-09
tags: [methodology, prompt-engineering, agentic-design]
sources: [["wiki/sources/agentic-design-patterns-chapter-1-prompt-chaining", "Agentic Design Patterns - Chapter 1 - Prompt Chaining"]]
---

# Context Engineering（上下文工程）

**上下文工程**是系统地设计、构建和向 AI 模型提供完整信息环境的方法论。它代表了从传统提示工程的重大演进。

## 核心命题

上下文工程断言：**模型输出的质量较少依赖于模型架构本身，而更多依赖于所提供上下文的丰富性和质量。**

即使是最先进的模型，在提供有限或构建不良的操作环境视图时也会表现不佳。相反，如果为模型提供全面、结构化的上下文，即使能力一般的模型也能产生高质量输出。

## 演进：从提示工程到上下文工程

| 传统提示工程 | 上下文工程 |
|-------------|-----------|
| 专注于优化单个查询的措辞 | 范围扩展到构建完整信息环境 |
| 单次交互 | 系统化构建多步骤工作流 |
| 以查询为中心 | 以智能体状态和环境为中心 |

## 上下文的组成

上下文工程整合多层信息：

### 1. 系统提示词 (System Prompt)
定义 AI 操作参数的基础指令集，例如：
> "你是一名技术作家；你的语气必须正式且精确。"

### 2. 检索文档 (Retrieved Documents)
AI 主动从知识库获取信息以指导响应。

### 3. 工具输出 (Tool Outputs)
AI 使用外部 API 获取实时数据的结果，例如查询日历、数据库、外部服务。

### 4. 隐式数据 (Implicit Data)
- 用户身份
- 交互历史
- 环境状态
- 对话上下文

## 核心思想

上下文工程将任务从"仅仅回答问题"重新定义为"为智能体系统构建全面的操作图景"。

**示例**：上下文工程化的智能体不会仅仅响应邮件撰写查询，而是会首先整合：
- 用户的日历可用性（工具输出）
- 与收件人的专业关系（隐式数据）
- 之前会议的笔记（检索文档）

然后才能生成高度相关、个性化和实用的输出。

## 关键实践

- **反馈循环**：建立持续改进上下文质量的反馈机制
- **自动化调优**：使用专门的调优系统大规模自动化改进过程，例如 Google Vertex AI 提示优化器
- **结构化方法**：将上下文本身视为主要组件，而不是理所当然的背景信息
- **情境感知**：确保模型对用户意图、历史和当前环境有全面理解

## 目标

通过系统化的上下文工程，将无状态的聊天机器人提升为**高度能干、情境感知的智能体系统**。

## 相关工具

- **Google Vertex AI Prompt Optimizer**：可编程式地完善上下文输入，提供结构化方法实现反馈循环

## 相关概念

- [[concepts/prompt-engineering|提示词工程]]
- [[concepts/prompt-chaining|提示词链]]
- [[concepts/agentic-design-patterns|智能体设计模式]]
- [[concepts/context-aware-agents|情境感知智能体]]

## 参考文献

- [[sources/agentic-design-patterns-chapter-1-prompt-chaining|Agentic Design Patterns - Chapter 1 - Prompt Chaining]]
