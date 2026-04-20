"""03_dynamic_model_selection.py
Example: Dynamic model selection based on conversation context.
"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from llm_config import get_llm
from typing import Callable

# Define multiple models with different capabilities/costs
basic_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0.1)
advanced_model = ChatOpenAI(model="gpt-4.1", temperature=0.1)


@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])

    if message_count > 10:
        # Use an advanced model for longer conversations
        model = advanced_model
    else:
        model = basic_model

    return handler(request.override(model=model))


# Tools would be defined here
tools = []

agent = create_agent(
    model=basic_model,  # Default model
    tools=tools,
    middleware=[dynamic_model_selection]
)
