"""10_streaming.py
Streaming responses using AIMessageChunk.
"""

from llm_config import default_llm

# Initialize model
model = default_llm

# Stream the response
chunks = []
full_message = None

print("Streaming response:")
for chunk in model.stream("Tell me a short joke"):
    chunks.append(chunk)
    print(chunk.text, end="", flush=True)
    full_message = chunk if full_message is None else full_message + chunk

print("\n\n--- Full message type:", type(full_message))
print("Total chunks:", len(chunks))
