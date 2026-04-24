"""
01_model_configuration.py - Model Configuration for Deep Agents

演示 Deep Agents 中模型配置的多种方式：
1. 使用 provider:model 字符串格式快速切换模型
2. 使用初始化的模型实例进行精细控制
3. 配置连接的弹性（重试次数、超时等）

Key Concepts:
- provider:model 字符串格式
- 模型实例初始化
- 连接弹性配置（max_retries, timeout）
"""

import os
from dotenv import load_dotenv
from llm_config import default_llm
load_dotenv()

# =============================================================================
# 方式 1: 使用 provider:model 字符串格式
# =============================================================================

from deepagents import create_deep_agent

# 快速配置 OpenAI 模型
agent_openai = create_deep_agent(model=default_llm)


# =============================================================================
# 模型选择建议
# =============================================================================

"""
模型选择建议：

| 场景                     | 推荐配置                       | 说明                        |
|------------------------|----------------------------|---------------------------|
| 快速原型开发               | provider:model 字符串         | 简洁，快速切换                |
| 生产环境                  | 模型实例 + 弹性配置            | 可控性强，错误处理好            |
| 不可靠网络环境             | max_retries=10-15           | 增加重试次数                 |
| 长时间任务               | checkpointer + 弹性配置       | 保存进度，防止丢失              |
| 多模型切换测试             | provider:model 字符串         | 方便快速切换不同提供商           |

"""

if __name__ == "__main__":
    print("=" * 60)
    print("Deep Agents - 模型配置示例")
    print("=" * 60)

    print("\n[1] provider:model 字符串格式:")
    print("  - openai:gpt-5.4")
    print("  - google_genai:gemini-3.1-pro-preview")
    print("  - anthropic:claude-sonnet-4-6")

    print("\n[2] 模型实例配置:")
    print("  - ChatOpenAI(...)")
    print("  - ChatAnthropic(...)")
    print("  - init_chat_model(...)")

    print("\n[3] 连接弹性配置:")
    print("  - max_retries=10 (默认 6)")
    print("  - timeout=120 (秒)")
    print("  - 配合 checkpointer 保存进度")
