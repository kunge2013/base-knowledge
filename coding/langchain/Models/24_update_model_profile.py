"""24_update_model_profile.py
Example: Updating an existing model profile.
"""

from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4.1-mini")

# Create new profile by merging with existing
new_profile = model.profile | {"key": "value"}
# Create a copy with updated profile (avoids mutation of shared state)
updated_model = model.model_copy(update={"profile": new_profile})
