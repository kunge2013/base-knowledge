"""04_dictionary_format.py
Using dictionary format for messages in OpenAI chat completions format.
"""

from llm_config import default_llm

# Initialize model
model = default_llm

# Specify messages directly in OpenAI chat completions format
messages = [
    {"role": "system", "content": "You are a poetry expert"},
    {"role": "user", "content": "Write a haiku about spring"},
    {"role": "assistant", "content": "Cherry blossoms bloom\nPink petals dance in breeze\nNature wakes from sleep"},
    {"role": "user", "content": "Now write one about winter"}
]
response = model.invoke(messages)

print(f"Response: {response.content}")
