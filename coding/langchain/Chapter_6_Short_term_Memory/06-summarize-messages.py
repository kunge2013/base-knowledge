"""
6. Summarize Messages with SummarizationMiddleware

Summarize older messages to retain information while staying within context window.
Uses SummarizationMiddleware that automatically triggers when token count exceeds threshold.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("6. SummarizationMiddleware Example")
print("Automatic summarization when token count exceeds threshold")
print("=" * 60)


print("\n🔧 Configuration:")
print("   - Trigger: token count > 4000")
print("   - Keep last 20 messages intact")
print("   - Summarize older messages into a single summary")
print("   - Uses separate smaller model for summarization to save cost")

checkpointer = InMemorySaver()

# Create agent with SummarizationMiddleware
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[],
    middleware=[
        SummarizationMiddleware(
            model=get_llm("gpt-4.1-mini"),  # Smaller model for summarization
            trigger=("tokens", 4000),      # Trigger when tokens > 4000
            keep=("messages", 20),          # Keep last 20 messages intact
        )
    ],
    checkpointer=checkpointer,
)

print("\n✅ Agent created with SummarizationMiddleware!")

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

# Multiple turns to demonstrate (would eventually trigger summarization)
turns = [
    "hi, my name is bob",
    "write a short poem about cats",
    "now do the same but for dogs",
    "what's my name?",
]

print("\n🚀 Running multiple conversation turns...")
print(f"Summarization triggers at 4000+ tokens, so this demo won't trigger it\nbut shows the setup that automatically summarizes when threshold reached.\n")

try:
    for i, turn in enumerate(turns):
        print(f"{'='*50}")
        print(f"Turn {i+1}: {turn}")
        print("-" * 50)

        result = agent.invoke({"messages": HumanMessage(content=turn)}, config)

        if isinstance(result, dict) and 'messages' in result:
            print(f"\nTotal messages: {len(result['messages'])}")
            last_msg = result['messages'][-1]
            if hasattr(last_msg, 'content'):
                print(f"Response: {last_msg.content}")

except Exception as e:
    print("-" * 50)
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("Summarization middleware example completed!")
print("\n💡 Benefits of summarization:")
print("   - Retains information from older messages")
print("   - Still controls context window size")
print("   - Automatic trigger on token or message count")
print("   - Uses cheaper/smaller model for summarization")
print("   - Better than trimming/deletion when you need to retain info")
print("\n⚙️ Configuration options:")
print("   - trigger: ('tokens', N) or ('messages', N)")
print("   - keep: How many recent messages to keep intact")
print("   - model: Which model to use for summarization")
print("   - system_prompt: Custom prompt for the summarization")
