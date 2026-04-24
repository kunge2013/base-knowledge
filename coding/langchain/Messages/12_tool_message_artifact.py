"""12_tool_message_artifact.py
Using ToolMessage with artifact field for storing supplementary data.
"""

from langchain.messages import ToolMessage

# Artifact example for retrieval tools
artifact = {"document_id": "doc_123", "page": 0}

# Sent to model
message_content = "It was the best of times, it was the worst of times."

# Artifact available downstream (not sent to model)
tool_message = ToolMessage(
    content=message_content,
    tool_call_id="call_123",
    name="search_books",
    artifact=artifact,
)

print(f"Message content (sent to model): {tool_message.content}")
print(f"Artifact (downstream only): {tool_message.artifact}")
print("\nThe artifact field stores supplementary data that won't be sent to the model")
print("but can be accessed programmatically for downstream processing.")
