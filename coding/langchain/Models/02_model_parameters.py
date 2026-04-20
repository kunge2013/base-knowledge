"""02_model_parameters.py
Example: Configuring model parameters with init_chat_model.
"""

from langchain.chat_models import init_chat_model

# Configure various model parameters when initializing
model = init_chat_model(
    "claude-sonnet-4-6",
    # Kwargs passed to the model constructor
    temperature=0.7,
    timeout=30,
    max_tokens=1000,
    max_retries=6,  # Default; increase for unreliable networks
)
