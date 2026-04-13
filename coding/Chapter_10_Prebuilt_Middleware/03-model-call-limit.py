"""
3. Model Call Limit Middleware Example

Limit the number of model calls to prevent infinite loops or excessive costs.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("Model Call Limit Middleware Example")
print("Prevents infinite loops and excessive API costs by limiting model calls")
print("=" * 60)

print("\n🔧 Configuration:")
print("   thread_limit: 10 (max model calls across all runs in a thread)")
print("   run_limit: 5 (max model calls per single invocation)")
print("   exit_behavior: 'end' (graceful termination when limit reached)")
print("   checkpointer: InMemorySaver (required for thread-level limiting)")

checkpointer = InMemorySaver()

agent = create_agent(
    model=get_llm("gpt-4.1"),
    checkpointer=checkpointer,
    tools=[],
    middleware=[
        ModelCallLimitMiddleware(
            thread_limit=10,
            run_limit=5,
            exit_behavior="end",
        ),
    ],
)

print("\n✅ Agent created successfully!")

# Invoke with a query
print("\n🚀 Invoking agent with a query to LLM...")
query = "Write a short essay about the benefits of using middleware in AI agents."
print(f"\n👤 User: {query}")
print("\n🤖 LLM is generating response...")
print("-" * 60)

# Configure thread ID
config = {"configurable": {"thread_id": "thread-1"}}

result = agent.invoke(
    {"messages": [HumanMessage(content=query)]},
    config=config
)

print("-" * 60)
print("\n📄 Agent execution result:")
if isinstance(result, dict) and 'messages' in result:
    last_msg = result['messages'][-1]
    if hasattr(last_msg, 'content'):
        print(last_msg.content)
    else:
        print(last_msg)
else:
    print(result)

print("\n" + "=" * 60)
print("Model Call Limit middleware example completed!")
print("\n💡 Note: If the agent gets stuck in a loop and exceeds the limit,")
print("   execution will terminate gracefully according to exit_behavior.")

