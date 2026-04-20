"""
5. Model Fallback Middleware Example

Automatically fallback to alternative models when the primary model fails.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("Model Fallback Middleware Example")
print("Automatically fallback to alternative models when primary model fails")
print("=" * 60)

print("\n🔧 Configuration:")
print("   Primary: gpt-4.1 (configured via llm_config)")
print("   Fallback 1: gpt-4.1-mini")
print("   Fallback 2: claude-3-5-sonnet-20241022")

# Note: The actual model instances are retrieved via llm_config
# For this example, we use string identifiers as shown in the docs
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[],
    middleware=[
        ModelFallbackMiddleware(
            "gpt-4.1-mini",
            "claude-3-5-sonnet-20241022",
        ),
    ],
)

print("\n✅ Agent created successfully!")

# Invoke with a query
print("\n🚀 Invoking agent with a query to LLM...")
query = "What are the benefits of having model fallback in production AI systems?"
print(f"\n👤 User: {query}")
print("\n🤖 LLM is generating response...")
print("-" * 60)

result = agent.invoke({
    "messages": [HumanMessage(content=query)]
})

print("-" * 60)
print("\n📄 LLM Response:")
if isinstance(result, dict) and 'messages' in result:
    last_msg = result['messages'][-1]
    if hasattr(last_msg, 'content'):
        print(last_msg.content)
    else:
        print(last_msg)
else:
    print(result)

print("\n" + "=" * 60)
print("Model Fallback middleware example completed!")
print("\n💡 If primary model fails (timeout, rate limit, error),")
print("   the middleware automatically tries the next fallback model in order.")
print("   This builds greater resilience into production agent deployments.")

