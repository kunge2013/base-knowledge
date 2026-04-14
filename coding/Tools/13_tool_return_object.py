"""13_tool_return_object.py
Tool that returns an object for structured results.
"""

from langchain.tools import tool

@tool
def get_weather_data(city: str) -> dict:
    """Get structured weather data for a city."""
    return {
        "city": city,
        "temperature_c": 22,
        "conditions": "sunny",
    }

# Use tool
result = get_weather_data.invoke({"city": "Shanghai"})
print(f"Tool result: {result}")
print(f"Result type: {type(result)}")
print(f"Temperature: {result['temperature_c']}")