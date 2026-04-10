"""20_structured_output_include_raw.py
Example: Structured output including raw AIMessage for metadata access.
"""

from pydantic import BaseModel, Field
from llm_config import default_llm


class Movie(BaseModel):
    """A movie with details."""
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    director: str = Field(description="The director of the movie")
    rating: float = Field(description="The movie's rating out of 10")


# Include raw AIMessage alongside parsed output
# Useful for accessing token counts and other metadata
model_with_structure = default_llm.with_structured_output(Movie, include_raw=True)
response = model_with_structure.invoke("Provide details about the movie Inception")

# Response contains both raw and parsed data
# {
#     "raw": AIMessage(...),
#     "parsed": Movie(title=..., year=..., ...),
#     "parsing_error": None,
# }
print(response)
