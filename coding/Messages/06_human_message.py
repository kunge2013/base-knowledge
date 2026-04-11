"""06_human_message.py
Using HumanMessage with different content types and metadata.
"""

from langchain.messages import HumanMessage
from llm_config import default_llm

# Initialize model
model = default_llm

# Text content
response = model.invoke([
    HumanMessage("What is machine learning?")
])
print(f"Text content response:\n{response.content}\n")

# Message metadata
human_msg = HumanMessage(
    content="Hello!",
    name="alice",  # Optional: identify different users
    id="msg_123",  # Optional: unique identifier for tracing
)

response = model.invoke([human_msg])
print(f"Message with metadata:\n{response.content}")
print(f"Message name: {human_msg.name}")
print(f"Message ID: {human_msg.id}")
