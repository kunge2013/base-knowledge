---
title: ReAct Pattern
date: 2026-04-14
last_updated: 2026-04-14
tags: [ai-agents, pattern, reasoning, acting]
sources: [["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# ReAct Pattern

ReAct（**Re**asoning + **Act**ing）是 AI Agent 最核心的执行模式，它让智能体在推理（Reasoning）和行动（Acting）之间交替迭代，逐步解决问题。

## 工作流程

1. **Reasoning（推理）**: Agent 分析当前状态，决定下一步该做什么
2. **Acting（行动）**: Agent 调用工具获取信息或执行操作
3. **Observation（观察）**: 获取工具执行结果
4. **Repeat（重复）**: 继续下一轮推理，直到问题解决

## 示例对话流程

**用户提示**: 找出当前最受欢迎的无线耳机并确认是否有货。

```
================================ Human Message =================================
Find the most popular wireless headphones right now and check if they're in stock
```

- **推理**: "流行度是时间敏感的，我需要使用搜索工具。"
- **行动**: 调用 `search_products("wireless headphones")`

```
================================== Ai Message ==================================
Tool Calls:
  search_products (call_abc123)
 Call ID: call_abc123
  Args:
    query: wireless headphones
```

```
================================= Tool Message =================================
Found 5 products matching "wireless headphones". Top 5 results: WH-1000XM5, ...
```

- **推理**: "我需要在回答前确认排名第一商品的库存。"
- **行动**: 调用 `check_inventory("WH-1000XM5")`

```
================================== Ai Message ==================================
Tool Calls:
  check_inventory (call_def456)
 Call ID: call_def456
  Args:
    product_id: WH-1000XM5
```

```
================================= Tool Message =================================
Product WH-1000XM5: 10 units in stock
```

- **推理**: "我已经获得了最受欢迎型号和库存状态，可以给出最终答案了。"
- **行动**: 输出最终答案

## 为什么 ReAct 有效

- 将复杂问题分解为可管理的步骤
- 每一步都可以从工具获取真实信息
- 允许模型在获取新信息后修正推理方向
- 相比于一次性生成所有步骤更可靠

## 在 LangChain 中的支持

LangGraph 原生实现了 ReAct 循环，`create_agent` API 默认使用 ReAct 执行模式。

## 相关链接

- [[concepts/ai-agents|AI Agents - AI 智能体]]
- [[concepts/langchain|LangChain]]
- [[concepts/langgraph|LangGraph]]
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
