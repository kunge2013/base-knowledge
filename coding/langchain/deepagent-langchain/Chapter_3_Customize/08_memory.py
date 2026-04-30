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
from urllib.request import urlopen, Request, build_opener, install_opener, ProxyHandler
from urllib.error import URLError, HTTPError
from dotenv import load_dotenv
from llm_config import default_llm
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
# 方式 1: 从 URL 加载记忆文件（带错误处理和代理支持）
# =============================================================================

from deepagents import create_deep_agent
from deepagents.backends.utils import create_file_data
from langgraph.checkpoint.memory import MemorySaver


def setup_proxy():
    """配置代理设置。"""
    # 从环境变量或硬编码设置代理
    # 方式1: 从环境变量读取
    proxy = os.getenv("http_proxy") or os.getenv("https_proxy") or os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")

    # 方式2: 直接配置代理（取消注释并修改为你的代理地址）
    proxy = "http://127.0.0.1:7890"  # 示例: 本地代理
    # proxy = "http://username:password@proxy.example.com:8080"  # 示例: 需要认证的代理

    if proxy:
        proxy_handler = ProxyHandler({'http': proxy, 'https': proxy})
        opener = build_opener(proxy_handler)
        install_opener(opener)
        print(f"✓ 已配置代理: {proxy}")
        return True
    else:
        print("ℹ 未配置代理，将直接连接")
        return False


# 配置代理
setup_proxy()

# GitHub URL
github_url = "https://raw.githubusercontent.com/langchain-ai/deepagents/refs/heads/main/examples/text-to-sql-agent/AGENTS.md"

# 尝试从 GitHub 加载 AGENTS.md 文件
agents_md = None
try:
    request = Request(github_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(request, timeout=30) as response:
        agents_md = response.read().decode("utf-8")
    print(f"✓ 成功从 GitHub 加载 AGENTS.md")
except (URLError, HTTPError) as e:
    print(f"✗ 无法从 GitHub 加载 AGENTS.md: {e}")
    print(f"  请检查网络连接或代理设置")
    # 使用本地示例内容作为回退
    agents_md = """# Agent 记忆文件

## 项目概述
这是一个示例 AGENTS.md 文件。

## 编码规范
- 使用 Python 3.10+
- 遵循 PEP 8 风格指南
- 所有函数必须有类型注解

## 工作流程
1. 理解用户需求
2. 分析代码库
3. 提供解决方案
"""
    print(f"  使用本地示例内容作为回退")
except Exception as e:
    print(f"✗ 发生未知错误: {e}")
    raise

checkpointer = MemorySaver()

# 创建方式 1 的 Agent（从 GitHub URL 加载）
agent_with_memory = create_deep_agent(
    model= default_llm,
    memory=["/AGENTS.md"],
    checkpointer=checkpointer,
)

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

# 创建方式 2 的 Agent（自定义项目记忆）
agent_with_project_memory = create_deep_agent(
    model= default_llm,
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

# 创建方式 3 的 Agent（多记忆文件配置）
agent_with_multiple_memories = create_deep_agent(
    model= default_llm,
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

# 创建方式 4 的 Agent（使用 FilesystemBackend）
agent_with_filesystem_memory = create_deep_agent(
    model= default_llm,
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

    print("\n[配置信息]")
    print(f"  当前模型: {default_llm.model}")
    print(f"  温度参数: {default_llm.temperature}")

    print("\n[示例说明]")
    print("  - 方式 1: 从 GitHub URL 加载记忆文件（带代理支持）")
    print("  - 方式 2: 自定义项目记忆")
    print("  - 方式 3: 多记忆文件配置（个人偏好+团队规范+领域知识）")
    print("  - 方式 4: 使用 FilesystemBackend 持久化记忆")

    print("\n" + "=" * 60)
    print("开始运行所有示例...")
    print("=" * 60)

    # 方式 1: 从 GitHub URL 加载记忆文件
    print("\n" + "=" * 60)
    print("方式 1: 从 GitHub URL 加载记忆文件")
    print("=" * 60)

    try:
        result1 = agent_with_memory.invoke(
            {
                "messages": [{"role": "user", "content": "Please tell me what's in your memory files."}],
                "files": {"/AGENTS.md": create_file_data(agents_md)},
            },
            config={"configurable": {"thread_id": "memory_demo_1"}},
        )
        print("\n【Agent 回复】:")
        print(result1["messages"][-1].content)
    except Exception as e:
        print(f"\n✗ 方式 1 执行失败: {e}")

    # 方式 2: 自定义项目记忆
    print("\n" + "=" * 60)
    print("方式 2: 自定义项目记忆")
    print("=" * 60)

    try:
        result2 = agent_with_project_memory.invoke(
            {
                "messages": [{"role": "user", "content": "根据项目规范，我应该使用什么 Python 版本和编码风格？"}],
                "files": project_memory_files,
            },
            config={"configurable": {"thread_id": "memory_demo_2"}},
        )
        print("\n【Agent 回复】:")
        print(result2["messages"][-1].content)
    except Exception as e:
        print(f"\n✗ 方式 2 执行失败: {e}")

    # 方式 3: 多记忆文件配置
    print("\n" + "=" * 60)
    print("方式 3: 多记忆文件配置")
    print("=" * 60)

    try:
        result3 = agent_with_multiple_memories.invoke(
            {
                "messages": [{"role": "user", "content": "根据个人偏好和团队规范，我应该如何编写代码提交信息？"}],
                "files": multi_memory_files,
            },
            config={"configurable": {"thread_id": "memory_demo_3"}},
        )
        print("\n【Agent 回复】:")
        print(result3["messages"][-1].content)
    except Exception as e:
        print(f"\n✗ 方式 3 执行失败: {e}")

    # 方式 4: 使用 FilesystemBackend 持久化记忆
    print("\n" + "=" * 60)
    print("方式 4: 使用 FilesystemBackend 持久化记忆")
    print("=" * 60)

    try:
        result4 = agent_with_filesystem_memory.invoke(
            {
                "messages": [{"role": "user", "content": "告诉我这个项目的三层架构是什么？"}],
            },
            config={"configurable": {"thread_id": "memory_demo_4"}},
        )
        print("\n【Agent 回复】:")
        print(result4["messages"][-1].content)
    except Exception as e:
        print(f"\n✗ 方式 4 执行失败: {e}")

    print("\n" + "=" * 60)
    print("所有示例执行完成")
    print("=" * 60)
