"""11_tool_message.py
Using ToolMessage to pass tool execution results back to the model.
"""

from langchain.messages import AIMessage, HumanMessage, ToolMessage
from llm_config import default_llm

# Initialize model
model = default_llm

# Simulate a tool call from the model
ai_message = AIMessage(
    content=[],
    tool_calls=[{
        "name": "get_weather",
        "args": {"location": "San Francisco"},
        "id": "call_123"
    }]
)

# Execute tool and create result message
weather_result = "Sunny, 72°F"
tool_message = ToolMessage(
    content=weather_result,
    tool_call_id="call_123"  # Must match the call ID
)

# Continue conversation
messages = [
    HumanMessage("What's the weather in San Francisco?"),
    ai_message,  # Model's tool call
    tool_message,  # Tool execution result
]

response = model.invoke(messages)
print(f"Response: {response.content}")
