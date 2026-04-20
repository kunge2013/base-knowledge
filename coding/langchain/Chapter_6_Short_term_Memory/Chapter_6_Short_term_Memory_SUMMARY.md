# 短期记忆

## 概述

短期记忆（Short-term Memory）用于在单个对话线程（thread）内记住之前的交互。在 LangGraph 中，短期记忆通过 `checkpointer` 持久化代理状态，使得对话可以在任意时候恢复，并分隔不同的对话线程。

## 什么是短期记忆

- **线程（Thread）**：组织一个会话/对话内的多次交互，类似于邮件线程把一个对话的消息分组在一起
- **上下文窗口问题**：长对话会超出 LLM 的上下文窗口，需要使用各种技术来删除或“忘记”过期信息
- **持久化**：通过 checkpointer 将状态存储在数据库中，重启应用后仍可恢复对话

## 基本用法

### 核心流程

```mermaid
graph TD
    A[创建代理] --> B[指定 checkpointer]
    B --> C[invoke 第一次 - 用户打招呼]
    C --> D[checkpointer 保存状态]
    D --> E[invoke 第二次 - 问之前的内容]
    E --> F[checkpointer 加载状态]
    F --> G[代理记住上下文回答]
```

### 基本代码示例

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from llm_config import get_llm
from langchain.tools import tool

@tool
def get_user_info(user_id: str) -> str:
    """Get user information by user ID."""
    return f"User {user_id}: John Smith"

# 创建 checkpointer 存在内存中（开发测试用）
checkpointer = InMemorySaver()

# 创建代理时传入 checkpointer
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[get_user_info],
    checkpointer=checkpointer,
)

# 第一次调用 - 自我介绍
config = {"configurable": {"thread_id": "conversation_1"}}
result = agent.invoke(
    {"messages": [HumanMessage(content="Hi! My name is Bob.")]},
    config,
)

# 第二次调用 - 代理已经记住你的名字
result2 = agent.invoke(
    {"messages": [HumanMessage(content="What's my name?")]},
    config,
)
# 输出: Your name is Bob!
```

**生产环境使用 Postgres**:

```python
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()  # 自动创建表
    agent = create_agent(
        get_llm("gpt-4.1"),
        tools=[get_user_info],
        checkpointer=checkpointer,
    )
    # 使用方式和 InMemory 完全一样
```

## 自定义状态

你可以扩展 `AgentState` 添加自定义字段来存储额外信息：

```python
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver

# 扩展基础 AgentState 添加自定义字段
class CustomAgentState(AgentState):
    user_id: str      # 存储用户 ID 在短期记忆
    preferences: dict # 存储用户偏好设置

checkpointer = InMemorySaver()
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[get_user_preferences],
    state_schema=CustomAgentState,  # 传入自定义 schema
    checkpointer=checkpointer,
)

# 调用时传入自定义状态初始值
result = agent.invoke(
    {
        "messages": [HumanMessage(content="Hello")],
        "user_id": "user_123",
        "preferences": {"theme": "dark"},
    },
    {"configurable": {"thread_id": "1"}},
)
```

## 上下文窗口管理策略

长对话会超出 LLM 上下文窗口，有三种常见策略：

### 1. 裁剪消息（Trim Messages）

使用 `@before_model` 中间件在每次 LLM 调用前裁剪消息，保留最近 N 条。

```mermaid
graph TD
    A[用户发送新消息] --> B[@before_model 触发]
    B --> C{消息数 > 阈值?}
    C -->|否| D[直接调用 LLM]
    C -->|是| E[保留第一条 + 最近几条]
    E --> F[删除旧消息]
    F --> G[调用 LLM]
```

**代码示例**:

```python
from typing import Any
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langgraph.checkpoint.memory import InMemorySaver

@before_model
def trim_messages(state: AgentState, runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window."""
    messages = state["messages"]

    if len(messages) <= 3:
        return None  # 不需要修改

    # 策略: 保留第一条 + 最近 3-4 条（保持对话轮次模式）
    first_msg = messages[0]
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages

    return {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            *new_messages
        ]
    }

checkpointer = InMemorySaver()
agent = create_agent(
    get_llm("gpt-4.1"),
    tools=[],
    middleware=[trim_messages],
    checkpointer=checkpointer,
)
```

**使用场景**

- 快速对话，不介意丢失旧信息
- 简单实现，不需要额外 LLM 调用
- 对话轮次不长，只是需要防止偶尔溢出

### 2. 删除消息（Delete Messages）

使用 `@after_model` 中间件在 LLM 响应后删除最早几条消息，渐进式控制增长。

```mermaid
graph TD
    A[LLM 返回响应] --> B[@after_model 触发]
    B --> C{总长度 > 阈值?}
    C -->|否| D[结束]
    C -->|是| E[删除最早 2 条]
    E --> F[更新状态]
```

**代码示例**:

```python
from langchain.messages import RemoveMessage
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langgraph.checkpoint.memory import InMemorySaver

@after_model
def delete_old_messages(state: AgentState, runtime) -> dict | None:
    """Remove oldest messages to keep conversation manageable."""
    messages = state["messages"]
    if len(messages) > 2:
        # 删除最早两条消息
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}
    return None

checkpointer = InMemorySaver()
agent = create_agent(
    get_llm("gpt-4.1"),
    tools=[],
    middleware=[delete_old_messages],
    checkpointer=checkpointer,
)
```

**使用场景**

- 渐进式对话增长
- 需要严格控制消息数量
- 删除不相关的旧消息

### 3. 摘要消息（Summarize Messages）

当达到 token 阈值时，自动摘要旧消息。使用 `SummarizationMiddleware` 内置实现。

```mermaid
graph TD
    A[添加新消息] --> B{token数 > 阈值?}
    B -->|否| C[直接调用 LLM]
    B -->|是| D[摘要旧消息]
    D --> E[保留最后 N 条不变]
    E --> F[替换旧消息为摘要]
    F --> G[调用 LLM]
```

**代码示例**:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[],
    middleware=[
        SummarizationMiddleware(
            model=get_llm("gpt-4.1-mini"),  # 使用较小模型摘要省钱
            trigger=("tokens", 4000),       # 超过 4000 token 触发
            keep=("messages", 20),           # 保留最后 20 条不变
        )
    ],
    checkpointer=checkpointer,
)
```

**使用场景**

- 长对话需要保留信息
- 愿意付出额外 token 成本换取信息保留
- 比直接裁剪/删除保留更多上下文

**三种策略对比**

| 策略 | 信息保留 | 额外成本 | 复杂度 | 适用场景 |
|------|----------|----------|--------|----------|
| 裁剪 | 差 | 无 | 低 | 短对话、简单交互 |
| 删除 | 较差 | 无 | 低 | 渐进式对话 |
| 摘要 | 好 | 额外 LLM 调用 | 中 | 长对话需要保留信息 |

## 访问短期记忆的方式

### 1. 工具中访问

工具可以通过 `runtime` 参数读取和修改短期记忆：

```python
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage
from langchain.agents import create_agent, AgentState

# 自定义状态
class CustomState(AgentState):
    user_name: str | None

# 自定义上下文
class CustomContext(BaseModel):
    user_id: str

@tool
def update_user_info(
    runtime: ToolRuntime[CustomContext, CustomState],
) -> Command:
    """Look up and update user info in short-term memory."""
    user_id = runtime.context.user_id  # 从 context 读取
    name = "John Smith" if user_id == "user_123" else "Unknown"
    # 返回 Command 更新状态
    return Command(update={
        "user_name": name,
        "messages": [
            ToolMessage(
                f"Found user: {name}",
                tool_call_id=runtime.tool_call_id
            )
        ]
    })

@tool
def greet(
    runtime: ToolRuntime[CustomContext, CustomState]
) -> str | Command:
    """Greet the user after getting name."""
    user_name = runtime.state.get("user_name")  # 从状态读取
    if user_name is None:
        return Command(...)  # 需要先查找
    return f"Hello {user_name}!"

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[update_user_info, greet],
    state_schema=CustomState,
    context_schema=CustomContext,
)
```

**关键点**

- `runtime`: 自动注入，对 LLM 隐藏
- `runtime.context`: 只读的配置上下文
- `runtime.state`: 读取当前状态
- 返回 `Command(update=...)`: 修改状态

### 2. 动态 Prompt 中间件

使用 `@dynamic_prompt` 根据内存生成动态系统提示：

```python
from typing import TypedDict
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.tools import tool

class CustomContext(TypedDict):
    user_name: str

@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is 68°F"

@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    user_name = request.runtime.context["user_name"]
    messages = request.state["messages"]
    # 根据内存生成个性化 prompt
    return f"""You are a helpful assistant.
Current user is: {user_name}
Address the user by name.
This is turn #{len(messages)} in this conversation.
"""

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[get_weather],
    middleware=[dynamic_system_prompt],
    context_schema=CustomContext,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in SF?"}]},
    context=CustomContext(user_name="John Smith"),
)
```

**使用场景**

- 个性化提示（用用户名）
- 根据当前会话状态调整指令
- 基于用户偏好动态调整行为

### 3. before_model 中间件

在 LLM 调用前处理状态（裁剪就是这种方式）：

```python
from langchain.agents.middleware import before_model

@before_model
def your_middleware(state: AgentState, runtime):
    # 在 LLM 调用前修改状态
    # 可以做裁剪、过滤、预处理等
    return modified_state_dict  # 返回 None 不修改
```

### 4. after_model 中间件

在 LLM 调用后处理响应（删除消息、验证就是这种方式）：

```python
from langchain.agents.middleware import after_model

@after_model
def validate_response(state: AgentState, runtime):
    # 在 LLM 响应后处理
    # 可以做验证、过滤、后处理
    last_message = state["messages"][-1]
    # 检查敏感词，删除违规内容
    STOP_WORDS = ["password", "secret"]
    if any(word in last_message.content for word in STOP_WORDS):
        return {"messages": [RemoveMessage(id=last_message.id)]}
    return None
```

## 不同访问方式对比

| 方式 | 时机 | 用途 | 例子 |
|------|------|------|------|
| `runtime` in tools | 工具执行 | 工具读写状态 | 查找用户信息存入状态 |
| `@dynamic_prompt` | 生成 prompt | 根据状态动态生成系统提示 | 个性化提示 |
| `@before_model` | LLM 调用前 | 预处理状态 | 裁剪消息 |
| `@after_model` | LLM 调用后 | 后处理响应 | 内容验证、过滤敏感词 |

## 生产环境选择

### Checkpointer 选择

| Checkpointer | 用途 | 持久化 |
|--------------|------|----------|
| `InMemorySaver` | 开发测试 | 否（重启丢失） |
| `PostgresSaver` | 生产环境 | 是 |
| `SqliteSaver` | 小型部署 | 是（文件） |
| `AzureCosmosDBSaver` | Azure 云 | 是 |

### 推荐依赖安装

```bash
# 基础
pip install langgraph langchain langchain-openai

# Postgres 生产
pip install langgraph-checkpoint-postgres psycopg2-binary

# SQLite
pip install langgraph-checkpoint-sqlite
```

## 完整文件列表

| 文件 | 主题 |
|------|------|
| [llm_config.py](coding/langchain/Chapter_6_Short_term_Memory/llm_config.py) | LLM 配置 |
| [01-basic-in-memory.py](01-basic-in-memory.py) | 基础内存示例 |
| [02-production-postgres.py](02-production-postgres.py) | Postgres 生产配置 |
| [03-custom-state.py](03-custom-state.py) | 自定义状态 |
| [04-trim-messages.py](04-trim-messages.py) | 裁剪消息 |
| [05-delete-messages.py](05-delete-messages.py) | 删除旧消息 |
| [06-summarize-messages.py](06-summarize-messages.py) | 摘要中间件 |
| [07-tool-access-memory.py](07-tool-access-memory.py) | 工具访问内存 |
| [08-dynamic-prompt-memory.py](08-dynamic-prompt-memory.py) | 动态 prompt |
| [09-after-model-validation.py](09-after-model-validation.py) | 响应验证 |
