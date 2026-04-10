"""25_multimodal_output.py
Example: Accessing multimodal content blocks from model response.
"""

from llm_config import default_llm

# Models that support multimodal output can return images
response = default_llm.invoke("Create a picture of a cat")
print(response.content_blocks)
# [
#     {"type": "text", "text": "Here's a picture of a cat"},
#     {"type": "image", "base64": "...", "mime_type": "image/jpeg"},
# ]
