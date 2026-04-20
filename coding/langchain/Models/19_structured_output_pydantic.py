"""19_structured_output_pydantic.py
Example: Structured output using Pydantic schema.
"""

from pydantic import BaseModel, Field
from llm_config import default_llm


class Movie(BaseModel):
    """A movie with details."""
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    director: str = Field(description="The director of the movie")
    rating: float = Field(description="The movie's rating out of 10")


# Get model configured to return structured output
model_with_structure = default_llm.with_structured_output(Movie)
response = model_with_structure.invoke("Provide details about the movie Inception")
print(response)  # Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8)
