"""08_tool_calls.py
Using AIMessage with tool calls.
"""

from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize model
model = ChatOpenAI(
    model=os.getenv("model"),
    temperature=float(os.getenv("temperature") or 0.1),
    max_tokens=1000,
    timeout=30,
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL") if os.getenv("OPENAI_BASE_URL") else None,
)

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"The weather in {location} is sunny, 72°F"

# Bind tools to model
model_with_tools = model.bind_tools([get_weather])

# Invoke with a question that requires tool use
response = model_with_tools.invoke("What's the weather in Paris?")

print(f"Response type: {type(response)}")
print(f"Response content: {response.content}")
print(f"\nTool calls:")
for tool_call in response.tool_calls:
    print(f"  Tool: {tool_call['name']}")
    print(f"  Args: {tool_call['args']}")
    print(f"  ID: {tool_call['id']}")
