"""11_batch_as_completed.py
Example: Streaming batch results as they complete.
"""

from llm_config import default_llm

# Stream results as they complete (out-of-order processing)
# Results may arrive out of order, each includes input index
for response in default_llm.batch_as_completed([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
]):
    print(response)
