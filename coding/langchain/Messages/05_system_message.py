"""05_system_message.py
Using SystemMessage to set the tone and define the model's role.
"""

from langchain.messages import SystemMessage, HumanMessage
from llm_config import default_llm

# Initialize model
model = default_llm

# Simple system message
system_msg = SystemMessage("You are a helpful coding assistant.")

messages = [
    system_msg,
    HumanMessage("How do I create a REST API?")
]
response = model.invoke(messages)

print(f"Simple System Message Response:\n{response.content}\n")

# Detailed system message with guidelines
system_msg = SystemMessage("""
You are a senior Python developer with expertise in web frameworks.
Always provide code examples and explain your reasoning.
Be concise but thorough in your explanations.
""")

messages = [
    system_msg,
    HumanMessage("How do I create a REST API?")
]
response = model.invoke(messages)

print(f"Detailed System Message Response:\n{response.content}")
