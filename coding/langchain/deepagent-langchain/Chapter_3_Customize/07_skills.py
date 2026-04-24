"""
07_skills.py - Skills Configuration for Deep Agents

演示如何为 Deep Agents 配置技能（Skills）：
1. 从 URL 加载技能文件
2. 使用 StateBackend 配置技能
3. 技能与工具的区别

Key Concepts:
- AGENTS.md 技能文件
- 按需加载技能
- 减少上下文 token 消耗
"""

import os
from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# Skills 概述
# =============================================================================

"""
Skills（技能）vs Tools（工具）:

Tools (工具):
- 低级功能（如文件操作、搜索 API）
- Agent 可以直接调用的函数
- 用于执行具体操作

Skills (技能):
- 高级任务能力和专业知识
- 包含详细说明、参考信息、模板
- 以 AGENTS.md 文件形式存在
- 按需加载，减少初始上下文

示例技能:
- LangChain 专家技能
- SQL 编写技能
- 代码审查技能
- 数据分析技能
"""


# =============================================================================
# 方式 1: 从 URL 加载技能
# =============================================================================

from deepagents import create_deep_agent
from deepagents.backends.utils import create_file_data
from langgraph.checkpoint.memory import MemorySaver
from llm_config import default_llm
checkpointer = MemorySaver()

# 从 GitHub 加载 LangChain 文档技能
skill_url = "https://raw.githubusercontent.com/langchain-ai/deepagents/refs/heads/main/libs/cli/examples/skills/langgraph-docs/SKILL.md"

with urlopen(skill_url) as response:
    skill_content = response.read().decode("utf-8")

# 创建技能文件映射
skills_files = {
    "/skills/langgraph-docs/SKILL.md": create_file_data(skill_content)
}

agent_with_skills = create_deep_agent(
    model=default_llm,
    skills=["/skills/"],  # 指定技能目录
    checkpointer=checkpointer,
)

# 使用时需要种子文件
# result = agent_with_skills.invoke(
#     {
#         "messages": [{"role": "user", "content": "What is langgraph?"}],
#         "files": skills_files,  # 种子文件到 StateBackend
#     },
#     config={"configurable": {"thread_id": "12345"}},
# )


# =============================================================================
# 方式 2: 自定义技能文件
# =============================================================================

# 创建自定义技能内容
custom_skill_content = """# Python 编码专家技能

## 角色
你是一位 Python 编码专家，拥有丰富的 Python 开发经验和最佳实践知识。

## 能力
- Python 3.10+ 现代语法和惯用法
- 类型注解和 Pydantic 模型
- 单元测试和 pytest
- 代码审查和优化
- 调试和性能分析

## 指导原则
1. 编写清晰、可读、Pythonic 的代码
2. 为所有函数添加类型注解
3. 使用 docstrings 说明函数用途
4. 遵循 PEP 8 风格指南
5. 为关键功能建议测试用例

## 代码示例模板

### 函数定义
```python
def function_name(param1: str, param2: int = 0) -> bool:
    \"\"\"
    函数说明。

    Args:
        param1: 参数 1 说明
        param2: 参数 2 说明

    Returns:
        返回值说明
    \"\"\"
    pass
```

### 类定义
```python
class ClassName:
    \"\"\"类说明。\"\"\"

    def __init__(self, value: str):
        self.value = value
"""

# 创建自定义技能文件
custom_skills_files = {
    "/skills/python-coding-expert/SKILL.md": create_file_data(custom_skill_content),
}

agent_with_custom_skills = create_deep_agent(
    model=default_llm,
    skills=["/skills/python-coding-expert/"],
    checkpointer=MemorySaver(),
)


# =============================================================================
# 方式 3: 多技能配置
# =============================================================================

# SQL 编写技能
sql_skill = """# SQL 专家技能

## 能力
- SQL 查询编写和优化
- 数据库模式设计
- 查询性能分析
- 常见数据库方言（PostgreSQL, MySQL, SQLite）

## 最佳实践
1. 使用参数化查询防止 SQL 注入
2. 为常用查询字段添加索引
3. 使用 EXPLAIN 分析查询计划
4. 避免 SELECT *，明确指定列
"""

# 数据分析技能
data_analysis_skill = """# 数据分析专家技能

## 能力
- 使用 Pandas 进行数据操作
- 使用 NumPy 进行数值计算
- 使用 Matplotlib/Seaborn 进行可视化
- 统计分析和假设检验

## 工作流程
1. 数据加载和探索
2. 数据清洗和预处理
3. 探索性数据分析 (EDA)
4. 建模和分析
5. 可视化和报告
"""

multi_skills_files = {
    "/skills/sql-expert/SKILL.md": create_file_data(sql_skill),
    "/skills/data-analyst/SKILL.md": create_file_data(data_analysis_skill),
    "/skills/python-coding-expert/SKILL.md": create_file_data(custom_skill_content),
}

agent_with_multiple_skills = create_deep_agent(
    model=default_llm,
    skills=["/skills/"],  # 加载所有子目录技能
    checkpointer=MemorySaver(),
)


# =============================================================================
# 方式 4: 使用 FilesystemBackend 配置技能
# =============================================================================

from deepagents.backends import FilesystemBackend
import tempfile

# 创建临时目录用于技能文件
temp_dir = tempfile.mkdtemp()
skills_dir = os.path.join(temp_dir, "skills")
os.makedirs(skills_dir, exist_ok=True)

# 写入技能文件
skill_file = os.path.join(skills_dir, "SKILL.md")
with open(skill_file, "w", encoding="utf-8") as f:
    f.write(custom_skill_content)

# 使用 FilesystemBackend
filesystem_backend = FilesystemBackend(root_dir=temp_dir)

agent_with_filesystem_skills = create_deep_agent(
    model=default_llm,
    skills=["/skills/"],
    backend=filesystem_backend,
    checkpointer=MemorySaver(),
)


# =============================================================================
# Skills 最佳实践
# =============================================================================

"""
Skills 最佳实践：

1. 技能文件结构
   - 使用 SKILL.md 作为文件名
   - 包含清晰的角色定义和能力说明
   - 提供使用示例和模板

2. 按需加载
   - 技能文件只在需要时加载
   - 减少初始 token 消耗
   - 提高 agent 启动速度

3. 技能组织
   - 按领域组织技能（如 python-coding-expert, sql-expert）
   - 每个技能文件专注于一个领域
   - 使用目录结构管理技能

4. 与工具配合
   - 技能提供知识，工具执行操作
   - 技能可以指导工具使用
   - 两者互补而非替代

5. Backend 选择
   - StateBackend: 适合临时技能
   - FilesystemBackend: 适合持久化技能
   - StoreBackend: 适合共享技能库
"""

if __name__ == "__main__":
    print("=" * 60)
    print("Deep Agents - Skills 配置示例")
    print("=" * 60)

    print("\n[1] Skills vs Tools:")
    print("  - Tools: 低级功能，直接调用")
    print("  - Skills: 高级能力，AGENTS.md 文件")

    print("\n[2] 加载方式:")
    print("  - 从 URL 加载 (GitHub)")
    print("  - 自定义技能内容")
    print("  - 多技能组合")

    print("\n[3] Backend 选项:")
    print("  - StateBackend: 临时技能")
    print("  - FilesystemBackend: 持久化技能")
    print("  - StoreBackend: 共享技能库")

    print("\n[4] 技能示例:")
    print("  - Python 编码专家")
    print("  - SQL 专家")
    print("  - 数据分析专家")

    print("\n[最佳实践]:")
    print("  - SKILL.md 标准命名")
    print("  - 按需加载减少 token")
    print("  - 按领域组织技能")
    print("  - 与工具互补使用")
