"""01_basic_initialization.py
Example: Basic model initialization with init_chat_model.
"""

import os
from langchain.chat_models import init_chat_model

# Set API key from environment
os.environ["OPENAI_API_KEY"] = "sk-..."

# Initialize a model - uses automatic provider inference
model = init_chat_model("gpt-5.2")

# Invoke the model
response = model.invoke("Why do parrots talk?")
print(response)
