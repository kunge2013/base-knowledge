---
title: Agent Middleware
date: 2026-04-14
last_updated: 2026-04-14
tags: [ai-agents, langchain, extensibility]
sources: [["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# Agent Middleware

Agent Middleware（Agent 中间件）是 LangChain 中用于自定义 Agent 行为的扩展机制，允许在执行的不同阶段拦截和修改数据流。

## 能力

Middleware 可以用来：

- 在模型调用前处理状态（消息修剪、上下文注入）
- 修改或验证模型响应（护栏、内容过滤）
- 用自定义逻辑处理工具执行错误
- 基于状态实现动态模型选择
- 添加自定义日志、监控或分析
- 动态过滤工具列表
- 动态生成系统提示词

## 装饰器

LangChain 提供几个方便的装饰器用于创建中间件：

- `@before_model` - 在模型调用前执行
- `@after_model` - 在模型调用后执行
- `@wrap_model_call` - 包装整个模型调用（可修改输入和输出）
- `@wrap_tool_call` - 包装工具调用
- `@dynamic_prompt` - 动态生成系统提示

## 使用示例

### 动态模型选择

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    # 根据对话复杂度选择不同模型
    message_count = len(request.state["messages"])
    model = advanced_model if message_count > 10 else basic_model
    return handler(request.override(model=model))
```

### 动态工具过滤

```python
@wrap_model_call
def state_based_tools(request: ModelRequest, handler) -> ModelResponse:
    # 根据用户认证状态过滤可用工具
    is_authenticated = request.state.get("authenticated", False)
    if not is_authenticated:
        tools = [t for t in request.tools if t.name.startswith("public_")]
        request = request.override(tools=tools)
    return handler(request)
```

### 自定义工具错误处理

```python
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage

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

### 动态系统提示

```python
from langchain.agents.middleware import dynamic_prompt, ModelRequest

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on user role."""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "You are a helpful assistant."

    if user_role == "expert":
        return f"{base_prompt} Provide detailed technical responses."
    elif user_role == "beginner":
        return f"{base_prompt} Explain concepts simply and avoid jargon."

    return base_prompt
```

## 架构特点

- 无缝集成到 Agent 执行流程
- 无需修改核心 Agent 逻辑
- 可以组合多个中间件
- 每个中间件关注一个横切关注点

## 相关链接

- [[concepts/dynamic-model-selection|Dynamic Model Selection]] - 应用示例
- [[concepts/dynamic-tools|Dynamic Tools]] - 应用示例
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
- [[concepts/langchain|LangChain]]
