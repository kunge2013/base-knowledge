"""05_invoke_conversation_objects.py
Example: Invoke model with conversation history using message objects.
"""

from llm_config import default_llm
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Conversation history using typed message objects
conversation = [
    SystemMessage("You are a helpful assistant that translates English to French."),
    HumanMessage("Translate: I love programming."),
    AIMessage("J'adore la programmation."),
    HumanMessage("Translate: I love building applications.")
]

response = default_llm.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")
