"""07_ai_message.py
Using AIMessage to represent model responses and create conversation history.
"""

from langchain.messages import AIMessage, SystemMessage, HumanMessage
from llm_config import default_llm

# Initialize model
model = default_llm

# Get AI message response
response = model.invoke("Explain AI")
print(f"Response type: {type(response)}")
print(f"Response content: {response.content}\n")

# Create an AI message manually (e.g., for conversation history)
ai_msg = AIMessage("I'd be happy to help you with that question!")

# Add to conversation history
messages = [
    SystemMessage("You are a helpful assistant"),
    HumanMessage("Can you help me?"),
    ai_msg,  # Insert as if it came from the model
    HumanMessage("Great! What's 2+2?")
]

response = model.invoke(messages)
print(f"Conversation response:\n{response.content}")
