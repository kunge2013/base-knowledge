"""34_configurable_model.py
Example: Runtime-configurable model with configurable_fields.
"""

from langchain.chat_models import init_chat_model

# Create a configurable model that allows changing model at runtime
configurable_model = init_chat_model(temperature=0)

# Run with different models using config
configurable_model.invoke(
    "what's your name",
    config={"configurable": {"model": "gpt-5-nano"}},  # Run with GPT-5-Nano
)
configurable_model.invoke(
    "what's your name",
    config={"configurable": {"model": "claude-sonnet-4-6"}},  # Run with Claude
)
