"""04_invoke_conversation_dict.py
Example: Invoke model with conversation history using dictionary format.
"""

from llm_config import default_llm

# Conversation history as list of dictionaries
conversation = [
    {"role": "system", "content": "You are a helpful assistant that translates English to French."},
    {"role": "user", "content": "Translate: I love programming."},
    {"role": "assistant", "content": "J'adore la programmation."},
    {"role": "user", "content": "Translate: I love building applications."}
]

response = default_llm.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")
