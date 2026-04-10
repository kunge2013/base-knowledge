"""35_configurable_multiple.py
Example: Configurable model with multiple configurable parameters and prefixes.
"""

from langchain.chat_models import init_chat_model

# Create a configurable model with multiple configurable parameters
# Use config_prefix for chains with multiple models
first_model = init_chat_model(
        model="gpt-4.1-mini",
        temperature=0,
        configurable_fields=("model", "model_provider", "temperature", "max_tokens"),
        config_prefix="first",  # Prefix for configurable params
)

# Default invocation uses configured defaults
first_model.invoke("what's your name")

# Invoke with different runtime configuration
first_model.invoke(
    "what's your name",
    config={
        "configurable": {
            "first_model": "claude-sonnet-4-6",
            "first_temperature": 0.5,
            "first_max_tokens": 100,
        }
    },
)
