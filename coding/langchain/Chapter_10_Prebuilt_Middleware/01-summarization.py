"""
1. Summarization Middleware Example

Automatically summarize conversation history when approaching token limits,
preserving recent messages while compressing older context.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("Summarization Middleware Example")
print("Automatically summarizes old conversation when token limit is approached")
print("=" * 60)

# Single condition: trigger if tokens >= 4000, keep last 20 messages
print("\n🔧 Creating agent with single condition trigger...")
print("   Trigger: tokens >= 4000")
print("   Keep: last 20 messages")

agent_single = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[],
    middleware=[
        SummarizationMiddleware(
            model=get_llm("gpt-4.1-mini"),
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
    ],
)

# Multiple conditions: trigger if number of tokens >= 3000 OR messages >= 6
print("\n🔧 Creating agent with multiple conditions...")
print("   Trigger: tokens >= 3000 OR messages >= 6")
print("   Keep: last 20 messages")

agent_multiple = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[],
    middleware=[
        SummarizationMiddleware(
            model=get_llm("gpt-4.1-mini"),
            trigger=[
                ("tokens", 3000),
                ("messages", 6),
            ],
            keep=("messages", 20),
        ),
    ],
)

# Using fractional limits
print("\n🔧 Creating agent with fractional limits...")
print("   Trigger: >= 80% of model context")
print("   Keep: 30% of model context after summarization")

agent_fractional = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[],
    middleware=[
        SummarizationMiddleware(
            model=get_llm("gpt-4.1-mini"),
            trigger=("fraction", 0.8),
            keep=("fraction", 0.3),
        ),
    ],
)

# Using custom profile with model
custom_profile = {
    "max_input_tokens": 100_000,
}
model = init_chat_model("gpt-4.1", profile=custom_profile)
print(f"\n✅ Created custom profile model with max_input_tokens = {custom_profile['max_input_tokens']:,}")

# Test invocation on the single condition agent
print("\n🚀 Invoking agent with a query to LLM...")
query = "Explain what is middleware in the context of LangChain agents and why it's useful."
print(f"\n👤 User: {query}")
print("\n🤖 LLM is generating response...")
print("-" * 60)

result = agent_single.invoke({
    "messages": [HumanMessage(content=query)]
})

print("-" * 60)
print("\n📄 LLM Response:")
if hasattr(result, 'content'):
    print(result.content)
elif isinstance(result, dict) and 'messages' in result:
    last_message = result['messages'][-1]
    print(last_message.content if hasattr(last_message, 'content') else last_message)
else:
    print(result)

print("\n" + "=" * 60)
print("Summarization middleware example completed!")
print("\n💡 Note: Summarization triggers automatically when token thresholds")
print("   are reached in longer conversations. In this short example,")
print("   summarization won't trigger yet, but the middleware is active.")

