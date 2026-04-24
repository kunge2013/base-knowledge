"""
04_middleware.py - Custom Middleware for Deep Agents

演示如何为 Deep Agents 创建和使用自定义中间件：
1. 使用 @wrap_tool_call 装饰器创建日志中间件
2. 使用 AgentMiddleware 类创建自定义中间件
3. 中间件的最佳实践（避免竞态条件）

Key Concepts:
- 中间件扩展功能
- @wrap_tool_call 装饰器
- 使用 graph state 避免竞态条件
- 前置/后置钩子
"""

import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# 方式 1: 使用 @wrap_tool_call 创建简单中间件
# =============================================================================

from langchain.tools import tool
from langchain.agents.middleware import wrap_tool_call
from deepagents import create_deep_agent


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."


@tool
def calculate_tax(amount: float, rate: float) -> float:
    """Calculate tax for a given amount and rate."""
    return amount * rate


# 日志中间件 - 记录所有工具调用
call_count = [0]  # 使用 list 允许在嵌套函数中修改


@wrap_tool_call
def log_tool_calls(request, handler):
    """
    拦截并记录每个工具调用 - 展示横切关注点。

    Args:
        request: 工具调用请求对象
        handler: 执行工具调用的处理函数

    Returns:
        工具执行结果
    """
    call_count[0] += 1
    tool_name = request.name if hasattr(request, 'name') else str(request)

    print(f"[Middleware] 工具调用 #{call_count[0]}: {tool_name}")
    print(f"[Middleware] 参数：{request.args if hasattr(request, 'args') else 'N/A'}")

    # 执行工具调用
    result = handler(request)

    # 记录结果
    print(f"[Middleware] 工具调用 #{call_count[0]} 完成")

    return result


agent_with_logging = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[get_weather, calculate_tax],
    middleware=[log_tool_calls],
)


# =============================================================================
# 方式 2: 使用 AgentMiddleware 类创建自定义中间件
# =============================================================================

from typing import Any
from langchain.agents.middleware import AgentMiddleware


class TimingMiddleware(AgentMiddleware):
    """
    记录工具执行时间的中间件。

    演示如何使用 AgentMiddleware 类创建更复杂的中间件。
    """

    def before_tool(
        self,
        tool_name: str,
        tool_args: dict[str, Any],
        runtime: Any,
    ) -> dict[str, Any] | None:
        """工具执行前的钩子。"""
        import time
        runtime._start_time = time.time()  # 记录开始时间
        print(f"[TimingMiddleware] 开始执行：{tool_name}")
        return None

    def after_tool(
        self,
        tool_name: str,
        tool_args: dict[str, Any],
        result: Any,
        runtime: Any,
    ) -> Any:
        """工具执行后的钩子。"""
        import time
        if hasattr(runtime, '_start_time'):
            elapsed = time.time() - runtime._start_time
            print(f"[TimingMiddleware] 完成：{tool_name} ({elapsed:.2f}s)")
        return result


class ValidationMiddleware(AgentMiddleware):
    """
    验证工具参数的中间件。

    演示如何在工具执行前验证参数。
    """

    def before_tool(
        self,
        tool_name: str,
        tool_args: dict[str, Any],
        runtime: Any,
    ) -> dict[str, Any] | None:
        """工具执行前的钩子 - 验证参数。"""
        # 示例：验证金额参数不能为负
        if tool_name == "calculate_tax":
            amount = tool_args.get("amount", 0)
            rate = tool_args.get("rate", 0)

            if amount < 0:
                raise ValueError(f"金额不能为负数：{amount}")
            if rate < 0 or rate > 1:
                raise ValueError(f"税率必须在 0-1 之间：{rate}")

        print(f"[ValidationMiddleware] 参数验证通过：{tool_name}")
        return None


agent_with_middleware_stack = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[get_weather, calculate_tax],
    middleware=[log_tool_calls, TimingMiddleware(), ValidationMiddleware()],
)


# =============================================================================
# 方式 3: 使用 Graph State 的中间件（推荐）
# =============================================================================

from langchain.agents.middleware.agent import AgentMiddleware


class SafeCountingMiddleware(AgentMiddleware):
    """
    安全的计数中间件 - 使用 graph state 而非实例变量。

    这是推荐的做法，因为在并发场景下更安全。
    """

    def __init__(self):
        # 不在实例中存储可变状态
        pass

    def before_agent(self, state: dict, runtime: Any) -> dict[str, Any] | None:
        """
        在 agent 执行前的钩子。

        使用 graph state 更新计数，避免竞态条件。
        """
        # 更新 graph state 而非 self.x
        current_count = state.get("tool_call_count", 0)
        return {"tool_call_count": current_count + 1}


class ContextAddingMiddleware(AgentMiddleware):
    """
    为 agent 添加额外上下文的中间件。

    演示如何通过 before_agent 添加信息到 state。
    """

    def before_agent(self, state: dict, runtime: Any) -> dict[str, Any] | None:
        """添加元数据到 state。"""
        import datetime

        return {
            "processing_started_at": datetime.datetime.now().isoformat(),
            "middleware_version": "1.0.0",
        }


agent_with_safe_middleware = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[get_weather],
    middleware=[SafeCountingMiddleware(), ContextAddingMiddleware()],
)


# =============================================================================
# 中间件最佳实践
# =============================================================================

"""
中间件最佳实践：

1. 避免可变状态
   - 不要在中间件实例中存储可变状态（如 self.count）
   - 并发场景下会导致竞态条件

   ❌ 错误示例:
   class BadMiddleware(AgentMiddleware):
       def __init__(self):
           self.counter = 0  # 危险！并发会修改共享状态

       def before_agent(self, state, runtime):
           self.counter += 1  # 竞态条件

   ✅ 正确示例:
   class GoodMiddleware(AgentMiddleware):
       def before_agent(self, state, runtime):
           # 使用 graph state
           return {"counter": state.get("counter", 0) + 1}

2. 钩子函数
   - before_tool: 工具执行前（验证、日志）
   - after_tool: 工具执行后（转换结果、日志）
   - before_agent: agent 执行前（添加上下文）
   - after_agent: agent 执行后（处理结果）

3. 中间件组合
   - 可以堆叠多个中间件
   - 注意中间件顺序可能影响行为
   - 每个中间件应该职责单一

4. 错误处理
   - 在中间件中捕获并记录异常
   - 决定是否重新抛出异常
"""

if __name__ == "__main__":
    print("=" * 60)
    print("Deep Agents - 自定义中间件示例")
    print("=" * 60)

    print("\n[1] @wrap_tool_call 装饰器:")
    print("  - 简单的工具调用拦截")
    print("  - 适用于日志、监控")

    print("\n[2] AgentMiddleware 类:")
    print("  - TimingMiddleware: 记录执行时间")
    print("  - ValidationMiddleware: 参数验证")
    print("  - 完整的钩子生命周期")

    print("\n[3] Graph State 中间件:")
    print("  - SafeCountingMiddleware: 安全计数")
    print("  - ContextAddingMiddleware: 添加上下文")
    print("  - 避免并发竞态条件")

    print("\n[最佳实践]:")
    print("  - ❌ 避免可变实例状态")
    print("  - ✅ 使用 graph state")
    print("  - ✅ 职责单一")
    print("  - ✅ 适当错误处理")
