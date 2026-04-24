"""05_summarize_messages.py
Summarize message history using built-in middleware.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from llm_config import default_llm

checkpointer = InMemorySaver()

# Create agent with summarization middleware
agent = create_agent(
    default_llm,
    tools=[],
    middleware=[
        SummarizationMiddleware(
            model=default_llm,
            trigger=("tokens", 4000),  # Trigger when exceeding 4000 tokens
            keep=("messages", 20)       # Keep last 20 messages
        )
    ],
    checkpointer=checkpointer,
)

config = {"configurable": {"thread_id": "1"}}

print("Summarizing message history to manage context window...")
agent.invoke({"messages": "hi, my name is bob"}, config)
agent.invoke({"messages": "write a short poem about cats"}, config)
agent.invoke({"messages": "now do same but for dogs"}, config)
final_response = agent.invoke({"messages": "what's my name?"}, config)

print(f"Final response: {final_response['messages'][-1].content}")
