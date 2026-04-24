"""03_message_prompts.py
Using message prompts for multi-turn conversations and complex scenarios.
"""

from langchain.messages import SystemMessage, HumanMessage, AIMessage
from llm_config import default_llm

# Initialize model
model = default_llm

# Create conversation history with multiple messages
messages = [
    SystemMessage("You are a poetry expert"),
    HumanMessage("Write a haiku about spring"),
    AIMessage("Cherry blossoms bloom\nPink petals dance in breeze\nNature wakes from sleep"),
    HumanMessage("Now write one about winter")
]
response = model.invoke(messages)

print(f"Response: {response.content}")

print("\n--- Use message prompts when: ---")
print("- Managing multi-turn conversations")
print("- Working with multimodal content (images, audio, files)")
print("- Including system instructions")
