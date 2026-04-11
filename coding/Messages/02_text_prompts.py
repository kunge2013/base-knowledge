"""02_text_prompts.py
Using text prompts for simple generation tasks.
"""

from llm_config import default_llm

# Initialize model
model = default_llm

# Use text prompt for simple generation
response = model.invoke("Write a haiku about spring")

print(f"Response: {response.content}")

print("\n--- Use text prompts when: ---")
print("- You have a single, standalone request")
print("- You don't need conversation history")
print("- You want minimal code complexity")
