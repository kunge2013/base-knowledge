"""08_dynamic_prompt.py
Create dynamic prompts based on conversation state.
"""

from langchain.agents import. create_agent
from typing import TypedDict
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from llm_config import default_llm
from langchain.tools import tool

class CustomContext(TypedDict):
    user_name: str

@tool
def get_weather(city: str) -> str:
    """Get weather in a city."""
    return f"The weather in {city} is always sunny!"

@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    user_name = request.runtime.context["user_name"]
    system_prompt = f"You are a helpful assistant. Address the user as {user_name}."
    return system_prompt

agent = create_agent(
    default_llm,
    tools=[get_weather],
    middleware=[dynamic_system_prompt],
    context_schema=CustomContext,
)

print("Dynamic prompt based on context:")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is weather in SF?"]]},
    context=CustomContext(user_name="John Smith"),
)

for msg in result["messages"]:
    print(f"{msg.type}: {msg.content[:100]}")
