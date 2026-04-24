"""12_structured_output_tool_strategy.py
Example: Structured output using ToolStrategy with with_structured_output helper.
"""

from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str


@tool
def search_tool(query: str) -> str:
    """Search for information."""
    return f"Search results: {query}"


# Use with_structured_output instead of ToolStrategy (works with thinking models)
llm = ChatOpenAI(
    model=os.getenv("model"),
    temperature=float(os.getenv("temperature") or 0.1),
    max_tokens=1000,
    timeout=30,
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL") if os.getenv("OPENAI_BASE_URL") else None,
).with_structured_output(ContactInfo)

result = llm.invoke("Extract contact info from: John Doe, john@example.com, (555) 123-4567. Respond with a json object.")

print(result)
# Output: ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
