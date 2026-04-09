---
title: Google ADK - 智能体开发工具包
date: 2026-04-09
last_updated: 2026-04-09
tags: [framework, google, agentic-design]
sources: [["wiki/sources/agentic-design-patterns-chapter-2-routing", "Agentic Design Patterns - Chapter 2 - Routing"]]
---

# Google ADK（智能体开发工具包）

**Google Agent Development Kit (ADK)** 是 Google 提供的用于构建 AI 智能体系统的开发框架。

## 概述

ADK 为定义智能体能力和行为提供了结构化开发环境。与基于显式计算图的架构相比，ADK 范式中的路由通常通过定义一组离散的"工具"来实现，这些工具代表智能体的功能。响应用户查询选择适当工具由框架的内部逻辑管理，该逻辑利用底层模型将用户意图与正确的功能处理程序匹配。

## 路由实现方式

在 ADK 中实现路由：
1. 开发者定义一组子智能体，每个子智能体专门处理特定类型的任务
2. 父协调器智能体定义委托指令
3. ADK 的自动流机制自动处理意图识别和委托路由
4. 框架根据用户意图将请求路由到正确的子智能体

这种方式对于具有明确定义离散操作集的智能体来说更加简洁。

## 示例架构

```python
# 定义专门子智能体
booking_agent = Agent(
    name="Booker",
    description="处理所有航班和酒店预订请求",
    tools=[booking_tool]
)

info_agent = Agent(
    name="Info",
    description="回答一般信息问题",
    tools=[info_tool]
)

# 协调器智能体自动路由
coordinator = Agent(
    name="Coordinator",
    instruction="分析请求并委托给适当专家智能体...",
    sub_agents=[booking_agent, info_agent]
)
# ADK 自动处理路由委托
```

## 与 LangGraph 的对比

| 维度 | Google ADK | LangGraph |
|------|-----------|-----------|
| 架构 | 基于能力，框架自动路由 | 基于显式状态图，开发者定义转换 |
| 复杂度 | 适合明确定义的离散操作集合，更简单 | 适合复杂路由，决策依赖累积状态 |
| 路由方式 | 框架内部处理，基于 LLM 意图匹配 | 开发者显式定义，完全控制 |

## 相关概念

- [[concepts/routing|路由]] - ADK 提供内置路由支持
- [[concepts/agentic-design-patterns|智能体设计模式]]
- [[entities/google|Google]] - ADK 由 Google 开发

## 参考文献

- [[sources/agentic-design-patterns-chapter-2-routing|Agentic Design Patterns - Chapter 2 - Routing]]
- https://google.github.io/adk-docs/
