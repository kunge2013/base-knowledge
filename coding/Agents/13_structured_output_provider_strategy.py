"""13_structured_output_provider_strategy.py
Example: Structured output using ProviderStrategy.
"""

from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from llm_config import get_llm
from langchain_openai import ChatOpenAI


class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str


# ProviderStrategy uses model provider's native structured output
model = get_llm(model_name="gpt-4.1")
agent = create_agent(
    model=model,
    response_format=ProviderStrategy(ContactInfo)
)

# As of langchain 1.0, you can also just pass the schema directly
# and it will default to ProviderStrategy if supported:
# agent = create_agent(model=model, response_format=ContactInfo)
