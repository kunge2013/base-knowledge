"""26_reasoning_blocks.py
Example: Accessing reasoning content blocks from streaming.
"""

from llm_config import default_llm

# Surface reasoning steps when supported by the model
for chunk in default_llm.stream("Why do parrots have colorful feathers?"):
    reasoning_steps = [r for r in chunk.content_blocks if r["type"] == "reasoning"]
    print(reasoning_steps if reasoning_steps else chunk.text)
