---
title: LangChain - 1. Agents
date: 2026-04-14
last_updated: 2026-04-14
tags: [langchain, ai-agents, documentation]
sources: [["raw/articles/llm/langchain/1.Agents.md", "LangChain Agents 官方文档"]]
---

# LangChain - 1. Agents

这是 LangChain 官方文档关于 Agents 的完整说明，介绍了如何使用 `create_agent` API 构建生产就绪的 AI Agent。

## 概述

Agents 将语言模型与工具结合，创建能够推理任务、决定使用哪些工具并迭代求解的系统。`create_agent` 基于 LangGraph 构建基于图的 Agent 运行时。

Agent 运行直至满足停止条件——当模型发出最终输出或达到迭代限制时停止。

## 核心组件

### 1. Model

Agent 的推理引擎，支持两种模式：

**静态模型** - 创建时配置，执行过程中保持不变（最常用）：
```python
from langchain.agents import create_agent
agent = create_agent("openai:gpt-5", tools=tools)
# 或直接传递模型实例
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-5", temperature=0.1, max_tokens=1000)
agent = create_agent(model, tools=tools)
```

**动态模型** - 根据上下文在运行时选择，支持复杂路由和成本优化：
- 使用 `@wrap_model_call` 装饰器创建中间件
- 根据对话复杂度或状态选择不同模型

### 2. Tools

为 Agent 提供行动能力，支持：

- 顺序多工具调用
- 并行工具调用
- 动态工具选择
- 工具重试和错误处理
- 跨工具调用的状态持久化

**静态工具** - 创建时定义：
```python
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(model, tools=[search, get_weather])
```

**动态工具** - 根据状态在运行时过滤：
- 基于权限、认证状态、对话阶段过滤可用工具
- 避免上下文过载，减少模型错误

**工具错误处理** - 使用 `@wrap_tool_call` 自定义错误处理：
```python
@wrap_tool_call
def handle_tool_errors(request, handler):
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )
```

**ReAct 循环**：Agent 遵循 ReAct（Reasoning + Acting）模式，在推理步骤和工具调用之间交替，直到获得最终答案。

### 3. System Prompt

塑造 Agent 的任务处理方式：

- 支持静态字符串或 `SystemMessage`
- 支持动态提示，基于运行时上下文生成
- 支持 Anthropic 提示缓存优化降低延迟和成本

### 4. Name

可选的 Agent 名称，用作子图的节点标识符（在多智能体系统中使用）。建议使用 `snake_case` 格式。

## 调用方式

通过向 Agent 的状态传递新消息来调用：

```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
```

支持 `stream` 模式进行流式输出。

## 高级概念

### 结构化输出

两种策略获取特定格式输出：

- **`ProviderStrategy`** - 使用模型原生结构化输出生成能力（更可靠，仅支持部分提供商）
- **`ToolStrategy`** - 使用人工工具调用生成结构化输出（适用于任何支持工具调用的模型）

LangChain 0.1+ 默认在支持时使用 `ProviderStrategy`，否则回退到 `ToolStrategy`。

### Memory

- Agent 通过消息状态自动维护对话历史
- 可配置自定义状态模式来记住额外信息
- 通过扩展 `AgentState` 作为 `TypedDict` 定义自定义状态
- 支持短期记忆（对话内）和长期记忆（跨会话）

### Streaming

支持流式输出，在多步骤执行中显示中间进度。

### Middleware

提供强大的可扩展性，可在执行的不同阶段拦截和修改数据流：

- 模型调用前处理状态（消息修剪、上下文注入）
- 修改或验证模型响应（护栏、内容过滤）
- 自定义工具错误处理逻辑
- 基于状态实现动态模型选择
- 添加自定义日志、监控或分析

## 相关链接

- [[concepts/langchain|LangChain]]  - LangChain 框架概念
- [[concepts/langgraph|LangGraph]]  - LangGraph 图执行框架
- [[concepts/ai-agents|AI Agents - AI 智能体]]  - AI 智能体概念
- [[concepts/react-pattern|ReAct Pattern]]  - ReAct 推理模式
