---
title: Pipeline Pattern - 管道模式
date: 2026-04-09
last_updated: 2026-04-09
tags: [design-pattern, agentic-pattern]
sources: [["wiki/sources/agentic-design-patterns-chapter-1-prompt-chaining", "Agentic Design Patterns - Chapter 1 - Prompt Chaining"]]
---

# Pipeline Pattern（管道模式）

**管道模式**是提示词链模式的另一个名称。它描述了将数据通过一系列处理步骤（"管道"）顺序传递的设计模式，每一步都对数据进行特定变换，然后传递给下一步。

## 别名

- **提示词链（Prompt Chaining）**：在 AI 智能体领域最常用的名称
- **流水线模式**：传统计算机科学中的常用译名

## 核心思想

将复杂处理分解为一系列顺序的处理阶段，每个阶段专注于一项特定任务，数据从一个阶段流向下一个阶段，类似于工厂中的装配线或输水管道。

## 在智能体系统中的应用

在 AI 智能体系统中，每个处理阶段通常是：
- 一个由 LLM 执行的提示词调用
- 或一个确定性的数据处理步骤
- 或一个外部工具调用

每个阶段的输出作为输入传递给下一个阶段，形成依赖链。

## 优势

1. **模块化**：每个阶段可以独立开发、测试和优化
2. **可理解性**：整个处理流程清晰透明
3. **可调试性**：可以在每个阶段检查输出，定位问题
4. **可复用性**：通用阶段可以在不同工作流中复用
5. **可扩展性**：可以在不修改其他阶段的情况下插入新步骤

## 与提示词链的关系

在智能体设计模式语境中，**管道模式 = 提示词链**。"管道模式"强调的是数据流动的结构性视图，而"提示词链"强调的是 LLM 提示词的顺序执行。

## 相关概念

- [[concepts/prompt-chaining|Prompt Chaining - 提示词链]]
- [[concepts/agentic-design-patterns|Agentic Design Patterns - 智能体设计模式]]

## 参考文献

- [[sources/agentic-design-patterns-chapter-1-prompt-chaining|Agentic Design Patterns - Chapter 1 - Prompt Chaining]]
