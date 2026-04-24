"""
06_human_in_the_loop.py - Human-in-the-Loop for Deep Agents

演示如何为 Deep Agents 配置人工审批流程：
1. 配置工具级别的人工审批
2. 自定义审批决策类型（approve, edit, reject）
3. Checkpointer 的必要性

Key Concepts:
- 工具调用人工审批
- interrupt_on 配置
- MemorySaver checkpointer
- 审批决策类型
"""

import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# 定义需要审批的工具
# =============================================================================

from langchain.tools import tool
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver
from llm_config import default_llm
from langchain.messages import HumanMessage
@tool
def delete_file(path: str) -> str:
    """Delete a file from the filesystem."""
    # 示例实现
    return f"Deleted {path}"


@tool
def read_file(path: str) -> str:
    """Read a file from the filesystem."""
    # 示例实现
    return f"Contents of {path}"


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    # 示例实现
    return f"Sent email to {to} with subject: {subject}"


@tool
def execute_command(command: str) -> str:
    """Execute a shell command."""
    # 示例实现
    return f"Executed: {command}"


@tool
def transfer_funds(amount: float, to_account: str) -> str:
    """Transfer funds to another account."""
    # 示例实现
    return f"Transferred ${amount} to {to_account}"


# =============================================================================
# 方式 1: 基础人工审批配置
# =============================================================================

# Checkpointer 是人工审批的必需组件
checkpointer = MemorySaver()

agent_with_approval = create_deep_agent(
    model=default_llm,
    tools=[delete_file, read_file, send_email],
    interrupt_on={
        # True: 使用默认审批选项 (approve, edit, reject)
        "delete_file": True,

        # False: 不需要审批
        "read_file": False,

        # 自定义审批选项
        # "send_email": {"allowed_decisions": ["approve", "reject"]},  # 不允许编辑
        "send_email": False,  # 不允许编辑
    },
    checkpointer=checkpointer,  # 必需！
)


# =============================================================================
# 方式 2: 详细的审批配置
# =============================================================================

agent_detailed_approval = create_deep_agent(
    model=default_llm,
    tools=[delete_file, execute_command, transfer_funds],
    interrupt_on={
        # 删除文件 - 需要审批
        "delete_file": {
            "allowed_decisions": ["approve", "reject", "edit"],
            # 可以添加更多配置选项
        },

        # 执行命令 - 高风险操作，只允许批准或拒绝
        "execute_command": {
            "allowed_decisions": ["approve", "reject"],
        },

        # 资金转移 - 最高风险，严格审批
        "transfer_funds": {
            "allowed_decisions": ["approve", "reject"],
            # 可以添加额外的验证逻辑
        },
    },
    checkpointer=MemorySaver(),
)


# =============================================================================
# 方式 3: 安全的文件操作代理
# =============================================================================

safe_file_agent = create_deep_agent(
    model=default_llm,
    tools=[delete_file, read_file],
    interrupt_on={
        # 只读操作不需要审批
        "read_file": False,

        # 写入/删除操作需要审批
        "delete_file": True,
    },
    checkpointer=MemorySaver(),
    system_prompt="""You are a file management assistant with safety constraints.

Safety Rules:
1. Reading files does not require approval
2. Deleting files ALWAYS requires human approval
3. Explain the consequences of file deletion before proceeding
4. Suggest alternatives to deletion when appropriate (e.g., move, archive)

When a user asks you to delete a file:
1. Confirm the file path
2. Warn about permanent data loss
3. Wait for human approval before proceeding
""",
)


# =============================================================================
# 人工审批工作流程
# =============================================================================

"""
人工审批工作流程：

1. 配置阶段
   ```python
   checkpointer = MemorySaver()  # 必需

   agent = create_deep_agent(
       tools=[sensitive_tool],
       interrupt_on={"tool_name": True},
       checkpointer=checkpointer,
   )
   ```

2. 运行时流程
   - Agent 决定调用工具
   - 检测到 interrupt_on 配置
   - 暂停执行并等待人类审批
   - 人类可以选择：approve（批准）、edit（编辑后批准）、reject（拒绝）
   - 根据决定继续或取消

3. 审批决策类型
   - approve: 直接执行工具调用
   - edit: 修改参数后执行
   - reject: 取消工具调用

4. 使用场景
   - 文件删除操作
   - 资金转移
   - 发送消息/邮件
   - 执行系统命令
   - API 写入操作
   - 数据库修改
"""


# =============================================================================
# 最佳实践
# =============================================================================

"""
人工审批最佳实践：

1. Checkpointer 必需
   - 没有 checkpointer，人工审批无法工作
   - MemorySaver 是最简单的选择

2. 工具分类
   - 只读操作：不需要审批（read_file, get_weather）
   - 写入操作：需要审批（delete_file, write_file）
   - 敏感操作：严格审批（transfer_funds, execute_command）

3. 审批粒度
   - 根据风险级别配置不同审批策略
   - 高风险操作只允许 approve/reject
   - 中等风险操作允许 edit

4. 系统提示配合
   - 在系统提示中说明哪些操作需要审批
   - 让 agent 预先告知用户后果

5. 线程管理
   - 使用 thread_id 追踪审批状态
   - config={"configurable": {"thread_id": "unique-id"}}
"""

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "thread-1"}}
    # data = safe_file_agent.invoke({"messages": [HumanMessage(content="删除1.txt")]},
    #                                config=config)
    print("=" * 60)
    agent_with_approval.invoke({"messages": [HumanMessage(content="先去读文件1.txt 再将内容发送邮件给 zhangsan@qq.com")]},
                               config=config)
    # print("Deep Agents - 人工审批 (Human-in-the-Loop) 示例")
    # print("=" * 60)
    #
    # print("\n[1] 基础审批配置:")
    # print("  - delete_file: True (默认审批选项)")
    # print("  - read_file: False (无需审批)")
    # print("  - send_email: {allowed_decisions: ['approve', 'reject']}")
    #
    # print("\n[2] 详细审批配置:")
    # print("  - 针对不同工具配置不同审批策略")
    # print("  - 高风险操作只允许 approve/reject")
    #
    # print("\n[3] 安全文件操作:")
    # print("  - 只读操作自动执行")
    # print("  - 删除操作必须审批")
    #
    # print("\n[关键要求]:")
    # print("  - ⚠️ checkpointer 是必需的!")
    # print("  - 使用 MemorySaver() 或持久化存储")
    #
    # print("\n[审批决策类型]:")
    # print("  - approve: 直接执行")
    # print("  - edit: 修改后执行")
    # print("  - reject: 取消执行")
