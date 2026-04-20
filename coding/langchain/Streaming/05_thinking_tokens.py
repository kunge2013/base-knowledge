"""05_thinking_tokens.py
Stream thinking/reasoning tokens from models.
"""

from langchain.agents import create_agent
from langchain.messages import AIMessageChunk
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from llm_config import get_llm

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# Create model with thinking enabled
model = get_llm()
if hasattr(model, 'with_config'):
    # Try to enable thinking if supported
    try:
        model = model.with_config({"thinking": {"type": "enabled", "budget_tokens": 5000}})
    except:
        pass

agent = create_agent(
    model,
    tools=[get_weather],
)

print("Streaming thinking tokens:")
for token, metadata in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="messages",
    version="v2",
):
    if not isinstance(token, AIMessageChunk):
        continue

    # Extract reasoning and text blocks
    reasoning = [b for b in token.content_blocks if b.get("type") == "reasoning"]
    text = [b for b in token.content_blocks if b.get("type") == "text"]

    if reasoning:
        print(f"[thinking] {reasoning[0].get('reasoning', '')[:100]}...")
    if text:
        print(text[0].get("text", ''), end="")
