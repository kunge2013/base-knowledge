"""01_basic_usage.py
Basic usage of LangChain messages.
"""

from langchain.messages import HumanMessage, AIMessage, SystemMessage
from llm_config import default_llm

# Initialize model
model = default_llm

# Create system and human messages
system_msg = SystemMessage("You are a helpful assistant.")
human_msg = HumanMessage("Hello, how are you?")

# Use with chat models
messages = [system_msg, human_msg]
response = model.invoke(messages)  # Returns AIMessage

print(f"Response type: {type(response)}")
print(f"Response content: {response.content}")
