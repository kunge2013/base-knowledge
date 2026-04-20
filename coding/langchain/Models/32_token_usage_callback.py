"""32_token_usage_callback.py
Example: Tracking aggregate token usage with callback handler.
"""

from langchain.chat_models import init_chat_model
from langchain_core.callbacks import UsageMetadataCallbackHandler

# Track aggregate token usage across multiple models
callback = UsageMetadataCallbackHandler()

model_1 = init_chat_model(model="gpt-4.1-mini")
model_2 = init_chat_model(model="claude-haiku-4-5-20251001")

result_1 = model_1.invoke("Hello", config={"callbacks": [callback]})
result_2 = model_2.invoke("Hello", config={"callbacks": [callback]})

# Print aggregated usage
print(callback.usage_metadata)

# Output:
# {
#     'gpt-4.1-mini-2025-04-14': {
#         'input_tokens': 8,
#         'output_tokens': 10,
#         'total_tokens': 18,
#         'input_token_details': {'audio': 0, 'cache_read': 0},
#         'output_token_details': {'audio': 0, 'reasoning': 0}
#     },
#     'claude-haiku-4-5-20251001': {
#         'input_tokens': 8,
#         'output_tokens': 21,
#         'total_tokens': 29,
#         'input_token_details': {'cache_read': 0, 'cache_creation': 0}
#     }
# }
