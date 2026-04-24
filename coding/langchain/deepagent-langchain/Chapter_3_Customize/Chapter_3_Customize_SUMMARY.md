# 自定义 Deep Agents - 代码摘要

## 1. 模型配置范式

### 核心代码

```python
# 01_model_configuration.py

# 方式 1: provider:model 字符串格式
agent_openai = create_deep_agent(model="openai:gpt-5.4")
agent_gemini = create_deep_agent(model="google_genai:gemini-3.1-pro-preview")
agent_claude = create_deep_agent(model="anthropic:claude-sonnet-4-6")

# 方式 2: 模型实例初始化（精细控制）
from langchain.chat_models import init_chat_model

agent_with_config = create_deep_agent(
    model=init_chat_model(
        model="google_genai:gemini-3.1-pro-preview",
        max_retries=10,  # 增加重试次数（默认 6 次）
        timeout=120,     # 增加超时时间（秒）
    ),
)

# 方式 3: 具体提供商模型类
from langchain_openai import ChatOpenAI

openai_model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.1,
    max_tokens=1000,
    api_key=os.getenv("OPENAI_API_KEY"),
)

agent_openai_instance = create_deep_agent(model=openai_model)
```

### 使用的范式

- **provider:model 字符串格式**: 快速切换不同提供商的模型
- **模型实例初始化**: 精细控制模型参数（重试、超时等）
- **连接弹性配置**: 自动重试、指数退避、网络容错

### 使用场景

| 场景 | 推荐配置 | 说明 |
|------|----------|------|
| 快速原型开发 | provider:model 字符串 | 简洁，快速切换 |
| 生产环境 | 模型实例 + 弹性配置 | 可控性强，错误处理好 |
| 不可靠网络 | max_retries=10-15 | 增加重试次数 |
| 长时间任务 | checkpointer + 弹性配置 | 保存进度，防止丢失 |

---

## 2. 工具定义范式

### 核心代码

```python
# 02_custom_tools.py

# 方式 1: Python 函数（类型注解自动生成 schema）
from typing import Literal
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run an internet search using Tavily API."""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

# 方式 2: @tool 装饰器
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."

@tool
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate Body Mass Index (BMI)."""
    return weight_kg / (height_m ** 2)

# 方式 3: Pydantic Schema
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    """Input schema for search tool."""
    query: str = Field(description="The search query string")
    max_results: int = Field(default=5, description="Maximum number of results")
    topic: Literal["general", "news", "finance"] = Field(default="general")
```

### 使用的范式

- **类型注解驱动 Schema 生成**: 利用 Python 类型注解自动生成工具调用 schema
- **@tool 装饰器**: 简化工具定义，自动提取元数据
- **Pydantic Schema**: 显式定义输入验证规则

### 使用场景

| 场景 | 推荐方式 | 说明 |
|------|----------|------|
| 简单工具 | Python 函数 | 快速定义，类型注解 |
| 需要验证 | @tool + Pydantic | 参数验证，清晰 schema |
| 复杂输入 | Pydantic Schema | 完整验证规则 |

---

## 3. 系统提示工程范式

### 核心代码

```python
# 03_system_prompt.py

# 方式 1: 基础系统提示
research_instructions = """\
You are an expert researcher. Your job is to conduct \
thorough research, and then write a polished report. \
"""

agent_researcher = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    system_prompt=research_instructions,
)

# 方式 2: 结构化系统提示（推荐）
detailed_research_prompt = """You are an expert researcher specializing in technology and AI.

## Your Role
You conduct thorough, accurate research and synthesize findings into clear, well-organized reports.

## Available Tools
### internet_search
Use this to search the web for information...

## Workflow
1. **Understand the Request**: Clarify what information is needed
2. **Plan Your Research**: Break down complex questions into searchable queries
3. **Gather Information**: Use internet_search to collect relevant data
4. **Verify Information**: Cross-reference multiple sources when possible
5. **Synthesize Findings**: Organize information logically
6. **Write Report**: Produce a clear, well-structured report

## Report Format
- Start with an executive summary
- Use clear headings and sections
- Cite sources where appropriate
"""

# 方式 3: 特定领域提示
coding_assistant_prompt = """You are an expert Python developer and coding assistant.

## Your Expertise
- Python 3.10+ with modern idioms
- Type hints and Pydantic models
- Testing with pytest
"""

# 方式 4: 多语言提示
chinese_assistant_prompt = """你是一个专业的 AI 助手，擅长回答各种问题。

## 你的能力
- 回答知识性问题
- 进行分析和推理
- 帮助写作和编辑
"""
```

### 使用的范式

- **角色定义**: 明确 AI 的身份和专业领域
- **工作流程指导**: 定义任务执行步骤
- **输出格式规范**: 指定期望的输出结构
- **多语言支持**: 根据用户语言调整

### 使用场景

| 场景 | 提示类型 | 说明 |
|------|----------|------|
| 简单任务 | 基础提示 | 简洁定义角色 |
| 复杂研究 | 结构化提示 | 详细工作流程 |
| 专业领域 | 领域专用提示 | 专业知识引导 |
| 本地化 | 多语言提示 | 用户体验优化 |

---

## 4. 中间件范式

### 核心代码

```python
# 04_middleware.py

# 方式 1: @wrap_tool_call 装饰器
from langchain.agents.middleware import wrap_tool_call

call_count = [0]

@wrap_tool_call
def log_tool_calls(request, handler):
    """拦截并记录每个工具调用。"""
    call_count[0] += 1
    tool_name = request.name if hasattr(request, 'name') else str(request)
    print(f"[Middleware] 工具调用 #{call_count[0]}: {tool_name}")
    result = handler(request)
    print(f"[Middleware] 工具调用 #{call_count[0]} 完成")
    return result

# 方式 2: AgentMiddleware 类
from langchain.agents.middleware import AgentMiddleware

class TimingMiddleware(AgentMiddleware):
    """记录工具执行时间的中间件。"""

    def before_tool(self, tool_name: str, tool_args: dict, runtime: Any) -> dict | None:
        import time
        runtime._start_time = time.time()
        print(f"[TimingMiddleware] 开始执行：{tool_name}")
        return None

    def after_tool(self, tool_name: str, tool_args: dict, result: Any, runtime: Any) -> Any:
        import time
        if hasattr(runtime, '_start_time'):
            elapsed = time.time() - runtime._start_time
            print(f"[TimingMiddleware] 完成：{tool_name} ({elapsed:.2f}s)")
        return result

class ValidationMiddleware(AgentMiddleware):
    """验证工具参数的中间件。"""

    def before_tool(self, tool_name: str, tool_args: dict, runtime: Any) -> dict | None:
        if tool_name == "calculate_tax":
            amount = tool_args.get("amount", 0)
            rate = tool_args.get("rate", 0)
            if amount < 0:
                raise ValueError(f"金额不能为负数：{amount}")
            if rate < 0 or rate > 1:
                raise ValueError(f"税率必须在 0-1 之间：{rate}")
        return None

# 方式 3: 使用 Graph State（避免竞态条件）
from langchain.agents.middleware.agent import AgentMiddleware

class SafeCountingMiddleware(AgentMiddleware):
    """安全的计数中间件 - 使用 graph state。"""

    def before_agent(self, state: dict, runtime: Any) -> dict | None:
        current_count = state.get("tool_call_count", 0)
        return {"tool_call_count": current_count + 1}

agent = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[get_weather],
    middleware=[log_tool_calls, TimingMiddleware(), ValidationMiddleware()],
)
```

### 使用的范式

- **@wrap_tool_call 装饰器**: 简单工具调用拦截
- **钩子函数生命周期**: before_tool, after_tool, before_agent, after_agent
- **Graph State 模式**: 避免并发竞态条件

### 使用场景

| 场景 | 中间件类型 | 说明 |
|------|------------|------|
| 日志监控 | @wrap_tool_call | 记录工具调用 |
| 性能分析 | TimingMiddleware | 执行时间追踪 |
| 参数验证 | ValidationMiddleware | 输入校验 |
| 并发安全 | Graph State | 避免竞态条件 |

---

## 5. 子代理范式

### 核心代码

```python
# 05_subagents.py

# 基础子代理配置
research_subagent = {
    "name": "research-agent",
    "description": "Used to research more in-depth questions",
    "system_prompt": "You are a great researcher",
    "tools": [internet_search],
    "model": "openai:gpt-5.4",  # 可选：覆盖主代理模型
}

agent_with_subagent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    subagents=[research_subagent],
)

# 多个专业化子代理
news_analyst_subagent = {
    "name": "news-analyst",
    "description": "Specialized in analyzing current news and recent events.",
    "system_prompt": "You are a news analyst specializing in current events...",
    "tools": [internet_search],
    "model": "google_genai:gemini-3.1-pro-preview",
}

tech_analyst_subagent = {
    "name": "tech-analyst",
    "description": "Expert in technical analysis, code review, and technology research.",
    "system_prompt": "You are a technical analyst with deep expertise...",
    "tools": [internet_search],
    "model": "anthropic:claude-sonnet-4-6",
}

finance_analyst_subagent = {
    "name": "finance-analyst",
    "description": "Specialized in financial analysis, market research, and economic data.",
    "system_prompt": "You are a financial analyst with expertise in markets...",
    "tools": [internet_search],
}

multi_agent_system = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    subagents=[news_analyst_subagent, tech_analyst_subagent, finance_analyst_subagent],
    system_prompt="You are a master analyst coordinating a team of specialized analysts...",
)
```

### 使用的范式

- **专业化分工**: 不同领域由不同子代理处理
- **任务隔离**: 避免主代理上下文膨胀
- **模型优化**: 简单任务用便宜模型，复杂分析用强大模型
- **层次化处理**: 初级代理收集信息，高级代理分析综合

### 使用场景

| 场景 | 子代理配置 | 说明 |
|------|------------|------|
| 多领域分析 | 多个专业子代理 | 新闻、技术、金融分工 |
| 成本优化 | 混合模型配置 | 简单任务用便宜模型 |
| 复杂任务 | 层次化子代理 | 初级/高级研究员 |
| 并行处理 | 独立子代理 | 提高整体效率 |

---

## 6. 人工审批范式

### 核心代码

```python
# 06_human_in_the_loop.py

from langchain.tools import tool
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

@tool
def delete_file(path: str) -> str:
    """Delete a file from the filesystem."""
    return f"Deleted {path}"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    return f"Sent email to {to} with subject: {subject}"

# Checkpointer 是必需的
checkpointer = MemorySaver()

agent_with_approval = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[delete_file, send_email],
    interrupt_on={
        # True: 默认审批选项 (approve, edit, reject)
        "delete_file": True,

        # 自定义审批选项
        "send_email": {"allowed_decisions": ["approve", "reject"]},  # 不允许编辑
    },
    checkpointer=checkpointer,  # 必需！
)
```

### 使用的范式

- **工具级审批**: 针对特定工具配置审批
- **决策类型控制**: approve（批准）、edit（编辑）、reject（拒绝）
- **Checkpointer 必需**: 持久化审批状态

### 使用场景

| 场景 | 审批配置 | 说明 |
|------|----------|------|
| 文件删除 | delete_file: True | 防止数据丢失 |
| 资金转移 | transfer_funds: {approve, reject} | 严格审批，不允许编辑 |
| 系统命令 | execute_command: {approve, reject} | 高风险操作 |
| 只读操作 | read_file: False | 无需审批 |

---

## 7. 技能配置范式

### 核心代码

```python
# 07_skills.py

from urllib.request import urlopen
from deepagents import create_deep_agent
from deepagents.backends.utils import create_file_data
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

# 从 URL 加载技能
skill_url = "https://raw.githubusercontent.com/langchain-ai/deepagents/refs/heads/main/libs/cli/examples/skills/langgraph-docs/SKILL.md"

with urlopen(skill_url) as response:
    skill_content = response.read().decode('utf-8')

skills_files = {
    "/skills/langgraph-docs/SKILL.md": create_file_data(skill_content)
}

agent_with_skills = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    skills=["/skills/"],
    checkpointer=checkpointer,
)

# 自定义技能
custom_skill_content = """# Python 编码专家技能

## 角色
你是一位 Python 编码专家，拥有丰富的 Python 开发经验。

## 能力
- Python 3.10+ 现代语法和惯用法
- 类型注解和 Pydantic 模型
- 单元测试和 pytest
"""

custom_skills_files = {
    "/skills/python-coding-expert/SKILL.md": create_file_data(custom_skill_content),
}

agent_with_custom_skills = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    skills=["/skills/python-coding-expert/"],
    checkpointer=MemorySaver(),
)
```

### 使用的范式

- **AGENTS.md 技能文件**: 专业知识和说明
- **按需加载**: 减少初始 token 消耗
- **目录结构管理**: 按领域组织技能

### 使用场景

| 场景 | 技能类型 | 说明 |
|------|----------|------|
| 领域专家 | LangChain 专家、SQL 专家 | 专业知识加载 |
| 代码能力 | Python 编码专家 | 编码最佳实践 |
| 数据分析 | 数据分析专家 | 统计和可视化 |

---

## 8. 记忆文件范式

### 核心代码

```python
# 08_memory.py

from urllib.request import urlopen
from deepagents import create_deep_agent
from deepagents.backends.utils import create_file_data
from langgraph.checkpoint.memory import MemorySaver

# 从 URL 加载 AGENTS.md
with urlopen("https://raw.githubusercontent.com/langchain-ai/deepagents/refs/heads/main/examples/text-to-sql-agent/AGENTS.md") as response:
    agents_md = response.read().decode("utf-8")

checkpointer = MemorySaver()

agent_with_memory = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    memory=["/AGENTS.md"],
    checkpointer=checkpointer,
)

# 自定义项目记忆
project_agents_md = """# 项目记忆 - LLM Wiki 项目

## 项目概述
这是一个基于 LLM 的个人知识库项目，遵循 Andrej Karpathy 的 LLM Wiki 模式。

## 三层架构
1. raw/ - 原始源文档（不可变）
2. wiki/ - LLM 维护的结构化 wiki
3. CLAUDE.md - 约定和工作流程定义

## 编码规范
- Python 3.10+
- 类型注解
- PEP 8 风格
"""

project_memory_files = {"/AGENTS.md": create_file_data(project_agents_md)}

agent_with_project_memory = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    memory=["/AGENTS.md"],
    checkpointer=MemorySaver(),
)
```

### 使用的范式

- **AGENTS.md 记忆文件**: 持久化上下文
- **跨会话记忆**: 启动时加载记忆
- **与 Skills 配合**: Memory 启动时加载，Skills 按需加载

### 使用场景

| 场景 | 记忆类型 | 说明 |
|------|----------|------|
| 项目规范 | 项目架构、编码规范 | 统一开发标准 |
| 个人偏好 | 沟通风格、代码偏好 | 个性化配置 |
| 团队规范 | Git 工作流、审查清单 | 团队协作 |
| 领域知识 | LangChain 生态 | 背景知识 |

---

## 9. 结构化输出范式

### 核心代码

```python
# 09_structured_output.py

from pydantic import BaseModel, Field
from deepagents import create_deep_agent

# 基础结构
class WeatherReport(BaseModel):
    """A structured weather report."""
    location: str = Field(description="The location for this weather report")
    temperature: float = Field(description="Current temperature in Celsius")
    condition: str = Field(description="Current weather condition")
    humidity: int = Field(description="Humidity percentage")
    forecast: str = Field(description="Brief forecast for the next 24 hours")

agent = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    response_format=WeatherReport,
)

# 嵌套结构
class ResearchSource(BaseModel):
    """A source used in research."""
    title: str = Field(description="Title of the source")
    url: str = Field(description="URL of the source")
    credibility: Literal["high", "medium", "low"] = Field(description="Credibility assessment")

class ResearchFindings(BaseModel):
    """Structured research findings."""
    topic: str = Field(description="The research topic")
    executive_summary: str = Field(description="Brief overview")
    key_points: list[str] = Field(description="Main findings")
    sources: list[ResearchSource] = Field(description="Sources used")
    limitations: str = Field(description="Any limitations")

agent_research = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    response_format=ResearchFindings,
    tools=[internet_search],
)

# 使用示例
result = agent.invoke({
    "messages": [{"role": "user", "content": "What's the weather?"}]
})
print(result["structured_response"])  # WeatherReport 实例
```

### 使用的范式

- **Pydantic 模型验证**: 类型安全、自动验证
- **嵌套结构**: 复杂报告组织
- **字段描述**: 帮助模型理解字段用途
- **验证约束**: ge/le、min_length、Literal

### 使用场景

| 场景 | 响应格式 | 说明 |
|------|----------|------|
| 天气报告 | WeatherReport | 结构化气象数据 |
| 研究报告 | ResearchFindings | 完整研究输出 |
| 产品对比 | ProductComparison | 多产品比较 |
| 代码审查 | CodeReviewReport | 结构化审查意见 |
| 数据分析 | DataAnalysisReport | 统计和洞察 |

---

## 流程图

```mermaid
graph TD
    A[用户请求] --> B[create_deep_agent 配置]

    B --> C[模型配置]
    B --> D[工具配置]
    B --> E[系统提示]
    B --> F[中间件]
    B --> G[子代理]
    B --> H[审批配置]
    B --> I[技能/记忆]
    B --> J[结构化输出]

    C --> C1[provider:model 字符串]
    C --> C2[模型实例]
    C --> C3[弹性配置]

    D --> D1[Python 函数]
    D --> D2[@tool 装饰器]
    D --> D3[Pydantic Schema]

    E --> E1[角色定义]
    E --> E2[工作流程]
    E --> E3[输出格式]

    F --> F1[@wrap_tool_call]
    F --> F2[AgentMiddleware 类]
    F --> F3[Graph State]

    G --> G1[专业化子代理]
    G --> G2[多子代理协作]
    G --> G3[层次化处理]

    H --> H1[工具级审批]
    H --> H2[决策类型控制]
    H --> H3[Checkpointer]

    I --> I1[AGENTS.md 文件]
    I --> I2[按需加载]
    I --> I3[目录管理]

    J --> J1[Pydantic 模型]
    J --> J2[嵌套结构]
    J --> J3[验证约束]

    C1 & C2 & C3 & D1 & D2 & D3 & E1 & E2 & E3 & F1 & F2 & F3 & G1 & G2 & G3 & H1 & H2 & H3 & I1 & I2 & I3 & J1 & J2 & J3 --> K[CompiledStateGraph]

    K --> L[Agent 执行]
    L --> M[工具调用]
    L --> N[子代理委派]
    L --> O[人工审批]
    L --> P[结构化响应]

    M --> Q[结果返回]
    N --> Q
    O --> Q
    P --> Q
```

---

## 完整流程代码

```python
# 完整示例：配置一个功能齐全的 Deep Agent

import os
from typing import Literal
from pydantic import BaseModel, Field
from tavily import TavilyClient
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

# 1. 配置 API Key
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["TAVILY_API_KEY"] = "your-tavily-api-key"

# 2. 定义工具
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run an internet search."""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

# 3. 定义结构化输出
class ResearchReport(BaseModel):
    """Research report."""
    topic: str = Field(description="Research topic")
    summary: str = Field(description="Executive summary")
    findings: list[str] = Field(description="Key findings")
    sources: list[str] = Field(description="Sources used")

# 4. 定义系统提示
system_prompt = """You are an expert researcher.

## Workflow
1. Understand the request
2. Search for information
3. Synthesize findings
4. Write structured report
"""

# 5. 创建 Agent
agent = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[internet_search],
    system_prompt=system_prompt,
    response_format=ResearchReport,
    checkpointer=MemorySaver(),
)

# 6. 运行 Agent
result = agent.invoke({
    "messages": [{"role": "user", "content": "Research AI agents trends."}]
})

# 7. 访问结构化响应
report = result["structured_response"]
print(f"Topic: {report.topic}")
print(f"Summary: {report.summary}")
print(f"Findings: {report.findings}")
```

---

## 范式使用场景总结

| 范式 | 适用场景 | 优势 |
|------|----------|------|
| 模型配置 | 多模型切换、生产部署 | 灵活性、弹性连接 |
| 工具定义 | 扩展 Agent 能力 | 类型注解、自动 schema |
| 系统提示 | 引导 Agent 行为 | 角色定义、工作流程 |
| 中间件 | 日志、验证、监控 | 横切关注点分离 |
| 子代理 | 复杂任务、专业化 | 任务隔离、成本优化 |
| 人工审批 | 敏感操作监督 | 风险控制、安全保障 |
| 技能配置 | 专业知识加载 | 按需加载、减少 token |
| 记忆文件 | 跨会话上下文 | 持久化、个性化 |
| 结构化输出 | 类型安全响应 | 自动验证、IDE 支持 |
