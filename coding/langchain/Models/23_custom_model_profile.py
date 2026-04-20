"""23_custom_model_profile.py
Example: Setting a custom model profile.
"""

from langchain.chat_models import init_chat_model

# Define a custom profile with capabilities information
custom_profile = {
    "max_input_tokens": 100_000,
    "tool_calling": True,
    "structured_output": True,
    # ...
}
model = init_chat_model("...", profile=custom_profile)
