"""36_configurable_tool_calling.py
Example: Configurable model with tool calling.
"""

from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model


class GetWeather(BaseModel):
    """Get the current weather in a given location"""
    location: str = Field(description="The city and state, e.g. San Francisco, CA")


class GetPopulation(BaseModel):
    """Get the current population in a given location"""
    location: str = Field(description="The city and state, e.g. San Francisco, CA")


# Create configurable model and bind tools
model = init_chat_model(temperature=0)
model_with_tools = model.bind_tools([GetWeather, GetPopulation])

# Run with different models at runtime
result_gpt = model_with_tools.invoke(
    "what's bigger in 2024 LA or NYC", config={"configurable": {"model": "gpt-4.1-mini"}}
).tool_calls
print(result_gpt)
# [
#     {
#         'name': 'GetPopulation',
#         'args': {'location': 'Los Angeles, CA'},
#         'id': 'call_Ga9m8FAArIyEjItHmztPYA22',
#         'type': 'tool_call'
#     },
#     {
#         'name': 'GetPopulation',
#         'args': {'location': 'New York, NY'},
#         'id': 'call_jh2dEvBaAHRaw5JUDthOs7rt',
#         'type': 'tool_call'
#     }
# ]

result_claude = model_with_tools.invoke(
    "what's bigger in 2024 LA or NYC",
    config={"configurable": {"model": "claude-sonnet-4-6"}},
).tool_calls
print(result_claude)
# [
#     {
#         'name': 'GetPopulation',
#         'args': {'location': 'Los Angeles, CA'},
#         'id': 'toolu_01JMufPf4F4t2zLj7miFeqXp',
#         'type': 'tool_call'
#     },
#     {
#         'name': 'GetPopulation',
#         'args': {'location': 'New York City, NY'},
#         'id': 'toolu_01RQBHcE8kEEbYTuuS8WqY1u',
#         'type': 'tool_call'
#     }
# ]
