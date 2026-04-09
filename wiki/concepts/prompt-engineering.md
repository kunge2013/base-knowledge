---
title: Prompt Engineering - 提示词工程
date: 2026-04-09
last_updated: 2026-04-09
tags: [technique, llm]
sources: [["wiki/sources/agentic-design-patterns-chapter-1-prompt-chaining", "Agentic Design Patterns - Chapter 1 - Prompt Chaining"]]
---

# Prompt Engineering（提示词工程）

**提示词工程**是设计和优化输入提示词，以获得大语言模型更好输出的技术。

## 定义

提示词工程是一门艺术和科学，通过精心设计输入指令，引导大语言模型按照预期方式生成输出。它包括：措辞优化、格式设计、约束说明、示例提供等技术。

## 与上下文工程的关系

传统提示工程主要专注于优化**单个用户查询**的措辞。这与 [[concepts/context-engineering|上下文工程]] 形成对比：

- **提示词工程**：聚焦单次交互，优化单个提示词的措辞
- **上下文工程**：系统化构建完整信息环境，包含系统提示词、检索文档、工具输出、隐式上下文等多层信息

上下文工程可以看作是提示工程向更大范围的演进。

## 常见技术

- **提示词链（Prompt Chaining）**：将复杂任务分解为多个顺序执行的提示词
- **结构化输出**：指定 JSON/XML 格式确保输出格式正确
- **角色设定**：为 LLM 指定特定角色引导输出风格
- **少样本学习**：在提示词中提供示例帮助模型理解任务
- **思维链（Chain-of-Thought）**：引导模型逐步推理

## 相关概念

- [[concepts/prompt-chaining|提示词链]]
- [[concepts/context-engineering|上下文工程]]
- [[concepts/agentic-design-patterns|智能体设计模式]]

## 参考文献

- [[sources/agentic-design-patterns-chapter-1-prompt-chaining|Agentic Design Patterns - Chapter 1 - Prompt Chaining]]
