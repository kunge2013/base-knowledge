"""29_custom_base_url.py
Example: Using a custom base URL for OpenAI-compatible APIs.
"""

from langchain.chat_models import init_chat_model

# Use custom base URL for OpenAI-compatible API
# Works with Together AI, vLLM, OpenRouter, etc.
model = init_chat_model(
    model="MODEL_NAME",
    model_provider="openai",
    base_url="BASE_URL",
    api_key="YOUR_API_KEY",
)
