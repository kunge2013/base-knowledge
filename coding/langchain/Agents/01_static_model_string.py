"""01_static_model_string.py
Example: Static model initialization with string identifier.
"""

from langchain.agents import create_agent
from llm_config import get_llm

# Assume tools are defined elsewhere
tools = []

# Using string identifier for automatic inference
agent = create_agent("openai:gpt-4.1-mini", tools=tools)
