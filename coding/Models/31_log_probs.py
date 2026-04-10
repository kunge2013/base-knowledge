"""31_log_probs.py
Example: Getting token-level log probabilities from model.
"""

from langchain.chat_models import init_chat_model

# Enable log probabilities to get token likelihoods
model = init_chat_model(
    model="gpt-4.1",
    model_provider="openai"
).bind(logprobs=True)

response = model.invoke("Why do parrots talk?")
# Access log probabilities from response metadata
print(response.response_metadata["logprobs"])
