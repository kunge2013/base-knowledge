"""22_model_profile.py
Example: Accessing and customizing model capability profiles.
"""

from langchain.chat_models import init_chat_model

# Access model profile to get capabilities information
model = init_chat_model("gpt-4.1-mini")
print(model.profile)
# {
#   "max_input_tokens": 400000,
#   "image_inputs": True,
#   "reasoning_output": True,
#   "tool_calling": True,
#   ...
# }
