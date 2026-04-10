"""12_structured_output_tool_strategy.py
Example: Structured output using ToolStrategy.
"""

from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool
from llm_config import default_llm


class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str


@tool
def search_tool(query: str) -> str:
    """Search for information."""
    return f"Search results: {query}"


agent = create_agent(
    model=default_llm,
    tools=[search_tool],
    response_format=ToolStrategy(ContactInfo)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

# Access structured response
structured_result = result["structured_response"]
print(structured_result)
# Output: ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
