"""02_static_model_instance.py
Example: Static model initialization with direct model instance.
"""

from langchain.agents import create_agent
from llm_config import get_llm

# Assume tools are defined elsewhere
tools = []

# Get configured model instance
model = get_llm(model_name="gpt-4.1-mini", temperature=0.1)

# Create agent with model instance
agent = create_agent(model, tools=tools)
