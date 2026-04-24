"""09_token_usage.py
Using AIMessage to access token usage metadata.
"""

from llm_config import default_llm



# Initialize model
model = default_llm

# Make a request
response = model.invoke("Hello!")

print(f"Response: {response.content}\n")

# Check token usage
if response.usage_metadata:
    print("Token usage:")
    print(f"  Input tokens: {response.usage_metadata.get('input_tokens', 'N/A')}")
    print(f"  Output tokens: {response.usage_metadata.get('output_tokens', 'N/A')}")
    print(f"  Total tokens: {response.usage_metadata.get('total_tokens', 'N/A')}")
else:
    print("Token usage metadata not available")
