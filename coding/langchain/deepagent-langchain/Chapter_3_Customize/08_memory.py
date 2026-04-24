"""
08_memory.py - Memory Configuration for Deep Agents

演示如何为 Deep Agents 配置记忆文件（Memory）：
1. 使用 AGENTS.md 文件提供持久化上下文
2. 从 URL 加载记忆文件
3. memory 参数的多种配置方式

Key Concepts:
- AGENTS.md 记忆文件
- 跨会话上下文持久化
- 与 skills 的区别
"""

import os
from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# Memory 概述
# =============================================================================

"""
Memory（记忆）vs Skills（技能）:

Skills:
- 专业能力和知识
- 按需加载，减少初始上下文
- 用于特定领域的专家知识

Memory:
- 持久化上下文信息
- 在会话开始时加载
- 用于项目规范、个人偏好、长期记忆

两者都使用 AGENTS.md 文件格式，但使用场景不同。
"""


# =============================================================================
# 方式 1: 从 URL 加载记忆文件
# =============================================================================

from deepagents import create_deep_agent
from deepagents.backends.utils import create_file_data
from langgraph.checkpoint.memory import MemorySaver

# 从 GitHub 加载 AGENTS.md 文件
with urlopen("https://raw.githubusercontent.com/langchain-ai/deepagents/refs/heads/main/examples/text-to-sql-agent/AGENTS.md") as response:
    agents_md = response.read().decode("utf-8")

checkpointer = MemorySaver()

agent_with_memory = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    memory=[
        "/AGENTS.md"  # 指定记忆文件路径
    ],
    checkpointer=checkpointer,
)

# 使用时需要种子文件
# result = agent_with_memory.invoke(
#     {
#         "messages": [{"role": "user", "content": "Please tell me what's in your memory files."}],
#         "files": {"/AGENTS.md": create_file_data(agents_md)},
#     },
#     config={"configurable": {"thread_id": "123456"}},
# )


# =============================================================================
# 方式 2: 自定义项目记忆
# =============================================================================

# 项目规范记忆
project_agents_md = """# 项目记忆 - LLM Wiki 项目

## 项目概述
这是一个基于 LLM 的个人知识库项目，遵循 Andrej Karpathy 的 LLM Wiki 模式。

## 三层架构
1. **raw/** - 原始源文档（不可变）
2. **wiki/** - LLM 维护的结构化 wiki（Claude 拥有）
3. **CLAUDE.md** - 约定和工作流程定义

## 编码规范
- 使用 Python 3.10+
- 所有函数必须有类型注解
- 遵循 PEP 8 风格指南
- 使用 pytest 进行测试

## 设计原则
- 不变性优先（immutable patterns）
- 小文件组织（<800 行）
- 明确的错误处理
- 输入验证在系统边界

## 工作流程
1. 阅读 CLAUDE.md 了解项目约定
2. 使用 TDD 方法开发新功能
3. 代码审查后提交

## 常用命令
- `pytest` - 运行测试
- `black .` - 格式化代码
- `ruff check .` - 代码检查
"""

project_memory_files = {
    "/AGENTS.md": create_file_data(project_agents_md),
}

agent_with_project_memory = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    memory=["/AGENTS.md"],
    checkpointer=MemorySaver(),
)


# =============================================================================
# 方式 3: 多记忆文件配置
# =============================================================================

# 个人偏好记忆
personal_preferences_md = """# 个人偏好

## 沟通风格
- 直接、简洁的技术表达
- 避免过度解释已知概念
- 使用中文回答技术问题

## 代码偏好
- 函数式编程风格
- 优先使用不可变数据
- 显式错误处理

## 输出格式
- 使用 Markdown 格式化
- 代码块带语言标识
- 复杂内容分点说明
"""

# 团队规范记忆
team_guidelines_md = """# 团队协作规范

## Git 工作流
- 功能分支命名：feature/xxx
- 提交信息使用英文
- 遵循 conventional commits

## 代码审查清单
- [ ] 代码可读性
- [ ] 错误处理
- [ ] 测试覆盖
- [ ] 性能考虑

## 会议记录模板
- 日期、参与者
- 讨论要点
- 决策和行动计划
"""

# 领域知识记忆
domain_knowledge_md = """# 领域知识 - LangChain 生态系统

## 核心组件
- ChatModel: 语言模型抽象
- Prompt: 提示模板
- OutputParser: 输出解析
- Memory: 对话记忆
- Agent: 自主决策
- Tool: 外部工具集成

## 常用集成
- 向量数据库：Chroma, Pinecone, Weaviate
- 模型提供商：OpenAI, Anthropic, Google
- 工具：Tavily, SerpAPI, Wolfram Alpha
"""

multi_memory_files = {
    "/memory/AGENTS.md": create_file_data(personal_preferences_md),
    "/memory/team.md": create_file_data(team_guidelines_md),
    "/memory/domain-knowledge.md": create_file_data(domain_knowledge_md),
}

agent_with_multiple_memories = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    memory=["/memory/"],
    checkpointer=MemorySaver(),
)


# =============================================================================
# 方式 4: 使用 FilesystemBackend 配置记忆
# =============================================================================

from deepagents.backends import FilesystemBackend
import tempfile

# 创建临时目录
temp_dir = tempfile.mkdtemp()
memory_dir = os.path.join(temp_dir, "memory")
os.makedirs(memory_dir, exist_ok=True)

# 写入记忆文件
memory_file = os.path.join(memory_dir, "AGENTS.md")
with open(memory_file, "w", encoding="utf-8") as f:
    f.write(project_agents_md)

# 使用 FilesystemBackend
filesystem_backend = FilesystemBackend(root_dir=temp_dir)

agent_with_filesystem_memory = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    memory=["/memory/"],
    backend=filesystem_backend,
    checkpointer=MemorySaver(),
)


# =============================================================================
# 记忆文件最佳实践
# =============================================================================

"""
记忆文件最佳实践：

1. 文件组织
   - 使用 AGENTS.md 作为标准文件名
   - 按类别组织记忆（personal, team, project）
   - 使用目录结构管理多个记忆

2. 内容类型
   - 项目规范和架构
   - 个人偏好和风格
   - 团队协作指南
   - 领域知识和参考

3. 与 Skills 配合
   - Memory: 持久化上下文，启动时加载
   - Skills: 按需加载，减少初始 token
   - 可以共用 AGENTS.md 格式

4. Backend 选择
   - StateBackend + files 参数：临时记忆
   - FilesystemBackend: 本地持久化
   - StoreBackend: 共享记忆库

5. 更新策略
   - 定期审查和更新记忆
   - 避免记忆冲突
   - 保持记忆简洁相关
"""

if __name__ == "__main__":
    print("=" * 60)
    print("Deep Agents - Memory 配置示例")
    print("=" * 60)

    print("\n[1] Memory vs Skills:")
    print("  - Memory: 持久化上下文，启动时加载")
    print("  - Skills: 按需加载，减少初始 token")

    print("\n[2] 加载方式:")
    print("  - 从 URL 加载 (GitHub)")
    print("  - 自定义项目记忆")
    print("  - 多记忆文件组合")

    print("\n[3] 记忆类型:")
    print("  - 项目规范 (project_agents)")
    print("  - 个人偏好 (personal_preferences)")
    print("  - 团队规范 (team_guidelines)")
    print("  - 领域知识 (domain_knowledge)")

    print("\n[4] Backend 选项:")
    print("  - StateBackend + files: 临时记忆")
    print("  - FilesystemBackend: 本地持久化")
    print("  - StoreBackend: 共享记忆库")

    print("\n[最佳实践]:")
    print("  - AGENTS.md 标准命名")
    print("  - 按类别组织记忆")
    print("  - 定期审查更新")
    print("  - 与 Skills 配合使用")
