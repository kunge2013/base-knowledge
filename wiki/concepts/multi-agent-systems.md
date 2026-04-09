---
title: Multi-Agent Systems - 多智能体系统
date: 2026-04-09
last_updated: 2026-04-09
tags: [agentic-design, architecture, pattern]
sources: [["wiki/sources/agentic-design-patterns-chapter-2-routing", "Agentic Design Patterns - Chapter 2 - Routing"]]
---

# Multi-Agent Systems（多智能体系统）

**多智能体系统**是由多个相互作用的智能体组成的系统，每个智能体专门处理特定类型的任务，通过协作完成更复杂的目标。

## 在路由模式中的角色

在 [[concepts/routing|路由]] 模式中，多智能体系统通常采用**协调器-专家**架构：
1. **协调器智能体**：分析用户请求，进行意图分类，通过路由将任务委托给专门专家
2. **专家智能体/子智能体**：每个专门处理特定领域任务，只关注自己擅长的问题类型

这是一种常见的委托模式，路由是实现这种委托的核心机制。

## 优势

- **专业化**：每个智能体可以针对特定任务优化提示词、模型和工具
- **模块化**：可以独立开发和维护不同专家智能体
- **可扩展**：增加新的专长只需要增加新的专家智能体，不影响现有系统
- **清晰责任边界**：每个智能体只负责自己的领域

## 典型架构

```
用户请求
    ↓
协调器智能体 (路由决策)
    ↓
┌──────────┴──────────┐
↓                    ↓
专家智能体 A       专家智能体 B
(预订)             (信息查询)
```

## 实现方式

- **LangChain + RunnableBranch**：显式实现路由分支
- **Google ADK**：框架通过 `sub_agents` 自动支持委托路由
- **[[concepts/langgraph|LangGraph]]**：基于图定义复杂多智能体交互和路由

## 相关概念

- [[concepts/routing|路由]] - 路由是多智能体系统中实现任务委托的核心机制
- [[concepts/crew-ai|Crew AI]] - 多智能体协作框架
- [[concepts/agentic-design-patterns|智能体设计模式]]

## 参考文献

- [[sources/agentic-design-patterns-chapter-2-routing|Agentic Design Patterns - Chapter 2 - Routing]]
