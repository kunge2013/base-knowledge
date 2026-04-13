"""07_human_in_the_loop.py
Handle human-in-the-loop interrupts during streaming.
"""

from typing import Any
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, Interrupt
from llm_config import default_llm

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

checkpointer = InMemorySaver()

agent = create_agent(
    default_llm,
    tools=[get_weather],
    middleware=[
        HumanInTheLoopMiddleware(interrupt_on={"get_weather": True}),
    ],
    checkpointer=checkpointer,
)

def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)

def _render_completed_message(message: AnyMessage) -> None:
    if (isinstance(message, AIMessage) and
        hasattr(message, 'tool_calls') and
        message.tool_calls):
        print(f"\nTool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")

def _render_interrupt(interrupt: Interrupt) -> None:
    interrupts = interrupt.value if hasattr(interrupt, 'value') else {}
    if "action_requests" in interrupts:
        for request in interrupts["action_requests"]:
            print(f"\nInterrupt: {request.get('description', str(request))}")

input = "Can you look up weather in Boston and San Francisco?"
config = {"configurable": {"thread_id": "some_id"}}

print("Streaming with human-in-the-loop:")
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": input}]},
    config=config,
    stream_mode=["messages", "updates"],
    version="v2",
):
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":
        for source, update in chunk["data"].items():
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
            elif source == "__interrupt__":
                if isinstance(update, list) and update:
                    _render_interrupt(update[0])
