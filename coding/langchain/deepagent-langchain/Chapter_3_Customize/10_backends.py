"""
10_backends.py - Backend Configuration for Deep Agents

演示 Deep Agents 中 Backend 的配置和使用：
1. StateBackend - 默认的临时文件系统后端
2. FilesystemBackend - 本地文件系统后端
3. StoreBackend - 持久化存储后端
4. CompositeBackend - 组合多个后端

Key Concepts:
- Backend 为 agent 提供虚拟文件系统
- StateBackend 仅在单个线程中持久化
- 使用 skills/memory 时需要预先加载文件
"""

import os
from dotenv import load_dotenv
from llm_config import default_llm

load_dotenv()

# =============================================================================
# 1. StateBackend (默认后端)
# =============================================================================

from deepagents import create_deep_agent
from deepagents.backends import StateBackend

# 默认使用 StateBackend - 临时文件系统,仅在单个线程中持久化
agent_default = create_deep_agent(model=default_llm)

# 显式配置 StateBackend
agent_state_backend = create_deep_agent(
    model=default_llm,
    backend=StateBackend()
)

# =============================================================================
# 2. FilesystemBackend
# =============================================================================

from deepagents.backends import FilesystemBackend

# 使用本地文件系统作为后端
# 注意: 这会直接修改本地文件系统
filesystem_backend = FilesystemBackend(
    root_dir="./agent_workspace",  # 工作目录
    allow_absolute_paths=False,    # 禁止绝对路径访问
)

agent_filesystem = create_deep_agent(
    model=default_llm,
    backend=filesystem_backend,
    system_prompt="You are a file management assistant with local filesystem access."
)

# =============================================================================
# 3. StoreBackend
# =============================================================================

from deepagents.backends import StoreBackend
from langgraph.store.memory import InMemoryStore

# 使用 LangGraph Store 进行持久化存储
store = InMemoryStore()

store_backend = StoreBackend(
    store=store,
    namespace=["agent_files"],  # 存储命名空间
)

agent_store = create_deep_agent(
    model=default_llm,
    backend=store_backend,
    system_prompt="You are an assistant with persistent storage capabilities."
)

# =============================================================================
# 4. CompositeBackend - 组合多个后端
# =============================================================================

from deepagents.backends import CompositeBackend

# 组合多个后端 - 优先级从高到低
composite_backend = CompositeBackend(
    backends=[
        StateBackend(),              # 优先使用临时存储
        filesystem_backend,          # 其次使用本地文件系统
    ]
)

agent_composite = create_deep_agent(
    model=default_llm,
    backend=composite_backend,
    system_prompt="You are an assistant with multi-tier storage."
)

# =============================================================================
# 5. 使用 Backend 加载 Skills/Memory 文件
# =============================================================================

from deepagents.backends.utils import create_file_data
from langgraph.checkpoint.memory import MemorySaver

# 创建 checkpointer (skills/memory 必需)
checkpointer = MemorySaver()

# 准备 skills 文件
skill_content = """
# SKILL.md - Research Skill

## Purpose
This skill helps the agent conduct thorough research.

## Instructions
1. Identify the research question
2. Search for relevant sources
3. Analyze and synthesize findings
4. Present conclusions clearly
"""

skills_files = {
    "/skills/research/SKILL.md": create_file_data(skill_content)
}

# 创建 agent 并预加载 skills 文件
agent_with_skills = create_deep_agent(
    model=default_llm,
    skills=["/skills/research/"],
    checkpointer=checkpointer,
)

# 调用时提供文件
result = agent_with_skills.invoke(
    {
        "messages": [{"role": "user", "content": "Help me research AI trends"}],
        "files": skills_files  # 预加载的文件
    },
    config={"configurable": {"thread_id": "research-session"}}
)

# =============================================================================
# Backend 选择建议
# =============================================================================

"""
Backend 选择指南:

| Backend 类型        | 适用场景                              | 持久性          |
|-------------------|-----------------------------------|---------------|
| StateBackend      | 临时文件处理,单次对话                    | 仅当前线程        |
| FilesystemBackend | 需要访问本地文件系统                     | 本地持久化       |
| StoreBackend      | 需要跨会话持久化                        | 跨会话持久化     |
| CompositeBackend  | 需要多层存储策略                        | 按优先级持久化    |

注意事项:
- 使用 skills 或 memory 时,必须预先将文件加载到 backend
- StateBackend 的文件仅在单个 thread 中可见
- FilesystemBackend 会修改真实文件系统,谨慎使用
- CompositeBackend 按顺序查找文件,第一个找到的优先

"""

if __name__ == "__main__":
    print("=" * 60)
    print("Deep Agents - Backend Configuration 示例")
    print("=" * 60)

    print("\n[1] StateBackend (默认):")
    print("  - 临时文件系统,仅在单个线程中持久化")
    print("  - 适用于: 临时文件处理,单次对话")

    print("\n[2] FilesystemBackend:")
    print("  - 本地文件系统访问")
    print("  - 适用于: 需要持久化本地文件")

    print("\n[3] StoreBackend:")
    print("  - 使用 LangGraph Store 持久化")
    print("  - 适用于: 跨会话数据持久化")

    print("\n[4] CompositeBackend:")
    print("  - 组合多个后端")
    print("  - 适用于: 多层存储策略")

    print("\n[5] Skills/Memory 文件加载:")
    print("  - 使用 create_file_data() 创建文件")
    print("  - 在 invoke() 时通过 'files' 参数提供")
    print("  - 需要 checkpointer 支持")

    print("\n✅ Backend 配置完成!")