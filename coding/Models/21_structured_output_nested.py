"""21_structured_output_nested.py
Example: Nested schemas for structured output.
"""

from pydantic import BaseModel, Field
from llm_config import default_llm


class Actor(BaseModel):
    name: str
    role: str


class MovieDetails(BaseModel):
    title: str
    year: int
    cast: list[Actor]
    genres: list[str]
    budget: float | None = Field(None, description="Budget in millions USD")


# Structured output with nested schemas works automatically
model_with_structure = default_llm.with_structured_output(MovieDetails)
response = model_with_structure.invoke("Provide details for The Dark Knight")
print(response)
