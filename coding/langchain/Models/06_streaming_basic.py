"""06_streaming_basic.py
Example: Basic streaming of model output.
"""

from llm_config import default_llm

# Stream output token by token
for chunk in default_llm.stream("Why do parrots have colorful feathers?"):
    print(chunk.text, end="|", flush=True)
