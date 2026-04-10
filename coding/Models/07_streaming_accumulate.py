"""07_streaming_accumulate.py
Example: Accumulating streaming chunks into a complete message.
"""

from llm_config import default_llm

# Accumulate chunks incrementally
full = None  # None | AIMessageChunk
for chunk in default_llm.stream("What color is the sky?"):
    full = chunk if full is None else full + chunk
    print(full.text)

# After accumulation, access content blocks
print(full.content_blocks)
# [{"type": "text", "text": "The sky is typically blue..."}]
